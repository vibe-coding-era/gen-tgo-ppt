# TGO鲲鹏会 GTLC/日常分享 PPT/HTML 演示稿生成 Skill

作者：肉山@TGO 杭州分会
版本：V1
Skill 名称：`gen-tgo-ppt-skill`

这是一个用于生成、改造和校验 TGO 鲲鹏会、GTLC 大会与日常分享材料的 Codex Skill。它可以把 PPT、PDF、Markdown、HTML、粘贴文本或现有演示稿，整理成符合 TGO/GTLC 风格的 PPTX 或 HTML 演示稿。

本 README 是给使用者和维护者看的简版说明；执行细则以 `SKILL.md`、`references/` 和 `scripts/` 为准。

## 适用场景

- GTLC 大会复盘、议程、招商、权益、项目汇报和董事会材料。
- TGO 鲲鹏会日常活动分享、主题演讲、会员交流和城市分会内容。
- 既有 PPT 套模板、优化版式、修复文字溢出、统一视觉风格。
- 从 Markdown、HTML、PDF 或粘贴内容生成新的 PPT/HTML 演示稿。
- 需要生成日志、样片确认、逐页渲染校验和交付证据链的正式材料。

## 核心能力

- 内容讨论：先澄清场景、目标、受众、规格、模板、风格和输出格式。
- 模板套版：支持 GTLC 主模板、TGO 日常分享模板和 LOOP Summit 橙白分支样式。
- PPT/HTML 输出：可生成 PPTX，也可生成 HTML 演示稿。
- 渐进式加载：按任务只读取需要的规则、模板和风格文件，降低上下文负担。
- 固定页规则：PPT 默认包含标题页后的 `嘉宾介绍` 页和末尾 `感谢聆听` 页。
- 多角色检查：生成内容、检查风格、检查文字尽量由不同子智能体或分离步骤完成。
- 质量校验：通过脚本检查 PPTX/HTML 版型、文本溢出、重叠、Logo/页脚碰撞等问题。
- 生成日志：每次正式生成前创建并维护 `gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md`。

## 输入与输出

常见输入：

- `Design.md`：场景、规格、风格、模板、Logo、输出格式等设计决策。
- `Content.md`：主题、提纲、正文、讲稿、页面结构或原始材料。
- `.pptx`：现有演示稿，可选择改内容并套模板，或只套模板不改内容。
- `.pdf`、`.md`、`.html`、粘贴文本：可转成 PPTX/HTML 演示稿。
- Logo、图片、截图、参考样式：可作为品牌或视觉素材使用。

常见输出：

- PPTX 演示稿。
- HTML 演示稿。
- 渲染预览图或总览图。
- 生成日志。
- PPTX/HTML 检查报告。
- SSOT 交接记录或任务证据文档。

## 内置模板与风格

主模板：

- `white`：白底内容页，适合正式文档、打印和密集内容。
- `light`：浅蓝灰内容页，适合多数 GTLC 商务汇报。
- `dark`：深蓝渐变，适合开场、收尾、章节页和强叙事 keynote。
- `tgo-daily`：TGO 日常分享模板，适合非 GTLC 日常活动。
- `loop-orange-white`：LOOP Summit 橙白峰会风，适合 AI 生态大会、招商权益和活动传播材料。

视觉风格：

- 内置 9 类风格：董事会汇报、硅谷科技、大厂 Keynote、AI Native、数据智能、极简高级、中国商务、创意节庆、企业 AI 咨询。
- 可以按页面混用，例如“封面用 3，内容页用 1，AI 架构页用 9”。

## 如何使用

在 Codex 中直接说明要使用本 Skill，并给出材料或目标。例如：

```text
使用 $gen-tgo-ppt-skill，把 Content.md 生成一份 GTLC 大会复盘 PPT，风格偏董事会汇报，输出 PPTX。
```

```text
使用 $gen-tgo-ppt-skill，把这个 PPT 套成 TGO 日常分享模板，只改版式，不改内容。
```

```text
使用 $gen-tgo-ppt-skill，根据这段文字生成 HTML 演示稿，适合 TGO 杭州分会日常分享。
```

推荐提供的信息：

- 用途：GTLC 大会、TGO 日常分享、招商材料、复盘汇报等。
- 输出：PPTX、HTML，或两者都要。
- 规格：16:9、页数范围、是否需要演讲稿。
- 内容：主题、提纲、正文、已有文件或粘贴材料。
- 风格：模板 key、视觉风格编号、参考图或参考 PPT。
- Logo：是否使用默认 GTLC/TGO Logo，是否替换为上传 Logo。

执行流程：

