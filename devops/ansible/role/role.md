# Ansible - Role

[Back](../ansible.md)

---

## Role

- `role`
  - group related tasks, variables, templates, and files into a predefined directory structure. This allows you to easily maintain, reuse, and share your configuration code.

- benefits:
  - **Modularity**:
    - They act like functions in programming, define the logic once and call it anywhere.
  - **Reusability**:
    - use the exact same role to configure a web server, install a database, or harden an operating system **across different projects**.
  - **Organization**: They enforce a **standard directory structure** so codebase stays clean.

---

### Standard Directory Structure

- A role automatically loads related files based on a known hierarchy:
- `defaults/`:
  - Default, **low-priority** **variables** for the role.
- `files/`:
  - **Static files that** need to be deployed to remote nodes.
  - the files usually work with `file`, `fetch` module
- `handlers/`:
  - Actions **triggered** by changes (like restarting a service).
- `meta/`:
  - Role **dependencies** and author information.
- `tasks/`:
  - The main list of steps the role executes.
- `templates/`:
  - Jinja2 templates (dynamic configuration files).
- `vars/`:
  - **Higher-priority variables** that can override defaults.

---

### Common Commands

| CMD                                   | DESC                                           |
| ------------------------------------- | ---------------------------------------------- |
| `ansible-galaxy role init nginx_role` | Create a new role skeleton named `nginx_role`. |
