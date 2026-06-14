# Ansible - Tag

[Back](../ansible.md)

- [Ansible - Tag](#ansible---tag)
  - [Tag](#tag)
    - [Common Command options](#common-command-options)
    - [Lab: tag](#lab-tag)

---

## Tag

- `tags`
  - labels applied to `tasks`, `plays`, or `roles`.
  - execute or skip specific parts of a playbook without running the entire file.
- can be used at `play` level to **control play execution**

- Built-In Tags
  - `always`:
    - The task will always run, even if explicitly target another tag
    - unless use `--skip-tags always`
  - `never`:
    - The task will **never run** unless explicitly call it with `--tags never`.
  - `tagged`:
    - Runs all tasks that have **at least one tag**.
  - `untagged`:
    - Runs all tasks that have **no tags** assigned to them.

---

### Common Command options

- `--tags <tag1>,<tag2>` / `-t <tag1>,<tag2>`
  - Executes only the tasks that match the specified tags.
- `--skip-tags <tag1>,<tag2>`:
  - Executes all tasks except those assigned the specified tags.
- `--list-tags`
  - Generates a quick overview listing all available tags within the target playbook.
- `--list-tasks --tags` / `--list-tasks --skip-tags`
  - displays a dry-run list of exactly which tasks will execute.

---

### Lab: tag

```yaml
---
# demo_tags.yaml
- name: "Tags Lab"
  hosts: ubuntu-c
  gather_facts: false

  tasks:
    - name: "Always task - start of play"
      debug:
        msg: "This task always runs, even with -t or --skip-tags"
      tags: always

    # --- regular tagged tasks ---
    - name: "Web task - deploy web server"
      debug:
        msg: "Running web task"
      tags: web

    - name: "DB task - deploy database"
      debug:
        msg: "Running db task"
      tags: db

    - name: "Web + DB task - run migrations"
      debug:
        msg: "Running web and db task"
      tags:
        - web
        - db

    # --- never tag: skipped unless explicitly called ---
    - name: "Never task - maintenance mode"
      debug:
        msg: "This task is hidden unless you call -t maintenance"
      tags: never, maintenance

    # --- always tag: runs regardless of any filter ---
    - name: "Always task - end of play"
      debug:
        msg: "This task always runs too"
      tags: always
```

```sh
ansible-playbook demo_tags.yaml --list-tags
# playbook: demo_tags.yaml
#   play #1 (ubuntu-c): Tags Lab  TAGS: []
#       TASK TAGS: [always, db, maintenance, never, web]

ansible-playbook demo_tags.yaml
# PLAY [Tags Lab] ********************************************************************************************************************************************

# TASK [Always task - start of play] *************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs, even with -t or --skip-tags"
# }

# TASK [Web task - deploy web server] ************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running web task"
# }

# TASK [DB task - deploy database] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running db task"
# }

# TASK [Web + DB task - run migrations] **********************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running web and db task"
# }

# TASK [Always task - end of play] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs too"
# }

ansible-playbook demo_tags.yaml -t web
# PLAY [Tags Lab] ********************************************************************************************************************************************

# TASK [Always task - start of play] *************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs, even with -t or --skip-tags"
# }

# TASK [Web task - deploy web server] ************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running web task"
# }

# TASK [Web + DB task - run migrations] **********************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running web and db task"
# }

# TASK [Always task - end of play] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs too"
# }

ansible-playbook demo_tags.yaml -t db
# PLAY [Tags Lab] ********************************************************************************************************************************************

# TASK [Always task - start of play] *************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs, even with -t or --skip-tags"
# }

# TASK [DB task - deploy database] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running db task"
# }

# TASK [Web + DB task - run migrations] **********************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running web and db task"
# }

# TASK [Always task - end of play] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs too"
# }

ansible-playbook demo_tags.yaml --skip-tags db
# PLAY [Tags Lab] ********************************************************************************************************************************************

# TASK [Always task - start of play] *************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs, even with -t or --skip-tags"
# }

# TASK [Web task - deploy web server] ************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running web task"
# }

# TASK [Always task - end of play] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs too"
# }

ansible-playbook demo_tags.yaml -t maintenance
# PLAY [Tags Lab] ********************************************************************************************************************************************

# TASK [Always task - start of play] *************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs, even with -t or --skip-tags"
# }

# TASK [Web task - deploy web server] ************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Running web task"
# }

# TASK [Always task - end of play] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs too"
# }

# PLAY RECAP *************************************************************************************************************************************************
# ubuntu-c                   : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

# ansible@ubuntu-c:~/diveintoansible/Structuring Ansible Playbooks/Using Tags/03$ ansible-playbook demo_tags.yaml -t maintenance

# PLAY [Tags Lab] ********************************************************************************************************************************************

# TASK [Always task - start of play] *************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs, even with -t or --skip-tags"
# }

# TASK [Never task - maintenance mode] ***********************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task is hidden unless you call -t maintenance"
# }

# TASK [Always task - end of play] ***************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "This task always runs too"
# }
```
