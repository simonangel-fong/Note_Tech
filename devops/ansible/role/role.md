# Ansible - Role

[Back](../ansible.md)

---

## Role

- `role`

  - a way to **organize playbooks** and related files into a **standardized directory structure**.

- Benefits:

  - **Encapsulation**:
    - A role **packages** everything needed to configure a service or perform a function (tasks, handlers, variables, templates, etc.).
  - **Reusability**:
    - You can **reuse the same role** across multiple projects or environments.
  - **Structure**:
    - Roles follow a **fixed directory layout**, so Ansible knows where to find tasks, handlers, templates, and files automatically.
  - **Composability**: You can include multiple roles in a single playbook.

- Ways to search for an existing role
  - galaxy UI
  - `ansible-galaxy search role_name`
- Install a role

  - `ansible-galaxy install role_name -p ./roles`

- Check the configuration of role
  - `ansible-config dump | grep ROLE`

---

### Standard Role Directory Structure

myrole/
├── defaults/ # Default variables (lowest priority)
│ └── main.yml
├── vars/ # Other variables (higher priority)
│ └── main.yml
├── files/ # Static files to copy
├── templates/ # Jinja2 templates
├── tasks/ # Main list of tasks
│ └── main.yml
├── handlers/ # Handlers triggered by notify
│ └── main.yml
├── meta/ # Role dependencies and metadata
│ └── main.yml
└── README.md # Documentation (optional but recommended)

- Command to create directory structure
  - `ansible-galaxy init role_name`

---

### Assign playbook a role

- Specify a role in a playbook

```yaml
- name: Install and configure mysql
  hosts: db-server
  roles:
    - mysql
```

- Specify with privilege and variable

```yaml
- name: Install and configure mysql
  hosts: db-server
  roles:
    - role: mysql
      become: yes
      vars:
        mysql_user_name: db_user
```

- Ways to reference a role for a playbook

1. create `roles` in the playbook dir, and place all files required by the role into this dir
2. Place the role required file in the default dir `/etc/ansible/roles`

---
