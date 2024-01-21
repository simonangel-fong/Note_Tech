# DBA - Multitenant: PDB

[Back](#dba---multitenant-cdb)

- [DBA - Multitenant: PDB](#dba---multitenant-pdb)
  - [PDB](#pdb)
  - [Open Modes](#open-modes)
  - [Open and Close PDBs](#open-and-close-pdbs)

---

## PDB

---

## Open Modes

- When you open a `PDB`, the database server **opens** the `data files` for that PDB.

  - Starting up a `PDB` and opening a `PDB` mean the same thing. 等价

- `PDB Open Modes`
  - levels of a PDB being opened.
  - Similar to a CDB
    - `READ WRITE` (the PDB is fully started/opened)
    - `READ ONLY`,
    - `MIGRATE`,
    - and `MOUNTED` (the PDB is shut down/closed).

---

## Open and Close PDBs

- Using `ALTER PLUGGABLE DATABASE` command to change from any open mode to another

  - from either the **root container** or within the **PDB itself**.

- `STARTUP` and `SHUTDOWN` commands

  - the `PDB` must first be in `MOUNTED` mode.

- Required privileges:

  - `AS SYSBACKUP`, `AS SYSDBA`, `AS SYSDG`, or `AS SYSOPER`.

- Example:

```sql
/* PDB1 is started up (opened). Its open mode is changed from MOUNT to READ WRITE. */
ALTER PLUGGABLE DATABASE PDB1 OPEN;

# PDB1 is shut down (closed). Its open mode is changed to MOUNT
ALTER PLUGGABLE DATABASE PDB1 CLOSE;

```

---

[TOP](#dba---multitenant-pdb)
