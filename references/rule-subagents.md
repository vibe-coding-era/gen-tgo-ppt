# 子智能体分工规则

## 固定名称

用户可见的子智能体名称必须使用：

- `生成内容`
- `检查风格`
- `检查文字`

不要在用户可见计划、日志和回复中使用英文 worker 名称。v0.8 起，除这三个基础角色外，所有独立规则都必须有独立规则子智能体。

## 职责

- `生成内容`：负责样片、完整 PPTX 或 HTML 生成。
- `检查风格`：只检查视觉、模板、版式、安全区、渲染、对比度、Logo、页脚、背景、异常换行和页面节奏。
- `检查文字`：只检查中文表达、错别字、逻辑、来源忠实度、标题准确性、内容密度、重复表达和是否需要拆页。

## 规则子智能体

每个已加载 rule 文件必须由不同子智能体独立执行或检查。默认命名：

| 规则文件 | 子智能体 |
| --- | --- |
| `references/rule-intake.md` | `规则-澄清` |
| `references/rule-ppt-structure.md` | `规则-结构` |
| `references/rule-template-selection.md` | `规则-模板` |
| `references/rule-layout-safety-v08.md` | `规则-排版` |
| `references/rule-page-styles.md` | `规则-页型` |
| `references/rule-validation.md` | `规则-校验` |
| `references/rule-guardrails.md` | `规则-守护` |
| `references/generation-log.md` | `规则-日志` |
| `references/conversion-workflows.md` | `规则-转换` |
| `references/rule-ssot-handoff.md` | `SSOT-合并` |

同一个子智能体不得同时负责两个不同 rule 文件；`SSOT-合并` 只负责汇总裁决，不生成、不修图、不改稿、不替代其他规则检查。

## 职责分离

- 生成和校验必须职责分离。
- `生成内容` 不得批准自己的输出。
- `检查风格` 和 `检查文字` 必须不同于 `生成内容`。
- 不同 rule 必须由不同规则子智能体独立执行，不能由同一个子智能体连续代审多个 rule。
- 如果工具策略不允许创建子智能体，主流程可以做分离自检，但必须在 SSOT、生成日志和最终回复中说明限制。

## 交接要求

- 每个规则子智能体只读取自己的 rule 文件、必要任务材料和上游 SSOT 摘要。
- 每个规则子智能体必须按 `references/rule-ssot-handoff.md` 输出结构化交接。
- 不同规则子智能体之间不直接改写对方结论，只把冲突提交给 `SSOT-合并`。
- `SSOT-合并` 负责形成唯一执行计划和最终交付摘要。

## 记录要求

生成日志必须记录：

- 生成者
- 风格检查者
- 文字检查者
- 规则子智能体分工表
- 每个 rule 的交接结论
- SSOT 路径或 SSOT 区块
- 是否满足生成/校验分离
- 不满足时的原因
