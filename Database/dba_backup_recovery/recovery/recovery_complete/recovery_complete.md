# Recovery - `Complete Recovery`

[Back](../../index.md)

- [Recovery - `Complete Recovery`](#recovery---complete-recovery)
  - [Restore Command](#restore-command)
  - [Restore Points](#restore-points)

---

## Restore Command

- Commands to check the validity of the backups

| RMAN Command              | Action                                                                   |
| ------------------------- | ------------------------------------------------------------------------ |
| `RESTORE PREVIEW`         | reports the backups and archived redo log files uesd to restore          |
| `RESTORE VALIDATE`        | determines and validate backup, copies, and archived redo log to restore |
| `RECOVER VALIDATE HEADER` | Reports and validates the backups to restore for the recovery            |

- `RESTORE PREVIEW`:

  - Reports on the `backups` and `archived redo log files` that RMAN **can use to restore and recover** the database to the **specified time**. 列出需要的文件
  - RMAN queries the **metadata**, but does **not actually read** the backup files.不读取文件
  - The **output** from this command is in the **same format** as the LIST BACKUP command output.

- `RESTORE VALIDATE`:

  - Specifies that RMAN should decide which `backup sets`, `data file copies`, and `archived redo log files` **need to be restored** and then **validate** them.
  - No files are restored.
  - For files on both disk and tape, RMAN **reads all blocks** in the `backup piece` or `image copy`. 读取文件
  - RMAN also validates **off-site** backups.

- `RECOVER VALIDATE HEADER`:
  - **Reports** on and **validates** the backups that RMAN can use to restore files needed for recovery.
  - RMAN performs the **same operations** as when you specify the `RESTORE PREVIEW` command.
    - Additional, RMAN **validates** the backup file **headers** to determine whether the files **on disk** or in the **media management catalog** correspond to what is in the metadata in the RMAN repository. 验证文件头

---

## Restore Points

- `restore point`

  - provides a name to a point in time
  - a **user-defined name** associated with an `SCN` of the database **corresponding to the time** of the creation of the restore point.
  - useful for future reference, when performing `point-in-time recovery` or `flashback` operations.

- There are **two types** of `restore points`:

  - `Guaranteed restore point`:
    - Enforces the **retention of flashback logs** required for `Flashback` Database **back to any point in time after** the creation of the earliest guaranteed restore point.
    - does **not age out** of the `control file`
    - must be explicitly dropped.
  - **Normal restore point**:
    - A label for an `SCN` or **time**.
    - exist in a **circular list**
    - can be **overwritten** in the `control file`.

- Example:

```sql
-- creates a restore point that represents the present point in time.
CREATE RESTORE POINT before_mods;

-- creates a restore point representing a past SCN, 100
CREATE RESTORE POINT end_ql AS OF SCN 100;
```

- Normally, `restore points` are maintained in the database **for at least as long as specified by** the `CONTROL_FILE_RECORD_KEEP_TIME` initialization parameter.默认保留时长=cf 参数
- `PRESERVE` option:

  - causes the restore point to be **saved until** you **explicitly delete** it.保留恢复点直到显式删除

- Views:
  - `V$RESTORE_POINT`: display estore points' name, SCN, time stamp, and other information.

---
