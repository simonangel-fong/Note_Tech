# Oracle DBA - Backup and Recovery

[All Notes](../../index.md)

---

- [Overview](./fundamemtal/fundamemtal.md)
- [Recoverability](./recoverability/recoverability.md)
  - [`Fast Recovery Area`](./recoverability/fra.md)
  - [Multiplexing `Control Files`](./recoverability/muli_cf.md)
  - [Multiplexing `Redo Log Files`](./recoverability/muli_redolog.md)
  - [Creating `Archived Redo Log Files`](./recoverability/archive_redolog.md)

Practice Overview

- Verifying that the Control File is Multiplexed
- Configuring the Size of the Fast Recovery Area
- Verifying that the Redo Log File Is Multiplexed
- Configuring ARCHIVELOG Mode



How to configure your database for recovery:
- Ensure redundancy of control files. If a control file is damaged or lost, recovery is
easier if you have another copy.
- Review the fast recovery area configuration.
- Ensure that there are at least two redo log members in each group. If a redo log
member is damaged or lost, recovery is easier when you have an additional member in
the group.
- Place your database in ARCHIVELOG mode. In all cases, you will be able to recover
the database either completely or incompletely depending on which database files
have been damaged or lost.
- Configure redundant archive log destinations. In cases where you lost archive log files
and you need them to recover the database, you will be able to perform an incomplete
recovery, unless you have a duplicate version of the archive log in another destination.