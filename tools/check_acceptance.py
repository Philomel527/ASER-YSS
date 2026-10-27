"""依据固定规则静态检查验收剧情和素材；不冒充 ASER 播放引擎。"""

from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "build/ASER_YSS_Acceptance"
RESOURCE = ROOT / "vendor/YayinStoryStudio/src/Plugin_ASERStudio/resource/cn.yxgeneral.aserstudio"
META = json.loads((RESOURCE / "astoryxMeta/default.json").read_text())
PLAN = json.loads((ROOT / "docs/acceptance-plan.json").read_text())
PROBES = set(PLAN["compatibility_probes"])


def protect(text):
    values = {}
    def replace(match):
        key = "◆PROTECT" + str(len(values)) + "◆"
        values[key] = match.group()[2:-1]
        return key
    protected = re.sub(r"&\{.*?\}", replace, text)
    if "&{" in protected:
        raise ValueError("未闭合的保护文段")
    def restore(value):
        for key, original in values.items():
            value = value.replace(key, original)
        return value
    return protected, restore


def expand(lines):
    macros, output, aliases = {}, [], {}
    in_aliases = False
    index = 3

    def call(line, source_line, stack=()):
        if not line.startswith("#use "):
            if "$(" in line:
                raise ValueError(f"第 {source_line} 行存在未替换的块参数")
            return [(source_line, line)]
        match = re.fullmatch(r"#use ([^(]+)\((.*)\)", line)
        if not match or match[1] not in macros:
            raise ValueError(f"第 {source_line} 行的块调用无效")
        name = match[1]
        if name in stack or len(stack) >= 16:
            raise ValueError(f"第 {source_line} 行的块调用存在递归循环")
        names, body = macros[name]
        values = match[2].split(",") if match[2] else []
        if len(names) != len(values):
            raise ValueError(f"第 {source_line} 行的块参数个数错误")
        result = []
        for original in body:
            replaced = original
            for parameter, value in zip(names, values, strict=True):
                replaced = replaced.replace("$(" + parameter + ")", value)
            result.extend(call(replaced, source_line, stack + (name,)))
        return result

    while index < len(lines):
        line, number = lines[index], index + 1
        index += 1
        if not line.strip() or line.startswith("//"):
            continue
        if line == "#aliases":
            if in_aliases:
                raise ValueError("别名区域嵌套")
            in_aliases = True
            continue
        if line == "#endaliases":
            if not in_aliases:
                raise ValueError("孤立的别名结束标记")
            in_aliases = False
            continue
        if in_aliases:
            parts = line.split("->")
            if len(parts) != 2 or not parts[0] or not parts[1]:
                raise ValueError(f"第 {number} 行别名无效")
            aliases[parts[0]] = parts[1].split("/")
            continue
        if line.startswith("#block "):
            match = re.fullmatch(r"#block ([^(]+)\((.*)\)", line)
            if not match or match[1] in macros:
                raise ValueError(f"第 {number} 行块定义错误或重名")
            body = []
            while index < len(lines) and lines[index] != "#endblock":
                if lines[index].startswith("#block "):
                    raise ValueError("不使用嵌套块定义")
                if lines[index].strip() and not lines[index].startswith("//"):
                    body.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError("块没有闭合")
            index += 1
            macros[match[1]] = (match[2].split(",") if match[2] else [], body)
            continue
        if line.startswith("#") and not line.startswith("#use "):
            raise ValueError(f"第 {number} 行存在未知／错位的预处理器")
        output.extend(call(line, number))
    if in_aliases:
        raise ValueError("别名区域没有闭合")
    return output, aliases, macros


def parse_controller(line, rule):
    kind = "Dialog"
    for name, item in sorted(rule.items(), key=lambda pair: len(pair[1]["header"] or ""), reverse=True):
        if item["header"] and line.startswith(item["header"]):
            kind = name
            break
    spec = rule[kind]
    body, restore = protect(line[len(spec["header"] or ""):])
    optional = spec["optionalParameters"]
    options = {}
    if kind == "Variable":
        pieces = body.split("=", 1)
        required = pieces[0]
        if len(pieces) == 2:
            options["Expression"] = pieces[1]
    elif optional and all(item["prefix"] == "/" for item in optional):
        pieces = body.split("/")
        if len(pieces) > len(optional) + 1:
            raise ValueError(f"{kind} 的位置参数过多或正文斜杠未保护")
        required = pieces[0]
        for item, value in zip(optional, pieces[1:]):
            if value:
                options[item["parameterName"]] = value
    elif all(item["prefix"].startswith(",@") for item in optional):
        matches = list(re.finditer(r",@([A-Za-z][A-Za-z0-9_]*)=", body))
        required = body[:matches[0].start()] if matches else body
        allowed = {item["parameterName"] for item in optional}
        for position, match in enumerate(matches):
            name = match[1]
            if name not in allowed:
                raise ValueError(f"{kind} 没有参数 {name}")
            if name in options:
                raise ValueError(f"{kind} 参数 {name} 重复")
            end = matches[position + 1].start() if position + 1 < len(matches) else len(body)
            options[name] = body[match.end():end]
    else:
        raise ValueError(f"本检查器未实现该规则的混合前缀：{kind}")
    if not required.strip():
        raise ValueError(f"{kind} 缺少主要参数")
    return kind, restore(required), {name: restore(value) for name, value in options.items()}


