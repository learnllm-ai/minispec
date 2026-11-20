---
description: Update project-level SDD specs after a new global decision or roadmap drift.
argument-hint: "[new decision or replanning goal]"
---

# Replan the Project

用户提供的新决策或重排目标：$ARGUMENTS

使用当前宿主已安装的 `spec-driven-development` skill。若无法按名称加载，先定位配套的 `SKILL.md`。

1. 没有新决策或重排目标时，先询问这次 replanning 要解决什么。
2. 判断受影响的是 `mission.md`、`tech-stack.md` 还是 `roadmap.md`。
3. 写文件前说明准备修改哪些文件及原因，取得用户确认。
4. 只更新受影响的顶层规格，并同步剩余 phase 的顺序。

本命令不改实现代码。完成后提示用户从 `next` 开始后续工作。
