# Docker - Fundamental

[Back](../index.md)

- [Docker - Fundamental](#docker---fundamental)
  - [Fundamental](#fundamental)
  - [Implement Container](#implement-container)
    - [Feature: `linux namespace`](#feature-linux-namespace)
    - [Linux kernel feature: `cgroups`](#linux-kernel-feature-cgroups)
    - [Feature: `syscall`](#feature-syscall)
    - [Feature: `Linux capabilities`](#feature-linux-capabilities)
    - [Feature: `Seccomp (secure computing mode)`](#feature-seccomp-secure-computing-mode)

---

## Fundamental

- `images`
  - object used to **package** `application` and required `envrionment`
    - contains the whole filesystem that the `application` will use and additional **metadata**
      - e.g., path to the executable file, ports the application listens on
- `registries`
  - a repository of container images that enables the exchange of images between different people and computers.
- `containers`
  - the instantiated object of a container image
  - a normal process running in the host operating system
    - isolated from other processes

---

## Implement Container

### Feature: `linux namespace`

- `Linux Namespaces`

  - a linux feature ensures that each process has its own view of the system.
    - a process running in a container will only see some of the files, processes and network interfaces on the system,
    - The process only sees resources that are in this namespace and none in the other namespaces.
  - used to implement containerization.

- namespace types
  - `Mount namespace (mnt)`: isolates mount points (file systems).
  - `Process ID namespace (pid)`: isolates process IDs.
  - `Network namespace (net)`: isolates network devices, stacks, ports, etc.
  - `Inter-process communication namespace (ipc)` isolates the communication between processes (this includes isolating message queues, shared memory, and others).
  - `UNIX Time-sharing System (UTS) namespace` isolates the system hostname and the Network Information Service (NIS) domain name.
  - `User ID namespace (user)`: isolates user and group IDs.
  - `Time namespace`: allows each container to have its own offset to the system clocks.
  - `Cgroup namespace`: isolates the Control Groups root directory.

---

```sh
# ubuntu
docker run -d --name busybox busybox sleep 300
# 8ef189a2907c47d349cc5c52f0bae3d8c7a611fc9f562e994a99eb83752c82fe

# host
pstree
# systemd─┬─2*[agetty]
#         ├─containerd───14*[{containerd}]
#         ├─containerd-shim─┬─sleep
#         │                 └─10*[{containerd-shim}]

ps aux | grep sleep
# root         681  0.0  0.0   4436  1716 ?        Ss   20:16   0:00 sleep 300

ip a
# 3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
#     link/ether 06:7b:a3:c8:28:94 brd ff:ff:ff:ff:ff:ff
#     inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
#        valid_lft forever preferred_lft forever
#     inet6 fe80::47b:a3ff:fec8:2894/64 scope link
#        valid_lft forever preferred_lft forever

# in container
docker exec -it busybox sh
# / #

ps -a
# PID   USER     TIME  COMMAND
#     1 root      0:00 sleep 300
#     7 root      0:00 sh
#    15 root      0:00 ps -a

ip a
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
#     link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
#     inet 127.0.0.1/8 scope host lo
#        valid_lft forever preferred_lft forever
#     inet6 ::1/128 scope host
#        valid_lft forever preferred_lft forever
# 2: eth0@if4: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
#     link/ether ea:13:d6:12:07:d0 brd ff:ff:ff:ff:ff:ff
#     inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
#        valid_lft forever preferred_lft forever
```

### Linux kernel feature: `cgroups`

- `Linux Control Groups (cgroups)`

  - a Linux kernel feature that organizes `processes` into **hierarchical groups** to **manage and limit system resources** like CPU, memory, disk I/O, and network bandwidth,
    - e.g.,a process or group of processes can only use the allotted CPU time, memory, and network bandwidth
    - processes cannot occupy resources that are reserved for other processes.
    - prevent one container from starving the other containers of compute resources.

- Resources alloacation
  - By default: unrestricted access to all CPU cores on the host
  - Specify:
    - `docker run --cpuset-cpus="1,2"`: only use cores one and two
    - `docker run --cpus="0.5"`: only half of a CPU core
    - `docker run --memory="100m"`: set the maximum memory size

---

### Feature: `syscall`

- `system call (syscall)`

  - serves as the essential interface that allows user-level applications to request services from the operating system's kernel.
  - a program's request for a service from the operating system (OS), acting as a **secure bridge** between **user applications** and the **privileged kernel**

- How it works:

  - **Request**:
    - A user program needs a `privileged service` (e.g., writing to a file).
  - **Transition**:
    - The program **triggers** a `system call`, causing a controlled **switch** from `User Mode` (limited privileges) to `Kernel Mode` (full privileges).
  - **Execution**: The OS kernel **performs** the requested action.
  - **Return**: The `kernel` **returns control** and **data** to the `user program`, switching back to `User Mode`.

- **Most** containers should run **without elevated privileges**.
  - Only those programs that you trust and that actually need the **additional privileges** should run in **privileged containers**.
  - `docker run --privileged`create a privileged container

---

### Feature: `Linux capabilities`

- `Linux capabilities`

  - a kernel feature that **break down** the traditional, monolithic `root (superuser) privileges` into smaller, distinct **units of permission**.

- `Principle of Least Privilege`:

  - Instead of an "all-or-nothing" root/non-root model, processes are **granted only the specific capabilities** they require to perform their intended tasks.

- Common Capabilities
  - `CAP_SYS_ADMIN`:
    - Allows a wide range of **administrative tasks**, often avoided in favor of more specific capabilities due to its broad power.
    - `CAP_NET_BIND_SERVICE`:
      - Allows a process to bind to **privileged ports** (those with a number **less than 1024**).
    - `CAP_NET_RAW`:
      - Permits the use of **raw and packet sockets**, necessary for tools like ping.
    - `CAP_CHOWN`:
      - Bypasses permission checks for changing file UIDs and GIDs.
    - `CAP_DAC_OVERRIDE`:
      - Bypasses all discretionary access control (DAC) read, write, and execute permission checks on files.
    - `CAP_KILL`:
      - Bypasses permission checks for sending signals to processes owned by a different user.

| CMD           | DESC                                                             |
| ------------- | ---------------------------------------------------------------- |
| `getcap FILE` | Displays the capabilities assigned to files (file capabilities). |
| `setcap FILE` | Assigns capabilities to an executable file.                      |
| `getpcaps`    | Shows the capabilities of a currently running process.           |

```sh
docker run -d --name busybox busybox sleep 300

ps -aux | grep sleep
# root        1569  0.0  0.0   4436  1652 ?        Ss   21:33   0:00 sleep 300

getpcaps 1569
# 1569: cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap=ep
```

- `Capabilities` can be added or removed (dropped) from a `container` when you create it.
  - Each capability represents a **set of privileges** available to the `processes` in the container.

---

### Feature: `Seccomp (secure computing mode)`

- `Seccomp (secure computing mode)`

  - a Linux kernel security feature used to **restrict** the `system calls (syscalls)` a process can make, thereby reducing the attack surface of an application.

- **Default Profiles**:
  - Container runtimes like `Docker`, `containerd`, and `CRI-O` ship with default `seccomp profiles` that **block** around 40+ dangerous `syscalls` by default while allowing common ones.
