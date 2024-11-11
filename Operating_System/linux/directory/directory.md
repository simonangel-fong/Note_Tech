# Linux - Directory

[Back](../index.md)

---

- [Linux - Directory](#linux---directory)
  - [Directory](#directory)
  - [Common Directories](#common-directories)
  - [Application Directory Structures](#application-directory-structures)

---

## Directory

- `Directory`:

  - Are Containers for other files and directories.
  - Provide a tree like structure.
  - Can be accessed by name or shortcut.

- Direcotry shortcuts:

| shortcut  | Desc                                |
| --------- | ----------------------------------- |
| `.`       | Current directory                   |
| `..`      | Parent directory                    |
| `cd -`    | change to the previouse directory   |
| `$OLDPWD` | An env var holds dir previously in. |

---

## Common Directories

- `/`: “Root”, the top of the file system hierarchy.

- System related

  - `/boot`: **Files** needed to **boot** the operating system.
  - `/etc`: System **configuration** files.
  - `/lib`: System **Libraries**. 存放基本代码库
  - `/lib64`: System **Libraries**, 64 bit.
  - `/sys`: Used to display and sometimes configure the devices known to the **Linux kernel**.

- Program related

  - `/bin`: Binaries and other **executable** programs.
  - `/sbin`: System **administration binaries**.
  - `/opt`: **Optional** or third party software.
  - `/usr`: **User related** programs.

    - `/usr/bin`: User related binaries and other executable programs.
    - `/usr/sbin`：超级用户使用的比较高级的管理程序和系统守护程序。
    - `/usr/lib`: User related libraries.
    - `/usr/local`: **Locally installed software** that is not part of the base operating system.
    - `/usr/src`：内核源代码默认的放置目录。

  - Note 重要：app that is not part of the base OS can be installed in:
    - `/usr/local`
    - `/opt`

- Process required

  - `/var`: **Variable** data, most notably **log** files.
    - `/var/log`: Log files
  - `/proc`: Provides info about **running processes**.
  - `/srv`: Contains **data** which is **served by the system**.
    - `/srv/www`: Web server files.
    - `/srv/ftp`: FTP files.

- Account and User

  - `/home`: **Home** directories.
  - `/root`: The home directory for the root account.

- External file management

  - `/dev`: **Device** files, typically controlled by the operating system and the system administrators.
  - `/media`: Used to **mount removable media** (CD-ROMs, USBs)
  - `/mnt`: Used to **mount external file systems**.
  - `/export`: **Shared file** systems.
  - `/tmp`: Temporary space, typically cleared on reboot.

- Security
  - `/cgroup`: **Control Groups** hierarchy.
  - `/lost+found`:| Used by the file system to **store recovered files** after a file system check.
  - `/selinux`: Used to display information about **SELinux**.

---

## Application Directory Structures

- Some application are not bundle with the Linux distro, meaning that they have their own application directory structure.

  - e.g., install crashplan

    - program files are installed into the path `/user/local/crashplan/`
    - `/usr/local/crashplan/bin`: program binary file
    - `/usr/local/crashplan/etc`: program configuration files
    - `/usr/local/crashplan/lib`: program library files
    - `/usr/local/crashplan/log`: program log files

- Can use companay or organization name as prefiex

  - e.g.,`/opt/acme`: acme is the company name
    - `/opt/acme/bin`
    - `/opt/acme/etc`
  - e.g.,
    - `/opt/google`
    - `/opt/google/chrome`
    - `/opt/google/earth`

- If a program not bundled with a Linux distro can get installed into `/opt`, it can have its own dir structure.
  - e.g., install program `avg`
    - `/opt/avg/bin`
    - `/opt/avg/etc`
    - `/opt/avg/lib`
    - `/opt/avg/log`
- e.g., exmaple of app dir structure:

  - `/opt/myapp/bin`: program binary files
  - `/opt/myapp/lib`: program lib
  - `/etc/opt/myapp`: configuration files
  - `/var/opt/myapp`: program log

- might not have their own dir structure, but using a **shared manner**
  - `/usr/local/bin/myapp`: binary
  - `/usr/local/etc/myapp.conf`: config
  - `/usr/local/lib/libmyspp.so`: lib

---

[TOP](#linux---directory)
