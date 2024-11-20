# Linux - Process

[Back](../../index.md)

---

- [Linux - Process](#linux---process)
  - [Process](#process)
    - [Process states](#process-states)
  - [Process Management](#process-management)
    - [Background and Foreground Processes](#background-and-foreground-processes)
  - [Killing Processes](#killing-processes)

---

## Process

- `Process`

  - In Linux, a `process` is a **running instance** of a **program** or **command**.

---

### Process states

- Processes can go through different states, including:
  - `Running`:
    - The process is either **running** or **ready to run**.
  - `Sleeping`:
    - The process is **waiting for a resource** to be available.
  - `Interruptible sleep`:
    - The process is **waiting on data**, such as input from the terminal.
  - `Uninterruptible sleep`:
    - The process is **waiting on something**, and **interrupting** could cause major **issues**.
  - `Stopped`:
    - The process is put **on hold** and **not responsive**.
  - `Zombie`:
    - The process is **dead** but the entry for the process is **still present** in the table.

---

## Process Management

| Command          | Desc                                       |
| ---------------- | ------------------------------------------ |
| `ps`             | Display process status of current session. |
| `ps -ef`         | Full format listing all processes.         |
| `ps -eH`         | Display a process tree.                    |
| `ps -e --forest` | Display a process tree.                    |
| `ps -u username` | Display username’s processes.              |
| `ps -p pid`      | Display information for PID.               |
| `pstree`         | Display processes in a tree format.        |
| `top`            | Interactive process viewer.                |

---

### Background and Foreground Processes

- 2 Types of processes:
  - `Foreground processes`:
    - Also known as `interactive processes`
    - these processes **depend on the user** for input.
  - `Background processes`:
    - Also known as `non-interactive` or `automatic processes`
    - these processes run **independently of the user**.

| Shortcut    | Desc                                    |
| ----------- | --------------------------------------- |
| `command &` | **Start** command in **background**.    |
| `Ctrl-c`    | **Kill** the **foreground** process.    |
| `Ctrl-z`    | **Suspend** the **foreground** process. |

- Suspend:
  - not running in the background, but stop running.

| Command     | Desc                                        |
| ----------- | ------------------------------------------- |
| `bg`        | Send the current job to the background.     |
| `bg %num`   | Background a suspended process with number. |
| `fg`        | Foreground the last background process.     |
| `fg %num`   | Foreground a background process with number |
| `kill`      | Kill a process by job number or PID.        |
| `jobs`      | List jobs.                                  |
| `jobs %num` | List a job wit job number.                  |

- Symbol for jobs:
  - `%%`/`%+`: current job
  - `%-`: previous job

```sh
# list current job
jobs %%
jobs %+

# list previous job
jobs %-
```

- foreground a bg process
  - `fg %num`
  - `%num`: donot need `fg`

---

## Killing Processes

| Command         | Desc                               |
| --------------- | ---------------------------------- |
| `Ctrl-c`        | **Kills** the **foreground** proc. |
| `kill pid`      | Kill a process with its id.        |
| `kill %jobnum`  | Kill a process with its job num.   |
| `kill -sig pid` | Send a signal to a process.        |
| `kill -l`       | Display a list of signals.         |

- Send a signal to a process.
  - default:
    - `kill -15 123` = `kill -TERM 123` = `kill 123`
  - `kill -9 123`
