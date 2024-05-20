# Recovery - Complete Recovery: `NOARCHIVELOG` Mode

[Back](../../index.md)

- [Recovery - Complete Recovery: `NOARCHIVELOG` Mode](#recovery---complete-recovery-noarchivelog-mode)
  - [`NOARCHIVELOG` Mode](#noarchivelog-mode)
  - [Using Incremental Backups with `NOREDO` option](#using-incremental-backups-with-noredo-option)

---

## `NOARCHIVELOG` Mode

- **Scenario to restore datafile**

  - `NOARCHIVELOG` mode + any data file is lost

- **Solution:**

  - requires **complete restoration** of the database, including control files and all data files.
  - recovery is possible **only** up to the **time of the last backup**.
  - users must reenter all changes made since that backup.

- **Steps:**

  1. **Shut down** the instance if it is not already down.
  2. **Restore** the **entire** database, including all `data` and `control files` from a backup.
  3. **Start** the instance and **open** the database (CDB and all PDBs).
  4. Inform users that they **must reenter** all changes that were made **since the last backup**.

- In `NoArchiveLog` mode, when the database is recovery to a specific time, all CDB and PDBs are bought back to this point of time. 整体恢复, 不存在个别 pdb 能恢复到不同的时间点.

- **Example:**

```sql
-- connect
rman target /

-- Restore Control Files
STARTUP FORCE NOMOUNT;
RESTORE CONTROLFILE;

-- restore and recover database
ALTER DATABASE MOUNT;
RESTORE DATABASE;
RECOVER DATABASE;

-- Start the Instance and Open the Database (CDB and All PDBs):
SQL 'ALTER PLUGGABLE DATABASE ALL OPEN';
```

---

## Using Incremental Backups with `NOREDO` option

- **Scenario**

  - `NOARCHIVELOG` mode + any `data file` is lost + `incremental backup strategy`

- **Solution:**

  - RMAN uses `level 0` and `level 1` backups to restore and recover the database.
  - RMAN restores the **most** recent `level 0 backup` and then RMAN recovery applies the incremental backups.

- **Prerequisites:**

  - The `incremental backups` **must be consistent** backups.

- **`NOREDO` option:**

  - If not specifying the `NOREDO` option, RMAN searches for the `online redo log files` after applying the incremental backups. 不使用`NOREDO`时, 自动搜索在线档
  - If the `online redo log files` are **not available**, RMAN issues an **error** message.

- **`RECOVER DATABASE` command **without** the `NOREDO` option:**

  - when the `current online redo log files` contain **all changes since the last `incremental backup`**. 当前 redo 包含自上次递增备份所有改变
  - the changes will be applied.

- **`RECOVER DATABASE` command + `NOREDO` option:**

  - When the `online redo log files` are **lost** or if the `redo` **cannot be applied** to the `incremental backups`. 当前 redo 不适用

- **Example:**

```sql
-- restore cf
STARTUP FORCE NOMOUNT;
RESTORE CONTROLFILE;

-- resotre df
ALTER DATABASE MOUNT;
RESTORE DATABASE;

-- recover noredo
RECOVER DATABASE NOREDO;
ALTER DATABASE OPEN RESETLOGS;
```

---

[TOP](#recovery---complete-recovery-noarchivelog-mode)
