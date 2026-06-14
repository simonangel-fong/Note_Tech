# Ansible - Magic Variables

[Back](../ansible.md)

- [Ansible - Magic Variables](#ansible---magic-variables)
  - [Magic Variables](#magic-variables)
    - [Common Variables](#common-variables)
    - [Lab: Common Vairables](#lab-common-vairables)
    - [Lab: hostvars in playbook](#lab-hostvars-in-playbook)

---

## Magic Variables

- `magic variables`
  - **pre-defined, read-only variables** automatically set by Ansible.
  - provide critical **metadata** about the environment, inventory structure, and playbook execution context.

- Commands to get magic variables

```sh
ansible <hosts> -m debug -a "var=<magic_variables>"
```

---

### Common Variables

- ref: https://docs.ansible.com/projects/ansible/latest/reference_appendices/special_variables.html

| Magic Variables      | Description                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------- |
| `inventory_hostname` | Host name defined in Ansible inventory.                                                      |
| `hostvars`           | A dictionary containing all **variables for every host** in the inventory.                   |
| `groups`             | A dictionary that lists all the **groups** in the inventory, and which hosts belong to them. |
| `group_names`        | A list of all the groups the **current host** belongs to.                                    |
| `playbook_dir`       | The **absolute path of the directory** containing the currently **executing playbook**.      |

---

### Lab: Common Vairables

```sh
ansible ubuntu-c --list-host
#   hosts (1):
#     ubuntu-c

ansible centos1 -m debug -a "var=inventory_hostname"
# centos1 | SUCCESS => {
#     "inventory_hostname": "centos1"
# }

# get var for port
ansible centos1 -m debug -a "var=hostvars[inventory_hostname]" | grep port
# "ansible_port": 2222,

ansible ubuntu-c -m debug -a "var=groups"
# ubuntu-c | SUCCESS => {
#     "groups": {
#         "all": [
#             "ubuntu-c",
#             "centos1",
#             "centos2",
#             "centos3",
#             "ubuntu1",
#             "ubuntu2",
#             "ubuntu3"
#         ],
#         "centos": [
#             "centos1",
#             "centos2",
#             "centos3"
#         ],
#         "control": [
#             "ubuntu-c"
#         ],
#         "linux": [
#             "centos1",
#             "centos2",
#             "centos3",
#             "ubuntu1",
#             "ubuntu2",
#             "ubuntu3"
#         ],
#         "ubuntu": [
#             "ubuntu1",
#             "ubuntu2",
#             "ubuntu3"
#         ],
#         "ungrouped": []
#     }
# }

ansible ubuntu-c -m debug -a "var=group_names"
# ubuntu-c | SUCCESS => {
#     "group_names": [
#         "control"
#     ]
# }

ansible ubuntu-c -m debug -a "var=playbook_dir"
# ubuntu-c | SUCCESS => {
#     "playbook_dir": "/home/ansible/diveintoansible/Ansible Playbooks, Deep Dive/Magic Variables/01"
# }
```

---

### Lab: hostvars in playbook

- `hostvars`:
  - used to access variables and facts belonging to other hosts in your inventory.

```yml
# demo_mv.yaml
- name: Print ansible_version
  hosts: ubuntu-c
  tasks:
    - debug:
        msg: "{{ hostvars['ubuntu-c'].ansible_version }}"
```

```sh
ansible-playbook demo_mv.yaml
# PLAY [Print ansible_version] ********************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]

# TASK [debug] ************************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": {
#         "full": "2.17.4",
#         "major": 2,
#         "minor": 17,
#         "revision": 4,
#         "string": "2.17.4"
#     }
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---
