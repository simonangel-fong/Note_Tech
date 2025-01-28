# RHCSA Synchronize Time

[Back](../../index.md)

- [RHCSA Synchronize Time](#rhcsa-synchronize-time)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
Configure your system to synchronize the time from form "time.google.com".
```

---

### Solution


```sh
yum install -y chrony
rpm -q chrony

# Edit the Configuration File
vi /etc/chrony.conf

server time.google.com iburst

# Restart and Enable the chronyd Service
systemctl restart chronyd
systemctl enable chronyd

# Verify Time Synchronization
systemctl status chronyd
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
# ^* time.google.com              1   6    37    31    +21us[ -122us] +/-   17ms

# Confirm the current synchronization status
chronyc tracking
# Reference ID    : D8EF2308 (time.google.com)
# Stratum         : 2
# Ref time (UTC)  : Sat Jan 25 22:18:10 2025
# System time     : 0.000113358 seconds slow of NTP time
# Last offset     : -0.000142851 seconds
# RMS offset      : 0.000142851 seconds
# Frequency       : 14.145 ppm slow
# Residual freq   : -4.996 ppm
# Skew            : 0.281 ppm
# Root delay      : 0.033960786 seconds
# Root dispersion : 0.000887074 seconds
# Update interval : 65.2 seconds
# Leap status     : Normal

# Test Time Synchronization
chronyc makestep
# 200 OK
date

# Allow NTP Traffic Through the Firewall
firewall-cmd --permanent --add-service=ntp
firewall-cmd --reload
```