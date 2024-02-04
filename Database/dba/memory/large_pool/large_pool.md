# DBA - SGA: Large Pool

[Back](../../index.md)

- [DBA - SGA: Large Pool](#dba---sga-large-pool)
  - [Large Pool](#large-pool)

---

## Large Pool

- `large pool`

  - an **optional** memory area intended for memory allocations that are **larger than** is appropriate for the `shared pool`.

- **Purpose**:
  - `UGA` for the shared server and the Oracle `XA` interface (used where transactions interact with multiple databases)
  - Message buffers used in parallel execution
  - Buffers for `Recovery Manager (RMAN)` I/O slaves
  - Buffers for deferred inserts (inserts with the `MEMOPTIMIZE_WRITE` hint)

---

[TOP](#dba---sga-large-pool)
