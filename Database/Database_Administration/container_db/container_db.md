# DBA - Container Database

[Back](../index.md)

- [DBA - Container Database](#dba---container-database)
    - [List all container](#list-all-container)
    - [Create CBD](#create-cbd)
  - [Default Tablespaces in the Multitenant Architecture](#default-tablespaces-in-the-multitenant-architecture)

---


### List all container

- View:

  - `V$CONTAINERS`

- lists all containers in the CDB:
  - `SELECT NAME, CON_ID, DBID, CON_UID, GUID FROM V$CONTAINERS ORDER BY CON_ID;`

---

### Create CBD

- Syntax:

```sql

```

---

## Default Tablespaces in the Multitenant Architecture

| Tablespace | Root                                         | PDB                         |
| ---------- | -------------------------------------------- | --------------------------- |
| `SYSTEM`   | Oracle-supplied metadata;                    | user metadata.              |
| `SYSAUX`   | exists                                       | exists in each              |
| `TEMP`     | a single default temporary tbsp for all PDB. | Can create tbsp for pdb     |
| `UNDO`     | one active                                   | local in each (recommended) |
| `USERS`    | one                                          | Each                        |

---

[TOP](#dba---container-database)
