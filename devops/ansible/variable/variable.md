# Ansible - Variable

[Back](../ansible.md)

- [Ansible - Variable](#ansible---variable)
  - [Variable](#variable)
    - [Variable Types](#variable-types)
  - [Variable Precedence](#variable-precedence)
  - [Register: Output a varialbe](#register-output-a-varialbe)
  - [Variable Scope](#variable-scope)
  - [Magic variable](#magic-variable)
    - [Magic variable - `hostvars`](#magic-variable---hostvars)
    - [Magic variable - `groups`](#magic-variable---groups)
  - [Ansible Fact](#ansible-fact)
  - [Lab: Get Fact Data](#lab-get-fact-data)

---

## Variable

- `Variable`

  - store information of the hosts

- Can be defined in

  - the playbook file
  - the a separated file

- Sematic

```yaml
# define
vars:
  var_name: var_values

# reference var
line: "nameserver {{ var_name }}" # use Jinja2 Templating format
```

- Example

```yaml
# define in variable file
http_port: 8081
snmp_port: 161-162
inter_ip_range: 192.0.2.0

# playbook file
name: Set firewall configuration
hosts: web
task:
  - firewalld:
      service: https
      permanent: true
      state: enabled
  - firewalld:
      port: "{{ http_port }}"/tcp
      permanent: true
      state: disabled
  - firewalld:
      port: "{{ snmp_port }}"/tcp
      permanent: true
      state: disabled
  - firewalld:
      source: "{{ inter_ip_range }}"/tcp
      permanent: internal
      state: enabled

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

## Variable Precedence

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

## Variable Scope

- Scope level:
  - Host, defined within a host.
    - ie., dns_server for a host.
  - Play, defined within a play.
    - ie., ntp_server a play, cannot be accessible in another play.
  - Global, defined in configuration file, env var, cli extra-vars.
    - ie., `ansible-playbook playbook.yml --extra-vars "ntp_server=10.0.0.1"`

---

## Magic variable

- Ansible `magic variables`
  - a set of **predefined, immutable variables** automatically provided by Ansible **during playbook execution**.
  - offer **insights** into the **current state** of the Ansible environment, the hosts involved, and the execution context.

### Magic variable - `hostvars`

- Ansible process explanation

- for the following inventroy

```ini
# /etc/ansible/hosts
web1 ansible_host=172.20.1.100
web2 ansible_host=172.20.1.101 dns_server=10.5.5.4
web3 ansible_host=172.20.1.102
```

- Subprocesses:
  - When executing, Ansible will create 3 subprocesses for web1, web2, and web3.
- Variable Interpolation:
  - Within each subprocess, variable will be created
  - web1: inventory_hostname=web1, ansible_host=172.20.1.100
  - web2: inventory_hostname=web2, ansible_host=172.20.1.101 dns_server=10.5.5.4
  - web3: inventory_hostname=web3, ansible_host=172.20.1.102
- As a result, the host varialbes dns_server are not available for others, because it exists only within the subprocess web2.

- The magic variable `hostvars` can be used to share variable only in subprocess web2.

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

### Magic variable - `groups`

| Magic variable         | Desc                                               |
| ---------------------- | -------------------------------------------------- |
| `groups['group_name']` | Get all hosts under a given group                  |
| `group_names`          | Get the group name of current host                 |
| `inventory_hostname`   | Get the name in the inventory for the current host |

---

## Ansible Fact

- `Ansible facts`

  - a type of variable automatically **gathered** by Ansible **about the remote systems (managed hosts)** during the **execution** of a playbook or ad-hoc command.
  - **provide detailed information** about the system's **state** and **configuration**, which can then be used in playbooks for conditional logic, task execution, or templating.

- Ref:

  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html

- gathers facts **before executing tasks**
  - using `setup` module
  - the host to be gathtered controlled by the playbook
    - a playbook for a specific host will gather fact only from the specific host, not from all hosts defined in the inventory.
- Control by
  - playbook directive `gather_facts`
    - default: `true`
    - Disabling Facts: `gather_facts: false`
  - Ansible configuration
    - default: `gathering = implicit`, gether facts automatically
    - Disabling: `gathering = explicit`, not gether facts when executing.
      - Can be overriden by playbook setting `gather_facts: true`
- Facts are **stored** in the `ansible_facts` variable

---

## Lab: Get Fact Data

```sh
# inventory.yml
tee > "inventory.yaml" <<EOF
all:
  hosts:
    server1:
      ansible_host: 192.168.100.107
      ansible_user: ubuntuadmin
EOF

ansible -i inventory.yaml all -m ping

tee >get_fact_variable.yaml << EOF
- name: Ansible Fact Lab Playbook
  hosts: all
  tasks:
    - name: Print all facts
      debug:
        msg: "{{ ansible_facts }}"

    - name: Print host facts
      debug:
        msg: "Memory: {{ ansible_memtotal_mb }} MB, Distribution: {{ ansible_distribution }}, Architecture: {{ ansible_architecture }}"
EOF

ansible-playbook -i inventory.yaml get_fact_variable.yaml
# TASK [Print host facts] **************************************************************************
# ok: [server1] => {
#     "msg": "Memory: 7892 MB, Distribution: Ubuntu, Architecture: x86_64"
# }
```
