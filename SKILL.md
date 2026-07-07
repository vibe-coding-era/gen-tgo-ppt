---
name: gen-tgo-ppt-skill
description: 生成或改造 TGO鲲鹏会 / GTLC 风格 PPT 与 HTML 演示稿。适用于从 PPT、PDF、Markdown、HTML、粘贴内容或既有演示稿生成、套版、修复、校验 TGO/GTLC 演示材料；必须使用 V8.02 工作流、渐进式加载独立规则文件、生成日志、标题页后嘉宾介绍页、末尾感谢聆听页、排版安全检查、逐页渲染校对，以及“生成内容/检查风格/检查文字”职责分离。
---

# TGO/GTLC 演示稿生成技能

## 重要说明和介绍

以下说明为用户指定的受保护内容。AI 后续不得改写、删除、弱化或移动本节内容。

本 SKILL 是 TGO 鲲鹏会为了 AI 时代内容生成准备的 SKILL，内置了相应的模板，也可以做内容探讨，会使用不同的 SubAgent 做生成、校验，作者是杭州分会的肉山，欢迎使用。

## 版本

- 作者：肉山
- 当前版本：V8.02
- 核心变化：`SKILL.md` 只保留工作流与加载路由；澄清、固定页、日志、模板、排版安全、页型、校验、子智能体和守护规则全部拆入独立文件。
- 执行机制：不同规则文件必须由不同子智能体独立执行或检查，并按 SSOT 原则合并交接内容。

## 启动语

每次首次响应先说：

```text
我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。
```

## 用户澄清入口

用户澄清阶段不能省略。执行前先加载 `references/rule-intake.md`，按其中规则处理：

- 缺少 `Design.md` 时，询问应用场景、规格、输出格式、模板倾向、风格选择、处理模式和 Logo 决策。
- 缺少 `Content.md` 时，询问主题、问题、思考模式和文本初稿。
- 用户提供 PPT/PDF 时，先确认 `1. 修改内容并套模板` 或 `2. 只套模板不改内容`。
- 用户上传 Logo 时，先确认是否替换 GTLC Logo。
- 用户已经明确提供的信息不重复询问；源文件可直接看出的页数、标题、图片等不作为澄清问题。

详细菜单、`Design.md` / `Content.md` 模板和少问原则只维护在 `references/rule-intake.md`。

## 总工作流

1. 先加载 `references/workflow.md`，按其中的阶段和确认门推进。
2. 按用户输入识别来源类型：PPT、PDF、Markdown、HTML、粘贴内容、既有 PPT 修复，或纯新建。
3. 按“渐进式加载索引”只读取当下需要的规则文件；不要一次性加载所有设计、模板和视觉风格文件。
4. 缺少 `Design.md` 或 `Content.md` 时，按 `references/rule-intake.md` 补齐并写入当前工作目录。
5. 涉及 PPT/PDF 来源时，先确认“修改内容并套模板”或“只套模板不改内容”，再继续处理。
6. 每加载一个 rule 文件，就按 `references/rule-subagents.md` 分配不同规则子智能体独立执行；交接按 `references/rule-ssot-handoff.md` 合并。
7. 生成或修改任何 PPTX/HTML 前，按 `references/generation-log.md` 创建生成日志。
8. PPTX 输出必须包含标题页后的空白 `嘉宾介绍` 页和最终 `感谢聆听` 页；具体规则见 `references/rule-ppt-structure.md`。
9. 样片确认后再生成完整文件；如用户明确要求跳过确认，也要在日志里保留计划、样片或跳过原因。
10. 生成后必须运行 `scripts/check_pptx_layout.py` 或对应 HTML 检查，并渲染/预览逐页复核。
11. 最终交付前按 `references/rule-validation.md`、`references/rule-subagents.md` 和 `references/rule-ssot-handoff.md` 完成版型、风格、文字、SSOT 合并检查，并更新生成日志。

## 渐进式加载索引

