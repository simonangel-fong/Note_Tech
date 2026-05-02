# Linux Debugging Cheatsheet (DevOps)

> Handbook for diagnosing and remediating common Linux issues in production/DevOps environments.

[Back](../index.md)

- [Linux Debugging Cheatsheet (DevOps)](#linux-debugging-cheatsheet-devops)
  - [CPU \& Memory](#cpu--memory)
    - [Diagnosis - CPU](#diagnosis---cpu)
    - [Diagnosis - Memory](#diagnosis---memory)
    - [Diagnosis - Log](#diagnosis---log)
    - [Remediation - Process](#remediation---process)
  - [Disk](#disk)
    - [Diagnosis - Disk](#diagnosis---disk)
  - [Network](#network)
  - [Service](#service)
  - [File \& Permission](#file--permission)
  - [Packages](#packages)

---

## CPU & Memory

### Diagnosis - CPU

```sh
# System load averages: 1-min, 5-min, 15-min
# Rule of thumb: load > number of CPU cores = overloaded
uptime

# Interactive process viewer — shows CPU%, MEM%, PID, command
top
# Inside top:
#   M  → sort by memory usage
#   P  → sort by CPU usage
#   k  → kill a process by PID
#   q  → quit

# Enhanced top with color, tree view, and mouse support (install if missing)
htop

# Top 5 processes by CPU or memory (non-interactive snapshot)
ps aux --sort=-%cpu | head -n 5
ps aux --sort=-%mem | head -n 5

# Full process list with PPID (parent PID) — useful for tracing spawned processes
ps -ef

# CPU core count — calibrate load average thresholds
nproc
```

---

### Diagnosis - Memory

```sh
# Human-readable summary: total, used, free, buff/cache, available
free -h

# Virtual memory stats every 1 second: r=run queue, si/so=swap in/out, us/sy/id=CPU breakdown
# High si/so = swapping heavily → memory pressure
vmstat 1

# Per-process memory snapshot sorted by RSS (resident set size)
ps aux --sort=-%cpu | head -n 10

# Identify OOM (Out Of Memory) kills in kernel log
dmesg | grep -i "oom\|killed process"
```

---

### Diagnosis - Log

```sh
# Tail logs for a specific service (follow mode -f = live stream)
journalctl -u <service_name>
journalctl -u <service_name> -f

# Show recent errors with context (-x = explanations, -e = jump to end)
journalctl -xe

# Filter by time range
journalctl -u <service_name> --since "1 hour ago"
journalctl -u <service_name> --since "2024-01-01 00:00" --until "2024-01-01 06:00"

# Kernel messages (hardware errors, OOM, driver issues)
dmesg -T | tail -50
dmesg -T | grep -i "error\|warn\|fail"
```

---

### Remediation - Process

```sh
# Find PID by process name
pgrep <process_name>
pgrep -a <process_name>     # also show full command line

# Show process tree — visualize parent/child relationships
pstree -p

# Trace system calls in real time — diagnose hangs, permission errors, missing files
strace -p <PID>
strace -p <PID> -e trace=network   # filter to network calls only
strace -p <PID> -e trace=file      # filter to file I/O only

# Graceful → forceful kill escalation
kill <PID>          # SIGTERM (15): ask process to shut down cleanly
kill -9 <PID>       # SIGKILL (9): force kill — use when SIGTERM is ignored
pkill <process_name>    # kill by name (SIGTERM)
killall <process_name>  # kill all instances by name

# Check if process is still alive after kill
ps -p <PID>
```

---

## Disk

### Diagnosis - Disk

```sh
# Filesystem usage (human-readable) — spot full or near-full mounts
df -h

# Alert on filesystems over 80% full
df -h | awk '$5+0 > 80 { print $0 }'

# Directory size summary — find what's consuming space
du -sh /path
du -sh /* 2>/dev/null | sort -rh | head -20   # top space consumers from /

# I/O performance stats — check read/write throughput and await time
iostat -x 1       # extended stats every 1 second
# High %util (>80%) or high await = I/O bottleneck

# Real-time I/O per process (requires iotop)
iotop -o          # show only processes doing I/O

# List open files on a mount point — find what's blocking umount
lsof +D /mount/point
```

---

## Network

```sh
# Hostname and OS info
hostnamectl

# Network interfaces and IP addresses
ip a

# Routing table — check default gateway and routes
ip r

# Active listening ports (t=TCP, u=UDP, l=listening, n=numeric, p=process)
# Preferred over netstat on modern systems
ss -tulnp

# Legacy equivalent (may not be installed by default)
netstat -tulnp

# Test connectivity and latency
ping -c 4 <host>

# Trace network path to a host — identify where packets drop
traceroute <host>

# DNS resolution
dig <domain>               # detailed DNS query with TTL
nslookup <domain>          # quick lookup (less detail)
dig +short <domain>        # IP only

# Test if a port is reachable (replace telnet)
nc -zv <host> <port>

# Capture packets on an interface (requires root)
tcpdump -i eth0 -n port 80
tcpdump -i any -n 'host <IP>'
```

---

## Service

```sh
# Check service status (shows recent log lines too)
systemctl status <service_name>

systemctl start   <service_name>
systemctl stop    <service_name>
systemctl restart <service_name>   # stop + start
systemctl reload  <service_name>   # reload config without full restart (if supported)

# Enable/disable auto-start on boot
systemctl enable  <service_name>
systemctl disable <service_name>

# List all failed services — first stop after an incident
systemctl --failed

# Reload systemd after editing a unit file
systemctl daemon-reload
```

---

## File & Permission

```sh
# Locate binary path — verify which version of a command is used
which <command>
type <command>      # also shows aliases and builtins

# List open files for a process or file path
lsof -p <PID>                  # all files opened by a process
lsof -c <process_name>         # by process name
lsof /path/to/file             # who has this file open
lsof -i :<port>                # process using a specific port

# Trace system calls (file I/O focus) — diagnose "permission denied" or "no such file"
strace -p <PID> -e trace=file

# File permissions
chmod +x <file>               # make executable
chmod 644 <file>              # rw-r--r-- (typical config file)
chmod 600 <file>              # rw------- (private key, .env)
chmod -R 755 /path/to/dir     # recursive: rwxr-xr-x

# Ownership
chown <user>:<group> <file>
chown -R <user>:<group> /path/to/dir

# Check SELinux/AppArmor denials if permissions look correct but still denied
ausearch -m avc -ts recent    # SELinux audit denials
```

---

## Packages

```sh
# Debian / Ubuntu (apt)
apt update                    # refresh package index
apt upgrade                   # upgrade all installed packages
apt install <package_name>
apt remove  <package_name>    # remove package, keep config
apt purge   <package_name>    # remove package + config files
apt autoremove                # remove unused dependencies

# Search for a package
apt search <keyword>
apt show   <package_name>     # show version, deps, description

# RHEL / CentOS / Amazon Linux (dnf/yum)
dnf update
dnf install <package_name>
dnf remove  <package_name>
dnf search  <keyword>
```
