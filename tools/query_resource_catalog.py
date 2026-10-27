"""查询用户提供的 ASER 名册、别名与差分；不读取或修改本地游戏资源。"""

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIGS = ROOT / "resource-catalog/Configs"
KINDS = ("characterTachies", "characterDynamics", "backgrounds", "musics", "soundEffects", "visualEffects")
CHARACTER_CONFIGS = {"characterTachies": "characterTachieOfficialConfigs", "characterDynamics": "characterSpineOfficialConfigs"}
FILES = {
    "collections": "officialAssets_collections.json",
    "aliases": "officialAssets_aliases.json",
    "user_configs": "officialAssets_userConfigs.json",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSON 键重复：{key}")
        result[key] = value
    return result


def load_catalog(configs=DEFAULT_CONFIGS):
    data = {}
    for section, name in FILES.items():
        value = json.loads((Path(configs) / name).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
        if not isinstance(value, dict):
            raise ValueError(f"{name} 的顶层必须是对象")
        expected = set(CHARACTER_CONFIGS.values()) if section == "user_configs" else set(KINDS)
        if set(value) != expected:
            raise ValueError(f"{name} 的类别发生变化：缺少 {sorted(expected-set(value))}，新增 {sorted(set(value)-expected)}")
        for kind, entries in value.items():
            if not isinstance(entries, dict):
                raise ValueError(f"{name}/{kind} 必须是对象")
            for key, item in entries.items():
                if not key:
                    raise ValueError(f"{name}/{kind} 存在空资源名")
                if section != "user_configs":
                    if not isinstance(item, str) or not item:
                        raise ValueError(f"{name}/{kind}/{key} 必须是非空字符串")
                elif not isinstance(item, dict) or not isinstance(item.get("variationNames", {}), dict):
                    raise ValueError(f"{name}/{kind}/{key} 的差分配置无效")
                elif any(not k or not isinstance(v, str) or not v for k, v in item.get("variationNames", {}).items()):
                    raise ValueError(f"{name}/{kind}/{key} 的差分名称无效")
        data[section] = value
    return data


def character_config(catalog, kind, raw_name):
    section = CHARACTER_CONFIGS.get(kind)
    return catalog["user_configs"][section].get(raw_name) if section else None


def query_resources(catalog, query, kind=None, exact=False):
    results = []
    for category in (kind,) if kind else KINDS:
        for raw_name, bundle in catalog["collections"][category].items():
            alias = catalog["aliases"][category].get(raw_name)
            names = {"raw_name": raw_name, "alias": alias}
            matches = [key for key, value in names.items() if value is not None and (value == query if exact else query.casefold() in value.casefold())]
            if not matches:
                continue
            config = character_config(catalog, category, raw_name)
            results.append({
                "kind": category, "raw_name": raw_name, "alias": alias,
                "asset_bundle": bundle, "matched_by": matches,
                "character_config": config,
            })
    return sorted(results, key=lambda entry: (entry["kind"], entry["alias"] or entry["raw_name"], entry["raw_name"]))


def audit_catalog(catalog):
    counts, stale_aliases, stale_configs, collisions, variation_collisions = {}, [], [], [], []
    for kind in KINDS:
        entries = catalog["collections"][kind]
        aliases = catalog["aliases"][kind]
        configs = catalog["user_configs"].get(CHARACTER_CONFIGS.get(kind), {})
        counts[kind] = {"resources": len(entries), "aliases": len(aliases), "character_configs": len(configs)}
        stale_aliases.extend({"kind": kind, "raw_name": key, "alias": value} for key, value in aliases.items() if key not in entries)
        stale_configs.extend({"kind": kind, "raw_name": key} for key in configs if key not in entries)
        by_name = defaultdict(set)
        for raw_name in entries:
            by_name[raw_name].add(raw_name)
            if raw_name in aliases:
                by_name[aliases[raw_name]].add(raw_name)
        collisions.extend({"kind": kind, "name": name, "raw_names": sorted(raws)} for name, raws in sorted(by_name.items()) if len(raws) > 1)
        for raw_name, config in configs.items():
            by_variation = defaultdict(set)
            for raw, display in config.get("variationNames", {}).items():
                by_variation[raw].add(raw)
                by_variation[display].add(raw)
            variation_collisions.extend({"kind": kind, "raw_name": raw_name, "name": name, "raw_variations": sorted(raws)} for name, raws in sorted(by_variation.items()) if len(raws) > 1)
    return {
        "scope": "用户上传名册中的名称映射；未验证游戏文件加载，也不推断 ASER 的同名解析优先级。",
        "counts": counts, "resource_count": sum(item["resources"] for item in counts.values()),
        "alias_count": sum(item["aliases"] for item in counts.values()),
        "character_config_count": sum(item["character_configs"] for item in counts.values()),
        "aliases_missing_from_collections": stale_aliases,
        "configs_missing_from_collections": stale_configs,
        "name_collisions": collisions, "variation_name_collisions": variation_collisions,
    }


def compare_catalogs(current, candidate):
    differences = {}
    for section in FILES:
        differences[section] = {}
        for kind, old in current[section].items():
            new = candidate[section][kind]
            differences[section][kind] = {
                "added": {key: new[key] for key in sorted(new.keys() - old.keys())},
                "removed": {key: old[key] for key in sorted(old.keys() - new.keys())},
                "changed": {key: {"before": old[key], "after": new[key]} for key in sorted(old.keys() & new.keys()) if old[key] != new[key]},
            }
    return differences


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", help="查询原始资源名或别名；默认匹配子串")
    parser.add_argument("--configs", type=Path, default=DEFAULT_CONFIGS, help="完整的三份配置所在目录")
    parser.add_argument("--kind", choices=KINDS)
    parser.add_argument("--exact", action="store_true", help="精确匹配，保留大小写；不自动选择同名结果")
    parser.add_argument("--compare", type=Path, help="与新版 Configs 比较，不覆盖任何文件")
    args = parser.parse_args()
    if args.query is not None and args.compare is not None:
        parser.error("查询和新版比较请分别执行")
    if args.query is None and (args.kind or args.exact):
        parser.error("--kind 和 --exact 需要查询词")
    try:
        catalog = load_catalog(args.configs)
        if args.compare:
            output = {"differences": compare_catalogs(catalog, load_catalog(args.compare))}
        elif args.query is not None:
            matches = query_resources(catalog, args.query, args.kind, args.exact)
            output = {"query": args.query, "match_count": len(matches), "matches": matches}
        else:
            output = audit_catalog(catalog)
    except (OSError, ValueError) as error:
        print(f"名册读取失败：{error}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if args.query is not None and not matches else 0


if __name__ == "__main__":
    raise SystemExit(main())
