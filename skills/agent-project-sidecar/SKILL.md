---
name: agent-project-sidecar
description: Create, connect, inspect, operate, migrate, or validate an adjacent project sidecar repository for AI-agent planning, decisions, task state, execution records, validation notes, and handoffs. Use when a user asks to add sidecar planning to a project, initialize a sibling project.plan workspace, use an existing sidecar board, enforce main-repo/sidecar boundaries, or explain sidecar project workflow.
---

# Agent Project Sidecar

使用这个 skill 为真实开发项目创建或维护相邻的 planning sidecar 仓库。Sidecar 将计划、决策、执行追溯和 handoff 从产品源码中分离出来，同时保持 agent 工作可审计、可恢复。

## 核心规则

- 产品源码、运行配置、密钥、生成产物、部署文件和正式产品文档留在主仓库。
- planning items、decisions、executable plans、sanitized runs、validation notes 和 handoffs 留在 sidecar。
- 默认 sidecar 路径是 `../<main-repo-name>.plan`，除非项目说明或 `plan.config.json` 声明了其他路径。
- 发现可执行工作时，优先使用主仓库声明的状态命令，例如 `pnpm --silent plan:status --json`。
- 默认只执行 `status: ready` 或 `status: running` 的 sidecar item。
- `discussing`、`needs-decision`、`decided` 和 `blocked` 默认不可直接实现，除非维护者显式覆盖流程。
- 不要把 credentials、cookies、tokens、private keys、Access JWTs、raw logs、personal identities、absolute user-home paths、private URLs、hostnames、local profile IDs 或未经审查的 runtime observations 写入 tracked sidecar 文件。
- 直接执行 sidecar item 的主仓库 commit 使用 `Plan-Item: <id>`。仅相关但不执行该 item 时才使用 `Related-Plan: <id>`。
- 日常 sidecar 变更应和对应主仓库变更一起提交，除非维护者明确要求单独 checkpoint。
- Sidecar 不默认接入 Agent Workspace，也不默认采用完整 Agent Docs contract。它拥有自己的轻量文档规范。

## 工作流

1. 先检查主仓库说明：`AGENTS.md`、文档路由、package scripts 和已有 sidecar 引用。
2. 创建 sidecar 前，阅读 `references/migration-guide.md`，然后运行 `scripts/init_sidecar.py`。
3. 操作已有 sidecar 前，阅读 `references/planning-workflow.md`，再检查 `plan.config.json`、`index.json`、目标 item 和 linked plan。
4. 处理与主仓库 Agent Docs、`execution-log.md`、`memory.json` 或 developer docs 的边界时，阅读 `references/agent-docs-coordination.md`。
5. 持久化 runtime observations 或 private operational details 前，阅读 `references/disclosure-boundaries.md`。
6. 检查边界或结构时，运行 `scripts/validate_sidecar.py <sidecar-path>`。
7. 按需更新主仓库说明，至少包含 sidecar path、status command、execution gate 和 commit-trailer rules。

## 单独运行场景

- 在主仓库中单独运行时：创建或连接相邻 sidecar，并只维护主仓库中必要的 sidecar discovery 和 execution gate。不要自动初始化完整 Agent Docs。
- 在 sidecar 仓库中单独运行时：读取 `plan.config.json`，校验 sidecar 结构、模板、状态、run/plan/item 关系和 disclosure 边界。不要接入 Agent Workspace。
- 与 `agent-docs` 同时使用时：本 skill 管 sidecar contract、模板、状态和 plan-bound traceability；`agent-docs` 只管主仓库长期项目知识和完整 Agent Docs contract。

## Bundled Resources

- `scripts/init_sidecar.py`: 创建标准相邻 sidecar 骨架，支持 `--language zh|en`，生成 config、board index、目录、模板和可选 Git 初始化。
- `scripts/validate_sidecar.py`: 校验 sidecar 结构、模板、状态、基础 item/run 字段和常见 disclosure 边界问题。
- `references/sidecar-contract.md`: Repository boundary、file ownership、commit linkage 和 customization rules。
- `references/planning-workflow.md`: Item statuses、item/plan/run lifecycle 和 operating procedure。
- `references/agent-docs-coordination.md`: Sidecar 与主仓库 Agent Docs、Agent Workspace、execution-log、memory、developer docs 的协作边界。
- `references/disclosure-boundaries.md`: Public/private data classes 和 sanitization rules。
- `references/migration-guide.md`: 将已有项目接入 sidecar planning 的流程。
