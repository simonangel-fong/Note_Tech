# Linux - System: Recover Root Password

[Back](../../index.md)

- [Linux - System: Recover Root Password](#linux---system-recover-root-password)
  - [Steps to Reset the Root Password](#steps-to-reset-the-root-password)
    - [1. Reboot the System](#1-reboot-the-system)
    - [2. Interrupt the GRUB Bootloader](#2-interrupt-the-grub-bootloader)
    - [3. Modify the Boot Parameters](#3-modify-the-boot-parameters)
    - [4. Boot into Emergency Mode](#4-boot-into-emergency-mode)
    - [5. Remount the Root Filesystem](#5-remount-the-root-filesystem)
    - [6. Change the Root Password](#6-change-the-root-password)
    - [7. Relabel SELinux Contexts](#7-relabel-selinux-contexts)
    - [8. Exit and Reboot](#8-exit-and-reboot)
    - [9. Log In with the New Password](#9-log-in-with-the-new-password)
  - [Lab: Recover Root Password](#lab-recover-root-password)
  - [Lab: Repair Filesystem from corruption](#lab-repair-filesystem-from-corruption)

---

## Steps to Reset the Root Password

### 1. Reboot the System

- From the terminal or console, reboot the system:

```sh
reboot
```

---

### 2. Interrupt the GRUB Bootloader

- As the server reboots, press the `e` key at the **GRUB menu** to edit the boot entry.

---

### 3. Modify the Boot Parameters

- Use the arrow keys to navigate to the line starting with `linux` or `linux16`.
- At the end of the line, append the following:

```sh
rd.break
```

- This tells the system to **stop the boot process** before the root filesystem is **mounted**.

？？

```sh
rw init=/bin/bash
```

---

### 4. Boot into Emergency Mode

- Press `Ctrl + X` to boot with the modified parameters.

---

### 5. Remount the Root Filesystem

Once the system stops in the emergency shell, **remount** the root filesystem in **read-write mode**:

```sh
mount -o remount,rw /sysroot
```

---

### 6. Change the Root Password

Access the system's root environment:

```sh
chroot /sysroot
```

Reset the root password using the passwd command:

```sh
passwd
```

Enter and confirm the new root password.

---

### 7. Relabel SELinux Contexts

Create an autorelabel file to ensure SELinux relabels the filesystem:

```sh
touch /.autorelabel
```

---

### 8. Exit and Reboot

```sh
# Exit the chroot environment:
exit

# Exit the emergency shell:
exit
```

- The system will reboot. Allow it to relabel files, which might take some time.

---

### 9. Log In with the New Password

Once the system completes the reboot, log in as root with the new password.

---

## Lab: Recover Root Password

- Steps
  - Restart machine
  - Edit Grub file
  - Change password
  - Reboot

---

1. Restart machine
2. Select kernel and press `e` to edit

![recovery_pwd01](./pic/recovery_pwd01.png)

3. Edit the Grub file
   - Find `ro`
   - Replace with `rw init=/sysroot/bin/sh`
   - Press `Ctrl+x` to start

![recovery_pwd02](./pic/recovery_pwd02.png)

4. The machine get started into single user mode.
   - Change the current root directory to /sysroot: `chroot /sysroot`
   - Change the root password: `passwd root`
   - Update the SELinux information: `touch /.autorelabel`
   - Exit the /sysroot: `exit`
   - Reboot the machine

![recovery_pwd03](./pic/recovery_pwd03.png)
![recovery_pwd04](./pic/recovery_pwd04.png)

5. Login the system as usual.
   - SELinux might take time for relabeling.

![recovery_pwd05](./pic/recovery_pwd05.png)

---

## Lab: Repair Filesystem from corruption

- Corruption can occur when

  - making mistake in `/etc` configuration file,
  - filesystem become corrupted at the disk level.

- When corruption occurs, the `systemd` will not be able to boot the system in the defined target and bring the system in emergency mode.

  - Admin can use the emergency target to diagnose and fix the issue, because no filesystem is mounted before the emergency shell.
  - After fixing filesytem issues with `etc/fstab`, run `systemctl daemon-reload` to reload.

- Common errors

| Error                                              | Result                                                                        |
| -------------------------------------------------- | ----------------------------------------------------------------------------- |
| Corrupt file system                                | systemd trigger an automatic fix for fs. If fails, bring into emergency shell |
| Nonexistent device or UUID refered in `/etc/fstab` | System waits for the device. If unavailable, bring into emergency shell       |
| Nonexistent mount point in `/etc/fstab`            | Bring into emergency shell                                                    |
| Incorrect mount option in `/etc/fstab`             | Bring into emergency shell                                                    |

---
