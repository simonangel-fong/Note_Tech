# DevOps - Ansible

[Back](../../index.md)

---

- [Fundamental](./fundamental/fundamental.md)
  - [Variable](./variable/variable.md)
  - [Facts](./fact/fact.md)
- [Configuration](./config/config.md)
- [Inventory](./inventory/inventory.md)
- [Module](./module/module.md)
- [Playbook](./playbook/playbook.md)
- [Conditional](./conditional/conditional.md)
  - [`command` module](./module/command/command.md)

- [Plugin](./plugin/plugin.md)
- [Role](./role/role.md)
- [Collection](./collection/collection.md)
- [Templating](./templating/templating.md)

---

- [Installation](./install/install.md)

---

- Lab: env

```sh
git clone https://github.com/spurin/diveintoansible-lab.git

docker compose up -d

# open ui localhost:1000
# login: ansible
# pwd: password
docker compose down -v
```

## SSH Connection

- Auto ssh pwd login
  - ansible@ubuntu-c
  - targets
    - host: ubuntu1, ubuntu2, ubuntu3, centos1, centos2, centos3
    - users: ansible,root
  - using sshpass

```sh
ssh ubuntu1
# pwd: password

# key gen
ssh-keygen
# Generating public/private rsa key pair.
# Enter file in which to save the key (/root/.ssh/id_rsa):
# Enter passphrase (empty for no passphrase):
# Enter same passphrase again:
# Your identification has been saved in /root/.ssh/id_rsa
# Your public key has been saved in /root/.ssh/id_rsa.pub
# The key fingerprint is:
# SHA256:ROy4EcK+B4Imn5Vs9pUqCqhIWkEvzhgBRX5Kal/kmLE root@ubuntu-c
# The key's randomart image is:
# +---[RSA 3072]----+
# |ooo.   ..        |
# |... o ...        |
# | +o=.+ +..       |
# |+++o^ o.+        |
# |=B.E * =S        |
# |=.B + =          |
# |=o o o           |
# |+ .              |
# |                 |
# +----[SHA256]-----+

ls -l
# id_rsa: private key
# id_rsa.pub: public key

ssh-copy-id ansible@ubuntu1

# test: login without pwd
ssh ansible@ubuntu1

# install sshpass
sudo apt update

sudo apt install sshpass -y

# create pwd txt
echo password > password.txt

# loop user
for user in ansible root
do
  # loop os
  for os in ubuntu centos
  do
    for instance in 1 2 3
    do
      sshpass -f password.txt ssh-copy-id -o StrictHostKeyChecking=no ${user}@${os}${instance}
    done
  done
done

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'ansible@ubuntu1'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'ansible@ubuntu2'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'ansible@ubuntu3'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'ansible@centos1'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'ansible@centos2'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'ansible@centos3'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'root@ubuntu1'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'root@ubuntu2'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'root@ubuntu3'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'root@centos1'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'root@centos2'"
# and check to make sure that only the key(s) you wanted were added.

# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh -o 'StrictHostKeyChecking=no' 'root@centos3'"
# and check to make sure that only the key(s) you wanted were added.

# test connectivity
ansible -i ubuntu1,ubuntu2,ubuntu3,centos1,centos2,centos3 all -m ping
# ubuntu3 | SUCCESS => {
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
# ubuntu2 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.10"
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
# centos3 | SUCCESS => {
#     "ansible_facts": {
#         "discovered_interpreter_python": "/usr/bin/python3.9"
#     },
#     "changed": false,
#     "ping": "pong"
# }

rm password.txt
rm .ssh/known_hosts
```

## Couse codes

- Clone to ubuntu-c

```sh
git clone https://github.com/spurin/diveintoansible.git
```

---

