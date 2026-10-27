# AStoryX 控制器参数参考

来源提交：`49e2528c42809779d046664373946378a8e04ac6`。规则来自上游 `template/3.6.7/Rules/`，类型、默认值和约束来自 `astoryxMeta/default.json`，说明来自 `i18n/zh_CN.json`。

由 `python3 tools/build_astoryx_reference.py` 生成。这里记录的是源码内的规则和元数据；不是已经通过 ASER 播放测试的运行时保证。实际 ASER 版本及项目自定义规则优先。

`BaseRule` 依靠位置和前缀，`AdvanceRule` 的大多数参数使用具名的 `,@参数名=` 前缀。变量赋值仍使用 `=`，必须以每一行表中的前缀为准。

## 背景 / Background

控制背景的显示。

行首：`背景：`；主要参数：`ImageName`；主要参数内分隔符：`+`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `ImageName` | String | `""` | — | `主要参数` | `主要参数` | 指定背景所使用的图片名称 |
| `FadeInTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定背景淡入的时间，单位为秒 |
| `StartPosition` | Vector | `"0,0,10"` | — | `/` | `,@StartPosition=` | 背景图片显示的起始坐标位置 |
| `EndPosition` | Vector | `"0,0,10"` | — | `/` | `,@EndPosition=` | 背景图片显示的结束坐标位置 |
| `MoveTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@MoveTime=` | 背景图片从起始位置移动到结束位置的时间，单位为秒 |
| `MoveCurve` | Enum | `"Linear"` | `{"enums": "MoveCurveEnums", "dimensions": [1, 3]}` | `/` | `,@MoveCurve=` | 背景图片移动的曲线类型 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |
| `StitchVertically` | Bool | `"true"` | — | `/` | `,@StitchVertically=` | 是否将多个图片进行垂直拼贴。这个布尔量true为垂直拼贴，false为水平拼贴。 |
| `StitchColumnCount` | Integer | `"1"` | `{"min": 0}` | `/` | `,@StitchColumnCount=` | 在当前拼贴方向上的最大拼贴个数，超出这个数目后会自动转到下一列或下一行，以进行网格状的拼贴 |

## 音乐 / Music

控制音乐的播放。

行首：`音乐：`；主要参数：`AudioName`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `AudioName` | String | `""` | — | `主要参数` | `主要参数` | 指定音乐所使用的音频名称 |
| `Volume` | Float | `"1"` | `{"range": [0, 1]}` | `/` | `,@Volume=` | 指定音乐的音量，范围从0到1 |
| `FadeInTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定音乐淡入的时间，单位为秒 |
| `SlotIndex` | Integer | `"0"` | `{"min": 0}` | `/` | `,@SlotIndex=` | 指定音乐的插槽索引，默认为0（即音轨序号）。如果需要同时播放多段音乐，可以使用不同的插槽索引来区分它们。 |
| `Position` | Float | `"0"` | `{"range": [-1, 1]}` | `/` | `,@Position=` | 音乐的空间位置，-1为左，1为右，可在这个范围内自由调整 |

## 音效 / SoundEffect

控制音效的播放。

行首：`音效：`；主要参数：`AudioName`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `AudioName` | String | `""` | — | `主要参数` | `主要参数` | 指定音效所使用的音频名称 |
| `Volume` | Float | `"1"` | `{"range": [0, 1]}` | `/` | `,@Volume=` | 指定音效的音量，范围从0到1 |
| `Position` | Float | `"0"` | `{"range": [-1, 1]}` | `/` | `,@Position=` | 音效的空间位置，-1为左，1为右，可在这个范围内自由调整 |
| `Steps` | Integer | `"0"` | `{"min": 0}` | `/` | `,@Steps=` | 指定音效播放的步数，即持续多少个控制器后终止 |
| `AsVoice` | Bool | `"false"` | — | `/` | `,@AsVoice=` | 是否将这个音效视作配音。如果视作配音的话，下一个对话控制器会自动协调这个音效的播放时间，以保证对话和配音的同步。 |

## 遮罩 / Mask

控制遮罩的显示。

行首：`遮罩：`；主要参数：`IsOn`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `IsOn` | Bool | `""` | — | `主要参数` | `主要参数` | 是否显示遮罩 |

## 角色 / Character

控制角色的显示。

