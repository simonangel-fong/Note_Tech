# DBA2 - Recoverability

[Back](../index.md)

- [DBA2 - Recoverability](#dba2---recoverability)
  - [Recoverability](#recoverability)

---

## Recoverability

Configure your database for maximum recoverability by:

- Scheduling **regular backups**
- **Multiplexing** `control files`
- **Multiplexing** `redo log groups`
- Retaining **archived** copies of `redo logs`

---

To provide the best protection for your data, you must:

- **Schedule regular backups**:
  - Most media failures require that you **restore** the lost or damaged file **from backup**.
- **Multiplex `control files`**:
  - All `control files` associated with a database are identical.
  - Recovering from the loss of a **single** `control file` is not difficult; recovering from the loss of all `control files` is much more **challenging**.
  - Guard against losing all control files by **having at least two copies**.
- **Multiplex `redo log groups`**:
  - To recover from instance or media failure,` redo log information` is used to roll data files forward to the last committed transaction.
  - If your redo log groups rely on a **single** redo log file, the loss of that file means that data is likely to be lost.
  - Ensure that there are **at least two copies** of each `redo log group`; if possible, each copy should be under **different disk controllers**.
- **Retain` archived copies of redo logs`**:
  - If a file is lost and restored from backup, the instance must apply redo information to bring that file up to the latest SCN contained in the control file.
  - With the **default** setting, the database can **overwrite** `redo information` after it has been written to the `data files`.
  - Your database can be configured to **retain** `redo information` in archived copies of the `redo logs`. This is known as placing the database in `ARCHIVELOG` mode. You can perform configuration tasks in `Enterprise Manager Cloud Control` or by using the SQL command line.

---

[TOP](#dba2---recoverability)
