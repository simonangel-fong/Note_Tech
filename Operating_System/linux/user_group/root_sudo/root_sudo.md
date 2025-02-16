# Linux - User Management: `root` and `sudo`

[Back](../../index.md)

- [Linux - User Management: `root` and `sudo`](#linux---user-management-root-and-sudo)
  - [Root User](#root-user)
  - [`sudo`: superuser do](#sudo-superuser-do)
  - [Doing as Superuser (or Doing as Substitute User)](#doing-as-superuser-or-doing-as-substitute-user)
    - [Configuration File](#configuration-file)
    - [Entry format](#entry-format)
    - [Sudo command log](#sudo-command-log)
  - [`wheel` Group](#wheel-group)
    - [Configuration File](#configuration-file-1)
    - [Lab: Enable a user to perform any sudo command](#lab-enable-a-user-to-perform-any-sudo-command)

---

## Root User

- Key Features of the Root User
- **Full Privileges**
  - Can **read, write, and execute** any file on the system, regardless of permissions.
  - Can **modify system configurations**, **manage users**, and install or remove **software**.
  - has **unrestricted access** to the **entire system**.
- **`UID` and `GID`**
  - The root user’s `UID (User ID)` and `GID (Group ID)` are both `0`.
- **Home Directory**
  - **Default home** directory is `/root`.
- **Shell**
  - Typically uses `/bin/bash` as the default shell, but it can be changed.
- **Password Storage**
  - The root user’s password is stored in the `/etc/shadow` file **in encrypted form**.
- **Default Ownership**

  - Many system files and processes are owned by the root user.

- The **first entry** in the `/etc/passwd`

```sh
su - root
id
# uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

- `uid=0(root)`:
  - User ID (UID) is `0`, indicating the `root` user who has unrestricted access to the system.
  - username is `root`
- `gid=0(root)`
  - Group ID (GID) is `0`, indicating the `root` group which also has full permissions across the system.
  - group name is `root`
- `groups=0(root)`
  - all the groups' id is `0`, indicating the `root` group
- `context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023`
  - SELinux (Security-Enhanced Linux) information
  - `unconfined_u (User)`:
    - SELinux user
    - the user is **not restricted** by SELinux policies.
  - `unconfined_r (Role)`:
    - SELinux role
    - the role has **no** SELinux **restrictions**.
  - `unconfined_t (Type)`:
    - SELinux type or domain
    - the user is operating in an **unrestricted domain**.

---

## `sudo`: superuser do

- `sudo` allows a permitted user to execute a command **as the superuser or another user**.

- Feature:
  - **Temporary Privileges**
    - Grants **temporary** root (or specified user) **privileges** to execute administrative tasks.
    - Users need their password, **not the root password**.
  - **Controlled Access**
    - Access to sudo is configured in the `/etc/sudoers` file, allowing fine-grained permission control.
  - **Session Timeout**
    - By default, sudo remembers your password for a short period (e.g., `5` minutes). This can be adjusted.

| CMD                    | DESC                     |
| ---------------------- | ------------------------ |
| `sudo -l`              | List available commands. |
| `sudo command`         | Run command as root.     |
| `sudo -u user command` | Run as user.             |
| `sudo -s`              | Start a shell            |
| `sudo -u user -s`      | Start a shell as user    |

- To use `sudo`, the current user must be in the sudoers file.

---

## Doing as Superuser (or Doing as Substitute User)

These users can then precede one of those commands with a
utility called sudo (superuser do, a.k.a. substitute user do) at
the time of executing that command. The users are prompted
to **enter their own password**, and if correct, the command is
executed successfully for them.

### Configuration File

- `visudo`

  - a command to edit `sudo` file.

- Example: Enable a user to execute a previlige command

- `/etc/sudoers` File

  - controls who can use sudo and what commands they can execute.
  - contains
    - a list of users
    - what commands that those users can run
    - as what users those commands can be run
  - It is edited using the `visudo` command, which prevents syntax errors that could lock you out.

---

### Entry format

- `user host=(users) [NOPASSWD:]commands`

- full access

```conf
# full access to every administrative function
root  ALL=(ALL) ALL    # root
user1 ALL=(ALL) ALL   # user
%dba  ALL=(ALL) ALL    # group
```

- Limited access

```conf
user1 ALL=/usr/bin/cat
%dba  ALL=/usr/bin/cat
```

- No password prompt

```conf
# No password prompt for all
user1 ALL=(ALL) NOPASSWD:ALL
%dba  ALL=(ALL) NOPASSWD:ALL

# No password prompt for a command
john  ALL=(ALL) NOPASSWD: /bin/systemctl restart apache2
```

- use alias

```conf
Cmnd_Alias  PKGCMD = /usr/bin/yum, /usr/bin/rpm
User_Alias  PKGADM = user1, user100, user200

PKGADM  ALL = PKGCMD
```

---

```sh
su -
# create a new usesr
useradd devops
passwd devops

# edit the /etc/sudoers file
sudo visudo

# devops ALL=(ALL) NOPASSWD: /bin/yum

# Test
# switch user
su - devops
sudo yum upgrade -y

# try other commands
sudo cat /
# Sorry, user devops is not allowed to execute '/bin/cat /' as root on rhelhost.localdomain.
```

---

### Sudo command log

The sudo command logs successful authentication and
command data to the /var/log/secure file under the name of
the actual user executing the command

```sh
tail /var/log/secure
# Feb 15 19:42:23 ServerB groupadd[4391]: new group: name=dba, GID=5000
# Feb 15 19:43:20 ServerB usermod[4398]: add 'user100' to group 'dba'
# Feb 15 19:43:20 ServerB usermod[4398]: add 'user100' to shadow group 'dba'
# Feb 15 19:46:35 ServerB groupmod[4411]: group changed in /etc/group (group linuxadmin/5000, new name: sysadm)
# Feb 15 19:46:35 ServerB groupmod[4411]: group changed in /etc/gshadow (group linuxadmin, new name: sysadm)
# Feb 15 19:46:53 ServerB groupmod[4425]: group changed in /etc/group (group sysadm/5000, new gid: 6000)
# Feb 15 19:46:53 ServerB groupmod[4425]: group changed in /etc/passwd (group sysadm/5000, new gid: 6000)
# Feb 15 19:48:36 ServerB groupdel[4432]: group 'sysadm' removed from /etc/group
# Feb 15 19:48:36 ServerB groupdel[4432]: group 'sysadm' removed from /etc/gshadow
# Feb 15 19:48:36 ServerB groupdel[4432]: group 'sysadm' removed
```

---

## `wheel` Group

- `wheel` group

  - a special user group in Linux systems, particularly on RHEL-based distributions (e.g., CentOS, Fedora, and Red Hat Enterprise Linux).
  - used to **manage administrative privileges**.
    - Users in the `wheel` group are **allowed to execute commands as the `root` user** or another privileged user via the `sudo` command.

- **Controlled Administrative Access**
  - Membership in the `wheel` group **gives users permission** to execute `sudo` commands, effectively allowing them to perform administrative tasks.
- **Security Best Practice**
  - Instead of giving every user sudo access, administrators can **manage membership** in the `wheel` group to control who can perform privileged actions.

---

### Configuration File

- `/etc/group`

  - `wheel:x:10:rheladmin,testuser`
  - A system group

- `/etc/sudoers`

  - `%wheel  ALL=(ALL)       ALL`
  - Allows people in group wheel to run all commands

---

### Lab: Enable a user to perform any sudo command

```sh
# Create the New User
sudo useradd devops1
# Set a Password for the User
sudo passwd devops1
# Add the User to the wheel Group
sudo usermod -aG wheel devops1
# Verify
groups devops1
# devops1 : devops1 wheel

# Test the Configuration
# Switch to the devops1 user:
su - devops1
# test sudo command
sudo yum update
```

---
