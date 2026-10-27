# ASER-YSS

本项目使用 YSS 编辑器和 ASER 播放器制作《明日方舟》二创剧情，实际脚本语言为 **AStoryX**。你负责剧情创作和剧本规定；我负责将剧本转换为 `.astoryx` 代码文本，并检查资源引用与播放效果。

## 目录约定

| 路径 | 用途 |
| --- | --- |
| `story-code/` | 只存放根据你的剧本编写的 YSS 剧情代码文本；不放说明、原始剧本、工具、资源、占位文件或测试结果。 |
| `vendor/YayinStoryStudio/` | 已下载并原样导入的 YSS 源码、插件、文档、规则、模板和示例资源。 |
| `vendor/ASER/` | 从用户三卷压缩包完整导入的 ASER 3.7.12 Windows 本体。 |
| `docs/` | 使用流程、资料来源、版本记录及待确认事项。 |
| `tools/` | 仓库辅助脚本，不是剧情代码。 |

Git 不保存空目录。第一次检出后运行：

```bash
cd /workspace/ASER-YSS
python3 tools/prepare_workspace.py
```

这会创建 `story-code/` 和 `vendor/ASER/`，保留其已有内容。`story-code/` 只提交按你的剧本编写的 `.astoryx` 文本，不使用占位代码填充目录。

## 当前状态

- 已从你提供的提交下载完整 YSS 快照：`49e2528c42809779d046664373946378a8e04ac6`，722 个文件、解压后约 37.5 MiB；原始上游内容保持不变。
- 版本头标为 YSS `0.18.0.255 EA TP1`；内含 ASER 3.0 和 3.6.7 模板。这是源码快照，不是已安装的编辑器程序或 ASER 本体。
- 已读取源码内的文档、解析器、规则和三个 3.6.7 官方示例，并生成 21 类控制器的参数参考。
- 三个 `ASE-Remake.part*.rar` 分卷已完整校验并解压：182 个文件，约 122 MiB。已从 Unity 元数据确认播放器版本为 `3.7.12`，本体文件保持原样。
- [语雀教程](https://www.yuque.com/tsingyayin/aser)访问已恢复，已阅读导航中 17 篇文章正文，学习笔记见 [语雀学习记录](docs/yuque-study-notes.md)。
- 云端尚未运行 YSS GUI、上游 C++ 解析器或 Windows ASER 播放；完整官方素材名单尚未取得，播放器包中没有包含这些名单。

先读 [AStoryX 工作说明](docs/astoryx-guide.md)及[参数参考](docs/astoryx-controller-reference.md)。资料和下载明细见 [docs/reference-status.md](docs/reference-status.md)，更新流程见 [docs/workflow.md](docs/workflow.md)。

核对导入文件和比较新版目录：

```bash
python3 tools/check_toolchain.py
python3 tools/check_toolchain.py --tool aser
python3 tools/check_toolchain.py --candidate /tmp/新版YSS解压目录
python3 tools/check_toolchain.py --tool aser --candidate /tmp/新版ASER解压目录
```

比较命令只报告差异，不覆盖文件。更换版本并更新清单后，用 `python3 tools/build_astoryx_reference.py` 重新生成参数参考。

## 接收你的 TXT 剧本

你可以直接提供格式不统一的 TXT，无须预先整理。我会结合上下文区分对白、旁白、动作和作者备注，保留你的内容与顺序，转换成 `story-code/` 中的 `.astoryx` 文件。影响剧情含义或素材选择的问题会集中确认；可确定的部分继续编写。

成功经验和后续约定已记在 [TXT 剧本转换与编写经验](docs/txt-to-astoryx.md)。原稿按需保存在 `story-input/`，技术说明放在 `docs/story-notes/`，代码目录仍只存放剧情代码。

## 本地全功能验收

[下载验收项目包](artifacts/ASER_YSS_acceptance.zip)，完整解压后在 ASER 中打开其中的 `ASER_YSS_Acceptance` 剧本集，先播放 `00_all_features`。它自带所需素材，不依赖官方素材名单。

主剧本包含 21 个场景；主剧本和 BaseRule 复核分别覆盖 21 类控制器及 101 项主要／可选参数。另有 9 个独立兼容性探针，用于核实文档和版本差异。具体预期现象见 [验收说明](docs/acceptance-checklist.md)。用户已反馈认可前次通过测试的格式，后续沿用该基线；云端完成的是自有静态检查与素材检查，边界探针的逐项本地结果尚未记录。

源文件在 `story-code/`；构建目录受忽略，文档与资源不会放进代码专用目录。重新构建和检查：

```bash
python3 tools/build_acceptance_project.py
python3 tools/check_acceptance.py
python3 -m unittest discover -s tests -v
```
