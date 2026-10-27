# 用户资源名册与别名

来源：用户于 2026-10-27 上传的 `Configs.rar`。本页记录该次快照；名册本身未声明对应的游戏版本。

三份原始配置保存在 [resource-catalog/Configs](../resource-catalog/Configs/)，保持上传时的文件内容；来源、文件大小与 SHA-256 见 [来源清单](../resource-catalog/source-manifest.json)，核对结果见 [audit.json](../resource-catalog/audit.json)。

## 当前可定位的范围

| 类别 | 名册资源数 | 已设置别名 | 已提供角色配置 |
| --- | ---: | ---: | ---: |
| 普通立绘 | 1,808 | 25 | 10 |
| 动态立绘 | 100 | 0 | 0 |
| 背景 | 2,799 | 45 | 0 |
| BGM | 582 | 22 | 0 |
| 音效 | 7,949 | 7 | 0 |
| 特效 | 274 | 1 | 0 |

合计 **13,512 项资源、100 个别名、10 份角色差分配置**。100 个别名和 10 份角色配置的目标都存在于本次名册；未发现差分名称冲突。

名册包含资源标识及对应的游戏资源包路径，配置包不包含这些图像、音乐或资源包本身。这里的“可定位”指名称映射可查，不表示云端已加载或播放游戏素材。未提供差分配置的角色仍可能有表情，不根据文件缺省推断其表情名称。

## 一处名称冲突

`35_i10` 既是背景原名，又被设为 `36_g4_redleafcliff` 的别名：

| 查询名称 | 原始标识 | 资源包路径 |
| --- | --- | --- |
| `35_i10` | `35_i10` | `avg/imgs/avg_img_35_0.ab` |
| `35_i10` | `36_g4_redleafcliff` | `avg/bg/avg_bkg_h1_36_0.ab` |

查询工具保留这两个候选，不假定 ASER 在原名和别名重合时的解析优先级。写到这个背景时先确认具体对象，保留原配置，不自动改名。

此外，用户的 `Mon3tr` 指向官方立绘 `avg_4179_monstr_1`；验收项目用的是外部立绘 `mon3tr(amb2026)`，两者不能混同。“霜星”和“霜星2”、旧立绘“年（旧立绘）”和“年”也分别指向不同资源。

## 查询与更新

```bash
python3 tools/query_resource_catalog.py
python3 tools/query_resource_catalog.py 霜星 --exact
python3 tools/query_resource_catalog.py 博士 --exact
python3 tools/query_resource_catalog.py 罗德岛餐厅 --kind backgrounds --exact
python3 tools/query_resource_catalog.py 温馨 --kind musics --exact
python3 tools/query_resource_catalog.py 35_i10 --kind backgrounds --exact
python3 tools/query_resource_catalog.py --compare /tmp/新版Configs
```

默认查找原名和别名的子串；`--exact` 保留大小写并精确匹配。结果列出类别、原始标识、别名、资源包路径及已提供的角色配置；无结果时退出码为 1，不自动猜测近似素材。比较新版只输出增删和改动，不覆盖文件。

后续正式剧本先按用户称呼查询准确标识，再核对目标项目采用的别名与覆盖配置。项目级配置可能改变实际映射；本次收到的是全局配置快照，不能推断未提供的项目覆盖。

名册更新须保留原始文件、更新来源哈希并同步本页。重新记录核对结果：

```bash
python3 tools/query_resource_catalog.py > resource-catalog/audit.json
```

## 已提供的立绘差分配置

这里只列出已命名差分；全部原始差分键可通过查询命令或原始 JSON 查看。带原始编号的差分不凭编号推断表情。

