# Linux - System: Shutdown

[Back](../../index.md)

- [Linux - System: Shutdown](#linux---system-shutdown)
  - [Power Off/Shutdown the system](#power-offshutdown-the-system)
  - [Reboot the system](#reboot-the-system)
  - [Halt](#halt)
  - [Suspend (Sleep) and Hibernate](#suspend-sleep-and-hibernate)

---

## Power Off/Shutdown the system

- **Shutdown/Power Off**

  - All running processes are terminated.
  - Filesystems are unmounted, and disks are safely synced.
  - The machine powers down.

- **shutdown delay**

  - give users time to save their work and log off the system.

- **Commands**

| CMD                  | DESC                             |
| -------------------- | -------------------------------- |
| `poweroff`           | Turns off the system             |
| `shutdown now`       | Turns off the system immeidately |
| `shutdown +5`        | Shutdown in 5 minutes            |
| `systemctl poweroff` | Turns off the system             |

- `poweroff` is the symbolic link to `systectl` equivalents

---

## Reboot the system

- Restarts the system **by powering it off** and **back on**.
- Filesystems are synced and **unmounted**.
- **Reinitializes** the entire boot process.

- Important:

  - restarting is considered **downtime** on a server and should be avoided if possible.
  - Try to use `systemctl restart {service-name}` to **restart services** rather than reboot the whole system.

- **Commands**

| CMD                 | DESC                           |
| ------------------- | ------------------------------ |
| `reboot`            | Reboots the system immediately |
| `shutdown -r now`   | Reboots the system immediately |
| `shutdown -r 22:00` | Reboots the system at 10pm     |
| `systemctl reboot`  | Reboots the system immediately |

- `reboot` is the symbolic link to `systectl` equivalents

---

## Halt

- **Halt**
  - **Stops** the operating system **without cutting power** to the machine.
  - **Halts** all **CPU** activity.
  - **Filesystems** are synced and **unmounted**.
  - The system **remains powered on** (useful for **maintenance** tasks).

| CMD                            | DESC                                                            |
| ------------------------------ | --------------------------------------------------------------- |
| `halt`                         | Halt the system                                                 |
| `shutdown --halt 22:00`        | Halt the system at 10pm                                         |
| `shutdown --halt +5`           | Halt the system after a five-minute delay                       |
| `shutdown --halt +5 "message"` | Halt the system after a delay and append a message to all users |
| `shutdown -c`                  | Cancel a timed shutdown                                         |
| `systemctl halt`               | Halt the system                                                 |

---

## Suspend (Sleep) and Hibernate

- **Suspend (Sleep)**

  - Puts the system into a **low-power state** while keeping the **session** in **memory (RAM)**.
  - Current state is saved in **RAM (volatile memory)**.
  - Power to most hardware components (like the CPU) is **reduced** or **turned off**.
  - **Quick to resume** as RAM remains powered.
  - **Use Case:**

    - Temporary breaks; resumes quickly without full system restart.

---

- **Hibernate(冬眠) the system:**

  - **Saves** the system state to the **disk** and powers off completely.
  - System state is saved to a `swap partition` or file.
  - Power is **completely cut off**.
  - On reboot, the system **restores** the session **from disk**.
  - **Use Case**:
    - Longer breaks; resumes from where you left off but takes longer than suspend.

---

- **Commands**

| CMD                      | DESC                                    |
| ------------------------ | --------------------------------------- |
| `systemctl suspend`      | Suspend the system                      |
| `systemctl hibernate`    | Hibernate the system                    |
| `systemctl hybrid-sleep` | Both suspends and hibernates the system |

---

[TOP](#linux---system-shutdown)
