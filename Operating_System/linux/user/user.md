# Linux - User

[Back](../index.md)

---

- [Linux - User](#linux---user)
  - [Groups](#groups)
  - [User](#user)
    - [`su`: Switch user](#su-switch-user)
    - [`sudo`: superuser do](#sudo-superuser-do)
      - [Changing the `sudo` configuration](#changing-the-sudo-configuration)

---

## Groups

- Every `user` is in **at least one** `group`.
- `Users` can belong to **many** `groups`.
- `Groups` are used to **organize** `users`.
- The `groups` command displays a user’s groups.
- You can also use `id -Gn`.

| Command            | Desc                                   |
| ------------------ | -------------------------------------- |
| `groups`           | show the groups the current user is in |
| `id -Gn`           | show the groups the current user is in |
| `groups user_name` | show the groups a specific user is in  |
| `id user_name -Gn` | show the groups a specific user is in  |

---

## User

---

### `su`: Switch user

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

### `sudo`: superuser do

| CMD                    | DESC                                                     |
| ---------------------- | -------------------------------------------------------- |
| `sudo -l`              | List available commands.                                 |
| `sudo command`         | Run command as root.                                     |
| `sudo -u root command` | Same as above.                                           |
| `sudo -u user command` | Run as user.                                             |
| `sudo su`              | Switch to the superuser account.                         |
| `sudo su -`            | Switch to the superuser account with root’s environment. |
| `sudo su - username`   | Switch to the username account.                          |
| `sudo -s`              | Start a shell                                            |
| `sudo -u root -s`      | Same as sudo -s                                          |
| `sudo -u user -s`      | Start a shell as user                                    |

- To use `sudo`, the current user must be in the sudoers file.

---

#### Changing the `sudo` configuration

- `sudoers file`

  - contains a list of users
  - and what commands that those users can run
  - and as what users those commands can be run

- `visudo`

  - a command to edit sudo file.

- Sudoers Format
  - `user host=(users) [NOPASSWD:]commands`
  - e.g.,

```sh
# adminuser at all host as all user, can execute all commands without password
adminuser ALL=(ALL) NOPASSWD:ALL

# jason at linuxsvr host as root, can execute the oracle command.
jason linuxsvr=(root) /etc/init.d/oracle
```
