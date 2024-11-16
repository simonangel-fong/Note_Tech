# Linux - Fundamental

[Back](../index.md)

---

- [Linux - Fundamental](#linux---fundamental)
  - [What is Linux](#what-is-linux)
  - [WSL](#wsl)
  - [Version](#version)

---

## What is Linux

- `Linux`

  - An **Operating System**
  - A Kernel
    - a layer between **applications** and physical **hardwares**.
  - A `FOSS(Free/Open Source Software)`
    - the source is free, but the distribution, binary, and compile code are not free.
  - Unix-like.

- `Linux Distributions`

  - Linux `Kernel` + Additional **software/application**
  - Each has its own focus
  - `distro` / `flavor`
    - short for `distributions`
    - https://distrowatch.com/
  - popular distro
    - Red Hat Enterprise Linux(RHEL)
    - Ubuntu
    - Fedora
    - CentOS
    - Debian
    - SuSE Linux Enterprise Server(SLES)
    - OpenSuSE

- Benefits

  - Run on many hardware platfoms
  - Stable, reliable, secure
    - great for server
  - FOSS
  - Free Software Ecosystem

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

[TOP](#linux---fundamental)
