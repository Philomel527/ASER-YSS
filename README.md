# ASER-YSS

本项目使用 YSS 和 ASER 制作《明日方舟》二创剧情。你负责剧情创作和剧本规定；我负责将剧本转换为经过核验的 YSS 代码文本，并检查资源引用与播放效果。

## 目录约定

| 路径 | 用途 |
| --- | --- |
| `story-code/` | 只存放根据你的剧本编写的 YSS 剧情代码文本；不放说明、原始剧本、工具、资源、占位文件或测试结果。 |
| `vendor/ASER/` | 计划存放工具包解压内容；当前尚未导入。 |
| `docs/` | 使用流程、资料来源、版本记录及待确认事项。 |
| `tools/` | 仓库辅助脚本，不是剧情代码。 |

Git 不保存空目录。第一次检出后运行：

```bash
cd /workspace/ASER-YSS
python3 tools/prepare_workspace.py
```

这会创建 `story-code/`，保留其已有内容。确认实际语法和导入格式后，再向其中提交合法的剧情代码文本；不使用占位代码填充目录。

## 当前状态

- 已记录创作分工、代码目录约束和工具更新流程。
- `ASER.rar` 尚未导入：附件超过当前下载工具的单文件 32 MiB 传输上限；你将直接上传工具文件到仓库，届时从仓库接收。
- [语雀教程](https://www.yuque.com/tsingyayin/aser)尚未读到：当前环境的网络策略阻止访问。
- 尚未确认 YSS 语法、文件编码、导入方式和工具版本，尚未执行解析、转换或 ASER 播放验证。

完整流程见 [docs/workflow.md](docs/workflow.md)，资料核验情况见 [docs/reference-status.md](docs/reference-status.md)。
