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
    - [Lab: System information](#lab-system-information)
      - [Session file and uptime](#session-file-and-uptime)
      - [System information](#system-information-1)
      - [CPU](#cpu)

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

| Command       | Description                                    |
| ------------- | ---------------------------------------------- |
| `tty`         | Display current active terminal session file   |
| `uptime`      | how long the system has been running           |
| `uptime -p`   | show uptime in pretty format                   |
| `uptime -s`   | system up since                                |
| `hostnamectl` | Query the system hostname                      |
| `date`        |                                                |
| `date -s`     |                                                |
| `uname`       | Display system information                     |
| `uname -a`    | Display all information                        |
| `uname -s`    | Display the kernel name                        |
| `uname -p`    | Display the processor type                     |
| `lscpu`       | Display information about the CPU architecture |

---

### Lab: System information

#### Session file and uptime

```sh
tty
# /dev/pts/1

uptime
#  18:23:11 up  2:13,  4 users,  load average: 0.00, 0.00, 0.00

uptime -p
# up 2 hours, 13 minutes
```

> `uptime`:
>
> - current system time: `18:23:11`
> - up duration: `2:13`
> - number of logged-in users: `4 users`
> - CPU load averages over the past 1, 5, and 15 minutes: `0.00, 0.00, 0.00`

---

#### System information

```sh
uname
# Linux

uname -a
# Linux localhost.localdomain 5.14.0-503.22.1.el9_5.x86_64 #1 SMP PREEMPT_DYNAMIC Wed Jan 15 08:02:15 EST 2025 x86_64 x86_64 x86_64 GNU/Linux

uname -p
# x86_64
```

---

#### CPU

```sh
lscpu
# Architecture:             x86_64
#   CPU op-mode(s):         32-bit, 64-bit
#   Address sizes:          45 bits physical, 48 bits virtual
#   Byte Order:             Little Endian
# CPU(s):                   2
#   On-line CPU(s) list:    0,1
# Vendor ID:                GenuineIntel
#   BIOS Vendor ID:         GenuineIntel
#   Model name:             Intel(R) Core(TM) 5 120U
#     BIOS Model name:      Intel(R) Core(TM) 5 120U
#     CPU family:           6
#     Model:                186
#     Thread(s) per core:   1
#     Core(s) per socket:   1
#     Socket(s):            2
#     Stepping:             3
#     BogoMIPS:             4991.99
#     Flags:                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36
#                           clflush mmx fxsr sse sse2 ss syscall nx pdpe1gb rdtscp lm constant_tsc a
#                           rch_perfmon rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid tsc_k
#                           nown_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt
#                            aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch pti ssbd
#                            ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rd
#                           seed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves avx_
#                           vnni arat umip gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clea
#                           r serialize flush_l1d arch_capabilities
# Virtualization features:
#   Hypervisor vendor:      VMware
#   Virtualization type:    full
# Caches (sum of all):
#   L1d:                    96 KiB (2 instances)
#   L1i:                    64 KiB (2 instances)
#   L2:                     2.5 MiB (2 instances)
#   L3:                     24 MiB (2 instances)
# NUMA:
#   NUMA node(s):           1
#   NUMA node0 CPU(s):      0,1
# Vulnerabilities:
#   Gather data sampling:   Not affected
#   Itlb multihit:          Not affected
#   L1tf:                   Mitigation; PTE Inversion
#   Mds:                    Mitigation; Clear CPU buffers; SMT Host state unknown
#   Meltdown:               Mitigation; PTI
#   Mmio stale data:        Unknown: No mitigations
#   Reg file data sampling: Vulnerable: No microcode
#   Retbleed:               Mitigation; IBRS
#   Spec rstack overflow:   Not affected
#   Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl
#   Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
#   Spectre v2:             Mitigation; IBRS; IBPB conditional; STIBP disabled; RSB filling; PBRSB-e
#                           IBRS Not affected; BHI SW loop, KVM SW loop
#   Srbds:                  Not affected
#   Tsx async abort:        Not affected
```
