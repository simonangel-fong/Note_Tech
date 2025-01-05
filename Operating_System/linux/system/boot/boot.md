# Linux - System: !Boot Process

[Back](../../index.md)

- [Linux - System: !Boot Process](#linux---system-boot-process)
  - [Terminologies](#terminologies)
  - [Boot Process](#boot-process)
    - [1. BIOS/UEFI Initialization](#1-biosuefi-initialization)
    - [2. BootLoader Stage (GRUB2)](#2-bootloader-stage-grub2)
    - [3. Kernel Initialization](#3-kernel-initialization)
    - [4. Initramfs/Initial RAM Disk](#4-initramfsinitial-ram-disk)
    - [5. Systemd Initialization](#5-systemd-initialization)
  - [Stages of the Boot Process](#stages-of-the-boot-process)
    - [1. BIOS/UEFI Stage](#1-biosuefi-stage)
    - [2. Bootloader Stage](#2-bootloader-stage)
    - [3. Kernel Stage](#3-kernel-stage)
    - [4. Systemd Stage](#4-systemd-stage)
  - [Runlevels and Targets](#runlevels-and-targets)

---

## Terminologies

- `BIOS (Basic Input/Output System)`

  - a **firmware** that initializes hardware components, like keyboard, screen, hard drives, and so on.
  - tied to the `Master Boot Record(MBR)` system, which limits disk size to 2TB.
  - Slower boot time
  - less secure boot

- `UEFI (Unified Extensible Firmware Interface)`

  - a software program offering faster boot times and better security features compared to the `BIOS`
  - uses the `GUID Partition Table (GPT)`, which offers a more flexible solution with no size constrains
  - Faster boot time
  - Secure boot

- `bootloader`

  - a program that loads a computer's operating system (OS) into memory when the computer starts up or restarts

- `Master Boot Record (MBR)`
  - the information in the first sector of a hard disk or a removable drive, responsible for loading the operating system (OS) when the computer is turned on.

- `GUID Partition Table (GPT)`
  - a standard for organizing the layout of partition tables on physical storage devices, such as hard disk drives and solid-state drives

- `initramfs (initial ram file system)`
  - a set of tools and scripts that prepares a Linux system for boot
  - loads the necessary kernel modules and drivers to mount file systems like `/usr` or `/var`.


---

## Boot Process

### 1. BIOS/UEFI Initialization

- When the system **powers on**, the `Basic Input/Output System (BIOS)` or `Unified Extensible Firmware Interface (UEFI)` **initializes**.
- **Jobs:**
  - Performs `POST (Power-On Self-Test)` to check hardware components.
  - Locates and loads the boot loader from the `Master Boot Record (MBR)` or `GPT (GUID Partition Table)`.

---

### 2. BootLoader Stage (GRUB2)

- The `boot loader`, typically `GRUB2 (Grand Unified Bootloader v2)`, **takes over** after BIOS/UEFI.
- Jobs:
  - Displays a **menu to select the operating system or kernel**.
  - Allows passing kernel parameters if needed.
  - **Loads** the selected `kernel` and `initramfs (initial RAM filesystem)` into memory.
- Key Files:
  - `GRUB` configuration file: `/boot/grub2/grub.cfg`.
  - `Kernel`: `/boot/vmlinuz-_`.
  - `Initramfs`: `/boot/initramfs-_`.

---

### 3. Kernel Initialization

- The Linux `kernel` is **loaded into memory** and executed.
- Jobs:
  - Initializes **hardware drivers**.
  - **Mounts** the `root filesystem` specified by GRUB.
  - Starts the `init process (PID 1)` from systemd.
- Key Files:
  - The kernel file and associated modules in `/lib/modules/`.

---

### 4. Initramfs/Initial RAM Disk

- A **temporary root filesystem** that contains tools and drivers needed to **initialize the real root filesystem**.
- Jobs:
  - Detects and initializes hardware needed for boot.
  - Prepares and **mounts the real root filesystem**.

---

### 5. Systemd Initialization

- The `init process (systemd)` takes control as the first process (PID 1).
- Jobs:
  - Initializes the rest of the system by activating units (services, mount points, sockets, etc.).
    Reads configuration files from /etc/systemd/system/ and /usr/lib/systemd/system/.
    Key Commands:
    systemctl: To manage systemd units.
    journalctl: To view logs.

1. Target Initialization
   Description: Systemd moves the system through various targets (equivalent to runlevels in older systems).
   Functions:
   Sets up a basic system environment.
   Activates multi-user mode, graphical interfaces, or other specific targets.
   Common Targets:
   basic.target: Minimal setup.
   multi-user.target: Full CLI environment.
   graphical.target: GUI environment.

## Stages of the Boot Process

- Boot sequence changes in `CentOS/Redhat 7` and above.
- `CentOS/Redhat 7` uses the service manager `systemd` to manage the boot sequence.
  - Previous versions like `RHEL 6` use `Sysv init scripts`.

---

### 1. BIOS/UEFI Stage

- Starts when the **power button** is pressed to turn on the machine
- Component: `BIOS`/`UEFI`
- Jobs:
  - performs `POST (Power-On Self-Test)` to **check hardware functionality**.
  - Searches for a **boot device** (disk, network, etc.) and `bootloader` software.

---

### 2. Bootloader Stage

- Starts when `BIOS`/`UEFI` find the Boot device and `bootloader`
- Component: `bootloader`
- Common bootloader:
  - `GRUB 2 (GRand Unified Bootloader v2)`(used in RHEL 7 and later)
  - `LILO(Linux loader)`(outdated)
- **Job:**
  - Locate the operating system kernel on the disk
  - Load the kernel into computer's memory
  - Start running the kernel code.
  - Displays the **boot menu**, allowing users to **select** a kernel or operating system.
  - **Loads** the selected `kernel` and the `initramfs (initial RAM filesystem)` into memory.

```sh
grub2-editenv - unset menu_auto_hide
```

---

### 3. Kernel Stage

- When the kernel is loaded into the memory and take control of the startup process.
- Component: `kernel`
- **Jobs**
  - Load itself into the memory
  - Check the hardware
  - Load device drivers and other kernel modules.
  - Start backgroud process.

---

### 4. Systemd Stage

- When the `init process(PID=1)` kicks off.
- Compoent: `Systemd`
  - parent of all other processes.
- Jobs:
  - Check the remaining hardware needed to be loaded.
  - Mount up all file systems and disk.
  - Launch all the background services
  - Handle user logins
  - Reads configuration from `/etc/systemd/system/default.target` and Brings the system to the desired target mode.

---

## Runlevels and Targets

- In RHEL 7 and above, traditional `runlevels` are replaced with `systemd targets`:

- CF: `/etc/systemd/system/default.target`

| Runlevel | SysV Equivalent     | systemd Target      |
| -------- | ------------------- | ------------------- |
| 0        | Halt                | `poweroff.target`   |
| 1        | Single User Mode    | `rescue.target`     |
| 3        | Multi-User Mode     | `multi-user.target` |
| 5        | Graphical Interface | `graphical.target`  |
| 6        | Reboot              | `reboot.target`     |

---

| CMD                     | DESC                          |
| ----------------------- | ----------------------------- |
| `systemctl get-default` | Display the current target    |
| `who -r`                | Display the current run-level |

- dependencies:
  - graphical target depends on multi-user.target, which depends on basic target.

```sh
systemctl list-dependencies graphical.target | grep target

# graphical.target
# ● └─multi-user.target
# ●   ├─basic.target
# ●   │ ├─paths.target
# ●   │ ├─slices.target
# ●   │ ├─sockets.target
# ●   │ ├─sysinit.target
# ●   │ │ ├─cryptsetup.target
# ●   │ │ ├─local-fs.target
# ●   │ │ └─swap.target
# ●   │ └─timers.target
# ●   ├─getty.target
# ●   ├─nfs-client.target
# ●   │ └─remote-fs-pre.target
# ●   └─remote-fs.target
# ●     └─nfs-client.target
# ●       └─remote-fs-pre.target
```

```sh
ls -al /lib/systemd/system/runlevel*
# lrwxrwxrwx. 1 root root 15 Nov  7 07:06 /lib/systemd/system/runlevel0.target -> poweroff.target
# lrwxrwxrwx. 1 root root 13 Nov  7 07:06 /lib/systemd/system/runlevel1.target -> rescue.target
# lrwxrwxrwx. 1 root root 17 Nov  7 07:06 /lib/systemd/system/runlevel2.target -> multi-user.target
# lrwxrwxrwx. 1 root root 17 Nov  7 07:06 /lib/systemd/system/runlevel3.target -> multi-user.target
# lrwxrwxrwx. 1 root root 17 Nov  7 07:06 /lib/systemd/system/runlevel4.target -> multi-user.target
# lrwxrwxrwx. 1 root root 16 Nov  7 07:06 /lib/systemd/system/runlevel5.target -> graphical.target
# lrwxrwxrwx. 1 root root 13 Nov  7 07:06 /lib/systemd/system/runlevel6.target -> reboot.target
```

- Setting the default target

```sh
systemctl set-default graphical.target
```
