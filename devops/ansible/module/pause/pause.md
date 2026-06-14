# Ansible - Module: `pause`

[Back](../../ansible.md)

- [Ansible - Module: `pause`](#ansible---module-pause)
  - [`pause` Module](#pause-module)
  - [Example](#example)
  - [`wait_for` module](#wait_for-module)
  - [Example](#example-1)

---

## `pause` Module

- `pause`:
  - **Pauses playbook execution** for a set amount of time, or until a prompt is acknowledged.
  - The default behavior is to pause with a prompt.

- ref: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/pause_module.html

---

## Example

- pause for 10s

```yaml
- hosts: localhost
  tasks:
    - name: Pause our playbook for 10 seconds
      pause:
        seconds: 10
```

- pause until enter

```yaml
- hosts: localhost
  tasks:
    - name: Prompt user to verify before continue
      pause:
        prompt: Please check that the webserver is running, press enter to continue
```

---

## `wait_for` module

- `wait_for`
  - wait for condition completed
- ref: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/wait_for_module.html#examples

---

## Example

```yaml
- name: Sleep for 300 seconds and continue with play
  ansible.builtin.wait_for:
    timeout: 300
  delegate_to: localhost

- name: Wait for port 8000 to become open on the host, don't start checking for 10 seconds
  ansible.builtin.wait_for:
    port: 8000
    delay: 10
```
