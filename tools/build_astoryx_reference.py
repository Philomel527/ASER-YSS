"""从固定版本的上游规则和中文说明生成控制器参数参考；不生成剧情。"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "vendor/YayinStoryStudio/src/Plugin_ASERStudio/resource/cn.yxgeneral.aserstudio"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def code(value) -> str:
    text = cell(value if value is not None else "无行首标识")
    if "`" in text:
        return "`` " + text + " ``"
    return "`" + text + "`"


def main() -> None:
    manifest = load(ROOT / "docs/yss-source-manifest.json")
    advanced = load(RESOURCE / "template/3.6.7/Rules/AdvanceRule.json")["rules"]
    basic = {rule["Key"]: rule["Value"] for rule in load(
        RESOURCE / "template/3.6.7/Rules/BaseRule.json"
    )["rules"]}
    meta = load(RESOURCE / "astoryxMeta/default.json")
    chinese = load(RESOURCE / "i18n/zh_CN.json")
    lines = [
        "# AStoryX 控制器参数参考", "",
        f"来源提交：`{manifest['commit']}`。规则来自上游 `template/3.6.7/Rules/`，类型、默认值和约束来自 `astoryxMeta/default.json`，说明来自 `i18n/zh_CN.json`。", "",
        "由 `python3 tools/build_astoryx_reference.py` 生成。这里记录的是源码内的规则和元数据；不是已经通过 ASER 播放测试的运行时保证。实际 ASER 版本及项目自定义规则优先。", "",
        "`BaseRule` 依靠位置和前缀，`AdvanceRule` 的大多数参数使用具名的 `,@参数名=` 前缀。变量赋值仍使用 `=`，必须以每一行表中的前缀为准。", "",
    ]
    for entry in advanced:
        key, rule = entry["Key"], entry["Value"]
        basic_rule = basic[key]
        description = chinese["document"][key]
        lines.extend([
            f"## {chinese['controller'][key]} / {key}", "",
            description["__description"], "",
            f"行首：{code(rule['header'])}；主要参数：{code(rule['requiredParametersName'])}；主要参数内分隔符：{code(rule['requiredParametersSeparator'])}。", "",
            "| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ])
        required = rule["requiredParametersName"]
        if [item["parameterName"] for item in basic_rule["optionalParameters"]] != [
            item["parameterName"] for item in rule["optionalParameters"]
        ]:
            raise ValueError(f"{key} 两套规则的参数次序已变化，需要重新核对")
        parameters = [(required, "主要参数", "主要参数")]
        parameters.extend((parameter["parameterName"], old["prefix"], parameter["prefix"])
                          for old, parameter in zip(
                              basic_rule["optionalParameters"], rule["optionalParameters"], strict=True))
        for name, basic_prefix, advanced_prefix in parameters:
            item = meta[key][name]
            constraints = {k: v for k, v in item.items() if k not in ("type", "defaultValue")}
            lines.append("| " + " | ".join([
                code(name), cell(item["type"]), code(json.dumps(item["defaultValue"], ensure_ascii=False)),
                code(json.dumps(constraints, ensure_ascii=False)) if constraints else "—",
                code(basic_prefix), code(advanced_prefix), cell(description.get(name, "")),
            ]) + " |")
        lines.append("")
    lines.extend(["## 共享枚举", ""])
    for name, values in meta["__GeneralMetaData__"].items():
        lines.extend([f"{code(name)}：" + "、".join(code(value) for value in values), ""])
    output = ROOT / "docs/astoryx-controller-reference.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"已从规则生成 {len(advanced)} 类控制器参考：{output}")


if __name__ == "__main__":
    main()
