# Linux - Software Management: Process

[Back](../../index.md)

- [Linux - Software Management: Process](#linux---software-management-process)
  - [Terminologies](#terminologies)
    - [`daemon` vs `service`](#daemon-vs-service)
  - [Process](#process)
    - [Process states](#process-states)
  - [`top`: Display processes](#top-display-processes)
    - [System Summary](#system-summary)
    - [Process List](#process-list)
    - [Useful Interactions (While Running)](#useful-interactions-while-running)
  - [`ps`: Display processes information](#ps-display-processes-information)
  - [Background and Foreground Processes](#background-and-foreground-processes)
    - [Switch between foreground and background processes](#switch-between-foreground-and-background-processes)
  - [Killing Processes](#killing-processes)
  - [Example: Switch Foreground and Background](#example-switch-foreground-and-background)
    - [Create a long running task.](#create-a-long-running-task)
    - [Bring process to Foreground](#bring-process-to-foreground)
    - [Send the jobs to Background](#send-the-jobs-to-background)
    - [Terminate the Jobs](#terminate-the-jobs)
  - [`lsof`: list files opened by processes](#lsof-list-files-opened-by-processes)

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
  - Often have names ending with a `d`. e.g.,
    - `sshd`: Handles incoming SSH connections.
    - `httpd`: Manages web server requests.
    - `crond`: Schedules tasks to run at specified times.

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

- `systemd`

  - a collection of system management daemons, utilities, and libraries which serves as a replacement of System V init daemon.
  - the parent process of most of the daemons.

- `systemctl`:
  - a **systemd utility** that is responsible for controlling the `systemd` system and service manage.
  - Services are controlled by `systemctl`

---

### `daemon` vs `service`

- A `service` can consist of one or more `daemons` or other `processes` working together.

| Aspect     | Daemon                                          | Service                                       |
| ---------- | ----------------------------------------------- | --------------------------------------------- |
| Definition | A background process performing specific tasks. | A system-wide functionality or feature.       |
| Relation   | A daemon often underpins a service.             | A service may consist of one or more daemons. |
| Management | Managed as processes in the OS.                 | Managed via init systems like `systemctl`.    |
| Examples   | sshd, httpd, crond                              | "SSH service", "Web Server service"           |

- Think of a `daemon` as a **worker** and a `service` as the **job** they perform. For example:
  - Daemon: `httpd` (Apache daemon).
  - Service: The **web server functionality** provided by Apache.

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

---

## `top`: Display processes

| Command           | Desc                                                  |
| ----------------- | ----------------------------------------------------- |
| `top`             | Display processes                                     |
| `top -dNUM`       | Set the delay between updates (default: `3` seconds). |
| `top -nNUM`       | Specify the number of updates before exiting.         |
| `top -u username` | Show processes for a specific user.                   |

![top01](./pic/top01.png)

### System Summary

- Line 1: uptime info
  - current time
  - uptime
  - number of login users
  - average system load over 1, 5, and 15 minutes.
- Line 2: Task info
  - `total`
  - `running`
  - `sleeping`
  - `stopped`
  - `zombie`
- Line 3: CPU Usage
  - `us`: CPU time % spent on **user processes**.
  - `sy`: CPU time % spent on **system (kernel) processes**.
  - `ni`: CPU time % spent on processes with **adjusted niceness**.
  - `id`: CPU time % spent **idle**.
  - `wa`: CPU time % **waiting for I/O** operations.
  - `hi`: CPU time % spent handling **hardware interrupts**.
  - `si`: CPU time % spent handling **software interrupts**.
  - `st`: CPU time % stolen **from the virtual machine** by the host.
- Line 4: Memory Usage Displays total,free, used, and buff/cache.
- Line 5: Swap Usage Displays total, used, free, and available memory.

---

### Process List

| Column    | Desc                                                                   |
| --------- | ---------------------------------------------------------------------- |
| `PID`     | Process ID, a unique identifier for the process.                       |
| `USER`    | The user who owns the process.                                         |
| `PR`      | The priority of the process (higher numbers mean lower priority).      |
| `NI`      | Niceness value, which affects process priority (highest:-20,lowest:19) |
| `VIRT`    | Virtual memory size.                                                   |
| `RES`     | Resident memory, the non-swappable physical memory                     |
| `SHR`     | Shared memory size, the memory shared with other processes.            |
| `S`       | Process state                                                          |
| `%CPU`    | CPU % being used by the process.                                       |
| `%MEM`    | RAM % being used by the process.                                       |
| `TIME+`   | Total CPU time consumed by the process (in minutes and seconds).       |
| `COMMAND` | The command name or path that initiated the process.                   |

- Process state:
  - `R`: Running
  - `S`: Sleeping
  - `D`: Uninterruptible sleep (usually I/O)
  - `T`: Stopped
  - `Z`: Zombie

---

### Useful Interactions (While Running)

| key | desc                                       |
| --- | ------------------------------------------ |
| `q` | Quit the top command.                      |
| `h` | Display help for key bindings.             |
| `k` | Kill a process (prompt for PID).           |
| `P` | Sort processes by CPU usage.               |
| `M` | Sort processes by memory usage.            |
| `T` | Sort processes by runtime.                 |
| `r` | Change the priority (renice) of a process. |
| `s` | Change the refresh rate.                   |

---

## `ps`: Display processes information

| Command                             | Desc                                                                         |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `ps`                                | shows processes with the current shell session                               |
| `ps pid`                            | Shows process with a given pid.                                              |
| `ps -ef`                            | Shows all processes in a full-format listing, with parent process ID (PPID). |
| `ps aux`                            | Displays detailed information about all processes.                           |
| `ps -C command`                     | Shows process with a given command name.                                     |
| `ps -u username`                    | Shows processes owned by a specific user.                                    |
| `ps aux \| grep command`            | Filters the output to find specific processes.                               |
| `ps aux --sort=-%mem \| head -n 10` | Find the top memory-consuming process                                        |
| `ps aux --sort=-%cpu \| head -n 10` | Find the top CPU-consuming process                                           |
| `ps -l`                             | Displays a long listing with additional details                              |
| `ps -eH`                            | Display a process tree.                                                      |
| `ps -e --forest`                    | Display a process tree.                                                      |
| `pstree`                            | Display processes in a tree format.                                          |

- Common Commands

```sh
# Return top memory-consuming process
ps aux --sort=-%mem | head -n 10
# Find the top CPU-consuming process
ps aux --sort=-%cpu | head -n 10

# search details of a command
ps aux | grep command

# return the pid related to a command
pidof command
# kill process to release resources
kill -9 pid
```

---

- Common columns

  - `PID`: Process ID.
  - `PPID`: Parent Process ID (which process spawned it).
  - `UID`: User ID of the owner.
  - `TTY`: Terminal associated with the process.
  - `TIME`: CPU time consumed by the process.
  - `CMD`: Command that started the process.

- Process state:
  - `R`: Running.
  - `S`: Sleeping (idle).
  - `D`: Uninterruptible sleep (usually IO operations).
  - `I`: Idle kernel thread
  - `T`: Stopped or traced.
  - `Z`: Zombie (terminated but not cleaned up).

---

## Background and Foreground Processes

- 2 Types of processes:
  - `Foreground processes`:
    - Also known as `interactive processes`
    - these processes **depend on the user** for input.
  - `Background processes`:
    - Also known as `non-interactive` or `automatic processes`
    - these processes run **independently of the user**.

---

### Switch between foreground and background processes

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
| `jobs`      | List jobs.                                  |
| `jobs %num` | List a job wit job number.                  |
| `kill`      | Kill a process by job number or PID.        |

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

---

## Example: Switch Foreground and Background

### Create a long running task.

- `vi /home/rheladmin/rhcsa/long_running_task.sh`

```sh
#!/bin/bash

# File to store logs
LOGFILE="task.log"

echo "Starting long-running task..."
echo "Logs will be saved to $LOGFILE"

# Loop for 5 minutes (10 iterations of 30 seconds)
for i in {1..100}; do
    echo "$(date): Iteration $i - Task is running..." >> $LOGFILE
    sleep 30
done

echo "Task completed!" >> $LOGFILE
echo "Task finished. Check $LOGFILE for details."
```

- Change mode

```sh
# Make the Script Executable
chmod +x /home/rheladmin/rhcsa/long_running_task.sh
```

- Run script in the background

```sh
# Run the Script 3 times in Background
./long_running_task.sh &
# [1] 9904
# [rheladmin@rhelhost rhcsa]$ Starting long-running task...
# Logs will be saved to task.log

./long_running_task.sh &
# [2] 9915
# [rheladmin@rhelhost rhcsa]$ Starting long-running task...
# Logs will be saved to task.log

./long_running_task.sh &
# [3] 9935
# [rheladmin@rhelhost rhcsa]$ Starting long-running task...
# Logs will be saved to task.log

# list background jobs
jobs
# [1]   Running                 ./long_running_task.sh &
# [2]-  Running                 ./long_running_task.sh &
# [3]+  Running                 ./long_running_task.sh &

ps -C long_running_task
# PID TTY          TIME CMD
# 9904 pts/0    00:00:00 long_running_ta
# 9915 pts/0    00:00:00 long_running_ta
# 9935 pts/0    00:00:00 long_running_ta
```

---

### Bring process to Foreground

```sh
# send the last jobs fg
fg
# ./long_running_task.sh

# suspend job last jobs
^Z
# [3]+  Stopped                 ./long_running_task.sh

jobs
# [1]   Running                 ./long_running_task.sh &
# [2]-  Running                 ./long_running_task.sh &
# [3]+  Stopped                 ./long_running_task.sh


# bring the job 2 using -
fg -
# ./long_running_task.sh
^Z
# [2]+  Stopped                 ./long_running_task.sh
jobs
# [1]   Running                 ./long_running_task.sh &
# [2]+  Stopped                 ./long_running_task.sh
# [3]-  Stopped                 ./long_running_task.sh

# bring the job 1 using number
fg 1
# ./long_running_task.sh
^Z
# [1]+  Stopped                 ./long_running_task.sh

jobs
# [1]+  Stopped                 ./long_running_task.sh
# [2]-  Stopped                 ./long_running_task.sh
# [3]   Stopped                 ./long_running_task.sh
```

---

### Send the jobs to Background

```sh
# bring the stopped jobs 1 running in bg
bg 1
# [1]+ ./long_running_task.sh &
jobs
# [1]-  Running                 ./long_running_task.sh &
# [2]+  Stopped                 ./long_running_task.sh
# [3]   Stopped                 ./long_running_task.sh

# bring the stopped jobs 2 running in bg
bg +
# [2]+ ./long_running_task.sh &
jobs
# [1]   Running                 ./long_running_task.sh &
# [2]-  Running                 ./long_running_task.sh &
# [3]+  Stopped                 ./long_running_task.sh

# bring the current stopped job running in bg
bg
# [3]+ ./long_running_task.sh &
jobs
# [1]   Running                 ./long_running_task.sh &
# [2]-  Running                 ./long_running_task.sh &
# [3]+  Running                 ./long_running_task.sh &
```

---

### Terminate the Jobs

```sh
kill %1
jobs
# [1]   Terminated              ./long_running_task.sh
# [2]-  Running                 ./long_running_task.sh &
# [3]+  Running                 ./long_running_task.sh &

ps -C long_running_task
# PID TTY          TIME CMD
# 9915 pts/0    00:00:00 long_running_ta
# 9935 pts/0    00:00:00 long_running_ta

kill -9 9915 9935
jobs
# [2]-  Killed                  ./long_running_task.sh
# [3]+  Killed                  ./long_running_task.sh
```

---

## `lsof`: list files opened by processes

- `lsof`: provides detailed information about files opened by processes.

| CMD                | DESC                                               |
| ------------------ | -------------------------------------------------- |
| `lsof`             | List all open files                                |
| `lsof -u username` | List open files for a specific user                |
| `lsof -p PID`      | List open files for a specific process ID (PID)    |
| `lsof file_name`   | List processes using a specific file               |
| `lsof -i:80`       | Find processes using a specific port               |
| `lsof -i`          | List network connections                           |
| `lsof /dev/sda1`   | List open files on a specific device or filesystem |

- Example

```sh
./long_running_task.sh &

lsof long_running_task.sh
# COMMAND     PID      USER   FD   TYPE DEVICE SIZE/OFF     NODE NAME
# long_runn 10407 rheladmin  255r   REG  253,0      373 19764850 long_running_task.sh
```

---

[TOP](#linux---software-management-process)