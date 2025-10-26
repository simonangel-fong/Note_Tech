# Linux - Hardware Management: Memory

[Back](../../index.md)

- [Linux - Hardware Management: Memory](#linux---hardware-management-memory)
  - [CPU](#cpu)
    - [Lab: CPU](#lab-cpu)
  - [Memory](#memory)
  - [Swap](#swap)
  - [Disk Info](#disk-info)

---

## CPU

| CMD                 | Desc                        |
| ------------------- | --------------------------- |
| `lscpu`             | Show CPU architecture       |
| `cat /proc/cpuinfo` | Print CPU architecture file |

### Lab: CPU

```sh
lscpu
# Architecture:             x86_64
#   CPU op-mode(s):         32-bit, 64-bit
#   Address sizes:          39 bits physical, 48 bits virtual
#   Byte Order:             Little Endian
# CPU(s):                   4
# ...

# key cpu info
lscpu | egrep 'Model name|Socket|Thread|NUMA|CPU\(s\)'
# CPU(s):                               4
# On-line CPU(s) list:                  0-3
# Model name:                           Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz
# BIOS Model name:                      Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz To Be Filled By O.E.M CPU @ 2.5GHz
# Thread(s) per core:                   2
# Socket(s):                            1
# CPU(s) scaling MHz:                   92%
# NUMA node(s):                         1
# NUMA node0 CPU(s):                    0-3

# get physical core
grep 'cpu cores' /proc/cpuinfo | uniq
# cpu cores       : 2

# threads
echo "CPU threads: $(grep -c processor /proc/cpuinfo)"
# CPU threads: 4

# number of processors
nproc --all
# 4
```

---

## Memory

| CMD       | Desc                                             |
| --------- | ------------------------------------------------ |
| `free`    | Show free and used memory                        |
| `free -h` | Show free and used memory in human readable size |
| `free -t` | showing the column totals.                       |

- Disk space calculation:
  - swap size + `/boot` size + `/` size = total Disk size

---

## Swap

- `Swap space`
  - an extension of **physical RAM**, offering **virtual memory** that helps maintain system stability and performance.

| CMD    | Desc                                    |
| ------ | --------------------------------------- |
| `swap` | Display summary about used swap devices |

---

## Disk Info

| CMD       | Desc                                       |
| --------- | ------------------------------------------ |
| `df -h`   | Show information about the file system     |
| `du -h .` | Summarize device usage of the set of FILEs |
