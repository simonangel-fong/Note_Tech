# Ansible - Playbook

[Back](../ansible.md)

- [Ansible - Playbook](#ansible---playbook)
  - [Play \& Playbook](#play--playbook)
    - [Components of a play](#components-of-a-play)
  - [Playbook Verification](#playbook-verification)
  - [Syntax Check](#syntax-check)
  - [Ansible Lint](#ansible-lint)

---

## Play & Playbook

- `Module`

  - the action defined in a `task` to be executed
  - common type of module:
    - command
    - script
    - yum
    - service

- `Task`

  - a list of actions to be performed on the hosts
  - a task is a dictionary
    - but task in a play is a **list**, **the ORDER of tasks matters**

- `Play`

  - a **single section** within a `playbook` that **maps** a set of **tasks** to a specific group of **hosts**.
  - Each play defines **which hosts to target**, **what tasks to perform**, and optional settings like **variables** or **directives** (e.g., `gather_facts` or `become`).
  - Purpose: **Groups tasks** for a specific set of **hosts**, allowing a playbook to target different hosts or perform different tasks in sequence.
  - Task execution:
    - a play is a **dictionary**, the position of **properties** does not matter.
      - But plays in a playbook is **list**, the position of the **plays** matters
    - tasks defined within a single play in an Ansible playbook are **executed in the order they are listed in the YAML file**, from top to bottom.
    - By default, each task must complete (or fail) before the next task begins

- `Playbook`

  - a list of plays
  - a YAML file that **defines a set of automated tasks to be executed** on one or more managed hosts.
  - used to **organize and orchestrate configuration management**, application deployment, or other automation tasks in Ansible.
  - Purpose: **Organizes and executes** a **collection** of automation **tasks**.
  - Play execution:
    - plays in a playbook are executed **in the order they are defined in the YAML file**.
    - By default, complete all tasks for all targeted hosts in one play before moving to the next play.
      - Ansible operates as a **single process** on the `control node`, managing **subprocesses** for tasks and connections to **hosts**.

- Command to run a playbook
  - `ansible-playbook playbook_file`

---

### Components of a play

- `hosts`:
  - Specifies the **target hosts** or **groups** from the inventory.
- `tasks`:

  - A list of **actions** (using `Ansible modules`) to execute.

- `vars`:
  - **Optional** variables for the play.
- `gather_facts`:
  - Boolean to enable/disable fact collection.

---

## Playbook Verification

- Good practices to verify playbook before executing in production.

  - Helps in catching the error or unexpected behaviors.

- Type of mode provided for verification:
  - `Check mode`:
    - execute the playbook without making any actual changes on the hosts, to preview the changes before applying them.
    - command: `ansible-playbook playbook_file --check`
    - Causion: not all module support `check mode`
  - `Diff mode`:
    - run with `check mode`
    - provide a before-and-after comparison of changes
    - command: `ansible-playbook playbook_file --check --diff`

---

## Syntax Check

- Ensure playbook syntax is error-free
- `ansible-playbook playbook_file --syntax-check`

---

## Ansible Lint

- `Ansible Lint`
  - a command-line tool used to **check** Ansible playbooks, roles, and collections for **best practices**, potential **errors**, and **style violations**.
  - ensures that Ansible code is **consistent, maintainable, and adheres to recommended guidelines**, helping to catch issues before execution.

```sh
ansible-lint playbook.yml
# WARNING  Listing 2 violation(s) that are fatal
# fqcn[action-core]: Use FQCN for builtin module actions (debug).
# get_fact_variable.yaml:4 Use `ansible.builtin.debug` or `ansible.legacy.debug` instead.

# fqcn[action-core]: Use FQCN for builtin module actions (debug).
# get_fact_variable.yaml:8 Use `ansible.builtin.debug` or `ansible.legacy.debug` instead.

# Read documentation for instructions on how to ignore specific rule violations.

#                  Rule Violation Summary
#  count tag               profile    rule associated tags
#      2 fqcn[action-core] production formatting

# Failed: 2 failure(s), 0 warning(s) on 1 files. Last profile that met the validation criteria was 'shared'. Rating: 4/5 star
```
