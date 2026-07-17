# V1.1 生成日志规则

## 何时需要

- `create`、`convert`、重大 `repair`：在样片或完整写入前必须创建。
- 轻微 `repair`：可使用简化日志，但必须记录来源、修改、检查与回滚点。
- `check_only`：默认不创建；正式审计需要耐久证据时才创建。
- `handoff`：不创建生成日志，只写移交摘要。

当前目录不可写时返回 `E_WORKDIR_READONLY`，不要把日志静默写到其他目录。

## 版本口径

- Skill 版本：`V1.1`。
- 排版安全版本：`V1`。
- 模板包版本：`V1.1`。
- Skill、模板包与排版安全版本独立演进，不得互相推导。

## 文件规则

- 文件名：`gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md`。
- 默认拒绝覆盖同名日志；可先用 `scripts/create_generation_log.py --dry-run` 预览。
- `create`、`convert`、`repair` 调用日志脚本时必须传入 `--source-authority current_turn|explicit_path|confirmed_workspace|confirmed_continuation`；缺失时返回 `E_INPUT_UNCONFIRMED` 且不得写文件。
- 最终回复给出日志路径，并在交付前更新结果和遗留问题。

## 必填内容

模式、执行意图证据、Skill/排版版本、时间、工作目录、已确认输入及归属、来源、场景、规格、格式、处理模式、Logo、模板/风格、Design/Content、内容改写边界、页纲与文本预算、样片决定、输出、检查命令与结果、渲染证据、失败码与恢复、通道分工及其真实性、SSOT（若适用）、用户批准例外和遗留问题。

## 模板骨架

```markdown
# gen-tgo-ppt 生成日志

- Skill 版本：V1.1
- 排版安全版本：V1
- 模板包版本：V1.1
- 任务模式：create / convert / repair / check_only
- 执行意图证据：
- 创建时间：
- 当前目录：
- 任务标题：
- Design.md：
- Content.md：
- 来源：
- 输入归属：current_turn / explicit_path / confirmed_workspace / confirmed_continuation / not_applicable
- 场景 / 规格 / 输出格式：
- 处理模式 / Logo / 模板 / 风格：

## 澄清与内容边界
## 页数、大纲与文本预算
## 样片与用户决定
## 完整输出
## PPTX/HTML 检查与逐页复核
## 失败、重试与降级
## 通道分工与交接
## SSOT（若适用）
## 操作记录
## 遗留问题
```