行首：`--`；主要参数：`Character&Variant`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Character&Variant` | String | `""` | — | `主要参数` | `主要参数` | 指定角色的名称和变体，如果没有变体则直接使用角色名称 |
| `SlotIndex` | Integer | `"0"` | — | `/` | `,@SlotIndex=` | 指定角色的插槽索引，默认为0。如果需要同时显示多位角色，可以使用不同的插槽索引来区分它们。 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |
| `FadeInTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定角色淡入的时间，单位为秒 |
| `StayTime` | Float | `"1.75"` | `{"min": 0}` | `/` | `,@StayTime=` | 指定角色持续的时间，单位为秒 |
| `FadeOutTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeOutTime=` | 指定角色淡出的时间，单位为秒 |
| `Effects` | String | `""` | — | `/` | `,@Effects=` | 指定角色的特效 |
| `Alpha` | Float | `"1"` | `{"range": [0, 1]}` | `/` | `,@Alpha=` | 角色的透明度，范围从0到1 |
| `RenderOrder` | Integer | `"0"` | — | `/` | `,@RenderOrder=` | 角色的渲染顺序，数值较大的角色会覆盖在数值较小的角色上 |
| `StartPosition` | Vector | `"0,0,10,0"` | `{"dimensions": [3, 4]}` | `/` | `,@StartPosition=` | 角色显示的起始坐标位置 |
| `EndPosition` | Vector | `"0,0,10,0"` | `{"dimensions": [3, 4]}` | `/` | `,@EndPosition=` | 角色显示的结束坐标位置 |
| `MoveTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@MoveTime=` | 角色从起始位置移动到结束位置的时间，单位为秒 |
| `MoveCurve` | Enum | `"Linear"` | `{"enums": "MoveCurveEnums", "dimensions": [1, 3]}` | `/` | `,@MoveCurve=` | 角色移动的曲线类型 |

## 选项 / Choice

控制选项的显示。

行首：`选项：`；主要参数：`ChoiceContent`；主要参数内分隔符：`` ` ``。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `ChoiceContent` | String | `""` | — | `主要参数` | `主要参数` | 选项的文本内容 |
| `OutputVariable` | String | `"choice"` | — | `/` | `,@OutputVariable=` | 选项的输出变量名称，玩家选择的结果会被存储在这个变量中 |

## 延迟 / Delay

控制延迟。

行首：`+`；主要参数：`DelayTime`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `DelayTime` | Float | `""` | `{"min": 0}` | `主要参数` | `主要参数` | 延迟的持续时间，单位为秒 |

## 视效 / VisualEffect

控制视效的显示。

行首：`特效：`；主要参数：`VisualEffectName`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `VisualEffectName` | String | `""` | — | `主要参数` | `主要参数` | 指定视效所使用的特效名称 |
| `Steps` | Integer | `"1"` | `{"min": 1}` | `/` | `,@Steps=` | 指定视效持续的步数，即持续多少个控制器后终止 |
| `Position` | Vector | `"0,0,10"` | — | `/` | `,@Position=` | 视效的坐标位置 |
| `RenderOrder` | Integer | `"0"` | — | `/` | `,@RenderOrder=` | 视效的渲染顺序，数值较大的视效会覆盖在数值较小的视效上 |

## 插播 / Interlude

控制插播的显示。

行首：`插播：`；主要参数：`Character&Variant`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Character&Variant` | String | `""` | — | `主要参数` | `主要参数` | 指定插播中角色的名称和变体，如果没有变体则直接使用角色名称 |
| `SlotIndex` | Integer | `"0"` | — | `/` | `,@SlotIndex=` | 指定插播中角色的插槽索引，默认为0。如果需要同时显示多位角色，可以使用不同的插槽索引来区分它们。 |
| `IsOn` | Bool | `"false"` | — | `/` | `,@IsOn=` | 是否显示插播 |
| `Type` | Integer | `"0"` | — | `/` | `,@Type=` | 插播的类型。0为灰色纵向类型，1为头像类型 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |
| `Effects` | String | `"0"` | — | `/` | `,@Effects=` | 指定插播的特效 |
| `RenderOrder` | Integer | `"0"` | — | `/` | `,@RenderOrder=` | 插播的渲染顺序，数值较大的插播会覆盖在数值较小的插播上 |
| `Position` | Vector | `"0,0,10,0"` | `{"dimensions": [3, 4]}` | `/` | `,@Position=` | 插播的坐标位置 |

## 色层 / ColorMask

控制色层的显示。

