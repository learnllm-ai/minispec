---
description: Show the current SDD stage and the single best next step.
---

# SDD Status

这是只读命令。使用当前宿主已安装的 `spec-driven-development` skill；若无法按名称加载，先定位配套的 `SKILL.md`。

读取 `specs/roadmap.md`、已有 feature 规格和 Git 状态，然后判断：

1. 没有完整顶层规格：下一步是 `init`。
2. 没有当前 feature 规格：下一步是 `next`。
3. 有三份 feature 规格但尚未实现：下一步是 `implement`。
4. 已实现但没有验证报告：下一步是在干净上下文执行 `verify`。
5. 已验证但 roadmap 未完成：下一步是 `finish`。
6. 已收尾或出现新全局变化：考虑 `replan`，否则继续 `next`。

只输出当前 phase/feature、已有与缺失产物、阻塞项和唯一的下一步阶段。不要修改文件。
