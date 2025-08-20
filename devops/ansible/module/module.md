# Ansible - Module

[Back](../ansible.md)

- [Ansible - Module](#ansible---module)
  - [Module](#module)
    - [Command Commands](#command-commands)
    - [Common Module](#common-module)

---

## Module

- `module`
  - a **reusable, standalone script or program** that performs a specific task on a managed host.
  - the building blocks of Ansible playbooks, enabling automation tasks like installing packages, managing files, configuring services, or interacting with cloud services.

---

### Command Commands

| Command                   | Desc                      |
| ------------------------- | ------------------------- |
| `ansible-doc -l`          | list all modules          |
| `ansible-doc module_name` | Get doc of a given module |

---

### Common Module

- System / Package Management

| Module        | Purpose                                               |
| ------------- | ----------------------------------------------------- |
| `apt`         | Manage packages on Debian/Ubuntu systems              |
| `yum` / `dnf` | Manage packages on RHEL/CentOS/Fedora                 |
| `package`     | Generic package manager abstraction (works across OS) |
| `service`     | Manage services (start, stop, enable, disable)        |
| `systemd`     | Advanced systemd service management                   |

- File & Directory Management

| Module      | Purpose                                                         |
| ----------- | --------------------------------------------------------------- |
| `file`      | Manage file attributes (permissions, owner, directory, symlink) |
| `copy`      | Copy files from control node to target                          |
| `fetch`     | Copy files from target back to control node                     |
| `template`  | Deploy Jinja2 template files with variables                     |
| `unarchive` | Extract archives (tar, zip, etc.)                               |

- User & Group Management

| Module           | Purpose                      |
| ---------------- | ---------------------------- |
| `user`           | Create, modify, remove users |
| `group`          | Manage groups                |
| `authorized_key` | Manage SSH keys for users    |

- Networking

| Module      | Purpose                                                 |
| ----------- | ------------------------------------------------------- |
| `ping`      | Test connectivity (simple check if host is reachable)   |
| `uri`       | Interact with web services / APIs (HTTP GET/POST, etc.) |
| `get_url`   | Download files from the internet                        |
| `firewalld` | Manage firewalld rules on Linux                         |
| `iptables`  | Manage iptables rules                                   |

- Database

| Module            | Purpose                                   |
| ----------------- | ----------------------------------------- |
| `mysql_db`        | Manage MySQL/MariaDB databases            |
| `mysql_user`      | Manage MySQL/MariaDB users and privileges |
| `postgresql_db`   | Manage PostgreSQL databases               |
| `postgresql_user` | Manage PostgreSQL users/roles             |

- Cloud & Virtualization

| Module                 | Purpose                       |
| ---------------------- | ----------------------------- |
| `ec2` / `ec2_instance` | Manage AWS EC2 instances      |
| `s3`                   | Manage AWS S3 buckets/objects |
| `azure_rm_*`           | Manage Azure resources        |
| `gcp_*`                | Manage GCP resources          |
| `docker_container`     | Manage Docker containers      |
| `docker_image`         | Manage Docker images          |

- Utilities & Command Execution

| Module    | Purpose                                                   |
| --------- | --------------------------------------------------------- |
| `command` | Run a command (no shell features like redirection, pipes) |
| `shell`   | Run a command through a shell (allows pipes, redirection) |
| `script`  | Upload and execute a local script on the remote node      |
| `debug`   | Print variables or messages for debugging                 |
| `assert`  | Validate conditions (fail if not true)                    |
