# DBA - Memory Structure: User Global Area

[Back](../../index.md)

- [DBA - Memory Structure: User Global Area](#dba---memory-structure-user-global-area)
  - [User Global Area](#user-global-area)

---

## User Global Area

- `User Global Area`

  - session memory for **session variables**
    - e.g.: logon information, and other information required by a database session.
    - Essentially, the UGA stores the `session state`.

- The UGA must be **available** to a database session **for the life of the session**.

- related to `SGA`/`PGA`
  - When using a **dedicated server connection**:
    - the `UGA` is stored in the `PGA`
    - 在 tnsname.ora 的 SERVER 参数, 默认是 DEDICATED, 此时专有的进程会分配给 user session. 此时 UGA 在 PGA 中.
  - When using a **shared server connection**:
    - the `UGA` is stored in the `SGA`, because the `UGA` cannot be stored in the `PGA` that is specific to a single process.
    - 当连接是分享时,因为 PGA 是进程独享, 不能保证完整的 session 生命周期,所以只能在 SGA

---

[TOP](#dba---memory-structure-user-global-area)
