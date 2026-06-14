# Ansible - Blocks

[Back](../ansible.md)

- [Ansible - Blocks](#ansible---blocks)
  - [Ansible Blocks](#ansible-blocks)
  - [Lab: block](#lab-block)

---

## Ansible Blocks

- `Ansible block`
  - logically **group** `tasks` and apply common directives (such as when, become, or ignore_errors) **to all tasks** within it.
  - used for robust:
    - `try-catch/finally-style` error handling using `rescue` and `always` sections.

- Sample:

```yaml
- name: Deploy application
  block:
    - name: task 1
      <module>:
        <arg>: value

    - name: task 2
      <module>:
        <arg>: value

  rescue:
    - name: rescue taks 1
      <module>:
        <arg>: value

    - name: rescue taks 2
      <module>:
        <arg>: value

  always:
    - name: always taks 2
      <module>:
        <arg>: value
```

---

## Lab: block

```yaml
# demo_block.yaml
- name: Demo block
  hosts: linux
  tasks:
    - name: Install patch and python3-dnspython
      block:
        - name: Install patch
          package:
            name: patch

        # install package, centos not applied, fails
        - name: Install python3-dnspython
          package:
            name: python3-dnspython

      rescue:
        - name: Rollback patch
          package:
            name: patch
            state: absent

        - name: Rollback python3-dnspython
          package:
            name: python3-dnspython
            state: absent

      always:
        - debug:
            msg: This always runs, regardless
```

```sh
ansible-playbook demo_block.yaml
# PLAY [Demo block] *******************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [centos2]
# ok: [centos3]
# ok: [ubuntu3]
# ok: [ubuntu2]
# ok: [ubuntu1]

# TASK [Install patch] ****************************************************************************************************************
# ok: [centos2]
# changed: [centos3]
# ok: [ubuntu1]
# ok: [ubuntu2]
# ok: [ubuntu3]

# TASK [Install python3-dnspython] ****************************************************************************************************
# fatal: [centos2]: FAILED! => {"changed": false, "failures": ["No package python3-dnspython available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}
# fatal: [centos3]: FAILED! => {"changed": false, "failures": ["No package python3-dnspython available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}
# changed: [ubuntu2]
# changed: [ubuntu3]
# changed: [ubuntu1]

# TASK [Rollback patch] ***************************************************************************************************************
# changed: [centos3]
# changed: [centos2]

# TASK [Rollback python3-dnspython] ***************************************************************************************************
# ok: [centos3]
# ok: [centos2]

# TASK [debug] ************************************************************************************************************************
# ok: [centos2] => {
#     "msg": "This always runs, regardless"
# }
# ok: [centos3] => {
#     "msg": "This always runs, regardless"
# }
# ok: [ubuntu1] => {
#     "msg": "This always runs, regardless"
# }
# ok: [ubuntu2] => {
#     "msg": "This always runs, regardless"
# }
# ok: [ubuntu3] => {
#     "msg": "This always runs, regardless"
# }

# PLAY RECAP **************************************************************************************************************************
# centos2                    : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
# centos3                    : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
# ubuntu1                    : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
