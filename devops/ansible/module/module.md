# Ansible - Module

[Back](../ansible.md)

- [Ansible - Module](#ansible---module)
  - [Module](#module)
    - [Command Commands](#command-commands)
    - [Common Module](#common-module)
  - [Lab: Module Document](#lab-module-document)
  - [Lab: setup module](#lab-setup-module)
  - [Lab: file module](#lab-file-module)
  - [Lab: `copy` Module Demo](#lab-copy-module-demo)
  - [Lab: `command` Module Demo](#lab-command-module-demo)
  - [Lab: `fetch` Module Demo](#lab-fetch-module-demo)

---

## Module

- `module`
  - a **reusable, standalone script or program** that performs a specific task on a managed host.
  - the building blocks of Ansible playbooks, enabling automation tasks like installing packages, managing files, configuring services, or interacting with cloud services.

---

### Command Commands

| Command                   | Desc                      |
| ------------------------- | ------------------------- |
| `ansible-doc -l`          | list all modules          |
| `ansible-doc module_name` | Get doc of a given module |

---

### Common Module

- Utilities & Command Execution

| Module    | Purpose                                                    |
| --------- | ---------------------------------------------------------- |
| `setup`   | Gathers remote hosts' `facts`(detailed system information) |
| `command` | Run a command (no shell features like redirection, pipes)  |
| `shell`   | Run a command through a shell (allows pipes, redirection)  |
| `script`  | Upload and execute a local script on the remote node       |
| `debug`   | Print variables or messages for debugging                  |
| `assert`  | Validate conditions (fail if not true)                     |

- System / Package Management

| Module        | Purpose                                               |
| ------------- | ----------------------------------------------------- |
| `apt`         | Manage packages on Debian/Ubuntu systems              |
| `yum` / `dnf` | Manage packages on RHEL/CentOS/Fedora                 |
| `package`     | Generic package manager abstraction (works across OS) |
| `service`     | Manage services (start, stop, enable, disable)        |
| `systemd`     | Advanced systemd service management                   |

- File & Directory Management

| Module      | Purpose                                                         |
| ----------- | --------------------------------------------------------------- |
| `file`      | Manage file attributes (permissions, owner, directory, symlink) |
| `copy`      | Copy files from control node to target                          |
| `fetch`     | Copy files from target back to control node                     |
| `template`  | Deploy Jinja2 template files with variables                     |
| `unarchive` | Extract archives (tar, zip, etc.)                               |

- User & Group Management

| Module           | Purpose                      |
| ---------------- | ---------------------------- |
| `user`           | Create, modify, remove users |
| `group`          | Manage groups                |
| `authorized_key` | Manage SSH keys for users    |

- Networking

| Module      | Purpose                                                 |
| ----------- | ------------------------------------------------------- |
| `ping`      | Test connectivity (simple check if host is reachable)   |
| `uri`       | Interact with web services / APIs (HTTP GET/POST, etc.) |
| `get_url`   | Download files from the internet                        |
| `firewalld` | Manage firewalld rules on Linux                         |
| `iptables`  | Manage iptables rules                                   |

- Database

| Module            | Purpose                                   |
| ----------------- | ----------------------------------------- |
| `mysql_db`        | Manage MySQL/MariaDB databases            |
| `mysql_user`      | Manage MySQL/MariaDB users and privileges |
| `postgresql_db`   | Manage PostgreSQL databases               |
| `postgresql_user` | Manage PostgreSQL users/roles             |

- Cloud & Virtualization

| Module                 | Purpose                       |
| ---------------------- | ----------------------------- |
| `ec2` / `ec2_instance` | Manage AWS EC2 instances      |
| `s3`                   | Manage AWS S3 buckets/objects |
| `azure_rm_*`           | Manage Azure resources        |
| `gcp_*`                | Manage GCP resources          |
| `docker_container`     | Manage Docker containers      |
| `docker_image`         | Manage Docker images          |

---

## Lab: Module Document

```sh
# list module
ansible-doc -l
# amazon.aws.autoscaling_group                                                                        Create or delete AWS AutoScaling Groups...
# amazon.aws.autoscaling_group_info                                                                   Gather information about EC2 Auto Scali...
# amazon.aws.aws_az_info                                                                              Gather information about availability z...
# amazon.aws.aws_caller_info                                                                          Get information about the user and acco...
# amazon.aws.aws_region_info                                                                          Gather information about AWS regions

# get doc of file module
ansible-doc file
# > MODULE ansible.builtin.file (/usr/local/lib/python3.10/dist-packages/ansible/modules/file.py)

#   Set attributes of files, directories, or symlinks and their targets.
#   Alternatively, remove files, symlinks or directories.
#   Many other modules support the same options as the ansible.builtin.file module - including
#   ansible.builtin.copy, ansible.builtin.template, and ansible.builtin.assemble.
#   For Windows targets, use the ansible.windows.win_file module instead.

# OPTIONS (red indicates it is required):

#    access_time  This parameter indicates the time the file's access time should be set to.
#                 Should be `preserve' when no modification is required, `YYYYMMDDHHMM.SS' when using
#                 default time format, or `now'.
#                 Default is `None' meaning that `preserve' is the default for `state=[file,directory,link,hard]' and
#                 `now' is default for `state=touch'.
#         default: null
#         type: str

#    access_time_format  When used with `access_time', indicates the time format that must be used.
#                        Based on default Python format (see time.strftime doc).
```


---


## Lab: setup module

```sh
ansible ubuntu1 -m setup | more
# ubuntu1 | SUCCESS => {
#     "ansible_facts": {
#         "ansible_all_ipv4_addresses": [
#             "172.19.0.5"
#         ],
#         "ansible_all_ipv6_addresses": [],
#         "ansible_apparmor": {
#             "status": "disabled"
#         },
#         "ansible_architecture": "x86_64",
#         "ansible_bios_date": "NA",
#         "ansible_bios_vendor": "NA",
#         "ansible_bios_version": "NA",
# ...
```

---

## Lab: file module

```sh
# create file
ansible ubuntu -m file -a 'path=/tmp/test state=touch'
# ubuntu1 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"dest": "/tmp/test","gid": 0,"group": "root","mode": "0644","owner": "root","size": 0,"state": "file","uid": 0}
# ubuntu3 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"dest": "/tmp/test","gid": 0,"group": "root","mode": "0644","owner": "root","size": 0,"state": "file","uid": 0}
# ubuntu2 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"dest": "/tmp/test","gid": 0,"group": "root","mode": "0644","owner": "root","size": 0,"state": "file","uid": 0}

# set permission
ansible ubuntu -m file -a 'path=/tmp/test state=file mode=600' -o
# ubuntu1 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"gid": 0,"group": "root","mode": "0600","owner": "root","path": "/tmp/test","size": 0,"state": "file","uid": 0}
# ubuntu2 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"gid": 0,"group": "root","mode": "0600","owner": "root","path": "/tmp/test","size": 0,"state": "file","uid": 0}
# ubuntu3 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"gid": 0,"group": "root","mode": "0600","owner": "root","path": "/tmp/test","size": 0,"state": "file","uid": 0}
```

---

## Lab: `copy` Module Demo

```sh
# create a new file locally
touch /tmp/x

# copy from local to remote
ansible ubuntu -m copy -a 'src=/tmp/x dest=/tmp/x' -o
# ubuntu2 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/x","gid": 0,"group": "root","md5sum": "d41d8cd98f00b204e9800998ecf8427e","mode": "0644","owner": "root","size": 0,"src": "/home/ansible/.ansible/tmp/ansible-tmp-1781212704.3009949-11844-278460051000657/.source","state": "file","uid": 0}
# ubuntu1 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/x","gid": 0,"group": "root","md5sum": "d41d8cd98f00b204e9800998ecf8427e","mode": "0644","owner": "root","size": 0,"src": "/home/ansible/.ansible/tmp/ansible-tmp-1781212704.2721531-11840-187423861372866/.source","state": "file","uid": 0}
# ubuntu3 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/x","gid": 0,"group": "root","md5sum": "d41d8cd98f00b204e9800998ecf8427e","mode": "0644","owner": "root","size": 0,"src": "/home/ansible/.ansible/tmp/ansible-tmp-1781212704.8100295-11916-145682453578275/.source","state": "file","uid": 0}

# copy from remote path to remote path
ansible ubuntu -m copy -a 'remote_src=yes src=/tmp/x dest=/tmp/y' -o
# ubuntu3 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/y","gid": 0,"group": "root","md5sum": "d41d8cd98f00b204e9800998ecf8427e","mode": "0644","owner": "root","size": 0,"src": "/tmp/x","state": "file","uid": 0}
# ubuntu1 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/y","gid": 0,"group": "root","md5sum": "d41d8cd98f00b204e9800998ecf8427e","mode": "0644","owner": "root","size": 0,"src": "/tmp/x","state": "file","uid": 0}
# ubuntu2 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/y","gid": 0,"group": "root","md5sum": "d41d8cd98f00b204e9800998ecf8427e","mode": "0644","owner": "root","size": 0,"src": "/tmp/x","state": "file","uid": 0}
```

---

## Lab: `command` Module Demo

```sh
ansible ubuntu -a "hostname" -o
# ubuntu1 | CHANGED | rc=0 | (stdout) ubuntu1
# ubuntu2 | CHANGED | rc=0 | (stdout) ubuntu2
# ubuntu3 | CHANGED | rc=0 | (stdout) ubuntu3

# create file
ansible ubuntu -a "touch /tmp/test_command_module creates=/tmp/test_command_module" -o
# ubuntu1 | CHANGED | rc=0 | (stdout)
# ubuntu3 | CHANGED | rc=0 | (stdout)
# ubuntu2 | CHANGED | rc=0 | (stdout)

# repeat: skip, with sucess
ansible ubuntu -a "touch /tmp/test_command_module creates=/tmp/test_command_module" -o
# ubuntu3 | SUCCESS | rc=0 | (stdout) skipped, since /tmp/test_command_module exists
# ubuntu1 | SUCCESS | rc=0 | (stdout) skipped, since /tmp/test_command_module exists
# ubuntu2 | SUCCESS | rc=0 | (stdout) skipped, since /tmp/test_command_module exists

# remove files
ansible ubuntu -a "rm /tmp/test_command_module removes=/tmp/test_command_module" -o
# ubuntu2 | CHANGED | rc=0 | (stdout)
# ubuntu3 | CHANGED | rc=0 | (stdout)
# ubuntu1 | CHANGED | rc=0 | (stdout)

ansible ubuntu -a "rm /tmp/test_command_module removes=/tmp/test_command_module" -o
# ubuntu2 | SUCCESS | rc=0 | (stdout) skipped, since /tmp/test_command_module does not exist
# ubuntu3 | SUCCESS | rc=0 | (stdout) skipped, since /tmp/test_command_module does not exist
# ubuntu1 | SUCCESS | rc=0 | (stdout) skipped, since /tmp/test_command_module does not exist
```

---

## Lab: `fetch` Module Demo

```sh
# create file in remote
ansible ubuntu -m file -a 'path=/tmp/test_modules.txt state=touch mode=600' -o
# ubuntu1 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"dest": "/tmp/test_modules.txt","gid": 0,"group": "root","mode": "0600","owner": "root","size": 0,"state": "file","uid": 0}
# ubuntu3 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"dest": "/tmp/test_modules.txt","gid": 0,"group": "root","mode": "0600","owner": "root","size": 0,"state": "file","uid": 0}
# ubuntu2 | CHANGED => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": true,"dest": "/tmp/test_modules.txt","gid": 0,"group": "root","mode": "0600","owner": "root","size": 0,"state": "file","uid": 0}

ansible ubuntu -m fetch -a 'src=/tmp/test_modules.txt dest=/tmp' -o
# ubuntu3 | CHANGED => {"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/ubuntu3/tmp/test_modules.txt","md5sum": "d41d8cd98f00b204e9800998ecf8427e","remote_checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","remote_md5sum": null}
# ubuntu2 | CHANGED => {"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/ubuntu2/tmp/test_modules.txt","md5sum": "d41d8cd98f00b204e9800998ecf8427e","remote_checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","remote_md5sum": null}
# ubuntu1 | CHANGED => {"changed": true,"checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","dest": "/tmp/ubuntu1/tmp/test_modules.txt","md5sum": "d41d8cd98f00b204e9800998ecf8427e","remote_checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709","remote_md5sum": null}

# confirm
ls /tmp/ubuntu*/tmp
# /tmp/ubuntu1/tmp:
# test_modules.txt

# /tmp/ubuntu2/tmp:
# test_modules.txt

# /tmp/ubuntu3/tmp:
# test_modules.txt

```