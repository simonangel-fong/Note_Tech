# Linux - Storage: Filesystem

[Back](../../index.md)

- [Linux - Storage: Filesystem](#linux---storage-filesystem)
  - [Filesystem](#filesystem)
    - [`mount` Command](#mount-command)
    - [Configure File: `/etc/fstab`](#configure-file-etcfstab)
    - [Common Filesystems Types:](#common-filesystems-types)
    - [Common Commands](#common-commands)
  - [Swap](#swap)
    - [Prioritizing Swap Spaces](#prioritizing-swap-spaces)
    - [Common Commands](#common-commands-1)
    - [Lab: Create SWAP](#lab-create-swap)

---

## Filesystem

- `filesystem`

  - a structure used to organize and store data on storage devices.
  - a logical container that stores files and directories
  - created in `logical volume`, or `Stratis pool`

- During OS installation, only two file systems are created in the default disk layout

  - and are required for installation and booting.
  - `/`
  - `/boot`

- **Storing disparate data in distinct file systems** versus **storing all data in a single file system**:

  - Make any file system accessible (mount) or inaccessible (unmount) to **users independent** of other file systems.
    - This **hides or reveals** information contained in that file system.
  - Perform file system **repair activities** on individual file systems
  - Keep dissimilar **data** in separate file systems
  - **Optimize** or **tune** each file system independently
  - **Grow** or **shrink** a file system independent of other file systems

- 3 basic groups of file systems

  - **disk-based file systems**
    - created on **physical drives** using SATA, USB, Fibre Channel, and other technologies
    - store information persistently
  - **networkbased file systems**
    - disk-based file systems shared over the network for remote access.
    - store information persistently
  - **memory-based file systems**
    - virtual;
    - they are created at system startup and destroyed when the system goes down.
    - data is not persistently saved.

---

### `mount` Command

- `mount point`

  - a desired attachment point at which a file system connected to the direcotry structure
  - any empty directory
  - e.g.,`/`, `/boot`

- A `mount point` should be **empty** when an attempt is made to mount a file system on it,
  - otherwise the content of the mount point will **hide**.
- As well, the mount point must **not be in use** or the mount attempt will fail.

- **options**

| Option          | Description                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------- |
| `acl`/`noacl`   | Enables/disables the support for ACLs                                                        |
| `auto`/`noauto` | Mounts (does not mount) the file system when the -a option is specified                      |
| `defaults`      | Mounts a file system with all the default values (async, auto, rw, etc.)                     |
| `_netdev`       | Used for a file system that requires network connectivity in place before it can be mounted. |
| `remount`       | **Remounts** an already mounted file system to enable or disable an option                   |
| `ro (rw)`       | Mounts a file system read-only (read/write)                                                  |

---

### Configure File: `/etc/fstab`

- `/etc/fstab`

  - A configuration file that defines how and where partitions, devices, and remote filesystems should be **mounted at system boot** or **manually**.
    - Automates the mounting of filesystems **at boot**.
    - Provides a convenient way to **manually mount** filesystems without specifying detailed options.

- **Structure**
  - Each line represents a filesystem and its mount configuration

| Field             | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| `Device`          | The block device or remote filesystem.                                    |
| `Mount Point`     | The directory where the filesystem will be mounted.                       |
| `Filesystem Type` | The type of filesystem (e.g., ext4, xfs, vfat, nfs).                      |
| `Options`         | Mount options (e.g., defaults, ro, noexec).                               |
| `Dump`            | Backup utility flag: 0 to skip dump or 1 to include.                      |
| `Pass`            | Filesystem check order during boot (0 to skip, 1 for root, 2 for others). |

- Example

```conf
# Device          Mount Point     FS Type     Options         Dump   Pass
/dev/sda1         /               ext4        defaults        1      1
/dev/sda2         /home           ext4        defaults        1      2
UUID=abc123       /mnt/storage    xfs         noatime         0      2
```

- Common Mount Options

  - `defaults`: Default options (rw, suid, dev, exec, auto, nouser, and async).
  - `ro`: Read-only.
  - `noatime`: Prevents updating file access times.
  - `noexec`: Prevents execution of binaries on this partition.
  - `user`: Allows non-root users to mount.

- RHEL attempts to **mount** all file systems listed in the `/etc/fstab` file at **reboots**.

---

### Common Filesystems Types:

| Filesystem types | Category | Description                                                         |
| ---------------- | -------- | ------------------------------------------------------------------- |
| `ext4`           | Disk     | Extended File System. Default traditional Linux filesystem.         |
| `xfs`            | Disk     | Default fs in RHEL 7/8/9, supports large files, better performance. |
| `vfat`           | Disk     | Used for compatibility with Windows (FAT32).                        |
| `btrfs`          | Disk     | Modern filesystem with snapshot support.                            |
| `iso9660`        | Disk     | Used for CD/DVDs.                                                   |
| `swap`           | Disk     | Used for virtual memory (swap space).                               |
| `nfs`            | Network  | Network File System for remote access                               |
| `autofs`         | Network  | NFS file system set to mount and unmount automatically              |

### Common Commands

- General File System Commands

| CMD                                     | DESC                                                  |
| --------------------------------------- | ----------------------------------------------------- |
| `blkid`                                 | List All Block Devices with Filesystem Info           |
| `blkid /dev/sdb1`                       | Display file system type and UUID.                    |
| `blkid -t UUID="uuid_number"`           | Find All Devices of a Specific Filesystem Type        |
| `blkid -t TYPE=xfs`                     | Find All Devices of a Specific Filesystem Type        |
| `blkid -t LABEL="MyPartition"`          | Find a Partition Using a Label                        |
| `df`                                    | Display Disk Space Usage                              |
| `df -h`                                 | Display Human-Readable Output                         |
| `df -h /home`                           | Display Disk Space where a Specific Directory locates |
| `df -a`                                 | Display Space for All Filesystems                     |
| `df -i`                                 | Display Inodes Instead of Disk Space                  |
| `df -Th`                                | Display Filesystem Type                               |
| `df -th ext4`                           | Display a specific Filesystem Type                    |
| `df -h -x tmpfs`                        | Exclude Certain Filesystems                           |
| `du /path/to/file`                      | Display Size of a File                                |
| `du /path/to/dir/`                      | Display Size of a Directory                           |
| `du /dir1 /dir2`                        | Display Size of multiple directories                  |
| `du -h /path/to/dir/`                   | Display Sizes in Human-Readable Format                |
| `du -ah /path/to/dir/`                  | Display Size of All Files in a Directory              |
| `du -sh /path/to/dir/`                  | Display Total Size of a Directory                     |
| `du -ah /path/to/dir/ \| sort -rh`      | Sort Files by Size                                    |
| `du -h --exclude="*.log" /path/to/dir/` | Exclude Certain File Types                            |
| `mount`                                 | Display all currently mounted file systems.           |
| `mount -t ext4`                         | Displlay file systems with specific type              |
| `mount fs_name mount_point`             | Mount a file system to a directory.                   |
| `mount -t ext4 fs_name mount_point`     | Mount with a specific file system type                |
| `mount --move olddir newdir`            | Move a mounted file system to another mount point     |
| `umount fs_name`                        | Unmount a File System                                 |
| `umount mount_point`                    | Unmount a File System                                 |

- `Extended File System(ext4)`

| CMD                          | DESC                                                 |
| ---------------------------- | ---------------------------------------------------- |
| `mkfs.ext4 /dev`             | Creates a file system on a partition/lv.             |
| `mkfs.ext4 -L "MyData" /dev` | Creates a file system with label.                    |
| `mkfs.ext4 -b 4096 /dev`     | Creates a file system with Block Size.               |
| `e2label /dev`               | Display the current label of a partition/fs          |
| `e2label /dev "MyPartition"` | Set a new label for an ext4 filesystem               |
| `tune2fs -l /dev`            | Tunes or displays file system attributes             |
| `tune2fs -m 2 /dev`          | Reduce reserved space to 2% (default is 5%)          |
| `tune2fs -L "NewLabel" /dev` | Change the filesystem label                          |
| `tune2fs -U random /dev`     | Change the UUID of the filesystem                    |
| `resize2fs /dev`             | Extend an ext4 filesystem to use all available space |
| `resize2fs /dev 10G`         | Resize an ext4 filesystem to 10GB                    |

- `X File System(XFS)`

| CMD                                            | DESC                                   |
| ---------------------------------------------- | -------------------------------------- |
| `mkfs.xfs /dev`                                | Creates a file system.                 |
| `mkfs.xfs -L "MyData" /dev/sdb1`               | Creates a file system with label.      |
| `mkfs.ext4 -b 4096 /dev/sdb1`                  | Creates a file system with Block Size. |
| `xfs_info mount_point` / `xfs_info fs_name`    | Display XFS Filesystem Info            |
| `xfs_admin -l /dev/sda1`                       | Display XFS Filesystem Attributes      |
| `xfs_admin -L "MyXFSData" /dev/sda1`           | Set a New Label                        |
| `xfs_admin -U generate /dev/sda1`              | Change the UUID                        |
| `xfs_growfs fs_name` /`xfs_growfs mount_point` | Increase XFS size                      |
| `xfs_growfs /mnt -D 500000`                    | Expand to a Specific Size              |

---

## Swap

- `Physical memory(main memory)`

  - a finite **temporary** storage resource employed for loading kernel and running user programs and applications.

- `Swap space`

  - an independent region on the **physical disk** used for **holding idle data** until it is needed.

- `pages`

  - small logical chunks into which `physical memory` is splitted
  - **mapped** their **physical locations** to **virtual locations** on the **swap** to facilitate access by system processors.

- `page table`

  - the data structure that stores the physical-to-virtual mapping of pages
  - maintained by the kernel.

- `page out`

  - the process of **moving** selected **idle pages** of data from physical memory to the swap space in an effort to make room to accommodate other programs when the free memory falls below that threshold, the system starts.

- `page in`
  - return of data to the physical memory from the swap
- `demand paging`
  - entire process of paging data out and in
- `thrashing`
  - The excessive amount of paging that affects the system performance.
  - When thrashing begins, the system **deactivates** idle processes and **prevents** new processes from being launched.

---

### Prioritizing Swap Spaces

- **Multiple** swap areas can be configured and activated to meet the workload demand.
  - The **default behavior** of RHEL is to use the **first** activated swap area and move on to the next when the first one is exhausted.
- The system allows us to **prioritize** one area over the other by adding the **option “pri”** to the swap entries in the `fstab` file.
  - This flag supports a value between `-2` and `32767` with `-2` being the **default**.
  - A **higher** value of “pri” sets a **higher priority** for the corresponding swap region.
  - For swap areas with an identical priority, the system alternates between them。

---

### Common Commands

| CMD                                | DESC                                                                   |
| ---------------------------------- | ---------------------------------------------------------------------- |
| `free -h`                          | Display Memory Usage in Human-Readable Format                          |
| `free -h -s 2`                     | Display Memory Continuously (Refresh Every 2 Seconds)                  |
| `free -h -s2 -c3`                  | Display Memory Continuously (Refresh Every 2 Seconds, repeate 3 times) |
| `free -m \| grep Swap`             | Display swap space                                                     |
| `mkswap /dev/sdb1`                 | Create a Swap Partition                                                |
| `mkswap -L "lable_name" /dev/sdb1` | Create a Swap Partition with a label                                   |
| `mkswap -c /dev/sdb1`              | Create a Swap Partition and check bad blocks                           |
| `swapon`                           | Displays all currently active swap spaces                              |
| `swapon -a`                        | Enables all swap entries in the `/etc/fstab`                           |
| `swapon -p 3 /dev/sdb1`            | Define a priority level for the swap space.                            |
| `swapoff /dev/sdb1`                | Disable a Swap Partition                                               |
| `swapoff -a`                       | Disable All Swap                                                       |

---

### Lab: Create SWAP

```sh
# create partition
parted /dev/sda print
# Model: ATA VMware Virtual S (scsi)
# Disk /dev/sda: 1074MB
# Sector size (logical/physical): 512B/512B
# Partition Table: gpt
# Disk Flags:

# Number  Start   End    Size   File system  Name  Flags
#  1      1049kB  512MB  511MB               main

parted /dev/sda mkpart primary 513 1024
# Information: You may need to update /etc/fstab.

parted /dev/sda print
# Model: ATA VMware Virtual S (scsi)
# Disk /dev/sda: 1074MB
# Sector size (logical/physical): 512B/512B
# Partition Table: gpt
# Disk Flags:
#
# Number  Start   End     Size   File system  Name     Flags
#  1      1049kB  512MB   511MB               main
#  2      513MB   1024MB  512MB               primary

# confirm
lsblk /dev/sda2
# NAME MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
# sda2   8:2    0  488M  0 part

# create swap from partition
mkswap /dev/sda2
# Setting up swapspace version 1, size = 488 MiB (511700992 bytes)
# no label, UUID=8bdc174a-93e8-4abf-8771-2bcf90fcc6ab

# confirm
 lsblk -f /dev/sda2
# NAME FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
# sda2 swap   1           8bdc174a-93e8-4abf-8771-2bcf90fcc6ab

# add entry to fstab
echo "UUID=8bdc174a-93e8-4abf-8771-2bcf90fcc6ab swap    swap    pri=1   0   0" >> /etc/fstab

# display current swap size
swapon
# NAME      TYPE      SIZE USED PRIO
# /dev/dm-1 partition   2G   0B   -2

# activate new swap
swapon -a

# confirm
swapon
# NAME      TYPE      SIZE USED PRIO
# /dev/dm-1 partition   2G   0B   -2
# /dev/sda2 partition 488M   0B    1

free -ht
#                total        used        free      shared  buff/cache   available
# Mem:           1.7Gi       953Mi       243Mi        12Mi       716Mi       790Mi
# Swap:          2.5Gi          0B       2.5Gi
# Total:         4.2Gi       953Mi       2.7Gi

# deactivate swap
swapoff /dev/sda2

# confirm
swapon
# NAME      TYPE      SIZE USED PRIO
# /dev/dm-1 partition   2G   0B   -2

# change the priority
# deactivate swap
swapoff /dev/sda2

# change priority
swapon -p 3 /dev/sda2

# activate swap
swapon -a

# confirm
swapon
# NAME      TYPE      SIZE USED PRIO
# /dev/dm-1 partition   2G   0B   -2
# /dev/sda2 partition 205M   0B    3
```
