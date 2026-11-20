# MiniSpec

MiniSpec 是一套以 `SKILL.md` 为核心的 Specification-Driven Development（SDD）工作流，基于 [SDD Starter](https://github.com/learnllm-ai/SDD_Starter) 整理。

它解决的是同一个问题：先确认目标，再写规格；按小阶段实现；由独立验证者验收；最后收尾并重新规划。核心 skill 不依赖 Codex、Claude Code、GitHub Copilot 或某个 IDE。斜杠命令是各平台的外置适配层。

## 支持范围

| 使用环境 | 斜杠语法 | 安装方式 |
| --- | --- | --- |
| Codex CLI | `/sdd:*` | Codex 插件 marketplace |
| Codex VS Code 集成 | `/sdd:*` | 与 Codex CLI 共用用户级插件 |
| Claude Code CLI | `/sdd-*` | 用户级或项目级 Agent Skills |
| Claude Code VS Code 扩展 | `/sdd-*` | 与 Claude Code CLI 共用本地配置 |
| GitHub Copilot CLI | `/sdd-*` | 用户级或项目级 Agent Skills |
| GitHub Copilot in VS Code | `/sdd-*` | 与 Copilot CLI 共用 Agent Skills |
| 其他 agent / IDE | `/sdd-*` 或自然语言 | 通用 `SKILL.md` 安装 |

包名是 MiniSpec，但由于命令已经稳定使用 `sdd` 命名空间，命令仍保留：

```text
Codex:        /sdd:init
其他平台:     /sdd-init
```

## 目录结构

```text
minispec/
├── README.md
├── install.py
├── spec-driven-development/
│   ├── SKILL.md
│   └── references/
├── plugins/
│   └── sdd/
│       ├── .codex-plugin/plugin.json
│       ├── commands/
│       └── skills/
├── .agents/
│   └── plugins/marketplace.json
└── dist/
    ├── spec-driven-development.zip
    ├── claude-code.zip
    └── copilot.zip
```

- `spec-driven-development/` 是唯一的核心 skill。
- `plugins/sdd/` 是 Codex 插件适配器，也是阶段命令的唯一源文件。
- `plugins/sdd/commands/` 同时供 Codex 直接使用和安装器生成 Claude/Copilot/通用命令。
- `.agents/` 是 Codex 本地 marketplace。
- `dist/` 是可直接分发的压缩包。
- `install.py` 负责安装和重新生成适配文件。

## 前置条件

必需：

- Python 3.9 或更高版本。
- 对本目录和对应 agent 配置目录的写权限。

可选：

- Codex CLI。
- Claude Code CLI。
- GitHub Copilot CLI。
- VS Code 及对应的 Codex、Claude Code 或 GitHub Copilot 扩展。
- Git；SDD 工作流会在 Git 仓库中创建 phase 分支并读取提交历史。

以下命令均在 MiniSpec 根目录执行，也就是本 README 所在目录。

## Codex 安装

### 首次安装

```bash
codex plugin marketplace add .
codex plugin add sdd@sdd-starter
```

验证：

```bash
codex plugin list
codex plugin marketplace list
```

`codex plugin list` 中应看到：

```text
sdd@sdd-starter  installed, enabled
```

然后在 Codex 中新建会话，输入 `/`，应看到：

```text
/sdd:init
/sdd:status
/sdd:next
/sdd:implement
/sdd:verify
/sdd:finish
/sdd:replan
```

Codex CLI 和 Codex VS Code 集成使用同一份用户级 Codex 插件配置。重装插件后需要新开会话。

### 从旧目录迁移

如果 marketplace 仍指向迁移前的旧目录，先移除旧配置，再在当前 MiniSpec 根目录重新注册：

```bash
codex plugin remove sdd
codex plugin marketplace remove sdd-starter

codex plugin marketplace add .
codex plugin add sdd@sdd-starter
```

### 更新 Codex 命令

修改核心 skill 后，先同步 Codex 插件中的 skill：

```bash
python3 install.py sync-codex
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" \
  plugins/sdd
```

阶段命令直接编辑 `plugins/sdd/commands/`；安装器会据此生成 Claude、Copilot 和通用命令。

本地插件内容变化后，如 Codex 仍使用缓存版本，更新版本缓存标记并重新安装：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" \
  plugins/sdd

codex plugin add sdd@sdd-starter
```

## Claude Code 安装

Claude Code 的 CLI 和 VS Code 扩展共享本地 `.claude` 配置。

### 用户级安装

适用于本机所有项目：

```bash
python3 install.py install-claude --scope user
```

安装位置：

```text
~/.claude/skills/spec-driven-development/
~/.claude/skills/sdd-init/
~/.claude/skills/sdd-status/
~/.claude/skills/sdd-next/
~/.claude/skills/sdd-implement/
~/.claude/skills/sdd-verify/
~/.claude/skills/sdd-finish/
~/.claude/skills/sdd-replan/
```

### 项目级安装

只让某个项目使用：

```bash
python3 install.py install-claude \
  --scope project \
  --project ../my-project
```

安装位置：

```text
<project>/.claude/skills/
├── spec-driven-development/
└── sdd-*/
    └── SKILL.md
```

### 验证

重新打开 Claude Code CLI 或刷新 VS Code 中的 Claude Code 扩展，然后输入 `/`。应看到：

```text
/sdd-init
/sdd-status
/sdd-next
/sdd-implement
/sdd-verify
/sdd-finish
/sdd-replan
```

如果安装了 Claude Code CLI，可运行：

```bash
claude plugin validate ~/.claude/skills
```

每个 `/sdd-*` 都带有 `user-invocable: true` 和 `disable-model-invocation: true`，会出现在 `/` 菜单中并只能由用户主动调用。

## GitHub Copilot 安装

GitHub Copilot in VS Code 和 GitHub Copilot CLI 使用 Agent Skills。

### 用户级安装

适用于所有工作区：

```bash
python3 install.py install-copilot --scope user
```

安装位置：

```text
~/.copilot/skills/
├── spec-driven-development/
└── sdd-*/
    └── SKILL.md
```

### 项目级安装

```bash
python3 install.py install-copilot \
  --scope project \
  --project ../my-project
```

安装位置：

```text
<project>/.github/skills/
├── spec-driven-development/
└── sdd-*/
    └── SKILL.md
```

### 验证

重新打开 Copilot CLI 会话，或在 VS Code 中新建 Copilot Chat session，然后输入 `/`。应看到：

```text
/sdd-init
/sdd-status
/sdd-next
/sdd-implement
/sdd-verify
/sdd-finish
/sdd-replan
```

MiniSpec 使用 Agent Skills，不使用只在已弃用 Local harness 中运行的 `.github/prompts/*.prompt.md`。

## 通用 Agent Skills 安装

任何能读取 `SKILL.md` 的 agent 都可以使用核心 skill。

### 只安装 skill

```bash
python3 install.py install \
  --dest ../my-project/.agents/skills
```

### 同时安装 Markdown 命令模板

```bash
python3 install.py install \
  --dest ../my-project/.agents/skills \
  --commands-dest ../my-project/.agent-commands
```

安装到通用命令目录后会生成：

```text
commands/sdd-init.md
commands/sdd-status.md
commands/sdd-next.md
commands/sdd-implement.md
commands/sdd-verify.md
commands/sdd-finish.md
commands/sdd-replan.md
```

宿主如果根据文件名生成命令，通常会得到 `/sdd-init` 到 `/sdd-replan`。不同宿主的命名规则可能不同，但不需要修改命令逻辑。

如果工具没有 skill 自动发现机制，可以直接让它读取：

```text
spec-driven-development/SKILL.md
```

或使用自然语言：

```text
使用 spec-driven-development skill 执行 status。
```

## 分发包

### 核心 skill + 通用命令

包含：

```text
spec-driven-development/
commands/
```

这里的 `commands/` 是打包产物，不是仓库中的第二个源目录。

文件：

[spec-driven-development.zip](dist/spec-driven-development.zip)

重新生成：

```bash
python3 install.py package \
  --output dist/spec-driven-development.zip \
  --force
```

### Claude Code

包含 `.claude/skills/` 下的核心 skill 和 7 个 `/sdd-*` stage skills。

文件：

[claude-code.zip](dist/claude-code.zip)

重新生成：

```bash
python3 install.py package-claude \
  --output dist/claude-code.zip \
  --force
```

### GitHub Copilot

包含 `.github/skills/` 下的核心 skill 和 7 个 `/sdd-*` stage skills。

文件：

[copilot.zip](dist/copilot.zip)

重新生成：

```bash
python3 install.py package-copilot \
  --output dist/copilot.zip \
  --force
```

## 日常使用

七个阶段：

| 阶段 | 用途 | 参数 |
| --- | --- | --- |
| `init` | 建立或重建项目级规格 | 可选：项目简介、目标用户、技术或交付约束 |
| `status` | 只读查看当前阶段并推荐下一步 | 无 |
| `next` | 生成下一个 feature 的三份规格 | 可选：phase、功能目标、范围或验收约束 |
| `implement` | 按 plan 实现并做实现者自检 | 可选：feature 目录、范围限制 |
| `verify` | 独立执行验收，只报告、不修代码 | 可选：feature 目录 |
| `finish` | 更新 roadmap 和 changelog | 可选：feature 目录、交付说明 |
| `replan` | 更新项目级规格 | 可选：新决策或重排目标 |

### 典型流程

```text
/sdd:init
/sdd:next
/sdd:implement
```

实现完成后，在干净会话中验证：

```text
/sdd:verify
```

用户复查验证报告并决定是否接受残余风险，然后回到实现会话：

```text
/sdd:finish
```

Claude Code 和 GitHub Copilot 使用 `/sdd-init` 等命令，流程完全相同。

### 新项目

```text
/sdd:init 做一个本地 Markdown 笔记 CLI，使用 TypeScript，只支持 macOS
```

此后 MiniSpec 会创建：

```text
specs/mission.md
specs/tech-stack.md
specs/roadmap.md
```

确认顶层规格后再执行：

```text
/sdd:next Phase 1
```

### 存量项目

```text
/sdd:init 这是存量项目，先按现有代码反向生成规格，不修改业务代码
```

`init` 会先只读探索仓库，对无法从代码确认的商业目标、优先级和边界请求用户确认。

### 指定 phase 或 feature

```text
/sdd:next Phase 2
/sdd:next 增加 Markdown 导出，只做 CLI，不改编辑器
/sdd:next 登录失败提示要区分密码错误和账号锁定
```

### 实现指定 feature

```text
/sdd:implement specs/2026-11-20-markdown-export
/sdd:implement specs/2026-11-20-markdown-export 只完成 Group 1 和 Group 2
```

范围约束只能缩小或澄清已确认规格，不能扩大 feature。

### 独立验证

推荐新开一个干净 session：

```text
/sdd:verify specs/2026-11-20-markdown-export
```

验证者逐项标记：

```text
通过 / 失败 / 跳过（说明原因）
```

失败项必须包含期望、实际、复现步骤和证据。

### 收尾

```text
/sdd:finish specs/2026-11-20-markdown-export
```

MiniSpec 会更新 `CHANGELOG.md` 和 `specs/roadmap.md`。提交、合并和删除分支前仍会请求确认。

### Replanning

```text
/sdd:replan 新增 Windows 支持，把兼容性工作放到 Phase 3 之前
/sdd:replan 不接入云数据库，全部本地优先
```

Replanning 只更新顶层规格，不顺手修改实现代码。

## 产物

项目级：

```text
specs/
├── mission.md
├── tech-stack.md
└── roadmap.md
```

每个 phase：

```text
specs/YYYY-MM-DD-feature-name/
├── requirements.md
├── plan.md
└── validation.md
```

收尾时可能产生或更新：

```text
CHANGELOG.md
```

核心约束：

1. 规格写清楚范围、范围外、行为、决策、背景和未决问题。
2. `plan.md` 按实现顺序拆成可 review 的 task group，并至少包含测试。
3. `validation.md` 写成另一人可执行的验收清单。
4. 实现者在正式验证前停止。
5. 验证者不修代码。
6. 用户根据报告决定改代码、改规格或接受风险。
7. 实现中发现 feature 规格有偏差时，同步更新三份 feature 规格。
8. 全局变化先 replanning，再开启新的 feature。

## 安全检查

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  spec-driven-development

python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" \
  plugins/sdd

unzip -t dist/spec-driven-development.zip
unzip -t dist/claude-code.zip
unzip -t dist/copilot.zip
```

测试通用安装：

```bash
python3 install.py install \
  --dest .tmp-test/skills \
  --commands-dest .tmp-test/commands \
  --force
```

测试 Claude 项目安装：

```bash
python3 install.py install-claude \
  --scope project \
  --project ../minispec-claude-test \
  --force
```

测试 Copilot 项目安装：

```bash
python3 install.py install-copilot \
  --scope project \
  --project ../minispec-copilot-test \
  --force
```

## 常见问题

### 输入 `/` 看不到命令

1. 确认安装了对应平台。
2. 确认命令位于本文档列出的目录。
3. 确认重新打开了 CLI session 或 VS Code chat session。
4. Codex 用户运行 `codex plugin list`，确认 `sdd@sdd-starter` 是 `installed, enabled`。
5. Claude/Copilot 用户确认 `spec-driven-development` 和 `sdd-*` skill 都存在。

### Claude 和 Copilot 的命令为什么不是 `/sdd:*`

Codex 插件用命名空间 `/sdd:command`；Claude Code 和 Copilot 的 Agent Skills 使用目录或 frontmatter 名称，通常为 `/sdd-command`。

### 为什么没有生成 `.github/prompts`

VS Code 官方将 prompt files 限定在已弃用的 Local harness。MiniSpec 使用可用于 Copilot CLI 和 VS Code Copilot 的 Agent Skills。

### 已有同名 skill

安装器默认拒绝覆盖。确认可以替换后添加：

```bash
--force
```

### VS Code 集成终端

VS Code 集成终端只是运行对应 CLI：

- 在终端运行 `codex`，使用 `/sdd:*`。
- 在终端运行 `claude`，使用 `/sdd-*`。
- 在终端运行 Copilot CLI，使用 `/sdd-*`。

它们分别继承 Codex、Claude Code、Copilot 的用户级配置。

## 卸载

只删除 MiniSpec 自己安装的目录，不要删除整个 agent 配置目录。

Codex：

```bash
codex plugin remove sdd
codex plugin marketplace remove sdd-starter
```

Claude Code 用户级：

```bash
rm -rf ~/.claude/skills/spec-driven-development
rm -rf ~/.claude/skills/sdd-init
rm -rf ~/.claude/skills/sdd-status
rm -rf ~/.claude/skills/sdd-next
rm -rf ~/.claude/skills/sdd-implement
rm -rf ~/.claude/skills/sdd-verify
rm -rf ~/.claude/skills/sdd-finish
rm -rf ~/.claude/skills/sdd-replan
```

Copilot 用户级：

```bash
rm -rf ~/.copilot/skills/spec-driven-development
rm -rf ~/.copilot/skills/sdd-init
rm -rf ~/.copilot/skills/sdd-status
rm -rf ~/.copilot/skills/sdd-next
rm -rf ~/.copilot/skills/sdd-implement
rm -rf ~/.copilot/skills/sdd-verify
rm -rf ~/.copilot/skills/sdd-finish
rm -rf ~/.copilot/skills/sdd-replan
```

项目级安装只需要删除项目内的 `.claude/skills/sdd-*`、`.claude/skills/spec-driven-development`、`.github/skills/sdd-*` 和项目内的 `spec-driven-development`。确认路径后再删除。

## 官方格式参考

Claude Code：

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Platforms and integrations](https://code.claude.com/docs/en/platforms)

GitHub Copilot 与 VS Code：

- [Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Prompt files in VS Code](https://code.visualstudio.com/docs/copilot/customization/prompt-files)

Codex 插件目录、marketplace 和命令文件由本仓库的插件校验器与当前 Codex CLI 实际安装流程验证。
