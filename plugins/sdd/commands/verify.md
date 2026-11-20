---
description: Run an independent validation report without changing implementation code.
argument-hint: "[feature directory]"
---

# Verify the Current Feature

用户指定或补充的信息：$ARGUMENTS

使用当前宿主已安装的 `spec-driven-development` skill。若无法按名称加载，先定位配套的 `SKILL.md`。

你是独立验证者，不参与实现，不修代码。如果当前会话刚刚实现或修改了这个 feature，停止并要求用户在干净会话重新执行验证。

1. 根据输入、当前分支或最新 feature 定位验证对象；有歧义时先询问。
2. 逐条执行 `validation.md` 的自动化检查、场景验证、文本检查和存量项目回归。
3. 每项标记「通过 / 失败 / 跳过」，跳过项说明原因。
4. 失败项写明期望、实际结果、复现步骤和证据。

只输出验证报告和阻塞项，由用户决定改代码、改规格或接受风险。
