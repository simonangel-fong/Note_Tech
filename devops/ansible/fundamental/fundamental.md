# Ansible - Fundamental

[Back](../ansible.md)

- [Ansible - Fundamental](#ansible---fundamental)
  - [Ansible](#ansible)
    - [Ansbile parameters](#ansbile-parameters)
    - [Configuration Files](#configuration-files)
    - [Override Default Configuration](#override-default-configuration)
      - [`[defaults]`](#defaults)
    - [Common Command](#common-command)

---

## Ansible

### Ansbile parameters

- The parameter used to define how Ansible runs playbooks
- Naming:
  - `ANSIBLE_<PARAMETER_NAME>`: All upper case.

---

### Configuration Files

- `Ansible configuration file`

  - defines how Ansible should behave when running playbooks, ad-hoc commands, or roles.

- By default, cf path:

  - `/etc/ansible/ansible.cfg`

- By default, Ansible looks for configuration files in this **order** (first found is used):

  - `ANSIBLE_CONFIG` (environment variable if set)
  - `./ansible.cfg` (in the current directory)
  - `~/.ansible.cfg` (in the user’s home directory)
  - `/etc/ansible/ansible.cfg` (system-wide default)

- If Ansible finds the above configuration, then the values defined in cf will be applied and the parameters that are not defined will be apply defautl values.

- Common Sections in cf
  - defaults
  - inventory
  - privilege_escalation
  - paramiko_connection
  - ssh_connection
  - persistent_connection
  - colors

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

#### `[defaults]`

- Defines global defaults for Ansible.

- Common Entries:

| Entry               | Desc                                |
| ------------------- | ----------------------------------- |
| `inventory`         | path to the default inventory file. |
| `remote_user`       | default SSH user.                   |
| `roles_path`        | path to roles.                      |
| `host_key_checking` | whether to check SSH host keys.     |
| `forks`             | number of parallel processes.       |

---

### Common Command

| CMD                                     | DESC                                                   |
| --------------------------------------- | ------------------------------------------------------ |
| `ansible-config list`                   | List all configuration                                 |
| `ansible-config view`                   | Show the currently active config file                  |
| `ansible-config dump`                   | Show the current settings and where they are picked up |
| `ansible-config dump \| grep GATHERING` | Show the a specific paramter settings                  |
