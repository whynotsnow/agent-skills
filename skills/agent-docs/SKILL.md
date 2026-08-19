---
name: agent-docs
description: 标准化、初始化、审计、迁移和维护真实开发项目的 Agent Docs 文档规范，包括根 README.md、AGENTS.md、固定 docs/agents 知识结构和可扩展 docs/developers 区域。Use when Codex needs to create or repair project documentation, decide document ownership, review documentation drift, validate the Agent Docs contract, or migrate a source repository to the standard layout.
---

# Agent Docs

使用这个 skill 维护真实开发项目的稳定文档契约，避免每次代码变更都演变成无边界的文档 churn。

## 文档契约

真实开发项目需要这些入口：

```text
README.md
AGENTS.md
docs/README.md
docs/agents/
docs/developers/README.md
```

`docs/agents/` 下的固定文件由 `references/document-contract.md` 定义。项目可以在 `docs/` 下增加其他文件或目录，但新增文档必须有明确读者和所有权，不能复制已有文档的职责。

Agent Docs 适用于 source repositories、真实开发项目和完整 project-knowledge repositories。它不定义 adjacent planning sidecars、process repositories 或其他 non-source workflow repositories 的文档契约。如果仓库声明了 `plan.config.json` 且 `sidecarKind: agent-project-sidecar`，将其视为完整 Agent Docs contract 的 out of scope 对象，并使用 Agent Project Sidecar skill 处理该仓库。

## 工作流

1. 在项目中运行 `python3 <skill>/scripts/agent_docs.py status`，或用 `--root <path>` 指定项目根目录。
2. 创建、移动、重命名或大幅重写文档前，阅读 `references/document-contract.md`。
3. 判断代码变更是否需要同步文档前，阅读 `references/maintenance-matrix.md`。
4. 持久化 runtime observations、identities、paths、logs、credentials 或 environment details 前，阅读 `references/disclosure-rules.md`。
5. 仅在用户要求初始化或修复结构时使用 `init`。它只创建缺失文件，不覆盖已有文件。
6. 更新拥有该行为的最小文档。能链接到其他 owner 时，不复制内容。
7. 结构或文档变更后运行 `validate`。如果项目本身有 Agent Workspace、文档检查或 pre-commit 检查，也应继续运行项目自己的验证。

当真实开发项目使用 adjacent sidecar 时，Agent Docs 仍只关注 durable project knowledge。Plan-bound execution records 属于 sidecar。只有产生 reusable project learning、recurring failure patterns 或 lasting maintenance rules 时，才更新 `docs/agents/execution-log.md`。

## Commands

```bash
python3 <skill>/scripts/agent_docs.py status
python3 <skill>/scripts/agent_docs.py init
python3 <skill>/scripts/agent_docs.py validate
python3 <skill>/scripts/agent_docs.py audit
python3 <skill>/scripts/agent_docs.py audit --staged
```

使用 `init --dry-run` 预览会创建的缺失模板。所有命令都可以在子命令前传入 `--root <path>`。

## Agent Workspace 兼容

将 Agent Docs 视为 documentation profile，而不是 Agent Workspace implementation。如果存在 `.agent-workspace/manifest.json`：

- 遵守它声明的 public、local 和 tooling 边界；
- 项目 conformance 优先使用 manifest-declared project-local tooling，而不是全局 skill scripts；
- Agent Docs validation 后继续运行 project-local validator；
- 永远不要把 `.agent-workspace/local/`、`.agent-workspace/raw/` 或 `.agent-workspace/quarantine/` 复制进 public documents。

不要静默安装 project-local validator 或 Git hook。只有用户要求时，才增加 enforcement integration。

## 维护规则

- 保持 `AGENTS.md` 简洁且规范化。
- 根 `README.md` 聚焦项目身份、setup 和主要使用方式。
- `docs/README.md` 作为唯一 documentation router。
- `docs/agents/` 保存 sanitized、reusable agent knowledge，不作为 transcript store。
- `docs/developers/` 保存 human-facing development 和 operations guidance。
- 没有 reusable learning 的 routine task 不更新 `execution-log.md`。
- 当项目 sidecar 提供 `runs/` 时，不要把 `execution-log.md` 当作 plan/RM execution log。
- 除非用户明确把 `agent-project-sidecar` 仓库转换成真实开发项目，否则不要在其中初始化完整 Agent Docs 结构。
- 不要因为某个 observation 出现一次就提升到 `memory.json`。
- 对不确定的 semantic drift 给出 review recommendation，不要编造文档变更。

## Reference Routing

- 需要 required files 和 exclusive ownership 时，阅读 `references/document-contract.md`。
- 需要 change-to-document routing 时，阅读 `references/maintenance-matrix.md`。
- 需要 public/private boundaries 时，阅读 `references/disclosure-rules.md`。
- 重组已有 documentation tree 前，阅读 `references/migration.md`。

只通过 initializer 使用 `assets/project-template/`，或在检查已有项目文件后再使用这些模板。
