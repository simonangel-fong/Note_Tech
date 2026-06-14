# Ansible - Include & Import

[Back](../ansible.md)

- [Ansible - Include \& Import](#ansible---include--import)
  - [Include vs Import](#include-vs-import)
  - [Imports (Static)](#imports-static)
  - [Includes (Dynamic)](#includes-dynamic)
    - [Lab: import](#lab-import)
    - [Lab: include](#lab-include)

## Include vs Import

| Feature           | Import                                        | Include                                              |
| ----------------- | --------------------------------------------- | ---------------------------------------------------- |
| When processed    | Static - Before execution (at **parse time**) | During **runtime**, as it's reached                  |
| Loops support     | Not supported                                 | Supported                                            |
| Conditionals      | Applied at runtime                            | Evaluates **runtime variables** per task             |
| Playbook Debugger | Finds syntax/missing file errors immediately  | Only throws errors when execution reaches that point |

---

## Imports (Static)

- `Imports`
  - **statically** loading external files or components into your automation.
  - Ansible **reads and compiles** imported files **before execution** begins (at parse time).
    - The `imported` tasks are **treated as if** they were written directly in the **main playbook**.

- Common Uses:
  - `import_tasks`:
    - Statically pulls in a YAML file of **tasks**.
  - `import_playbook`:
    - Pulls in an entirely separate **playbook file**.
  - `import_role`:
    - Statically injects an Ansible **role**.

```yaml
- name: Playbook to import tasks
  hosts: all
  tasks:
    - name: Import web server tasks
      ansible.builtin.import_tasks: web-setup.yml
```

---

## Includes (Dynamic)

- `Includes`
  - the **dynamic** reuse of files or roles within the playbooks.
  - Ansible reads and processes included files **during runtime**, exactly when the task is reached.
    - Ansible evaluates each file one by one **while executing** the playbook.

- Common Uses:
  - `include_tasks`:
    - Dynamically pulls a task file at runtime.
  - `include_role`:
    - Dynamically pulls an Ansible role, letting you loop or run conditionals on the role itself.
  - `include_vars`:
    - Dynamically loads YAML or JSON variable files during playbook execution.

---

### Lab: import

```yaml
# demo_import_task_main.yaml
---
- name: "Import Tasks Lab"
  hosts: ubuntu-c
  gather_facts: false

  tasks:
    - name: Before import
      debug:
        msg: "About to import task file..."

    - name: Import say_hello tasks
      import_tasks: demo_import_task_main_hello.yaml

    - name: After import
      debug:
        msg: "Task file imported and complete"

---
# demo_import_task_main_hello.yaml
- name: Confirm task file was loaded
  debug:
    msg: "This is the task file"
```

```sh
ansible-playbook demo_import_task_main.yaml
# PLAY [Import Tasks Lab] ************************************************************************************************************************************

# TASK [Before import] ***************************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "About to import task file..."
# }

# TASK [Confirm task file was loaded] ************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This is the task file"
# }

# TASK [After import] ****************************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Task file imported and complete"
# }
```

---

### Lab: include

```yaml
---
# demo_include_task_main_hello.yaml
- name: Confirm task file was loaded
  debug:
    msg: "This is the task file"
---
# demo_include_task_main.yaml
- name: "Include Tasks Lab"
  hosts: ubuntu-c
  gather_facts: true

  tasks:
    - name: Before include
      debug:
        msg: "About to include task file..."

    - name: Include say_hello tasks
      include_tasks: demo_include_task_main_hello.yaml

    - name: After include
      debug:
        msg: "Include block complete"
```

```sh
ansible-playbook demo_include_task_main.yaml
# PLAY [Include Tasks Lab] ***********************************************************************************************************************************

# TASK [Gathering Facts] *************************************************************************************************************************************
# ok: [ubuntu-c]

# TASK [Before include] **************************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "About to include task file..."
# }

# TASK [Include say_hello tasks] *****************************************************************************************************************************
# included: /home/ansible/diveintoansible/Structuring Ansible Playbooks/Using Include and Import/02/demo_include_task_main_hello.yaml for ubuntu-c

# TASK [Confirm task file was loaded] ************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This is the task file"
# }

# TASK [After include] ***************************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Include block complete"
# }
```
