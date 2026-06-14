# Ansible - Playbook: Fork & Serial

[Back](../ansible.md)

- [Ansible - Playbook: Fork \& Serial](#ansible---playbook-fork--serial)
  - [Fork \& Serial](#fork--serial)
  - [Lab: `forks` \& `serial`](#lab-forks--serial)
    - [Default](#default)
    - [Fortk](#fortk)
    - [Serial](#serial)
    - [Step Serial](#step-serial)
  - [`free` strategy](#free-strategy)

---

## Fork & Serial

- `Forks`
  - **how many hosts** Ansible works on **simultaneously**.
  - Global configuration: `ansible.cfg`
  - Default: `5`

---

- `Serial`
  - **how many hosts** move through the **entire play** before the next batch starts.
  - Default:
    - no serial
    - executes task across all hosts:

```yaml
serial: 1          # one host at a time
serial: 3          # 3 hosts at a time
serial: "30%"      # 30% of hosts at a time
serial:            # ramp up — slow start, then faster
  - 1
  - 3
  - "50%"
```

---

- `forks` vs `serial`

| Feature         | `forks`                                        | `serial`                                            |
| --------------- | ---------------------------------------------- | --------------------------------------------------- |
| Primary Purpose | Global **parallelism** & CPU/memory management | **Rolling updates** & application uptime management |
| Scope           | Task-level execution                           | Play-level execution                                |
| Default Value   | 5                                              | All hosts in the inventory at once                  |
| Where Defined   | `ansible.cfg` or via command-line `-f`         | Directly inside the Playbook                        |

---

## Lab: `forks` & `serial`

### Default

```yaml
# demo_baseline.yaml
- name: "Lab - Baseline Demo"
  hosts: linux
  gather_facts: false
  tasks:
    - name: Record start time
      command: date +%s
      register: start_time

    - name: "Slow task (5s) on {{ inventory_hostname }}"
      command: sleep 5

    - name: Show host completion time
      command: date +"%T"
      register: ts

    - name: "Done"
      debug:
        msg: "HOST={{ inventory_hostname }} finished at {{ ts.stdout }}"

    - name: Record end time
      command: date +%s
      register: end_time
      run_once: true

    - name: Show total elapsed time
      debug:
        msg: "Total elapsed: {{ end_time.stdout | int - start_time.stdout | int }}s"
      run_once: true
```

```sh
# centos1,centos2,centos3,ubuntu1,ubuntu2,ubuntu3 -> total elapsed
ansible-playbook demo_baseline.yaml
# # TASK [Show total elapsed time] ******************************************************************************************************
# ok: [centos1] => {
#     "msg": "Total elapsed: 6s"
# }
```

---

### Fortk

```sh
# centos1,centos2 -> centos3,ubuntu1 -> ubuntu2,ubuntu3 -> total elapsed
ansible-playbook demo_baseline.yaml -f 2
# PLAY [Lab - Baseline Demo] **********************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [centos1]
# changed: [centos2]
# changed: [ubuntu1]
# changed: [centos3]
# changed: [ubuntu2]
# changed: [ubuntu3]

# TASK [Slow task (5s) on centos1] ****************************************************************************************************
# changed: [centos2]
# changed: [centos1]
# changed: [centos3]
# changed: [ubuntu1]
# changed: [ubuntu2]
# changed: [ubuntu3]

# TASK [Show host completion time] ****************************************************************************************************
# changed: [centos1]
# changed: [centos2]
# changed: [centos3]
# changed: [ubuntu1]
# changed: [ubuntu2]
# changed: [ubuntu3]

# TASK [Done] *************************************************************************************************************************
# ok: [centos1] => {
#     "msg": "HOST=centos1 finished at 22:32:03"
# }
# ok: [centos2] => {
#     "msg": "HOST=centos2 finished at 22:32:03"
# }
# ok: [centos3] => {
#     "msg": "HOST=centos3 finished at 22:32:03"
# }
# ok: [ubuntu1] => {
#     "msg": "HOST=ubuntu1 finished at 22:32:03"
# }
# ok: [ubuntu2] => {
#     "msg": "HOST=ubuntu2 finished at 22:32:04"
# }
# ok: [ubuntu3] => {
#     "msg": "HOST=ubuntu3 finished at 22:32:04"
# }

# TASK [Record end time] **************************************************************************************************************
# changed: [centos1]

# TASK [Show total elapsed time] ******************************************************************************************************
# ok: [centos1] => {
#     "msg": "Total elapsed: 18s"
# }

# PLAY RECAP **************************************************************************************************************************
# centos1                    : ok=6    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# centos2                    : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# centos3                    : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### Serial

```yaml
# demo_serial.yaml
- name: "Lab - Serial Demo"
  hosts: linux
  gather_facts: false
  serial: 2

  tasks:
    - name: Record start time
      command: date +%s
      register: start_time

    - name: "Slow task (5s) on {{ inventory_hostname }}"
      command: sleep 5

    - name: Show host completion time
      command: date +"%T"
      register: ts

    - name: "Done"
      debug:
        msg: "HOST={{ inventory_hostname }} finished at {{ ts.stdout }}"

    - name: Record end time
      command: date +%s
      register: end_time
      run_once: true

    - name: Show total elapsed time
      debug:
        msg: "Total elapsed: {{ end_time.stdout | int - start_time.stdout | int }}s"
      run_once: true
```

```sh
# centos1,centos2 -> total elapsed ->
# ubuntu1,centos3 -> total elapsed ->
# ubuntu2,ubuntu3 -> total elapsed
ansible-playbook demo_serial.yaml
# PLAY [Lab - Serial Demo] ************************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [centos1]
# changed: [centos2]

# TASK [Slow task (5s) on centos1] ****************************************************************************************************
# changed: [centos1]
# changed: [centos2]

# TASK [Show host completion time] ****************************************************************************************************
# changed: [centos1]
# changed: [centos2]

# TASK [Done] *************************************************************************************************************************
# ok: [centos1] => {
#     "msg": "HOST=centos1 finished at 22:26:17"
# }
# ok: [centos2] => {
#     "msg": "HOST=centos2 finished at 22:26:17"
# }

# TASK [Record end time] **************************************************************************************************************
# changed: [centos1]

# TASK [Show total elapsed time] ******************************************************************************************************
# ok: [centos1] => {
#     "msg": "Total elapsed: 6s"
# }

# PLAY [Lab - Serial Demo] ************************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [ubuntu1]
# changed: [centos3]

# TASK [Slow task (5s) on centos1] ****************************************************************************************************
# changed: [centos3]
# changed: [ubuntu1]

# TASK [Show host completion time] ****************************************************************************************************
# changed: [centos3]
# changed: [ubuntu1]

# TASK [Done] *************************************************************************************************************************
# ok: [centos3] => {
#     "msg": "HOST=centos3 finished at 22:26:23"
# }
# ok: [ubuntu1] => {
#     "msg": "HOST=ubuntu1 finished at 22:26:23"
# }

# TASK [Record end time] **************************************************************************************************************
# changed: [centos3]

# TASK [Show total elapsed time] ******************************************************************************************************
# ok: [centos3] => {
#     "msg": "Total elapsed: 6s"
# }

# PLAY [Lab - Serial Demo] ************************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [ubuntu3]
# changed: [ubuntu2]

# TASK [Slow task (5s) on centos1] ****************************************************************************************************
# changed: [ubuntu2]
# changed: [ubuntu3]

# TASK [Show host completion time] ****************************************************************************************************
# changed: [ubuntu2]
# changed: [ubuntu3]

# TASK [Done] *************************************************************************************************************************
# ok: [ubuntu2] => {
#     "msg": "HOST=ubuntu2 finished at 22:26:29"
# }
# ok: [ubuntu3] => {
#     "msg": "HOST=ubuntu3 finished at 22:26:29"
# }

# TASK [Record end time] **************************************************************************************************************
# changed: [ubuntu2]

# TASK [Show total elapsed time] ******************************************************************************************************
# ok: [ubuntu2] => {
#     "msg": "Total elapsed: 6s"
# }
```

---

### Step Serial

```yaml
# demo_serial_step.yaml
- name: "Lab - Serial Demo"
  hosts:
    - ubuntu
    - centos1
    - centos2
  gather_facts: false
  serial:
    - 20%
    - 40%
    - 40%

  tasks:
    - name: Record start time
      command: date +%s
      register: start_time

    - name: "Slow task (5s) on {{ inventory_hostname }}"
      command: sleep 5

    - name: Show host completion time
      command: date +"%T"
      register: ts

    - name: "Done"
      debug:
        msg: "HOST={{ inventory_hostname }} finished at {{ ts.stdout }}"

    - name: Record end time
      command: date +%s
      register: end_time
      run_once: true

    - name: Show total elapsed time
      debug:
        msg: "Total elapsed: {{ end_time.stdout | int - start_time.stdout | int }}s"
      run_once: true
```

```sh
# ubuntu1 -> total elapsed ->
# ubuntu2,ubuntu2 -> total elapsed ->
# centos1,centos2 -> total elapsed
ansible-playbook demo_serial_step.yaml
# PLAY [Lab - Serial Demo] ************************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [ubuntu1]

# TASK [Slow task (5s) on ubuntu1] ****************************************************************************************************
# changed: [ubuntu1]

# TASK [Show host completion time] ****************************************************************************************************
# changed: [ubuntu1]

# TASK [Done] *************************************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "HOST=ubuntu1 finished at 22:44:56"
# }

# TASK [Record end time] **************************************************************************************************************
# changed: [ubuntu1]

# TASK [Show total elapsed time] ******************************************************************************************************
# ok: [ubuntu1] => {
#     "msg": "Total elapsed: 7s"
# }

# PLAY [Lab - Serial Demo] ************************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [ubuntu2]
# changed: [ubuntu3]

# TASK [Slow task (5s) on ubuntu1] ****************************************************************************************************
# changed: [ubuntu3]
# changed: [ubuntu2]

# TASK [Show host completion time] ****************************************************************************************************
# changed: [ubuntu3]
# changed: [ubuntu2]

# TASK [Done] *************************************************************************************************************************
# ok: [ubuntu2] => {
#     "msg": "HOST=ubuntu2 finished at 22:45:03"
# }
# ok: [ubuntu3] => {
#     "msg": "HOST=ubuntu3 finished at 22:45:03"
# }

# TASK [Record end time] **************************************************************************************************************
# changed: [ubuntu2]

# TASK [Show total elapsed time] ******************************************************************************************************
# ok: [ubuntu2] => {
#     "msg": "Total elapsed: 6s"
# }

# PLAY [Lab - Serial Demo] ************************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [centos2]
# changed: [centos1]

# TASK [Slow task (5s) on ubuntu1] ****************************************************************************************************
# changed: [centos2]
# changed: [centos1]

# TASK [Show host completion time] ****************************************************************************************************
# changed: [centos1]
# changed: [centos2]

# TASK [Done] *************************************************************************************************************************
# ok: [centos1] => {
#     "msg": "HOST=centos1 finished at 22:45:09"
# }
# ok: [centos2] => {
#     "msg": "HOST=centos2 finished at 22:45:09"
# }

# TASK [Record end time] **************************************************************************************************************
# changed: [centos1]

# TASK [Show total elapsed time] ******************************************************************************************************
# ok: [centos1] => {
#     "msg": "Total elapsed: 5s"
# }

# PLAY RECAP **************************************************************************************************************************
# centos1                    : ok=6    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# centos2                    : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=6    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=6    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

## `free` strategy

- `free` strategy:
  - a **play-level execution** setting that lets each managed host work through playbook tasks **independently**.

```yaml
# demo_random.yaml
- name: "Lab - free Strategy Demo(base)"
  hosts: linux
  gather_facts: false
  tasks:
    - name: Task 1
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 2
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 3
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 4
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 5
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 6
      command: "/bin/sleep {{ 10 |random}}"
```

```sh
ansible-playbook demo_random.yaml
# PLAY [Lab - free Strategy Demo(base)] ***********************************************************************************************

# TASK [Task 1] ***********************************************************************************************************************
# changed: [ubuntu3]
# changed: [centos2]
# changed: [ubuntu1]
# changed: [ubuntu2]
# changed: [centos3]
# changed: [centos1]

# TASK [Task 2] ***********************************************************************************************************************
# changed: [centos3]
# changed: [ubuntu2]
# changed: [centos1]
# changed: [centos2]
# changed: [ubuntu1]
# changed: [ubuntu3]

# TASK [Task 3] ***********************************************************************************************************************
# changed: [centos3]
# changed: [ubuntu2]
# changed: [centos2]
# changed: [centos1]
# changed: [ubuntu1]
# changed: [ubuntu3]

# TASK [Task 4] ***********************************************************************************************************************
# changed: [ubuntu2]
# changed: [ubuntu1]
# changed: [centos3]
# changed: [ubuntu3]
# changed: [centos2]
# changed: [centos1]

# TASK [Task 5] ***********************************************************************************************************************
# changed: [ubuntu2]
# changed: [ubuntu1]
# changed: [centos3]
# changed: [centos1]
# changed: [centos2]
# changed: [ubuntu3]

# TASK [Task 6] ***********************************************************************************************************************
# changed: [ubuntu2]
# changed: [centos2]
# changed: [ubuntu1]
# changed: [centos1]
# changed: [centos3]
# changed: [ubuntu3]

# PLAY RECAP **************************************************************************************************************************
# centos1                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# centos2                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# centos3                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

```yaml
# demo_random_free.yaml
- name: "Lab - free Strategy Demo(free)"
  hosts: linux
  gather_facts: false
  strategy: free

  tasks:
    - name: Task 1
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 2
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 3
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 4
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 5
      command: "/bin/sleep {{ 10 |random}}"

    - name: Task 6
      command: "/bin/sleep {{ 10 |random}}"
```

```sh
ansible-playbook demo_random_free.yaml
# PLAY [Lab - free Strategy Demo(free)] ***********************************************************************************************

# TASK [Task 1] ***********************************************************************************************************************
# changed: [ubuntu3]
# changed: [centos2]
# changed: [ubuntu1]
# changed: [centos3]

# TASK [Task 2] ***********************************************************************************************************************
# changed: [ubuntu3]

# TASK [Task 1] ***********************************************************************************************************************
# changed: [ubuntu2]
# changed: [centos1]

# TASK [Task 2] ***********************************************************************************************************************
# changed: [centos1]
# changed: [ubuntu2]
# changed: [ubuntu1]
# changed: [centos2]

# TASK [Task 3] ***********************************************************************************************************************
# changed: [centos1]
# changed: [ubuntu3]
# changed: [ubuntu1]

# TASK [Task 2] ***********************************************************************************************************************
# changed: [centos3]

# TASK [Task 3] ***********************************************************************************************************************
# changed: [centos2]
# changed: [centos3]

# TASK [Task 4] ***********************************************************************************************************************
# changed: [centos1]

# TASK [Task 3] ***********************************************************************************************************************
# changed: [ubuntu2]

# TASK [Task 4] ***********************************************************************************************************************
# changed: [centos2]

# TASK [Task 5] ***********************************************************************************************************************
# changed: [centos1]
# changed: [centos2]

# TASK [Task 4] ***********************************************************************************************************************
# changed: [ubuntu3]
# changed: [ubuntu1]

# TASK [Task 6] ***********************************************************************************************************************
# changed: [centos2]

# TASK [Task 4] ***********************************************************************************************************************
# changed: [ubuntu2]
# changed: [centos3]

# TASK [Task 5] ***********************************************************************************************************************
# changed: [ubuntu3]

# TASK [Task 6] ***********************************************************************************************************************
# changed: [ubuntu3]

# TASK [Task 5] ***********************************************************************************************************************
# changed: [ubuntu2]
# changed: [centos3]

# TASK [Task 6] ***********************************************************************************************************************
# changed: [centos1]

# TASK [Task 5] ***********************************************************************************************************************
# changed: [ubuntu1]

# TASK [Task 6] ***********************************************************************************************************************
# changed: [centos3]
# changed: [ubuntu1]
# changed: [ubuntu2]

# PLAY RECAP **************************************************************************************************************************
# centos1                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# centos2                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# centos3                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu1                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=6    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
