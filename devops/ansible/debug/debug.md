# Ansible - Troubleshooting

[Back](../ansible.md)

- [Ansible - Troubleshooting](#ansible---troubleshooting)
  - [Common Issue](#common-issue)
    - [SSH connection](#ssh-connection)
    - [Debug Playbook](#debug-playbook)
    - [Configuration](#configuration)

---

## Common Issue

### SSH connection

```sh
# client side: show debug info
ssh -v <remote_host>

# server side: show debug info, looking for refused/fails
/usr/sbin/sshd -d -p 22
```

- Common issue:
  - password
  - authorized_keys mode <> 0600

---

### Debug Playbook

```sh
# syntax check
ansible-playbook <playbook> --syntax-check

# execution step by step
ansible-playbook <playbook> --step

# start at task name
ansible-playbook <playbook> --start-at-task='task_name'

# verbosity: 4 levels
ansible-playbook <playbook> -v
ansible-playbook <playbook> -vv
ansible-playbook <playbook> -vvv
ansible-playbook <playbook> -vvvv
```

---

### Configuration

- enable log

```ini
# ansible.cfg
log_path=log.txt
```

---
