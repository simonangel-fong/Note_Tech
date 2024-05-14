# Backup - Backing up Recovery Data

[Back](../../index.md)

- [Backup - Backing up Recovery Data](#backup---backing-up-recovery-data)
  - [Backing Up Recovery Data](#backing-up-recovery-data)

---

## Backing Up Recovery Data

- There are two ways to back up recovery data:
  - `BACKUP RECOVERY AREA`
  - `BACKUP RECOVERY FILES`

---

- `BACKUP RECOVERY AREA` command:

  - backs up all files that are found in the **current** and any **previous** `fast recovery areas`.

- `BACKUP RECOVERY FILES` command:

  - backs up all recovery files, **even if they are not in the FRA**.
  - can back up any copies of control files or data files that are **not in the fast recovery area**.

- **Characteristics:**

  - By default, `backup optimization` is **in effect** for these two commands, even if you have **disabled** it by using the `CONFIGURE` command. 自动适用优化
    - the only recovery files that this command backs up are those that are **not already backed up**. 默认只备份未备份的.
  - You can force all files to be backed up by using the `FORCE` option.强制备份所有.
  - cannot specify `DEVICE TYPE DISK` for either of these commands.
    - To back up to disk, you **must specify a directory** or an `Automatic Storage Management (ASM)` disk group in the `TO DESTINATION` subclause.
  - RMAN backs up only database files: `data files`, `control files`, `SPFILES`, `archive log files`, and **backups of these files**.
    - Placing an operating system file in the fast recovery area does **not cause it to be included with** a backup of the recovery area.

- Syntax:

```sql
-- Back up only the files in the fast recovery area:
BACKUP RECOVERY AREA;

-- Back up all recovery files:
BACKUP RECOVERY FILES;
```

---

[TOP](#backup---backing-up-recovery-data)
