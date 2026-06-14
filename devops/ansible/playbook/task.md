# Ansible - Task

[Back](../ansible.md)

- [Ansible - Task](#ansible---task)
  - [Task](#task)
  - [Key Components](#key-components)
  - [Execution \& Behavior Directives](#execution--behavior-directives)

---

## Task

- `Task`
  - a **single unit of action** within a playbook.
  - includes a list of `module`
    - execute specific `modules` against the target machines **in a defined sequence**.
  - a **dictionary**
    - `task` in a play is a **list**, **the ORDER of tasks matters**

## Key Components

- `name`:
  - A human-readable text block detailing the task's purpose.
  - displays in the command line interface output during execution.
- **Module Call** :
  - specifies the executable code segment that carries out the target system configuration
    - e.g., `ansible.builtin.apt`, `ansible.builtin.copy`.
- **Module Arguments**:
  - The indented **key-value pairs** nested directly beneath the **module name**.
  - supply data parameters (like path, state, or mode) to customize the action.

- Sample:

```yaml
- name: Ensure Apache is installed
  ansible.builtin.apt:
    name: apache2
    state: present
```

---

## Execution & Behavior Directives

- `become`
  - **Escalates privileges** on the target node.
  - `become: true`

- `when`
  - Evaluates a conditional statement so a task only runs if specific criteria are met.

- `loop` / `with_<lookup>`
  - Loops
  - **Repeats** the task iteration sequence over an array or dictionary of values.

- `register`
  - **captures** a task’s **output** and **storing** it in a **variable** for use in later tasks.

- `notify`
  - Handler Triggers
  - Flags a named `Ansible Handler Task` to execute at the end of the play if the current module forces a status change on the host.

- `ignore_errors`
  - Error Control, Dictates whether playbook progression should stop or continue if the specific task encounters a failure state.

- `tags`:
  - Filtering Labels. Attaches metadata keywords to the task, allowing users to run or skip specific blocks via CLI arguments.

- `delegate_to`:
  - execute a specific task on a different machine than the target host defined by the play.

```yaml
- name: Ensure Apache is installed
  ansible.builtin.apt:
    name: apache2
    state: present
  become: true
  when: ansible_os_family == "Debian"
  register: install_result
  notify: Restart Apache
```

---
