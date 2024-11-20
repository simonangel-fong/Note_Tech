# Linux - User Management: User

[Back](../../index.md)

- [Linux - User Management: User](#linux---user-management-user)
  - [User ID](#user-id)
    - [Types of UIDs](#types-of-uids)
    - [Types of UID for proecess](#types-of-uid-for-proecess)
  - [Group Configuration Files](#group-configuration-files)
    - [`/etc/passwd`](#etcpasswd)
    - [`/etc/shadow`](#etcshadow)
  - [User Management](#user-management)
    - [Add a new user](#add-a-new-user)
    - [Delete a user account](#delete-a-user-account)
    - [Change a user account](#change-a-user-account)
    - [Display user information](#display-user-information)
    - [Switch user](#switch-user)
  - [Password](#password)
    - [Password Mangement](#password-mangement)

---

## User ID

- `UserID`:

  - a **unique number** which is an **integer** number to identified every user in Linux.

- Why UID Is Important:
  - **File Ownership**
    - Every `file` or `directory` is **associated with** a `UID`.
    - The system uses it to **determine the owner** of the resource.
  - **Process Ownership**
    - Each `running process` is **associated with** a `UID`.
    - This ensures `processes` are restricted by **user permissions**.
  - **Access Control**
    - **Permissions** (read, write, execute) depend on the `UID` of the user trying to access a file or resource.
  - **System Security**
    - System administrators can **restrict access** to files, processes, and commands based on **UIDs**, enhancing security.

---

### Types of UIDs

- `Root User (UID 0)`

  - The **superuser** with `UID 0` has **unrestricted access** to the **entire** system.
  - Example: The root account.

- `System Users (UID 1–999)`

  - Reserved for system accounts and services like `daemon`, `sys`, and `nobody`.
  - These accounts are **not intended for human login** but for `system processes`.

- `Regular Users (UID 1000 and above)`

  - Assigned to **human users created** by `system administrators`.
  - Example: A user account created **during installation** typically gets `UID 1000`.

- `Nobody User (Typically UID 65534)`
  - A special user with **minimal permissions**, often used for **anonymous** or **unprivileged processes**.

---

### Types of UID for proecess

- 3 types of `UID` defined for a **process**, which can be dynamically changed as per the privilege of task.

  - 1. `Real UserID`
  - 2. `Effective UserID`
  - 3. `Saved UserID`

- `Real UserID`:

  - usually the ID of the user **who started the process**.
  - used to identifies the user **who owns the process**.
  - used to determine **ownership for accounting** purposes.

- `Effective UserID`:

  - used to determines the **permissions** the process has **during execution**.
  - typically the same as the `RUID` unless the program has the `setuid bit` set.即只针对“与所有者同权”的程序
    - If the `setuid bit` is set, the `EUID` becomes the `UID` of the **file owner**, allowing the process to **temporarily escalate privileges**.
  - 一般情况： `EUID=RUID`
    - 当程序是 `setuid` 时，`EUID=UID of file owner`
  - Example: `passwd`, a `setuid` program. When executing `passwd`, `EUID = root id`

- `Saved UserID`:

  - stores the **original** `EUID` when a process changes its `EUID`.
  - allows the process to **revert** to the **original** `EUID` **after temporarily escalating privileges**.
  - primarily used in programs that need to **drop and regain** `elevated privileges`.

  - Example:

    - The file owner is `root` (`UID: 0`).
    - It has the `setuid bit` set.
    - When a regular user (bob) executes the program:
      - `RUID = 1001 (bob)`
      - `EUID = 0 (root) (due to the setuid bit)`
      - `SUID = 0 (saved EUID for privilege restoration)`
      - The program can drop privileges by changing the `EUID` to the `RUID (1001)` and later restore privileges by reverting the `EUID` to the `SUID (0)`.

  - It is used when a process is **running with elevated privileges** (generally `root`) needs to **do some `under-privileged work`**, this can be **achieved** by temporarily switching to a non-privileged account.
  - While performing `under-privileged work`, the `effective UID` is **changed** to some **lower privilege value**, and the `euid` is saved to `saved userID(suid)`, so that it can be **used for switching back** to a `privileged account` when the task is completed.

---

## Group Configuration Files

### `/etc/passwd`

- User information, including `UIDs`, is stored in the `/etc/passwd` file.

- File permission

```conf
-rw-r--r--. 1 root root 2679 Nov 19 16:44 /etc/passwd
```

- Format of an entry:

```conf
username:x:UID:GID:comment:home_directory:shell
```

- `username`
  - The login name of the user.
  - Must be unique on the system.
- `x`
  - Placeholder indicating that the **encrypted password is stored** in `/etc/shadow`.
  - Historically, passwords were stored here in an insecure form, but modern systems separate them for security.
- `UID (User ID)`
  - A **unique numeric identifier** for the user.
  - `System users` typically have UIDs below `1000`.
  - `Regular users` have **higher** UIDs.
  - `UID 0` is reserved for the root user (administrator).
- `GID (Group ID)`
  - The **primary group** ID associated with the user.
  - Corresponds to an entry in `/etc/group`.
- `comment`
  - A field for user information, such as the user’s **full name** or other details.
  - Often **populated** when creating a user with `useradd`.
- `home_directory`
  - The **absolute path** to the user’s **home** directory.
  - Defaults to `/home/username`.
- `shell`

  - The user’s **default login shell** (e.g., `/bin/bash`, `/bin/zsh`).
  - If set to `/sbin/nologin` or `/bin/false`, the user cannot log in interactively.

---

### `/etc/shadow`

- Contains user accounts information
- File permission

```conf
----------. 1 root root 1426 Nov 19 16:43 /etc/shadow
```

- Entry format:

```conf
username:encrypted_password:last_change:min:max:warn:inactive:expire:
```

- `username`
  - The name of the user (must match the username in `/etc/passwd`).
- `encrypted_password`
  - The **hashed password** for the user.
  - Commonly hashed using algorithms like MD5, SHA-256, or SHA-512.
  - Special values:
    - `*` or `!`: Account is **locked** or **disabled**.
    - **Empty field** (`::`): **No password** is set.
- `last_change`
  - The number of days **since January 1, 1970**, when the password was **last changed**.
- `min`
  - Minimum number of days **before** the password can be **changed**.
- `max`
  - Maximum number of days the password is **valid before** requiring a change.
- `warn`
  - Number of days before password **expiration to warn** the user.
- `inactive`
  - Number of days after password expiration before the account is disabled.
- `expire`
  - Number of days since January 1, 1970, when the **account** will be **disabled**.
  - If empty, the account does **not expire**.
- `reserved`

  - Reserved for **future use** (optional).

---

## User Management

### Add a new user

| CMD                           | DESC                                           |
| ----------------------------- | ---------------------------------------------- |
| `useradd username`            | Create a new user                              |
| `useradd username -c comment` | Create a new user with comment                 |
| `useradd username -d path`    | Create a new user and specify a user directory |
| `useradd username -g group`   | Create a new user and specify primary group    |
| `useradd username -G g1,g2`   | Create a new user and specify additional group |
| `useradd username -s bash`    | Create a new user and specify shell            |
| `useradd username -u uid`     | Create a new user and specify UID              |

- If username already exists:

  - `useradd: user already exists`

- Example

```sh
useradd testuser \
  -u 2001 \
  -g rheladmin  \
  -G wheel,root,rheladmin \
  -c "user for testing" \
  -d /home/test_user  \
  -s /usr/bin/sh

id testuser
# uid=2001(testuser) gid=1000(rheladmin) groups=1000(rheladmin),0(root),10(wheel)

tail -1 /etc/passwd
# testuser:x:2001:1000:user for testing:/home/test_user:/usr/bin/sh
```

---

### Delete a user account

| CMD                   | DESC                              |
| --------------------- | --------------------------------- |
| `userdel username`    | Delete a user account             |
| `userdel username -f` | Force to delete a user            |
| `userdel username -r` | Delete a user with home directory |

---

### Change a user account

| CMD                             | DESC                                |
| ------------------------------- | ----------------------------------- |
| `usermod username -l logname`   | Modify a user's login name          |
| `usermod username -u UID`       | Modify a user's UID                 |
| `usermod username -g group`     | Modify a user's initial login group |
| `usermod username -G g1,g2`     | Modify a user's group list          |
| `usermod username -c comment`   | Modify a user's comment             |
| `usermod username -d home_path` | Modify content to a user's new home |
| `usermod username -s shell`     | Modify a user's shell               |

- Example

```sh
# create a new user
useradd testuser \
  -u 2001 \
  -g rheladmin  \
  -G wheel,root,rheladmin \
  -c "user for testing" \
  -d /home/test_user  \
  -s /usr/bin/sh


# verify
id testuser
# uid=2001(testuser) gid=1000(rheladmin) groups=1000(rheladmin),0(root),10(wheel)

tail -1 /etc/passwd
# testuser:x:2001:1000:user for testing:/home/test_user:/usr/bin/sh

# modify user
usermod testuser  \
  -l testlog  \
  -u 4321 \
  -g root \
  -G rheladmin,wheel  \
  -c "testing user" \
  -d /home/testuser -m  \
  -s /bin/bash

# verify
id testuser
# id: ‘testuser’: no such user

id testlog
# uid=4321(testlog) gid=0(root) groups=0(root),10(wheel),1000(rheladmin)

tail -1 /etc/passwd
# testlog:x:4321:0:testing user:/home/testuser:/bin/bash
```

---

### Display user information

| CMD           | DESC                                                       |
| ------------- | ---------------------------------------------------------- |
| `id`          | print the current user's `UID`, `GID`, and groups.         |
| `id username` | print information for the specified user.                  |
| `id -u`       | Show Only `UID`                                            |
| `id -g`       | Outputs the primary group ID of the user.                  |
| `id -G`       | Outputs all group IDs the user belongs to.                 |
| `id -nu`      | Show username                                              |
| `id -ng`      | Show primary group name                                    |
| `id -nG`      | Show all group names                                       |
| `whoami`      | print effective userid                                     |
| `who`         | Print information about users who are currently logged in. |
| `w`           | Show who is logged on and what they are doing.             |

---

### Switch user

| Command                       | Desc                                               |
| ----------------------------- | -------------------------------------------------- |
| `whoami`                      | Display the effective username                     |
| `su`                          | Change become superuser                            |
| `su username`                 | Change user ID                                     |
| `su - username`               | Change user ID and load env                        |
| `su username -c 'command1'`   | Change user ID without env and execute the command |
| `su - username -c 'command1'` | Change user ID with env and execute the command    |

- If an evn var has exported, the env var can be used after switching to another user without loading its env var, `su username`.
  - If the user is changed using `su - username`, then the env var for this user will be loaded and the exported env var in the same session cannot be used.

---

## Password

### Password Mangement

| CMD                   | DESC                                |
| --------------------- | ----------------------------------- |
| `usermod username -L` | Lock user's pwd                     |
| `usermod username -U` | Unlock user's pwd                   |
| `passwd`              | Modify pwd for the current user     |
| `passwd user`         | Modify pwd for a user               |
| `passwd user -l`      | Lock a user's pwd                   |
| `passwd user -u`      | Unlock a user's pwd                 |
| `passwd user -e`      | Expire a user's pwd                 |
| `passwd user -d`      | Delete a user's pwd                 |
| `passwd user -f`      | Force user to change pwd next login |

---

[TOP](#linux---user-management-user)
