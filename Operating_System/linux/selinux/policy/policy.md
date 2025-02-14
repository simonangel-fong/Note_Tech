# Linux - SELinux: Policy

[Back](../../index.md)

- [Linux - SELinux: Policy](#linux---selinux-policy)
  - [SELinux Policy](#selinux-policy)
    - [Types of SELinux Policies](#types-of-selinux-policies)
    - [Policy Components](#policy-components)
    - [Common Commands](#common-commands)
  - [SELinux Boolean](#selinux-boolean)
    - [SELinux Policy vs Boolean](#selinux-policy-vs-boolean)
    - [Common Commands](#common-commands-1)
    - [Lab: Allowing HTTPD to Connect to the Network](#lab-allowing-httpd-to-connect-to-the-network)
    - [Lab: View and Toggle SELinux Boolean Values](#lab-view-and-toggle-selinux-boolean-values)
  - [Audit](#audit)

---

## SELinux Policy

- `SELinux Policies`
  - a set of rules that define **how processes (subjects) can interact with system resources (objects)**.
- The policy enforces `mandatory access control (MAC)` by specifying what actions (read, write, execute) are allowed or denied based on the SELinux `contexts` of subjects and objects.

---

### Types of SELinux Policies

- **Targeted Policy**
  - Most common type.
  - **Focuses on protecting specific processes** while leaving others unrestricted.
  - Example: Protects httpd, sshd, mysqld.
- **Strict Policy**
  - Applies **restrictions to all processes**.
  - Used in highly secure environments.
- **MLS (Multi-Level Security) Policy**
  - Adds **sensitivity levels** and compartments to enforce strict information flow policies.
  - Used in government or military environments.

---

### Policy Components

- `Types`:
  - Defines file, process, and object types.
  - Example: `httpd_t` (process type), `httpd_sys_content_t` (file type).
- `Rules`:
  - **Allow or deny** specific actions between subjects and objects.
  - Example: `allow httpd_t httpd_sys_content_t:file { read write }`;
- `Booleans`:
  - Toggles specific features in policies.
  - Example: `httpd_can_network_connect` enables/disables network access for Apache.
- `Modules`:
  - **Contains** SELinux policy **rules** and can be loaded/unloaded dynamically.
  - Example: `httpd.pp` is a module for the HTTP daemon.

---

### Common Commands

- Current Policy

| CMD           | DESC                                                           |
| ------------- | -------------------------------------------------------------- |
| `sestatus`    | Display the Current Policy Type                                |
| `seinfo`      | Display the components of a SELinux policy                     |
| `seinfo -t`   | Display a list of types                                        |
| `seinfo -r`   | Display a list of roles                                        |
| `seinfo -u`   | Display a list of users                                        |
| `sesearch -A` | Search for allow rules in a SELinux policy                     |
| `sesearch -T` | Search for type_transition, type_member, and type_change rules |

- Module

| CMD                            | DESC                        |
| ------------------------------ | --------------------------- |
| `semodule -l`                  | Check Loaded Policy Modules |
| `semodule -i custom_module.pp` | Add a New Module            |
| `semodule -r custom_module`    | Remove a Module             |

---

## SELinux Boolean

- `SELinux Boolean`

  - a tunable option in `SELinux policies` that allows system administrators to **enable or disable specific behaviors or features** without modifying the entire SELinux policy.
  - Booleans provide a way to **dynamically adjust the policy** to accommodate different use cases, making it more flexible.
  - e.g.,
    - Allowing or disallowing HTTPD (Apache) to connect to the network (`httpd_can_network_connect`).
    - Permitting NFS home directories (`use_nfs_home_dirs`).

- CF:
  - `/sys/fs/selinux/booleans`

---

### SELinux Policy vs Boolean

- Part of SELinux Policy

  - SELinux Booleans are **defined within SELinux policies**.
  - They act as toggles that control optional rules within the policy.

- **Dynamic Modification** of Policy

  - Booleans allow administrators to change the behavior of policies **without recompiling or reinstalling the policy**.

- Granular Control

  - Booleans enable **fine-tuned control** over system behavior, allowing specific features to be turned on or off based on security requirements.

- Runtime and Persistent Changes
  - Runtime: Immediate but **temporary** changes that affect the current system state.
  - Persistent: Changes that survive **reboots**, stored in the SELinux configuration.

---

### Common Commands

| CMD                                                                 | DESC                                                           |
| ------------------------------------------------------------------- | -------------------------------------------------------------- |
| `getsebool -a`                                                      | List all available SELinux Booleans and their current state    |
| `semanage boolean -l`                                               | List all Booleans and their descriptions                       |
| `getsebool httpd_can_network_connect`                               | Display the state of a specific Boolean                        |
| `setsebool httpd_can_network_connect on`                            | Enable a Boolean value for the current session **Temporarily** |
| `setsebool -P httpd_can_network_connect=1 samba_enable_home_dirs=1` | Enable a Boolean Persistently                                  |
| `semanage boolean -m --on http_allow_homedirs`                      | Enable a Boolean Persistently                                  |

---

### Lab: Allowing HTTPD to Connect to the Network

```sh
# View a bool
getsebool httpd_can_network_connect
# httpd_can_network_connect --> off

# Enable the Boolean Temporarily
setsebool httpd_can_network_connect on

# Verify the Change
getsebool httpd_can_network_connect
# httpd_can_network_connect --> on
semanage boolean -l | grep httpd_can_network_connect
# httpd_can_network_connect      (on   ,  off)  Allow httpd to can network connect

# Make the Change Persistent
semanage boolean -m httpd_can_network_connect --on

# verify
semanage boolean -l | grep httpd_can_network_connect
# httpd_can_network_connect      (on   ,   on)  Allow httpd to can network connect
```

---

### Lab: View and Toggle SELinux Boolean Values

- display the current state of the Boolean nfs_export_all_rw. You will toggle its value temporarily, and reboot the system. You will flip its value persistently after the system has been back up.

```sh
# display boolean nfs_export_all_rw
getsebool -a | grep nfs_export_all_rw
# nfs_export_all_rw --> on

getsebool nfs_export_all_rw
# nfs_export_all_rw --> on

semanage boolean -l | grep nfs_export_all_rw
# nfs_export_all_rw              (on   ,   on)  Allow nfs to export all rw
```

- Temporarily turn off

```sh
# Turn off the value of nfs_export_all_rw
setsebool nfs_export_all_rw off
# confirm
getsebool -a | grep nfs_export_all_rw
# nfs_export_all_rw --> off

# reboot
reboot

# confirm
getsebool -a | grep nfs_export_all_rw
# nfs_export_all_rw --> on
```

- Persistently turn off

```sh
semanage boolean -m nfs_export_all_rw -0

# confirm
semanage boolean -l | grep nfs_export_all_rw
# nfs_export_all_rw              (off  ,  off)  Allow nfs to export all rw

getsebool nfs_export_all_rw
# nfs_export_all_rw --> off

# reboot
reboot

getsebool nfs_export_all_rw
# nfs_export_all_rw --> off
```

---

## Audit

- SELinux generates **alerts** for system activities when it runs in enforcing or permissive mode.
  - It writes the alerts to
    - the `/var/log/audit/audit.log` file if the `auditd daemon` is running, or
    - to the `/var/log/`messages file via the `rsyslog daemon` in the absence of auditd.
- SELinux also logs the alerts that are generated due to **denial of an action**, and identifies them with a type tag `AVC (Access Vector Cache)` in the `audit.log` file.

  - It also writes the **rejection** in the messages file with a **message ID**, and how to view the message details.

- Example of AVC denied log

```log
type=AVC msg=audit(1739222970.855:62): avc:  denied  { name_bind } for  pid=1149 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0
type=AVC msg=audit(1739224751.486:66): avc:  denied  { name_bind } for  pid=1061 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0
type=AVC msg=audit(1739224751.486:67): avc:  denied  { name_bind } for  pid=1061 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0
type=AVC msg=audit(1739225039.728:61): avc:  denied  { name_bind } for  pid=1117 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0
type=AVC msg=audit(1739225039.728:62): avc:  denied  { name_bind } for  pid=1117 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0
```

- analyze (-a) all AVC records in the audit.log file

```sh
sealert -a /var/log/audit/audit.log
```

- Using ausearch to check the recen denials

```sh
# try to restart service
systemctl restart httpd.service
# Job for httpd.service failed because the control process exited with error code.
# See "systemctl status httpd.service" and "journalctl -xeu httpd.service" for details.

# check the recent denials
ausearch -m avc -ts recent
# ----
# time->Mon Feb 10 17:24:52 2025
# type=PROCTITLE msg=audit(1739226292.355:144): proctitle=2F7573722F7362696E2F6874747064002D44464F524547524F554E44
# type=SYSCALL msg=audit(1739226292.355:144): arch=c000003e syscall=49 success=no exit=-13 a0=4 a1=55cfd8e9c4a0 a2=1c a3=7fff32576f5c items=0 ppid=1 pid=2333 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm="httpd" exe="/usr/sbin/httpd" subj=system_u:system_r:httpd_t:s0 key=(null)
# type=AVC msg=audit(1739226292.355:144): avc:  denied  { name_bind } for  pid=2333 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0
# ----
# time->Mon Feb 10 17:24:52 2025
# type=PROCTITLE msg=audit(1739226292.355:145): proctitle=2F7573722F7362696E2F6874747064002D44464F524547524F554E44
# type=SYSCALL msg=audit(1739226292.355:145): arch=c000003e syscall=49 success=no exit=-13 a0=3 a1=55cfd8e9c3e0 a2=10 a3=7fff32576f5c items=0 ppid=1 pid=2333 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm="httpd" exe="/usr/sbin/httpd" subj=system_u:system_r:httpd_t:s0 key=(null)
# type=AVC msg=audit(1739226292.355:145): avc:  denied  { name_bind } for  pid=2333 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0

# check the log
journalctl -u httpd --no-pager
# Feb 10 17:24:52 localhost.localdomain systemd[1]: Starting The Apache HTTP Server...
# Feb 10 17:24:52 localhost.localdomain httpd[2333]: AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using localhost.localdomain. Set the 'ServerName' directive globally to suppress this message
# Feb 10 17:24:52 localhost.localdomain httpd[2333]: (13)Permission denied: AH00072: make_sock: could not bind to address [::]:82
# Feb 10 17:24:52 localhost.localdomain httpd[2333]: (13)Permission denied: AH00072: make_sock: could not bind to address 0.0.0.0:82
# Feb 10 17:24:52 localhost.localdomain httpd[2333]: no listening sockets available, shutting down
# Feb 10 17:24:52 localhost.localdomain httpd[2333]: AH00015: Unable to open logs
# Feb 10 17:24:52 localhost.localdomain systemd[1]: httpd.service: Main process exited, code=exited, status=1/FAILURE
# Feb 10 17:24:52 localhost.localdomain systemd[1]: httpd.service: Failed with result 'exit-code'.
# Feb 10 17:24:52 localhost.localdomain systemd[1]: Failed to start The Apache HTTP Server.
```
