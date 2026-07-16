# TGO鲲鹏会 GTLC/日常分享 PPTX/HTML Skill

- 作者：肉山@TGO 杭州分会
- Skill 版本：V1.1
- 模板包 / 排版安全版本：V1
- Skill 名称：`gen-tgo-ppt-skill`

这是一个用于生成、转换、修复和校验 TGO 鲲鹏会、GTLC 大会与日常分享演示材料的 Codex Skill。它接受 PPT、PDF、Markdown、HTML、粘贴文本或既有演示稿，输出 PPTX、HTML 和相应检查证据。

README 面向使用者和维护者；执行入口以 `SKILL.md` 为准，机器事实以 `references/skill-manifest.json` 为准，模板资产事实以 `references/template-manifest.json` 为准。

## V1.1 的变化

- 入口同时声明正触发、负触发和加载后的 handoff 边界。
- 增加 `check_only`、`repair`、`convert`、`create`、`handoff` 五种模式。
- 单 Agent 为默认；正式或高风险交付再启用独立的生成、风格、文字通道。
- 增加失败分类、稳定错误码、重试上限和安全写入合同。
- 增加 Skill manifest，明确 Python、第三方发行包、脚本副作用和宿主能力。
- 增加回归/holdout 语料与评测器，明确区分结构 fixture 与真实模型行为。
- `run_v11_skill_checks.py` 成为当前 Harness；`run_v1_skill_checks.py` 保留为单向兼容入口。
- V1.1 不改变模板资产、排版几何阈值或现有 PPTX/HTML 检查算法。

## 何时使用

适用：

- GTLC 大会复盘、议程、招商、权益、项目汇报和董事会材料。
- TGO 日常活动分享、主题演讲、会员交流和城市分会内容。
- 既有 PPTX 套模板、修复版式、统一 TGO/GTLC 风格或只读审计。
- 从 PDF、Markdown、HTML 或文本生成/转换 PPTX 或 HTML 演示稿。

不适用：普通文章写作、Excel/Word 处理、通用海报/网页设计、仅阅读 PDF，或完全不涉及 TGO/GTLC 演示稿的任务。这些任务不应触发本 Skill；若已加载后才发现越界，使用 `handoff`。

## 五种模式

| 模式 | 用途 | 默认写入 | 日志/SSOT |
| --- | --- | --- | --- |
| `check_only` | 只读检查、审计、评价 | 不写源文件 | 默认不强制；正式审计可创建 |
| `repair` | 修复既有 PPTX/HTML | 默认写新版本文件 | 重大修复需要日志，正式/高风险需要 SSOT |
| `convert` | 来源格式转成 PPTX/HTML | 创建新产物 | 日志必需，正式/高风险需要 SSOT |
| `create` | 从主题、提纲或素材新建 | 创建新产物 | 日志必需，正式/高风险需要 SSOT |
| `handoff` | 已加载后发现能力越界 | 不写演示稿 | 只给移交摘要 |

## 核心能力与模板

- 渐进式加载场景、模板、视觉风格和规则，避免一次性灌入全部上下文。
- 支持 `white`、`light`、`dark`、`tgo-daily`、`loop-orange-white` 模板。
- 内置九类视觉风格，可按页组合。
- 新建/转换 PPTX 默认包含标题页后的 `嘉宾介绍` 页和末尾 `感谢聆听` 页。
- 提供 PPTX/HTML 静态检查、内容预算、任务上下文扫描和检查报告压缩脚本。
- 对正式/高风险任务使用 `生成内容`、`检查风格`、`检查文字` 独立通道；工具不可用时只声明分离自检。

## 使用示例

```text
使用 $gen-tgo-ppt-skill，把 Content.md 生成一份 GTLC 大会复盘 PPTX，董事会汇报风格。
```

```text
使用 $gen-tgo-ppt-skill，只检查这个季度汇报 PPT 的版式和文字，不要修改文件。
```

```text
使用 $gen-tgo-ppt-skill，把现有 PPT 套成 TGO 日常分享模板，只改版式，不改内容。
```

推荐提供用途、输出格式、规格、内容来源、模板/视觉偏好和 Logo 决定。Skill 只追问无法从材料推断且会改变产物的问题。

## 执行与质量门禁

