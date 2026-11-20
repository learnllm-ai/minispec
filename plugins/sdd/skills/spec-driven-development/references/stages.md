# SDD 工作阶段

本 skill 不定义特定 agent 的斜杠命令。工具可以提供自己的命令适配，也可以直接用自然语言要求执行某个阶段：

```text
使用 spec-driven-development skill。阶段：next。补充信息：<输入>
```

各阶段的可选输入都是普通自然语言；省略时根据当前项目和已有规格推断，无法唯一确定时询问用户。一次只推进一个阶段。

## `init`

输入：可选的项目简介、目标用户、技术限制、交付要求或明确不做什么。

作用：创建或补齐 `specs/mission.md`、`specs/tech-stack.md`、`specs/roadmap.md`。没有输入时优先读取 `prd.md`、现有文档和代码；仍缺关键信息时再提问。只写项目级规格，不写实现。

示例：

```text
使用 spec-driven-development skill 执行 init。
项目是一个本地 Markdown 笔记 CLI，使用 TypeScript，只支持 macOS。
```

## `status`

输入：无。

作用：只读查看当前 phase、feature、已有产物、验证状态和阻塞项，并推荐一个下一步阶段。不修改文件。

## `next`

输入：可选的 phase 编号/名称、功能描述、范围约束或验收偏好。

作用：把 roadmap 中的一个 phase 转成完整 feature 规格，创建 `requirements.md`、`plan.md`、`validation.md`，不写实现。没有输入时选择下一个未完成且前置条件满足的 phase。

如果输入要求 roadmap 之外的功能，先确认是否需要 `replan`。

示例：

```text
使用 spec-driven-development skill 执行 next。
范围：增加 Markdown 导出，只做 CLI，不改编辑器。
```

## `implement`

输入：可选的 feature 目录和范围约束。

作用：按当前 feature 的 `plan.md` 实现并做实现者自检，在正式验证前停止。没有输入时根据当前分支、roadmap 和 feature 规格定位；不唯一时询问。

范围约束只能收缩或澄清已确认规格，不能扩大 feature。

## `verify`

输入：可选的 feature 目录。

作用：在干净上下文中独立执行 `validation.md`，只报告，不修代码。不得由刚刚实现 feature 的会话执行正式验收。

## `finish`

输入：可选的 feature 目录和交付说明。

作用：在用户确认验证结果后，更新 `CHANGELOG.md` 和 `specs/roadmap.md`，准备当前 phase 的提交或合并。没有输入时定位当前待收尾 feature。提交、合并和删除分支前仍请求确认。

## `replan`

输入：可选的新决策或重排目标。

作用：根据新的全局要求或执行偏差，更新 `mission.md`、`tech-stack.md`、`roadmap.md`，不改实现代码。没有输入时先询问这次 replanning 要解决什么。

## 推荐顺序

```text
init
next
implement
verify（干净上下文）
finish
```

`status` 可以随时只读执行；`replan` 在新全局决策出现、顶层规格与现实不一致或 roadmap 需要重排时执行。
