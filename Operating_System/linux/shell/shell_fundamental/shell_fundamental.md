# Linux - Shell: Fundamental

[Back](../../index.md)

- [Linux - Shell: Fundamental](#linux---shell-fundamental)
  - [What is the Shell](#what-is-the-shell)
    - [Types of Shells](#types-of-shells)
    - [Find Shell Path](#find-shell-path)
  - [Shell Prompt](#shell-prompt)
    - [Shell prompt customization](#shell-prompt-customization)
    - [Persist PS1 Changes](#persist-ps1-changes)
  - [Environmental Variables](#environmental-variables)
  - [Environment Variables](#environment-variables)
    - [Persisting Environment Variables](#persisting-environment-variables)
    - [Common Env Var](#common-env-var)
    - [Env Var Management](#env-var-management)
    - [Lab: Env](#lab-env)
    - [Lab: Create and export Local variable; Unset the variable](#lab-create-and-export-local-variable-unset-the-variable)
  - [Customize the primary shell prompt](#customize-the-primary-shell-prompt)
  - [Executing Commands](#executing-commands)
    - [Privileged Execution](#privileged-execution)
    - [Command Path](#command-path)
    - [Lab: which, whereis, type](#lab-which-whereis-type)
    - [`man`](#man)
  - [Aliases](#aliases)
    - [Commands](#commands)
    - [Persisting Aliases](#persisting-aliases)
  - [Shell History](#shell-history)
    - [`history`](#history)
    - [`!`syntax](#syntax)
  - [Grep](#grep)

---

## What is the Shell

- `shell`
  - a **command-line interpreter** that provides a **user interface** to **interact** with the Linux **kernel**.
  - It processes commands entered by the user and executes them, often by calling programs or performing built-in operations.

---

### Types of Shells

- `Bash (Bourne Again Shell)`

  - **Default shell** in Red Hat-based systems (like RHEL).

- `sh (Bourne shell)`: Basic and simple.
- `zsh`: Advanced features, customizable.
- `csh` and `tcsh`: C-like syntax.
- `ksh (KornShell)`: Powerful scripting capabilities.

---

### Find Shell Path

- List available shell

```sh
cat /etc/shells
# /bin/sh
# /bin/bash
# /usr/bin/sh
# /usr/bin/bash
```

- Ways to find current shell

```sh
echo $SHELL
# /bin/bash

echo $0
# -bash
```

- Shell of a user

```sh
cat /etc/passwd
# rheladmin:x:1000:1000:rheladmin:/home/rheladmin:/bin/bash
```

---

## Shell Prompt

- Format: `[user_name@instance_name current_path] $`

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

### Shell prompt customization

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

## Environmental Variables

- `Environmental Variables`

  - Storage location that has name-value pairs
  - 这些是由操作系统或用户设置的特殊变量，用于配置 Shell 的行为和影响其执行环境。
  - Typically **uppercase**
  - Access the contents by executing:
    - `echo $VAR_NAME`

- types of variables
  - local variable:
    - value of a local variable is only available in the **current** shell.
  - environment variable
    - the value stored in an environment variable is accessible to the program, as well as any **subprograms** that it spawns during its lifecycle.

---

## Environment Variables

- `Environment Variable`

  - a **storage location** that has a name and a value.
    - They often effect the way programs behave.
    - used to enhance and to standardize your shell environment on Linux systems.
  - Name/Value pairs
    - `NAME=value`
  - Default: upper case

- Value:

  - do not use space sign

- vs **program/process**
  - When a `process` is **started** it **inherits** the **exported** `environment variables` of the process that **spawned** it.
  - A variable that is set or changed **only effects** the **current running process** unless it is exported.
  - The variables that are **not exported** are called `local variables`.
  - The `export` command allows variables to be used by **subsequently** executed commands

---

### Persisting Environment Variables

```sh
echo 'export TZ="US/Pacific"' >> ~/.bash_profile
```

### Common Env Var

| Environment Variables | Variable Description                                          |
| --------------------- | ------------------------------------------------------------- |
| `EDITOR`              | The program to run to perform edits.                          |
| `HOME`                | The Home directory of the user.                               |
| `LOGNAME`             | The login name of the user.                                   |
| `MAIL`                | The location of the user's local inbox.                       |
| `OLDPWD`              | The previous working directory.                               |
| `PATH`                | A colon separated list of directories to search for commands. |
| `PAGER`               | This program may be called to view a file.                    |
| `PS1`                 | The primary prompt string.                                    |
| `PWD`                 | The present working directory.                                |
| `USER`                | The username of the user.                                     |

---

### Env Var Management

| Command                      | Desc                                 |
| ---------------------------- | ------------------------------------ |
| `env`                        | list all env var                     |
| `printenv`                   | print all environment                |
| `printenv \| less`           | print all environment                |
| `printenv ENV_VAR1 ENV_VAR2` | print environment var, without `$`   |
| `echo $ENV_VAR1 $ENV_VAR2`   | print environment var                |
| `export ENV_VAR="value"`     | **Create/Update** an environment var |
| `unset ENV_VAR`              | Removing an env var                  |

---

### Lab: Env

```sh
echo $PATH
# /root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin

printenv PATH
# /root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin

echo $SHELL
# /bin/bash

printenv SHELL
# /bin/bash
```

---

### Lab: Create and export Local variable; Unset the variable

```sh
# define local
VR1=RHEL9
# display
echo $VR1
# RHEL9

# create a sub-shell
bash
# try to display local var\
# note: nothing returns
echo $VR1
#

# exit the subshell
exit
# make a var an env var
echo $VR1
# RHEL9
export VR1

# create sub-shell
bash
# display env
echo $VR1
# RHEL9
```

- Unset

```sh
unset VR1
# try to display
# note: nothing returns
echo $VR1

```

---

## Customize the primary shell prompt

- `$PS1`: store primary command prompt

```sh
# display the default prompt
echo $PS1
# [\u@\h \W]\$

# modify temporarily
export PS1="<$LOGNAME on $(hostname) in \$PWD>"
# new prompt
# <root on ServerB in /var/log>

# permanently
# Edit the .profile file
vi /root/.bash_profile
# export PS1="<$LOGNAME on $(hostname) in $PWD>"

# logout and login
exit
su -
# <root on ServerB in /root>
```

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

### Privileged Execution

- `root`:
  - prompt: `#`
  - can do any operation that Linux system can do.
  - restricted to system administrators.
  - be required to install, start, or stop an application.
- Normal user:

  - prompt: `$`
  - can only do a **subset** of the things root can do.

- `sudo`: execute a command as another user

---

### Command Path

- `Path`:

  - An environment variable
  - Contains a list of directories separated by colons.
  - Controls the command `search` path
    - when a command is typed in the prompt, it will be searched for in the directories that are listed in the path env variable.
  - `echo $PATH`

- `which`:
  - shows the full path of (shell) commands.

---

### Lab: which, whereis, type

```sh
which cd
# /usr/bin/cd

type cd
# cd is a shell builtin

whereis cd
# cd: /usr/bin/cd /usr/share/man/man1/cd.1.gz /usr/share/man/man1p/cd.1p.gz
```

---

### `man`

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

## Aliases

- `Aliases`
  - Shortcuts
  - Use for long commands
  - Use for commands you type often
    - Fix Typos
    - Make Linux behave like another OS

---

### Commands

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

### `history`

- three variables—HISTFILE, HISTSIZE, and HISTFILESIZE—that control the location and history storage.
- `.bash_history`: in the user’s home directory

- `HISTSIZE`: Controls the number of commands to retain in history

  - default: `1000`

```sh
echo $HISTFILE
# /root/.bash_history

echo $HISTSIZE
# 1000

echo $HISTFILESIZE
# 1000
```

- Searching history:

  - `Ctrl-r`: reverse shell history search
  - `Arrows`: Change the command
  - `Enter`: execute the command
  - `Ctrl-g`: cancel shell history search

| CMD       | DESC                       |
| --------- | -------------------------- |
| `history` | Displays the shell history |

```sh
history
# 1  clear
# 2  cat /etc/hostname
# 3  clear
# 4  vi /etc/hosts
# 5  clear
# 6  useradd xanadu
# ...

history 5
# 362  echo $HISTSIZE
# 363  echo $HISTFILESIZE
# 364  history
# 365  history --help
# 366  history 5

# To re-execute
# note: #3=clear
!3

# re-execute the most recent occurrence starting with "ch"
# note: chage
!ch

# To remove entry 24 from history:
history -d 24
```

- disable the shell’s history expansion feature

```sh
set +o history
# reenble
set -o history
```

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

---

## Grep

| CMD                                       | DESC                                                         |
| ----------------------------------------- | ------------------------------------------------------------ |
| `grep root /etc/passwd`                   | Search for pattern                                           |
| `grep ^root /etc/passwd`                  | Search for pattern at the beginning of the line              |
| `grep bash$ /etc/passwd`                  | Search for pattern at the end of the line                    |
| `grep 'aliases and functions' ~/.bashrc`  | Search for pattern                                           |
| `grep -n 'nologin' /etc/passwd`           | show the line numbers                                        |
| `grep -v root /etc/passwd`                | Search exclusively                                           |
| `grep -v $^ ~/.bashrc`                    | exclude all the empty lines                                  |
| `grep -i path /etc/bashrc`                | case-insensitive search                                      |
| `grep -w acce.. /etc/lvm/lvm.conf`        | begin with letters “acce” followed by exactly two characters |
| `ls -l /etc \| grep -E 'cron\|ly'`        | Using Regex                                                  |
| `grep -ve ^& -ve ^# /etc/ssh/sshd_config` | Multiple patterns                                            |
