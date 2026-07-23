# Claude Code - Plan Mode

[Back](../index.md)

- [Claude Code - Plan Mode](#claude-code---plan-mode)
  - [GitHub Workflow](#github-workflow)

---

## GitHub Workflow

- `Plan Mode`
  - a safety and brainstorming state where the AI can read, search, and analyze your codebase
  - designed to separate "thinking and designing" from "writing code".
    - restricted **from making any changes** to your files.

- features
  - **True Read-Only Constraint**:
    - Claude **cannot edit** files, write new ones, or run destructive bash commands.
    - It literally lacks the ability to make changes.
  - **Research and Scoping**:
    - Claude explores your files, reasons through the task, and asks clarifying questions to clear up any ambiguities.
  - **The Deliverable**:
    - It **generates a structured implementation plan** (often saved in a plan.md file) detailing what files it needs to touch and the exact steps it will take.
  - **Approval Gate**:
    - Nothing happens until you review the plan, edit or approve it, and explicitly switch Claude out of Plan Mode.

- Commnad:
  - Toggle:
    - Press `Shift` + `Tab` twice to enter Plan Mode
    - and press it again to exit.
  - Command: Type `/plan` during an active Claude Code session.
  - Workflow:
    - Power users typically start in Plan Mode to scope out complex multi-file changes or refactors, refine the plan, and then switch to Auto-Accept Mode for execution.
