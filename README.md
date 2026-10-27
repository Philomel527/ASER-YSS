# ASER-YSS

本项目使用 YSS 编辑器和 ASER 播放器制作《明日方舟》二创剧情，实际脚本语言为 **AStoryX**。你负责剧情创作和剧本规定；我负责将剧本转换为 `.astoryx` 代码文本，并检查资源引用与播放效果。

## 目录约定

| 路径 | 用途 |
| --- | --- |
| `story-code/` | 只存放根据你的剧本编写的 YSS 剧情代码文本；不放说明、原始剧本、工具、资源、占位文件或测试结果。 |
| `vendor/YayinStoryStudio/` | 已下载并原样导入的 YSS 源码、插件、文档、规则、模板和示例资源。 |
| `vendor/ASER/` | 为 ASER 本体保留的位置；附件传输受限，当前尚未导入。 |
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
- 最新附件 `ASE-Remake.rar` 仍超过当前下载工具的单文件 32 MiB 传输上限，尚未下载或解压到 `vendor/ASER/`。
- [语雀教程](https://www.yuque.com/tsingyayin/aser)尚未读到：当前环境的网络策略阻止访问。
- 尚未运行 YSS GUI、上游 C++ 解析器或 ASER 播放；本地 ASER 的实际版本和完整素材名单待核实。

先读 [AStoryX 工作说明](docs/astoryx-guide.md)及[参数参考](docs/astoryx-controller-reference.md)。资料和下载明细见 [docs/reference-status.md](docs/reference-status.md)，更新流程见 [docs/workflow.md](docs/workflow.md)。

核对导入文件和比较新版目录：

```bash
python3 tools/check_toolchain.py
python3 tools/check_toolchain.py --candidate /tmp/新版YSS解压目录
```

比较命令只报告差异，不覆盖文件。更换版本并更新清单后，用 `python3 tools/build_astoryx_reference.py` 重新生成参数参考。
