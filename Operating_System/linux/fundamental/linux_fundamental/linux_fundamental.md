# Linux - Fundamental

[Back](../../index.md)

- [Linux - Fundamental](#linux---fundamental)
  - [What is Linux](#what-is-linux)
  - [WSL](#wsl)
  - [Version](#version)
  - [Help Commands](#help-commands)

---

## What is Linux

- `Linux`

  - An **Operating System**
  - A Kernel
    - a layer between **applications** and physical **hardwares**.
  - A `FOSS(Free/Open Source Software)`
    - the source is free, but the distribution, binary, and compile code are not free.
  - Unix-like.

- `Kernel`
  - the core of Linux
  - layer between hardware and applications.

---

## WSL

- `WSL`

  - `Windows Subsystem for Linux`
  - **Alternative** to creating Virtual Machines
  - **Multiple** Linux Distros are available.
  - Lightweight.
  - Windows 10 or newer
  - Virualization Settings Enabled in BIOS.
  - Internet connection is required.
    - Default Linux Distro: Ubuntu LTS

- Run Terminal as administrator
  - Command to install WSL: `wsl --install`
    - input user and pwd
  - relogin:
    - win search Ubuntu

| Command                      | Desc                               |
| ---------------------------- | ---------------------------------- |
| `wsl -l -o`                  | list available distro online       |
| `wsl -l`                     | list all installed distro locally  |
| `wsl --install`              | Install default(Ubuntu) distro wsl |
| `wsl --install -d Debian`    | Install Debian distro wsl          |
| `wsl --unregister -d Debian` | remove Debian distro from wsl      |

- When a distro is not on the online list, can search for and install the distro using `Store`
- To completely uninstall distro, the uninstallation using `Apps & features` is required.

---

## Version

- `LTS`
  - `Long Term Support`
  - Released every 2 years
  - Supported for 5 years
  - releases are even numbered versions with a minor version of .04.
- Version represents year and month

- `Developer Releases`
  - non `LTS` version
  - released every 6 months
  - Supported for just 9 months.

---

## Help Commands

- 3 types of help commands

| CMD                        | DESC                                         |
| -------------------------- | -------------------------------------------- |
| `help`                     | Provides information on built-in commands    |
| `whatis command1 command2` | Display one-line manual page descriptions    |
| `command -help`            | Display all options of a command             |
| `man command`              | Display a completed manual page of a command |

---

[TOP](#linux---fundamental)
