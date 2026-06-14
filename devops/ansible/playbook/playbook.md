# Ansible - Playbook

[Back](../ansible.md)

- [Ansible - Playbook](#ansible---playbook)
  - [Play \& Playbook](#play--playbook)
  - [Play](#play)
  - [Playbook](#playbook)
    - [Common Commands](#common-commands)
  - [Common Practices](#common-practices)
  - [Lab: Hello world Play Book](#lab-hello-world-play-book)
  - [Lab: Handler](#lab-handler)
  - [Lab: When](#lab-when)

---

## Play & Playbook

- `module`
  - a **reusable, standalone script or program** that performs a specific task on a managed host.
  - common type of module: `command`, `setup`, `copy`,...


## Play

- `play`
  - **groups a list of tasks** for a specific set of **hosts**
  - a **dictionary**, the position of **properties** does not matter.
    - `plays` in a playbook is **list**, the position of the **plays** matters
- **Components**
  - `host`:
    - **which hosts to target**
    - Specifies the **target hosts** or **groups** from the inventory.

  - `tasks`:
    - **what tasks to perform**
    - A list of `modules` to execute.
  - `vars`:
    - **Optional**
    - variables for the play.
  - `handlers`
    - **Optional**
    - special tasks that only run when they are **explicitly "notified" by another task**, and only if that task actually **makes a change** on the system

  - **directives**
    - **Optional**
    - `gather_facts`:a directive used to enable/disable fact collection.
    - `become`: a directive used for privilege escalation

  - By default, each `task` must complete (or fail) **before the next** `task` begins

---

## Playbook

- `Playbook`
  - a YAML file that **defines a set of automated tasks to be executed** on one or more managed hosts.
  - used to **organize and orchestrate configuration management**, application deployment, or other automation tasks in Ansible.
  - a list of `plays`
  - `plays` in a `playbook` are executed **in the order they are defined in the YAML file**.
  - By default, **complete** all `tasks` for all targeted hosts in one `play` **before** moving to the **next** `play`.
    - Ansible operates as a **single process** on the `control node`, managing `subprocesses` for `tasks` and connections to **hosts**.

---

### Common Commands

- Run playbook

| CMD                                                               | DESC                                                                      |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `ansible-playbook playbook.yml`                                   | Run a playbook using the default inventory.                               |
| `ansible-playbook playbook.yml --start-at-task "Install nginx"`   | Start execution from a specific task name.                                |
| `ansible-playbook playbook.yml --step`                            | Ask for **confirmation** before each task.                                |
| `ansible-playbook playbook.yml -b`                                | Run with privilege escalation, usually `sudo`.                            |
| `ansible-playbook playbook.yml -b -K`                             | Run with `sudo` and ask for the sudo **password**.                        |
| `ansible-playbook playbook.yml --tags install`                    | Run only tasks **tagged** `install`.                                      |
| `ansible-playbook playbook.yml --skip-tags restart`               | Run the playbook but skip tasks **tagged** `restart`.                     |
| `ansible-playbook playbook.yml --limit web`                       | Run only against **hosts or groups** matching `web`.                      |
| `ansible-playbook playbook.yml --limit server1`                   | Run only against one **host**. Useful for testing.                        |
| `ansible-playbook playbook.yml -e "app_version=1.2.3"`            | Pass extra **variables** from the command line.                           |
| `ansible-playbook playbook.yml -e @vars.yml`                      | Load extra **variables** from a YAML file.                                |
| `ansible-playbook playbook.yml --ask-vault-pass`                  | Ask for `Ansible Vault` password when encrypted variables/files are used. |
| `ansible-playbook playbook.yml --vault-password-file .vault_pass` | Use a vault password file instead of typing the password interactively.   |
| `ansible-playbook site.yml --flush-cache`                         | Clear Ansible fact cache before running.                                  |
| `ansible-playbook playbook.yml -f 20`                             | Set parallelism/forks. Runs against more hosts at once.                   |

- Inspection

| CMD                                            | DESC                                                                         |
| ---------------------------------------------- | ---------------------------------------------------------------------------- |
| `ansible-playbook playbook.yml --check`        | Dry run. Show what Ansible would change without actually changing the hosts. |
| `ansible-playbook playbook.yml --diff`         | Show file/config differences caused by supported modules.                    |
| `ansible-playbook playbook.yml --check --diff` | Very common safe test command: dry run plus show expected changes.           |
| `ansible-playbook playbook.yml --syntax-check` | Check YAML/playbook syntax without running tasks.                            |
| `ansible-playbook playbook.yml --list-hosts`   | Show which hosts the playbook would target.                                  |
| `ansible-playbook playbook.yml --list-tasks`   | Show tasks that would run.                                                   |
| `ansible-playbook playbook.yml --list-tags`    | Show available tags in the playbook.                                         |
| `ansible-playbook playbook.yml -v`             | Verbose output.                                                              |
| `ansible-playbook playbook.yml -vvv`           | More detailed debug output, useful for SSH/module troubleshooting.           |

- Connection

| CMD                                                                          | DESC                                           |
| ---------------------------------------------------------------------------- | ---------------------------------------------- |
| `ansible-playbook -i inventory.ini playbook.yml`                             | Run a playbook with a specific inventory file. |
| `ansible-playbook -i inventory.ini playbook.yml -u ubuntu`                   | Run as a specific remote SSH user.             |
| `ansible-playbook -i inventory.ini playbook.yml --private-key ~/.ssh/id_rsa` | Use a specific SSH private key.                |

---

## Common Practices

```sh
# Validate syntax
ansible-playbook playbook.yml --syntax-check

# Preview target hosts
ansible-playbook -i inventory.ini playbook.yml --list-hosts

# Safe dry run
ansible-playbook -i inventory.ini playbook.yml --check --diff

# Test on one host
ansible-playbook -i inventory.ini playbook.yml --limit server1

# Run one part only
ansible-playbook -i inventory.ini playbook.yml --tags install

# Skip risky tasks
ansible-playbook -i inventory.ini playbook.yml --skip-tags restart

# Run with sudo
ansible-playbook -i inventory.ini playbook.yml -b

# Pass variable
ansible-playbook -i inventory.ini playbook.yml -e "version=1.0.0"
```

---

## Lab: Hello world Play Book

```yaml
# hello_world.yaml
---
- name: Create and read hello world file
  hosts: localhost
  connection: local
  gather_facts: no

  # variable
  vars:
    message: "Hello World\n"

  tasks:
    - name: Create hello-world.txt in home directory
      ansible.builtin.copy:
        content: "{{ message }}"
        dest: "~/hello-world.txt"

    - name: Cat the contents of the file
      ansible.builtin.shell: cat ~/hello-world.txt
      register: command_output

    - name: Display file contents
      ansible.builtin.debug:
        msg: "{{ command_output.stdout }}"
```

```sh
# Validate syntax
ansible-playbook hello_world.yaml --syntax-check
# playbook: hello_world.yaml

ansible-playbook hello_world.yaml --list-hosts
# playbook: hello_world.yaml

#   play #1 (localhost): Create and read hello world file TAGS: []
#     pattern: ['localhost']
#     hosts (1):
#       localhost

ansible-playbook hello_world.yaml
# PLAY [Create and read hello world file] **********************************************************************************************

# TASK [Create hello-world.txt in home directory] **************************************************************************************
# ok: [localhost]

# TASK [Cat the contents of the file] **************************************************************************************************
# changed: [localhost]

# TASK [Display file contents] *********************************************************************************************************
# ok: [localhost] => {
#     "msg": "Hello World"
# }

# PLAY RECAP ***************************************************************************************************************************
# localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

# confirm
cat ~/hello-world.txt
# Hello World
```

- customized variable with command line

```sh
ansible-playbook hello_world.yaml -e 'message="Test on localhost\n"'
# PLAY [Create and read hello world file] **********************************************************************************************

# TASK [Create hello-world.txt in home directory] **************************************************************************************
# changed: [localhost]

# TASK [Cat the contents of the file] **************************************************************************************************
# changed: [localhost]

# TASK [Display file contents] *********************************************************************************************************
# ok: [localhost] => {
#     "msg": "Test on localhost"
# }

# PLAY RECAP ***************************************************************************************************************************
# localhost                  : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

cat ~/hello-world.txt
# Test on localhost

```

---

## Lab: Handler

- hello_world.yaml

```yaml
---
- name: Simple Handler Example
  hosts: localhost
  connection: local

  tasks:
    - name: Write hello world to file
      ansible.builtin.shell: echo "hello world\n" > ~/message.txt
      notify: Print success message

  handlers:
    - name: Print success message
      ansible.builtin.debug:
        msg: "Job done"
```

```sh
ansible-playbook hello_world.yaml
# PLAY [Simple Handler Example] ********************************************************************************************************

# TASK [Gathering Facts] ***************************************************************************************************************
# ok: [localhost]

# TASK [Write hello world to file] *****************************************************************************************************
# changed: [localhost]

# RUNNING HANDLER [Print success message] **********************************************************************************************
# ok: [localhost] => {
#     "msg": "Job done"
# }

# PLAY RECAP ***************************************************************************************************************************
# localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

--

## Lab: When

```ini
# hosts.ini
[control]
ubuntu-c ansible_connection=local

[centos]
centos[1:3]

[centos:vars]
ansible_user=root

[ubuntu]
ubuntu[1:3]

[linux:children]
centos
ubuntu
```

```yaml
# hello_world.yaml
- name: Demo - tasks when
  hosts: linux
  connection: local

  vars:
    msg_centos: "Welcome to CentOS Linux\n"
    msg_ubuntu: "Welcome to Ubuntu Linux\n"

  tasks:
    - name: Configure centos message
      # condition
      when: ansible_distribution == "CentOS"
      copy:
        content: "{{ msg_centos }}"
        dest: ~/message.txt
      notify: message changed

    - name: Configure ubuntu message
      # condition
      when: ansible_distribution == "Ubuntu"
      copy:
        content: "{{ msg_ubuntu }}"
        dest: ~/message.txt
      notify: message changed

  handlers:
    - name: message changed
      debug:
        msg: The message was changed
```

```sh
ansible-playbook -i hosts.ini hello_world.yaml --list-hosts

# playbook: hello_world.yaml

#   play #1 (linux): Demo - tasks when    TAGS: []
#     pattern: ['linux']
#     hosts (6):
#       centos1
#       ubuntu3
#       ubuntu1
#       ubuntu2
#       centos2
#       centos3

ansible-playbook -i hosts.ini hello_world.yaml --syntax-check
# playbook: hello_world.yaml

ansible-playbook -i hosts.ini hello_world.yaml
```

---
