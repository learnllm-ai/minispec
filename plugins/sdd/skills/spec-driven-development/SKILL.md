---
name: spec-driven-development
description: Guide software work through project and feature specifications, implementation, independent validation, closeout, and replanning. Use for adopting SDD in a new or existing project or running a delivery phase from specs; not for isolated edits that need no lasting project specification.
---

# Spec-Driven Development

使用 SDD 把项目目标转成小而独立、可验证、可合并的阶段。规格不是开工前的装饰：它们是被确认的意图，也是实现和验收的共同依据。

## 工作阶段

识别用户当前要推进的工作阶段：

- `init`：建立或重建项目级规格。
- `status`：只读检查当前进度并推荐下一步。
- `next`：把一个 roadmap phase 转成 feature 规格。
- `implement`：按已确认规格实现。
- `verify`：独立执行验收并报告。
- `finish`：更新 roadmap 和 changelog，完成当前 phase。
- `replan`：根据新决策更新项目级规格。

阶段名称不依赖某个工具的斜杠命令语法。各阶段的适用条件、可选输入和示例见 [references/stages.md](references/stages.md)。每次只推进用户指定的阶段，不自动跳过确认或进入下一阶段。

## 先判断入口

开始前先读现有规格和项目结构，不要只凭用户的一句话猜下一步：

- 没有 `specs/mission.md`，且没有现存业务代码：按新项目处理。
- 有现存代码、提交历史或运行中的产品，但没有顶层规格：按存量项目引入处理。
- 已有 `specs/mission.md`、`specs/tech-stack.md`、`specs/roadmap.md`：从 roadmap 的下一个未完成 phase 继续。

仓库或用户材料已经给出清楚事实时直接继续；只有缺失信息会改变范围、关键决策或验收标准时才提问。

## 按任务读取资料

- 新项目初始化、存量项目反向建立规格，或重构顶层规格：读 [references/project-setup.md](references/project-setup.md)。
- 为 roadmap 中的一个 phase 写规格、实现、验证、收尾，或继续下一轮：读 [references/feature-loop.md](references/feature-loop.md)。
- 即将创建或修改 `mission.md`、`tech-stack.md`、`roadmap.md`、`requirements.md`、`plan.md`、`validation.md`：同时读 [references/artifacts.md](references/artifacts.md)。
- 用户指定 `init`、`status`、`next`、`implement`、`verify`、`finish` 或 `replan`，或询问各阶段的输入：读 [references/stages.md](references/stages.md)。

## 必须守住的门槛

1. **先证据、后规格。** 存量项目先读 README、依赖、配置、目录、Git 历史和现有测试。代码事实与推断分开，不能把猜测写成现状。
2. **写规格前先确认。** 在创建顶层规格或 feature 规格前，向用户确认会影响结果的「范围、决策、背景」。可以一次问完，也可以分批自然对话，但不能替用户猜商业目标、优先级或不可见约束。
3. **规格阶段不顺手写代码。** 顶层 replanning 更新完受影响规格后应停下；只有范围很小、用户同意且全部 diff 可一次复查时，才考虑同轮修改实现。
4. **一个 phase 一个闭环。** 每轮依次经过 feature 规格、实现、独立验证、用户决策、收尾和必要的 replanning，再进入下一轮。
5. **实现者不自验。** 正式验收由干净上下文中的独立验证者按 `validation.md` 执行并报告；实现者不替验证者勾选结果。用户根据报告决定改代码、改规格或接受风险。
6. **规格与实现同步。** 实现中发现本 feature 的规格缺失或错误时，同步修正该 feature 的三份规格；不要越权修改 roadmap、changelog 等由独立步骤维护的文件。
7. **保持阶段可回滚、可 review。** 不主动扩张到核心重构、数据库迁移、认证改造或跨模块依赖升级。新增依赖、破坏兼容性或推进 roadmap 中未确认的范围前，先取得用户同意。
8. **用用户能验证的语言写作。** 规格写行为、边界、决策和证据，不堆实现口号；删除占位符、调试思路和无法判定真假的完成标准。

完成当前步骤时，明确告诉用户产出了哪些文件、哪些检查已经执行，以及下一步需要用户确认什么。任务只要求起草或审查规格时，不自动进入实现。
