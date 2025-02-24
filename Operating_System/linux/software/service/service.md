# Linux - Software: Service

[Back](../../index.md)

- [Linux - Software: Service](#linux---software-service)
  - [Service](#service)
  - [`systemd`](#systemd)
    - [Unit File](#unit-file)
    - [`systemctl` and `service` Command](#systemctl-and-service-command)
  - [`systemd` Management](#systemd-management)
  - [Unit Management](#unit-management)
  - [Service Units Management](#service-units-management)
  - [Target Unit Management](#target-unit-management)
    - [Lab: Change target](#lab-change-target)
      - [Default target](#default-target)
      - [Switch currrent target](#switch-currrent-target)
    - [Start/Stop a service](#startstop-a-service)
      - [Start a Service](#start-a-service)
      - [Stop a Service](#stop-a-service)
    - [Enable/Disable a Service](#enabledisable-a-service)
      - [Enable a Service](#enable-a-service)
      - [Disable a Service](#disable-a-service)
    - [Mask/Unmask a Service](#maskunmask-a-service)
      - [Mask a Service](#mask-a-service)
      - [Unmask a Service](#unmask-a-service)
  - [Lab: Manage `nginx`](#lab-manage-nginx)
    - [Install `nginx` Package](#install-nginx-package)
    - [Start/Stop `nginx`](#startstop-nginx)
    - [Enable/Disable `nginx`](#enabledisable-nginx)
    - [Mask/Unmask `nginx`](#maskunmask-nginx)
    - [Clear up](#clear-up)
  - [Service Log](#service-log)

---

## Service

- `service`

  - a `background process` that performs **specific system tasks** or provides a particular **functionality**.
  - These services are typically **started automatically** during the system boot process and continue running in the background, waiting for requests or events to respond to.

- Features

  - **Background Process**:
    - Runs **without user interaction**.
  - **Managed by System Daemons**:
    - Handled by init systems like systemd, SysVinit, or Upstart.
  - **Essential for System Functionality**:
    - Examples include network management (NetworkManager), file sharing (NFS), and web servers (httpd).

- Common Types of Linux Services
  - Networking:
    - `network`, `ssh`, `firewalld`
  - Web Servers:
    - `apache2`, `nginx`
  - Database Servers:
    - `mysqld`, `postgresql`
  - File Sharing:
    - `nfs`, `smb`
  - System Tools:
    - `cron`, `syslog`

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

| CMD                                        | DESC                                   |
| ------------------------------------------ | -------------------------------------- |
| `systemctl --version`                      | Used to check if the systemd installed |
| `ps -ef \| grep systemd`                   | Used to check if the systemd running   |
| `systemctl --all` / `systemctl list-units` | Display all available systemd units    |
| `systemctl list-unit-files`                | List all unit files                    |

---

- Services vs packages

```sh
# shows installed software packages and their versions.
rpm -qa
rpm -qa | wc -l

# shows the status of services and other systemd units
systemctl --all

```

---

## Unit Management

| CMD                                  | DESC                                                 |
| ------------------------------------ | ---------------------------------------------------- |
| `systemctl` / `systemctl list-units` | Lists **active units(in memory)** and current states |
| `systemctl list-units -a`            | Lists all units, active + inactive                   |
| `systemctl list-units -t socket`     | Lists all socke type unit                            |
| `systemctl list-units --failed`      | Lists all failed unit at last system boot            |
| `systemctl list-unit-files`          | Lists `unit files` and states                        |
| `systemctl list-sockets`             | Lists units of type socket                           |
| `systemctl list-dependencies`        | Lists dependency tree for all unit                   |
| `systemctl list-dependencies crond`  | Lists dependency tree for a unit                     |
| `systemctl show`                     | Show all properties                                  |
| `systemctl show crond`               | Show the service's properties                        |

## Service Units Management

| CMD                               | DESC                                                  |
| --------------------------------- | ----------------------------------------------------- |
| `systemctl list-units -t service` | Lists all serivces type unit                          |
| `systemctl daemon-reload`         | Re-reads and reloads all unit configuration files     |
| `systemctl status crond`          | Check the status of a service                         |
| `systemctl is-enabled crond`      | Check if a service is enabled                         |
| `systemctl is-active crond`       | Checks whether a unit is running                      |
| `systemctl is-failed crond`       | Checks whether a unit is in the failed state          |
| `systemctl start crond`           | Start a service                                       |
| `systemctl stop crond`            | Stop a service                                        |
| `systemctl reload crond`          | Reload the configuration of a service                 |
| `systemctl restart crond`         | Stop and Start a service after a configuration change |
| `systemctl enable crond`          | Enable a service at boot time                         |
| `systemctl disable crond`         | Disable a service at boot time                        |
| `systemctl mask crond`            | Disable a service completely including dependencies   |
| `systemctl unmask crond`          | Enable a service completely including dependencies    |
| `systemctl kill unit_name`        | Terminates all processes for a unit                   |

## Target Unit Management

- `rescue` and `emergency` targets are for troubleshooting and system recovery purposes
- `poweroff` and `halt` are similar to `shutdown`, and `hibernate` is suitable for mobile devices.

| CMD                                             | DESC                                                       |
| ----------------------------------------------- | ---------------------------------------------------------- |
| `systemctl list-units -t target`                | Lists all target type unit                                 |
| `systemctl list-units -t target --state active` | Get the current ative target units                         |
| `systemctl get-default`                         | Shows the default boot target                              |
| `systemctl set-default graphical.target`        | Set the system to boot into a graphical environment.       |
| `systemctl isolate rescue.target`               | Switch to Rescue Mode (Start one unit and stop all others) |
| `systemctl reboot`                              | Reboots a Linux system                                     |
| `systemctl poweroff`                            | Shut down the system                                       |

### Lab: Change target

#### Default target

```sh
systemctl get-default
# graphical.target

systemctl set-default multi-user
# Removed "/etc/systemd/system/default.target".
# Created symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/multi-user.target.

systemctl set-default graphical.target
Removed "/etc/systemd/system/default.target".
Created symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/graphical.target.
```

#### Switch currrent target

```sh
# To switch into multi-user
systemctl isolate multi-user
# To return to the graphical target:
systemctl isolate graphical

```

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

## Lab: Manage `nginx`

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

## Service Log

```sh
journalctl -u service_name
```

---

[TOP](#linux---software-management-service)