行首：`色层：`；主要参数：`Color`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Color` | Vector | `"0,0,0,1"` | `{"dimensions": [3, 4]}` | `主要参数` | `主要参数` | 色层的颜色，使用四维向量 |
| `FadeInTime` | Float | `"0.125"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定色层淡入的时间，单位为秒 |
| `StayTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@StayTime=` | 指定色层持续的时间，单位为秒 |
| `FadeOutTime` | Float | `"0.375"` | `{"min": 0}` | `/` | `,@FadeOutTime=` | 指定色层淡出的时间，单位为秒 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |

## 震屏 / Shake

控制震屏。

行首：`抖动：`；主要参数：`Intensity`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Intensity` | String | `"0.5"` | — | `主要参数` | `主要参数` | 震屏的强度 |
| `FadeInTime` | Float | `"0.125"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定震屏淡入的时间，单位为秒 |
| `StayTime` | Float | `"0.25"` | `{"min": 0}` | `/` | `,@StayTime=` | 指定震屏持续的时间，单位为秒 |
| `FadeOutTime` | Float | `"0.375"` | `{"min": 0}` | `/` | `,@FadeOutTime=` | 指定震屏淡出的时间，单位为秒 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |

## 自由文本 / FreeText

控制自由文本的显示。

行首：`自由文本：`；主要参数：`Content`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Content` | String | `""` | — | `主要参数` | `主要参数` | 文本的内容 |
| `IsAdditional` | Bool | `"false"` | — | `/` | `,@IsAdditional=` | 是否为附加文本。附加文本会在原有文本的基础上增加，而不是替换原有文本 |
| `Immediate` | Bool | `"false"` | — | `/` | `,@Immediate=` | 是否立即显示文本，而不是逐字显示 |
| `Alignment` | Enum | `"Left"` | `{"enums": "TextAlignmentEnums"}` | `/` | `,@Alignment=` | 文本的对齐方式 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |
| `FadeInTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定文本淡入的时间，单位为秒 |
| `StayTime` | Float | `"1.75"` | `{"min": 0}` | `/` | `,@StayTime=` | 指定文本持续的时间，单位为秒 |
| `FadeOutTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeOutTime=` | 指定文本淡出的时间，单位为秒 |
| `SlotIndex` | Integer | `"0"` | — | `/` | `,@SlotIndex=` | 指定文本的插槽索引，默认为0。如果需要同时显示多段文本，可以使用不同的插槽索引来区分它们。 |
| `AsSceneObject` | Bool | `"false"` | — | `/` | `,@AsSceneObject=` | 是否将文本作为场景对象来处理，这会使它受到场景中其他控制器的影响，例如震屏和色层等 |
| `Position` | Vector | `"0,0,10"` | — | `/` | `,@Position=` | 文本的坐标位置 |
| `RenderOrder` | Integer | `"0"` | — | `/` | `,@RenderOrder=` | 文本的渲染顺序，数值较大的文本会覆盖在数值较小的文本上 |
| `Interval` | Float | `"0.04"` | `{"min": 0}` | `/` | `,@Interval=` | 逐字显示时每个字出现的时间间隔，单位为秒 |
| `ExtraStayTime` | Float | `"0.05"` | `{"min": 0}` | `/` | `,@ExtraStayTime=` | 逐字显示时文本完全显示后额外持续的时间，单位为秒 |

## 切屏 / Cut

控制屏幕裁切。

行首：`裁切：`；主要参数：`Intensity`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Intensity` | Float | `""` | `{"range": [0, 1]}` | `主要参数` | `主要参数` | 裁切的强度 |
| `Angle` | Float | `"0"` | — | `/` | `,@Angle=` | 裁切的角度，单位为度 |
| `SlotIndex` | Integer | `"0"` | — | `/` | `,@SlotIndex=` | 指定裁切的插槽索引，默认为0。如果需要同时使用多段裁切，可以使用不同的插槽索引来区分它们。 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |
| `FadeInTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定裁切淡入的时间，单位为秒 |
| `StayTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@StayTime=` | 指定裁切持续的时间，单位为秒 |
| `FadeOutTime` | Float | `"0"` | `{"min": 0}` | `/` | `,@FadeOutTime=` | 指定裁切淡出的时间，单位为秒 |
| `RenderOrder` | Integer | `"700"` | — | `/` | `,@RenderOrder=` | 裁切的渲染顺序，数值较大的裁切会覆盖在数值较小的裁切上 |

## 滤镜 / Filter

控制滤镜的显示。

