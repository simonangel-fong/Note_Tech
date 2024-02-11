# DBA - Process: Server Process

[Back](../../index.md)

- [DBA - Process: Server Process](#dba---process-server-process)
  - [Server Processes](#server-processes)
    - [Dedicated Server Processes](#dedicated-server-processes)
    - [Shared Server Processes](#shared-server-processes)
  - [How Oracle Database Creates Server Processes](#how-oracle-database-creates-server-processes)

---

## Server Processes

- `Server processes`
  - process created by Oracle Database to to **handle the requests of `client processes`** connected to the instance.
- A `client process` **always communicates** with a database **through** a separate `server process`.

- `Server processes` created on behalf of a database application can perform one or more of the following tasks:
  - **Parse and run SQL statements** issued through the application, including creating and executing the **query plan**
  - **Execute** `PL/SQL` code
  - **Read** `data blocks` from `data files` into the database `buffer cache` (the DBW background process has the task of writing modified blocks back to disk)
  - **Return results** in such a way that the application can process the information

---

### Dedicated Server Processes

- In **dedicated server connections**, the client connection is associated with **one and only one** `server process`.一对一专用
  - `server process` is **dedicated to** its `client process` for the duration of the `session`.
  - Each `client process` communicates directly with its `server process`.
- The `server process` **stores** process-specific information and the `UGA` in its `PGA`.内存位置: PGA

---

### Shared Server Processes

- In **shared server connections**, client applications connect over a network to a `dispatcher process`, **not a server process**.

  - e.g., 20 `client processes` can connect to a single `dispatcher process`.

- `dispatcher process`:

  - **receives requests** from connected clients and puts them into a **request queue** in the `large pool`.

- Request processing: 请求队->shared 服务器进程->回应对->传输

  - The first available `shared server process` takes the request from the queue and **processes** it.
  - Afterward, the shared server places the **result** into the **dispatcher response queue**.
  - The dispatcher process monitors this queue and **transmits** the result to the client.

- Memory:
  - a `shared server process` has its **own** `PGA`.
  - The `UGA` for a session is in the `SGA` so that any shared server can access session data.

---

| Mode      | Process               | Process Location | Session/UGA Location |
| --------- | --------------------- | ---------------- | -------------------- |
| Dedicated | server process        | PGA              | PGA                  |
| Shared    | shared server process | PGA              | SGA                  |

---

## How Oracle Database Creates Server Processes

- The database creates server processes in various ways, **depending on the connection methods**.

  - `Bequeath`:
    - `SQL*Plus`, an `OCI` client, or another client application **directly spawns** the server process.

  - `Oracle Net listener`
    - The client application connects to the database **through a listener**. 通过监听器

  - `Dedicated broker`
    - database process that creates foreground processes. 
    - the broker **resides within the database instance**. 
    - When using a `dedicated broker`, the client connects to the listener, which then hands off the connection to the dedicated broker.

- When a connection does not use bequeath, the database creates the server process as follows:
  - 1. The `client application` **requests a new connection** from the listener or broker.
  - 2. The listener or broker **initiates the creation** of a new process or thread.
  - 3. The `operating system` **creates** the new process or thread.
  - 4. `Oracle Database` **initializes** various components and notifications.
  - 5. The database **hands over** the connection and connection-specific code.


---

[TOP](#dba---process-server-process)
