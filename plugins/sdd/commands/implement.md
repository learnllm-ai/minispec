---
description: Implement the current feature from its SDD plan and stop before formal validation.
argument-hint: "[feature directory] [scope constraint]"
---

# Implement the Current Feature

用户指定或补充的信息：$ARGUMENTS

使用当前宿主已安装的 `spec-driven-development` skill。若无法按名称加载，先定位配套的 `SKILL.md`。重点读取 `references/feature-loop.md`。

1. 根据输入、当前分支、roadmap 和 `specs/*-*/` 定位当前 feature；仍不唯一时询问。
2. 完整读取该 feature 的 `requirements.md`、`plan.md`、`validation.md`，核对三者一致。
3. 规格缺失、冲突或未确认时停止，先修正规格。
4. 按 `plan.md` 实现，遵守 `specs/tech-stack.md` 和仓库约定；未经批准不新增依赖或扩大范围。
5. 发现规格偏差时同步更新当前 feature 的三份规格。
6. 执行 plan 要求的实现者自检，记录真实结果。

本命令不执行正式验收。完成后提示用户在新会话执行 `verify`。
