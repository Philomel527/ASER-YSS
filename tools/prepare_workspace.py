"""创建剧情代码专用目录；不生成占位文件，不改动已有内容。"""

from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    destination = root / "story-code"
    destination.mkdir(exist_ok=True)
    print(f"剧情代码目录：{destination}")


if __name__ == "__main__":
    main()