生成或重大修改的典型流程：模式选择 → 最小澄清 → 页纲/预算 → 日志 → 样片 → 完整产物 → 静态检查 → 逐页渲染 → 返工 → 交付。

关键门禁：

- 默认保留来源，覆盖或批量写入需预览、确认、执行和事后核对。
- 修复所有未批准的检查器 `FAIL`，并人工判断 `WARN`。
- 逐页检查溢出、裁切、重叠、异常换行、字号、Logo/页脚和固定页。
- 无法渲染时标记降级，不能把静态检查写成视觉质量验证。
- 结构 fixture、真实模型路由和真实产物质量是三种不同证据。

## 脚本

先把 `SKILL_DIR` 指向 Skill 根目录，再从任务目录执行：

```bash
python -B "$SKILL_DIR/scripts/scan_task_context.py" . --output task-context.json
python -B "$SKILL_DIR/scripts/content_budget.py" Content.md --format markdown
python -B "$SKILL_DIR/scripts/create_generation_log.py" --mode create --title "演示稿标题" --dry-run
python -B "$SKILL_DIR/scripts/check_pptx_layout.py" output.pptx
python -B "$SKILL_DIR/scripts/check_html_layout.py" output.html
python -B "$SKILL_DIR/scripts/inspect_pptx_style.py" source.pptx
python -B "$SKILL_DIR/scripts/summarize_layout_report.py" layout-check.json --format markdown
```

当前维护门禁：

```bash
python -B scripts/run_v11_skill_checks.py
python -B scripts/run_v11_skill_checks.py --temp-root /path/to/existing-writable-dir
```

Harness 默认依次使用 `GEN_TGO_PPT_TEMP_ROOT` 和系统临时目录；显式路径必须已经存在且可写。若没有可写临时目录，无写入检查仍会执行，但依赖 fixture 写入的门禁会标为 `INSUFFICIENT`，进程返回 `3`，不会把未执行项算成 PASS。

V1 兼容入口仍可用，但只会委托当前 V1.1 Harness：

```bash
python -B scripts/run_v1_skill_checks.py
python -B scripts/run_v1_skill_checks.py --temp-root /path/to/existing-writable-dir
```

路由评测示例：

```bash
python -B scripts/evaluate_v11_contract.py \
  references/evals/routing-regression.json \
  references/evals/evaluator-smoke-observations-regression.json
```

fixture PASS 只证明评测器和语料结构自洽，不证明真实模型行为。行为结论必须来自隔离上下文的真实观察；结果质量结论还必须有真实输出和渲染证据。

## 如何增加新模板

### 方式 A：在 Codex 中加入

把模板文件交给 Codex，并说明模板 key、适用场景和默认条件，例如：

```text
请把 /path/to/new-template.pptx 加入 gen-tgo-ppt-skill，key 为 sponsor-blue；
适用于 GTLC 招商材料，不替代 light/white/dark。请更新设计说明、索引、manifest，并运行 V1.1 Harness。
```

Codex 应完成：复制资产、检查母版/版式/字体/颜色/Logo/页脚、创建模板 `design.md`、更新设计索引和模板选择规则、更新 template manifest、补充预览（若需要），最后运行 Harness 和真实 PPTX 检查。

### 方式 B：直接放入文件夹

推荐结构：

```text
assets/design/templates/<template-key>/<template-key>.pptx
references/design/templates/<template-key>/design.md
```

`design.md` 至少写清资产路径、视觉角色、默认/避免场景、版式、关键位置和验证说明。随后更新：

- `references/design/index.md`
- `references/rule-template-selection.md`
- `references/template-manifest.json`
- 必要时更新 `SKILL.md` 的渐进加载路由

新增模板不能改写或移动 `SKILL.md` 中的受保护说明段；模板产物仍需通过 PPTX 检查与真实渲染复核。

## 维护与发布边界

- 功能规则写入 `references/rule-*.md`，机器事实只写入 Skill manifest。
- Skill 版本、模板包版本、排版算法版本独立维护。
- 发布前先跑 V1.1 Harness，再执行与改动风险相匹配的真实产物测试。
- 本地验证通过不等于已提交、推送或发布；这些动作需单独授权。

## GitHub

- [vibe-coding-era/gen-tgo-ppt](https://github.com/vibe-coding-era/gen-tgo-ppt)
