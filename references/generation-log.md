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
- Scene: GTLC or daily sharing.
- Output format: PPT, HTML, or both.
- Selected visual style numbers and any per-page/per-section mapping.
- Template choice: white, light, dark, or mixed.
- Content optimization decision and approved edits.
- Confirmed page count and slide-by-slide outline.
- Sample output path and user feedback.
- Final PPTX/HTML paths.
- Render/preview checks and fixes.
- `检查风格` findings and fixes.
- `检查文字` findings and fixes.
- Deferred issues approved by the user.

## Starter Template

```markdown
# gen-tgo-ppt 生成日志

- Skill 版本：v0.4
- 创建时间：
- 当前目录：
- 来源：
- 场景：
- 输出格式：
- 风格选择：
- 模板选择：

## 内容探讨

## 页数与大纲

## 样片

## 完整输出

## 检查风格

## 检查文字

## 待处理问题
```
