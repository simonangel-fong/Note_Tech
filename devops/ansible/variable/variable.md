# Ansible - Variable

[Back](../ansible.md)

- [Ansible - Variable](#ansible---variable)
  - [Variable](#variable)
    - [Syntax](#syntax)
    - [Variable Types](#variable-types)
    - [Variable Scope](#variable-scope)
    - [Variable Precedence](#variable-precedence)
  - [Define Variable](#define-variable)
    - [Lab: Variables with `vars` keyword](#lab-variables-with-vars-keyword)
    - [Lab: Variables with `vars_files` keyword](#lab-variables-with-vars_files-keyword)
    - [Lab: Variables with `vars-prompt` keyword](#lab-variables-with-vars-prompt-keyword)
  - [Register: Output a varialbe](#register-output-a-varialbe)
  - [`host_vars` and `group_vars` Directory](#host_vars-and-group_vars-directory)
  - [Magic variable](#magic-variable)
    - [`hostvars`](#hostvars)
    - [`groups`](#groups)

---

## Variable

- `Variable`
  - store information of the hosts
  - Can be defined in
    - playbook file
    - a separated file
    - command `-e`

### Syntax

```yaml
# define
vars:
  var_name: var_values

# reference var
line: "nameserver {{ var_name }}" # use Jinja2 Templating format
```

---

### Variable Types

- String
- Number
  - can be integer or floating-piont
- Boolean
  - Truthly values: `True 'true', 't', 'yes', 'y', 'on', '1', 1, 1.0`
  - Falsy values: `False 'false', 'f', 'no', 'n', 'off', '0', 0, 0.0`
- List
  - **ordered** collection of value
  - can be any type
- Dictionary
  - key-value pairs
  - keys and values can be of any type
  - referencing value: ie.,`user.name`

---

### Variable Scope

- Scope level:
  - Host, defined within a host.
    - ie., dns_server for a host.
  - Play, defined within a play.
    - ie., ntp_server a play, cannot be accessible in another play.
  - Global, defined in configuration file, env var, cli extra-vars.
    - ie., `ansible-playbook playbook.yml --extra-vars "ntp_server=10.0.0.1"`

---

### Variable Precedence

- When same variable is defined in multiple places

- **Precedence:**(highest at the bottom)
  - Role Defaults
  - Group Vars
  - Host Vars
  - Host Facts
  - Play Vars
  - Role Vars
  - Include Vars
  - Set Facts
  - Extra Vars

- ref:
  - https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html#variables

---

- Example:
  - dns_server are defined for both group level and host level

```ini
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101 dns_server=10.5.5.4 # define for this host
web3 ansible_host=172.20.1.102

[web_servers]
web1
Web2
web3

[web_servers:vars]
dns_server=10.5.5.3 # variable defined for groups to be applied for each host
```

> dns_server of web1 and web2: 10.5.5.3
> dns_server of web2: 10.5.5.4

---

- Example:
  - a dns_server defined in the playbook

```yaml
- name: Configure DNS server
  hosts: all
  vars:
    dns_server: 10.5.5.5 # play level
  task:
    - nsupdate:
      server: "{{ dns_server }}"
```

> dns_server of all web host: 10.5.5.5

---

- Exmaple:
  - pass value using `--extra-vars`

```sh
ansible-playbook playbook.yml --extra-vars "dns_server=10.5.5.6"
```

> all hosts included in this playbook: 10.5.5.6

---

## Define Variable

- `vars`: define within the playbook
- `vars_files`: define from yaml file
- `vars_prompt`: define from user prompt
- `ansible-playbook -e`: define from command
  - key-value pair: `ansible-playbook -e var_key="var_value"`
  - yaml dict: `ansible-playbook -e {var_key: var_value}`
  - json dict: `ansible-playbook -e {"var_key": "var_value"}`
- `ansible-playbook -e @yaml_file`: define from command sourced from a file
  - key-value pair file: `var_key="var_value"`
  - yaml file: `var_key: var_value`
  - json file: `{"var_key": "var_value"}`

---

### Lab: Variables with `vars` keyword

```yaml
# demo_
- name: demo variable
  hosts: ubuntu
  vars:
    message: "A demo message"
  tasks:
    - name: disploy message
      debug:
        msg: "{{ message }}"
```

```sh
ansible-playbook demo.yaml
# PLAY [demo variable] *****************************************************************************************************************

# TASK [Gathering Facts] ***************************************************************************************************************
# ok: [ubuntu3]
# ok: [ubuntu2]
# ok: [ubuntu1]

# TASK [disploy message] ***************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "A demo message"
# }
# ok: [ubuntu2] => {
#     "msg": "A demo message"
# }
# ok: [ubuntu3] => {
#     "msg": "A demo message"
# }

# PLAY RECAP ***************************************************************************************************************************
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### Lab: Variables with `vars_files` keyword

```yaml
# e_vars.yaml
var_empty_dict: {}
var_str: this is a string
var_int: 2
var_dict:
  dict_key: dict value
  dict_key_null:
  dict_key_empty: {}
var_list:
  - itm1
  - itm2
  - itm3
```

```yaml
# demo.yaml
- hosts: ubuntu
  gather_facts: False
  vars_files:
    - e_vars.yaml
  tasks:
    - name: Test empty dict
      debug:
        msg: "{{ var_empty_dict }}"

    - name: Test string value
      debug:
        msg: "{{ var_str }}"

    - name: Test integer value
      debug:
        msg: "{{ var_int }}"

    - name: Test dictionary key
      debug:
        msg: "{{ var_dict['dict_key'] }}"

    - name: Test dictionary empty key
      debug:
        msg: "{{ var_dict['dict_key_empty'] }}"

    - name: Test dictionary null key
      debug:
        msg: "{{ var_dict['dict_key_null'] }}"

    - name: Test list
      debug:
        msg: "{{ var_list }}"

    - name: Test list item
      debug:
        msg: "{{ var_list[1] }}"
```

```sh
ansible-playbook demo.yaml --syntax-check
ansible-playbook demo.yaml --list-hosts
# playbook: demo.yaml
#   play #1 (ubuntu): ubuntu      TAGS: []
#     pattern: ['ubuntu']
#     hosts (3):
#       ubuntu1
#       ubuntu2
#       ubuntu3

ansible-playbook demo.yaml
# PLAY [ubuntu] ************************************************************************************************************************

# TASK [Test empty dict] ***************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": {}
# }
# ok: [ubuntu2] => {
#     "msg": {}
# }
# ok: [ubuntu3] => {
#     "msg": {}
# }

# TASK [Test string value] *************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "this is a string"
# }
# ok: [ubuntu2] => {
#     "msg": "this is a string"
# }
# ok: [ubuntu3] => {
#     "msg": "this is a string"
# }

# TASK [Test integer value] ************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": 2
# }
# ok: [ubuntu2] => {
#     "msg": 2
# }
# ok: [ubuntu3] => {
#     "msg": 2
# }

# TASK [Test dictionary key] ***********************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "dict value"
# }
# ok: [ubuntu2] => {
#     "msg": "dict value"
# }
# ok: [ubuntu3] => {
#     "msg": "dict value"
# }

# TASK [Test dictionary empty key] *****************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": {}
# }
# ok: [ubuntu2] => {
#     "msg": {}
# }
# ok: [ubuntu3] => {
#     "msg": {}
# }

# TASK [Test dictionary null key] ******************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": ""
# }
# ok: [ubuntu2] => {
#     "msg": ""
# }
# ok: [ubuntu3] => {
#     "msg": ""
# }

# TASK [Test list] *********************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": [
#         "itm1",
#         "itm2",
#         "itm3"
#     ]
# }
# ok: [ubuntu2] => {
#     "msg": [
#         "itm1",
#         "itm2",
#         "itm3"
#     ]
# }
# ok: [ubuntu3] => {
#     "msg": [
#         "itm1",
#         "itm2",
#         "itm3"
#     ]
# }

# TASK [Test list item] ****************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "itm2"
# }
# ok: [ubuntu2] => {
#     "msg": "itm2"
# }
# ok: [ubuntu3] => {
#     "msg": "itm2"
# }

# PLAY RECAP ***************************************************************************************************************************
# ubuntu1                    : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### Lab: Variables with `vars-prompt` keyword

```yaml
# demo_vars_prompt.yaml
- hosts: ubuntu
  gather_facts: False
  vars_prompt:
    - name: username
      private: False

  tasks:
    - name: Test empty dict
      debug:
        msg: "{{ username }}"
```

```sh
ansible-playbook demo_vars_prompt.yaml
# username: abc

# PLAY [ubuntu] ************************************************************************************************************************

# TASK [Test empty dict] ***************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "abc"
# }
# ok: [ubuntu2] => {
#     "msg": "abc"
# }
# ok: [ubuntu3] => {
#     "msg": "abc"
# }

# PLAY RECAP ***************************************************************************************************************************
# ubuntu1                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

# with -e
ansible-playbook demo_vars_prompt.yaml -e 'username="XYZ"'
# PLAY [ubuntu] ************************************************************************************************************************

# TASK [Test empty dict] ***************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "XYZ"
# }
# ok: [ubuntu2] => {
#     "msg": "XYZ"
# }
# ok: [ubuntu3] => {
#     "msg": "XYZ"
# }

# PLAY RECAP ***************************************************************************************************************************
# ubuntu1                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- Private Prompt

```yaml
# demo_vars_prompt_private.yaml
- hosts: ubuntu
  gather_facts: False
  vars_prompt:
    - name: username
      private: True

  tasks:
    - name: Test empty dict
      debug:
        msg: "{{ username }}"
```

```sh
ansible-playbook demo_vars_prompt_private.yaml
# username:

# PLAY [ubuntu] ************************************************************************************************************************

# TASK [Test empty dict] ***************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "qazxsw"
# }
# ok: [ubuntu2] => {
#     "msg": "qazxsw"
# }
# ok: [ubuntu3] => {
#     "msg": "qazxsw"
# }

# PLAY RECAP ***************************************************************************************************************************
# ubuntu1                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

## Register: Output a varialbe

- Output a variable, using `register: var_name`

```yaml
- name: check /etc/hosts file
  hosts: all
  tasks:
    - shell: cat /etc/hosts
      register: result # capture the output in var result
    - debug:
        var: result # assign the result to var, this print all message
        # var: result.stdout # print only the stdout message
```

- option: using option `-v`
  - `ansible-playbook -i inventory playbook.yml -v`

---

## `host_vars` and `group_vars` Directory

- `host_vars`:
  - a **dedicated directory** used to store variable files that apply exclusively to **individual, specific hosts**.
- `group_vars`:
  - a **dedicated directory** used to store variable files that apply exclusively to **groups of hosts**.

- Ansible automatically looks for a directory named `host_vars` and group_vars in two locations:
  - adjacent to the inventory file
  - adjacent to the playbook file.

- Key Behavioral Rules
  - **File Naming**:
    - The file extension can be `.yml`, `.yaml`, or omitted entirely.
    - The filename before the extension **must perfectly match the inventory name**
      - e.g., webserver1 == webserver1.yml
  - **Variable Precedence**:
    - Variables declared inside `host_vars` will automatically **override** identical variables defined inside `group_vars` (such as group_vars/all.yml).
    - However, they will be **overridden** by variables declared directly **inside the playbook** (`vars`: blocks) or via the command line (`-e`).
  - **Complex Data Structures**:
    - `host_vars` files allow to easily define multi-line strings, arrays, nested hashes, and Ansible Vault encrypted secrets.

- Standard Directory Structure

```txt
├── inventory/
│   ├── hosts.ini            # Your inventory list
│   ├── group_vars/
│   │   ├── all.yml          # Variables applied to EVERY host
│   │   ├── webservers.yml   # Variables applied to [webservers] group
│   │   └── databases.yml    # Variables applied to [databases] group
│   └── host_vars/
│       ├── web01.yml        # Variables applied ONLY to host 'web01'
│       └── db01.yaml        # Variables applied ONLY to host 'db01'
├── site.yml                 # Your playbook file
└── ansible.cfg              # Ansible configuration
```

---

## Magic variable

- Ansible `magic variables`
  - a set of **predefined, immutable variables** automatically provided by Ansible **during playbook execution**.
  - offer **insights** into the **current state** of the Ansible environment, the hosts involved, and the execution context.

### `hostvars`

- `hostvars`:
  - used to access variables and facts belonging to other hosts in your inventory.

```yml
- name: Print dns server
  hosts: all
  task:
    - debug:
        msg: "{{ hostvars['web2'].dns_server }}"
```

- Common Parameters of magic variable `hostvars`

| Parameter                                          | Desc                                  |
| -------------------------------------------------- | ------------------------------------- |
| `hostvars['host_name'].ansible_host`               | Get the hostname/IP of a host         |
| `hostvars['host_name'].ansible_facts.architecture` | Get the architecture of a host's fact |
| `hostvars['host_name'].ansible_facts.devices`      | Get the devices of a host's fact      |
| `hostvars['host_name'].ansible_facts.mounts`       | Get the mounts of a host's fact       |
| `hostvars['host_name'].ansible_facts.processor`    | Get the processor of a host's fact    |

---

### `groups`

- `groups`
  - an ansible magic variable that contains a dictionary mapping all inventory group names to the lists of hostnames belonging to each group.

| Magic variable         | Desc                                               |
| ---------------------- | -------------------------------------------------- |
| `groups['group_name']` | Get all hosts under a given group                  |
| `group_names`          | Get the group name of current host                 |
| `inventory_hostname`   | Get the name in the inventory for the current host |

---
