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