行首：`滤镜：`；主要参数：`Type&Intensity`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Type&Intensity` | String | `""` | — | `主要参数` | `主要参数` | 指定滤镜的类型和强度，不同类型的滤镜会有不同的强度范围 |
| `FadeInTime` | Float | `"1"` | `{"min": 0}` | `/` | `,@FadeInTime=` | 指定滤镜淡入的时间，单位为秒 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |

## 动态文本 / AnimatedText

控制动态文本的显示。

行首：`动态文本：`；主要参数：`Content`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Content` | String | `""` | — | `主要参数` | `主要参数` | 文本的内容 |
| `Type` | Integer | `"0"` | — | `/` | `,@Type=` | 动态文本的类型，不同类型的动态文本会有不同的动画效果 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。阻塞的控制器会等待全部动画结束才开始执行下一行 |

## 标签 / Sign

声明一个标签

行首：`标记：`；主要参数：`Name`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Name` | String | `""` | — | `主要参数` | `主要参数` | 标签的名称 |

## 变量 / Variable

声明一个变量

行首：`变量：`；主要参数：`Name`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Name` | String | `""` | — | `主要参数` | `主要参数` | 变量的名称 |
| `Expression` | String | `""` | — | `=` | `=` | 变量的表达式，变量的值会被计算为这个表达式的结果 |

## 判断 / Judge

进行一个判断

行首：`判断：`；主要参数：`Name`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Name` | String | `""` | — | `主要参数` | `主要参数` | 需要保存的判断结果的变量名称 |
| `Expressions` | String | `""` | — | `/` | `,@Expressions=` | 判断的表达式列表，如果计算结果大于0，就存储到变量中 |

## 分支 / Branch

根据条件进行分支

行首：`分支：`；主要参数：`Name`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Name` | String | `""` | — | `主要参数` | `主要参数` | 分支的名称 |
| `Branches` | String | `""` | — | `/` | `,@Branches=` | 将要跳转到的标记的名称 |

## 旁白 / Narration

设置旁白的文本内容。这个旁白是用于在对话记录中显示的上下文提示，供快速浏览剧情时使用，并非显示在播放过程中的独白。

行首：`*`；主要参数：`Content`；主要参数内分隔符：`:`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Content` | String | `""` | — | `主要参数` | `主要参数` | 旁白的文本内容 |

## 对话 / Dialog

控制对话的显示。

行首：`无行首标识`；主要参数：`Speaker&Content`；主要参数内分隔符：`	`。

| 参数 | 类型 | 元数据默认值 | 约束 | BaseRule 前缀 | AdvanceRule 前缀 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `Speaker&Content` | String | `""` | — | `主要参数` | `主要参数` | 说话者的名称和对话的文本内容 |
| `IsAdditional` | Bool | `"false"` | — | `/` | `,@IsAdditional=` | 是否为附加对话。附加对话会在原有对话的基础上增加，而不是替换原有对话 |
| `ModifyCharacters` | Bool | `"true"` | — | `/` | `,@ModifyCharacters=` | 是否同步控制已有角色立绘的显示以匹配对话中说话者的变化，这会使角色立绘随着对话的进行而自动明暗切换 |
| `BasicStayTime` | Float | `"1.75"` | `{"min": 0}` | `/` | `,@BasicStayTime=` | 对话持续的基本时间，单位为秒。对话会在这个基本时间的基础上根据文本长度增加额外的持续时间 |
| `Interval` | Float | `"0.04"` | `{"min": 0}` | `/` | `,@Interval=` | 逐字显示时每个字出现的时间间隔，单位为秒 |
| `ExtraStayTime` | Float | `"0.05"` | `{"min": 0}` | `/` | `,@ExtraStayTime=` | 逐字显示时文本完全显示后额外持续的时间，单位为秒 |
| `IsBlocker` | Bool | `"true"` | — | `/` | `,@IsBlocker=` | 是否阻塞。当这个对话控制器关联到一个角色立绘时，这个选项会控制这个对话控制器是否要等待角色立绘中的动画全部结束才开始执行下一行。 |

## 共享枚举

`MoveCurveEnums`：`Unset`、`Linear`、`InSine`、`OutSine`、`InOutSine`、`InQuad`、`OutQuad`、`InOutQuad`、`InCubic`、`OutCubic`、`InOutCubic`、`InQuart`、`OutQuart`、`InOutQuart`、`InQuint`、`OutQuint`、`InOutQuint`、`InExpo`、`OutExpo`、`InOutExpo`、`InCirc`、`OutCirc`、`InOutCirc`、`InElastic`、`OutElastic`、`InOutElastic`、`InBack`、`OutBack`、`InOutBack`、`InBounce`、`OutBounce`、`InOutBounce`

`TextAlignmentEnums`：`left`、`center`、`right`
