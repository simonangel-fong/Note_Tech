# Linux - Shell

[Back](../../index.md)

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
  - [Execution Permissions](#execution-permissions)
  - [Shell prompt customization](#shell-prompt-customization)
    - [Persist PS1 Changes](#persist-ps1-changes)
  - [Using Aliases](#using-aliases)
    - [Persisting Aliases](#persisting-aliases)
  - [Shell History](#shell-history)
  - [History](#history)
    - [`!`syntax](#syntax)

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

---

## Execution Permissions

| Command | Desc                              |
| ------- | --------------------------------- |
| `sudo`  | execute a command as another user |

---

## Shell prompt customization

- Use an environment variable to customize.
- Bash, ksh, and sh use `$PS1`.
- Csh, tcsh, and zsh use `$prompt`.

- Customizing the Prompt with `PS1`

| Sysmbol | Desc                                                |
| ------- | --------------------------------------------------- |
| `\h`    | Short hostname, up to the first period              |
| `\H`    | Full hostname                                       |
| `\n`    | Newline                                             |
| `\d`    | Date in "Weekday Month Date" format "Tue May 26"    |
| `\t`    | Current time in **24-hour** `HH:MM:SS` format       |
| `\A`    | Current time in **24-hour** `HH:MM` format          |
| `\T`    | Current time in **12-hour** `HH:MM:SS` format       |
| `\@`    | Current time in **12-hour** `am/pm` format          |
| `\u`    | Username of the current user                        |
| `\w`    | Current working directory                           |
| `\W`    | Basename of the current working directory           |
| `\$`    | if the effective UID is `0`, a `#`, otherwise a `$` |

- Example

```sh
PS1="[\A \u@\h \W] \$ "
```

---

### Persist PS1 Changes

```sh
echo 'export PS1="[\A \u@\h \W]\$ "' >> ~/.bash_profile
```

---

## Using Aliases

- `Aliases`
  - Shortcuts
  - Use for long commands
  - Use for commands you type often
    - Fix Typos
    - Make Linux behave like another OS

| Command              | Desc               |
| -------------------- | ------------------ |
| `alias `             | List all aliases   |
| `alias name='value'` | Create an alias    |
| `unalias name`       | Remove an alias    |
| `unalias -a`         | Remove all aliases |

- Example

```sh
alias cls='clear'
```

---

### Persisting Aliases

- Add aliases to your personal initialization files.
  - `.bash_profile`

```sh
echo 'alias cls='clear'' >> ~/.bash_profile
```

---

## Shell History

- `Shell history`
  - Executed commands are added to the history.
  - can be displayed and recalled.
  - stored in memory and on disk
    - redhat: `~/.bash_history`
    - `~/.history`
    - `~/.histfile`

---

## History

- `HISTSIZE`: Controls the number of commands to retain in history

  - default: `1000`

- Searching history:

  - `Ctrl-r`: reverse shell history search
  - `Arrows`: Change the command
  - `Enter`: execute the command
  - `Ctrl-g`: cancel shell history search

| CMD       | DESC                       |
| --------- | -------------------------- |
| `history` | Displays the shell history |

### `!`syntax

| Syntax    | DESC                                                       |
| --------- | ---------------------------------------------------------- |
| `!N`      | Repeat command line number N                               |
| `!!`      | Repeat the previous command line                           |
| `!string` | Repeat the most recent command line starting with "string" |

- `!:N <Event> <Separator> <Word>`
  - `!`: the most recent command line
  - `!=!!`
  - `:N`: represens a word on the command line.
    - `0` = command
    - `1` = first argument
- `!^`: the 1st argument
- `!$`: the last argument

- Example

```sh
head file1 file2 hamlet.txt
# output

!!
# repeat the last command and output

vi !:2
# vi file2
# ! is to repeat the most recent command, which is !!, which is head command
# :N represents the 2nd argument, which is file2.
# so the this command is to open the file2 in vim editor.

head file1 file2 hamlet.txt
vi !$
```