1. Codex 先说启动语，并询问缺失的关键选择。
2. 按需创建或补齐 `Design.md` 和 `Content.md`。
3. 选择场景、模板、视觉风格和输出格式。
4. 生成页面计划和样片。
5. 样片确认后生成完整 PPTX/HTML。
6. 运行版型检查脚本并逐页复核。
7. 更新生成日志，交付最终文件和检查结论。

## 质量标准

交付前至少满足：

- 已创建并更新生成日志。
- 已按需加载独立规则文件，没有把所有上下文一次性塞入。
- PPTX 输出通过 `scripts/check_pptx_layout.py`，HTML 输出通过 `scripts/check_html_layout.py`。
- 每页已预览或渲染检查，处理文本溢出、裁切、重叠、Logo/页脚碰撞。
- 固定页顺序正确，标题页后有 `嘉宾介绍` 页，末尾有 `感谢聆听` 页。
- 风格检查和文字检查与生成步骤分离；无法使用独立子智能体时，需要在日志里说明。

## 如何增加新模板

新增模板时，要同步模板资产、设计说明、索引、模板选择规则、manifest 和验证脚本。推荐使用短横线 key，例如 `sponsor-blue`、`city-roadshow`。

### 方式 A：在 Codex 中加入

把模板文件交给 Codex，并说明模板 key、适用场景和默认使用条件。示例：

```text
请把 /path/to/new-template.pptx 加入 gen-tgo-ppt-skill，模板 key 为 sponsor-blue。
适用于 GTLC 大会赞助招商材料，默认不替代 light/white/dark。
请生成设计说明，更新索引、manifest、模板选择规则，并运行 V1 Harness。
```

Codex 应完成：

1. 复制 PPTX 到 `assets/design/templates/<template-key>/`。
2. 检查 PPTX 尺寸、母版、版式、字体、颜色、Logo、页脚和背景资产。
3. 创建 `references/design/templates/<template-key>/design.md`。
4. 更新 `references/design/index.md` 的模板加载路由。
5. 更新 `references/rule-template-selection.md` 的模板资产、默认选择或适用场景。
6. 更新 `references/template-manifest.json` 的 `design_resources.templates` 和 `templates`。
7. 如需展示，补充 `assets/design/previews/templates/` 下的预览图或 contact sheet。
8. 如新增场景或分支样式，按需更新 `SKILL.md` 的渐进式加载索引和相关 rule 文件。
9. 运行 V1 校验：

```bash
python /Users/Rou/.codex/skills/gen-tgo-ppt-skill/scripts/run_v1_skill_checks.py
```

### 方式 B：直接放入文件夹

先按固定目录放入模板文件和设计说明，再让 Codex 或维护者补齐索引。

推荐目录：

```text
assets/design/templates/<template-key>/
  <template-key>.pptx

references/design/templates/<template-key>/
  design.md
```

`design.md` 至少写清：

```markdown
# <Template Name> Template Design

## Asset

- PPTX: `assets/design/templates/<template-key>/<template-key>.pptx`
- Visual role:
- Default scene:
- Not default for:

## Layouts

- `<layout name>`:

## Key Positions

- Cover title:
- Default content title:
- Default content body:
- Logo:
- Footer:

## Use

- Best for:
- Avoid for:
- Validation notes:
```

放入文件后，必须更新：

- `references/design/index.md`
- `references/rule-template-selection.md`
- `references/template-manifest.json`
- 必要时更新 `SKILL.md`、`agents/openai.yaml`、`references/generation-log.md`

然后运行验证：

```bash
python /Users/Rou/.codex/skills/gen-tgo-ppt-skill/scripts/inspect_pptx_style.py assets/design/templates/<template-key>/<template-key>.pptx
python /Users/Rou/.codex/skills/gen-tgo-ppt-skill/scripts/run_v1_skill_checks.py
```

## 新模板验收标准

- 模板文件存在于 `assets/design/templates/<template-key>/` 或明确的分支样式目录。
- `references/design/index.md` 能路由到模板设计文件。
- `references/template-manifest.json` 中相关 `assets/`、`references/`、`scripts/` 路径存在。
- 模板选择规则写清默认使用、适用场景和避免场景。
- 不改写、删除、弱化或移动 `SKILL.md` 中的“重要说明和介绍”。
- PPTX 输出仍必须通过 `check_pptx_layout.py`，HTML 输出仍必须通过 `check_html_layout.py`。

## 维护提示

- 功能规则优先写入 `references/rule-*.md`，不要把细则堆回 `SKILL.md`。
- 模板体系变化时，同步更新 README、manifest、模板选择规则和生成日志规则。
- 发布前运行 `scripts/run_v1_skill_checks.py`，确保 V1 Harness 通过。

## GitHub

- 仓库地址：[vibe-coding-era/gen-tgo-ppt.git](https://github.com/vibe-coding-era/gen-tgo-ppt.git)