| 场景 | 必须加载 | 条件加载 |
| --- | --- | --- |
| 任意任务启动 | `references/workflow.md` | `references/rule-intake.md`、`references/generation-log.md` |
| PPT/PDF/Markdown/HTML 转换 | `references/conversion-workflows.md` | 按来源类型读取对应段落 |
| 首次设计澄清或模板选择 | `references/design/index.md`、`references/design/shared/design.md` | 场景、模板、视觉风格文件按用户选择加载 |
| GTLC 大会 | `references/design/scenarios/gtlc-conference/design.md` | 选择的模板与视觉风格 |
| TGO 日常活动分享 | `references/design/scenarios/tgo-daily-sharing/design.md` | 默认优先 `references/design/templates/tgo-daily/design.md` |
| 固定页、Logo、品牌结构 | `references/rule-ppt-structure.md` | 用户上传 Logo 时再读取相关替换规则 |
| 模板选择 | `references/rule-template-selection.md` | `references/template-manifest.json` 仅在需要机器可读摘要时读取 |
| 排版、溢出、半尺寸画布、首尾页、项目基本信息页 | `references/rule-layout-safety-v802.md` | `references/rule-page-styles.md` |
| 生成日志 | `references/generation-log.md` | `scripts/create_generation_log.py` |
| 规则子智能体与 SSOT 交接 | `references/rule-subagents.md`、`references/rule-ssot-handoff.md` | 无 |
| 交付前检查 | `references/rule-validation.md` | `references/rule-subagents.md`、`references/rule-ssot-handoff.md` |
| 风险边界、不得做事项 | `references/rule-guardrails.md` | 无 |

## 设计文件加载规则

1. 先读 `references/design/index.md` 和 `references/design/shared/design.md`。
2. 根据场景只读一个场景文件：
   - `GTLC 大会`：`references/design/scenarios/gtlc-conference/design.md`
   - `TGO日常活动分享`：`references/design/scenarios/tgo-daily-sharing/design.md`
3. 根据模板只读相关模板文件：
   - `white`：`references/design/templates/white/design.md`
   - `light`：`references/design/templates/light/design.md`
   - `dark`：`references/design/templates/dark/design.md`
   - `tgo-daily`：`references/design/templates/tgo-daily/design.md`
4. 只读取用户选择或计划需要的视觉风格文件，不要把 `references/design/visual-styles/` 全部读入。
5. 当前目录的 `Design.md` 是本次任务决策记录，不要和 `references/design/**/design.md` 混用。

## 脚本入口

- 对比 PPTX 与模板：`python scripts/inspect_pptx_style.py path/to/deck.pptx`
- 创建生成日志：`python /path/to/gen-tgo-ppt-skill/scripts/create_generation_log.py --title "演示稿标题" --source "source.md" --format PPT`
- 检查 PPTX 版型：`python /path/to/gen-tgo-ppt-skill/scripts/check_pptx_layout.py path/to/generated.pptx`

运行脚本时从用户当前工作目录执行；脚本路径按本技能所在目录解析。

## 交付条件

交付前至少确认：

- 已创建并更新生成日志。
- 已按需加载独立规则文件，而不是只凭 `SKILL.md` 记忆执行。
- 已为不同 rule 分配不同子智能体并形成 SSOT；工具不支持时已在 SSOT 和日志里说明。
- PPTX 已通过 `scripts/check_pptx_layout.py`，且没有未处理的 `FAIL`。
- 已渲染或预览每一页，并修复异常换行、文本溢出、裁切、重叠、Logo/页脚碰撞和固定页错误。
- 若可用，`生成内容`、`检查风格`、`检查文字` 使用不同子智能体；不可用时在日志和最终回复里说明。

## 维护约束

- 不得改写、删除、弱化或移动“重要说明和介绍”。
- 新增规则优先写入 `references/rule-*.md` 或已有对应规则文件，不要把细则堆回 `SKILL.md`；新增 rule 时必须同步补充规则子智能体和 SSOT 交接要求。
- 修改版本时同步更新 `README.md`、`agents/openai.yaml`、`references/template-manifest.json`、`references/generation-log.md` 和 `scripts/create_generation_log.py`。
