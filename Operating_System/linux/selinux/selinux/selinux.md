# Linux - SELinux

[Back](../../index.md)

- [Linux - SELinux](#linux---selinux)
  - [SELinux](#selinux)
    - [`Mandatory Access Control (MAC)`](#mandatory-access-control-mac)
    - [SELinux types](#selinux-types)
    - [vs `Discretionary Access Control (DAC)`](#vs-discretionary-access-control-dac)
    - [Architecture](#architecture)
  - [States and Modes](#states-and-modes)
    - [Configuration File `/etc/selinux/config`](#configuration-file-etcselinuxconfig)
  - [Common Commands](#common-commands)
  - [Lab:](#lab)
    - [Labeling](#labeling)
    - [Type Enforcement (TE)](#type-enforcement-te)
  - [](#)
  - [SELinux policies](#selinux-policies)
    - [Types of SELinux Policies](#types-of-selinux-policies)
    - [???](#-1)
  - [SELinux Policy Management tool: `semanage`](#selinux-policy-management-tool-semanage)
    - [Manage file contexts](#manage-file-contexts)
    - [`semanage port`: Manage SELinux port contexts](#semanage-port-manage-selinux-port-contexts)
  - [Booleans](#booleans)
    - [Lab: Configure SELinux Boolean](#lab-configure-selinux-boolean)

---

## SELinux

- `Security Enhanced Linux (SELinux)`

  - provides an **additional layer** of system security.
  - It was originally developed by the `United States National Security Agency (NSA)` as a way to enforce the principle of `least privilege` and limit the potential damage of exploited vulnerabilities.

- **Benefits**:

  - Enhances system security **by limiting the actions** that processes can perform.
  - Protects **against privilege escalation** and exploits.
  - Helps mitigate the impact of vulnerabilities by **containing compromised processes**.

- **Challenges**:
  - Complex configuration and management.
  - May cause disruptions if improperly configured or if policies conflict with legitimate application behavior.

---

### `Mandatory Access Control (MAC)`

- `SELinux context` / `SELinux label`:

  - a **special security label** associated with every **process** and system **resource**
  - an identifier which abstracts away the system-level details and focuses on the **security properties** of the entity.
    - provide a consistent way of **referencing objects** in the `SELinux policy`
    - removes any ambiguity that can be found in other identification methods

- `SELinux policy`

  - a series of rules which use these contexts to define **how processes can interact with each other** and the various system **resources**.
  - By **default**, the policy does **not allow any interaction** unless a rule explicitly grants access.

- `Mandatory Access Control (MAC)`

  - an access policy using `SELinux context`

- `SELinux contexts` have several **fields**:
  - user,
  - role,
  - type,
  - and security level.

---

### SELinux types

- `SELinux types`
  - used by the most common policy rule to **define the allowed interactions between processes and system resources**
  - usually end with `_t`.
  - e.g.,
    - the type name for the web server: `httpd_t`
    - type context for files and directories in `/var/www/html/`: `httpd_sys_content_t`
    - type contexts for files and directories in `/tmp` and `/var/tmp/`: `tmp_t`
    - type context for web server **ports**: `http_port_t`
  - e.g., a policy has
    - a rule that permits Apache (the **web server process** running as `httpd_t`) to access **files and directories** with a context normally found in `/var/www/html/` and other web server directories (`httpd_sys_content_t`).
    - **no allow rule** in the policy for files normally found in `/tmp` and `/var/tmp/`, so access is **not permitted**.
    - With SELinux, even if Apache is **compromised**, and a malicious script gains access, it is still **not able to** access the `/tmp` directory.

![example_selinux_context_type](./pic/example_selinux_context_type.png)

---

### vs `Discretionary Access Control (DAC)`

- `Discretionary Access Control (DAC)`
  - The **standard access policy** based on the **user**, **group**, and other **permissions**
  - does not enable system administrators to create comprehensive and fine-grained security policies
    - e.g., restricting specific applications to only viewing log files, while allowing other applications to append new data to the log files
  - **Users** have more control over their data, and can grant permissions to others.
  - **resource owners** can grant permissions at their own discretion.
  - traditional, flexible, and scalable
    - can be vulnerable to security **risks**
  - typical command `chmod`

![dac](./pic/dac_diagram.png)

---

- `Mandatory Access Control (MAC)`
  - A system enforces strict **policies that restrict access** based on the sensitivity of the data and the user's clearance.
  - **administrators** control access based on predefined security labels.
    - **access** is determined by a single individual based on **predetermined rules**
  - SELinux enforces **system-wide policies** that cannot be altered by individual users.
  - more **secure** than DAC, but can be **time-consuming to implement**.

![mac](./pic/mac_diagram.png)

---

### Architecture

- `SELinux` is a `Linux Security Module (LSM)` that is built into the Linux kernel.
- The **SELinux subsystem** in the kernel is driven by **a security policy** which is controlled by the administrator and loaded at boot.
- All security-relevant, kernel-level access operations on the system are **intercepted** by SELinux and examined in the **context** of the loaded security policy.

  - If the loaded policy **allows** the operation, it continues.
  - Otherwise, the operation is **blocked** and the process receives an error.

- `Access Vector Cache (AVC)`
  - the cached SELinux decisions, such as allowing or disallowing access
  - When using these cached decisions, SELinux policy rules need to be **checked less**, which increases performance.
  - Remember that SELinux policy rules have **no effect** if `DAC` rules **deny** access first.

---

## States and Modes

Use the setenforce utility to change between enforcing and permissive mode. Changes made with setenforce do not persist across reboots. To change to enforcing mode, enter the setenforce 1 command as the Linux root user. To change to permissive mode, enter the setenforce 0 command. Use the getenforce utility to view the current SELinux mode:

- SELinux can operate in three modes:
  - `Enforcing`
    - **default**, recommended
    - Policies are **enforced**, and access violations are **blocked** and **logged**.
    - enforcing the loaded security policy on the entire system
  - `Permissive`:
    - Policies are **not enforced**, but **violations are logged**.
    - not actually deny any operations
    - not recommended for production systems
    - Useful for debugging and testing policies.
  - `Disabled`:
    - SELinux is **turned off**, and **no** policies are **enforced** or **logged**.
    - enforcing the SELinux policy: avoid
    - labeling any persistent objects: avoids
      - such as labeling files, making it difficult to enable SELinux in the future.
    - strongly discouraged

---

### Configuration File `/etc/selinux/config`

- Persist the configuration for reboot.
- Path: `/etc/selinux/config`
- Parameter:
  - `SELINUX=enforcing`
  - `SELINUX=permissive`
  - `SELINUX=disabled`
- Best practise:

  - create **snapshot** of VM before modifying config file

- CF:
  - By default: SELinux mode is `enforcing`

```sh
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
```

---

## Common Commands

| CMD                                   | DESC                                    |
| ------------------------------------- | --------------------------------------- |
| `sestatus`/`getenforce`               | Check SELinux Status                    |
| `setenforce enforcing`/`setenforce 1` | Temporarily Enable enforcing SELinux    |
| `setenforce permissive`               | Temporarily set Permissive SELinux Mode |
| `setenforce 0`                        | Temporarily set Permissive SELinux Mode |
| `semanage permissive -a httpd_t`      | Make the httpd_t domain permissive      |

- Change SELinux Mode Persistently
  - `/etc/selinux/config`
  - `SELINUX=enforcing`

---

## Lab:

```sh
# Check the SELinux status
sestatus
# SELinux status:                 enabled
# SELinuxfs mount:                /sys/fs/selinux
# SELinux root directory:         /etc/selinux
# Loaded policy name:             targeted
# Current mode:                   enforcing
# Mode from config file:          enforcing
# Policy MLS status:              enabled
# Policy deny_unknown status:     allowed
# Memory protection checking:     actual (secure)
# Max kernel policy version:      33

# Check if SELinux enforce
getenforce
# Enforcing
```

- Disable SELinux permanently

```sh
# backup cf before editing
cp /etc/selinux/config /etc/selinux/config.bak

# get cf
cat /etc/selinux/config
# # This file controls the state of SELinux on the system.
# # SELINUX= can take one of these three values:
# #     enforcing - SELinux security policy is enforced.
# #     permissive - SELinux prints warnings instead of enforcing.
# #     disabled - No SELinux policy is loaded.
# SELINUX=enforcing
# # SELINUXTYPE= can take one of these three values:
# #     targeted - Targeted processes are protected,
# #     minimum - Modification of targeted policy. Only selected processes are protected.
# #     mls - Multi Level Security protection.
# SELINUXTYPE=targeted

# edit cf
vi /etc/selinux/config
# SELINUX=disabled

# confirm
cat /etc/selinux/config | grep SELINUX=
# SELINUX=disabled
sestatus
# SELinux status:                 enabled
# SELinuxfs mount:                /sys/fs/selinux
# SELinux root directory:         /etc/selinux
# Loaded policy name:             targeted
# Current mode:                   enforcing
# Mode from config file:          disabled
# Policy MLS status:              enabled
# Policy deny_unknown status:     allowed
# Memory protection checking:     actual (secure)
# Max kernel policy version:      33


# restart
reboot
sestatus
# SELinux status:                 disabled
getenforce
# Disabled
```

---

### Labeling

- `SELinux context`

  - security-relevant information of a file or process

- `label` in SELinux

  - used to represent `SELinux context`
  - includes 4 components:
    - `User`:
      - **SELinux user** (e.g., system_u, unconfined_u).
    - `Role`:
      - Defines the **role** of the subject (e.g., system_r, object_r).
    - `Type`:
      - The most critical part, representing the **type** of the object or subject (e.g., httpd_t, var_t).
    - `Level` (optional):
      - For Multi-Level Security (MLS), indicating **sensitivity levels** (e.g., s0, s0-s15:c0.c1023).

- Type in Labeling

  - `Subject type`:
    - Assigned to **processes** (e.g., httpd_t for the Apache HTTP server process).
  - `Object type`:
    - Assigned to **resources** (e.g., httpd_sys_content_t for web content files).

- SELinux **policies** are enforced **based on types**.

| CMD                                                     | DESC                                  |
| ------------------------------------------------------- | ------------------------------------- |
| `ls -Z /path/to/file`                                   | View SELinux context of a file        |
| `ps -eZ \| grep process_name`                           | View SELinux context of a process     |
| `chcon -t httpd_sys_content_t /var/www/html/index.html` | Temporaryly change the type of a file |
| `restorecon -Rv /path/to/files`                         | relabel the file system               |

---

### Type Enforcement (TE)

- `Type Enforcement`

  - the main **access control mechanism** in SELinux.
  - It defines the **rules** for how **processes (subjects)** with a specific type can **interact** with **objects** of another type.

- How Type Enforcement Works:
  - **Rules Define Access**:
    - **Policies** are written to **allow** or **deny** actions (like read, write, execute) **based on the types** of the subject and object.
    - e.g., `allow httpd_t httpd_sys_content_t: file { read write };`
    - This allows processes labeled `httpd_t` (e.g., Apache) to **read** and **write** files labeled `httpd_sys_content_t`.
    - If a file is mislabeled, the process will be denied access.
- **Default Deny Policy**:
  - SELinux operates with a "default deny" policy, meaning anything **not explicitly allowed is denied**.
- **Domain Transitions**:
  - A process can **change its type (domain)** when running a specific executable.
  - For example, executing a binary labeled `httpd_exec_t` may transition the process to the `httpd_t` domain.
- **Containment**:
  - By enforcing strict rules, TE ensures that even if a process is **compromised**, its actions are **limited** to what the policy allows.

```sh
# get the label of a file(Object type)
ls -hlZ /usr/sbin/nginx
# -rwxr-xr-x. 1 root root system_u:object_r:httpd_exec_t:s0 1.3M Oct 12  2023 /usr/sbin/nginx

# get the label of a directory(Object type)
ls -dhlZ /etc/nginx/
# drwxr-xr-x. 4 root root system_u:object_r:httpd_config_t:s0 4.0K Dec 14 23:13 /etc/nginx/

# get the label of a process(Subject type)
ps -eZ | grep nginx
# system_u:system_r:httpd_t:s0       1259 ?        00:00:00 nginx
# system_u:system_r:httpd_t:s0       1262 ?        00:00:00 nginx
# system_u:system_r:httpd_t:s0       1264 ?        00:00:00 nginx
# system_u:system_r:httpd_t:s0       1265 ?        00:00:00 nginx
# system_u:system_r:httpd_t:s0       1266 ?        00:00:00 nginx

# get the label of a socke level
netstat -tnlpZ | grep http
# tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1259/nginx: master   system_u:system_r:httpd_t:s0
# tcp6       0      0 :::80                   :::*                    LISTEN      1259/nginx: master   system_u:system_r:httpd_t:s0
```

---

##

Manage SELinux settings

- `semanage`
  - used to **manage SELinux policies**
  - including file contexts, user mappings, ports, and more. Changes made with semanage are persistent across system reboots or SELinux relabeling.

---

## SELinux policies

- `SELinux policies`
  - the core components of SELinux that **define how security is enforced** on a system.
  - specify the rules that govern **what actions subjects (processes) can perform on objects** (files, directories, ports, devices, etc.).

---

### Types of SELinux Policies

- **Targeted Policy** (**Default** Policy):

  - Focuses on protecting **key services and processes** while leaving most of the system in an unconfined(无限制的) state.
  - Example: **Protecting services** like `httpd`, `sshd`, or `mysqld`.

- **MLS Policy (Multi-Level Security)**:

  - Used in environments requiring **strict data classification and compartmentalization(区分)**.
  - Typically deployed in military or **highly secure systems**.
  - Adds sensitivity levels (e.g., `s0`, `s0-s15:c0.c1023`).

- **Strict Policy**:

  - **All** processes and objects are **confined** by SELinux policies.
  - Offers **comprehensive security** but requires extensive customization and testing.

- **Custom Policies**:
  - Created to support **specific applications or systems** not covered by default policies.

---

### ???

??login, user, port, interface, module, node, file context, boolean, permissive state, dontaudit

- `Boolean`

  - ON/OFF switch
  - toggles that allow dynamic modification of policies without editing the policy files.
  - Whether an action/access is allowed.
  - Command to get pre-defined boolean
    - `getsebool -a`
    - `semanage boolean -l`
  - Command to manage booleans
    - `setsebool -P boolean_name on`
  - Command to query error messages related to selinux
    - `journalctl`
  - To change the type in a label
    - `chcon -t httpd_sys_content_t FILENAME`
    - `semanage -t httpd_sys_content_t FILENAME`

- Lab: get all boolean

```sh
getsebool -a

# count the total number of booleans
getsebool -a | wc -l
# 340

# Check a specific boolean
getsebool -a | grep httpd

# turn on a boolean
getsebool -a | grep httpd_can_connect_ftp
# httpd_can_connect_ftp --> off
setsebool -P httpd_can_connect_ftp on
# confirm
getsebool -a | grep httpd_can_connect_ftp
# httpd_can_connect_ftp --> on

# turn it back off
setsebool -P httpd_can_connect_ftp off
# confirm
getsebool -a | grep httpd_can_connect_ftp
# httpd_can_connect_ftp --> off
```

---

## SELinux Policy Management tool: `semanage`

### Manage file contexts

- SELinux uses **file contexts** to enforce security policies on files and directories.

- Temporary Changes:
  - Directly modifying a file's SELinux context with `chcon` is **temporary** and **reset upon relabeling**.
- Use `semanage fcontext` for permanent changes.

| CMD                                                   | DESC                             |
| ----------------------------------------------------- | -------------------------------- |
| `semanage fcontext -l`                                | Lists all the file context rules |
| `ls -Z /path/to/file`                                 | Lists SELinux contexts of a file |
| `semanage fcontext -a -t file_context '/path(/.*)?'`  | Add a custom context to a path   |
| `semanage fcontext -a -t file_context '/path/to/file` | Add a custom context to a file   |
| `semanage fcontext -m -t file context '/path(/.*)?'`  | Modify an Existing File Context  |
| `semanage fcontext -d '/path(/.*)?'`                  | Remove the file context rule     |
| `restorecon -Rv /path`                                | Apply the changes                |

---

### `semanage port`: Manage SELinux port contexts

- `semanage port`
  - used to manage **SELinux port contexts**.
- SELinux policies enforce which **processes can bind to specific ports**.
  - With semanage port, you can list, add, modify, or delete port contexts to allow or restrict services from using certain ports.

| CMD                                               | DESC                                                                |
| ------------------------------------------------- | ------------------------------------------------------------------- |
| `semanage port -l`                                | List All Port Contexts (SELinux types, protocols, and port ranges.) |
| `semanage port -l \| grep ':8080'`                | View a Specific Port's Context                                      |
| `semanage port -a -t http_port_t -p tcp 8080`     | Add a New Port Context                                              |
| `semanage port -a -t ftp_port_t -p tcp 2100-2105` | Add an SELinux type to a range of ports.                            |
| `semanage port -m -t mysqld_port_t -p tcp 8080`   | Modify an Existing Port Context                                     |
| `semanage port -d -t http_port_t -p tcp 8080`     | Remove a port from a specific SELinux type.                         |

- Tips:
  - **Temporarily**:
    - modifying a port with `firewalld`
    - not persist after a reboot
  - **Permanently**:
    - Using `semanage port` ensures the changes are permanent for SELinux.
  - SELinux **Logs**:
    - If a port-related denial occurs, check `/var/log/audit/audit.log` for details.
  - **Testing**:
    - Use `netstat -tuln` or `ss -tuln` to verify services listening on ports.

---

The semanage boolean command is used to manage SELinux booleans, which are toggles that enable or disable specific SELinux policy features. SELinux booleans provide flexibility, allowing administrators to modify SELinux behavior without rewriting policy rules.

## Booleans

- `SELinux Booleans`
  - allow parts of SELinux policy to be **changed at runtime**, without reloading or recompiling SELinux policy.

| CMD                                                  | DESC                                                                     |
| ---------------------------------------------------- | ------------------------------------------------------------------------ |
| `semanage boolean -l`                                | List All SELinux Booleans(Boolean Name, State, Default, Description)     |
| `getsebool -a`                                       | Lists Booleans(Boolean Name, on/off)                                     |
| `getsebool boolean_name1 boolean_name2`              | Get value of a boolean name                                              |
| `semanage boolean -m --on httpd_enable_homedirs`     | Enable a Boolean(HTTPD to access home directories)                       |
| `semanage boolean -m --off httpd_use_nfs`            | Disable a Boolean(NFS access by HTTPD)                                   |
| `semanage boolean -m -N --on samba_enable_home_dirs` | **Temporarily** enable Samba's use of home directories                   |
| `setsebool httpd_can_network_connect_db on`          | **Temporarily** enable Apache HTTP Server to connect to database servers |

---

### Lab: Configure SELinux Boolean

- View all

```sh
# list all booleans
semanage boolean -l
# SELinux boolean                State  Default Description
# abrt_anon_write                (off  ,  off)  Allow abrt to anon write
# abrt_handle_event              (off  ,  off)  Allow abrt to handle event
# abrt_upload_watch_anon_write   (on   ,   on)  Allow abrt to upload watch anon write
# antivirus_can_scan_system      (off  ,  off)  Allow antivirus to can scan system
# antivirus_use_jit              (off  ,  off)  Allow antivirus to use jit
# auditadm_exec_content          (on   ,   on)  Allow auditadm to exec content
# authlogin_nsswitch_use_ldap    (off  ,  off)  Allow authlogin to nsswitch use ldap
# authlogin_radius               (off  ,  off)  Allow authlogin to radius
# authlogin_yubikey              (off  ,  off)  Allow authlogin to yubikey
# ...

getsebool -a
# abrt_anon_write --> off
# abrt_handle_event --> off
# abrt_upload_watch_anon_write --> on
# antivirus_can_scan_system --> off
# antivirus_use_jit --> off
# auditadm_exec_content --> on
# authlogin_nsswitch_use_ldap --> off
# authlogin_radius --> off
# ...
```

- Temporarily enable

```sh
# get a specific bool
semanage boolean -l | grep "httpd_can_network_connect_db"
# httpd_can_network_connect_db   (off  ,  off)  Allow httpd to can network connect db
getsebool httpd_can_network_connect_db
# httpd_can_network_connect_db --> off

# temporarily enable a bool
setsebool httpd_can_network_connect_db on
# confirm
getsebool httpd_can_network_connect_db
# httpd_can_network_connect_db --> on

# restart OS
# Confirm bool state after reboot
getsebool httpd_can_network_connect_db
# httpd_can_network_connect_db --> off
```

- Permanently enable

```sh
# get a specific bool
semanage boolean -l | grep "httpd_can_network_connect_db"
# httpd_can_network_connect_db   (off  ,  off)  Allow httpd to can network connect db
getsebool httpd_can_network_connect_db
# httpd_can_network_connect_db --> off

# permanently enable
semanage boolean -m --on httpd_can_network_connect_db
# confirm
semanage boolean -l | grep "httpd_can_network_connect_db"
# httpd_can_network_connect_db   (on   ,   on)  Allow httpd to can network connect db
getsebool httpd_can_network_connect_db
# httpd_can_network_connect_db --> on

# reboot
# confirm
semanage boolean -l | grep "httpd_can_network_connect_db"
# httpd_can_network_connect_db   (on   ,   on)  Allow httpd to can network connect db
getsebool httpd_can_network_connect_db
# httpd_can_network_connect_db --> on
```

- Permanently disable

```sh
# disable
semanage boolean -m --off httpd_can_network_connect_db

# confirm
getsebool "httpd_can_network_connect_db"
# httpd_can_network_connect_db --> off
semanage boolean -l | grep "httpd_can_network_connect_db"
# httpd_can_network_connect_db   (off  ,  off)  Allow httpd to can network connect db
```
