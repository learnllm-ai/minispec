---
description: Establish SDD top-level specs for a new or existing project.
argument-hint: "[project brief or additional constraints]"
---

# Initialize SDD

用户提供的项目补充信息：$ARGUMENTS

使用当前宿主已安装的 `spec-driven-development` skill。若宿主不能按名称加载 skill，先定位配套的 `SKILL.md`；不要凭记忆重写流程。读取 skill 的 `references/project-setup.md` 和 `references/artifacts.md`。

1. 检查当前目录和 Git 状态，判断新项目、存量项目还是已有 `specs/` 的项目。
2. 新项目读取 `prd.md`、现有文档和用户参数；缺少关键输入时，只询问「范围、关键决策、背景」。
3. 存量项目先只读探索 README、依赖、配置、入口、目录、测试、Git 历史和现有 issue/TODO，再给出发现摘要。`[推断]` 需要用户确认。
4. 创建或补齐 `specs/mission.md`、`specs/tech-stack.md`、`specs/roadmap.md`。
5. roadmap 写成高层、独立可交付的 phase。

本命令只建立项目级规格。完成后停在规格 review，不开始 feature 实现。
