# Recovery - `PITR` in PDB

[Back](../../index.md)

- [Recovery - `PITR` in PDB](#recovery---pitr-in-pdb)
  - [PITR of PDBs](#pitr-of-pdbs)
  - [TSPITR in a PDB](#tspitr-in-a-pdb)

---

## PITR of PDBs

- `PDB PITR`;

  - Recover a PDB to a point in time

- **not affect** all parts of the CDB 独立性

  - the whole `CDB` is **still opened** and, therefore, **all other** `PDBs` are **opened**.不影响其他
  - put the tablespace back **online** after pdb pitr. 所以只需要重新加载在线即可.

- the `old backup` of the PDB **After** recovery 旧备份

  - **remains valid** and **can be used** if a m`edia failure` occurs.旧备份能使用

- If you do not use a `fast recovery area`,

  - you must **specify the temporary location** of the `auxiliary set files` by using the `AUXILIARY DESTINATION` clause

- `PDB incarnation`

  - a **subincarnation** of the `CDB`.
  - e.g., if the CDB is incarnation 5, and a PDB is incarnation 3, then the fully specified incarnation number of the PDB is **(5, 3)**.
  - The **initial** incarnation of a PDB is `0`.
  - View:
    - `V$PDB_INCARNATION`

- `RESETLOGS` option

  - used to **open** the pdb after pdb pitr
  - Conceptually, a `PDB` `resetlogs` is **similar to** a database `resetlogs`.概念上类似
    - The `PDB` `RESETLOGS` does **not perform** a `RESETLOGS` for the `CDB`.不同于 cdb
  - a **new incarnation** of the PDB is created.
  - A `PDB` **record** in the `control file` is **updated**. 在控制文件中更新
  - Each `redo log record` carries `PDB ID` in the **redo header**.
    - This is how recovery knows which `redo` applies to which `PDB`.
    - `Redo logs` are **shared** by **all PDBs**
    - `redo` from each `PDB` is written to **a single set** of `redo logs`.

- **Example:**

```sql
SQL "ALTER PLUGGABLE DATABASE pdbl CLOSE";
RUN {
  SET UNTIL SCN = 1851648;
  RESTORE pluggable DATABASE pdbl;
  RECOVER pluggable DATABASE pdbl
  -- specify the temporary location of the auxiliary set files
  AUXILIARY DESTINATION='/u0l/app/oracle/oradata’';
  SQL "ALTER PLUGGABLE DATABASE pdbl OPEN RESETLOGS";
}
```

---

## TSPITR in a PDB

- `TSPITR` can be used to **recover a tablespace** to an earlier point in time.

  - specifying the full tablespace name including the PDB name.

- Example:

```sql
RECOVER TABLESPACE pdbl:test_tbs
UNTIL SCN 832972
AUXILIARY DESTINATION '/tmp/CDBl/reco';

SQL "ALTER TABLESPACE pdbl:test_tbs ONLINE";
```

---

[TOP](#recovery---pitr-in-pdb)
