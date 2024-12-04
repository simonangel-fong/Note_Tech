# Linux - System Management

[Back](../../index.md)

- [Linux - System Management](#linux---system-management)
  - [`systemd`](#systemd)
    - [Unit File](#unit-file)
    - [`systemctl` and `service` Command](#systemctl-and-service-command)
  - [`systemd` Management](#systemd-management)
  - [Service Management](#service-management)
    - [Start/Stop a service](#startstop-a-service)
      - [Start a Service](#start-a-service)
      - [Stop a Service](#stop-a-service)
    - [Enable/Disable a Service](#enabledisable-a-service)
      - [Enable a Service](#enable-a-service)
      - [Disable a Service](#disable-a-service)
    - [Mask/Unmask a Service](#maskunmask-a-service)
      - [Mask a Service](#mask-a-service)
      - [Unmask a Service](#unmask-a-service)
  - [Example: Manage `nginx`](#example-manage-nginx)
    - [Install `nginx` Package](#install-nginx-package)
    - [Start/Stop `nginx`](#startstop-nginx)
    - [Enable/Disable `nginx`](#enabledisable-nginx)
    - [Mask/Unmask `nginx`](#maskunmask-nginx)
    - [Clear up](#clear-up)
  - [System Information](#system-information)
    - [System Time](#system-time)
      - [Lab: Configure `chronyd`](#lab-configure-chronyd)

---

## `systemd`

- `systemd`

  - a **system and service manager** for Linux operating systems.
  - designed to be backwards compatible with `SysV init scripts`
  - provides a number of features such as

    - parallel startup of system services at boot time,
    - on-demand activation of daemons,
    - or dependency-based service control logic.

  - acts as the **init system** that brings up and maintains user space services when run as the **first process on boot**
  - PID: `1`
    - known as `init` and is the **first** Linux **user-mode process** created
    - if it is killed, the entire OS will be kill, because all the other of services depends on `systemd`.

- `systemd units`

  - represented by `unit configuration files` located in one of the directories,
  - encapsulate information about system services, listening sockets, and other objects that are relevant to the init system.

---

### Unit File

- Systemd `Unit Files Locations`

| Directory                  | Created                                                 | Precedence                             |
| -------------------------- | ------------------------------------------------------- | -------------------------------------- |
| `/usr/lib/systemd/system/` | By **installed RPM packages**.                          | -                                      |
| `/run/systemd/system/`     | At **run time**.                                        | over installed **service** unit files. |
| `/etc/systemd/system/`     | by `systemctl enable` and added for extending a service | over **runtime** unit files.           |

- Available `systemd Unit` Types

| Unit Type      | File Extension | Description                                                             |
| -------------- | -------------- | ----------------------------------------------------------------------- |
| Service unit   | `.service`     | A system service.                                                       |
| Target unit    | `.target`      | A group of systemd units.                                               |
| Automount unit | `.automount`   | A file system automount point.                                          |
| Device unit    | `.device`      | A device file recognized by the kernel.                                 |
| Mount unit     | `.mount`       | A file system mount point.                                              |
| Path unit      | `.path`        | A file or directory in a file system.                                   |
| Scope unit     | `.scope`       | An externally created process.                                          |
| Slice unit     | `.slice`       | A group of hierarchically organized units that manage system processes. |
| Snapshot unit  | `.snapshot`    | A saved state of the systemd manager.                                   |
| Socket unit    | `.socket`      | An inter-process communication socket.                                  |
| Swap unit      | `.swap`        | A swap device or a swap file.                                           |
| Timer unit     | `.timer`       | A systemd timer.                                                        |

- `unit file` status:

  - **enabled**: The unit is enabled to **start automatically at boot**.
  - **disabled**: The unit is disabled and will **not start automatically at boot**.
  - **static**: The unit is not directly enabled or disabled, but it is **pulled in by other units when needed**.
  - **masked**: The unit is **masked and cannot be started**, either manually or automatically.

- units columns:
  - **UNIT**:
    - The name of the unit.
  - **LOAD**:
    - The **load status** of the unit.
    - This indicates **whether the unit is successfully loaded into memory**.
  - **ACTIVE**:
    - The **current state** of the unit.
    - This shows whether the unit is **active (running)**, **inactive (stopped)**, or in another state.
  - **SUB**:
    - The **sub-state** of the unit, which provides more specific information about its status.
  - **DESCRIPTION**:
    - A short description of the unit, usually indicating its purpose.

---

```sh
# get unit status for a specific system unit
systemctl list-units | grep firewalld

# get all unit file enabled at boot.
systemctl list-unit-files | grep enabled
# get all unit file disabled at boot.
systemctl list-unit-files | grep disabled
# get all unit file sattic at boot.
systemctl list-unit-files | grep sattic
# get all unit file masked at boot.
systemctl list-unit-files | grep masked
```

---

### `systemctl` and `service` Command

- `systemctl`

  - the command-line interface used to **interact with systemd**.
  - allows administrators to manage and query system services and states.

- `service` command
  - run a `System V init script`
  - `/etc/init.d`: The directory containing System V init scripts.

---

## `systemd` Management

| CMD                                        | DESC                                                 |
| ------------------------------------------ | ---------------------------------------------------- |
| `systemctl --version`                      | Used to check if the systemd installed               |
| `ps -ef \| grep systemd`                   | Used to check if the systemd running                 |
| `systemctl --all` / `systemctl list-units` | Display all available systemd units                  |
| `systemctl list-unit-files`                | List all unit files                                  |
| `systemctl reboot`                         | Reboots a Linux system                               |
| `systemctl poweroff`                       | Shut down the system                                 |
| `systemctl get-default`                    | View the current default target                      |
| `systemctl set-default <target_name>`      | Change the default target                            |
| `systemctl set-default graphical.target`   | Set the system to boot into a graphical environment. |
| `systemctl isolate rescue.target`          | Switch to Rescue Mode                                |

---

- Services vs packages

```sh
# shows installed software packages and their versions.
rpm -qa
rpm -qa | wc -l

# shows the status of services and other systemd units
systemctl --all

```

- `systemctl list-unit` vs `systemctl list-unit-files`

| Command                     | Output                                    | Use Case                                 |
| --------------------------- | ----------------------------------------- | ---------------------------------------- |
| `systemctl list-units`      | Lists **active units** and current states | Which units currently active or inactive |
| `systemctl list-unit-files` | Lists `unit files` and states             | Which services to **start at boot**      |

---

## Service Management

| CMD                                 | DESC                                                  |
| ----------------------------------- | ----------------------------------------------------- |
| `systemctl show unit_name`          | Show the service's properties                         |
| `systemctl status service_name`     | Check the status of a service                         |
| `systemctl start service_name`      | Start a service                                       |
| `systemctl stop service_name`       | Stop a service                                        |
| `systemctl reload service_name`     | Reload the configuration of a service                 |
| `systemctl restart service_name`    | Stop and Start a service after a configuration change |
| `systemctl is-enabled service_name` | Check if a service is enabled                         |
| `systemctl enable service_name`     | Enable a service at boot time                         |
| `systemctl disable service_name`    | Disable a service at boot time                        |
| `systemctl mask service_name`       | Disable a service completely including dependencies   |
| `systemctl unmask service_name`     | Enable a service completely including dependencies    |

---

### Start/Stop a service

#### Start a Service

- `systemctl start service_name` command

  - used to **start a service immediately** on a system managed by `systemd`.

- 1. **Unit Activation**

  - The `systemd manager` **reads** the service's `unit file` (usually located in `/usr/lib/systemd/system/` or `/etc/systemd/system/`) to determine how to start the service.

- 2. **Dependency Resolution**

  - `systemd` checks for and activates any **dependencies** required by the service (defined in the `Requires=` or `Wants=` directives of the unit file).
  - If the service **depends** on other services or system targets, they are **started first**.

- 3. **Service Initialization**

  - `systemd` **executes the commands** specified in the `[Service]` section of the `unit file`.
  - This often includes:
    - Running the `ExecStart=` command to **initialize the service**.
    - Setting up **environment variables**, if specified in the `unit file`.

- 4. **Immediate Effect**
  - The service **starts immediately** and runs in the current session.
  - This does **not affect** the service's **startup behavior** after a reboot unless you also use the enable command.

---

#### Stop a Service

- `systemctl stop service_name` command

  - used to **stop** a running service **immediately** on a system managed by `systemd`.

- **Service Termination**
  - `systemd` **sends a signal** to the service's main process to **terminate** it.
  - By default, it uses the `SIGTERM` signal, but this can be **overridden** in the `unit file`.
- **Stops Related Services**
  - If the service has **dependencies** defined in the `unit file` (e.g., `Requires=` or `PartOf=`), they may also be stopped, depending on the configuration.
- **Updates Service State**
  - The service's state **changes** to `inactive`. This means it is no longer running.

---

### Enable/Disable a Service

#### Enable a Service

- `systemctl enable service_name` command

  - the system sets up the specified service (service_name) to **start automatically at boot time**.

- **Creation of Symlinks**

  - The command **creates symbolic links** in the appropriate systemd target directory (e.g., `/etc/systemd/system/<target>.wants/`).
  - These links point to the service's `unit file`, usually located in `/usr/lib/systemd/system/` or `/etc/systemd/system/`.
    - `/etc/systemd/system/multi-user.target.wants/httpd.service -> /usr/lib/systemd/system/httpd.service`

- **Service Dependency Configuration**

  - The system associates the service with a **specific target**, such as `multi-user.target` (typically equivalent to runlevel 3 or 5 in traditional init systems).
  - This ensures the service **starts** when the system **reaches the specified target** during boot.

- **Persistence**
  - The change is persistent, meaning the service will start automatically at every subsequent boot, even after a system reboot.

---

#### Disable a Service

- `systemctl disable service_name` command

  - the service is **disabled**
  - it will **no** longer start **automatically** at boot time.
  - However, the service can still be **started manually** or by another **service** that **depends** on it.

- **Removes Symlinks**
  - The command **removes the symbolic links** that were created when the service was enabled.
  - These symlinks are located in the `target directory` (e.g., `/etc/systemd/system/<target>.wants/`).
    - `/etc/systemd/system/multi-user.target.wants/httpd.service`
- **Stops Automatic Startup**

  - The service will no longer start automatically when the system boots into the **specified target** (like `multi-user.target` or `graphical.target`).

- **Service Remains Available**
  - The service is not completely disabled. You can still:
    - Start it **manually** using `systemctl start service_name`.
    - Start it **automatically if triggered** by another service

---

### Mask/Unmask a Service

#### Mask a Service

- `systemctl mask service_name`

  - To mask a service.
  - the service is completely **disabled** and cannot be started, either manually or automatically, **even by another service that depends on it**.

- **Symlink Creation to `/dev/null`**
  - The `systemctl mask` command **creates a symbolic link** for the service unit file that **points to** `/dev/null`.
  - `/etc/systemd/system/service_name.service -> /dev/null`
  - This effectively prevents the service from being started, as the system **cannot read the configuration** for the service unit.
- **Overrides Enablement**
  - Even if the service is enabled or has dependencies set up, **masking overrides** them, ensuring the service cannot start.
- **Prevents Manual Starts**
  - Attempting to **start** a masked service **manually** with `systemctl start service_name` will **fail** with an error:
  - `Failed to start service_name.service: Unit service_name.service is masked.`

---

#### Unmask a Service

- `systemctl unmask service_name` command

  - it **removes the masking** from a service, allowing it to be **started again manually**, **automatically**, or by other **dependent services**.

- **Removes the Symlink to `/dev/null`**

  - `systemctl mask service_name`: its unit file is **replaced** with a **symbolic link** pointing to `/dev/null`.
    - This **prevents** the service from **starting**.
  - `systemctl unmask service_name` **removes** this symlink, **restoring** the ability for the system to **access the original `unit file`**.

- **Restores Service Availability**

  - After unmasking, the service can be:
    - **Started manually** (`systemctl start service_name`).
    - **Enabled** to **start at boot** (`systemctl enable service_name`).
    - **Started by dependent** services if required.

- **Does Not Automatically Enable or Start the Service**
  - Unmasking does not re-enable or start the service. You **must explicitly enable or start** it if needed.

---

## Example: Manage `nginx`

### Install `nginx` Package

```sh
su -

dnf update -y
dnf upgrade -y
dnf install nginx -y

# confirm
rpm -qa | grep nginx
# nginx-mod-http-image-filter-1.14.1-9.module+el8.0.0+4108+af250afe.x86_64
# nginx-1.14.1-9.module+el8.0.0+4108+af250afe.x86_64
# nginx-mod-http-xslt-filter-1.14.1-9.module+el8.0.0+4108+af250afe.x86_64
# nginx-mod-stream-1.14.1-9.module+el8.0.0+4108+af250afe.x86_64
# nginx-filesystem-1.14.1-9.module+el8.0.0+4108+af250afe.noarch
# nginx-mod-mail-1.14.1-9.module+el8.0.0+4108+af250afe.x86_64
# nginx-all-modules-1.14.1-9.module+el8.0.0+4108+af250afe.noarch
# nginx-mod-http-perl-1.14.1-9.module+el8.0.0+4108+af250afe.x86_64
systemctl list-unit-files | grep nginx
# nginx.service                              disabled
```

---

### Start/Stop `nginx`

```sh
systemctl show nginx
# Type=forking
# Restart=no
# PIDFile=/run/nginx.pid
# NotifyAccess=none
# RestartUSec=100ms
# TimeoutStartUSec=1min 30s
# TimeoutStopUSec=5s
# RuntimeMaxUSec=infinity
# WatchdogUSec=0
# ...

systemctl --all | grep nginx
# none
systemctl start nginx
# display status
systemctl status nginx
# ● nginx.service - The nginx HTTP and reverse proxy server
#    Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; vendor preset: disabled)
#    Active: active (running) since Sun 2024-12-01 00:46:26 EST; 1min 26s ago
#   Process: 73366 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
#   Process: 73364 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
#   Process: 73362 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
#  Main PID: 73367 (nginx)
#     Tasks: 9 (limit: 22878)
#    Memory: 16.6M
#    CGroup: /system.slice/nginx.service
#            ├─73367 nginx: master process /usr/sbin/nginx
#            ├─73368 nginx: worker process
#            ├─73369 nginx: worker process
#            ├─73370 nginx: worker process
#            ├─73371 nginx: worker process
#            ├─73372 nginx: worker process
#            ├─73373 nginx: worker process
#            ├─73374 nginx: worker process
#            └─73375 nginx: worker process

# Dec 01 00:46:26 rhelhost.localdomain systemd[1]: Starting The nginx HTTP and reverse proxy server.>
# Dec 01 00:46:26 rhelhost.localdomain nginx[73364]: nginx: the configuration file /etc/nginx/nginx.>
# Dec 01 00:46:26 rhelhost.localdomain nginx[73364]: nginx: configuration file /etc/nginx/nginx.conf>
# Dec 01 00:46:26 rhelhost.localdomain systemd[1]: Started The nginx HTTP and reverse proxy server.
systemctl --all | grep nginx
# nginx.service    loaded    active   running   The nginx HTTP and reverse proxy server
# verify
curl 127.0.0.1
# return the default nginx website

# stop service
systemctl stop nginx
# display status
systemctl status nginx
# ● nginx.service - The nginx HTTP and reverse proxy server
#    Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; vendor preset: disabled)
#    Active: inactive (dead)

# Dec 01 00:36:22 rhelhost.localdomain systemd[1]: nginx.service: Unit cannot be reloaded because it>
# Dec 01 00:46:26 rhelhost.localdomain systemd[1]: Starting The nginx HTTP and reverse proxy server.>
# Dec 01 00:46:26 rhelhost.localdomain nginx[73364]: nginx: the configuration file /etc/nginx/nginx.>
# Dec 01 00:46:26 rhelhost.localdomain nginx[73364]: nginx: configuration file /etc/nginx/nginx.conf>
# Dec 01 00:46:26 rhelhost.localdomain systemd[1]: Started The nginx HTTP and reverse proxy server.
# Dec 01 00:56:03 rhelhost.localdomain systemd[1]: Stopping The nginx HTTP and reverse proxy server.>
# Dec 01 00:56:03 rhelhost.localdomain systemd[1]: nginx.service: Succeeded.
# Dec 01 00:56:03 rhelhost.localdomain systemd[1]: Stopped The nginx HTTP and reverse proxy server.
systemctl --all | grep nginx
# none
curl 127.0.0.1
# curl: (7) Failed to connect to 127.0.0.1 port 80: Connection refused

```

---

### Enable/Disable `nginx`

```sh
# Check link before operations
ll /etc/systemd/system/multi-user.target.wants | grep nginx*
# none
ll /etc/systemd/system/ | grep nginx*
# drwxr-xr-x. 2 root root    6 Aug 30  2019 nginx.service.d

systemctl enable nginx.service
# Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.
systemctl is-enabled nginx.service
# enabled
systemctl list-unit-files | grep nginx.service
# nginx.service                              enabled
ll /etc/systemd/system/multi-user.target.wants | grep nginx*
# lrwxrwxrwx. 1 root root 37 Dec  1 00:38 nginx.service -> /usr/lib/systemd/system/nginx.service
ll /etc/systemd/system/ | grep nginx*
# drwxr-xr-x. 2 root root    6 Aug 30  2019 nginx.service.d

systemctl disable nginx.service
# Removed /etc/systemd/system/multi-user.target.wants/nginx.service.
systemctl is-enabled nginx.service
# disabled
systemctl list-unit-files | grep nginx.service
# nginx.service                              disabled
ll /etc/systemd/system/multi-user.target.wants | grep nginx*
# none
ll /etc/systemd/system/ | grep nginx*
# drwxr-xr-x. 2 root root    6 Aug 30  2019 nginx.service.d
```

---

### Mask/Unmask `nginx`

```sh
systemctl mask nginx.service
# Created symlink /etc/systemd/system/nginx.service → /dev/null.
systemctl list-unit-files | grep nginx.service
# nginx.service                              masked
ll /etc/systemd/system/multi-user.target.wants | grep nginx*
# none
ll /etc/systemd/system/ | grep nginx*
# lrwxrwxrwx. 1 root root    9 Dec  1 00:41 nginx.service -> /dev/null
# drwxr-xr-x. 2 root root    6 Aug 30  2019 nginx.service.d

systemctl unmask nginx.service
# Removed /etc/systemd/system/nginx.service.
systemctl list-unit-files | grep nginx.service
# nginx.service                              disabled
ll /etc/systemd/system/multi-user.target.wants | grep nginx*
# none
ll /etc/systemd/system/ | grep nginx*
# drwxr-xr-x. 2 root root    6 Aug 30  2019 nginx.service.d
```

---

### Clear up

```sh
dnf remove -y nginx
ll /etc/systemd/system/ | grep nginx*
# none
```

---

## System Information

| Command              | Description                                           |
| -------------------- | ----------------------------------------------------- |
| `uptime`             | how long the system has been running                  |
| `uptime -p`          | show uptime in pretty format                          |
| `uptime -s`          | system up since                                       |
| `hostnamectl`        | query the system hostname                             |
| `hostnamectl status` | Show current system hostname and related information. |
| `set-hostname NAME`  | Set the system hostname to NAME.                      |

---

### System Time

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

- chronyc command

| CMD       | Desc                    |
| --------- | ----------------------- |
| `help`    | Show help info          |
| `sources` | Show current NTP server |
| `quit`    | Exit current session    |

---

#### Lab: Configure `chronyd`

```sh
su -

# confirm package installed
rpm -qa | grep chrony
# chrony-4.5-2.el8_10.x86_64

# change configuration
vi /etc/chrony.conf
# make some changes for the NTP server
# 8.8.8.8 is not a valid NTP server
pool 8.8.8.8

# restart service
systemctl restart chronyd
systemctl status chronyd

# start a chrony session
chronyc

sources
# MS Name/IP address         Stratum Poll Reach LastRx Last sample
# ===============================================================================
# ^? dns.google                    0   6     0     -     +0ns[   +0ns] +/-    0ns
# ^- 23.133.168.247                4   6    17    58  -1194us[-1194us] +/-   46ms
# ^* 64.ip-54-39-23.net            2   6    17    64   -191us[ -831us] +/-   19ms
# ^- 155.138.150.39.vultruser>     3   6    17    63   -421us[ -421us] +/-   32ms
# ^+ hub.coreserv.net              2   6    17    64  -2015us[-2656us] +/-   51ms

quit

# Remove the 8.8.8.8 entry
vi /etc/chrony.conf

# restart service
systemctl restart chronyd
systemctl status chronyd
```

---

[TOP](#linux---system-management)
