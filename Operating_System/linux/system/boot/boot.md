# Linux - System: Boot Process

[Back](../../index.md)

- [Linux - System: Boot Process](#linux---system-boot-process)
  - [Boot Process](#boot-process)
    - [Stage 1: BIOS/UEFI Initialization](#stage-1-biosuefi-initialization)
      - [Components Involved](#components-involved)
      - [Tasks](#tasks)
      - [Configuration Files](#configuration-files)
    - [Stage 2: Bootloader (GRUB2) Initialization](#stage-2-bootloader-grub2-initialization)
      - [Components Involved](#components-involved-1)
      - [Tasks](#tasks-1)
      - [Congfiguration Files](#congfiguration-files)
      - [Common Commands](#common-commands)
    - [Stage 3: Kernel Initialization](#stage-3-kernel-initialization)
      - [Components Involved](#components-involved-2)
      - [Tasks](#tasks-2)
      - [Configuration Files](#configuration-files-1)
    - [Stage 4: systemd Initialization](#stage-4-systemd-initialization)
      - [Components Involved](#components-involved-3)
      - [Tasks](#tasks-3)
      - [Configuration Files](#configuration-files-2)
  - [Targets](#targets)
    - [Configuration File and Command](#configuration-file-and-command)
  - [Boot Log](#boot-log)
  - [Lab: Recover root password (RHEL 9)(using rd.break)](#lab-recover-root-password-rhel-9using-rdbreak)
    - [Overview](#overview)
    - [1. Interrupt the Boot Process](#1-interrupt-the-boot-process)
    - [2. Modify the GRUB2 Boot Parameters](#2-modify-the-grub2-boot-parameters)
    - [3. Access the Emergency Shell](#3-access-the-emergency-shell)
  - [Lab: Recover root password (RHEL 9)(using init=/bin/sh)](#lab-recover-root-password-rhel-9using-initbinsh)
    - [Modify the GRUB2 Boot Parameters](#modify-the-grub2-boot-parameters)
    - [Access the Emergency Shell](#access-the-emergency-shell)

---

## Boot Process

### Stage 1: BIOS/UEFI Initialization

- **Starts With**:
  - When **powering on** the system and the execution of the firmware (BIOS or UEFI).
- **Ends With**:

  - Transferring control to the `bootloader (GRUB2)`.

---

#### Components Involved

- **Hardware** Components:

  - CPU
  - RAM
  - Storage devices (HDD, SSD, or NVMe)
  - Network cards, peripherals, etc.

- **Firmware**:
  - `UEFI (Unified Extensible Firmware Interface)`:
    - a software program that **connects** a computer's **firmware** to its **operating system (OS)**
    - uses the `GUID Partition Table (GPT)`, which offers a more flexible solution with no size constrains
    - preferred in RHEL 9. 3
    - Faster boot time
    - Secure boot
  - `BIOS (Basic Input/Output System)`:
    - a **firmware** that initializes hardware components, like keyboard, screen, hard drives, and so on.
    - tied to the `Master Boot Record(MBR)` system, which limits disk size to 2TB
    - Legacy systems
    - Slower boot time
    - less secure boot

---

#### Tasks

- `Power-On Self-Test (POST)`:
  - to **check hardware functionality**
  - Verifies hardware integrity (CPU, memory, and storage devices).
  - Ensures that critical hardware is functioning correctly.
  - Signals issues using beep codes or diagnostic messages if errors are detected.
- **Detect and Initialize Hardware**:
  - Identifies connected hardware devices like disks, network interfaces, and peripherals.
  - Initializes basic hardware functions.
- **Search for Bootable Devices**:
  - Identifies `bootable devices` (e.g., HDD, SSD, USB, PXE network boot).
  - The boot order is determined by the firmware settings.
- **Load the `Bootloader`**:
  - **Locates** and **loads** the primary `bootloader` **into memory** from the selected boot device
    - e.g., GRUB2 stored in the MBR, GPT, or EFI system partition.
  - Hands control to the bootloader.

---

#### Configuration Files

- `UEFI` Configuration Files:

  - Location: `/boot/efi/EFI/`
  - The UEFI firmware maintains boot entries for installed operating systems and bootloaders.
  - Configuration stored in `NVRAM` (Non-Volatile RAM) for **boot options**.

- Boot Order Settings:

  - Controlled through the `BIOS/UEFI` firmware interface.
  - Boot order settings dictate the sequence of devices checked for a bootable OS.

- `GRUB Bootloader` Pointer:

  - For `UEFI` systems: GRUB resides in the `EFI system partition`
  - For `BIOS` systems: GRUB is located in the `Master Boot Record (MBR)` of the bootable disk.
    - e.g., `/boot/efi/EFI/redhat/`.

- `BIOS` Settings:
  - Configuration stored in non-volatile memory (`CMOS`).
  - Adjusted through the **BIOS setup utility** (e.g., key combinations like `Del`, `F2`, or `Esc` during boot).

---

### Stage 2: Bootloader (GRUB2) Initialization

- **Starts With**:
  - Control is handed over to the `bootloader (GRUB2)` by the BIOS/UEFI firmware.
- **Ends With**:
  - **Loading** the selected `Linux kernel` and the initial RAM disk (`initramfs`) into memory and transferring control to the kernel.

---

#### Components Involved

- `GRand Unified Bootloader (GRUB 2)`

  - allows the user to select an operating system or kernel to be loaded at system boot time.
  - also allows the user to pass arguments to the kernel.

- `GRUB2 Bootloader`:

  - The primary bootloader used in RHEL 9.
  - Installed in the `EFI system partition` (for `UEFI`) or the `Master Boot Record` (for legacy `BIOS`).

- `Initramfs(initial ram file system)`:
  - a root filesystem image that's used to boot the kernel

---

#### Tasks

1. **Load** the `Bootloader`:
   - `GRUB2` is loaded into memory by the BIOS/UEFI firmware.
2. **Display Boot Menu**:
   - GRUB2 reads its configuration file (`grub.cfg`) and displays a menu with available boot options.
   - Users can **select** the desired option or let the default boot entry load automatically.
3. **Load** the `Kernel` and `Initramfs`:
   - Loads the specified **Linux kernel** (`vmlinuz-*`) into memory.
   - Loads the `initramfs` (`initramfs-*`) into memory to initialize hardware and mount the root filesystem.
4. **Pass Boot Parameters**:
   - GRUB2 passes kernel parameters (e.g., quiet, rhgb, or custom parameters like root=) defined in grub.cfg.
5. **Transfer Control** to the Kernel:
   - GRUB2 hands over control to the Linux kernel to continue the boot process.

---

#### Congfiguration Files

- `grub.cfg`

  - the configuration file of GRUB2
  - generated during installation
  - Path:
    - **UEFI** machines: `/boot/efi/EFI/redhat/grub.cfg`
    - Traditional **BIOS-based** machines:`/boot/grub2/grub.cfg`

- `/etc/default/grub`
  - contain the simple `GRUB` options
  - parsed as a shell script

```sh
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=1G-4G:192M,4G-64G:256M,64G-:512M resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet"
GRUB_DISABLE_RECOVERY="true"
GRUB_ENABLE_BLSCFG=true
```

> `GRUB_TIMEOUT`: Time in seconds before the default entry boots.
> `GRUB_DEFAULT`: Default boot entry (0-based index or entry name).
> `GRUB_CMDLINE_LINUX`: Additional kernel parameters.

- `/etc/grub.d/`

  - a directory that contains shell scripts which generate GRUB configuration based on settings on `/etc/default/grub`
  - `grub-mkconfig` command runs these scripts to generate actual GRUB configuration.

- Don't manually edit `/boot/grub2/grub.cfg` / `/boot/efi/EFI/redhat/grub.cfg`.
  - When setting GRUB options, it actually edits `/etc/default/grub`.
  - When needs to generate additional GRUB entries or alter the entries generated, then add or change scripts in `/etc/grub.d`.

---

#### Common Commands

| CMD                                               | DECS                                                |
| ------------------------------------------------- | --------------------------------------------------- |
| `grub2-install --version`                         | Displays the GRUB2 version installed on the system. |
| `grub2-install /dev/path`                         | Installing GRUB2 Bootloader                         |
| `grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg` | Generates or updates the grub.cfg file              |
| `grub2-editenv list`                              | View GRUB Environment Variables                     |
| `grub2-set-default 1`                             | Sets the default boot entry by index or name.       |
| `grub2-editenv - unset menu_auto_hide`            | Disable GRUB menu auto-hide function                |

---

### Stage 3: Kernel Initialization

- **Start Point**:
  - GRUB2 has loaded the kernel image (vmlinuz) and the initial RAM disk (initramfs) into memory, and control is passed to the kernel.
- **End Point**:
  - The `init` (or its modern equivalent, `systemd`) process is executed.

---

#### Components Involved

- **Kernel Image** (`vmlinuz`):
  - The kernel binary starts execution.
  - Performs hardware and software initialization.
- **Initial RAM Disk** (`initramfs`):
  - A **temporary filesystem** loaded into memory during the Bootloader stage.
  - Provides essential modules and drivers required to initialize the system and mount the actual root filesystem.
- **Kernel Parameters**:
  - Passed by `GRUB2`, these parameters configure kernel behavior during initialization.
  - Example: `root=/dev/sda1`, `ro`, `quiet`.

---

#### Tasks

1. **Kernel Decompression and Initialization**:
   - The compressed `kernel image (vmlinuz)` **decompresses** itself and initializes core subsystems, including:
     - CPU and memory management.
     - Interrupt handling.
     - Device discovery.
2. **Mounting `initramfs`**:
   - The `initramfs` is mounted as a **temporary root filesystem**.
   - Drivers and tools within initramfs are used to **locate** and mount the **actual root filesystem**.
3. **Root Filesystem Mounting**:
   - The kernel uses drivers and parameters from initramfs to mount the root filesystem specified by GRUB2 (`root=/dev/sda1`).
4. **Transfer of Control** to `init/systemd`:
   - The kernel executes `/sbin/init` or `/lib/systemd/systemd`, transitioning control to **user space**.

---

#### Configuration Files

- **Kernel Image**:

  - `/boot/vmlinuz-<version>`

- **Initial RAM Disk**:

  - `/boot/initramfs-<version>.img`

- **Kernel Parameters**:
  - Defined in GRUB2's configuration
  - `/etc/default/grub`
  - e.g., `GRUB_CMDLINE_LINUX="rhgb quiet"`

---

### Stage 4: systemd Initialization

- This stage marks the transition from the **kernel space** to the **user space**.
- The systemd process (or its alternatives, like init in older systems) takes control, initializes user-space services, and sets up the operating environment.

- **Start Point**:
  - The kernel executes the first user-space program
    - `/sbin/init` or
    - `/lib/systemd/systemd`(modern replacement).
- **End Point**:
  - The system reaches the desired target
  - e.g., graphical.target for GUI, multi-user.target for CLI.

---

#### Components Involved

- `systemd`:
  - The primary **system and service manager** in RHEL 9.
  - Responsible for managing all services, mounts, sockets, timers, and targets.
- `Targets`:
  - A set of **predefined states** for the system
    - similar to `runlevels` in `SysVinit`.
  - Examples:
    - `multi-user.target`: Multi-user CLI environment.
    - `graphical.target`: Multi-user GUI environment.
    - `rescue.target`: **Single-user mode** for system repair.
- **Unit Files**:
  - Configuration files describing how systemd manages services, targets, mounts, etc.
  - Located in `/usr/lib/systemd/system/` and `/etc/systemd/system/`.

---

#### Tasks

- `systemd` **Initialization**:
  - `systemd` **reads** its configuration from `/etc/systemd/system/` and determines the **default target** (configured in `/etc/systemd/system/default.target`).
- **Mount Filesystems**:
  - Filesystems listed in `/etc/fstab` are mounted.
  - Swap partitions are activated.
- **Start Essential Services**:
  - Services required for basic operation, such as `udev` (for device management) and `networkd` (for network setup), are started.
- **Activate the Target**:
  - The **default** target (e.g., multi-user.target or graphical.target) is activated.
  - This involves starting all associated services and dependencies.

---

#### Configuration Files

- **Default Target**:
  - `/etc/systemd/system/default.target`
- **Service Unit Files**:
  - `/usr/lib/systemd/system/`: **default** system-provided units.
  - `/etc/systemd/system/`:**custom** overrides and additions.
- **System Configuration Files**:
  - `/etc/fstab`: defines filesystem mounts.
  - `/etc/systemd/system.conf` and `/etc/systemd/user.conf`: global systemd settings.

---

## Targets

- `Targets`:

  - A set of **predefined states** for the system
  - similar to `runlevels` in `SysVinit`.
    - In RHEL 7 and above, traditional `runlevels` are replaced with `systemd targets`:

  | Runlevel | SysV Equivalent     | systemd Target      |
  | -------- | ------------------- | ------------------- |
  | 0        | Halt                | `poweroff.target`   |
  | 1        | Single User Mode    | `rescue.target`     |
  | 3        | Multi-User Mode     | `multi-user.target` |
  | 5        | Graphical Interface | `graphical.target`  |
  | 6        | Reboot              | `reboot.target`     |

- dependencies:
  - graphical target depends on multi-user.target, which depends on basic target.

---

### Configuration File and Command

- CF: `/etc/systemd/system/default.target`

- Common Comand

| CMD                                      | DESC                          |
| ---------------------------------------- | ----------------------------- |
| `systemctl get-default`                  | Display the current target    |
| `systemctl set-default graphical.target` | Set default target            |
| `who -r`                                 | Display the current run-level |

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

---

## Boot Log

| CMD                | DESC                                              |
| ------------------ | ------------------------------------------------- |
| `journalctl -b`    | Shows logs from the last boot                     |
| `journalctl -b -1` | Shows logs from the previous boot                 |
| `journalctl -b -2` | Shows logs from the boot before the previous boot |

---

## Lab: Recover root password (RHEL 9)(using rd.break)

### Overview

- Recovering the root password involves **interrupting** the boot process and gaining access to a **single-user** or **rescue mode**.
- This process is associated with **Stage 2 (Bootloader Initialization)** because of **modification GRUB2** to boot into a mode that allows root access without a password.

---

### 1. Interrupt the Boot Process

- When the GRUB2 boot menu appears during startup:
  - Highlight the kernel you want to boot (usually the default one).
  - Press `e` to edit the selected boot entry.
- At this step, interact with the bootloader (GRUB2), modifying its default behavior to **enable** `single-user mode`.

---

### 2. Modify the GRUB2 Boot Parameters

- Locate the line that begins with linux (or `linux16` or `linuxefi`) and contains the kernel path (e.g., `/boot/vmlinuz`).
- At the end of this line, append: `rd.break`
  - The `rd.break` parameter interrupts the boot process and gives **access to an emergency shell before the root filesystem is mounted**.
- Alternatively: `init=/bin/sh`
- Press `Ctrl + X` or F10 to boot with the modified parameters.

---

### 3. Access the Emergency Shell

- The system boots into an emergency shell (with root access).

```sh
# Remount the Root Filesystem as Read-Write
# need write access to edit the root user's password in the system's shadow file.
mount -o remount,rw /sysroot

# Switch to the sysroot Environment
# Change the root directory to /sysroot, enabling commands to work as if the system has booted normally.
chroot /sysroot

# Reset the Root Password
# updates the root password in /etc/shadow.
passwd

# Re-label the Filesystem (SELinux Contexts)
# Create an empty file to signal SELinux to relabel files during the next boot
# SELinux enforces security contexts, and any changes to the system require relabeling to ensure proper access controls.
touch /.autorelabel

# Exit and Reboot the System
# The system will boot normally, applying the SELinux relabeling and allowing access with the new root password.
exit
reboot
```

---

## Lab: Recover root password (RHEL 9)(using init=/bin/sh)

- In RHEL 9, dracut-055-45.git20220404.el9_0 has this issue, upgrade to dracut-057-13.git20220816.el9 or later will fix this issue.
  - ref: https://access.redhat.com/solutions/6983531

---

### Modify the GRUB2 Boot Parameters

- `init=/bin/sh`

---

### Access the Emergency Shell

- The switch_root prompt appears.

```sh
# Remount the file system as writeable
mount -o remount,rw /

# Reset the root password.
passwd

# To relabel all files on the next system boot
touch /.autorelabel

# Reboot the system
/usr/sbin/reboot -f
```
