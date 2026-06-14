# Ansible - Module: `group_by `

[Back](../../ansible.md)

- [Ansible - Module: `group_by `](#ansible---module-group_by-)
  - [`group_by ` Module](#group_by--module)
  - [Example](#example)

---

## `group_by ` Module

- `group_by `
  - create ad-hoc groups based on facts

- ref: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/add_host_module.html

---

## Example

```yaml
- hosts: all
  tasks:
    - name: Create group based on ansible_distribution
      group_by:
        key: "custom_{{ ansible_distribution | lower }}"

- hosts: custom_centos
  tasks:
    - name: Ping all in custom_centos
      ping:
```
