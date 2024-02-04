# DBA - SGA: Fixed SGA

[Back](../../index.md)

- [DBA - SGA: Fixed SGA](#dba---sga-fixed-sga)
  - [Fixed SGA](#fixed-sga)

---

## Fixed SGA

- `fixed SGA`

  - an **internal housekeeping area**.
  - contains:
    - **General information** about the **state** of the database and the instance, which the background processes need to access
    - **Information communicated between processes**, such as information about locks

- The size of the fixed SGA is set by Oracle Database and **cannot be altered manually**. The fixed SGA size can change from release to release.
