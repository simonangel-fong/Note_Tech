# Linux - Process

[Back](../../index.md)

---

- [Linux - Process](#linux---process)
  - [Terminologies](#terminologies)
  - [Process](#process)
    - [Process states](#process-states)
  - [Process Management](#process-management)
    - [Background and Foreground Processes](#background-and-foreground-processes)
  - [Killing Processes](#killing-processes)

---

## Terminologies

- `Command`

  - refers to an **instruction** you give to the **shell** (the command-line interface) to execute a specific task.
  - can be a simple program, part of a larger application, or a shell built-in command.
  - can be used to **invoke** programs or **trigger** scripts to perform actions on the system.
  - e.g.,
    - `ls`, `pwd`, `cat`

- `Script`

  - a series of `commands` written in a scripting language,
  - designed to automate tasks.
  - e.g.,
    - A Bash script (`backup.sh`) to back up files

- `Program`

  - a set of **instructions** or code written to perform a specific task when executed.
  - can be as simple as a **script** or a **compiled binary**.
  - A program is usually **a single executable file**, which can be run on its own.
  - can be **standalone** (e.g., a simple utility like cat), or they can form **part of** a larger application.
  - e.g.,
    - `/bin/ls`, `/usr/bin/vim`, `myscript.sh`.

- `Application`

  - a software designed to **perform specific tasks** for the user or another application.
  - typically includes a **user interface** and interacts with the operating system or other applications to fulfill its purpose.
  - e.g.,
    - Web browser (e.g., Chrome, Firefox)
    - Word processor (e.g., Microsoft Word)
    - Music player (e.g., Spotify)

- `Process`

  - an **instance** of a **program** running on a computer.
  - Each process has its own memory space and system resources allocated to it.
    - A `process` is an **independent program** running in its own memory space
  - e.g.,
    - A running instance of the `python` interpreter.
    - The `nginx` web server process serving HTTP requests.

- `Daemon`

  - a **background process** that **runs continuously** to perform specific tasks or services.
  - Daemons usually start at boot time and do not interact directly with users.
  - e.g.,
    - `sshd`: Handles SSH connections.
    - `cron`: Schedules and runs jobs at specified times.

- `Threads`

  - the **smallest unit of execution** within a process.
  - A process can have multiple threads running concurrently, sharing the same memory space.
  - used to perform **multiple tasks simultaneously** within a single process, making them essential for **multitasking** and improving the **efficiency** of programs, especially in **multi-core systems**.
  - e.g.,
    - A web browser using multiple threads for rendering pages, handling user input, and downloading files.
    - A multithreaded application like a game that processes graphics, audio, and AI logic simultaneously.

- `Job`
  - a task or set of tasks that a system manages and executes.
  - In Unix-like systems, jobs often refer to tasks started by the shell and can be managed in the background or foreground.
  - e.g.,
    - A `wget` command downloading a file in the background
    - A data processing task scheduled by a job scheduler like `cron` or `at`.

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