| 角色 | 原始标识 | 配置差分数 | 已命名差分（名称 ← 原始键） |
| --- | --- | ---: | --- |
| 博士 | `avg_doc_1` | 1 | 常规 ← `#0$1` |
| 霜星 | `char_1505_frstar_1` | 10 | 常规 ← `#1$1`；阴影 ← `shadow`；战斗闭眼 ← `#3$1`；战斗常规 ← `#4$1`；战斗呵斥 ← `#5$1`；闭眼 ← `#7$1`；微笑 ← `#8$1`；呵斥 ← `#9$1` |
| 缄默德克萨斯 | `avg_1028_texas2_1` | 22 | 正常 ← `#1$1`；闭眼 ← `#2$1`；吃惊 ← `#3$1`；呵斥 ← `#4$1`；不爽 ← `#6$1`；生气 ← `#7$1`；目移 ← `#8$1`；微笑 ← `#9$1`；闭眼微笑 ← `#10$1` |
| 芋圆安洁莉娜 | `avg_1015_aglna2_1` | 52 | 正常 ← `#1$1`；目移 ← `#3$1`；闭眼 ← `#5$1`；wink ← `#6$1`；吃惊 ← `#7$1`；大吃一惊 ← `#8$1`；难过 ← `#9$1`；惊慌 ← `#11$1`；屑表情 ← `#16$1`；生气 ← `#17$1`；呵斥 ← `#18$1`；满意 ← `#19$1`；笑 ← `#21$1` |
| 爱布拉娜 | `avg_450_necras_1` | 34 | 仅保留原始编号 |
| 澄闪 | `avg_377_gdglow_1` | 13 | 正常 ← `#1$1`；惊讶 ← `#4$1`；失落 ← `#5$1`；闭眼 ← `#6$1`；生气 ← `#8$1`；呵斥 ← `#9$1`；开心 ← `#10$1`；开心2 ← `#11$1`；不开心 ← `#12$1` |
| 司霆惊蛰 | `avg_1043_leizi2_1` | 16 | 仅保留原始编号 |
| 凛御银灰 | `avg_1045_svash2_1` | 12 | 仅保留原始编号 |
| 圣聆初雪 | `avg_1046_sbell2_1` | 13 | 正常 ← `#1$1`；高低眉 ← `#2$1`；微笑 ← `#4$1`；目移 ← `#5$1`；吃惊 ← `#6$1`；呵斥 ← `#7$1`；眯眼笑 ← `#8$1`；睡着 ← `#9$1`；生气 ← `#10$1`；哈欠 ← `#11$1`；疑惑 ← `#12$1` |
| 初雪 | `avg_174_slbell_1` | 13 | 仅保留原始编号 |

## 全部用户别名

下表按上传文件记录，完整保留用字、大小写与标点，不擅自修正名字。别名表达的场景含义以用户创作意图为准，不根据名字编造素材画面。

### 普通立绘（25）

| 用户别名 | 原始资源标识 |
| --- | --- |
| 霜星 | `char_1505_frstar_1` |
| 博士 | `avg_doc_1` |
| Mon3tr | `avg_4179_monstr_1` |
| 缪尔赛思 | `char_249_muesys_8` |
| 缄默德克萨斯 | `avg_1028_texas2_1` |
| 芋圆安洁莉娜 | `avg_1015_aglna2_1` |
| 年（旧立绘） | `char_2014_nian_1` |
| 年 | `avgnew_2014_nian_1` |
| 遥 | `avg_4202_haruka_1` |
| 莫斯提马 | `avg_213_mostma_1` |
| 霜星2 | `avg_1505_frstar_1` |
| 暴行 | `avg_230_savage_1` |
| 凯尔希 | `avg_003_kalts_1` |
| 可露希尔 | `avg_007_closre_1` |
| 煌 | `avg_017_huang_1` |
| 浊心斯卡蒂 | `avg_1012_skadisp_1` |
| 水陈 | `avg_1013_spchen_1` |
| 焰影苇草 | `avg_1020_reed2_1` |
| 晓歌 | `avg_497_ctable_1` |
| 爱布拉娜 | `avg_450_necras_1` |
| 澄闪 | `avg_377_gdglow_1` |
| 圣聆初雪 | `avg_1046_sbell2_1` |
| 司霆惊蛰 | `avg_1043_leizi2_1` |
| 凛御银灰 | `avg_1045_svash2_1` |
| 初雪 | `avg_174_slbell_1` |

### 背景（45）

