# OS - WSL

[Back](../../index.md)

- [OS - WSL](#os---wsl)
  - [Common Commands](#common-commands)
  - [Install Ubuntu](#install-ubuntu)

---

## Common Commands

| Commands                                         | Description                                                |
| ------------------------------------------------ | ---------------------------------------------------------- |
| `wsl --help`                                     | Display help information about WSL commands.               |
| `wsl --status`                                   | Check WSL status.                                          |
| `wsl --list --online`                            | List available Linux distributions                         |
| `wsl --list --verbose`                           | List installed Linux distributions                         |
| `wsl --list --running`                           | List running distributions.                                |
| `wsl --install`                                  | Install the default Linux distribution (Ubuntu) on WSL.    |
| `wsl --update`                                   | Update the WSL 2 Linux kernel.                             |
| `wsl --set-version distro_name versionNumber`    | Set the default WSL version for a specific distribution.   |
| `wsl --shutdown`                                 | Gracefully shutdown all WSL distributions.                 |
| `wsl --user <Username>`                          | Run as a specific user                                     |
| `wsl --unregister <Distro>`                      | Unregister a WSL distribution.                             |
| `wsl --terminate <Distro>`                       | Terminate a running distribution.                          |
| `wsl --export <Distro> <File>`                   | Export a distribution to a tar file for backup or sharing. |
| `wsl --import <Distro> <InstallLocation> <File>` | Import a distribution from a tar file.                     |

---

## Install Ubuntu

```sh
wsl --status
# Default Distribution: Ubuntu
# Default Version: 2

wsl --list
# Windows Subsystem for Linux Distributions:
# Ubuntu (Default)
# docker-desktop
# Debian

wsl --list --running
#   NAME              STATE           VERSION
# * Ubuntu            Stopped         2
#   docker-desktop    Stopped         2
#   Debian            Stopped         2

wsl --list --online
# Ubuntu                          Ubuntu
# Debian                          Debian GNU/Linux
# kali-linux                      Kali Linux Rolling
# Ubuntu-18.04                    Ubuntu 18.04 LTS
# Ubuntu-20.04                    Ubuntu 20.04 LTS
# Ubuntu-22.04                    Ubuntu 22.04 LTS
# Ubuntu-24.04                    Ubuntu 24.04 LTS
# OracleLinux_7_9                 Oracle Linux 7.9
# OracleLinux_8_10                Oracle Linux 8.10
# OracleLinux_9_5                 Oracle Linux 9.5
# openSUSE-Leap-15.6              openSUSE Leap 15.6
# SUSE-Linux-Enterprise-15-SP6    SUSE Linux Enterprise 15 SP6
# openSUSE-Tumbleweed             openSUSE Tumbleweed

# install Ubuntu
wsl --install

# Export a distribution
wsl --export Ubuntu ./ubuntu_origin.tar
```
