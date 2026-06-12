# Ansible - Inventory

[Back](../ansible.md)

- [Ansible - Inventory](#ansible---inventory)
  - [Inventory](#inventory)
    - [Static Inventory \& Dynamic Inventory](#static-inventory--dynamic-inventory)
    - [Common Commands](#common-commands)
  - [Inventory File](#inventory-file)
    - [Lab: cfg file specify inventory file](#lab-cfg-file-specify-inventory-file)
    - [Lab: json inventory file](#lab-json-inventory-file)
  - [Groups](#groups)
    - [Lab: Group](#lab-group)
    - [Lab: Parent and children](#lab-parent-and-children)
  - [Inventory variables](#inventory-variables)
    - [Common Variables](#common-variables)
    - [Group Vairable](#group-vairable)
    - [Lab: Variables](#lab-variables)
    - [Lab: ssh as root](#lab-ssh-as-root)
    - [Lab: privilege escalation](#lab-privilege-escalation)

---

## Inventory

- `inventory`
  - a centralized list or catalog of the **servers, devices, and nodes** mananged by Ansible
  - enable to
    - organize them into `groups`
    - assign specific `variables`

- Connections can be built:
  - Linux: SSH
  - Windows: Powershell Remoting

### Static Inventory & Dynamic Inventory

- `Static Inventory`
  - Manually curated text files in `INI` or `YAML` format.
  - Best for:
    - Small-scale environments,
    - bare-metal servers,
    - or staging environments where IP addresses and hostnames rarely change.
  - Common Grouped by:
    - function, e.g., `[web_servers]`
    - environment, e.g., `[production]`
  - Common variables:
    - ansible_ssh_user
    - ansible_network_os

- `Dynamic Inventory`
  - Plugins that query external APIs in real-time
  - best for:
    - Large, elastic environments where servers scale up and down rapidly,
    - or ephemeral CI/CD environments.
  - Common grouped by
    - tag, region

---

### Common Commands

| CMD                                                | DESC                                                             |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| `ansible-inventory --list`                         | Show the full inventory in JSON format.                          |
| `ansible-inventory -i inventory.ini --list`        | Show full inventory from a specific inventory file.              |
| `ansible-inventory --list --yaml`                  | Output full inventory in YAML format instead of JSON.            |
| `ansible-inventory --list --toml`                  | Output inventory in TOML format instead of JSON.                 |
| `ansible-inventory --list --export`                | Export inventory in a more static/export-friendly format.        |
| `ansible-inventory --list --output inventory.json` | Save inventory output to a file instead of printing to terminal. |
| `ansible-inventory --graph`                        | Show inventory groups and hosts as a tree/graph.                 |
| `ansible-inventory --graph all`                    | Show the full inventory tree from the `all` group.               |
| `ansible-inventory --graph web`                    | Show the inventory graph starting from the `web` group.          |
| `ansible-inventory --graph --vars`                 | Show inventory graph including variables.                        |
| `ansible-inventory --host server1`                 | Show variables for one specific host.                            |

---

## Inventory File

- `inventory file`:
  - a **configuration file** that defines the managed nodes (servers, network devices, or virtual machines) that Ansible interacts with and automates.
  - uses INI or YAML formats
- Default: `/etc/ansible/hosts`
- usage: with `-i`
  - `ansible-playbook -i production_inventory.yml deploy.yml`

- Components:
  - **Hosts**:
    - **individual machines** identified by `IP addresses` or `Fully Qualified Domain Names (FQDN)`
  - **Groups**:
    - **Logical collections** of hosts (e.g., webservers, dbservers, production).
    - `[GROUP_NAME]`
  - **Variables**
    - **Key-value pairs assigned** to hosts or groups (e.g., SSH users, connection ports, or OS types) so Ansible knows how to connect to them.
    - connection details, credentials, or custom settings per host/group.

- Specify inventory file
  - `ansible -i inventory_file`

---

- Host name can use range:

```ini
[centos]
centos1 ansible_user=root ansible_port=2222
centos[2:3] ansible_user=root

[ubuntu]
ubuntu[1:3] ansible_become=true ansible_become_pass=password
```

---

### Lab: cfg file specify inventory file

- cf can specify the `inventory file`

```sh
ls
# ansible.cfg  hosts

cat ansible.cfg
# [defaults]
# inventory = hosts
# host_key_checking = False

cat hosts
# [all]
# centos1

ansible all -m ping
# centos1 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }
```

---

### Lab: json inventory file

```sh
ls
# ansible.cfg hosts.json

cat ansible.cfg
# [defaults]
# inventory = hosts.json
# host_key_checking = False

cat hosts.json
# {
#     "control": {
#         "hosts": {
#             "ubuntu-c": {
#                 "ansible_connection": "local"
#             }
#         }
#     },
#     "centos": {
#         "hosts": {
#             "centos1": {
#                 "ansible_port": 2222
#             },
#             "centos2": null,
#             "centos3": null
#         },
#         "vars": {
#             "ansible_user": "root"
#         }
#     },
#     "ubuntu": {
#         "hosts": {
#             "ubuntu1": null,
#             "ubuntu2": null,
#             "ubuntu3": null
#         },
#         "vars": {
#             "ansible_become": true,
#             "ansible_become_pass": "password"
#         }
#     },
#     "linux": {
#         "children": {
#             "centos": null,
#             "ubuntu": null
#         }
#     }
# }

ansible all -m ping -o
# ubuntu2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# centos3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# ubuntu3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
```

---

## Groups

- `[all]`: default, applied to all hosts in inventory

- Sample: ini

```ini
[webservers]
web1.example.com ansible_user=ubuntu
web2.example.com ansible_user=ubuntu

[dbservers]
db1.example.com ansible_port=2222
db2.example.com
```

---

- Sample: yaml file

```yaml
all:
  hosts:
    mail.example.com:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
    dbservers:
      hosts:
        db1.example.com:
```

---

- Parent and Child relationship
  - common configuration can be applied to parent group level
  - specific configuration can be applied to children group level

---

- Sample: ini file

```ini
# parent
[webservers:children]
webservers_us
webservers_eu

# Children
[webservers_us]
server1_us.com ansible_host=192.168.8.101
server2_us.com ansible_host=192.168.8.102

# Children
[webservers_eu]
server1_eu.com ansible_host=10.12.0.101
server2_eu.com ansible_host=10.12.0.102
```

---

- yaml file

```yaml
# parent
all:
  children:
    # children-parent
    webservers:
      children:
        # children
        webservers_us:
          hosts:
            server1_us.com:
              ansible_host: 192.168.8.101
            server2_us.com:
              ansible_host: 192.168.8.102
        webservers_eu:
          hosts:
            server1_eu.com:
              ansible_host: 10.12.0.101
            server2_eu.com:
              ansible_host: 10.12.0.102
```

---

### Lab: Group

```sh
cat hosts
# [centos]
# centos1
# centos2
# centos3

# [ubuntu]
# ubuntu1
# ubuntu2
# ubuntu3

# ping a group
ansible centos -m ping
# centos3 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }
# centos1 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }
# centos2 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }


# ping all
ansible all -m ping
# ubuntu2 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.10"
#     },
#     "changed": false,
#     "ping": "pong"
# }
# ubuntu1 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.10"
#     },
#     "changed": false,
#     "ping": "pong"
# }
# centos3 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }
# centos2 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }
# centos1 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }
# ubuntu3 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.10"
#     },
#     "changed": false,
#     "ping": "pong"
# }

# same as all
ansible '*' -m ping

# condense oneline output
ansible all -m ping -o
# ubuntu2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# centos3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# ubuntu3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}

# list hosts
ansible all --list-host
  # hosts (6):
  #   centos1
  #   centos2
  #   centos3
  #   ubuntu1
  #   ubuntu2
  #   ubuntu3
ansible centos --list-host
  # hosts (3):
  #   centos1
  #   centos2
  #   centos3

# filter by regex
ansible ~.*3 --list-hosts
  # hosts (2):
  #   centos3
  #   ubuntu3
```

---

### Lab: Parent and children

```ini
[control]
ubuntu-c ansible_connection=local

[centos]
centos1 ansible_port=2222
centos[2:3]

[centos:vars]
ansible_user=root

[ubuntu]
ubuntu[1:3]

[ubuntu:vars]
ansible_become=true
ansible_become_pass=password

# parent:children
[linux:children]
centos
ubuntu
```

```sh
ansible linux -m ping -o
# centos1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# ubuntu2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"
```

---

## Inventory variables

- Using `-e` to specify extract variables or override existing variables.
  - `ansible all -e 'key=val'`

- ini file:

```ini
host_name var1=val1 var2=val2
```

- yaml

```yaml
group_name:
  hosts:
  vars:
```

---

### Common Variables

- Connection

| variables                      | Desc                                                          |
| ------------------------------ | ------------------------------------------------------------- |
| `ansible_host`                 | Target host IP or DNS name.                                   |
| `ansible_connection`           | Connection type, usually `ssh`, `local`, `winrm`, etc.        |
| `ansible_port`                 | Remote connection port, usually `22` for SSH.                 |
| `ansible_user`                 | Remote login user.                                            |
| `ansible_password`             | Remote login password. Newer/common name for SSH password.    |
| `ansible_ssh_pass`             | SSH password. Older alias; prefer `ansible_password`.         |
| `ansible_ssh_private_key_file` | SSH private key path.                                         |
| `ansible_ssh_common_args`      | Extra SSH arguments, often used for proxy/jump host settings. |
| `ansible_ssh_extra_args`       | Extra SSH arguments for SSH only.                             |
| `ansible_scp_extra_args`       | Extra arguments for `scp`.                                    |
| `ansible_sftp_extra_args`      | Extra arguments for `sftp`.                                   |

- privilege escalation

| Parameter                    | Desc                                                              |
| ---------------------------- | ----------------------------------------------------------------- |
| `ansible_become`             | Whether to use privilege escalation, like `sudo`.                 |
| `ansible_become_user`        | User to become, usually `root`.                                   |
| `ansible_become_pass`        | Password for privilege escalation.                                |
| `ansible_become_method`      | Escalation method, usually `sudo`; can also be `su`, `doas`, etc. |
| `ansible_python_interpreter` | Python path on remote host, for example `/usr/bin/python3`.       |
| `ansible_shell_type`         | Remote shell type, for example `sh`, `csh`, `powershell`.         |
| `ansible_shell_executable`   | Remote shell executable path, for example `/bin/bash`.            |

---

### Group Vairable

- define variable for group

```ini
# var for all
[all:vars]
# key=value

# var for a group
[group_name:vars]
# key=value
```

```yaml
group_name:
  hosts:
  vars:
```

- precedence:
  - host variables > group variables > parent variables

---

### Lab: Variables

### Lab: ssh as root

```sh
cat hosts
# [centos]
# centos1 ansible_user=root
# centos2 ansible_user=root
# centos3 ansible_user=root

# [ubuntu]
# ubuntu1
# ubuntu2
# ubuntu3

# test connect
ansible all -m ping -o
# ubuntu1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# centos3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# centos2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.9"},"changed": false,"ping": "pong"}
# ubuntu3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}

# check id
ansible all -m command -a 'id' -o
# ubuntu1 | CHANGED | rc=0 | (stdout) uid=1000(ansible) gid=1000(ansible) groups=1000(ansible),27(sudo)
# ubuntu2 | CHANGED | rc=0 | (stdout) uid=1000(ansible) gid=1000(ansible) groups=1000(ansible),27(sudo)
# ubuntu3 | CHANGED | rc=0 | (stdout) uid=1000(ansible) gid=1000(ansible) groups=1000(ansible),27(sudo)
# centos1 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
# centos2 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
# centos3 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
```

---

### Lab: privilege escalation

```sh
cat hosts
# [centos]
# centos1 ansible_user=root
# centos2 ansible_user=root
# centos3 ansible_user=root

# [ubuntu]
# ubuntu1 ansible_become=true ansible_become_pass=password
# ubuntu2 ansible_become=true ansible_become_pass=password
# ubuntu3 ansible_become=true ansible_become_pass=password

ansible all -a "id" -o
# ubuntu1 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
# ubuntu2 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
# centos1 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
# centos2 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
# centos3 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
# ubuntu3 | CHANGED | rc=0 | (stdout) uid=0(root) gid=0(root) groups=0(root)
```

---
