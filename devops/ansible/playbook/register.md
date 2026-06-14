# Ansible - Register

[Back](../ansible.md)

- [Ansible - Register](#ansible---register)
  - [Register](#register)
  - [Lab: Register](#lab-register)
  - [Lab: Register \& Condition](#lab-register--condition)

---

## Register

---

## Lab: Register

```yaml
# demo_register.yaml
- hosts: ubuntu2, centos2
  tasks:
    - name: Exploring register
      command: hostname -s
      register: hostname_output

    - name: Show hostname_output
      debug:
        var: hostname_output
```

```sh
ansible-playbook demo_register.yaml
# PLAY [ubuntu2, centos2] *************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu2]
# ok: [centos2]

# TASK [Exploring register] ***********************************************************************************************************
# changed: [centos2]
# changed: [ubuntu2]

# TASK [Show hostname_output] *********************************************************************************************************
# ok: [ubuntu2] => {
#     "hostname_output": {
#         "changed": true,
#         "cmd": [
#             "hostname",
#             "-s"
#         ],
#         "delta": "0:00:00.002205",
#         "end": "2026-06-13 13:36:25.406967",
#         "failed": false,
#         "msg": "",
#         "rc": 0,
#         "start": "2026-06-13 13:36:25.404762",
#         "stderr": "",
#         "stderr_lines": [],
#         "stdout": "ubuntu2",
#         "stdout_lines": [
#             "ubuntu2"
#         ]
#     }
# }
# ok: [centos2] => {
#     "hostname_output": {
#         "changed": true,
#         "cmd": [
#             "hostname",
#             "-s"
#         ],
#         "delta": "0:00:00.003679",
#         "end": "2026-06-13 13:36:25.397951",
#         "failed": false,
#         "msg": "",
#         "rc": 0,
#         "start": "2026-06-13 13:36:25.394272",
#         "stderr": "",
#         "stderr_lines": [],
#         "stdout": "centos2",
#         "stdout_lines": [
#             "centos2"
#         ]
#     }
# }

# PLAY RECAP **************************************************************************************************************************
# centos2                    : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

## Lab: Register & Condition

```yaml
# demo_register_when.yaml
- hosts: ubuntu2,centos2
  tasks:
    - name: Exploring register
      command: hostname -s
      when:
        - ansible_distribution == "CentOS"
        - ansible_distribution_major_version | int >= 8
      register: command_register

    - name: Install patch when changed
      yum:
        name: patch
        state: present
      # condition with `is`
      when: command_register is changed
```

```sh
# only change in centos
ansible-playbook demo_register_when.yaml
# PLAY [ubuntu2,centos2] **************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [centos2]
# ok: [ubuntu2]

# TASK [Exploring register] ***********************************************************************************************************
# skipping: [ubuntu2]
# changed: [centos2]

# TASK [Install patch when changed] ***************************************************************************************************
# skipping: [ubuntu2]
# changed: [centos2]

# PLAY RECAP **************************************************************************************************************************
# centos2                    : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=1    changed=0    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
```
