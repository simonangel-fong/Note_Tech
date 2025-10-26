# Linux - System: System Setting

[Back](../../index.md)

- [Linux - System: System Setting](#linux---system-system-setting)
  - [System Time](#system-time)
    - [Lab: system time](#lab-system-time)

---

## System Time

| CMD                                          | DESC                                           |
| -------------------------------------------- | ---------------------------------------------- |
| `timedatectl`                                | Get system time                                |
| `timedatectl status`                         | Show current time settings                     |
| `timedatectl show`                           | Show properties of systemd-timedated           |
| `timedatectl set-ntp true`                   | Enable or disable network time synchronization |
| `timedatectl set-time 'YYYY-MM-DD HH:MM:SS'` | Set system time                                |
| `date -s "YYYY-MM-DD HH:MM:SS"`              | Set system time                                |

### Lab: system time

```sh
timedatectl
#                Local time: Mon 2025-10-13 11:57:32 EDT
#            Universal time: Mon 2025-10-13 15:57:32 UTC
#                  RTC time: Mon 2025-10-13 15:57:32
#                 Time zone: America/Toronto (EDT, -0400)
# System clock synchronized: yes
#               NTP service: active
#           RTC in local TZ: no

timedatectl status
#                Local time: Mon 2025-10-13 11:58:00 EDT
#            Universal time: Mon 2025-10-13 15:58:00 UTC
#                  RTC time: Mon 2025-10-13 15:58:00
#                 Time zone: America/Toronto (EDT, -0400)
# System clock synchronized: yes
#               NTP service: active
#           RTC in local TZ: no

timedatectl show
# Timezone=America/Toronto
# LocalRTC=no
# CanNTP=yes
# NTP=yes
# NTPSynchronized=yes
# TimeUSec=Mon 2025-10-13 11:58:19 EDT
# RTCTimeUSec=Mon 2025-10-13 11:58:19 EDT

timedatectl set-ntp true
```
