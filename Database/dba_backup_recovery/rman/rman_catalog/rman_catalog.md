# RMAN - Catelog

[Back](../../index.md)

- [RMAN - Catelog](#rman---catelog)
  - [Cataloging Additional Backup Files](#cataloging-additional-backup-files)

---

## Cataloging Additional Backup Files

- Using the `CATALOG` command:

  - To catalog existing `backup files` that are **no longer listed** in the `control file`
  - To catalog files that were **never included** in the `control file` or `recovery catalog`
  - To add the following file types to the recovery catalog:
    - `CONTROLFILECOPY`: Control file copies
    - `DATAFILECOPY`: Data file copies
    - `BACKUPPIECE`: Backup pieces
    - `ARCHIVELOG`: Archived redo log files

- The `CATALOG` command can be used **without being connected to a recovery catalog**.

---

- Cataloging Additional Backup Files:
  - If you have **additional** `control file` copies, `data file` copies, `backup pieces`, or `archived redo log files` on disk, you can catalog them in the recovery catalog by using the `CATALOG` command.
  - If backups have **aged out** of the `control file`, you can catalog them so that RMAN **can use them during a restore operation**.
  - You can also catalog split datafile copies from a mirror split.

---

- Example: to catalog all files in the currently enabled `fast recovery area`

```sql
CATALOG RECOVERY AREA NOPROMPT;
```

---

- `START WITH` option:

  - to catalog all files found in the specified directory tree.
  - Provide a **prefix** that indicates the **directory** and possibly a **file prefix** to look for.
    - You cannot use wildcards;
    - this is only a prefix.

- ## Example:

```sql
CATALOG ARCHIVELOG '/diskl/arch_logs/archivel_731.log', '/diskl/arch_logs/archivel_732.log';
-- catalogs all types of backup files that are found in the `/tmp/arch` logs directory.
CATALOG START WITH '/tmp/arch_logs/';

--  catalog only those files in the `/tmp` directory whose file names start with the `bset` string.
CATALOG START WITH '/tmp/bset';
```

---
