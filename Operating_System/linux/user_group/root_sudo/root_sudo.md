# Linux - User Management: `root` and `sudo`

[Back](../../index.md)

- [Linux - User Management: `root` and `sudo`](#linux---user-management-root-and-sudo)
  - [Root User](#root-user)
  - [`sudo`: superuser do](#sudo-superuser-do)
    - [Configuration File](#configuration-file)
  - [`wheel` Group](#wheel-group)
    - [Configuration File](#configuration-file-1)
    - [Example: Enable a user to perform any sudo command](#example-enable-a-user-to-perform-any-sudo-command)

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

### Configuration File

- `/etc/sudoers` File

  - controls who can use sudo and what commands they can execute.
  - contains
    - a list of users
    - what commands that those users can run
    - as what users those commands can be run
  - It is edited using the `visudo` command, which prevents syntax errors that could lock you out.

  - Entry format: `user host=(users) [NOPASSWD:]commands`

  ```conf
  # The root user has unrestricted privileges.
  root ALL=(ALL) ALL
  # The user john can restart Apache without a password.
  john ALL=(ALL) NOPASSWD: /bin/systemctl restart apache2
  ```

- `visudo`

  - a command to edit `sudo` file.

- Example: Enable a user to execute a previlige command

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

### Example: Enable a user to perform any sudo command

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
