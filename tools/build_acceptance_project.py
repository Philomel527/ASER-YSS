"""把已编写的验收剧情、规则和自带素材打包成可独立打开的 ASER 项目。"""

import hashlib
import json
import math
from pathlib import Path
import shutil
import struct
import wave
import zipfile
import zlib


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "vendor/YayinStoryStudio/src/Plugin_ASERStudio/resource/cn.yxgeneral.aserstudio/template/3.6.7"
PROJECT = ROOT / "build/ASER_YSS_Acceptance"
ARTIFACT = ROOT / "artifacts/ASER_YSS_acceptance.zip"


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def png_tile(path: Path, letter: str, color: tuple[int, int, int]) -> None:
    """创建全新的校准图，不裁切或修改第三方图片。"""
    width, height = 960, 540
    glyphs = {
        "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
        "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
        "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    }
    rows = bytearray()
    glyph = glyphs[letter]
    scale, left, top = 32, 400, 158
    for y in range(height):
        rows.append(0)
        for x in range(width):
            pixel = color
            if x % 120 < 2 or y % 90 < 2:
                pixel = tuple(min(255, component + 35) for component in color)
            if min(x, y, width - x - 1, height - y - 1) < 10:
                pixel = (240, 240, 240)
            gx, gy = (x - left) // scale, (y - top) // scale
            if 0 <= gx < 5 and 0 <= gy < 7 and glyph[gy][gx] == "1":
                pixel = (255, 255, 255)
            rows.extend(pixel)

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(rows), level=9))
        + chunk(b"IEND", b"")
    )


