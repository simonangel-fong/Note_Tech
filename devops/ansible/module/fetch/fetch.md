# Ansible - Module: `fetch`

[Back](../../ansible.md)

- [Ansible - Module: `fetch`](#ansible---module-fetch)
  - [`fetch` Module](#fetch-module)
  - [Example](#example)

---

## `fetch` Module

- `fetch`:
  - fetch files from remote machines and storing them locally

- ref: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/fetch_module.html

---

## Example

```yaml
- name: Store file into /tmp/fetched/host.example.com/tmp/somefile
  ansible.builtin.fetch:
    src: /tmp/somefile
    dest: /tmp/fetched
```
