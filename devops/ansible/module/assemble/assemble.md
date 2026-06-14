# Ansible - Module: `assemble`

[Back](../../ansible.md)

- [Ansible - Module: `assemble`](#ansible---module-assemble)
  - [`assemble` Module](#assemble-module)
  - [Example](#example)

---

## `assemble` Module

- `assemble`
  - concatenated segmented configuration files into one

ref: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/assemble_module.html

---

## Example

```yaml
- name: Assemble from fragments from a directory
  ansible.builtin.assemble:
    src: /etc/someapp/fragments
    dest: /etc/someapp/someapp.conf
```
