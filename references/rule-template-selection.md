# V1.2 模板与视觉风格选择规则

## 选择门

`create`、`convert`、重大 `repair` 在 Brief 确认后必须展示本规则中的模板与视觉风格卡。模板或风格未明确确认时，不得静默采用场景默认值、历史选择或模型偏好。用户可选择具体项目、分页面映射，或选择“智能推荐”；智能推荐仍须展示推荐组合和理由，并等待确认。

过去的“默认优先”仅是智能推荐的候选依据，不是自动执行许可：`TGO日常活动分享 -> tgo-daily`、`GTLC 大会 -> light`、密集文字 -> `white`、强叙事页 -> `dark`、活动峰会/招商 -> `loop-orange-white`。用户明确选择优先于推荐。

## 模板选择卡

| 键 | 模板 | 适用表达 | 预览 |
| --- | --- | --- | --- |
| `white` | 白底内容页、深蓝封面/封底 | 正式文档、打印、密集事实和表格 | `assets/design/previews/templates/template-contact-sheet.png` |
| `light` | 浅蓝灰内容页 | 多数 GTLC 商务汇报与平衡型内容 | `assets/design/previews/templates/template-contact-sheet.png` |
| `dark` | 深蓝渐变 | 开场、收尾、章节和强叙事 keynote | `assets/design/previews/templates/template-contact-sheet.png` |
| `tgo-daily` | TGO 日常分享 16:9 | 非 GTLC 场景的主题分享 | `assets/design/previews/templates/tgo-daily-template-contact-sheet.png` |
| `loop-orange-white` | LOOP 大会正式模板 | AI 生态大会、招商权益、活动传播 | `assets/design/templates/loop-orange-white/tgo-loop-summit-16x9-contact-sheet.png` |

`D｜LOOP 大会`、`LOOP Summit`、`LOOP Orange White` 与 `LOOP 橙白峰会风` 均映射到 `loop-orange-white`。展示时应附上现有模板总览；用户可选择一个全局模板或明确的页面/章节模板映射。

## 视觉风格选择卡

展示总览 `assets/design/previews/styles/tgo-presentation-design-system-v1.png`，并用以下卡片说明选择会如何影响内容表达。按用户确认后才加载对应 `references/design/visual-styles/*/design.md`。

| 编号 | 风格 | 内容表达重点 |
| --- | --- | --- |
| `1` | Executive Board | 决策结论、清晰图表、克制留白 |
| `2` | Silicon Valley | 单页单主张、大标题、增长叙事与主视觉 |
| `3` | Big Tech Keynote | 沉浸式全幅视觉、极少文字、发布节奏 |
| `4` | AI Native | Agent/网络/流程图解解释 AI 系统 |
| `5` | Data Intelligence | 图表主导、指标分组、仪表盘式分析 |
| `6` | Minimal Luxury | 编辑感、极简短句、留白和精选图片 |
| `7` | Chinese Business | 克制东方科技点缀、产业叙事与结构图解 |
| `8` | Creative Festival | 高对比插画/创意图形、强故事节奏 |
| `9` | Enterprise AI Consulting | 可编辑架构、流程、公式和企业 AI 框架 |

可明确选择“封面用 `3`，内容页用 `1`，AI 组织/架构页用 `9`”等映射；每个映射都必须在日志与页纲中记录。风格 `9` 可额外展示 `assets/design/previews/styles/style-09-enterprise-ai-consulting.png`。

## 智能推荐卡

若用户选择“智能推荐”，在完整生成前展示：

```markdown
## 智能推荐（待确认）

- 推荐模板：<template key>
- 推荐视觉风格：<1-9，或分页面映射>
- 推荐理由：<仅基于已确认 Brief 的 1-3 条理由>
- 对图片/图解的影响：<将优先使用的视觉载体>
```

用户明确确认该卡后才标记 `design_confirmed`。未确认或只回复“你看着办”时，继续请求一次明确确认，不得进入完整生成。

## 选择记录

生成日志必须记录：展示过的预览资源、最终模板、最终风格/映射、智能推荐（若有）及确认依据。`check_only` 可根据检查范围读取模板信息，但不得把检查行为变成新的风格选择或写入操作。
