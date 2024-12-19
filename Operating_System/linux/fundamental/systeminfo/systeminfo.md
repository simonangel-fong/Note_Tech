# Linux - Fundamental: System Information

[Back](../../index.md)

---

- [Linux - Fundamental: System Information](#linux---fundamental-system-information)
  - [Linux Distro](#linux-distro)
    - [Debian-based Distributions](#debian-based-distributions)
    - [Red Hat-based Distributions](#red-hat-based-distributions)
    - [Arch-based Distributions](#arch-based-distributions)
    - [SUSE-based Distributions](#suse-based-distributions)
    - [Others](#others)
    - [Method: Identifying Linux Distro](#method-identifying-linux-distro)
  - [Lab: Get Linux Distro](#lab-get-linux-distro)
    - [`/etc/os-release` File](#etcos-release-file)
    - [Command `uname -a`](#command-uname--a)
    - [Command `hostnamectl`](#command-hostnamectl)
  - [System Information](#system-information)

---

## Linux Distro

- `Linux Distributions`

  - Linux `Kernel` + Additional **software/application**
  - Each has its own focus
  - `distro` / `flavor`
    - short for `distributions`
    - https://distrowatch.com/

---

### Debian-based Distributions

- Originates from the **Debian Project**, one of the oldest and most influential Linux distributions.

- Key Features:

  - Uses `.deb` packages and the `APT` (Advanced Package Tool) system.

- **Popular Distributions**
  - `Debian`:
    - The upstream distribution, emphasizing free software and stability.
  - `Ubuntu`:
    - User-friendly, widely adopted for desktops, servers, and cloud environments.
  - `Linux Mint`:
    - Aimed at beginners, based on Ubuntu or directly on Debian.
  - `Kali Linux`:
    - Based on Debian, tailored for penetration testing and security analysis.

---

### Red Hat-based Distributions

- Originates from **Red Hat Linux**, a **commercial distribution** focused on enterprise environments.
- **Key Features**: Uses `.rpm` packages and tools like `YUM` or `DNF`.
- **Enterprise Focus**: Offers **features tailored** for servers, virtualization, and cloud computing.
- **Popular Distributions**

  - `Red Hat Enterprise Linux (RHEL)`:
    - A **commercial** distribution with professional support.
  - `Fedora`:
    - A cutting-edge, **community**-driven distribution, often serving as a **testing ground** for RHEL.
  - `CentOS/AlmaLinux/Rocky Linux`:
    - **Community**-supported alternatives to RHEL, compatible for enterprise use.
  - `Oracle Linux`:
    - Supported by Oracle. Aims to be fully compatible with Red Hat Enterprise Linux.

---

### Arch-based Distributions

- Originates from **Arch Linux**, a minimalist and lightweight distribution that emphasizes simplicity and user control.
- **Key Features**:

  - **Package Management**:
    - Uses the pacman package manager and supports the `Arch User Repository (AUR)`.
  - **Rolling Release**:
    - Always up-to-date **without major version upgrades**.
  - **Manual Setup**: - **Requires users to configure** most aspects, providing a deeper understanding of Linux.

- **Popular Distributions**

  - `Arch Linux`:
    - The original, requiring manual installation and configuration.
  - `Manjaro`:
    - A user-friendly version of Arch Linux with preconfigured tools and graphical interfaces.
  - `EndeavourOS`: A lightweight, beginner-friendly Arch-based distribution.

---

### SUSE-based Distributions

- Originates from **SUSE Linux**, a **German** distribution focused on enterprise environments and ease of use.
- Key Features
  - **Package Management**:
    - Uses `.rpm` packages with the **zypper package manager**.
  - **Enterprise Tools**:
    - Includes tools like `YaST (Yet another Setup Tool)` for system administration.
- **Popular Distributions**

  - `openSUSE Leap`: Stable, fixed-release version ideal for production use.
  - `openSUSE Tumbleweed`: Rolling release version for users who want the latest software.
  - `SUSE Linux Enterprise (SLE):` A commercial distribution with professional support.

---

### Others

- `Alpine Linux`:
  - **Minimalist** and security-focused, widely used in **containerized environments** like Docker.

---

### Method: Identifying Linux Distro

- Identifying the flavor (distribution) of Linux is **important**:

  - **Package Management** and **Software Installation**
    - **Debian-based** (Ubuntu, Debian, etc.): Use `apt` with `.deb` packages.
    - **Red Hat-based** (RHEL, CentOS, AlmaLinux, etc.): Use `yum` or `dnf` with `.rpm` packages.
    - **SUSE-based**: Use `zypper`.
  - **Configuration File** Locations and **System Tools**
    - Network:
      - Ubuntu:`/etc/network/interfaces`
      - RHEL: `/etc/sysconfig/network-scripts/`
    - System Tools:
      - `YaST` (SUSE) or `firewalld` (RHEL)

---

- Check `/etc/os-release` File
  - Most modern Linux distributions include the `/etc/os-release` file, which provides detailed information about the operating system.
- Distribution-Specific Files

  - `/etc/redhat-release` or `/etc/centos-release`: Red Hat-based (RHEL, CentOS, AlmaLinux, etc.)
  - `/etc/debian_version`: Debian-based (Debian, Ubuntu, etc.)

- Command:
  - `uname -a`: provides information about a Linux system's operating system and hardware platform
  - `hostnamectl`: provides information about the operating system and the hostname.

---

## Lab: Get Linux Distro

### `/etc/os-release` File

```sh
# rhel8
cat /etc/os-release
# NAME="Red Hat Enterprise Linux"
# VERSION="8.10 (Ootpa)"
# ID="rhel"
# ID_LIKE="fedora"
# VERSION_ID="8.10"
# PLATFORM_ID="platform:el8"
# PRETTY_NAME="Red Hat Enterprise Linux 8.10 (Ootpa)"
# ANSI_COLOR="0;31"
# CPE_NAME="cpe:/o:redhat:enterprise_linux:8::baseos"
# HOME_URL="https://www.redhat.com/"
# DOCUMENTATION_URL="https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8"
# BUG_REPORT_URL="https://issues.redhat.com/"

# REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 8"
# REDHAT_BUGZILLA_PRODUCT_VERSION=8.10
# REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
# REDHAT_SUPPORT_PRODUCT_VERSION="8.10"

# kali
cat /etc/os-release
# PRETTY_NAME="Kali GNU/Linux Rolling"
# NAME="Kali GNU/Linux"
# VERSION_ID="2024.3"
# VERSION="2024.3"
# VERSION_CODENAME=kali-rolling
# ID=kali
# ID_LIKE=debian
# HOME_URL="https://www.kali.org/"
# SUPPORT_URL="https://forums.kali.org/"
# BUG_REPORT_URL="https://bugs.kali.org/"
# ANSI_COLOR="1;31"

# Ubuntu
cat /etc/os-release
# PRETTY_NAME="Ubuntu 24.04.1 LTS"
# NAME="Ubuntu"
# VERSION_ID="24.04"
# VERSION="24.04.1 LTS (Noble Numbat)"
# VERSION_CODENAME=noble
# ID=ubuntu
# ID_LIKE=debian
# HOME_URL="https://www.ubuntu.com/"
# SUPPORT_URL="https://help.ubuntu.com/"
# BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
# PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
# UBUNTU_CODENAME=noble
# LOGO=ubuntu-logo
```

---

### Command `uname -a`

```sh
# rhel
uname -a
# Linux serverhost 4.18.0-553.30.1.el8_10.x86_64 #1 SMP Fri Nov 15 03:46:25 EST 2024 x86_64 x86_64 x86_64 GNU/Linux

# kali
uname -a
# Linux kali 6.8.11-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.8.11-1kali2 (2024-05-30) x86_64 GNU/Linux

# Ubuntu
uname -a
# Linux ubuntuhost 6.8.0-50-generic #51-Ubuntu SMP PREEMPT_DYNAMIC Sat Nov  9 17:58:29 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
```

---

### Command `hostnamectl`

```sh
# rhel
hostnamectl
  #  Static hostname: serverhost
  #        Icon name: computer-vm
  #          Chassis: vm
  #       Machine ID: ca299475723c4510bf96994f9b0391d6
  #          Boot ID: d2b092c72847419299d28371039f322b
  #   Virtualization: vmware
  # Operating System: Red Hat Enterprise Linux 8.10 (Ootpa)
  #      CPE OS Name: cpe:/o:redhat:enterprise_linux:8::baseos
  #           Kernel: Linux 4.18.0-553.30.1.el8_10.x86_64
  #     Architecture: x86-64

# kali
hostnamectl
#  Static hostname: kali
#        Icon name: computer-vm
#          Chassis: vm 🖴
#       Machine ID: 30e662c5c81d4191bd2444a79c97d2e0
#          Boot ID: e71d7023d146411b8f35e5febc4b0f97
#     AF_VSOCK CID: 2318294775
#   Virtualization: vmware
# Operating System: Kali GNU/Linux Rolling
#           Kernel: Linux 6.8.11-amd64
#     Architecture: x86-64
#  Hardware Vendor: VMware, Inc.
#   Hardware Model: VMware Virtual Platform
# Firmware Version: 6.00
#    Firmware Date: Thu 2020-11-12
#     Firmware Age: 4y 1month 3d

# Ubuntu
hostnamectl
#  Static hostname: ubuntuhost
#        Icon name: computer-vm
#          Chassis: vm 🖴
#       Machine ID: f03cfca8f1fd42509cb87977b8ba9444
#          Boot ID: ec79fc9686df4b16878786c1edbf1370
#   Virtualization: vmware
# Operating System: Ubuntu 24.04.1 LTS
#           Kernel: Linux 6.8.0-50-generic
#     Architecture: x86-64
#  Hardware Vendor: VMware, Inc.
#   Hardware Model: VMware Virtual Platform
# Firmware Version: 6.00
#    Firmware Date: Thu 2020-11-12
#     Firmware Age: 4y 1month 3d
```

---

## System Information

| Command       | Description                          |
| ------------- | ------------------------------------ |
| `uptime`      | how long the system has been running |
| `uptime -p`   | show uptime in pretty format         |
| `uptime -s`   | system up since                      |
| `hostnamectl` | Query the system hostname            |
| `date`        |                                      |
| `date -s`     |                                      |

---
