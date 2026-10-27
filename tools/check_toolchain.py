"""核对导入的 YSS 或 ASER 文件；比较新版目录时只报告差异，不覆盖文件。"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = {
    "yss": ROOT / "docs/yss-source-manifest.json",
    "aser": ROOT / "docs/aser-source-manifest.json",
}


def inventory(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        raise ValueError(f"目录不存在：{directory}")
    files = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"目录中包含链接，未继续检查：{path}")
        if path.is_file():
            with path.open("rb") as stream:
                files[path.relative_to(directory).as_posix()] = hashlib.file_digest(
                    stream, "sha256"
                ).hexdigest()
    return files


def compare(expected: dict[str, str], current: dict[str, str]) -> dict:
    return {
        "added": sorted(current.keys() - expected.keys()),
        "removed": sorted(expected.keys() - current.keys()),
        "changed": sorted(
            name for name in expected.keys() & current.keys()
            if expected[name] != current[name]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=MANIFESTS, default="yss", help="选择要核对的工具，默认 yss")
    parser.add_argument(
        "--candidate", type=Path,
        help="对比另一份完整解压目录；仅报告新增、删除、改动，不自动更新清单",
    )
    args = parser.parse_args()
    try:
        manifest = json.loads(MANIFESTS[args.tool].read_text(encoding="utf-8"))
        expected = {item["path"]: item["sha256"] for item in manifest["files"]}
        directory = args.candidate if args.candidate is not None else ROOT / manifest["directory"]
        current = inventory(directory)
        differences = compare(expected, current)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"检查失败：{error}\n")
    print(json.dumps({
        "tool": args.tool,
        **({"baseline_commit": manifest["commit"]} if args.tool == "yss" else {
            "baseline_version": manifest["application_version"]
        }),
        "checked_files": len(current),
        **differences,
    }, ensure_ascii=False, indent=2))
    if args.candidate is not None:
        return 0
    return int(any(differences.values()))


if __name__ == "__main__":
    raise SystemExit(main())
