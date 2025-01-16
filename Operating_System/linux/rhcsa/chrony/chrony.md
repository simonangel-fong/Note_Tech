# RHCSA Synchronize Time

[Back](../../index.md)

- [RHCSA Synchronize Time](#rhcsa-synchronize-time)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
Configure your system to synchronize the time from form "classroom.example.com".
```

---

### Solution


```sh
yum install -y chrony
rpm -q chrony

# Edit the Configuration File
vi /etc/chrony.conf

server classroom.example.com iburst

# Restart and Enable the chronyd Service
systemctl restart chronyd
systemctl enable chronyd

# Verify Time Synchronization
systemctl status chronyd
chronyc sources -v

# Test Time Synchronization
chronyc makestep
date

# Allow NTP Traffic Through the Firewall
firewall-cmd --permanent --add-service=ntp
firewall-cmd --reload
```