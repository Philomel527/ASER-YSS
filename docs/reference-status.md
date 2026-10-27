# 资料、下载与验证记录

记录日期：2026-10-27。

## 已下载并提交的文件

- 来源：[用户指定的 YSS 提交](https://github.com/tsingyayin/YayinStoryStudio/commit/49e2528c42809779d046664373946378a8e04ac6)。
- 下载：[GitHub 完整源码 ZIP](https://codeload.github.com/tsingyayin/YayinStoryStudio/zip/49e2528c42809779d046664373946378a8e04ac6)。压缩包为 30,399,964 字节，解压文件为 39,369,914 字节，共 722 个文件。
- 已导入位置：`vendor/YayinStoryStudio/`。没有导入额外 `.git`，不是子模块，也没有新建 Git worktree。
- 原始 ZIP SHA-256：`d12fc0a1122e934cf7a6b782296e26cf6c971a640829dda94883f5c08a4d163d`。
- 逐文件来源、大小和 SHA-256：[yss-source-manifest.json](yss-source-manifest.json)。已检查 ZIP CRC，且提交时所有 Git 暂存文件与原始解压内容逐字节一致。
- 导入内容包括上游 README、许可证、开发文档、全部源码与构建配置、ASERStudio 插件、两套版本模板的规则和素材，以及三个 3.6.7 官方剧情示例。原有许可证和相关第三方声明均保留。
- 没有额外下载与此提交版本不同的发行包，也没有把 YSS 源码称为 ASER 本体。原始 ZIP 保留在当前机器的临时目录，仓库提交的是完整解压内容。

## 资料核验状态

| 资料／能力 | 已核实情况 | 尚未完成 |
| --- | --- | --- |
| YSS 源码 | 完整导入指定提交；版本头为 `0.18.0.255 EA TP1`。 | 未编译或启动 GUI；不能推断本地编辑器已安装此版本。 |
| ASER 模板 | 有 3.0 和 3.6.7 两套模板。 | 用户本地播放器实际版本仍待从本体核实。 |
| AStoryX 规则 | 两套 3.6.7 规则各含 21 类控制器；已对照参数元数据和中文说明生成参考。 | 未运行上游 C++ 解析器；未执行 ASER 播放。 |
| 官方示例 | 已读三个 3.6.7 示例，涵盖主要演出、别名、块、变量和分支。 | 部分示例需要完整官方素材连接；并非当前云环境已能播放。 |
| 资源目录名单 | 已确认源码中的监视路径、索引结构和模板资源。 | 完整 `officialAssets_collections.json`、`officialAssets_aliases.json`、`officialAssets_userConfigs.json` 尚未取得。 |
| ASER 本体 | 用户提供 `ASE-Remake.rar`；已尝试下载。 | 下载工具明确拒绝超过单文件 32 MiB 的附件，未下载、未解压、未提交。位置保留为 `vendor/ASER/`。此前的 `ASER.rar` 同样未取得。 |
| ASER 教程 | https://www.yuque.com/tsingyayin/aser ；访问曾被环境代理 CONNECT 403 阻止，当前生效策略仍不含该域名。 | `www.yuque.com` 已加入配置草稿，但不等于运行时已放行；需要环境设置生效后重试，或取得教程导出。 |
| YSS 教程 | 上游 README 另指向 https://www.yuque.com/tsingyayin/yss 。 | 同属尚未放行的语雀域名，尚未读到全文。 |

## 已执行的检查

- 完整下载和 ZIP CRC：通过。
- 722 个源码文件的哈希清单及提交内容比对：通过。
- 当前模板规则、元数据与中文参数说明读取和参考生成：通过。
- 更新比较工具对新增、删除、修改及符号链接的识别：通过。
- YSS GUI、上游 C++ 解析和 ASER 播放：未运行。

目前可以根据源码确认 AStoryX 的核心编写方法并建立转换流程，不能声称已读完语雀教程或已经验证完整播放。后续取得 ASER 本体或资源配置后，应更新此记录并继续运行验证。
