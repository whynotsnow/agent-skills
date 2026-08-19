---
name: agent-workspace
description: 维护 Agent Workspace Spec 项目，包括检查、初始化、验证、迁移或解释 .agent-workspace/manifest.json、.agent-workspace/tools/、public agent memory、disclosure boundaries、runtime profiles、team-local identity profiles，以及 reusable Codex Skill 与 project-local Agent Workspace tooling 的边界。
---

# Agent Workspace

使用这个 skill 作为 Agent Workspace Spec workspace 的 operator。不要把 skill 当作 workspace implementation。只要 `.agent-workspace/manifest.json` 声明了本地实现，就优先使用该 local implementation。

## 核心边界

- Skill：发现 workspace、读取 manifest、选择 workflow，并维护 disclosure rules。
- Manifest：声明 spec version、conformance levels、public knowledge、local state 和 local tooling。
- `.agent-workspace/tools/`：project-local implementation，可以是 Node、Python、Bash、Make、package-manager wrappers、CI commands 或其他声明的 runtime。
- Public knowledge：tracked instructions、sanitized memory、runtime requirements、specs、schemas 和 examples。
- Local state：ignored developer、machine、session、raw 和 quarantine data。

当 developer、machine、session 或 diagnostic context 与当前任务相关时，可以读取和分析 local state。Privacy 是输出和持久化边界，不是访问禁令。不要无任务理由地检查 local state。

不要把 `.agent-workspace/local/`、`.agent-workspace/raw/` 或 `.agent-workspace/quarantine/` 中的 private local values 复述、枚举、引用或复制到 tracked files 或 handoffs。handoff 只能报告最小的、与任务相关的 sanitized conclusion，例如某个 required capability 是否可用，并且不能暴露 identity、path、hostname、opaque profile ID、private URL、credential 或 raw observation。

## 工作流

1. 在仓库或子目录中运行 `scripts/agent_workspace.py status`。
2. 如果存在 manifest，读取它并优先使用其中的 `tooling.entry`。
3. 使用 `scripts/agent_workspace.py run -- <args>` 调用 local tooling，避免硬编码项目内命令路径。
4. 如果 local tooling 缺失或不完整，报告 workspace capability gap。不要静默用 bundled validation 替代项目自己的验证。
5. 如果用户要求在新仓库采用 Agent Workspace Spec，先阅读 `references/adoption.md`，检查已有项目文件后再从 `assets/reference-workspace/` 复制模板。
6. 如果用户询问 disclosure、open-source readiness、runtime memory 或 team identity，编辑前阅读对应 reference。

## 常用命令

```bash
python3 /path/to/skill/scripts/agent_workspace.py status
python3 /path/to/skill/scripts/agent_workspace.py run -- validate
python3 /path/to/skill/scripts/agent_workspace.py run -- public-check --staged
python3 /path/to/skill/scripts/agent_workspace.py run -- profile status
```

这些命令会从当前目录向上查找 `.agent-workspace/manifest.json`。

## Reference Routing

- 需要 normative workspace structure 和 conformance levels 时，阅读 `references/spec.md`。
- 修改 `.agent-workspace/tools/` 或判断 skill script 是否可替代 local tools 前，阅读 `references/tooling.md`。
- 提升 runtime observations 或准备 open source 前，阅读 `references/disclosure.md`。
- 处理 browser automation、sandbox failures 或 local capability profiles 前，阅读 `references/runtime.md`。
- 修改 developer、machine、session 或 Git identity mapping 前，阅读 `references/team.md`。
- 初始化或迁移仓库前，阅读 `references/adoption.md`。

保持 `SKILL.md` 精简。只有当前任务需要时才加载 references。
