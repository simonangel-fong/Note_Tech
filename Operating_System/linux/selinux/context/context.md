# Linux - SELinux: Context

[Back](../../index.md)

- [Linux - SELinux: Context](#linux---selinux-context)
  - [SELinux Context](#selinux-context)
    - [Components of an SELinux Context](#components-of-an-selinux-context)
    - [Common Commands](#common-commands)
  - [How SELinux Context Works for Files and Processes](#how-selinux-context-works-for-files-and-processes)
    - [Example Scenario: Web Server and File Access](#example-scenario-web-server-and-file-access)
  - [SELinux Ports](#selinux-ports)

---

## SELinux Context

- `SELinux context`
  - a set of labels assigned to processes, files, and other system objects to **control access** based on SELinux rules.

---

### Components of an SELinux Context

- `user:role:type:level`
- `User`:

  - Represents the `SELinux user` **associated with the object or process**.
  - e.g., `system_u`, `unconfined_u`.

- `Role`:

  - Defines the role **associated with the object or process**.
  - determine what `SELinux types` **a user can access**.
  - Common roles include:
    - `object_r`: Used for **files**, **directories**, and other **objects**.
    - `system_r`: Used for system **processes**.

- `Type`:

  - Specifies the **type** of the object or process.
  - e.g.,
    - `httpd_sys_content_t`: For web server content.
    - `ssh_t`: For SSH processes.
  - `SELinux policies` define the **access permissions** between types.

- `Level`:
  - Indicates the **sensitivity level (MLS/MCS category)**.
  - Most systems use a single level, `s0`.

---

### Common Commands

- View

| CMD                    | DESC                                              |
| ---------------------- | ------------------------------------------------- |
| `ls -Z /var/www/html`  | Display SELinux contexts of files and directories |
| `ps -eZ \| grep httpd` | Display SELinux contexts of running processes     |

- Default SELinux context

| CMD                                     | DESC                                                  |
| --------------------------------------- | ----------------------------------------------------- |
| `matchpathcon /var/www/html/index.html` | Check the default SELinux context for a specific file |
| `matchpathcon /var/www/html`            | Check the default context for a directory             |

- Temporarily change context
  - Changes made with `chcon` are not persistent and will reset after a system relabel.

| CMD                                                      | DESC                                     |
| -------------------------------------------------------- | ---------------------------------------- |
| `chcon -t httpd_sys_content_t /var/www/html/index.html`  | Change the type of a file                |
| `chcon -u system_u -r object_r /var/www/html/index.html` | Change the user and role (rarely needed) |

- Persistent Context Changes
  - `semanage fcontext` command
  - `relabel` command

| CMD                                                                | DESC                           |
| ------------------------------------------------------------------ | ------------------------------ |
| `semanage fcontext -a -t httpd_sys_content_t '/custom/path(/.*)?'` | Add a custom file context rule |
| `restorecon -Rv /custom/path`                                      | Apply the changes              |

- Troubleshooting

| CMD                                                 | DESC                                 |
| --------------------------------------------------- | ------------------------------------ |
| `ausearch -m avc -ts recent`                        | Check the SELinux logs for denials   |
| `grep "denied" /var/log/audit/audit.log`            | Analyze AVC Denials                  |
| `grep denied /var/log/audit/audit.log \| audit2why` | Generate Human-Readable Explanations |
| `sealert -a /var/log/audit/audit.log`               | View Troubleshooting Suggestions     |

---

## How SELinux Context Works for Files and Processes

- SELinux enforces access control through **policies** that match the `context` of processes (subjects) and files (objects).
- The decision to allow or deny access depends on whether the process context has the appropriate permissions to interact with the file context.

---

### Example Scenario: Web Server and File Access

- Scenario:
  - A web server (process) like `httpd` needs to serve a **file** located in `/var/www/html/index.html`.
  - SELinux ensures that the web server **process** (`httpd_t`) can access the **file** (`httpd_sys_content_t`) based on the defined **policy**

1. Process Context
   - Every running process in Linux has an SELinux context.
   - the Apache web server runs under the `httpd_t` type.

```sh
ps -eZ | grep httpd
# system_u:system_r:httpd_t:s0       1066 ?        00:00:00 httpd
```

2. File Context
   - Every file has an SELinux context.
   - Files in `/var/www/html` should have the type `httpd_sys_content_t` to allow the web server to access them.

```sh
ls -Z /var/www/html/hello_world/index.html
# unconfined_u:object_r:httpd_sys_content_t:s0 /var/www/html/hello_world/index.html
```

3. Policy Rules

   - SELinux policies define which types of **processes** can access which types of **files** and how they can **interact**.

4. Access Request

   - When the httpd process tries to read `/var/www/html/hello_world/index.html`, SELinux checks:
     - The process type (`httpd_t`).
     - The file type (`httpd_sys_content_t`).
     - The policy for allowed **actions**.
     - If the action (e.g., read) is permitted by the policy, access is granted. Otherwise, access is denied.

5. Handling Denied Access

   - If the file context is incorrect, SELinux will deny access.
   - Check the Denial Log: `ausearch -m avc -ts recent`

6. Fixing Contexts
   - To fix mismatched contexts, change the file type using `restorecon` or `chcon`.

---

## SELinux Ports

- `SELinux Ports`

  - ports are managed **as part of the policy** to control **which ports services are allowed to use**.
  - The SELinux policy includes a **mapping of port numbers to security labels** (contexts) for specific services.
  - This helps enforce that **only allowed services** can bind to specific **ports**, enhancing system security.

- Port Context
  - SELinux associates a **port** with a **context**, which includes a **type** that defines which service can use that port.
  - e.g.,
    - **HTTP (Port 80)**: `http_port_t` type.
    - **SSH (Port 22)**: `ssh_port_t` type.
- Port Types
  - Port types define the **services that are allowed to bind to specific ports**.
  - Common port types include:
    - `http_port_t`: For HTTP services.
    - `ssh_port_t`: For SSH services.
    - `mysqld_port_t`: For MySQL services.
- TCP/UDP Ports

  - SELinux differentiates between `TCP` and `UDP` ports.
  - Ports for both protocols can be labeled and managed **separately**.

- Audit Logs for Port Denials
  - If a service fails to bind to a port, check SELinux logs in `/var/log/audit/audit.log` for denial messages.

| CMD                                               | DESC                                                      |
| ------------------------------------------------- | --------------------------------------------------------- |
| `semanage port -l`                                | List all SELinux-managed ports and their associated types |
| `semanage port -l \| grep ':8080'`                | View a Specific Port's Context                            |
| `semanage port -a -t http_port_t -p tcp 8080`     | Add a New Port Context                                    |
| `semanage port -a -t ftp_port_t -p tcp 2100-2105` | Add an SELinux type to a range of ports.                  |
| `semanage port -m -t mysqld_port_t -p tcp 8080`   | Modify an Existing Port Context                           |
| `semanage port -d -t http_port_t -p tcp 8080`     | Remove a port from a specific SELinux type.               |

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
  - Back Up Configuration
    - Use `semanage export` to back up SELinux configurations, including port mappings.
    - e.g., `semanage export > selinux_config_backup.txt`

---
