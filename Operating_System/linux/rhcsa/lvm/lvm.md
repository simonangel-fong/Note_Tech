# RHCSA LVM

[Back](../../index.md)

- [RHCSA LVM](#rhcsa-lvm)
  - [Question](#question)
    - [Soluion](#soluion)
  - [Question](#question-1)
    - [Solution](#solution)
  - [Question](#question-2)
    - [Solution](#solution-1)
  - [Question](#question-3)
    - [Solution](#solution-2)

---

## Question

```conf
Create an LVM name wshare from wgroup volume group. Note the following:
PE size should be 8MB
LVM size should be 50 extents
Format with "ext4" file system and mount it under /mnt/wshare. And it should auto mount after next reboot
Exam can have filesystem - vfat, xfs
```

---

### Soluion

- Add new storage disk
- Create partition
  - careful, the following question might need the the space
  - size = PE size \* extents = 400MB

```sh
# find the new disk
lsblk
# sda             8:0    0    5G  0 disk
# nvme0n1       259:0    0   20G  0 disk
# ├─nvme0n1p1   259:1    0  600M  0 part /boot/efi
# ├─nvme0n1p2   259:2    0    1G  0 part /boot
# └─nvme0n1p3   259:3    0 18.4G  0 part
#   ├─rhel-root 253:0    0 16.4G  0 lvm  /
#   └─rhel-swap 253:1    0    2G  0 lvm  [SWAP]

# find the disk location
fdisk -l | grep sda
# Disk /dev/sda: 5 GiB, 5368709120 bytes, 10485760 sectors

# create a new partition
fdisk /dev/sda
n # to create a new partition.
p # for a primary partition
# Accept the default partition number.
# Accept the default start sector
+500M # set the end sector according to calculation
# Created a new partition 1 of type 'Linux' and of size 500 MiB.

t # change the partition type
L # to check the aliases for Linux LVM: 8e
8e # Change type to Linux LVM
# Changed type of partition 'Linux' to 'Linux LVM'.

p # confirm
# Disk /dev/sda: 5 GiB, 5368709120 bytes, 10485760 sectors
# Disk model: VMware Virtual S
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0x98de5601

# Device     Boot Start     End Sectors  Size Id Type
# /dev/sda1        2048 1026047 1024000  500M 8e Linux LVM

w # to write the changes and exit.

# confirm
lsblk
# NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
# sda             8:0    0    5G  0 disk
# └─sda1          8:1    0  500M  0 part
# nvme0n1       259:0    0   20G  0 disk
# ├─nvme0n1p1   259:1    0  600M  0 part /boot/efi
# ├─nvme0n1p2   259:2    0    1G  0 part /boot
# └─nvme0n1p3   259:3    0 18.4G  0 part
#   ├─rhel-root 253:0    0 16.4G  0 lvm  /
#   └─rhel-swap 253:1    0    2G  0 lvm  [SWAP]

# Create physical volume
pvcreate /dev/sda1
# Physical volume "/dev/sda1" successfully created.

# confirm
pvdisplay
# --- Physical volume ---
# PV Name               /dev/sda1
# VG Name               wgroup
# PV Size               500.00 MiB / not usable 4.00 MiB
# Allocatable           yes
# PE Size               4.00 MiB
# Total PE              124
# Free PE               124
# Allocated PE          0
# PV UUID               Wype4P-xJT9-u5Mr-b5D0-FYGy-NSwu-GIAbI9

# Create a volume group named wgroup
# -s|--physicalextentsize
vgcreate -s 8M wgroup /dev/sda1
# Volume group "wgroup" successfully created

# confirm the size of PE
vgdisplay wgroup
# --- Volume group ---
# VG Name               wgroup
# System ID
# Format                lvm2
# Metadata Areas        1
# Metadata Sequence No  1
# VG Access             read/write
# VG Status             resizable
# MAX LV                0
# Cur LV                0
# Open LV               0
# Max PV                0
# Cur PV                1
# Act PV                1
# VG Size               496.00 MiB
# PE Size               8.00 MiB
# Total PE              62
# Alloc PE / Size       0 / 0
# Free  PE / Size       62 / 496.00 MiB
# VG UUID               1u9W5s-8I1y-eBg1-geie-E6sT-Lhy6-a8ubLl

# Create a logical volume
# named wshare
# extent size: 50 extents
# use volume group: wgroup
lvcreate -n wshare -l 50 wgroup
# Logical volume "wshare" created.


# Verify
lvdisplay /dev/wgroup/wshare
# --- Logical volume ---
# LV Path                /dev/wgroup/wshare
# LV Name                wshare
# VG Name                wgroup
# LV UUID                KRn9g0-xsKS-HyqV-5pJt-PNsB-NErf-F8QgHb
# LV Write Access        read/write
# LV Creation host, time clienthost, 2025-01-22 19:01:35 -0500
# LV Status              available
# # open                 0
# LV Size                400.00 MiB
# Current LE             50
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:2

# confirm by the LSize = PE * Extent
lvs
# LV     VG     Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
# root   rhel   -wi-ao----  16.41g
# swap   rhel   -wi-ao----   2.00g
# wshare wgroup -wi-a----- 400.00m

# format the logical volume
mkfs.ext4 /dev/wgroup/wshare
# mke2fs 1.46.5 (30-Dec-2021)
# Creating filesystem with 409600 1k blocks and 102400 inodes
# Filesystem UUID: 895e72d0-93e5-40c6-8156-c749dbae7c31
# Superblock backups stored on blocks:
#         8193, 24577, 40961, 57345, 73729, 204801, 221185, 401409

# Allocating group tables: done
# Writing inode tables: done
# Creating journal (8192 blocks): done
# Writing superblocks and filesystem accounting information: done

# Create the mount point /mnt/wshare
mkdir -p /mnt/wshare
# Mount the LVM
mount /dev/wgroup/wshare /mnt/wshare

# confirm
df -h /mnt/wshare
# Filesystem                 Size  Used Avail Use% Mounted on
# /dev/mapper/wgroup-wshare  365M   14K  341M   1% /mnt/wshare

# Configure Auto-Mounting at Boot
vi /etc/fstab

/dev/wgroup/wshare  /mnt/wshare ext4 defaults 0 0
```

- Troubleshootting

```sh
# remove logical volume
lvremove /dev/wgroup/wshare
# Do you really want to remove active logical volume wgroup/wshare? [y/n]: y
#   Logical volume "wshare" successfully removed.

# remove volume group
vgremove /dev/wgroup
#  Volume group "wgroup" successfully removed
```

---

## Question

```conf
Create a swap partition of 400M MB and make it available permanent.
```

---

### Solution

```sh
# create a new partition
fdisk /dev/sda

n # to create a new partition.
p # for a primary partition
# Accept the default partition number.
# Accept the default start sector
+400M # set the end sector according to calculation
# Created a new partition 2 of type 'Linux' and of size 400 MiB.

t # change the partition type
2 # the partition number: 2
L # to check the aliases for Linux swap: 82
82 # Change type to Linux swap
# Changed type of partition 'Linux' to 'Linux swap / Solaris'.

p # confirm
# Disk /dev/sda: 5 GiB, 5368709120 bytes, 10485760 sectors
# Disk model: VMware Virtual S
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0x98de5601

# Device     Boot   Start     End Sectors  Size Id Type
# /dev/sda1          2048 1026047 1024000  500M 8e Linux LVM
# /dev/sda2       1026048 1845247  819200  400M 82 Linux swap / Solaris

w # to write the changes and exit.

# Verify the new partition
lsblk
# NAME              MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
# sda                 8:0    0    5G  0 disk
# ├─sda1              8:1    0  500M  0 part
# │ └─wgroup-wshare 253:2    0  400M  0 lvm  /mnt/wshare
# └─sda2              8:2    0  400M  0 part
# nvme0n1           259:0    0   20G  0 disk
# ├─nvme0n1p1       259:1    0  600M  0 part /boot/efi
# ├─nvme0n1p2       259:2    0    1G  0 part /boot
# └─nvme0n1p3       259:3    0 18.4G  0 part
#   ├─rhel-root     253:0    0 16.4G  0 lvm  /
#   └─rhel-swap     253:1    0    2G  0 lvm  [SWAP]

# Create the swap area
mkswap /dev/sda2
# Setting up swapspace version 1, size = 400 MiB (419426304 bytes)
# no label, UUID=ba97d5af-f1d0-47dc-a96c-069c80f06d44

# Enable the swap partition
swapon /dev/sda2
# Verify the swap space
swapon --show
# NAME      TYPE      SIZE USED PRIO
# /dev/dm-1 partition   2G   0B   -2
# /dev/sda2 partition 400M   0B   -3
free -h
#                total        used        free      shared  buff/cache   available
# Mem:           1.7Gi       807Mi       676Mi        12Mi       427Mi       934Mi
# Swap:          2.4Gi          0B       2.4Gi
lsblk

# Make the Swap Space Permanent
# get the UUID
blkid
# /dev/sda2: UUID="ba97d5af-f1d0-47dc-a96c-069c80f06d44" TYPE="swap" PARTUUID="98de5601-02"
vi /etc/fstab
UUID=ba97d5af-f1d0-47dc-a96c-069c80f06d44 swap swap defaults 0 0

# confirm
swapon -a # enable all
swapon -s
# Filename                                Type            Size            Used            Priority
# /dev/dm-1                               partition       2097148         0               -2
# /dev/sda2                               partition       409596          0               -3
```

---

## Question

```conf
Resize your vo logical volume, it should be approx 300MB( note -> only size accepted from
270mb to 290mb).
```

---

### Solution

- `vo` is the logical volume name
- The following use the `wshare` lv

```sh
# Display the details of the logical volume:
lvdisplay /dev/wgroup/wshare
# --- Logical volume ---
# LV Path                /dev/wgroup/wshare
# LV Name                wshare
# VG Name                wgroup
# LV UUID                KRn9g0-xsKS-HyqV-5pJt-PNsB-NErf-F8QgHb
# LV Write Access        read/write
# LV Creation host, time clienthost, 2025-01-22 19:01:35 -0500
# LV Status              available
# # open                 1
# LV Size                400.00 MiB
# Current LE             50
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:2

# Check the current filesystem size
df -h /mnt/wshare
# Filesystem                 Size  Used Avail Use% Mounted on
# /dev/mapper/wgroup-wshare  365M   14K  341M   1% /mnt/wshare


# Unmount the Logical Volume
umount /mnt/wshare

#  Check filesystem for errors
e2fsck -f /dev/wgroup/wshare
# e2fsck 1.46.5 (30-Dec-2021)
# Pass 1: Checking inodes, blocks, and sizes
# Pass 2: Checking directory structure
# Pass 3: Checking directory connectivity
# Pass 4: Checking reference counts
# Pass 5: Checking group summary information
# /dev/wgroup/wshare: 11/102400 files (0.0% non-contiguous), 36256/409600 blocks

# shrink the filesystem size
resize2fs /dev/wgroup/wshare 300M
# resize2fs 1.46.5 (30-Dec-2021)
# Resizing the filesystem on /dev/wgroup/wshare to 307200 (1k) blocks.
# The filesystem on /dev/wgroup/wshare is now 307200 (1k) blocks long.

# Resize the Logical Volume
lvreduce -L -100M /dev/wgroup/wshare
# Rounding size to boundary between physical extents: 96.00 MiB.
#   File system ext4 found on wgroup/wshare.
#   File system size (300.00 MiB) is smaller than the requested size (304.00 MiB).
#   File system reduce is not needed, skipping.
#   Size of logical volume wgroup/wshare changed from 400.00 MiB (50 extents) to 304.00 MiB (38 extents).
#   Logical volume wgroup/wshare successfully resized.

# confirm
lvs
  # LV     VG     Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  # root   rhel   -wi-ao----  16.41g
  # swap   rhel   -wi-ao----   2.00g
  # wshare wgroup -wi-ao---- 304.00m

# Remount the Logical Volume
mount -a
# confirm
df -h /mnt/wshare
# Filesystem                 Size  Used Avail Use% Mounted on
# /dev/mapper/wgroup-wshare  271M   14K  252M   1% /mnt/wshare
```

---

## Question

```conf
Resize to 400MB
```

---

### Solution

```sh
# check the current file system
df -h /mnt/wshare
# Filesystem                 Size  Used Avail Use% Mounted on
# /dev/mapper/wgroup-wshare  271M   14K  252M   1% /mnt/wshare

# Extend the logical volume
# lvextend -r -L 400M /dev/mapper/wgroup-wshare # resize the fs
lvextend -L 400M /dev/mapper/wgroup-wshare
# Size of logical volume wgroup/wshare changed from 304.00 MiB (38 extents) to 400.00 MiB (50 extents).
# Logical volume wgroup/wshare successfully resized.

# verify
lvdisplay /dev/mapper/wgroup-wshare
# --- Logical volume ---
# LV Path                /dev/wgroup/wshare
# LV Name                wshare
# VG Name                wgroup
# LV UUID                KRn9g0-xsKS-HyqV-5pJt-PNsB-NErf-F8QgHb
# LV Write Access        read/write
# LV Creation host, time clienthost, 2025-01-22 19:01:35 -0500
# LV Status              available
# # open                 1
# LV Size                400.00 MiB
# Current LE             50
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:2

# Resize the Filesystem
resize2fs /dev/mapper/wgroup-wshare
# resize2fs 1.46.5 (30-Dec-2021)
# Filesystem at /dev/mapper/wgroup-wshare is mounted on /mnt/wshare; on-line resizing required
# old_desc_blocks = 3, new_desc_blocks = 4
# The filesystem on /dev/mapper/wgroup-wshare is now 409600 (1k) blocks long.

# Verify 
df -h /mnt/wshare
# Filesystem                 Size  Used Avail Use% Mounted on
# /dev/mapper/wgroup-wshare  365M   14K  342M   1% /mnt/wshare
```
