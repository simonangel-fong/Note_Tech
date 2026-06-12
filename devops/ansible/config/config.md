# Ansible - Configuration File

[Back](../ansible.md)

- [Ansible - Configuration File](#ansible---configuration-file)
  - [Configuration File](#configuration-file)
    - [Common Commands](#common-commands)
    - [Lab: Set Configuration File](#lab-set-configuration-file)
    - [Override Default Configuration](#override-default-configuration)

---

## Configuration File

- `Ansible configuration file`
  - defines how Ansible should behave when running playbooks, ad-hoc commands, or roles.

- By default, Ansible looks for configuration files in this **order** (first found is used):
  - `ANSIBLE_CONFIG`
    - an **environment variable** used to define the **absolute path** to the specific Ansible configuration file
  - `./ansible.cfg`
    - local configuration file in a project directory
  - `~/.ansible.cfg`:
    - user-level configuration file in the user’s home directory
  - `/etc/ansible/ansible.cfg`
    - global configuration file that defines default system-wide settings

- If Ansible finds the above configuration, then
  - the **values** defined in cf will be **applied**
  - the parameters that are **not defined** will be apply **defautl values**.

- Common Entries:

| Entry               | Desc                                |
| ------------------- | ----------------------------------- |
| `inventory`         | path to the default inventory file. |
| `remote_user`       | default SSH user.                   |
| `roles_path`        | path to roles.                      |
| `host_key_checking` | whether to check SSH host keys.     |
| `forks`             | number of parallel processes.       |

---

### Common Commands

| CMD                                          | DESC                                                                      |
| -------------------------------------------- | ------------------------------------------------------------------------- |
| `ansible-config --version`                   | Show Ansible version and config-related path information.                 |
| `ansible-config list`                        | List all available Ansible configuration options.                         |
| `ansible-config view`                        | Display the current `ansible.cfg` file content.                           |
| `ansible-config view --config ./ansible.cfg` | Display a specific config file.                                           |
| `ansible-config dump`                        | Show current Ansible configuration values.                                |
| `ansible-config dump --only-changed`         | Show only configuration values that are different from the default.       |
| `ansible-config dump -c ./ansible.cfg`       | Dump configuration using a specific config file.                          |
| `ansible-config dump -v`                     | Show verbose output while dumping config.                                 |
| `ansible-config dump -vvv`                   | Show very detailed debug output. Useful when config loading is confusing. |

- create

| CMD                                            | DESC                                                             |
| ---------------------------------------------- | ---------------------------------------------------------------- |
| `ansible-config init --disabled`               | Generate a sample `ansible.cfg` with most options commented out. |
| `ansible-config init --disabled > ansible.cfg` | Create a starter `ansible.cfg` file in the current directory.    |
| `ansible-config init --disabled -t all`        | Generate sample config for all plugin types.                     |

---

### Lab: Set Configuration File

```sh
ansible --version
# ansible [core 2.17.4]
#   config file = None

# create global configuration
touch /etc/ansible/ansible.cfg
ansible --version
# ansible [core 2.17.4]
#   config file = /etc/ansible/ansible.cfg


# create ~/.ansible.cfg
touch ~/.ansible.cfg
ansible --version
# ansible [core 2.17.4]
#   config file = /root/.ansible.cfg

# create local configuration file
mkdir project
cd project
touch ansible.cfg
ansible --version
# ansible [core 2.17.4]
#   config file = /root/project/ansible.cfg

# create env
touch /tmp/ansible.cfg
export ANSIBLE_CONFIG=/tmp/ansible.cfg
ansible --version
# ansible [core 2.17.4]
#   config file = /tmp/ansible.cfg


# clean up
rm /etc/ansible/ansible.cfg
rm /root/.ansible.cfg
rm -rf /root/project
rm /tmp/ansible.cfg
unset ANSIBLE_CONFIG

# confirm
ansible --version
# ansible [core 2.17.4]
#   config file = None
```

---

### Override Default Configuration

- Ways to override the default configuration:

- Perssit parameters across shells ans uses
  - Create custom cf `ansible.cfg` within the directory of specific playbook.

- Execute a playbook using a cf rathen in the default path

```sh
ANSIBLE_CONFIG=/opt/ansible-web.cfg ansible-playbook web-playbook.yml
```

- to override a specific paramters **for a single execution**:

```sh
ANSIBLE_PARAMETER_NAME=new_value ansible-playbook playbook.yml
```

- Persist the **throughout the shell session**:

```sh
export ANSIBLE_PARAMETER_NAME=new_value
ansible-playbook playbook.yml
```

---
