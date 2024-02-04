# DBA - Memory Architecture

[Back](../../index.md)

- [DBA - Memory Architecture](#dba---memory-architecture)
  - [Basic Memory Structures](#basic-memory-structures)
    - [Memory Management](#memory-management)

---

## Basic Memory Structures

- Basic Memory Structures include:

  - `System global area (SGA)` / `SGA components`:

    - a group of **shared memory** structures that contain **data** and **control information** for <u>one Oracle Database instance</u>.
    - All server and background processes share the SGA.

  - `Program global area (PGA)`

    - a **nonshared memory** region that contains **data** and **control information** exclusively for use by <u>an Oracle process</u>.
    - Oracle Database **creates** the PGA **when an Oracle process starts**.
    - **One** `PGA` exists for **each** `server process` and `background process`.
    - `total instance PGA` / `instance PGA`:
      - The collection of individual PGAs.
      - Database initialization parameters set the size of the instance PGA, not individual PGAs. 即参数设置只针对实例 PGA, 不针对个体 PGA.

  - `User global area (UGA)`

    - the memory associated with a user session.

  - `Software code areas`
    - portions of memory **used to store code** that is being run or can be run.
    - a more exclusive or protected location, that is typically at a different location from user programs.

| Memory Structures           | Associated with | Processes                         |
| --------------------------- | --------------- | --------------------------------- |
| `System global area (SGA)`  | instance        | shared by server + bg processes   |
| `Program global area (PGA)` | processes       | exclusively for server/bg Process |
| `User global area (UGA)`    | user session    |                                   |
| `Software code areas`       | code            |                                   |

---

### Memory Management

- `Memory management`

  - maintain **optimal sizes** for the Oracle instance memory structures as demands on the database change.

- memory-related `initialization parameters`

  - used to manages memory

- Options:

  - **Automatic** memory management

    - default option of `Database Configuration Assistant (DBCA)`
    - DBA **specify** the `target size` for the **database instance memory**.
    - The instance **automatically tunes** to the `target memory size`, redistributing memory as needed between the SGA and the instance PGA.
    - DBA 设置实例内存大小 + 实例自动分配

  - **Automatic shared** memory management

    - partially automated.
    - DBA set a `target size` for the `SGA`
    - have the option of setting an `aggregate target size` for the `PGA` or managing PGA work areas individually.
    - DBA 设置 SGA 大小+PGA 大小

  - **Manual** memory management
    - DBA set many `initialization parameters` to manage components of the `SGA` and instance `PGA` **individually**.

| Options          | Description                      |
| ---------------- | -------------------------------- |
| Automatic        | `target size` of instance memory |
| Automatic shared | `target size` of SGA             |
| Manual           | `i parameters` of SGA + PGS      |

---

[TOP](#dba---memory-architecture)