def tone(path: Path, notes: list[tuple[float, float]], rate: int = 24000) -> None:
    """生成已知时长的 PCM 检测音；不冒充人声配音。"""
    frames = bytearray()
    for frequency, duration in notes:
        count = round(rate * duration)
        ramp = min(round(rate * 0.015), count // 2)
        for index in range(count):
            envelope = min(1.0, index / max(1, ramp), (count - 1 - index) / max(1, ramp))
            value = 0 if frequency == 0 else round(6500 * envelope * math.sin(2 * math.pi * frequency * index / rate))
            frames.extend(struct.pack("<h", value))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as output:
        output.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        output.writeframes(frames)


def main() -> None:
    plan = json.loads((ROOT / "docs/acceptance-plan.json").read_text())
    # 只清理本脚本专用的已忽略构建目录，不触碰剧情源文件及用户的其他项目。
    if PROJECT.exists():
        assert PROJECT.resolve() == ROOT / "build/ASER_YSS_Acceptance"
        shutil.rmtree(PROJECT)
    PROJECT.mkdir(parents=True)
    for folder in ["Configs", "Resources/Background", "Rules", "Stories"]:
        (PROJECT / folder).mkdir(parents=True, exist_ok=True)

    for name in ["BaseRule.json", "AdvanceRule.json"]:
        copy_file(TEMPLATE / "Rules" / name, PROJECT / "Rules" / name)
    copy_file(TEMPLATE / "Resources/Background/bg_amb2026.png", PROJECT / "Resources/Background/bg_amb2026.png")
    copy_file(TEMPLATE / "Resources/Background/bg_amb2026.png", PROJECT / "cover.png")
    shutil.copytree(TEMPLATE / "Resources/Char_Picture", PROJECT / "Resources/Char_Picture")
    spine = TEMPLATE / "Resources/Char_Spine/Amiya(furnace_finale)"
    for source in spine.iterdir():
        copy_file(source, PROJECT / "Resources/Char_Spine/阿米娅(furnace_finale)" / source.name.replace("Amiya(furnace_finale)", "阿米娅(furnace_finale)"))
    shutil.copytree(TEMPLATE / "Resources/VisualEffect", PROJECT / "Resources/VisualEffect")
    copy_file(TEMPLATE / "Configs/override_userConfigs.json", PROJECT / "Configs/override_userConfigs.json")
    aliases = {name: {} for name in ["characterTachies", "backgrounds", "musics", "soundEffects", "visualEffects", "characterDynamics"]}
    (PROJECT / "Configs/override_aliases.json").write_text(json.dumps(aliases, ensure_ascii=False, indent=2) + "\n")

    for letter, color in zip("ABCD", [(40, 82, 130), (135, 70, 50), (45, 115, 78), (100, 65, 125)], strict=True):
        png_tile(PROJECT / f"Resources/Background/grid_{letter}.png", letter, color)
    music = PROJECT / "Resources/Music"
    tone(music / "验收序曲_intro.wav", [(261.63, 0.25), (329.63, 0.25), (392, 0.25), (523.25, 0.25)])
    tone(music / "验收序曲_loop.wav", [(330, 0.3), (0, 0.2), (440, 0.3), (0, 0.2)])
    tone(music / "验收右声道.wav", [(660, 0.3), (0, 0.7)])
    sound = PROJECT / "Resources/SoundEffect"
    tone(sound / "验收短音.wav", [(880, 0.16), (0, 0.24)])
    tone(sound / "验收配音标记.wav", [(440, 0.2), (0, 0.8)] * 3)

    for item in plan["stories"]:
        copy_file(ROOT / "story-code" / item["file"], PROJECT / "Stories" / item["file"])
    opened = "./Stories/" + plan["main_story"]
    project_config = {
        "Project": {
            "Name": "ASER YSS 全功能验收",
            "Description": "21 类控制器、全参数、两套规则及独立兼容性探针；尚未在 Windows 播放验证。",
            "IconPath": "./cover.png", "Version": "0.2", "Author": "",
            "DebugServerID": "cn.yxgeneral.aserstudio.astoryxdebugger",
            "CreateTime": "2026-10-27 00:00:00", "LastModifyTime": "2026-10-27 00:00:00",
            "RequiredPlugins": ["cn.yxgeneral.aserstudio"],
        },
        "Editor": {"OpenedFiles": {"0": opened}, "FocusedFile": opened},
        # JsonConfig 使用点分路径保存插件 ID；这里与 YSSProject::saveProjectConfigForPlugin 一致。
        "MetaData": {"cn": {"yxgeneral": {"aserstudio": {"ASERVersion": "3.7.12"}}}},
    }
    (PROJECT / "project.yssp").write_text(json.dumps(project_config, ensure_ascii=False, indent=2) + "\n")
    copy_file(ROOT / "docs/acceptance-checklist.md", PROJECT / "验收说明.md")
    copy_file(ROOT / "docs/acceptance-plan.json", PROJECT / "acceptance-plan.json")
    copy_file(ROOT / "vendor/YayinStoryStudio/LICENSE.txt", PROJECT / "YSS_UPSTREAM_LICENSE.txt")
    (PROJECT / "素材来源.md").write_text(
        "背景、Mon3tr、阿米娅 Spine 与特效来自用户指定的 YayinStoryStudio "
        "49e2528c42809779d046664373946378a8e04ac6 项目模板，按其项目创建映射保留内容。\n"
        "A/B/C/D 校准图片和所有检测音为本次验收新生成的素材；检测音不是人声。\n"
        "没有打包 ASER 播放器或完整官方素材库。第三方素材权利仍归原权利人。\n",
        encoding="utf-8",
    )
    records = []
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file():
            records.append({
                "path": path.relative_to(PROJECT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    (PROJECT / "package-manifest.json").write_text(json.dumps({
        "target_aser_version": plan["target_aser_version"],
        "runtime_status": "not_run_on_windows",
        "files": records,
    }, ensure_ascii=False, indent=2) + "\n")
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARTIFACT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in sorted(PROJECT.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo("ASER_YSS_Acceptance/" + path.relative_to(PROJECT).as_posix(), (2026, 10, 27, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                output.writestr(info, path.read_bytes())
    print(f"项目：{PROJECT}")
    print(f"压缩包：{ARTIFACT} ({ARTIFACT.stat().st_size} 字节)")
    print(f"SHA-256：{hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
