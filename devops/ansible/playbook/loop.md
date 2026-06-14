# Ansible - Playbook: Loops

[Back](../ansible.md)

- [Ansible - Playbook: Loops](#ansible---playbook-loops)
  - [Loops](#loops)
  - [`with_items`](#with_items)
    - [Lab: `with_items`](#lab-with_items)
  - [`with_dict`](#with_dict)
    - [Lab: `with_dict`](#lab-with_dict)
  - [`with_subelements`](#with_subelements)
    - [Lab: `with_subelements`](#lab-with_subelements)
  - [`with_nested`](#with_nested)
  - [`with_sequence`](#with_sequence)
    - [Lab: `with_sequence`](#lab-with_sequence)
  - [`until`](#until)

---

## Loops

- `loop`
  - a construct used in playbooks to **iterate over a list of items**
  - allow a task to be executed **multiple times** with different values.
  - Loops are useful for performing **repetitive tasks**, such as installing multiple packages, creating multiple users, or processing a list of files, without writing duplicate tasks.

- Looping Deirective

---

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

## `with_items`

- `with_items`: iterate over a list of items. current items: `{{ item }}`

---

### Lab: `with_items`

- with `when`

```yaml
# demo_with_items.yaml
- hosts: ubuntu2, centos2
  tasks:
    - name: Configure a MOTD (message of the day)
      copy:
        content: "Welcome to {{ item }} Linux - Ansible Rocks!\n"
        dest: /etc/motd
      notify: MOTD changed
      with_items:
        - CentOS
        - Ubuntu
      when: ansible_distribution == item

  handlers:
    - name: MOTD changed
      debug:
        msg: The MOTD was changed
```

```sh
ansible-playbook demo_with_items.yaml
# TASK [Configure a MOTD (message of the day)] ****************************************************************************************
# skipping: [ubuntu2] => (item=CentOS)
# changed: [centos2] => (item=CentOS)
# skipping: [centos2] => (item=Ubuntu)
# changed: [ubuntu2] => (item=Ubuntu)

# RUNNING HANDLER [MOTD changed] ******************************************************************************************************
# ok: [ubuntu2] => {
#     "msg": "The MOTD was changed"
# }
# ok: [centos2] => {
#     "msg": "The MOTD was changed"
# }
```

---

- create users

```yaml
# demo_with_item_user.yaml
- hosts:
    - ubuntu
    - centos2
    - centos3
  tasks:
    - name: Creating user
      user:
        name: "{{ item }}"
      with_items:
        - james
        - hayley
        - lily
        - anwen
```

```sh
ansible-playbook demo_with_item_user.yaml
# TASK [Creating user] ****************************************************************************************************************
# changed: [ubuntu3] => (item=james)
# changed: [ubuntu1] => (item=james)
# changed: [ubuntu2] => (item=james)
# changed: [centos3] => (item=james)
# changed: [centos2] => (item=james)
# changed: [ubuntu3] => (item=hayley)
# changed: [ubuntu2] => (item=hayley)
# changed: [ubuntu1] => (item=hayley)
# changed: [centos2] => (item=hayley)
# changed: [centos3] => (item=hayley)
# changed: [ubuntu3] => (item=lily)
# changed: [ubuntu2] => (item=lily)
# changed: [ubuntu1] => (item=lily)
# changed: [centos3] => (item=lily)
# changed: [centos2] => (item=lily)
# changed: [ubuntu1] => (item=anwen)
# changed: [ubuntu3] => (item=anwen)
# changed: [ubuntu2] => (item=anwen)
# changed: [centos3] => (item=anwen)
# changed: [centos2] => (item=anwen)

ansible-playbook demo_with_item_user.yaml
# TASK [Creating user] ****************************************************************************************************************
# ok: [centos2] => (item=james)
# ok: [ubuntu2] => (item=james)
# ok: [ubuntu3] => (item=james)
# ok: [centos3] => (item=james)
# ok: [ubuntu1] => (item=james)
# ok: [centos2] => (item=hayley)
# ok: [ubuntu2] => (item=hayley)
# ok: [centos3] => (item=hayley)
# ok: [ubuntu1] => (item=hayley)
# ok: [ubuntu3] => (item=hayley)
# ok: [centos2] => (item=lily)
# ok: [ubuntu2] => (item=lily)
# ok: [centos3] => (item=lily)
# ok: [ubuntu1] => (item=lily)
# ok: [ubuntu3] => (item=lily)
# ok: [centos2] => (item=anwen)
# ok: [centos3] => (item=anwen)
# ok: [ubuntu2] => (item=anwen)
# ok: [ubuntu1] => (item=anwen)
# ok: [ubuntu3] => (item=anwen)
```

- delete users

```yaml
# demo_with_item_user_del.yaml
- hosts:
    - ubuntu
    - centos2
    - centos3
  tasks:
    - name: Removing user
      user:
        name: "{{ item }}"
        state: absent
      with_items:
        - james
        - hayley
        - lily
        - anwen
```

```sh
ansible-playbook demo_with_item_user_del.yaml
# TASK [Creating user] ****************************************************************************************************************
# changed: [ubuntu1] => (item=james)
# changed: [ubuntu3] => (item=james)
# changed: [ubuntu2] => (item=james)
# changed: [centos3] => (item=james)
# changed: [centos2] => (item=james)
# changed: [ubuntu1] => (item=hayley)
# changed: [ubuntu3] => (item=hayley)
# changed: [ubuntu2] => (item=hayley)
# changed: [centos3] => (item=hayley)
# changed: [centos2] => (item=hayley)
# changed: [ubuntu1] => (item=lily)
# changed: [ubuntu3] => (item=lily)
# changed: [ubuntu2] => (item=lily)
# changed: [centos3] => (item=lily)
# changed: [centos2] => (item=lily)
# changed: [ubuntu3] => (item=anwen)
# changed: [ubuntu1] => (item=anwen)
# changed: [ubuntu2] => (item=anwen)
# changed: [centos3] => (item=anwen)
# changed: [centos2] => (item=anwen)
```

---

## `with_dict`

- `with_dict`: iterate over a dictionary. current items: `{{ item.key }}` and `{{ item.value }}`

---

### Lab: `with_dict`

```yaml
# demo_with_dict_user_create.yaml
- hosts:
    - ubuntu
    - centos2
    - centos3
  tasks:
    - name: Creating user
      user:
        name: "{{ item.key }}"
        comment: "{{ item.value.full_name }}"
      with_dict:
        james:
          full_name: James Spurin
        hayley:
          full_name: Hayley Spurin
        lily:
          full_name: Lily Spurin
        anwen:
          full_name: Anwen Spurin
```

```sh
ansible-playbook demo_with_dict_user_create.yaml
# TASK [Creating user] ****************************************************************************************************************
# changed: [ubuntu1] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [ubuntu2] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [ubuntu3] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [centos2] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [centos3] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [ubuntu2] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [ubuntu1] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [ubuntu3] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [centos2] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [centos3] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [ubuntu1] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [ubuntu2] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [ubuntu3] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [centos2] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [centos3] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [ubuntu1] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [ubuntu2] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [ubuntu3] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [centos2] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [centos3] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
```

- remove

```yaml
# demo_with_dict_user_del.yaml
- hosts:
    - ubuntu
    - centos2
    - centos3
  tasks:
    - name: Removing user
      user:
        name: "{{ item.key }}"
        comment: "{{ item.value.full_name }}"
        state: absent
      with_dict:
        james:
          full_name: James Spurin
        hayley:
          full_name: Hayley Spurin
        lily:
          full_name: Lily Spurin
        anwen:
          full_name: Anwen Spurin
```

```sh
ansible-playbook demo_with_dict_user_del.yaml
# TASK [Removing user] ****************************************************************************************************************
# changed: [ubuntu3] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [ubuntu1] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [centos2] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [ubuntu2] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [centos3] => (item={'key': 'james', 'value': {'full_name': 'James Spurin'}})
# changed: [ubuntu2] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [ubuntu3] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [ubuntu1] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [centos2] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [centos3] => (item={'key': 'hayley', 'value': {'full_name': 'Hayley Spurin'}})
# changed: [ubuntu2] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [ubuntu3] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [ubuntu1] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [centos2] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [centos3] => (item={'key': 'lily', 'value': {'full_name': 'Lily Spurin'}})
# changed: [ubuntu2] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [ubuntu3] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [ubuntu1] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [centos2] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
# changed: [centos3] => (item={'key': 'anwen', 'value': {'full_name': 'Anwen Spurin'}})
```

---

## `with_subelements`

- `with_subelements`: iterate over a list of dictionaries and a nested list attribute within each dictionary.

---

### Lab: `with_subelements`

- create user and pwd

```yaml
# demo_with_subelements_user_del.yaml
- hosts:
    - ubuntu
    - centos2
    - centos3
  tasks:
    - name: Creating user
      user:
        name: "{{ item.1 }}"
        comment: "{{ item.1 | title }} {{ item.0.surname }}"
        # https://docs.ansible.com/ansible/latest/plugins/lookup/password.html
        password: "{{ lookup('password', '/dev/null length=15 chars=ascii_letters,digits,hexdigits,punctuation') | password_hash('sha512') }}"
      with_subelements:
        - - surname: Spurin
            members:
              - james
              - hayley
              - lily
              - anwen
          - surname: Darlington
            members:
              - freya
          - surname: Jalba
            members:
              - ana
          - surname: Angne
            members:
              - abhishek
          - surname: Mahmood
            members:
              - sara
        - members
```

```sh
ansible-playbook demo_with_subelements_user_del.yaml
# TASK [Creating user] ****************************************************************************************************************
# changed: [ubuntu2] => (item=[{'surname': 'Spurin'}, 'james'])
# changed: [ubuntu1] => (item=[{'surname': 'Spurin'}, 'james'])
# changed: [ubuntu3] => (item=[{'surname': 'Spurin'}, 'james'])
# changed: [centos3] => (item=[{'surname': 'Spurin'}, 'james'])
# changed: [centos2] => (item=[{'surname': 'Spurin'}, 'james'])
# changed: [ubuntu3] => (item=[{'surname': 'Spurin'}, 'hayley'])
# changed: [ubuntu1] => (item=[{'surname': 'Spurin'}, 'hayley'])
# changed: [ubuntu2] => (item=[{'surname': 'Spurin'}, 'hayley'])
# changed: [centos3] => (item=[{'surname': 'Spurin'}, 'hayley'])
# changed: [centos2] => (item=[{'surname': 'Spurin'}, 'hayley'])
# changed: [ubuntu3] => (item=[{'surname': 'Spurin'}, 'lily'])
# changed: [ubuntu1] => (item=[{'surname': 'Spurin'}, 'lily'])
# changed: [ubuntu2] => (item=[{'surname': 'Spurin'}, 'lily'])
# changed: [centos2] => (item=[{'surname': 'Spurin'}, 'lily'])
# changed: [centos3] => (item=[{'surname': 'Spurin'}, 'lily'])
# changed: [ubuntu3] => (item=[{'surname': 'Spurin'}, 'anwen'])
# changed: [ubuntu2] => (item=[{'surname': 'Spurin'}, 'anwen'])
# changed: [centos2] => (item=[{'surname': 'Spurin'}, 'anwen'])
# changed: [ubuntu1] => (item=[{'surname': 'Spurin'}, 'anwen'])
# changed: [centos3] => (item=[{'surname': 'Spurin'}, 'anwen'])
# changed: [ubuntu3] => (item=[{'surname': 'Darlington'}, 'freya'])
# changed: [ubuntu2] => (item=[{'surname': 'Darlington'}, 'freya'])
# changed: [ubuntu1] => (item=[{'surname': 'Darlington'}, 'freya'])
# changed: [centos2] => (item=[{'surname': 'Darlington'}, 'freya'])
# changed: [centos3] => (item=[{'surname': 'Darlington'}, 'freya'])
# changed: [ubuntu3] => (item=[{'surname': 'Jalba'}, 'ana'])
# changed: [ubuntu2] => (item=[{'surname': 'Jalba'}, 'ana'])
# changed: [ubuntu1] => (item=[{'surname': 'Jalba'}, 'ana'])
# changed: [centos2] => (item=[{'surname': 'Jalba'}, 'ana'])
# changed: [centos3] => (item=[{'surname': 'Jalba'}, 'ana'])
# changed: [ubuntu3] => (item=[{'surname': 'Angne'}, 'abhishek'])
# changed: [ubuntu2] => (item=[{'surname': 'Angne'}, 'abhishek'])
# changed: [ubuntu1] => (item=[{'surname': 'Angne'}, 'abhishek'])
# changed: [centos2] => (item=[{'surname': 'Angne'}, 'abhishek'])
# changed: [centos3] => (item=[{'surname': 'Angne'}, 'abhishek'])
# changed: [ubuntu3] => (item=[{'surname': 'Mahmood'}, 'sara'])
# changed: [ubuntu2] => (item=[{'surname': 'Mahmood'}, 'sara'])
# changed: [ubuntu1] => (item=[{'surname': 'Mahmood'}, 'sara'])
# changed: [centos2] => (item=[{'surname': 'Mahmood'}, 'sara'])
# changed: [centos3] => (item=[{'surname': 'Mahmood'}, 'sara'])
```

---

## `with_nested`

- `with_nested`:
  - iterate over multiple lists by creating a Cartesian product of all their elements.

```yaml
# demo_with_nested_user_del.yaml
- hosts:
    - ubuntu
    - centos2
    - centos3
  tasks:
    - name: Creating user directories
      file:
        dest: "/home/{{ item.0 }}/{{ item.1 }}"
        owner: "{{ item.0 }}"
        group: "{{ item.0 }}"
        state: directory
      with_nested:
        - [james, hayley, freya, lily, anwen, ana, abhishek, sara]
        - [photos, movies, documents]
```

```sh
ansible-playbook demo_with_nested_user_del.yaml
# changed: [centos3] => (item=['james', 'photos'])
# changed: [centos2] => (item=['james', 'photos'])
# changed: [ubuntu1] => (item=['james', 'photos'])
# changed: [ubuntu2] => (item=['james', 'photos'])
# changed: [ubuntu3] => (item=['james', 'photos'])
# changed: [centos3] => (item=['james', 'movies'])
# changed: [centos2] => (item=['james', 'movies'])
# changed: [ubuntu1] => (item=['james', 'movies'])
# changed: [ubuntu3] => (item=['james', 'movies'])
# changed: [ubuntu2] => (item=['james', 'movies'])
# changed: [centos2] => (item=['james', 'documents'])
# changed: [centos3] => (item=['james', 'documents'])
# ...
```

---

## `with_sequence`

- `with_sequence`:
  - generate and iterate over a numerical sequence of items.

### Lab: `with_sequence`

```yaml
# demo_with_sequence.yaml
- hosts:
    - ubuntu
    - centos2
    - centos3
  tasks:
    - name: Create sequence directories
      file:
        dest: "/home/james/sequence_{{ item }}"
        state: directory
      with_sequence: start=0 end=100 stride=10
```

```sh
ansible-playbook demo_with_sequence.yaml
# TASK [Create sequence directories] **************************************************************************************************
# changed: [centos3] => (item=0)
# changed: [centos2] => (item=0)
# changed: [ubuntu2] => (item=0)
# changed: [ubuntu3] => (item=0)
# changed: [ubuntu1] => (item=0)
# changed: [centos2] => (item=10)
# changed: [centos3] => (item=10)
# changed: [ubuntu2] => (item=10)
# changed: [ubuntu3] => (item=10)
# ...
```

---

## `until`


