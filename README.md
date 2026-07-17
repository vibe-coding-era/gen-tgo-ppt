# TGO鲲鹏会 GTLC/日常分享 PPTX/HTML Skill

- 作者：肉山@TGO 杭州分会
- Skill 版本：V1.1
- 模板包版本：V1.1；排版安全版本：V1
- Skill 名称：`gen-tgo-ppt-skill`

这是一个用于生成、转换、修复和校验 TGO 鲲鹏会、GTLC 大会与日常分享演示材料的 Codex Skill。它接受 PPT、PDF、Markdown、HTML、粘贴文本或既有演示稿，输出 PPTX、HTML 和相应检查证据。

## 何时使用

适用：

- GTLC 大会复盘、议程、招商、权益、项目汇报和董事会材料。
- TGO 日常活动分享、主题演讲、会员交流和城市分会内容。
- 既有 PPTX 套模板、修复版式、统一 TGO/GTLC 风格或只读审计。
- 从 PDF、Markdown、HTML 或文本生成/转换 PPTX 或 HTML 演示稿。

不适用：普通文章写作、Excel/Word 处理、通用海报/网页设计、仅阅读 PDF，或完全不涉及 TGO/GTLC 演示稿的任务。这些任务不应触发本 Skill；若已加载后才发现越界，使用 `handoff`。



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

```text
使用 $gen-tgo-ppt-skill，模板选择 LOOP 大会，只套模板不改内容。
```

推荐提供用途、输出格式、规格、内容来源、模板/视觉偏好和 Logo 决定。Skill 只追问无法从材料推断且会改变产物的问题。

仅输入“运行此 SKILL”或只点名 `$gen-tgo-ppt-skill` 时，Skill 只启动并返回 `E_ROUTE_AMBIGUOUS`，不会读取当前目录中的旧材料或自动进入 `create`。目录里的文件只有被本轮请求明确点名或经用户确认后，才成为有效输入。



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
