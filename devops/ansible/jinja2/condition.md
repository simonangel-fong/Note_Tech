# Ansible - Jinja2: Condition

[Back](../ansible.md)

- [Ansible - Jinja2: Condition](#ansible---jinja2-condition)
  - [Conditional](#conditional)
    - [Lab: `if` statement](#lab-if-statement)
    - [Lab: `if elif` statement](#lab-if-elif-statement)
    - [Lab: `if elif else` statement](#lab-if-elif-else-statement)

---

## Conditional

- if:

```yaml
{% if  -%}
{% endif %}
```

- if elif:

```yaml
{% if -%}
{% elif -%}
{% endif %}
```

- if elif else:

```yaml
{% if -%}
{% elif -%}
{% else -%}
{% endif %}
```

---

### Lab: `if` statement

```yaml
# demo_if.yaml
- hosts:
    - ubuntu-c
    - ubuntu
  tasks:
    - name: Ansible Jinja2 if
      debug:
        msg: >
          --== Ansible Jinja2 if statement ==--

          {# If the hostname is ubuntu-c, include a message -#}
          {% if ansible_hostname == "ubuntu-c" -%}
                This is ubuntu-c
          {% endif %}
```

```sh
ansible-playbook demo_if.yaml --syntax-check
# playbook: demo_if.yaml

ansible-playbook demo_if.yaml --list-hosts
# playbook: demo_if.yaml

#   play #1 (ubuntu-c,ubuntu): ubuntu-c,ubuntu    TAGS: []
#     pattern: ['ubuntu-c', 'ubuntu']
#     hosts (4):
#       ubuntu2
#       ubuntu-c
#       ubuntu1
#       ubuntu3

ansible-playbook demo_if.yaml
# PLAY [ubuntu-c,ubuntu] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]
# ok: [ubuntu2]
# ok: [ubuntu1]
# ok: [ubuntu3]

# TASK [Ansible Jinja2 if] ************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "--== Ansible Jinja2 if statement ==--\nThis is ubuntu-c\n"
# }
# ok: [ubuntu1] => {
#     "msg": "--== Ansible Jinja2 if statement ==--\n"
# }
# ok: [ubuntu2] => {
#     "msg": "--== Ansible Jinja2 if statement ==--\n"
# }
# ok: [ubuntu3] => {
#     "msg": "--== Ansible Jinja2 if statement ==--\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### Lab: `if elif` statement

```yaml
# demo_if_elif.yaml
- hosts:
    - ubuntu-c
    - ubuntu
  tasks:
    - name: Ansible Jinja2 if elif
      debug:
        msg: >
          --== Ansible Jinja2 if elif statement ==--

          {% if ansible_hostname == "ubuntu-c" -%}
             This is ubuntu-c
          {% elif ansible_hostname == "ubuntu1" -%}
             This is ubuntu1
          {% endif %}
```

```sh
ansible-playbook demo_if_elif.yaml --syntax-check
# playbook: demo_if_elif.yaml

ansible-playbook demo_if_elif.yaml --list-hosts
# playbook: demo_if_elif.yaml

#   play #1 (ubuntu-c,ubuntu): ubuntu-c,ubuntu    TAGS: []
#     pattern: ['ubuntu-c', 'ubuntu']
#     hosts (4):
#       ubuntu2
#       ubuntu1
#       ubuntu-c
#       ubuntu3

ansible-playbook demo_if_elif.yaml
# PLAY [ubuntu-c,ubuntu] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]
# ok: [ubuntu3]
# ok: [ubuntu2]
# ok: [ubuntu1]

# TASK [Ansible Jinja2 if elif] *******************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "--== Ansible Jinja2 if elif statement ==--\nThis is ubuntu-c\n"
# }
# ok: [ubuntu1] => {
#     "msg": "--== Ansible Jinja2 if elif statement ==--\nThis is ubuntu1\n"
# }
# ok: [ubuntu2] => {
#     "msg": "--== Ansible Jinja2 if elif statement ==--\n"
# }
# ok: [ubuntu3] => {
#     "msg": "--== Ansible Jinja2 if elif statement ==--\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### Lab: `if elif else` statement

```yaml
# demo_if_elif_else.yaml
- hosts:
    - ubuntu-c
    - ubuntu
  tasks:
    - name: Ansible Jinja2 if elif
      debug:
        msg: >
          --== Ansible Jinja2 if elif else statement ==--

          {% if ansible_hostname == "ubuntu-c" -%}
             This is ubuntu-c
          {% elif ansible_hostname == "ubuntu1" -%}
             This is ubuntu1
          {% else -%}
             This is good old {{ ansible_hostname }}
          {% endif %}
```

```sh
ansible-playbook demo_if_elif_else.yaml --syntax-check
# playbook: demo_if_elif_else.yaml

ansible-playbook demo_if_elif_else.yaml
# PLAY [ubuntu-c,ubuntu] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]
# ok: [ubuntu1]
# ok: [ubuntu3]
# ok: [ubuntu2]

# TASK [Ansible Jinja2 if elif] *******************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "--== Ansible Jinja2 if elif else statement ==--\nThis is ubuntu-c\n"
# }
# ok: [ubuntu1] => {
#     "msg": "--== Ansible Jinja2 if elif else statement ==--\nThis is ubuntu1\n"
# }
# ok: [ubuntu2] => {
#     "msg": "--== Ansible Jinja2 if elif else statement ==--\nThis is good old ubuntu2\n"
# }
# ok: [ubuntu3] => {
#     "msg": "--== Ansible Jinja2 if elif else statement ==--\nThis is good old ubuntu3\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
