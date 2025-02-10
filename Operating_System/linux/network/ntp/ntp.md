# Linux - Network: NTP & System Date Time

[Back](../../index.md)

- [Linux - Network: NTP \& System Date Time](#linux---network-ntp--system-date-time)
  - [NTP](#ntp)
  - [`chronyd`: System Time Package](#chronyd-system-time-package)
    - [Configuration File](#configuration-file)
    - [Command: `chronyc`](#command-chronyc)
    - [Lab: Configure `chronyd`](#lab-configure-chronyd)
  - [System Date and Time](#system-date-and-time)
    - [Lab: Configure data time](#lab-configure-data-time)

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

- Daemon

  - `systemctl start/restart chronyd`

- Log file

  - `/var/log/chrony/`
  - `journalctl -u chronyd`

- Firewall Configuration
  - `firewall-cmd --permanent --add-service=ntp`
  - `ss -ntlp | grep 123`

---

### Configuration File

- `/etc/chronyd.conf`

  - `pool`: NTP server

- Common Config

| Directive   | desc                                                              |
| ----------- | ----------------------------------------------------------------- |
| `driftfile` | location and name of the drift file                               |
| `logdir`    | Sets the log file location                                        |
| `pool`      | hostname for a pool of time servers.                              |
| `server`    | hostname or IP address of a single time server.                   |
| `peer`      | hostname or IP address of a timeserver at the same stratum level. |

- `iburst` option
  - dictates the `Chrony` service to send the first four update requests to the time server every 2 seconds.

---

### Command: `chronyc`

- chronyc command

| CMD                   | Desc                                              |
| --------------------- | ------------------------------------------------- |
| `chronyc sources -v`  | Lists detailed NTP sources and their statuses.    |
| `chronyc sources`     | Lists configured NTP servers and their state.     |
| `chronyc tracking`    | Shows system time status, drift, and sync source. |
| `chronyc sourcestats` | Displays statistics about NTP sources.            |
| `chronyc activity`    | Shows the number of active and inactive sources.  |
| `chronyc ntpdata`     | Displays detailed NTP source data.                |
| `chronyc makestep`    | manually force synchronization                    |

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
pool 8.8.8.8 iburst

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

## System Date and Time

- Commands and tools:

| CMD                                          | DESC                                  |
| -------------------------------------------- | ------------------------------------- |
| `date`                                       | print or set the system date and time |
| `timedatectl`                                | Control the system time and date      |
| `timedatectl set-ntp true/false`             | Enable/Disable NTP synchronization    |
| `timedatectl list-timezones`                 | Show known time zones                 |
| `timedatectl set-timezone America/New_York`  | Set a time zone                       |
| `timedatectl set-time HH:MM:SS`              | Set a time                            |
| `timedatectl set-time '2024-11-11 11:11:11'` | Set date and time                     |

- When configure the system date and time, it requires that the NTP/Chrony service is deactivated in order to make time adjustments.
  - `timedatectl set-ntp false`

---

### Lab: Configure data time

- Display date time

```sh
date
# Sat 08 Feb 2025 04:54:41 PM EST

timedatectl
#                Local time: Sat 2025-02-08 16:57:19 EST
#            Universal time: Sat 2025-02-08 21:57:19 UTC
#                  RTC time: Sat 2025-02-08 21:57:19
#                 Time zone: America/Toronto (EST, -0500)
# System clock synchronized: yes
#               NTP service: active
#           RTC in local TZ: no
```

- Configure date time

```sh
# try set date time without disabling ntp
timedatectl set-time "2019-11-18 23:00"
# Failed to set time: Automatic time synchronization is enabled

# disable ntp
timedatectl set-ntp false
# confirm
timedatectl
#                Local time: Sat 2025-02-08 16:59:12 EST
#            Universal time: Sat 2025-02-08 21:59:12 UTC
#                  RTC time: Sat 2025-02-08 21:59:12
#                 Time zone: America/Toronto (EST, -0500)
# System clock synchronized: yes
#               NTP service: inactive
#           RTC in local TZ: no

# set new date time
timedatectl set-time "2019-11-18 23:00"
# confirm
date
# Mon 18 Nov 2019 11:00:24 PM EST
timedatectl
#                Local time: Mon 2019-11-18 23:00:03 EST
#            Universal time: Tue 2019-11-19 04:00:03 UTC
#                  RTC time: Tue 2019-11-19 04:00:03
#                 Time zone: America/Toronto (EST, -0500)
# System clock synchronized: no
#               NTP service: inactive
#           RTC in local TZ: no
```

- Re-enable ntp

```sh
# enable ntp
timedatectl set-ntp true

date
# Sat 08 Feb 2025 05:02:49 PM EST
timedatectl
#                Local time: Sat 2025-02-08 17:02:42 EST
#            Universal time: Sat 2025-02-08 22:02:42 UTC
#                  RTC time: Sat 2025-02-08 22:02:42
#                 Time zone: America/Toronto (EST, -0500)
# System clock synchronized: yes
#               NTP service: active
#           RTC in local TZ: no
```
