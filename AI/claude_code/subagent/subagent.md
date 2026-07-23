# Claude Code - Subagents

[Back](../index.md)

- [Claude Code - Subagents](#claude-code---subagents)
  - [Subagents](#subagents)
    - [Built-in subagents](#built-in-subagents)
    - [Custom](#custom)
  - [Agent Markdown](#agent-markdown)

---

## Subagents

- `subagents`
  - specialized, **isolated AI worker instances** spawned by the main chat session to handle specific, focused tasks.
  - main agent can hand off tasks to subagents, which then do the work and return only the final results.

- Benefts:
  - **Context Isolation**:
    - `Subagents` have their own `context windows`.
    - keeps main conversation clean and ensures the AI doesn't get confused by "noise" (like long file contents or tool results) from side tasks.
  - **Parallel Execution**:
    - can run multiple `subagents` **at the same time** to speed up tasks like repo exploration or testing.
  - **Cost Savings**:
    - can assign cheaper, faster models (like Claude Haiku) to simple subagent tasks, saving the expensive models for complex reasoning.
  - **Scoped Permissions**:
    - can restrict a subagent's **tool access**
    - e.g., giving a research agent only "Read-only" and "Grep" access so it can never accidentally modify your files.

---

### Built-in subagents

- three main default subagents that are invoked automatically:
  - `Explore`
    - fast, read-only code search,
  - `Plan`
    - reconnaissance before acting,
  - `General-purpose`
    - complex reasoning and code editing.

### Custom

- create your own agents
  - e.g., "Code Reviewer" or "Test Runner"

- Command
  - `/agents` command
  - by writing Markdown/YAML files in
    - `.claude/agents/`: project level
    - `~/.claude/agents/`: user level

---

## Agent Markdown

| Key         | Required | Accepted Values                                             | Description                                                               |
| ----------- | -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- |
| name        | Yes      | Alphanumeric and hyphens only. The unique ID of your agent. | It must match your filename exactly.                                      |
| description | Yes      | Text string (under 200 words)                               | The routing trigger. Describe the precise tasks this agent handles.       |
| tools       | No       | Read, Write, Grep, Glob, Bash                               | A comma-separated list limiting what this subagent is allowed to execute. |
| model       | No       | sonnet \| haikuThe                                          | brain power. Defaults to sonnet if omitted. Use haiku for lower latency.  |

---

- sample

```md
---
name: agent-kebab-case-name
description: A clear explanation of what this agent does. Claude uses this text to decide exactly when to hand off tasks to this subagent.
tools: Read, Write, Grep, Glob, Bash
model: sonnet
---

# Optional Section Header

This is the system prompt. Insert your primary instructions, constraints, and operational guidelines for the agent here.

## Rules and Behavior

- Bullet point 1
- Bullet point 2
```

---
