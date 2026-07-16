---
name: gen-tgo-ppt-skill
description: 生成、改造、转换、修复或校验 TGO鲲鹏会 / GTLC 风格 PPTX 与 HTML 演示稿；输入可为 PPT、PDF、Markdown、HTML、粘贴文本或既有演示稿。普通写作、通用视觉设计、Excel/Word 处理、仅阅读 PDF，或不涉及 TGO/GTLC 演示稿的任务不要触发；已加载后发现超出能力边界时按 handoff 模式移交。
---

# TGO/GTLC 演示稿生成技能

## 重要说明和介绍

以下说明为用户指定的受保护内容。AI 后续不得改写、删除、弱化或移动本节内容。

本 SKILL 是 TGO 鲲鹏会为了 AI 时代内容生成准备的 SKILL，内置了相应的模板，也可以做内容探讨，会使用不同的 SubAgent 做生成、校验，作者是杭州分会的肉山，欢迎使用。

## 版本

- 作者：肉山
- 当前版本：V1.1
- 模板包版本：V1；V1.1 不改变模板资产或排版几何算法。
- 核心变化：增加模式路由、负触发与 handoff、失败恢复、Skill manifest、隔离评测和 V1.1 Harness；单 Agent 为默认执行方式，正式或高风险任务再启用独立检查通道。

## 启动语

每次首次响应先说：

```text
我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。
```

## 先路由，再执行

1. 首先加载 `references/rule-routing-and-modes.md`，选择且只选择一个模式：`check_only`、`repair`、`convert`、`create`、`handoff`。
2. `description` 负责 Skill 是否应被隐式触发；`handoff` 只处理 Skill 已加载后发现的能力越界，不替代宿主路由。
3. 仅 `create`、`convert` 和重大 `repair` 强制进入完整澄清、日志、样片和交付流程。
4. `check_only` 默认只读：不强制创建 `Design.md`、`Content.md`、生成日志或 SSOT，也不得修改源文件。
5. 信息不足时只问会改变输出或不可逆操作的最少问题；可从源文件直接看出的信息不再询问。

## 总工作流

1. 加载 `references/workflow.md`，按已选模式进入对应阶段和确认门。
2. 只加载当前阶段需要的规则、场景、模板和视觉风格文件，不一次性读取全部引用。
3. `create`、`convert` 或重大 `repair` 按 `references/rule-intake.md` 补足输入；涉及 PPT/PDF 时确认“修改内容并套模板”或“只套模板不改内容”。
4. 生成或重大修改前按 `references/generation-log.md` 创建日志；`check_only` 与轻微 `repair` 按模式矩阵决定是否需要。
5. PPTX 新建/转换输出默认包含标题页后的空白 `嘉宾介绍` 页和最终 `感谢聆听` 页，细则见 `references/rule-ppt-structure.md`。
6. 样片确认后再完整生成；用户跳过确认时记录原因。
7. 输出后运行 `scripts/check_pptx_layout.py` 或 `scripts/check_html_layout.py`，并渲染/预览逐页复核。
8. 出错时加载 `references/rule-failure-recovery.md`，按错误码和重试边界修复最小层，不把失败样本写入封存 holdout。
9. 交付前按 `references/rule-validation.md` 验证；只有正式或高风险任务才要求独立生成、风格、文字通道和 SSOT。

## 渐进式加载索引

| 场景 | 必须加载 | 条件加载 |
| --- | --- | --- |
| 任意任务启动 | `references/rule-routing-and-modes.md`、`references/workflow.md` | `references/rule-intake.md`、`references/generation-log.md` |
| 失败、降级或恢复 | `references/rule-failure-recovery.md` | `references/skill-manifest.json` |
| PPT/PDF/Markdown/HTML 转换 | `references/conversion-workflows.md` | 按来源类型读取对应段落 |
| 首次设计澄清或模板选择 | `references/design/index.md`、`references/design/shared/design.md` | 场景、模板、视觉风格文件按用户选择加载 |
| GTLC 大会 | `references/design/scenarios/gtlc-conference/design.md` | 选择的模板与视觉风格 |
| TGO 日常活动分享 | `references/design/scenarios/tgo-daily-sharing/design.md` | 默认优先 `references/design/templates/tgo-daily/design.md` |
| 固定页、Logo、品牌结构 | `references/rule-ppt-structure.md` | 用户上传 Logo 时再读取相关替换规则 |
| 模板选择 | `references/rule-template-selection.md` | `references/template-manifest.json` 仅在需要机器可读摘要时读取 |
| 排版、溢出、半尺寸画布、首尾页、项目基本信息页 | `references/rule-layout-safety-v1.md` | `references/rule-page-styles.md` |
| 生成日志 | `references/generation-log.md` | `scripts/create_generation_log.py` |
| 独立检查通道与 SSOT | `references/rule-subagents.md` | 正式或高风险时加载 `references/rule-ssot-handoff.md` |
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
   - `loop-orange-white`：`references/design/templates/loop-orange-white/design.md`，仅当用户选择 `D｜LOOP Summit 橙白峰会风` 或明确要求 LOOP 分支样式时加载
