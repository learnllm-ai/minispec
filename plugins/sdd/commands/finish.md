---
description: Close a verified feature by updating the roadmap and changelog.
argument-hint: "[feature directory] [delivery note]"
---

# Finish the Current Feature

用户指定或补充的信息：$ARGUMENTS

使用当前宿主已安装的 `spec-driven-development` skill。若无法按名称加载，先定位配套的 `SKILL.md`。

- 当前 feature 的 `validation.md` 已有执行结果。
- 阻塞失败项已修复，或用户明确接受残余风险。
- 未执行的检查不能标记为通过。

条件不满足时停止。

1. 根据 feature 分支的 Git 提交记录创建或更新 `CHANGELOG.md`。
2. 在 `specs/roadmap.md` 中把对应 phase 标记为 `✅`。
3. 核对 requirements、plan、validation、实现和 changelog。
4. 展示收尾 diff，并提出提交或合并建议。

提交、切换主分支、合并和删除 feature 分支前先取得确认，并保留用户已有改动。
