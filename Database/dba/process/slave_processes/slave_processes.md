# DBA - Process: Slave Processes

[Back](../../index.md)

- [DBA - Process: Slave Processes](#dba---process-slave-processes)
  - [Slave Processes](#slave-processes)
    - [I/O Slave Processes(Innn)](#io-slave-processesinnn)
    - [Parallel Execution (PX) Server Processes](#parallel-execution-px-server-processes)

---

## Slave Processes

- `Slave processes`
  - the background processes that **perform work** on behalf of other processes.

---

### I/O Slave Processes(Innn)

- `I/O slave processes (Innn)`

  - **simulate asynchronous I/O** for systems and devices that do not support it.

- `asynchronous I/O`
  - there is **no timing requirement** for transmission, enabling other processes to start before the transmission has finished.

---

### Parallel Execution (PX) Server Processes

- `parallel execution`

  - **multiple** processes work together **simultaneously** to **run a single SQL statement**.
  - reduces response time for data-intensive operations on large databases such as data warehouses.

- `serial execution`

  - a **single** server process performs **all** necessary processing for the sequential execution of a SQL statement.

---

[TOP](#dba---process-slave-processes)
