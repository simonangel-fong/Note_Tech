# Linux - SELinux

[Back](../../index.md)

- [Linux - SELinux](#linux---selinux)
  - [SELinux](#selinux)
    - [`Discretionary Access Control (DAC)` vs `Mandatory Access Control (MAC)`](#discretionary-access-control-dac-vs-mandatory-access-control-mac)
  - [SELinux Modes](#selinux-modes)
  - [Configuration File `/etc/selinux/config`](#configuration-file-etcselinuxconfig)
  - [Common Commands](#common-commands)
  - [Lab:](#lab)
    - [Labeling](#labeling)
    - [Type Enforcement (TE)](#type-enforcement-te)
  - [](#)
  - [SELinux policies](#selinux-policies)
    - [Types of SELinux Policies](#types-of-selinux-policies)
    - [???](#-1)

---

## SELinux

- `SELinux (Security-Enhanced Linux)`

  - a **security architecture** integrated into the Linux **kernel** that provides a mechanism for supporting `access control security policies`.
  - It was originally developed by the `United States National Security Agency (NSA)` as a way to enforce the principle of `least privilege` and limit the potential damage of exploited vulnerabilities.

- **Benefits**:

  - Enhances system security **by limiting the actions** that processes can perform.
  - Protects **against privilege escalation** and exploits.
  - Helps mitigate the impact of vulnerabilities by **containing compromised processes**.

- **Challenges**:
  - Complex configuration and management.
  - May cause disruptions if improperly configured or if policies conflict with legitimate application behavior.

---

### `Discretionary Access Control (DAC)` vs `Mandatory Access Control (MAC)`

- `Discretionary Access Control (DAC)`

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

## SELinux Modes

- SELinux can operate in three modes:
  - `Enforcing` (**default**):
    - Policies are **enforced**, and access violations are **blocked** and **logged**.
  - `Permissive`:
    - Policies are **not enforced**, but **violations are logged**.
    - Useful for debugging and testing policies.
  - `Disabled`:
    - SELinux is **turned off**, and **no** policies are **enforced** or **logged**.

---

## Configuration File `/etc/selinux/config`

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

| CMD                                   | DESC                                            |
| ------------------------------------- | ----------------------------------------------- |
| `sestatus`/`getenforce`               | Check SELinux Status                            |
| `setenforce enforcing`/`setenforce 1` | Temporarily Enable enforcing SELinux            |
| `setenforce permissive`               | Temporarily set Permissive SELinux Mode         |
| `setenforce 0`                        | Temporarily set Permissive/Disable SELinux Mode |

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