def check_value(kind, name, value, file, warnings):
    item = META[kind][name]
    value_type = item["type"]
    if value_type == "String":
        return
    if value_type == "Bool":
        if value not in {"true", "false", "1", "0"}:
            raise ValueError(f"{kind}.{name} 布尔值无效：{value}")
        return
    if value_type == "Enum":
        values = value.split(",")
        allowed = META["__GeneralMetaData__"][item["enums"]]
        if any(part not in allowed for part in values):
            raise ValueError(f"{kind}.{name} 枚举不存在：{value}")
        dimensions = item.get("dimensions", [1])
        if len(values) not in dimensions:
            if file in PROBES and kind == "Character" and name == "MoveCurve" and len(values) in {2, 4}:
                warnings.append("语雀描述该曲线维数，但固定 YSS 元数据不接受；留待目标播放器验收")
            else:
                raise ValueError(f"{kind}.{name} 维数不符合元数据：{value}")
        return
    if value_type == "Integer":
        if not re.fullmatch(r"[+-]?\d+", value):
            raise ValueError(f"{kind}.{name} 不是整数")
        number = int(value)
    elif value_type == "Float":
        number = float(value)
    elif value_type == "Vector":
        numbers = [float(part) for part in value.split(",")]
        if not all(math.isfinite(part) for part in numbers):
            raise ValueError(f"{kind}.{name} 包含非有限数")
        if len(numbers) not in item.get("dimensions", [3]):
            raise ValueError(f"{kind}.{name} 向量维数错误：{value}")
        return
    else:
        raise ValueError(f"尚未支持的元数据类型：{value_type}")
    if not math.isfinite(number):
        raise ValueError(f"{kind}.{name} 包含非有限数")
    if number < item.get("min", -math.inf) or number > item.get("max", math.inf):
        raise ValueError(f"{kind}.{name} 超出限制")
    if "range" in item and not item["range"][0] <= number <= item["range"][1]:
        raise ValueError(f"{kind}.{name} 超出范围")


def check_asset(kind, required, file, warnings):
    resources = PROJECT / "Resources"
    if kind == "Background":
        for name in required.split("+"):
            if name not in {"无", "none"} and not (resources / "Background" / (name + ".png")).is_file():
                raise ValueError(f"背景不存在：{name}")
    elif kind == "Music":
        if required in {"无", "none"}:
            return
        if required == "null" and file == "08_music_null.astoryx":
            warnings.append("null 为上游示例出现的兼容性停止标记，尚未运行验证")
            return
        folder = resources / "Music"
        if not ((folder / (required + ".wav")).is_file() or all((folder / (required + suffix + ".wav")).is_file() for suffix in ["_intro", "_loop"])):
            raise ValueError(f"音乐不存在：{required}")
    elif kind == "SoundEffect":
        if not (resources / "SoundEffect" / (required + ".wav")).is_file():
            raise ValueError(f"音效不存在：{required}")
    elif kind in {"Character", "Interlude"}:
        if required in {"无", "none"}:
            return
        if ":" not in required:
            raise ValueError("角色没有以冒号指定差分")
        name, variation = required.split(":", 1)
        picture = resources / "Char_Picture" / name / (name + "_config.json")
        spine = resources / "Char_Spine" / name / (name + "_config.json")
        if picture.is_file():
            config = json.loads(picture.read_text())
            if variation not in config["variations"]:
                raise ValueError(f"角色差分不存在：{required}")
        elif spine.is_file():
            config = json.loads(spine.read_text())
            if ";" in variation:
                skin, variation = variation.split(";", 1)
                if skin != "default":
                    raise ValueError(f"未经骨架核实的皮肤：{skin}")
            if variation not in config["animationConfigs"]:
                raise ValueError(f"Spine 差分不存在：{required}")
        else:
            raise ValueError(f"角色不存在：{name}")
    elif kind == "VisualEffect":
        folder = resources / "VisualEffect"
        manifest = json.loads((folder / "manifest.json").read_text())
        if required not in manifest:
            raise ValueError(f"特效不存在：{required}")
        item = manifest[required]
        for path in [item["bundlePath"], *item["dependencies"]]:
            if not (folder / path).is_file():
                raise ValueError(f"特效依赖不存在：{path}")
    elif kind == "Filter":
        parts = required.split(":")
        if len(parts) != 2 or parts[0] not in {"0", "1", "2", "3"}:
            raise ValueError("滤镜类型或强度格式不符")
        float(parts[1])


