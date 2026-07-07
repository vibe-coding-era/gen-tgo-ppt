# Generation Log

Every generation run must leave a Markdown log in the user's current working directory.

## File Rule

- Location: the current working directory where the user invoked the skill.
- Filename: `gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md`.
- Timing: create before generating the first sample page or full PPTX/HTML.
- Delivery: include the log path in the final response.
- Blocker: if the current directory is not writable, stop before generation and ask for a writable directory.

## Required Content

Record these items as the run progresses:

- Source file or pasted-content description.
- `Design.md` path and design intake summary.
- `Content.md` path and text-draft summary.
- Scene: GTLC大会 or TGO日常活动分享.
- Spec: default 16:9 or another confirmed ratio.
- Output format: PPT, HTML, or both.
- PPT/PDF processing mode: modify content + apply template, or template-only.
- Logo replacement decision and uploaded logo path if applicable.
- Selected visual style numbers and any per-page/per-section mapping.
- Template choice: white, light, dark, or mixed.
- Content optimization decision and approved edits.
- Confirmed page count and slide-by-slide outline, including the mandatory PPT `嘉宾介绍` and `感谢聆听` pages.
- Per-slide v0.6 layout safety budget: title/body line estimates, density risk, keep-out zones, and split/fit plan.
- Sample output path and user feedback.
- Final PPTX/HTML paths.
- PPTX layout-check command and PASS/WARN/FAIL results when applicable.
- Generation subagent and validation subagents, with confirmation that generation and validation used different subagents.
- Render/preview checks and per-slide layout fixes.
- `检查风格` findings and fixes.
- `检查文字` findings and fixes.
- Deferred issues approved by the user.

## Starter Template

```markdown
# gen-tgo-ppt 生成日志

- Skill 版本：v0.6
- 排版安全版本：v0.6
- 创建时间：
- 当前目录：
- Design.md：
- Content.md：
- 来源：
- 场景：
- 规格：
- 输出格式：
- 处理模式：
- Logo替换：
- 风格选择：
- 模板选择：
- 生成 subagent：
- 校验 subagent：
- 生成/校验是否不同 subagent：

## 设计澄清

- 应用场景：
- 规格：
- 处理模式：
- Logo替换：
- PPT固定页：
  - 标题页后：嘉宾介绍
  - 结束页：感谢聆听

## 内容探讨

- 主题、问题：
- 思考模式：

## 页数与大纲

- 逐页排版预算：

## 样片

## 完整输出

## v0.6 排版安全校验

- 检查命令：
- 检查结果：
- FAIL/WARN 页面：
- 修复动作：
- 复查结果：

## Subagent 分工

- `生成内容`：
- `检查风格`：
- `检查文字`：
- 生成者是否参与校验：
- 如果未使用独立 subagent，原因：

## 逐页版型校对

## 检查风格

## 检查文字

## 待处理问题
```