4. 只读取用户选择或计划需要的视觉风格文件，不要把 `references/design/visual-styles/` 全部读入。
5. 当前目录的 `Design.md` 是本次任务决策记录，不要和 `references/design/**/design.md` 混用。

## 脚本入口

先设置 `SKILL_DIR` 为本技能所在目录，再从用户当前工作目录执行脚本：

```bash
SKILL_DIR="<gen-tgo-ppt-skill 目录>"
```

- 生成当前工作目录任务摘要：`python "$SKILL_DIR/scripts/scan_task_context.py" . --output task-context.json`
- 估算 Content/Markdown 文本密度：`python "$SKILL_DIR/scripts/content_budget.py" Content.md --format markdown`
- 压缩版型检查 JSON 报告：`python "$SKILL_DIR/scripts/summarize_layout_report.py" layout-check.json --format markdown`
- 对比 PPTX 与模板：`python "$SKILL_DIR/scripts/inspect_pptx_style.py" path/to/deck.pptx`
- 创建生成日志：`python "$SKILL_DIR/scripts/create_generation_log.py" --title "演示稿标题" --source "source.md" --format PPT`
- 检查 PPTX 版型：`python "$SKILL_DIR/scripts/check_pptx_layout.py" path/to/generated.pptx`
- 检查 HTML 演示稿：`python "$SKILL_DIR/scripts/check_html_layout.py" path/to/generated.html`
- 运行 V1.1 Harness：`python -B "$SKILL_DIR/scripts/run_v11_skill_checks.py"`；受限环境可用 `--temp-root <已存在且可写目录>` 显式指定隔离工作区。
- V1 兼容入口：`python -B "$SKILL_DIR/scripts/run_v1_skill_checks.py"`（单向委托 V1.1 Harness，并转发 `--temp-root`）
- Harness 找不到可写临时目录时只运行无写入门禁，fixture 门禁标为 `INSUFFICIENT` 并返回退出码 `3`，不得把未执行项计为 PASS。

运行脚本时从用户当前工作目录执行；脚本路径按本技能所在目录解析。
新增摘要脚本只用于预检和压缩上下文，不替代 `check_pptx_layout.py`、渲染预览、逐页复核或最终校验。

## 交付条件

交付门槛按模式执行：

- `check_only`：报告范围、证据、PASS/WARN/FAIL、限制；保持源文件不变。
- `repair`：记录修改与回滚点，对修改后的文件执行针对性检查和视觉复核。
- `convert` / `create`：更新日志，运行版型检查，逐页渲染复核，修复全部未批准 `FAIL`。
- 正式或高风险任务：`生成内容`、`检查风格`、`检查文字` 使用独立通道；不能使用独立子智能体时，只能声明“分离自检”，不得声称独立验证。
- `handoff`：说明越界原因、已知输入、建议接手能力和未执行操作，不伪造演示稿产物。

## 维护约束

- 不得改写、删除、弱化或移动“重要说明和介绍”。
- 新增细则优先写入 `references/rule-*.md`；机器事实写入 `references/skill-manifest.json`，不要复制成多份可写版本事实。
- 修改 Skill 版本时同步更新 README、`agents/openai.yaml`、Skill manifest、生成日志规则与脚本；模板包和排版算法版本独立维护。
- 不修改 `assets/**`、`references/design/**` 或 V1 排版算法，除非任务明确授权并新增相应结果级验证。
