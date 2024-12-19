# Linux - Software Management: Log

[Back](../../index.md)

- [Linux - Software Management: Log](#linux---software-management-log)
  - [Log](#log)
  - [Default Logging Daemon](#default-logging-daemon)
    - [`journald daemon`](#journald-daemon)
    - [`rsyslogd daemon`](#rsyslogd-daemon)
  - [Common Log Files](#common-log-files)
  - [Service Log](#service-log)
  - [Get Support from Redhat](#get-support-from-redhat)

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

- `/var/log/messages`

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

## Get Support from Redhat

- To get support from Redhat, the system administrator can run the untility `sosreport` or `sos report` which will collect the logs and configuration file and transfer them over to the Redhat support server.
- Can use Cockpit app to generate the report at the web-based portal.

```sh
sos report
# sos report (version 4.8.1)
#
# This command will collect diagnostic and configuration information from
# this Red Hat Enterprise Linux system and installed applications.
#
# An archive containing the collected information will be generated in
# /var/tmp/sos.bdqjxjl0 and may be provided to a Red Hat support
# representative.
#
# Any information provided to Red Hat will be treated in accordance with
# the published support policies at:
#
#         Distribution Website : https://www.redhat.com/
#         Commercial Support   : https://access.redhat.com/
#
# The generated archive may contain data considered sensitive and its
# content should be reviewed by the originating organization before being
# passed to any third party.
#
# No changes will be made to system configuration.
#
# Press ENTER to continue, or CTRL-C to quit.
# ...
# Running plugins. Please wait ...
#
#   Finishing plugins              [Running: subscription_manager]                          ]h]d]
#   Finished running plugins
# Creating compressed archive...
#
# Your sos report has been generated and saved in:
#         /var/tmp/sosreport-clienthost-54353-2024-12-14-ttdzzri.tar.xz
#
#  Size   16.12MiB
#  Owner  root
#  sha256 a3657fa92bfc982427ca0fad81b4f823f9da0185739766d1007336872a7d300c
#
# Please send this file to your support representative.
```

---

[TOP](#linux---software-management-log)
