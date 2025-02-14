# Linux - System: Log

[Back](../../index.md)

- [Linux - System: Log](#linux---system-log)
  - [Log](#log)
    - [Common Log File](#common-log-file)
  - [Default Logging Daemon](#default-logging-daemon)
    - [`journald daemon`](#journald-daemon)
    - [`rsyslogd daemon`](#rsyslogd-daemon)
  - [Common Log Files](#common-log-files)
  - [Service Log](#service-log)
  - [Get Support from Redhat](#get-support-from-redhat)
  - [Help](#help)

---

## Log

- `Log files`
  - files that contain **messages about the system**, including the kernel, services, and applications running on it.
  - can be used to troubleshoot a problem
- There are **different** log files for different information.

  - For example, there is a **default system** log file, a log file just for **security messages**, and a log file for **cron tasks**.

---

### Common Log File

- Most system logs are stored in `/var/log/`.
- Common log files include:

| Log File                    | Description                           |
| --------------------------- | ------------------------------------- |
| `/var/log/messages`         | General system logs                   |
| `/var/log/secure`           | Authentication & security logs        |
| `/var/log/boot.log`         | Boot process logs                     |
| `/var/log/dnf.log`          | Package management logs               |
| `/var/log/cron`             | Cron job logs                         |
| `/var/log/chrony/`          | a directory to store `Chrony` logs    |
| `/var/log/maillog`          | Mail server logs(postfix, smtpd, ...) |
| `/var/log/httpd/access.log` | Apache web server access log          |
| `/var/log/httpd/error.log`  | Apache error log                      |
| `/var/log/mysql.log`        | MySQL database log                    |
| `/var/log/audit/audit.log`  | SELinux & security audit logs         |

---

## Default Logging Daemon

- By **default**, these **2** logging tools **coexist** on your system.

  - `journald`:
    - the default logging system in RHEL 9.
  - `rsyslogd`:
    - Traditional Syslog
    - RHEL 9 still supports rsyslog for compatibility.

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

## Help

- Manual pages
  - online documentation that provides details on commands, configuration files, etc.
  - installed under the `/usr/share/man` directory when associated software packages are installed.

```sh
ls /usr/share/man
# ca  es  it     man1   man2type   man3head  man4   man6   man8   mann       pt     sr  zh_CN
# cs  fr  ja     man1p  man2x      man3p     man4x  man6x  man8x  nl         pt_BR  sv  zh_TW
# da  hu  ko     man1x  man3       man3type  man5   man7   man9   overrides  ru     tr
# de  id  man0p  man2   man3const  man3x     man5x  man7x  man9x  pl         sk     uk
```

- man

```sh
# build an indexed database of the manual pages.
mandb
# Purging old database entries in /usr/share/man/overrides...
# Processing manual pages under /usr/share/man/overrides...
# Purging old database entries in /usr/share/man...
# Processing manual pages under /usr/share/man...
# Purging old database entries in /usr/share/man/overrides...
# Processing manual pages under /usr/share/man/overrides...
# Purging old database entries in /usr/share/man/ru...
# Processing manual pages under /usr/share/man/ru...
# Purging old database entries in /usr/share/man/cs...
# Processing manual pages under /usr/share/man/cs...
# Purging old database entries in /usr/share/man/da...
# Processing manual pages under /usr/share/man/da...
# Purging old database entries in /usr/share/man/de...
# Processing manual pages under /usr/share/man/de...
# Purging old database entries in /usr/share/man/fr...
# Processing manual pages under /usr/share/man/fr...
# Purging old database entries in /usr/share/man/hu...
# Processing manual pages under /usr/share/man/hu...
# Purging old database entries in /usr/share/man/id...
# Processing manual pages under /usr/share/man/id...
# Purging old database entries in /usr/share/man/it...
# Processing manual pages under /usr/share/man/it...
# Purging old database entries in /usr/share/man/ja...
# Processing manual pages under /usr/share/man/ja...
# Purging old database entries in /usr/share/man/ko...
# Processing manual pages under /usr/share/man/ko...
# Purging old database entries in /usr/share/man/pl...
# Processing manual pages under /usr/share/man/pl...
# Purging old database entries in /usr/share/man/pt_BR...
# Processing manual pages under /usr/share/man/pt_BR...
# Purging old database entries in /usr/share/man/sv...
# Processing manual pages under /usr/share/man/sv...
# Purging old database entries in /usr/share/man/tr...
# Processing manual pages under /usr/share/man/tr...
# Purging old database entries in /usr/share/man/zh_CN...
# Processing manual pages under /usr/share/man/zh_CN...
# Purging old database entries in /usr/share/man/zh_TW...
# Processing manual pages under /usr/share/man/zh_TW...
# Purging old database entries in /usr/share/man/uk...
# Processing manual pages under /usr/share/man/uk...
# Purging old database entries in /usr/share/man/es...
# Processing manual pages under /usr/share/man/es...
# Purging old database entries in /usr/share/man/nl...
# Processing manual pages under /usr/share/man/nl...
# Purging old database entries in /usr/share/man/ca...
# Processing manual pages under /usr/share/man/ca...
# Purging old database entries in /usr/share/man/sk...
# Processing manual pages under /usr/share/man/sk...
# Purging old database entries in /usr/share/man/pt...
# Processing manual pages under /usr/share/man/pt...
# Purging old database entries in /usr/share/man/sr...
# Processing manual pages under /usr/share/man/sr...
# Purging old database entries in /usr/local/share/man...
# Processing manual pages under /usr/local/share/man...
# 0 man subdirectories contained newer manual pages.
# 0 manual pages were added.
# 0 stray cats were added.
# 0 old database entries were purged.

#  search for a string “xfs”
man -k xfs
# attr (1)             - extended attributes on XFS filesystem objects
# filesystems (5)      - Linux filesystem types: ext, ext2, ext3, ext4, hpfs, iso9660, JFS, minix...
# fs (5)               - Linux filesystem types: ext, ext2, ext3, ext4, hpfs, iso9660, JFS, minix...
# fsck.xfs (8)         - do nothing, successfully
# fsfreeze (8)         - suspend access to a filesystem (Ext3/4, ReiserFS, JFS, XFS)
# mkfs.xfs (8)         - construct an XFS filesystem
# xfs (5)              - layout, mount options, and supported file attributes for the XFS filesystem
# xfs_admin (8)        - change parameters of an XFS filesystem
# xfs_bmap (8)         - print block mapping for an XFS file
# xfs_copy (8)         - copy the contents of an XFS filesystem
# xfs_db (8)           - debug an XFS filesystem
# xfs_estimate (8)     - estimate the space that an XFS filesystem will take
# xfs_freeze (8)       - suspend access to an XFS filesystem
# xfs_fsr (8)          - filesystem reorganizer for XFS
# xfs_growfs (8)       - expand an XFS filesystem
# xfs_info (8)         - display XFS filesystem geometry information
# xfs_io (8)           - debug the I/O path of an XFS filesystem
# xfs_logprint (8)     - print the log of an XFS filesystem
# xfs_mdrestore (8)    - restores an XFS metadump image to a filesystem image
# xfs_metadump (8)     - copy XFS filesystem metadata to a file
# xfs_mkfile (8)       - create an XFS file
# xfs_ncheck (8)       - generate pathnames from i-numbers for XFS
# xfs_quota (8)        - manage use of quota on XFS filesystems
# xfs_repair (8)       - repair an XFS filesystem
# xfs_rtcp (8)         - XFS realtime copy command
# xfs_spaceman (8)     - show free space information about an XFS filesystem
# xfsdump (8)          - XFS filesystem incremental dump utility
# xfsinvutil (8)       - xfsdump inventory database checking and pruning utility
# xfsrestore (8)       - XFS filesystem incremental restore utility
# xqmstats (8)         - Display XFS quota manager statistics from /proc
```

- whatis: searches for a short description of the specified command or file in the manual database.

```sh
whatis yum.conf
# yum.conf (5)         - redirecting to DNF Configuration Reference
whatis passwd
# passwd (5)           - password file
# passwd (1ossl)       - OpenSSL application commands
# passwd (1)           - update user's authentication tokens

# same as
man -f yum.conf
# yum.conf (5)         - redirecting to DNF Configuration Reference
man -f passwd
# passwd (5)           - password file
# passwd (1ossl)       - OpenSSL application commands
# passwd (1)           - update user's authentication tokens
```

---

[TOP](#linux---software-management-log)
