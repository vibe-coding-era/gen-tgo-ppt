# V1.1 失败分类与恢复规则

先归类失败，再只修改最小责任层。每次失败必须留下稳定错误码、阶段、证据和下一动作；面向用户的错误不得只给原始 traceback。

## 错误合同

| 分类 | 错误码 | 可重试 | 处理 |
| --- | --- | --- | --- |
| routing | `E_ROUTE_AMBIGUOUS` | 是 | 询问一个决定模式的问题 |
| routing | `E_ROUTE_OUT_OF_SCOPE` | 否 | 进入 `handoff`，不伪造产物 |
| process | `E_INPUT_MISSING` | 是 | 列出最小缺失输入或采用明确降级 |
| grounding | `E_INPUT_UNCONFIRMED` | 是 | 只展示候选文件名/时间并请求用户选择；确认前不读取正文、不写日志或产物 |
| process | `E_WORKDIR_READONLY` | 条件式 | 停止写入，索取可写目录 |
| process | `E_OUTPUT_EXISTS` | 条件式 | 预览目标并取得覆盖确认，或改用新文件名 |
| grounding | `E_SOURCE_UNREADABLE` | 条件式 | 报告损坏/不支持格式并请求替代来源 |
| output | `E_DEPENDENCY_MISSING` | 条件式 | 列出发行包名和受影响命令；安装后重试 |
| output | `E_VALIDATION_FAIL` | 是 | 修复失败页后只重跑受影响检查与最终全量门禁 |
| output | `E_RENDER_UNAVAILABLE` | 条件式 | 标记降级，不能把静态检查冒充视觉验证 |
| efficiency | `E_RETRY_EXHAUSTED` | 否 | 同一确定性操作两次失败后停止，保留证据并移交 |
| governance | `E_SSOT_CONFLICT` | 是 | 按用户要求、安全规则、模式合同、默认值顺序裁决 |
| governance | `E_INSTALL_DRIFT` | 否 | 停止同步，先核对安装副本中的未知修改 |
| governance | `E_EVAL_INVALID` | 否 | 修复 schema/hash/split 后重跑 |
| governance | `E_EVAL_INSUFFICIENT` | 否 | 只能声明证据不足，不能声明行为或效果通过 |

脚本错误建议格式：`<ERROR_CODE>: <human-readable message>; action=<next step>`。CLI 应返回非零退出码，并把可预期错误压缩为稳定信息；只有显式调试模式才输出完整 traceback。

## 重试和降级

1. 同一输入、同一命令的确定性重试最多两次；重试前必须改变导致失败的条件。
2. 缺依赖、不可写目录、已有输出或缺宿主能力不能靠盲重试解决。
3. 静态检查通过只证明结构；真实模型观测才证明路由行为；对真实生成物的渲染与人工/程序检查才支持结果质量。
4. 无法渲染时可以交付静态检查报告，但必须标记 `degraded`，不得写“逐页视觉检查已完成”。

## 安全写入

对覆盖、批量修改或外部写入遵循：预览目标 → 明确确认 → 执行 → 事后核对。默认保留来源文件；修复或转换优先创建带版本后缀的新产物。

## 失败样本与评测隔离

- 生产失败样本只能加入 `routing-regression.json` 的后续版本，并记录修复原因。
- `routing-holdout.json` 是发布评测集；不得因看到失败结果而即时改写 gold、prompt 或阈值。
- fixture 结果只能标 `structural_fixture`；没有真实模型运行记录时不得标 `observed_model_behavior`。
