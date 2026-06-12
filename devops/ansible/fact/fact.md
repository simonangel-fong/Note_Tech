# Ansible - Fact

[Back](../ansible.md)

- [Ansible - Fact](#ansible---fact)
  - [Ansible Facts](#ansible-facts)
  - [Lab: Get Fact Data](#lab-get-fact-data)
  - [Custom Facts](#custom-facts)
    - [Lab: Create Custom Facts](#lab-create-custom-facts)

---

## Ansible Facts

- `Ansible Facts`:
  - a type of variable automatically **gathered** from remote managed nodes about **remote system properties and data**
  - gathered by the `setup` module at the **start of every playbook run** and **stored** as variables to make automation dynamic and adaptable.

- **stored** in the `ansible_facts` variable

- Ref:
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html

- gathers facts **before executing tasks**
  - using `setup` module
  - the host to be gathtered controlled by the playbook
    - a playbook for a specific host will gather fact only **from the specific host**, not from all hosts defined in the inventory.

- Control by
  - playbook directive `gather_facts`
    - default: `true`
    - Disabling Facts: `gather_facts: false`
  - Ansible configuration
    - default: `gathering = implicit`, gether facts automatically
    - Disabling: `gathering = explicit`, not gether facts when executing.
      - Can be overriden by playbook setting `gather_facts: true`

---

## Lab: Get Fact Data

```ini
# hosts.ini
[control]
ubuntu-c

[centos]
centos[1:3]

[ubuntu]
ubuntu[1:3]

[linux:children]
centos
ubuntu
```

```yaml
# demo_fact.yaml
- name: Ansible Fact Lab Playbook
  hosts: ubuntu
  tasks:
    - name: Print all facts
      debug:
        msg: "{{ ansible_facts }}"

    - name: Print host facts
      debug:
        msg: "Memory: {{ ansible_memtotal_mb }} MB, Distribution: {{ ansible_distribution }}, Architecture: {{ ansible_architecture }}"
```

```sh
ansible-playbook -i hosts.ini demo_fact.yaml
# PLAY [Ansible Fact Lab Playbook] ****************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu2]
# ok: [ubuntu3]
# ok: [ubuntu1]

# TASK [Print all facts] **************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": {
#         "all_ipv4_addresses": [
#             "172.19.0.6"
#         ],
#         "all_ipv6_addresses": [],
# ...
#     }
# }

# TASK [Print host facts] *************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "Memory: 7789 MB, Distribution: Ubuntu, Architecture: x86_64"
# }
# ok: [ubuntu2] => {
#     "msg": "Memory: 7789 MB, Distribution: Ubuntu, Architecture: x86_64"
# }
# ok: [ubuntu3] => {
#     "msg": "Memory: 7789 MB, Distribution: Ubuntu, Architecture: x86_64"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu1                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

---

## Custom Facts

- By default, Ansible custom facts is placed in `/ect/ansible/facts.d`
  - work around:
    - create dir at `/home/ansible/facts.d`
    - `setup` module with path to this dir
- format:
  - json:

  ```json
  { "date": "Day Mon DD HH:MM:SS TZ YYYY" }
  ```

  - ini:

  ```ini
  [date]
  date=Day Mon DD HH:MM:SS TZ YYYY
  ```

- Query custom fact
  - `ansible all -m setup -a 'filter=ansible_local'`

---

### Lab: Create Custom Facts

```sh
# create default dir
sudo mkdir -p /etc/ansible/facts.d

# create facts json
sudo tee /etc/ansible/facts.d/getdate_json.fact <<EOF
#!/bin/bash
echo {\""date\"" : \""`date`\""}
EOF

# create facts ini
sudo tee /etc/ansible/facts.d/getdate_ini.fact <<EOF
#!/bin/bash
echo [date]
echo date=`date`
EOF

# grant x
sudo chmod 755 /etc/ansible/facts.d/getdate_json.fact
sudo chmod 755 /etc/ansible/facts.d/getdate_ini.fact

# test
sudo /etc/ansible/facts.d/getdate_json.fact
# {"date" : "Fri Jun 12 17:12:18 EDT 2026"}
sudo /etc/ansible/facts.d/getdate_ini.fact
# [date]
# date=Fri Jun 12 17:13:40 EDT 2026

# get custom fact
ansible ubuntu-c -m setup | grep -A2 getdate_json
            # "getdate_json": {
            #     "date": "Fri Jun 12 17:12:18 EDT 2026"
            # }
ansible ubuntu-c -m setup | grep -A3 getdate_ini
            # "getdate_ini": {
            #     "date": {
            #         "date": "Fri Jun 12 17:13:40 EDT 2026"
            #     }

# get all
ansible ubuntu-c -m setup -a 'filter=ansible_local'
# ubuntu-c | SUCCESS => {
#     "ansible_facts": {
#         "ansible_local": {
#             "getdate_ini": {
#                 "date": {
#                     "date": "Fri Jun 12 17:13:40 EDT 2026"
#                 }
#             },
#             "getdate_json": {
#                 "date": "Fri Jun 12 17:12:18 EDT 2026"
#             }
#         },
#         "discovered_interpreter_python": "/usr/bin/python3.10"
#     },
#     "changed": false
# }
```

- used in playbook

```yaml
# demo_custom_fact.yaml
- hosts: ubuntu-c
  tasks:
    - name: get IP
      debug:
        msg: "{{ ansible_default_ipv4.address }}"

    - name: Show Custom Fact getdate_json
      debug:
        msg: "{{ ansible_local.getdate_json.date }}"

    - name: Show Custom Fact getdate_ini
      debug:
        msg: "{{ ansible_local.getdate_ini.date.date }}"

    - name: Get Custom Fact getdate_ini From HostVars
      debug:
        msg: "{{ hostvars[ansible_hostname].ansible_local.getdate_ini.date.date }}"
```

```sh
ansible-playbook demo_custom_fact.yaml

# PLAY [ubuntu-c] *********************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu-c]

# TASK [get IP] ***********************************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "172.19.0.5"
# }

# TASK [Show Custom Fact getdate_json] ************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Fri Jun 12 17:12:18 EDT 2026"
# }

# TASK [Show Custom Fact getdate_ini] *************************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Fri Jun 12 17:13:40 EDT 2026"
# }

# TASK [Get Custom Fact getdate_ini From HostVars] ************************************************************************************
# ok: [ubuntu-c] => {
#     "msg": "Fri Jun 12 17:13:40 EDT 2026"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu-c                   : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
