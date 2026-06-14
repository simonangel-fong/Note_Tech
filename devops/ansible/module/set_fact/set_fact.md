# Ansible - Module: `set_fact`

[Back](../../ansible.md)

- [Ansible - Module: `set_fact`](#ansible---module-set_fact)
  - [`set_fact` Module](#set_fact-module)
  - [Example](#example)

---

## `set_fact` Module

- `set_fact`:
  - the module used to **set variables** to **subsequent plays** during an `ansible-playbook` run via the host they were set on.
- ref: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/set_fact_module.html

---

## Example

- Set fact variables

```yaml
- hosts: localhost
  tasks:
    - name: Set a fact
      set_fact:
        # set a custom fact variable
        our_fact: Ansible Rocks!
        # process existing fact variable
        ansible_distribution: "{{ ansible_distribution | upper }}"

    - name: Show our_fact
      debug:
        msg: "{{ our_fact }}"

    - name: Show ansible_distribution
      debug:
        msg: "{{ ansible_distribution }}"
```

---

- with `when`, custom variable based on condition

```yaml
- hosts:
    - ubuntu3
    - centos3
  tasks:
    - name: Set our installation variables for CentOS
      set_fact:
        webserver_application_port: 80
        webserver_application_path: /usr/share/nginx/html
        webserver_application_user: root
      when: ansible_distribution == 'CentOS'

    - name: Set our installation variables for Ubuntu
      set_fact:
        webserver_application_port: 8080
        webserver_application_path: /var/www/html
        webserver_application_user: nginx
      when: ansible_distribution == 'Ubuntu'

    - name: Show pre-set distribution based facts
      debug:
        msg: "webserver_application_port:{{ webserver_application_port }} webserver_application_path:{{ webserver_application_path }} webserver_application_user:{{ webserver_application_user }}"
```
