# Claude Code - Memory

[Back](../index.md)

- [Claude Code - Memory](#claude-code---memory)
  - [Memory](#memory)
  - [CLAUDE.md files](#claudemd-files)
  - [Memory Hierarchy](#memory-hierarchy)
  - [Common Commands](#common-commands)
  - [Best Practices](#best-practices)

---

## Memory

- Each `Claude Code` **session** begins with a **fresh context window**.
- Two mechanisms carry knowledge **across sessions**:
  - `CLAUDE.md` files: instructions you write to give Claude persistent context
  - **Auto memory**: notes Claude writes itself based on your corrections and preferences

---

## CLAUDE.md files

- `CLAUDE.md` files
  - markdown files that give `Claude` **persistent instructions** for a project, your personal workflow, or your entire organization.
    - You write these files in plain text;
    - Claude reads them at the start of every session.

Add to it when:
Claude makes the same mistake a second time
A code review catches something Claude should have known about this codebase
You type the same correction or clarification into chat that you typed last session
A new teammate would need the same context to be productive

---

## Memory Hierarchy

| Scope                | Location                     | Purpose                                                    | Use case examples                                                    | Shared with                     |
| -------------------- | ---------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------- |
| Managed policy       | `/etc/claude-code/CLAUDE.md` | Organization-wide instructions managed by IT/DevOps        | Company coding standards, security policies, compliance requirements | All users in organization       |
| User instructions    | `~/.claude/CLAUDE.md`        | Personal preferences for all projects                      | Code styling preferences, personal tooling shortcuts                 | Just you (all projects)         |
| Project instructions | `./CLAUDE.md`                | Team-shared instructions for the project                   | Project architecture, coding standards, common workflows             | Team members via source control |
| Local instructions   | `./CLAUDE.local.md`          | Personal project-specific preferences; add to `.gitignore` | Your sandbox URLs, preferred test data                               | Just you (current project)      |

---

## Common Commands

| Command    | Description                                  |
| ---------- | -------------------------------------------- |
| `/init`    | generate a starting CLAUDE.md automatically. |
| `/memory`  | pens your memory files                       |
| `/clear`   | Clears out heavy, accumulated context        |
| `# input`  | Add a memory                                 |
| `/compact` | compact memory                               |

---

## Best Practices

- Keep files **lean**:
  - Avoid exceeding ~**150 to 200 lines** in your `CLAUDE.md` files, otherwise Claude may silently ignore portions of them.
- Use **conversational updates**:
  - Instead of **manually writing** everything, you can simply ask Claude to remember rules during conversation
  - e.g., "Remember that we prefer async/await over promises", and it will automatically update its auto-memory.
- **Maintain documentation**:
  - Store large, static project documentation in a `docs/` folder instead of memory, and reference it when needed.