def check_story(file, text=None):
    path = ROOT / "story-code" / file
    raw = path.read_bytes() if text is None else text.encode()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("源文件含 BOM")
    text = raw.decode("utf-8")
    if "\\t" in text:
        raise ValueError("使用了字面量反斜杠 t，而非真正 Tab")
    lines = text.splitlines()
    if len(lines) < 3 or lines[1] not in {"#useRule:BaseRule", "#useRule:AdvanceRule"} or lines[2] != "#version:2":
        raise ValueError("简介、第二行规则、第三行版本格式错误")
    rule_name = lines[1].split(":", 1)[1]
    rule = {entry["Key"]: entry["Value"] for entry in json.loads((PROJECT / "Rules" / (rule_name + ".json")).read_text())["rules"]}
    expanded, aliases, macros = expand(lines)
    counts, parameters, warnings = Counter(), defaultdict(set), []
    labels, branches, variables, references, curves = set(), [], set(), set(), set()
    for number, line in expanded:
        try:
            kind, required, options = parse_controller(line, rule)
            counts[kind] += 1
            parameters[kind].add(rule[kind]["requiredParametersName"])
            parameters[kind].update(options)
            for name, value in options.items():
                check_value(kind, name, value, file, warnings)
            check_value(kind, rule[kind]["requiredParametersName"], required, file, warnings)
            check_asset(kind, required, file, warnings)
            if kind == "Sign":
                if required in labels:
                    raise ValueError(f"标记重名：{required}")
                labels.add(required)
            if kind == "Branch":
                branches.extend(options.get("Branches", "").split(","))
                if required != "_":
                    references.add(required)
            if kind in {"Variable", "Judge"}:
                variables.add(required)
            if kind == "Choice":
                variables.add(options.get("OutputVariable", "choice"))
            references.update(re.findall(r"\$\[([^\]]+)\]", line))
            if "MoveCurve" in options:
                curves.update(options["MoveCurve"].split(","))
        except (ValueError, KeyError) as error:
            raise ValueError(f"{file}:{number}: {error}") from error
    if set(branches) - labels:
        raise ValueError(f"分支落点不存在：{set(branches) - labels}")
    if references - variables:
        raise ValueError(f"引用了未在验收脚本赋值的变量：{references - variables}")
    expected = {key: {value["requiredParametersName"], *(p["parameterName"] for p in value["optionalParameters"])} for key, value in rule.items()}
    missing = {key: sorted(values - parameters[key]) for key, values in expected.items() if values - parameters[key]}
    return {
        "file": file, "rule": rule_name, "source_lines": len(lines),
        "validation_status": "structural_check_done_runtime_pending" if file in PROBES else "core_static_check_passed",
        "expanded_controllers": dict(sorted(counts.items())), "macro_count": len(macros),
        "alias_count": len(aliases), "actual_tab_count": text.count("\t"),
        "explicit_parameter_count": sum(map(len, parameters.values())),
        "missing_parameters": missing, "curve_names": sorted(curves),
        "compatibility_notes": sorted(set(warnings)),
    }


def main():
    results, errors = [], []
    for item in PLAN["stories"]:
        try:
            results.append(check_story(item["file"]))
        except (ValueError, KeyError, OSError) as error:
            errors.append(str(error))
    for file in [PLAN["main_story"], "01_base_rule.astoryx"]:
        result = next((item for item in results if item["file"] == file), None)
        if result and result["missing_parameters"]:
            errors.append(file + " 未覆盖的参数：" + json.dumps(result["missing_parameters"], ensure_ascii=False))
    all_curves = set().union(*(set(item["curve_names"]) for item in results))
    if set(PLAN["expected_curve_names"]) - all_curves:
        errors.append("运动曲线未覆盖完整")
    report = {
        "status": "core_static_passed_probes_pending" if not errors else "failed",
        "core_static_status": "passed" if not errors else "failed",
        "compatibility_probe_status": "awaiting_local_playback",
        "scope": "Own static checker using pinned rules, metadata and packaged resources; not the upstream parser or ASER runtime.",
        "windows_runtime": "not_run", "stories": results, "errors": errors,
        "source_sha256": {item["file"]: hashlib.sha256((ROOT / "story-code" / item["file"]).read_bytes()).hexdigest() for item in PLAN["stories"]},
    }
    (ROOT / "docs/acceptance-static-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for result in results:
        print(result["file"], "控制器类型", len(result["expanded_controllers"]), "显式参数", result["explicit_parameter_count"])
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    print("静态检查：", report["status"], "；Windows 播放：未运行")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
