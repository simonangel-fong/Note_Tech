# Ansible - Installation

[Back](../ansible.md)

- [Ansible - Installation](#ansible---installation)
  - [Architecture](#architecture)
  - [Initialize](#initialize)
    - [Installation on Control node](#installation-on-control-node)
    - [Create connection](#create-connection)
    - [Create Playbook](#create-playbook)

---

## Architecture

- Control Node: 192.168.100.108
  - target node: 192.168.100.107

---

## Initialize

- Control Node:

```sh
sudo hostnamectl set-hostname control-node

sudo vi /etc/hosts
# 127.0.0.1 localhost control-node
```

- Target Node:

```sh
sudo hostnamectl set-hostname target-node

sudo vi /etc/hosts
# 127.0.0.1 localhost target-node
```

### Installation on Control node

```sh
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

# confirm
ansible --version
```

---

### Create connection

- Control node

```sh
ssh-keygen
ssh-copy-id ubuntuadmin@192.168.100.107

# test
ssh ubuntuadmin@192.168.100.107
```

---

### Create Playbook

ansible_ssh_private_key_file=~/.ssh/id_rsa

```sh
cat > ./inventory.ini<<EOF
[target_nodes]
192.168.100.107 ansible_user=ubuntuadmin ansible_become=yes ansible_become_method=sudo ansible_become_password=Welcome!234 ansible_ssh_pass=Welcome!234

[target_nodes:vars]
ansible_become=yes
ansible_become_method=sudo
EOF

# Test the connection
ansible -i inventory.ini target_nodes -m ping
# 192.168.100.107 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.12"
#     },
#     "changed": false,
#     "ping": "pong"
# }

# Create Playbook
cat >./playbook_install_nginx.yml<<EOF
---
- name: Update packages on all nodes
  hosts: target_nodes
  become: yes
  tasks:
    - name: Update all packages
      ansible.builtin.apt:
        name: "*"
        state: latest
        update_cache: yes
- name: Update system and install Nginx
  hosts: target_nodes
  become: yes  # run tasks with sudo
  tasks:
    - name: Update all packages
      ansible.builtin.apt:
        update_cache: yes

    - name: Install Nginx package
      ansible.builtin.apt:
        name: nginx
        state: present # Ensures the package is installed

    - name: Ensure Nginx is running and enabled
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: yes
EOF

# Run the Playbook
ansible-playbook -i inventory.ini playbook_install_nginx.yml
# TASK [Update all packages] *******************************************************
# ok: [192.168.100.107]

# PLAY [Update system and install Nginx] *******************************************

# TASK [Gathering Facts] ***********************************************************
# ok: [192.168.100.107]

# TASK [Update all packages] *******************************************************
# changed: [192.168.100.107]

# TASK [Install Nginx package] *****************************************************
# ok: [192.168.100.107]

# TASK [Ensure Nginx is running and enabled] ***************************************
# ok: [192.168.100.107]

# PLAY RECAP ***********************************************************************
# 192.168.100.107            : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```
