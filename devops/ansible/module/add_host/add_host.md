# Ansible - Module: `add_host`

[Back](../../ansible.md)

- [Ansible - Module: `add_host`](#ansible---module-add_host)
  - [`add_host` Module](#add_host-module)
  - [Example](#example)

---

## `add_host` Module

- `add_host`
  - dynamically add targets to the running playbooks

- ref: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/add_host_module.html

---

## Example

```yaml
# set on client
- hosts: ubuntu-c
  tasks:
    - name: Add centos1 to adhoc_group
      add_host:
        name: centos1
        groups: adhoc_group1, adhoc_group2

# use new group
- hosts: adhoc_group1
  tasks:
    - name: Ping all in adhoc_group1
      ping:
```
