# Linux - Disk

[Back](../../index.md)

---

- [Linux - Disk](#linux---disk)
  - [Disk Usage Information](#disk-usage-information)
  - [Check Disk Space Usage](#check-disk-space-usage)
  - [View File System Details](#view-file-system-details)
  - [Mount and Unmount File Systems](#mount-and-unmount-file-systems)
  - [Disk Partitioning and Formatting](#disk-partitioning-and-formatting)
  - [Logical Volume Management (LVM)](#logical-volume-management-lvm)
  - [Monitoring Disk Health](#monitoring-disk-health)

---

## Disk Usage Information

| Command          | Desc                                         |
| ---------------- | -------------------------------------------- |
| `df`             | Report file system disk usage.               |
| `df -a`          | show all disk space usage                    |
| `df -BM`         | show disk space usage in MB size             |
| `df -h`          | show disk space usage in human readable size |
| `df -T`          | show disk space usage with file system type  |
| `du`             | Estimates file usage in current path         |
| `du dir/file`    | Estimates file usage of a dir/file           |
| `du -k dir/file` | Display sizes in Kilobytes.                  |
| `du -h dir/file` | Display sizes in human readable format.      |

---

## Check Disk Space Usage

| Command           | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| `df`              | Report file system disk usage.                                   |
| `df -h`           | Display disk usage in human-readable format.                     |
| `df -T`           | Include file system type in the output.                          |
| `du`              | Estimate file and directory space usage.                         |
| `du -sh /var/log` | Summarize size of `/var/log` directory in human-readable format. |



---

## View File System Details

| Command    | Description                                          |
| ---------- | ---------------------------------------------------- |
| `lsblk`    | List information about block devices.                |
| `lsblk -f` | Display file system type and UUID.                   |
| `blkid`    | Show UUID and type for a device (e.g., `/dev/sda1`). |

---

## Mount and Unmount File Systems

| Command                     | Description                                     |
| --------------------------- | ----------------------------------------------- |
| `mount /dev/sdb1 /mnt/data` | Mount `/dev/sdb1` to `/mnt/data`.               |
| `umount /mnt/data`          | Unmount the file system mounted at `/mnt/data`. |
| `mount -a`                  | Mount all file systems defined in `/etc/fstab`. |

---

## Disk Partitioning and Formatting

| Command               | Description                                     |
| --------------------- | ----------------------------------------------- |
| `fdisk /dev/sda`      | Interactive partition manager for MBR disks.    |
| `parted /dev/sdb`     | Partition manager for GPT/MBR disks.            |
| `mkfs.ext4 /dev/sdb1` | Format the partition with the ext4 file system. |

---

## Logical Volume Management (LVM)

| Command                           | Description                                              |
| --------------------------------- | -------------------------------------------------------- |
| `pvcreate /dev/sdb`               | Initialize a physical volume for LVM.                    |
| `vgcreate my_vg /dev/sdb`         | Create a volume group named `my_vg`.                     |
| `lvcreate -L 10G -n my_lv my_vg`  | Create a 10GB logical volume named `my_lv` in `my_vg`.   |
| `lvextend -L+5G /dev/my_vg/my_lv` | Extend the logical volume by 5GB.                        |
| `resize2fs /dev/my_vg/my_lv`      | Resize the file system to match the logical volume size. |

---

## Monitoring Disk Health

| Command                | Description                                               |
| ---------------------- | --------------------------------------------------------- |
| `smartctl -a /dev/sda` | Display SMART health information for the disk `/dev/sda`. |
| `iostat -x 1`          | Show extended disk I/O stats every second.                |
| `iotop`                | Display real-time I/O usage by processes.                 |

F
