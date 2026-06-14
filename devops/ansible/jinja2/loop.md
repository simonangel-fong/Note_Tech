# Ansible - Jinja2: Loop

[Back](../ansible.md)

- [Ansible - Jinja2: Loop](#ansible---jinja2-loop)
  - [Loop](#loop)
    - [Lab: `for`](#lab-for)
    - [Lab: `for` `range`](#lab-for-range)
    - [Lab: `break`](#lab-break)
    - [Lab: `continue`](#lab-continue)

---

## Loop

- syntax:

```yaml
# for loop
{% for entry in ansible_interfaces -%}
  Interface entry {{ loop.index }} = {{ entry }}
{% endfor %}

# for range
{% for entry in range(1, 11) -%}
  {{ entry }}
{% endfor %}

# break
{% for entry in range(10, 0, -1) -%}
    {% if entry == 5 -%}
       {% break %}
    {% endif -%}
    {{ entry }}
{% endfor %}

# continue
{% for entry in range(10, 0, -1) -%}
  {% if entry is odd -%}
     {% continue %}
  {% endif -%}
  {{ entry }}
{% endfor %}
```

---

### Lab: `for`

```yaml
# demo_for.yaml
- hosts:
    - ubuntu-c
    - ubuntu
  tasks:
    - name: Ansible Jinja2 for
      debug:
        msg: >
          --== Ansible Jinja2 for statement ==--

          {% for entry in ansible_interfaces -%}
            Interface entry {{ loop.index }} = {{ entry }}
          {% endfor %}
```

```sh
ansible-playbook demo_for.yaml --syntax-check
# playbook: demo_for.yaml

ansible-playbook demo_for.yaml --list-hosts

ansible-playbook demo_for.yaml
# PLAY [ubuntu-c,ubuntu] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]
# ok: [ubuntu2]
# ok: [ubuntu3]
# ok: [ubuntu1]

# TASK [Ansible Jinja2 for] ************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "--== Ansible Jinja2 for statement ==--\nInterface entry 1 = eth0\nInterface entry 2 = lo\n"
# }
# ok: [ubuntu1] => {
#     "msg": "--== Ansible Jinja2 for statement ==--\nInterface entry 1 = lo\nInterface entry 2 = eth0\n"
# }
# ok: [ubuntu2] => {
#     "msg": "--== Ansible Jinja2 for statement ==--\nInterface entry 1 = lo\nInterface entry 2 = eth0\n"
# }
# ok: [ubuntu3] => {
#     "msg": "--== Ansible Jinja2 for statement ==--\nInterface entry 1 = lo\nInterface entry 2 = eth0\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

---

### Lab: `for` `range`

```yaml
# demo_for_range.yaml
- hosts:
    - ubuntu-c
    - ubuntu
  tasks:
    - name: Ansible Jinja2 for range
      debug:
        msg: >
          --== Ansible Jinja2 for range

          {% for entry in range(1, 11) -%}
             {{ entry }}
          {% endfor %}
```

```sh
ansible-playbook demo_for_range.yaml
# PLAY [ubuntu-c,ubuntu] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]
# ok: [ubuntu3]
# ok: [ubuntu1]
# ok: [ubuntu2]

# TASK [Ansible Jinja2 for range] ************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "--== Ansible Jinja2 for range\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"
# }
# ok: [ubuntu1] => {
#     "msg": "--== Ansible Jinja2 for range\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"
# }
# ok: [ubuntu2] => {
#     "msg": "--== Ansible Jinja2 for range\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"
# }
# ok: [ubuntu3] => {
#     "msg": "--== Ansible Jinja2 for range\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### Lab: `break`

```yaml
# demo_for_break.yaml
- hosts:
    - ubuntu-c
    - ubuntu
  tasks:
    - name: Ansible Jinja2 for range, reversed (simulate while greater 5)
      debug:
        msg: >
          --== Ansible Jinja2 for range, reversed (simulate while greater 5) ==--

          {% for entry in range(10, 0, -1) -%}
             {% if entry == 5 -%}
                {% break %}
             {% endif -%}
             {{ entry }}
          {% endfor %}
```

```sh
ansible-playbook demo_for_break.yaml
# PLAY [ubuntu-c,ubuntu] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]
# ok: [ubuntu3]
# ok: [ubuntu2]
# ok: [ubuntu1]

# TASK [Ansible Jinja2 for range, reversed (simulate while greater 5)] ****************************************************************
# ok: [ubuntu-c] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (simulate while greater 5) ==--\n10\n9\n8\n7\n6\n"
# }
# ok: [ubuntu1] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (simulate while greater 5) ==--\n10\n9\n8\n7\n6\n"
# }
# ok: [ubuntu2] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (simulate while greater 5) ==--\n10\n9\n8\n7\n6\n"
# }
# ok: [ubuntu3] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (simulate while greater 5) ==--\n10\n9\n8\n7\n6\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### Lab: `continue`

```yaml
# demo_for_continue.yaml
- hosts:
    - ubuntu-c
    - ubuntu
  tasks:
    - name: Ansible Jinja2 for range, reversed (continue if odd)
      debug:
        msg: >
          --== Ansible Jinja2 for range, reversed (continue if odd) ==--

          {% for entry in range(10, 0, -1) -%}
             {% if entry is odd -%}
                {% continue %}
             {% endif -%}
             {{ entry }}
          {% endfor %}
```

```sh
ansible-playbook demo_for_continue.yaml
# PLAY [ubuntu-c,ubuntu] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]
# ok: [ubuntu3]
# ok: [ubuntu2]
# ok: [ubuntu1]

# TASK [Ansible Jinja2 for range, reversed (continue if odd)] *************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (continue if odd) ==--\n10\n8\n6\n4\n2\n"
# }
# ok: [ubuntu1] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (continue if odd) ==--\n10\n8\n6\n4\n2\n"
# }
# ok: [ubuntu2] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (continue if odd) ==--\n10\n8\n6\n4\n2\n"
# }
# ok: [ubuntu3] => {
#     "msg": "--== Ansible Jinja2 for range, reversed (continue if odd) ==--\n10\n8\n6\n4\n2\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```
