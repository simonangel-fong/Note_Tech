# Linux - Storage: Partition

[Back](../../index.md)

- [Linux - Storage: Partition](#linux---storage-partition)
  - [Partition](#partition)
    - [Types of Partitions](#types-of-partitions)
    - [Partitioning Schemes](#partitioning-schemes)
    - [Thin Provisioning](#thin-provisioning)
    - [Geting Disk Device Info](#geting-disk-device-info)
  - [Configuration File](#configuration-file)
    - [`/etc/mtab`](#etcmtab)
    - [`/proc/partitions`](#procpartitions)
  - [Common Commands](#common-commands)
    - [`parted`: Manage Partitions](#parted-manage-partitions)
    - [Lab: Create new parition](#lab-create-new-parition)
    - [`fdisk`: Manage Partitions](#fdisk-manage-partitions)
    - [`mkfs`: Format a partition](#mkfs-format-a-partition)
    - [`mount`: Attach a Filesystem](#mount-attach-a-filesystem)
  - [Lab: Create and Attach a New Partition](#lab-create-and-attach-a-new-partition)
    - [Add the New Disk to the VM](#add-the-new-disk-to-the-vm)
    - [Identify the New Disk in Linux](#identify-the-new-disk-in-linux)
    - [Partition the New Disk](#partition-the-new-disk)
    - [Create a Filesystem](#create-a-filesystem)
    - [Mount the New Partition](#mount-the-new-partition)
    - [Persist the Mount in `/etc/fstab`](#persist-the-mount-in-etcfstab)
  - [Lab: Unmount an Existing Partition](#lab-unmount-an-existing-partition)
  - [Lab: Mount all partition mentioned in `/etc/fstab`](#lab-mount-all-partition-mentioned-in-etcfstab)

---

## Partition

- `Partition`

  - a **logical division** of a **physical storage device** (e.g., a hard disk or SSD).
  - allows a single physical disk to be **divided into separate sections**, each **functioning as an independent unit** for organizing data.
    - can exist on a portion of a disk, on an entire disk, or it may span **multiple** disks.

- Benefits:

  - To **separate** the operating **system**, user **data**, and application **files**.
  - To install **multiple operating systems** on a single disk.
  - To optimize performance by **allocating** specific partitions for **swap** or **log** files.
  - To **enable different filesystem types** for different purposes.

- `Partitioning information`
  - stored at special disk locations that the system **references at boot time**.

---

### Types of Partitions

- `Primary Partition`:
  - A disk can have up to **4** primary partitions.
  - Each primary partition can **directly hold data** or an **operating system**.
- `Extended Partition`:
  - A special type of primary partition that can **contain multiple logical partitions**.
  - Used to overcome the 4-partition limit.
- **Logical Partition**:
  - **Sub-partitions** within an `extended partition`.
  - Can be used for additional filesystems, swap space, etc.

---

### Partitioning Schemes

- `MBR (Master Boot Record)`:
  - **Older** partitioning scheme, **supports up to 4** `primary partitions`.
  - **Maximum** disk size: **2 TB.**
- `GPT (GUID Partition Table)`:
  - **Modern** scheme, supports **unlimited** partitions (typically **128 by default**).
  - Handles disks **larger than 2 TB**.

---

### Thin Provisioning

- `Thin provisioning` technology
  - allows for an economical allocation and utilization of storage space by moving arbitrary data blocks to contiguous locations, which **results in empty block elimination**.

---

- **Partition Files**

  - `Partitions` are **represented as special files** in Linux:
  - e.g.,
    - `/dev/sda1` - First partition on the first disk.
    - `/dev/sdb2` - Second partition on the second disk.

- Commands

  - `fdisk`: For MBR disks.
  - `parted`: For both MBR and GPT disks.
  - `lsblk`: To view partition layout.

- **Partition Lifecycle**

  - **Create**: Use `fdisk` or `parted` to define partitions.
  - **Format**: **Apply** a filesystem (`mkfs.ext4`, `mkfs.xfs`).
  - **Mount**: **Attach** the partition to the system's directory structure (`mount /dev/sda1 /mnt`).

- Common Partitions
  - `Root Partition (/)`: Contains the operating system files.
  - `Boot Partition (/boot)`: Contains boot loader files
  - `Swap Partition`: Acts as virtual memory.
  - `Home Partition (/home)`: Stores user-specific data.

---

### Geting Disk Device Info

| CMD         | DESC                                                    |
| ----------- | ------------------------------------------------------- |
| `lsblk`     | List all block devices, including disks and partitions. |
| `fdisk -l`  | List disks and partitions.                              |
| `parted -l` | List disks and partitions.                              |
| `blkid`     | Get UUIDs and filesystem types for all devices.         |
| `df -h`     | Display disk space usage of mounted filesystems         |

---

## Configuration File


### `/etc/mtab`

- `/etc/mtab`

  - `Mount Table`
  - dynamically records all currently mounted filesystems and their details.
  - Provides information about active mounts on the system.
  - Includes mounts **not listed** in `/etc/fstab`, such as temporary or user-specific mounts.

- **Structure**
  - Each line in /etc/mtab **represents a mounted filesystem with details** similar to /etc/fstab, but **dynamically** updated.

| Field           | Description                          |
| --------------- | ------------------------------------ |
| `Device`        | Mounted device or remote filesystem. |
| `Mount Point`   | Where the filesystem is mounted.     |
| `FS Type`       | The type of filesystem.              |
| `Mount Options` | Options used for the mount.          |

- Example

```conf
/dev/sda1 /     ext4  rw,relatime       0   0
/dev/sda2 /home ext4  rw,relatime       0   0
tmpfs     /tmp  tmpfs rw,nosuid,nodev   0   0
```

---

### `/proc/partitions`

- `/proc/partitions`:

  - contains partition block allocation information.

- Sample

```conf
major minor  #blocks  name

 259        0   20971520 nvme0n1
 259        1     614400 nvme0n1p1
 259        2    1048576 nvme0n1p2
 259        3   19306496 nvme0n1p3
 253        0   17207296 dm-0
 253        1    2097152 dm-1
   8        0    1048576 sda
   8        1      97280 sda1
```

---

## Common Commands

### `parted`: Manage Partitions

- `parted`

  - **disk partitioning tool** used to create, modify, delete, and manage partitions on a disk.
  - supports both `MBR` and `GPT` schemes
  - supports to create up to 128 partitions on a single GPT disk.

- Common Partition table type:

  - `gpt`: provides support for GUID partition tables;
  - `msdos`: provides support for DOS-style MBR partition tables;

- Common Flags
  - `boot` :Marks the partition as bootable.
  - `esp`: Marks an EFI System Partition (for UEFI boot).
  - `lvm` Indicates the partition is used by LVM (Logical Volume Manager).
  - `swap`: Marks the partition as swap space.
  - `raid`: Marks the partition as part of a RAID array.
  - `hidden`： Hides the partition from the OS.
  - `msftres`: Microsoft Reserved Partition (for Windows).

| Subcommands                                        | Description                                              |
| -------------------------------------------------- | -------------------------------------------------------- |
| `parted /dev/sda`                                  | Start Interactive Mode                                   |
| `parted /dev/sda print`                            | Displays the partition table                             |
| `parted /dev/sda mklabel gpt`                      | Create a new disklabel. Common labels are gpt and msdos. |
| `parted /dev/sda mkpart part_name 1MiB 10GiB`      | Create a New Partition.                                  |
| `parted /dev/sda mkpart part_name ext4 1MiB 10GiB` | Create a New Partition with filesystem.                  |
| `parted /dev/sda name part_num part_name`          | Assigns a name to a partition                            |
| `parted /dev/sda resizepart 1 15GiB`               | Resize a Partition                                       |
| `pparted /dev/sdX set part_num lvm on/off`         | Set a flags                                              |
| `parted /dev/sda rm 1`                             | Delete a Partition                                       |

### Lab: Create new parition

- Assign label

```sh
# sda is the new disk
lsblk
# NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
# sda             8:0    0    1G  0 disk
# nvme0n1       259:0    0   20G  0 disk
# ├─nvme0n1p1   259:1    0  600M  0 part /boot/efi
# ├─nvme0n1p2   259:2    0    1G  0 part /boot
# └─nvme0n1p3   259:3    0 18.4G  0 part
#   ├─rhel-root 253:0    0 16.4G  0 lvm  /
#   └─rhel-swap 253:1    0    2G  0 lvm  [SWAP]

# view the current partition, error: unrecognised disk label
parted sda print
# Error: /dev/sda: unrecognised disk label
# Model: ATA VMware Virtual S (scsi)
# Disk /dev/sda: 1074MB
# Sector size (logical/physical): 512B/512B
# Partition Table: unknown
# Disk Flags:

# assign label
parted /dev/sda mklabel msdos
# Information: You may need to update /etc/fstab

# Confirm
parted /dev/sda print
# Model: ATA VMware Virtual S (scsi)
# Disk /dev/sda: 1074MB
# Sector size (logical/physical): 512B/512B
# Partition Table: msdos
# Disk Flags:

# Number  Start  End  Size  Type  File system  Flags
```

- Create primary partition with a size of 100mb

```sh
parted /dev/sda mkpart primary 1mb 101mb
# Information: You may need to update /etc/fstab.

# confirm
parted /dev/sda print
# Model: ATA VMware Virtual S (scsi)
# Disk /dev/sda: 1074MB
# Sector size (logical/physical): 512B/512B
# Partition Table: msdos
# Disk Flags:

# Number  Start   End    Size    Type     File system  Flags
#  1      1049kB  101MB  99.6MB  primary

lsblk
# NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
# sda             8:0    0    1G  0 disk
```

- Delete a partition

```sh
# display table before deleting
parted /dev/sda print
# Model: ATA VMware Virtual S (scsi)
# Disk /dev/sda: 1074MB
# Sector size (logical/physical): 512B/512B
# Partition Table: msdos
# Disk Flags:

# Number  Start   End    Size    Type     File system  Flags
#  1      1049kB  101MB  99.6MB  primary

# delete
parted /dev/sda rm 1
# Information: You may need to update /etc/fstab.

# confirm
parted /dev/sda print
# Model: ATA VMware Virtual S (scsi)
# Disk /dev/sda: 1074MB
# Sector size (logical/physical): 512B/512B
# Partition Table: msdos
# Disk Flags:

# Number  Start  End  Size  Type  File system  Flags

```

---

### `fdisk`: Manage Partitions

- `fdisk`

  - **disk partitioning tool** used to create, modify, delete, and manage partitions on a disk.

- **Precautions**
  - **Data Loss**:
    - Modifying partitions can result in data loss. Always back up important data before using fdisk.
  - **Check Disk Details**:
    - Use `lsblk` or `fdisk -l` to verify the correct device before making changes.
  - **Partition Table Updates**:
    - Changes take effect only after writing (w) in fdisk.

| CMD                                 | DESC                                                       |
| ----------------------------------- | ---------------------------------------------------------- |
| `lsblk`                             | Display block devices and their partitions in a tree view. |
| `lsblk -f`                          | Display partitions with file system type.                  |
| `blkid`                             | Display UUIDs and file system types for all partitions.    |
| `fdisk -l`                          | Display details for all disks                              |
| `fdisk -l /dev/sda`                 | View partition details of a specific disk                  |
| `fdisk /dev/sda`                    | Open a specific disk for editing in Interactive Mode       |
| `parted /dev/sdX`                   | Open a specific disk for editing in Interactive Mode       |
| `parted /dev/sdX resizepart 1 5GiB` | Resize a Partition                                         |

- **`fdisk` Interactive Mode Commands**

| Command | Description                           |
| ------- | ------------------------------------- |
| `m`     | Display a list of available commands. |
| `p`     | Display the current partition table.  |
| `n`     | **Create a new** partition.           |
| `d`     | **Delete** an existing partition.     |
| `t`     | **Change** the type of a partition.   |
| `w`     | **Write changes** to the disk.        |
| `q`     | Quit without saving changes.          |

---

### `mkfs`: Format a partition

- `mkfs`

  - used to **create and format** a filesystem on a storage device or partition

- **Supported Filesystems**

| CMD          | filesystem                              |
| ------------ | --------------------------------------- |
| `mkfs.ext4`  | ext4                                    |
| `mkfs.xfs`   | xfs                                     |
| `mkfs.vfat`  | FAT32 (for compatibility with Windows). |
| `mkfs.ntfs`  | NTFS (requires the ntfs-3g package).    |
| `mkfs.btrfs` | Btrfs                                   |

- Common Commands

| CMD                             | DESC                                                    |
| ------------------------------- | ------------------------------------------------------- |
| `mkfs -t xfs /dev/sdb1`         | Specify the type of filesystem to create                |
| `mkfs.ext4 -L mydata /dev/sdb1` | Label the Filesystem                                    |
| `mkfs.ext4 -b 4096 /dev/sdb1`   | Specify Block Size                                      |
| `mkfs.ext4 -v /dev/sdb1`        | Display detailed information during filesystem creation |
| `mkfs.ext4 -c /dev/sdb1`        | Check for Bad Blocks                                    |

---

### `mount`: Attach a Filesystem

- `mount`

  - **attaches** a **filesystem** to a **directory** (the **mount point**) in the Linux file hierarchy.
  - Once mounted, the data stored on the device **can be accessed** as part of the Linux filesystem.

- `umount`

  - **detaches** a mounted filesystem from the directory structure, ensuring no processes are using it.

- `mount point`
  - a directory or file that **makes** a new file system, directory, or file **accessible**.

| CMD                                    | DESC                                                        |
| -------------------------------------- | ----------------------------------------------------------- |
| `mount`                                | View All Mounted Filesystems                                |
| `mount -a`                             | Mount all filesystems mentioned in `fstab`                  |
| `mount /dev/sdb1 /mnt`                 | Mounts the partition /dev/sdb1 to the directory /mnt        |
| `mount -t ext4 /dev/sdb1 /mnt`         | Mount a Filesystem with a Specific Type                     |
| `mount -o ro /dev/sdb1 /mnt`           | Mounts the partition as read-only.                          |
| `mount -o loop /path/to/file.iso /mnt` | Temporary mounts an ISO file as a loopback device.          |
| `mount /mnt`                           | Mount a Filesystem Using /etc/fstab                         |
| `umount /mnt`                          | Unmount Using Mount Point                                   |
| `umount /dev/sdb1`                     | Unmount Using Device                                        |
| `umount -f /mnt`                       | Forces the unmount if the filesystem is busy.               |
| `umount -l /mnt`                       | Detaches the filesystem but waits for any pending processes |

---

## Lab: Create and Attach a New Partition

### Add the New Disk to the VM

- Scenario: running out of space, additional space is required
- For VM, add a 2GB new disk(IDE).

---

### Identify the New Disk in Linux

```sh
lsblk
# NAME                   MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
# sda                      8:0    0   2G  0 disk
# nvme0n1                259:0    0  30G  0 disk
# ├─nvme0n1p1            259:1    0   1G  0 part /boot
# └─nvme0n1p2            259:2    0  29G  0 part
#   ├─rhel_rhelhost-root 253:0    0  26G  0 lvm  /
#   └─rhel_rhelhost-swap 253:1    0   3G  0 lvm  [SWAP]

fdisk -l
# Disk /dev/nvme0n1: 30 GiB, 32212254720 bytes, 62914560 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0xed2f4154

# Device         Boot   Start      End  Sectors Size Id Type
# /dev/nvme0n1p1 *       2048  2099199  2097152   1G 83 Linux
# /dev/nvme0n1p2      2099200 62914559 60815360  29G 8e Linux LVM


# Disk /dev/sda: 2 GiB, 2147483648 bytes, 4194304 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes


# Disk /dev/mapper/rhel_rhelhost-root: 26 GiB, 27913093120 bytes, 54517760 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes


# Disk /dev/mapper/rhel_rhelhost-swap: 3 GiB, 3221225472 bytes, 6291456 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
```

> Note: the /dev/sda is the new device.

---

### Partition the New Disk

```sh
# Open fdisk for the New Disk in the interactive mode
fdisk /dev/sda
# Welcome to fdisk (util-linux 2.32.1).
# Changes will remain in memory only, until you decide to write them.
# Be careful before using the write command.

# Device does not contain a recognized partition table.
# Created a new DOS disklabel with disk identifier 0xca628ef4.

# Command (m for help):

# ---------------------------

# m for help
m
# Help:

#   DOS (MBR)
#    a   toggle a bootable flag
#    b   edit nested BSD disklabel
#    c   toggle the dos compatibility flag

#   Generic
#    d   delete a partition
#    F   list free unpartitioned space
#    l   list known partition types
#    n   add a new partition
#    p   print the partition table
#    t   change a partition type
#    v   verify the partition table
#    i   print information about a partition

#   Misc
#    m   print this menu
#    u   change display/entry units
#    x   extra functionality (experts only)

#   Script
#    I   load disk layout from sfdisk script file
#    O   dump disk layout to sfdisk script file

#   Save & Exit
#    w   write table to disk and exit
#    q   quit without saving changes

#   Create a new label
#    g   create a new empty GPT partition table
#    G   create a new empty SGI (IRIX) partition table
#    o   create a new empty DOS partition table
#    s   create a new empty Sun partition table


# Command (m for help):
# ---------------------------
# n   add a new partition
n
# Partition type
#    p   primary (0 primary, 0 extended, 4 free)
#    e   extended (container for logical partitions)
# ---------------------------
# p to create a primary partition
p
# Partition number (1-4, default 1):enter
# First sector (2048-4194303, default 2048):enter
# Last sector, +sectors or +size{K,M,G,T,P} (2048-4194303, default 4194303):enter
#
# Created a new partition 1 of type 'Linux' and of size 2 GiB.
# ---------------------------
# w   write table to disk and exit
w
# The partition table has been altered.
# Calling ioctl() to re-read partition table.
# Syncing disks.
# ---------------------------


# confirm
lsblk
# NAME                   MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
# sda                      8:0    0   2G  0 disk
# └─sda1                   8:1    0   2G  0 part
# nvme0n1                259:0    0  30G  0 disk
# ├─nvme0n1p1            259:1    0   1G  0 part /boot
# └─nvme0n1p2            259:2    0  29G  0 part
#   ├─rhel_rhelhost-root 253:0    0  26G  0 lvm  /
#   └─rhel_rhelhost-swap 253:1    0   3G  0 lvm  [SWAP]

fdisk -l
# Disk /dev/nvme0n1: 30 GiB, 32212254720 bytes, 62914560 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0xed2f4154

# Device         Boot   Start      End  Sectors Size Id Type
# /dev/nvme0n1p1 *       2048  2099199  2097152   1G 83 Linux
# /dev/nvme0n1p2      2099200 62914559 60815360  29G 8e Linux LVM


# Disk /dev/sda: 2 GiB, 2147483648 bytes, 4194304 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0xca628ef4

# Device     Boot Start     End Sectors Size Id Type
# /dev/sda1        2048 4194303 4192256   2G 83 Linux


# Disk /dev/mapper/rhel_rhelhost-root: 26 GiB, 27913093120 bytes, 54517760 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes


# Disk /dev/mapper/rhel_rhelhost-swap: 3 GiB, 3221225472 bytes, 6291456 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
```

> Note: a new partition `sda1` has been created within the device `sda`

---

### Create a Filesystem

```sh
# makes an XFS filesystem on the new device
mkfs.ext4 /dev/sda1
# mke2fs 1.45.6 (20-Mar-2020)
# Creating filesystem with 524032 4k blocks and 131072 inodes
# Filesystem UUID: a62ee1c5-9e09-48ed-8671-0723f8899601
# Superblock backups stored on blocks:
#         32768, 98304, 163840, 229376, 294912

# Allocating group tables: done
# Writing inode tables: done
# Creating journal (8192 blocks): done
# Writing superblocks and filesystem accounting information: done
```

---

### Mount the New Partition

```sh
# Create a Mount Point
mkdir /data
ll -d /data
# drwxr-xr-x. 2 root root 6 Dec 19 20:25 /data

# Mount the Partition
mount /dev/sda1 /data

# confirm
df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.5M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.3G   19G  28% /
# /dev/nvme0n1p1                 1014M  362M  653M  36% /boot
# tmpfs                           364M   12K  364M   1% /run/user/42
# tmpfs                           364M  4.0K  364M   1% /run/user/1001
# /dev/sda1                       2.0G   24K  1.9G   1% /data
```

> Note: partition `/dev/sda1` has been mounted on the `/data`

---

### Persist the Mount in `/etc/fstab`

- Edit /etc/fstab

```sh
# Edit /etc/fstab
# add an entry for the new partition
vi /etc/fstab
# append the entry
# partition         mount point   fs type
# /dev/sda1         /data         ext4         defaults      0       0


# Test the /etc/fstab configuration without rebooting:
mount -a
```

- Reboot to verify

```sh
# reboot and confirm
reboot

df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.6M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.3G   19G  28% /
# /dev/nvme0n1p1                 1014M  362M  653M  36% /boot
# /dev/sda1                       2.0G   24K  1.9G   1% /data
# tmpfs                           364M   12K  364M   1% /run/user/42
# tmpfs                           364M  4.0K  364M   1% /run/user/1001
```

---

## Lab: Unmount an Existing Partition

- Unmount `/dev/sda1`

```sh
su -

df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.6M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.3G   19G  28% /
# /dev/nvme0n1p1                 1014M  362M  653M  36% /boot
# /dev/sda1                       2.0G   24K  1.9G   1% /data
# tmpfs                           364M   12K  364M   1% /run/user/42
# tmpfs                           364M  4.0K  364M   1% /run/user/1001

# unmount a partition from a mount point
umount /data

# confirm
df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.5M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.3G   19G  28% /
# /dev/nvme0n1p1                 1014M  362M  653M  36% /boot
# tmpfs                           364M   12K  364M   1% /run/user/42
# tmpfs                           364M  4.0K  364M   1% /run/user/1001
```

---

## Lab: Mount all partition mentioned in `/etc/fstab`

```sh
df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.5M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.3G   19G  28% /
# /dev/nvme0n1p1                 1014M  362M  653M  36% /boot
# tmpfs                           364M   12K  364M   1% /run/user/42
# tmpfs                           364M  4.0K  364M   1% /run/user/1001

#  mount all
mount -a

# confirm
df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.5M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.3G   19G  28% /
# /dev/nvme0n1p1                 1014M  362M  653M  36% /boot
# tmpfs                           364M   12K  364M   1% /run/user/42
# tmpfs                           364M  4.0K  364M   1% /run/user/1001
# /dev/sda1                       2.0G   24K  1.9G   1% /data
```

---
