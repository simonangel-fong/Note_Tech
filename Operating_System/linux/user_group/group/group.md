# Linux - User Management: Group

[Back](../../index.md)

---

- [Linux - User Management: Group](#linux---user-management-group)
  - [Group](#group)
  - [Group Configuration Files](#group-configuration-files)
    - [`/etc/group`](#etcgroup)
    - [`/etc/gshadow`](#etcgshadow)
  - [Group Management](#group-management)
    - [Adding a new group](#adding-a-new-group)
    - [Lab: create group](#lab-create-group)
    - [Changing a new group](#changing-a-new-group)
    - [Lab: Update and delete group](#lab-update-and-delete-group)
    - [Group Administration](#group-administration)
    - [Deleting a new group](#deleting-a-new-group)
    - [Display Group Info](#display-group-info)

---

## Group

- `Group`
  - a **collection of users** that **share permissions** to access files, directories, or other system resources.
- `Groups` are a fundamental **part** of Linux’s **permission model**, helping manage access efficiently.
- Every `user` is in **at least one** `group` - `Primary Group`

- `Primary Group`

  - the **default group** associated with a user account.
  - When a user **creates** a file, its **group ownership** is set to the **user’s primary group**.
  - Specified during user **creation** or **modified** using the `usermod` command.

- `Secondary Groups`

  - A user can belong to **multiple** secondary groups in addition to their primary group.
  - **grant additional access** to shared resources.

- `Group ID (GID)`

  - Each group is identified by a **unique numeric** `Group ID (GID)`.
  - GIDs **below** `1000` are **reserved for** `system groups`.

---

## Group Configuration Files

### `/etc/group`

- Lists all groups, their members, and group-related information.

```conf
group_name:x:group_id:member1,member2
```

- file permission:

```conf
-rw-r--r--. 1 root root 1054 Nov 19 16:37 /etc/group
```

---

### `/etc/gshadow`

- Contains secure group **passwords** and administrative information.
- If a group has a password, it is stored here in an encrypted format.

```conf
group_name:encrypted_password:group_admins:group_members
```

- `group_name`
  - The **name** of the group (must match the group in /etc/group).
- `encrypted_password`
  - The group **password** in **encrypted form** (if set).
  - `!` or `*`:
    - Indicates that the group **cannot** be accessed **with a password**.
  - `Empty field` (`::`):
    - Group does **not require a password**.
- `group_admins`
  - A comma-separated list of **users who can manage** the group (add or remove members).
  - If empty, no specific administrators are assigned.
- `group_members`

  - A comma-separated list of users who belong to the group (same as /etc/group).

- file permission:

```conf
----------. 1 root root 850 Nov 19 16:37 /etc/gshadow
```

---

| Command            | Desc                                   |
| ------------------ | -------------------------------------- |
| `groups`           | show the groups the current user is in |
| `id -Gn`           | show the groups the current user is in |
| `groups user_name` | show the groups a specific user is in  |
| `id user_name -Gn` | show the groups a specific user is in  |

---

## Group Management

### Adding a new group

| CMD                         | DESC                                           |
| --------------------------- | ---------------------------------------------- |
| `groupadd g_name`           | create a new group                             |
| `groupadd g_name -g GID`    | create a new group and specify a gid           |
| `groupadd g_name -g GID -o` | create a new group and specify a duplicate gid |
| `groupadd g_name -r`        | create a system group below 1000               |

- updates `/etc/group`

---

### Lab: create group

```sh
su -
groupadd -g 5000 linuxadmin
groupadd -o -g 5000 dba

# confirm
tail -2 /etc/group
# linuxadmin:x:5000:
# dba:x:5000:

# add user
usermod -aG dba user100

# confirm
id user100
# uid=1003(user100) gid=1003(user100) groups=1003(user100),5000(linuxadmin)

groups user100
# user100 : user100 linuxadmin

grep dba /etc/group
# dba:x:5000:user100
```

---

### Changing a new group

| CMD                           | DESC                                    |
| ----------------------------- | --------------------------------------- |
| `groupmod g_name -n new_name` | Modify group's name                     |
| `groupmod g_name -g GID`      | Modify group's GID                      |
| `groupmod g_name -g GID -o`   | Modify group's GID with a duplicate gid |

- updates `/etc/group`

- Example

```sh
# Create a new user
useradd testuser

# Create a New Group
groupadd testgroup

# Change a User's Primary Group
usermod testuser -g testgroup

# Add a User to a Group
usermod testuser -aG testgroup,wheel
```

---

### Lab: Update and delete group

```sh
groupmod -n sysadm linuxadmin
groupmod -g 6000 sysadm

# confirm
grep sysadm /etc/group
# sysadm:x:6000:

# remove group
groupdel sysadm
grep sysadm /etc/group
```

---

### Group Administration

| CMD                                 | DESC                            |
| ----------------------------------- | ------------------------------- |
| `gpasswd group_name`                | Set or Change a Group Password  |
| `gpasswd group_name -r`             | Remove a Group Password         |
| `gpasswd group_name -A admin_user`  | Add a Group Administrator       |
| `gpasswd group_name -a username`    | Add a Member to a Group         |
| `gpasswd group_name -M user1,user2` | Add a list of member to a Group |
| `gpasswd group_name -d username`    | Remove a Member from a Group    |

- Prompts for a new group password and updates `/etc/gshadow`.

- Example

```sh
su -
# create users
useradd dev_admin
useradd dev1
useradd dev2

# set password for admin
passwd dev_admin

# create group
groupadd dev_group -g 3001

# Set group password
gpasswd dev_group

# add admin adn members
gpasswd dev_group -A dev_admin
gpasswd dev_group -a dev1
gpasswd dev_group -M root,rheladmin

# verify
tail /etc/group | grep dev_group
# dev_group:x:3001:root,rheladmin
tail /etc/gshadow | grep dev_group
# dev_group:$6$FRBtW/S9e$z8Xp7BKwwjBmv9pyIDfS.2cmwM9qNuO90sEfZe3nK9IeSOKZ2meY7mu9twHSRXcjrwlDvd7hkjlpfVUPHoIUZ/:dev_admin:root,rheladmin

su - dev_admin
# add user to group as admin
gpasswd dev_group -a dev2
# Adding user dev2 to group dev_group
gpasswd dev_group
```

---

### Deleting a new group

| CMD               | DESC               |
| ----------------- | ------------------ |
| `groupdel g_name` | Delete a new group |

---

### Display Group Info

| CMD               | DESC                                |
| ----------------- | ----------------------------------- |
| `groups`          | List Current logged-in user's group |
| `groups username` | List group for a specific user      |

---

[TOP](#linux---user-management-group)
