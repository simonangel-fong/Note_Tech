# Claude Code - Skill

[Back](../index.md)

- [Claude Code - Skill](#claude-code---skill)
  - [Skill](#skill)
  - [Install](#install)

---

## Skill

- `Skills`
  - **reusable packages of instructions, scripts, and context** that teach Claude how to execute specific, repeatable tasks.
  - package these workflows into files, allowing Claude to dynamically load them whenever your prompt matches the skill.

- **How they work**:
  - Skills are stored as `SKILL.md` files in your `.claude/skills/` directory (either project-specific or globally).

- **Progressive Disclosure**:
  - Claude **scans only the name and description** of available skills on startup, keeping your context window clear.
  - When it identifies a match for your task, it loads the complete instructions and helper scripts.
- **Types of Skills**:
  - You can write your own custom skills, use bundled default skills (like /debug, /code-review, or /doctor), or download open-source skills created by the developer community.

---

## Install

```sh
# install anthropics/skills
/plugin marketplace add anthropics/skills

/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```
