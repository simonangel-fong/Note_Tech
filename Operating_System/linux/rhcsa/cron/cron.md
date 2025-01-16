# RHCSA Cron job

[Back](../../index.md)

- [RHCSA Cron job](#rhcsa-cron-job)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
Set The Cron Job for the user "Natasha" that should runs daily every 1 minutes local time and executes "Ex200 Testing" with logger.
```

---

### Solution

```sh
# ensure service is
systemctl status crond
# ● crond.service - Command Scheduler
#      Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; preset: enabled)
#      Active: active (running) since Mon 2025-01-13 12:15:53 EST; 50min ago
#    Main PID: 1006 (crond)
#       Tasks: 2 (limit: 10748)
#      Memory: 1.5M
#         CPU: 69ms
#      CGroup: /system.slice/crond.service
#              ├─1006 /usr/sbin/crond -n
#              └─6298 /usr/sbin/anacron -s

crontab -e -u natasha
*/1 * * * * logger "Ex200 Testing"
# if a given time per date
10 13 * * * logger "Ex200 Testing"


# confirm
crontab -l -u natasha
# check log
journalctl -f
tail -f /var/log/messages
tail -f /var/log/syslog
```
