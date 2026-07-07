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
- Sample output path and user feedback.
- Final PPTX/HTML paths.
- Render/preview checks and per-slide layout fixes.
- `检查风格` findings and fixes.
- `检查文字` findings and fixes.
- Deferred issues approved by the user.

## Starter Template

```markdown
# gen-tgo-ppt 生成日志

- Skill 版本：v0.5
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

## 样片

## 完整输出

## 逐页版型校对

## 检查风格

## 检查文字

## 待处理问题
```