| 用户别名 | 原始资源标识 |
| --- | --- |
| 35_i10 | `36_g4_redleafcliff` |
| 写信 | `cg_letter` |
| 烟花 | `cg_firework` |
| 玻璃雨滴 | `cg_droplets_glass` |
| 干员宿舍 | `bg_room_2` |
| 罗德岛活动室 | `bg_rhodesroom` |
| 罗德岛休息区 | `bg_rhodeslounge` |
| 罗德岛休息区2 | `bg_rhodeslounge_2` |
| 罗德岛餐厅，源石危机 | `60_g11_rhodescanteen_origin` |
| 罗德岛餐厅 | `bg_canteen` |
| 罗德岛办事处1 | `21_g9_rhodes_xqoffice` |
| 罗德岛甲板 | `49_g14_rhodesdeck_d` |
| 罗德岛甲板，夜晚 | `49_g15_rhodesdeck_n` |
| 罗德岛舰桥 | `60_g12_rhodesdeck_cloudy` |
| 罗德岛abyss | `60_g4_rhodesabyss_w` |
| 干员宿舍，夜晚 | `bg_rhodesbedroom` |
| 罗德岛走廊1 | `bg_corridor` |
| 罗德岛走廊2 | `bg_corridor_2` |
| 罗德岛走廊3 | `bg_corridor_3` |
| 罗德岛走廊4 | `bg_corridor_4` |
| 监狱走廊 | `bg_prison_corridor` |
| 维多利亚街道1 | `21_g3_victoria_street_d` |
| 维多利亚街道2 | `21_g7_decisivebattlealley_d` |
| 谢拉格雪山树林 | `24_g1_snowyforest` |
| 维多利亚街道2，夜晚 | `25_mini02_victoria_street_n` |
| 塔拉街道1 | `59_g1_citystreets_d` |
| 塔拉小酒馆 | `59_g10_indoor` |
| 塔拉宫殿走廊 | `59_g11_castlecorridor_d` |
| 塔拉宫殿走廊夜晚 | `59_g12_castlecorridor_n` |
| 塔拉城堡露台 | `59_g13_castlebalcony` |
| 塔拉城堡露天，夜晚 | `59_g15_castlebalcony_n` |
| 塔拉街道1，夜晚 | `59_g2_citystreets_n` |
| 塔拉街道2 | `59_g3_dragonsquare_d` |
| 塔拉街道2，夜晚 | `59_g4_dragonsquare_n` |
| 塔拉森林 | `59_g7_blackforest_d` |
| 塔拉森林，夜晚 | `59_g8_blackforest_n` |
| 博士暴行阿米娅 | `46_i01` |
| 罗德岛指挥中心 | `bg_rhodescom` |
| 罗德岛会议室 | `bg_rhodesmeetingroom` |
| 罗德岛缓冲甲板 | `bg_rhodeslowerdeck` |
| 罗德岛发射甲板 | `bg_rhodesupperdeck` |
| 罗德岛病房 | `bg_rhodesinpatientcenter` |
| 罗德岛病房2 | `bg_rhodesward` |
| 罗德岛天花板 | `cg_rhodes_ceiling` |
| 罗德岛底层 | `bg_rhodescorner` |

### BGM（22）

| 用户别名 | 原始资源标识 |
| --- | --- |
| 尘环行动纯音乐 | `m_sys_recalrune_reward2` |
| 平常 | `m_avg_normal` |
| 温馨 | `m_avg_siestacity` |
| 剧情推进，迷雾 | `m_avg_sjoyasorrow` |
| speedoflight | `m_avg_speedoflight` |
| 悠闲 | `m_avg_victorianormal` |
| renegade纯音乐 | `m_avg_w` |
| 灾难后，温暖 | `m_avg_warm` |
| 破碎的大地 | `m_avg_wasteland` |
| coloryournight | `m_avg2_act54side` |
| 揭幕者们主题曲 | `m_bat_cnvlap` |
| 愚人曲 | `m_bat_dsdevr` |
| 玩乐时光 | `m_dia_farce` |
| 悬疑 | `m_dia_mist` |
| 楼梯两人快递箱 | `m_dia_street` |
| 旅途前方 | `m_dia_path` |
| 大柏墟 | `m_dia_nightoflongmen` |
| 新希望2 | `m_dia_newhope02` |
| 新希望1 | `m_dia_newhope01` |
| 逃离 | `m_dia_escape` |
| 黑暗1 | `m_dia_darkness01` |
| 黑暗2 | `m_dia_darkness02` |

### 音效（7）

| 用户别名 | 原始资源标识 |
| --- | --- |
| 爆炸1 | `p_skill_fireboomexplo` |
| 脚步 | `d_avg_wtchkgopenftstp` |
| 仪器滴滴 | `d_avg_heartratemonitor` |
| 车水马龙 | `d_avg_noisycitytraffic` |
| 拍手 | `d_avg_strangeclap` |
| 传送 | `g_ui_transition` |
| 传送2 | `g_ui_linetransition` |

### 特效（1）

| 用户别名 | 原始资源标识 |
| --- | --- |
| 渐变白屏 | `avg_062_white_02` |
