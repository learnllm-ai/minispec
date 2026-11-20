---
description: Turn the next roadmap phase into one complete feature specification.
argument-hint: "[phase name, feature idea, or constraints]"
---

# Define the Next Feature

用户指定的 phase 或补充要求：$ARGUMENTS

使用当前宿主已安装的 `spec-driven-development` skill。若无法按名称加载，先定位配套的 `SKILL.md`。重点读取 `references/feature-loop.md` 和 `references/artifacts.md`。

1. 缺少顶层规格时停止，并提示先执行 `init`。
2. 读取 `specs/roadmap.md`，选择下一个未完成且前置条件满足的 phase。用户输入要求其他 phase 时，先确认它与 roadmap 的关系。
3. 读取相关代码、文档和测试；存量项目必须确认兼容性约束。
4. 只询问会影响本 feature 的「范围、关键决策、背景」。
5. 项目在 Git 仓库中时，创建 `phase-N-<kebab-name>` feature 分支。
6. 创建 `specs/YYYY-MM-DD-feature-name/` 下的 `requirements.md`、`plan.md`、`validation.md`。

本命令不写实现。完成后停在 feature 规格 review。
