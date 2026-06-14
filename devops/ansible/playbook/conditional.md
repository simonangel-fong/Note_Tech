# Ansible - Task: Conditional

[Back](../ansible.md)

- [Ansible - Task: Conditional](#ansible---task-conditional)
  - [Conditional](#conditional)

---

## Conditional

- `when` directive:
  - define the condition of a task

- Syntax:

```yaml
- name: task name
  <module>:
  when: <condition>

# multiple conditions
- name: task name
  <module>:
  when: 
    - <condition1>
    - <condition2>
```




```yaml
- name: Install NGINX
  hosts: all
  tasks:
    - name: Install NGINX on Debian
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "Debian"

    - name: Install NGINX on Redhat
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "RedHat" or ansible_os_family == "SUSE"
```

---


- Task action based on the output.

```yaml
- name: Check status of a service and email if its down
  hosts: localhost
  tasks:
    - command: service httpd status
      register: result # register an ouput

    - mail:
        to: admin@company.com
        subject: Service Alert
        body: Httpd Service is down
        when: result.stdout.find('down') != -1 # send email based on the ouput
```

---

- Common User case
  - use fact to determine the distro of OS, then use conditional to control the action based on the OS facts.

```yaml
- name: Install Nginx on Ubuntu 18.04
  apt:
    name: nginx=1.18.0
    state: present
    when: ansible_facts['os_family'] == 'Debian' and ansible_facts['distribution_major_version'] == '18'
```

---
