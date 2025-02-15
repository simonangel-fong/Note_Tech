# RHCSA User and Group

[Back](../../index.md)

- [RHCSA User and Group](#rhcsa-user-and-group)
  - [Question](#question)
    - [Solution](#solution)
  - [Question: user uid](#question-user-uid)
  - [Solution](#solution-1)
  - [Question: welcome message](#question-welcome-message)
    - [Solution](#solution-2)

---

## Question

```conf
Create the following users, groups, and group membership:

A group named sysadm.
A user "harry" who belongs to sysadm as a secondary group.
A user "natasha" who belongs to sysadm as a secondary group.
A user "sarah" who does not have access to an interactive shell & who is not a member of sysadm group.
"harry", "natasha", and "sarah" should all have the password of password.
"sysadm" group has access to add user in the server
"harry" user has access to set password for users without asking sudo password

More:
Grant harry full access
Grant harry full access without passowrd
```

---

### Solution

- Create user and group

```sh
# create group
groupadd sysadm

# confirm
tail -1 /etc/group
# sysadm:x:1001:

# create users and pwd
useradd -G sysadm harry
useradd -G sysadm natasha
useradd -s /sbin/nologin sarah

echo "password" | passwd --stdin harry
echo "password" | passwd --stdin natasha
echo "password" | passwd --stdin sarah

# confirm group member
id harry
id natasha
id sarah

# confirm shell
grep sarah /etc/passwd
# confirm pwd
tail -3 /etc/shadow
```

- Grant permission

```sh
# get the path of command
which useradd
which passwd

visudo
# add entry
# %sysadm ALL=/usr/sbin/useradd
# harry ALL=(ALL) NOPASSWD: /usr/bin/passwd, !/usr/bin/passwd root


# switch to harry to test passwd
su - harry
# confirm
passwd natasha

# switch to natasha to test useradd
su - natasha
sudo useradd newuser
```

- More

```sh
visudo
# full access
# harry ALL=(ALL) ALL

# confirm
su - harry
# sudo whoami
# with pwd

visudo
# full access without pwd
# harry ALL=(ALL) NOPASSWD: ALL

# confirm
su - harry
# sudo whoami
# without pwd


```

---

## Question: user uid

```conf
Create a user "unilao" with UID "2334" with password as "ablerate".
```
---

## Solution

```sh
# create user
useradd -u 2334 unilao
# pwd
echo "unilao:ablerate" | sudo chpasswd

# confirm
id unilao
```

---

## Question: welcome message

```conf
Build an application rhcsa that print the message when logged in as ablerate user
"Welcome to user ablerate "
```
---

- Confiregure: create user "ablerate"

```sh
useradd ablerate
passwd ablerate
```

---

### Solution

```sh
su - ablerate

# Create a shell script
vi ~/rhcsa

#!/bin/bash
echo "Welcome to user ablerate"

# Set execute permissions
chmod +x ~/rhcsa

# Modify the .bashrc File
vi ~/.bashrc

# add a line
~/rhcsa

# logout and login
exit
su - ablerate
# Welcome to user ablerate
```

- Troubleshooting

```sh
# If it show "permission denied" when logging in, change mod
chmod +x ~/rhcsa
```