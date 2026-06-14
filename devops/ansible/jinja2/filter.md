# Ansible - Jinja2: Filter

[Back](../ansible.md)

- [Ansible - Jinja2: Filter](#ansible---jinja2-filter)
  - [Filter](#filter)
    - [Lab: filters](#lab-filters)

---

## Filter

```yaml
# min []
{{ [1, 2, 3, 4, 5] | min }}

# max []
{{ [1, 2, 3, 4, 5] | max }}

# unique []
{{ [1, 1, 2, 2, 3, 3, 4, 4, 5, 5] | unique }}

# difference [1, 2, 3, 4, 5] [2, 3, 4]
{{ [1, 2, 3, 4, 5] | difference([2, 3, 4]) }}

# random ['rod', 'jane', 'freddy']
{{ ['rod', 'jane', 'freddy'] | random }}

# urlsplit hostname
{{ "http://docs.ansible.com/ansible/latest/playbooks_filters.html" | urlsplit('hostname') }}
```

---

### Lab: filters

```yaml
# demo_filer.yaml
- hosts:
    - ubuntu-c
  tasks:
    - name: Ansible Jinja2 filters
      debug:
        msg: >
          ---=== Ansible Jinja2 filters ===---
          --== min [1, 2, 3, 4, 5] ==--
          {{ [1, 2, 3, 4, 5] | min }}

          --== max [1, 2, 3, 4, 5] ==--
          {{ [1, 2, 3, 4, 5] | max }}

          --== unique [1, 1, 2, 2, 3, 3, 4, 4, 5, 5] ==--
          {{ [1, 1, 2, 2, 3, 3, 4, 4, 5, 5] | unique }}

          --== difference [1, 2, 3, 4, 5] vs [2, 3, 4] ==--
          {{ [1, 2, 3, 4, 5] | difference([2, 3, 4]) }}

          --== random ['rod', 'jane', 'freddy'] ==--
          {{ ['rod', 'jane', 'freddy'] | random }}

          --== urlsplit hostname ==--
          {{ "http://docs.ansible.com/ansible/latest/playbooks_filters.html" | urlsplit('hostname') }}
```

```sh
ansible-playbook demo_filer.yaml
# PLAY [ubuntu-c] *********************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]

# TASK [Ansible Jinja2 filters] *******************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "---=== Ansible Jinja2 filters ===--- --== min [1, 2, 3, 4, 5] ==-- 1\n--== max [1, 2, 3, 4, 5] ==-- 5\n--== unique [1, 1, 2, 2, 3, 3, 4, 4, 5, 5] ==-- [1, 2, 3, 4, 5]\n--== difference [1, 2, 3, 4, 5] vs [2, 3, 4] ==-- [1, 5]\n--== random ['rod', 'jane', 'freddy'] ==-- freddy\n--== urlsplit hostname ==-- docs.ansible.com\n"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
