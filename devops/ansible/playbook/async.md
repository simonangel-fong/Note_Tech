# Ansible - Playbook: Asynchronous

[Back](../ansible.md)

- [Ansible - Playbook: Asynchronous](#ansible---playbook-asynchronous)
  - [Asynchronous](#asynchronous)
    - [Lab: Sync vs Async](#lab-sync-vs-async)
      - [Sync](#sync)
      - [Async](#async)

---

## Asynchronous

- By default, `Ansible` runs tasks **synchronously**
  - it waits **for each task** to **finish** before moving to the next one.
- `Async`:
  - fire off a long-running task and move on, checking back on it later (or not at all).

- key components:
  - `async`: **max seconds** to wait for the task to **complete** (sets a **timeout**)
  - `poll`: **how often** (in seconds) to **check** on the task.
    - `0`: fire and forget

---

### Lab: Sync vs Async

#### Sync

```yaml
# demo_sync.yaml
- name: Sync Demo - Sequential Tasks
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Record start time
      command: date +%s
      register: start_time

    - name: Task 1 - Slow operation (10s)
      command: sleep 10

    - name: Task 2 - Slower operation (15s)
      command: sleep 15

    - name: Task 3 - Slowest operation (20s)
      command: sleep 20

    - name: Record end time
      command: date +%s
      register: end_time

    - name: Show elapsed time
      debug:
        msg: >
          All 3 tasks completed sequentially.
          Elapsed time: {{ end_time.stdout | int - start_time.stdout | int }} seconds
          (expected ~45s = 10 + 15 + 20)
```

```sh
ansible-playbook demo_sync.yaml
# PLAY [Sync Demo - Sequential Tasks] *************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [localhost]

# TASK [Task 1 - Slow operation (10s)] ************************************************************************************************
# changed: [localhost]

# TASK [Task 2 - Slower operation (15s)] **********************************************************************************************
# changed: [localhost]

# TASK [Task 3 - Slowest operation (20s)] *********************************************************************************************
# changed: [localhost]

# TASK [Record end time] **************************************************************************************************************
# changed: [localhost]

# TASK [Show elapsed time] ************************************************************************************************************
# ok: [localhost] => {
#     "msg": "All 3 tasks completed sequentially. Elapsed time: 47 seconds (expected ~45s = 10 + 15 + 20)\n"
# }

# PLAY RECAP **************************************************************************************************************************
# localhost                  : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

---

#### Async

```yaml
# demo_async.yaml
- name: Async Demo - Parallel Tasks
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Record start time
      command: date +%s
      register: start_time

    - name: Task 1 - Slow operation (10s) [async]
      command: sleep 10
      async: 60     # max timeout — must be longer than the sleep duration
      poll: 0       # don't wait — move on immediately
      register: task1

    - name: Task 2 - Slower operation (15s) [async]
      command: sleep 15
      async: 60
      poll: 0
      register: task2

    - name: Task 3 - Slowest operation (20s) [async]
      command: sleep 20
      async: 60
      poll: 0
      register: task3

    - name: Wait for Task 1 to complete
      async_status:
        jid: "{{ task1.ansible_job_id }}"
      register: result1
      until: result1.finished
      retries: 12
      delay: 5

    - name: Wait for Task 2 to complete
      async_status:
        jid: "{{ task2.ansible_job_id }}"
      register: result2
      until: result2.finished
      retries: 12
      delay: 5

    - name: Wait for Task 3 to complete
      async_status:
        jid: "{{ task3.ansible_job_id }}"
      register: result3
      until: result3.finished
      retries: 12
      delay: 5

    - name: Record end time
      command: date +%s
      register: end_time

    - name: Show elapsed time
      debug:
        msg: >
          All 3 tasks completed in parallel.
          Elapsed time: {{ end_time.stdout | int - start_time.stdout | int }} seconds
          (expected ~20s = longest task wins, not 10 + 15 + 20)
```

```sh
ansible-playbook demo_async.yaml
# PLAY [Async Demo - Parallel Tasks] **************************************************************************************************

# TASK [Record start time] ************************************************************************************************************
# changed: [localhost]

# TASK [Task 1 - Slow operation (10s) [async]] ****************************************************************************************
# changed: [localhost]

# TASK [Task 2 - Slower operation (15s) [async]] **************************************************************************************
# changed: [localhost]

# TASK [Task 3 - Slowest operation (20s) [async]] *************************************************************************************
# changed: [localhost]

# TASK [Wait for Task 1 to complete] **************************************************************************************************
# FAILED - RETRYING: [localhost]: Wait for Task 1 to complete (12 retries left).
# FAILED - RETRYING: [localhost]: Wait for Task 1 to complete (11 retries left).
# changed: [localhost]

# TASK [Wait for Task 2 to complete] **************************************************************************************************
# FAILED - RETRYING: [localhost]: Wait for Task 2 to complete (12 retries left).
# changed: [localhost]

# TASK [Wait for Task 3 to complete] **************************************************************************************************
# FAILED - RETRYING: [localhost]: Wait for Task 3 to complete (12 retries left).
# changed: [localhost]

# TASK [Record end time] **************************************************************************************************************
# changed: [localhost]

# TASK [Show elapsed time] ************************************************************************************************************
# ok: [localhost] => {
#     "msg": "All 3 tasks completed in parallel. Elapsed time: 22 seconds (expected ~20s = longest task wins, not 10 + 15 + 20)\n"
# }

# PLAY RECAP **************************************************************************************************************************
# localhost                  : ok=9    changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```