# Linux - SELinux: Context

[Back](../../index.md)

- [Linux - SELinux: Context](#linux---selinux-context)
  - [SELinux Context](#selinux-context)
    - [Copying, Moving, and Archiving Files with SELinux Contexts](#copying-moving-and-archiving-files-with-selinux-contexts)
    - [Lab: Copy Files with and without Context](#lab-copy-files-with-and-without-context)
    - [Components of an SELinux Context](#components-of-an-selinux-context)
    - [Common Commands](#common-commands)
    - [Lab: Change Context](#lab-change-context)
  - [How SELinux Context Works for Files and Processes](#how-selinux-context-works-for-files-and-processes)
    - [Example Scenario: Web Server and File Access](#example-scenario-web-server-and-file-access)
  - [SELinux Ports](#selinux-ports)
    - [Common Commands](#common-commands-1)
    - [Lab: Add and Delete Network Ports](#lab-add-and-delete-network-ports)

---

## SELinux Context

- `SELinux context`
  - a set of labels assigned to processes, files, and other system objects to **control access** based on SELinux rules.

---

### Copying, Moving, and Archiving Files with SELinux Contexts

- If a file is **copied** to a different directory, the destination file will **receive the destination directory’s context**, unless the `--preserve=context` switch is specified with the cp command to retain the source file’s original context.复制新文件：适应新标签

- If a copy operation **overwrites** the destination file in the same or different directory, the file being copied will **receive the context of the overwritten file**, unless the `--preserve=context` switch is specified with the `cp` command to **preserve** the source file’s **original context**. 覆盖复制：保留旧文件标签

- If a file is **moved** to the same or different directory, the SELinux context will **remain intact**, which may differ from the destination directory’s context. 移动：保留旧标签

- If a file is archived with the tar command, use the `--selinux` option to preserve the context. 存档：默认不保留标签

---

### Lab: Copy Files with and without Context

```sh
touch /tmp/sefile2
ll -Z /tmp/sefile2
# -rw-r--r--. 1 root root unconfined_u:object_r:user_tmp_t:s0 0 Feb 10 16:45 /tmp/sefile2

# copy file without context
cp /tmp/sefile2 /etc/default
ll -Z /etc/default/sefile2
# -rw-r--r--. 1 root root unconfined_u:object_r:etc_t:s0 0 Feb 10 16:48 /etc/default/sefile2
```

> The **target** file (/etc/default/sefile2) **received** the **default** context of the **destination** directory (/etc/default).

```sh
# Remove the /etc/default/sefile2 file, and copy it again with the --preserve=context option:
rm /etc/default/sefile2
cp /tmp/sefile2 /etc/default --preserve=context

# confirm
ll -Z /etc/default/sefile2
# -rw-r--r--. 1 root root unconfined_u:object_r:user_tmp_t:s0 0 Feb 10 16:51 /etc/default/sefile2
```

> - The original context (user_tmp_t) is preserved on the target file after the copy operation has finished.

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

- **Temporarily** change context
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

### Lab: Change Context

- Temporaly

```sh
# create file
mkdir /tmp/sedir1
touch /tmp/sedir1/sefile1

# list context
ll -dZ /tmp/sedir1
# drwxr-xr-x. 2 root root unconfined_u:object_r:user_tmp_t:s0 21 Feb 10 00:44 /tmp/sedir1
ll -Z /tmp/sedir1/sefile1
# -rw-r--r--. 1 root root unconfined_u:object_r:user_tmp_t:s0 0 Feb 10 00:44 /tmp/sedir1/sefile1

# change contenxt
chcon -v -u user_u -t public_content_t -R /tmp/sedir1/
# changing security context of '/tmp/sedir1/sefile1'
# changing security context of '/tmp/sedir1/'

# confirm
ll -dZ /tmp/sedir1
# drwxr-xr-x. 2 root root user_u:object_r:public_content_t:s0 21 Feb 10 00:44 /tmp/sedir1
ll -Z /tmp/sedir1/sefile1
# -rw-r--r--. 1 root root user_u:object_r:public_content_t:s0 0 Feb 10 00:44 /tmp/sedir1/sefile1

semanage fcontext -lC
# SELinux fcontext                                   type               Context
# /tmp/sedir1(/.*)?                                  all files          user_u:object_r:public_content_t:s0

```

- Persistently
  - Add the directory recursively to the policy database

```sh
# add context to the policy database
semanage fcontext -a -s user_u -t public_content_t "/tmp/sedir1(/.*)?"
semanage fcontext -lC
# SELinux fcontext                                   type               Context
# /tmp/sedir1(/.*)?                                  all files          user_u:object_r:public_content_t:s0

# Temporarily change context
chcon -v -u staff_u -t etc_t -R /tmp/sedir1
# changing security context of '/tmp/sedir1/sefile1'
# changing security context of '/tmp/sedir1'
ll -dZ /tmp/sedir1; ll -Z /tmp/sedir1/sefile1
# drwxr-xr-x. 2 root root staff_u:object_r:etc_t:s0 21 Feb 10 16:12 /tmp/sedir1
# -rw-r--r--. 1 root root staff_u:object_r:etc_t:s0 0 Feb 10 16:12 /tmp/sedir1/sefile1

# Apply the New Context to the Files
restorecon -Rv /tmp/sedir1
# Relabeled /tmp/sedir1 from staff_u:object_r:etc_t:s0 to staff_u:object_r:public_content_t:s0
# Relabeled /tmp/sedir1/sefile1 from staff_u:object_r:etc_t:s0 to staff_u:object_r:public_content_t:s0

# confirm
ll -dZ /tmp/sedir1; ll -Z /tmp/sedir1/sefile1
# drwxr-xr-x. 2 root root staff_u:object_r:public_content_t:s0 21 Feb 10 16:12 /tmp/sedir1
# -rw-r--r--. 1 root root staff_u:object_r:public_content_t:s0 0 Feb 10 16:12 /tmp/sedir1/sefile1
```

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

### Common Commands

| CMD                                               | DESC                                                      |
| ------------------------------------------------- | --------------------------------------------------------- |
| `semanage port -l`                                | List all SELinux-managed ports and their associated types |
| `semanage port -l \| grep ':8080'`                | View a Specific Port's Context                            |
| `semanage port -a -t http_port_t -p tcp 8080`     | Add a New Port Context                                    |
| `semanage port -a -t ftp_port_t -p tcp 2100-2105` | Add an SELinux type to a range of ports.                  |
| `semanage port -m -t mysqld_port_t -p tcp 8080`   | Modify an Existing Port Context                           |
| `semanage port -d -t http_port_t -p tcp 8080`     | Remove a port from a specific SELinux type.               |

---

### Lab: Add and Delete Network Ports

- add a non-standard network port 8010 to the SELinux policy database for the httpd service and confirm the addition.

```sh
# List (-l) the ports for the httpd service
semanage port -l | grep ^http_port
# http_port_t                    tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000

# Add (-a) port 8010 with type (-t) http_port_t and protocol (-p) tcp to the policy
semanage port -a -t http_port_t -p tcp 8010

# confirm
semanage port -Cl
# SELinux Port Type              Proto    Port Number
# http_port_t                    tcp      8010

semanage port -l | grep ^http_port
# http_port_t                    tcp      8010, 80, 81, 443, 488, 8008, 8009, 8443, 9000

# Delete (-d) port 8010 from the policy and confirm:
semanage port -d -p tcp 8010

# confirm
semanage port -Cl
# return nothting
semanage port -l | grep ^http_port
# http_port_t                    tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000
```
