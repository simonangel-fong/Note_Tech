# Linux - Network: NTP

[Back](../../index.md)

- [Linux - Network: NTP](#linux---network-ntp)
  - [NTP](#ntp)
  - [`chronyd`: System Time Package](#chronyd-system-time-package)
    - [Lab: Configure `chronyd`](#lab-configure-chronyd)

---

## NTP

- `Network Time Protocol (NTP)`

  - a protocol that **synchronizes computer clocks** over the internet.
  - It's used to keep clocks in sync with a precise time source
  - can synchronize time over networks with varying latency.

- Layer 4: `UDP` protocol
- Port: `123`
- Tools implement NTP: `chrony`

---

## `chronyd`: System Time Package

- `chronyd`

  - a package used for time synchronization
  - a replacement of `ntpd`
    - cannot corun with `ntpd`

- `Network Time Protocol(NTP)`:

  - a standard way to synchronized the time to the NTP server.

- Package
  - `dnf install chrony`
- Command
  - `chronyc`
- Service
  - `systemctl start/restart chronyd`
- Configuration File
  - `/etc/chronyd.conf`
    - `pool`: NTP server
- Log file
  - `/var/log/chrony/`
- Firewall Configuration

  - `firewall-cmd --permanent --add-service=ntp`
  - `ss -ntlp | grep 123`

- Commands and tools:

| CMD                                          | DESC                                  |
| -------------------------------------------- | ------------------------------------- |
| `date`                                       | print or set the system date and time |
| `timedatectl`                                | Control the system time and date      |
| `timedatectl list-timezones`                 | Show known time zones                 |
| `timedatectl set-timezone America/New_York`  | Set a time zone                       |
| `timedatectl set-time HH:MM:SS`              | Set a time                            |
| `timedatectl set-time '2024-11-11 11:11:11'` | Set date and time                     |
| `timedatectl set-ntp true`                   | Enable NTP synchronization            |

- chronyc interaction mode

| CMD       | Desc                    |
| --------- | ----------------------- |
| `help`    | Show help info          |
| `sources` | Show current NTP server |
| `quit`    | Exit current session    |

- chronyc command

| CMD                  | Desc                                              |
| -------------------- | ------------------------------------------------- |
| `chronyc sources -v` | Displays the list of Synchronization Sources      |
| `chronyc tracking`   | Shows the current time source, offset, and drift. |
| `chronyc ntpdata`    | Manually Query NTP Server                         |
| `chronyc makestep`   | Manually Update Time.                             |

---

### Lab: Configure `chronyd`

```sh
su -

# confirm package installed
rpm -q chrony
# chrony-4.5-3.el9.x86_64

# change configuration
vi /etc/chrony.conf
# make some changes for the NTP server
# 8.8.8.8 is not a valid NTP server
pool 8.8.8.8

# restart service
systemctl restart chronyd
systemctl status chronyd
# ● chronyd.service - NTP client/server
#      Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2025-01-15 23:03:40 EST; 4s ago
#        Docs: man:chronyd(8)
#              man:chrony.conf(5)
#     Process: 3318 ExecStart=/usr/sbin/chronyd $OPTIONS (code=exited, status=0/SUCCESS)
#    Main PID: 3321 (chronyd)
#       Tasks: 1 (limit: 10748)
#      Memory: 1.1M
#         CPU: 28ms
#      CGroup: /system.slice/chronyd.service
#              └─3321 /usr/sbin/chronyd -F 2

# Jan 15 23:03:40 ServerA systemd[1]: Starting NTP client/server...
# Jan 15 23:03:40 ServerA chronyd[3321]: chronyd version 4.5 starting (+CMDMON +NTP +REFCLOCK +RTC >
# Jan 15 23:03:40 ServerA chronyd[3321]: Loaded 0 symmetric keys
# Jan 15 23:03:40 ServerA chronyd[3321]: Using right/UTC timezone to obtain leap second data
# Jan 15 23:03:40 ServerA chronyd[3321]: Frequency -12.324 +/- 3.755 ppm read from /var/lib/chrony/>
# Jan 15 23:03:40 ServerA chronyd[3321]: Loaded seccomp filter (level 2)
# Jan 15 23:03:40 ServerA systemd[1]: Started NTP client/server.


# Confirm
chronyc sources -v
#   .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
#  / .- Source state '*' = current best, '+' = combined, '-' = not combined,
# | /             'x' = may be in error, '~' = too variable, '?' = unusable.
# ||                                                 .- xxxx [ yyyy ] +/- zzzz
# ||      Reachability register (octal) -.           |  xxxx = adjusted offset,
# ||      Log2(Polling interval) --.      |          |  yyyy = measured offset,
# ||                                \     |          |  zzzz = estimated error.
# ||                                 |    |           \
# MS Name/IP address         Stratum Poll Reach LastRx Last sample
# ===============================================================================
# ^* archer.fsck.ca                2   6    17    33   +421us[+6019us] +/-   14ms
# ^- 69-196-152-39.dsl.teksav>     3   6    17    33  +5711us[+5711us] +/-   86ms
# ^- ntp.netlinkify.com            2   6    27    31  +1822us[+1822us] +/-   13ms
# ^- drax.kayaks.hungrycats.o>     4   6    17    33  +1042us[+1042us] +/-   18ms
# ^? dns.google                    0   6     0     -     +0ns[   +0ns] +/-    0ns

chronyc tracking
# Reference ID    : 953813A3 (archer.fsck.ca)
# Stratum         : 3
# Ref time (UTC)  : Thu Jan 16 04:04:51 2025
# System time     : 0.001715553 seconds fast of NTP time
# Last offset     : +0.001740796 seconds
# RMS offset      : 0.001740796 seconds
# Frequency       : 12.317 ppm slow
# Residual freq   : +16.986 ppm
# Skew            : 4.219 ppm
# Root delay      : 0.028784681 seconds
# Root dispersion : 0.002550795 seconds
# Update interval : 64.4 seconds
# Leap status     : Normal

chronyc ntpdata
# Remote address  : 149.56.19.163 (953813A3)
# Remote port     : 123
# Local address   : 192.168.128.100 (C0A88064)
# Leap status     : Normal
# Version         : 4
# Mode            : Server
# Stratum         : 2
# Poll interval   : 6 (64 seconds)
# Precision       : -25 (0.000000030 seconds)
# Root delay      : 0.001190 seconds
# Root dispersion : 0.000900 seconds
# Reference ID    : BD9C7C8F ()
# Reference time  : Thu Jan 16 03:50:24 2025
# Offset          : -0.001854833 seconds
# Peer delay      : 0.027594496 seconds
# Peer dispersion : 0.000055333 seconds
# Response time   : 0.000048660 seconds
# Jitter asymmetry: +0.00
# NTP tests       : 111 111 1111
# Interleaved     : No
# Authenticated   : No
# TX timestamping : Daemon
# RX timestamping : Kernel
# Total TX        : 5
# Total RX        : 5
# Total valid RX  : 5
# Total good RX   : 5

chronyc makestep
# 200 OK
```

---
