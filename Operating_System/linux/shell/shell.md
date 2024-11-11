# Linux - Shell

[Back](../index.md)

---

- [Linux - Shell](#linux---shell)
  - [What is the Shell](#what-is-the-shell)
    - [The Prompt](#the-prompt)
    - [Root, the Superuser](#root-the-superuser)
    - [LInux command](#linux-command)
    - [List available shell](#list-available-shell)
  - [`man`](#man)
  - [Environmental Variables](#environmental-variables)
    - [`$PATH`](#path)
    - [`which`](#which)
  - [Executing Commands](#executing-commands)

---

## What is the Shell

- `Shell`
  - aka `command line interpreter`.
  - The `Command Line Interface` to the Linux Operating System
  - The **default** interface to Linux.
  - A program that **accepts** your commands and **executes** those commands.

---

### The Prompt

- format:

  - `[user_name@instance_name current_path] $`

- `#`:
  - pound sign,
  - current user is a root
- `$`:

  - dollar sign
  - current user is a normal user

- `~`:
  - tilde sign
  - home directory
  - e.g.,
    - `~jason`: `/home/jason`
    - `~root`: `/root`
    - `~ftp`: `/var/ftp`, the home dir of ftp service account

---

### Root, the Superuser

- `root`:
  - prompt: `#`
  - can do any operation that Linux system can do.
  - restricted to system administrators.
  - be required to install, start, or stop an application.
- Normal user:
  - prompt: `$`
  - can only do a **subset** of the things root can do.

---

### LInux command

- Most of the commands are lower case.
  - e.g., `PWD`: `command not found ...`

| Command            | Desc                                                  |
| ------------------ | ----------------------------------------------------- |
| `pwd`              | Display the present working direcotry                 |
| `cd dir_name`      | Changes the current directory to dir.                 |
| `ls`               | Lists directory contents.                             |
| `ls -l`            | Lists directory contents using a long listing format. |
| `cat`              | Concatenates and displays files                       |
| `clear`            | Clears the screen                                     |
| `man command_name` | Displays the online manual for command.               |
| `exit`             | Exits the shell or your current session.              |

- Navigate in `man`

| Shortcut | Desc                  |
| -------- | --------------------- |
| `space`  | display the next page |
| `q`      | quit                  |

---

### List available shell

```sh
cat /etc/shells
# /bin/sh
# /bin/bash
# /usr/bin/sh
# /usr/bin/bash
```

## `man`

- Navigating Man Pages

| Shortcut | Desc                            |
| -------- | ------------------------------- |
| `Enter`  | Move down one line.             |
| `Space`  | Move down one page.             |
| `g`      | Move to the top of the page.    |
| `G`      | Move to the bottom of the page. |
| `q`      | Quit.                           |

- Search the short descriptions and manual page names for the keyword

```sh
man -k key_word
```

---

## Environmental Variables

- `Environmental Variables`
  - Storage location that has name-value pairs
  - 这些是由操作系统或用户设置的特殊变量，用于配置 Shell 的行为和影响其执行环境。
  - Typically **uppercase**
  - Access the contents by executing:
    - `echo $VAR_NAME`

### `$PATH`

- `Path`:
  - An environment variable
  - Contains a list of directories separated by colons.
  - Controls the command `search` path
    - when a command is typed in the prompt, it will be searched for in the directories that are listed in the path env variable.
- `echo $PATH`

### `which`

- `which`:
  - shows the full path of (shell) commands.

---

## Executing Commands

- Defaut:
  - `$PATH` determines command search path.
- can execute command not in `$PATH`.
  - can specify a command **with a full path**.
    - `/path/to/command_name`
  - Execute command in this dir
    - `./command`
