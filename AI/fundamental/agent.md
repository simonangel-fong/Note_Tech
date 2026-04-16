# AI Agent & Agentic AI

[Back](./index.md)

- [AI Agent \& Agentic AI](#ai-agent--agentic-ai)
  - [AI Agent](#ai-agent)
    - [Types of AI Agents](#types-of-ai-agents)
  - [Agentic AI](#agentic-ai)
    - [How Agentic AI Works](#how-agentic-ai-works)
  - [AI Agent vs Agentic AI](#ai-agent-vs-agentic-ai)

## AI Agent

- `AI agent`
  - an autonomous **software program** that uses artificial intelligence(`Large Language Models (LLMs)`) to **achieve specific goals** by **reasoning**, **planning**, and **using external tools**.

- **Key Characteristics**
  - Goal-driven
  - Can use tools (APIs, databases, CLI)
  - Semi-autonomous
  - Often powered by LLM + tools + memory

---

### Types of AI Agents

- **Reactive Agent**
  - No memory
  - Rule-based

- **Tool-Using Agent**
  - Calls APIs/tools
  - Most common today

- **Planning Agent**
  - Breaks tasks into steps
  - Uses reasoning

- **Multi-Agent System**
  - Multiple agents collaborate
  - Each has a role

---

## Agentic AI

- `Agentic AI`
  - the **autonomous systems** that act as agents to achieve specific **goals** with **limited human supervision**, moving beyond passive, reactive AI to **proactive**, goal-driven action.
  - These systems leverage Large Language Models (LLMs) to **reason**, **plan**, **take independent actions**, and adapt to new situations to complete complex, multi-step tasks rather than just generating content.

- **Agentic AI** is a paradigm where AI systems:
  - **Plan** tasks autonomously
  - Make **decisions**
  - **Execute** multi-step workflows
  - **Iterate until** goal is achieved

- **Core Capabilities**
  - Task decomposition
  - Decision-making
  - Tool usage
  - Memory/context retention
  - Self-correction

---

### How Agentic AI Works

1. **Goal**
   - e.g., "Fix CI/CD failure"

2. **Perception**
   - Read logs, configs, metrics

3. **Planning**
   - Break into steps

4. **Action**
   - Call tools (API, CLI, DB)

5. **Reflection**
   - Evaluate result

6. **Repeat**
   - Until goal achieved

---

## AI Agent vs Agentic AI

- **AI Agent = one worker**
- **Agentic AI = system of workers**

| Aspect       | AI Agent                 | Agentic AI                |
| ------------ | ------------------------ | ------------------------- |
| Scope        | Single task              | Multi-step system         |
| Complexity   | Low–Medium               | High                      |
| Behavior     | Reactive + some planning | Autonomous planning       |
| Architecture | Single component         | Multi-agent orchestration |
| Example      | Log analyzer             | Full CI/CD assistant      |

---
