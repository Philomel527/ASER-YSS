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

ASER 本体已从用户上传的三个 RAR5 分卷完整导入：

- 分卷大小依次为 20,971,520、20,971,520、8,330,868 字节。7-Zip 26.05 对全部三卷的整体校验结果为 `Everything is Ok`。
- 解压位置为 `vendor/ASER/`，共 182 个文件，127,901,044 字节。保留本体和运行库原始内容，未执行或修改可执行程序。
- 从 `ASE-Remake_Data/globalgamemanagers` 的 Unity `PlayerSettings.bundleVersion` 读取版本 **3.7.12**；程序为 Windows x86-64 Unity Mono。
- 分卷及逐文件 SHA-256 见 [aser-source-manifest.json](aser-source-manifest.json)。已核对 182 个 Git 提交文件与原始解压内容逐字节相同。

## 资料核验状态

| 资料／能力 | 已核实情况 | 尚未完成 |
| --- | --- | --- |
| YSS 源码 | 完整导入指定提交；版本头为 `0.18.0.255 EA TP1`。 | 未编译或启动 GUI；不能推断本地编辑器已安装此版本。 |
| ASER 模板 | 有 3.0 和 3.6.7 两套模板；本体元数据版本另外确认为 3.7.12。 | 模板与实际本体的运行兼容性尚需播放验证。 |
| AStoryX 规则 | 两套 3.6.7 规则各含 21 类控制器；已对照参数元数据和中文说明生成参考。 | 未运行上游 C++ 解析器；未执行 ASER 播放。 |
| 官方示例 | 已读三个 3.6.7 示例，涵盖主要演出、别名、块、变量和分支。 | 部分示例需要完整官方素材连接；并非当前云环境已能播放。 |
| 资源目录名单 | 已确认源码中的监视路径、索引结构和模板资源。 | 完整 `officialAssets_collections.json`、`officialAssets_aliases.json`、`officialAssets_userConfigs.json` 尚未取得。 |
| ASER 本体 | 三个分卷已完整校验并导入 `vendor/ASER/`；版本为 3.7.12。 | 当前 Linux 环境未运行 Windows 播放器，不把文件导入当作播放验证。 |
| ASER 教程 | 网络策略已改为 unrestricted，首页和公开正文请求均成功；已读导航中的 17 篇文章正文。 | 图片未逐张视觉核验；资料中的默认值和语法边界差异已记录，仍需结合目标本体测试。 |
| YSS 教程 | 上游 README 另指向 https://www.yuque.com/tsingyayin/yss ；同域网络阻碍已解除。 | 本轮优先学习用户指定的 ASER 知识库，未系统阅读另一本 YSS 使用手册。 |

## 已执行的检查

- 完整下载和 ZIP CRC：通过。
- 722 个源码文件的哈希清单及提交内容比对：通过。
- 三个 RAR 分卷的整体校验、182 个 ASER 文件的哈希与提交内容比对：通过。
- ASER 内置版本元数据读取：3.7.12。
- 当前模板规则、元数据与中文参数说明读取和参考生成：通过。
- 更新比较工具对新增、删除、修改及符号链接的识别：通过。
- ASER 语雀知识库 17 篇文章正文请求与阅读：完成，来源和更新日期见 [yuque-reference-index.json](yuque-reference-index.json)，学习与差异记录见 [yuque-study-notes.md](yuque-study-notes.md)。
- YSS GUI、上游 C++ 解析和 ASER 播放：未运行。

目前已对照源码和 ASER 教程正文整理核心编写方法、演出控制及分支逻辑；没有声称已验证完整播放。网络和压缩包传输问题已解决，后续需按用户当前素材名单核对引用，并在 Windows 本体上验证实际效果。
