# Ansible - Conditional

[Back](../ansible.md)

- [Ansible - Conditional](#ansible---conditional)
  - [Conditional](#conditional)
  - [Loops](#loops)

---

## Conditional

- `when` directive:
  - define the condition of a task

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

- Conditional in loop

  - using the `loop` directive to identify the list to loop
  - using the `item.property_name` to refer the property of the item in the list

```yaml
- name: Install Softwares
  hosts: all
  become: true
  vars:
    packages:
      - name: nginx
        required: true
      - name: mysql-client
        required: true
      - name: apache
        required: false

  tasks:
    - name: Install "{{ item.name }}" on Debian
      apt:
        name: "{{ item.name }}"
        state: present
      when: item.required == True
      loop: "{{ packages }}"
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

## Loops

- `loop`

  - a construct used in playbooks to **iterate over a list of items**
  - allow a task to be executed **multiple times** with different values.
  - Loops are useful for performing **repetitive tasks**, such as installing multiple packages, creating multiple users, or processing a list of files, without writing duplicate tasks.

- Create multiple users using loop

```yaml
- name: Create users
  hosts: localhost
  tasks:
    - user: name= "{{ item }}" state=present
      loop:
        - joe
        - george
        - ravi
        - mani
        - kiran
        - jazlan
        - emaan
        - mazin
        - izaan
        - mike
        - menaal
        - shoeb
        - rani
```

- Create multiple users with id using loop

```yaml
- name: Create users
  hosts: localhost
  tasks:
    - user: name= "{{ item.name }}" state=present uid="{{ item.uid }}"
      loop:
        - name: joe
          uid: 1010
        - name: george
          uid: 1011
        - name: ravi
          uid: 1012
        - name: mani
          uid: 1013
        - name: kiran
          uid: 1014
        - name: jazlan
          uid: 1015
        - name: emaan
          uid: 1016
        - name: mazin
          uid: 1017
        - name: izaan
          uid: 1018
        - name: mike
```

---

- Can use `with_*`
  - work with loopup plugin, same as loop

```yaml
- name: Create users
  hosts: localhost
  tasks:
    - user: name="{{ item }}" state=present
      with_items:
        - joe
        - george
        - ravi
        - mani
```

```yaml
- name: "loop fruit"
  hosts: loacalhost
  vars:
    fruits:
        - apple
        - banana
        - grape
        - orange
   tasks:
    - command: "echo {{ item }}"    # loop the with_itmes
      with_items: "{{ fruits }}" # refre to var define in a play

```
