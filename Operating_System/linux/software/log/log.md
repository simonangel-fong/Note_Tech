# Linux - Software Management: Log

[Back](../../index.md)

- [Linux - Software Management: Log](#linux---software-management-log)
  - [Log](#log)
  - [Default Logging Daemon](#default-logging-daemon)
    - [`journald daemon`](#journald-daemon)
    - [`rsyslogd daemon`](#rsyslogd-daemon)
  - [Common Log Files](#common-log-files)
  - [Service Log](#service-log)

---

## Log

- `Log files`
  - files that contain **messages about the system**, including the kernel, services, and applications running on it.
  - can be used to troubleshoot a problem
- There are **different** log files for different information.

  - For example, there is a **default system** log file, a log file just for **security messages**, and a log file for **cron tasks**.

- Log File Location

- `/var/log/`:
  - Most log files
  - Some applications
    - e.g., `httpd`, `samba`

---

## Default Logging Daemon

- By **default**, these **2** logging tools **coexist** on your system.

  - `journald`
  - `rsyslogd`

---

### `journald daemon`

- `journald daemon`

  - a component of `systemd` to manage log files
  - the **primary tool** for troubleshooting
  - used to **captures and indexes**
    - `Syslog` messages,
    - **kernel** log messages,
    - initial RAM disk and early **boot** messages
    - messages written to `standard output` and `standard error output` of all services
  - provides additional data necessary for creating structured log messages
    - Data acquired by `journald` is forwarded into the `/run/systemd/journal/socket` that may be used by `rsyslogd` to process the data further.

- `systemd journal file`

  - a structured and **indexed binary file**
  - stores meta data information like **time stamps** or **user IDs**.
  - improves searching and provides faster operation

- `journald` log file:

  - **By default not persistent**:
    - stored only **in memory** or a small **ring-buffer** in the `/run/log/journal/` directory.
      - The amount of logged data **depends on free memory**, when you reach the capacity limit, the oldest entries are deleted.
  - **Persistent location**: `/var/log/`

---

### `rsyslogd daemon`

- `rsyslogd`

  - a daemon controls log files.
  - an enhanced replacement for `sysklogd`

- Configuration file of `rsyslogd`:
  - `/etc/rsyslog.conf`

---

## Common Log Files

- Most log files located at `/var/log/`

- `/var/log/boot.log` / `/var/log/boot.log-<date>`

  - a Linux log file that contains information about the **server's startup process**, including messages that are logged as the server starts up.
  - This log file is useful for diagnosing issues with a system's boot.

- `/var/log/chrony/`

  - a directory to store `Chrony` logs
  - `Network Time Protocol (NTP)`
    - a protocol that allows the synchronization of system clocks
  - `chronyd`
    - a tool that synchronizes the time of a system with a `Network Time Protocol (NTP)` server

- `/var/log/cron`

  - stores cron logs for CentOS and RHEL systems

- `/var/log/maillog`

  - used for mail server logs, handy for postfix, smtpd, or email-related services info running on server.

- `/var/log/secure`

  - contains information related to **authentication** and **authorization** privileges.

- `/var/log/message`

  - Contains global **system messages**, including the messages that are logged during system startup.

```sh
# find the error message in the system
grep -i error /var/log/messages
```

- `/var/log/nginx`
  - a directory is the default location for NGINX log files
  - two types of logs in this directory:
    - `access_log`: Stores information about web **client requests**, such as which pages users are requesting
    - `error_log`: Stores other unexpected or informative messages

---

## Service Log

```sh
journalctl -u service_name
```

---

[TOP](#linux---software-management-log)
