# RMAN - Reporting

[Back](../../index.md)

- [RMAN - Reporting](#rman---reporting)
  - [Reporting on Backups](#reporting-on-backups)

---

## Reporting on Backups

RMAN commands:

- `LIST`: Displays information about backup sets, proxy copies, and image copies recorded in the repository
- `REPORT`: Produces a **detailed analysis** of the repository
- `REPORT NEED BACKUP`: Lists all **data files that require a backup**
  - assumes that the **most recent backup** would be used in the event of a restore.
- `REPORT OBSOLETE`: Identifies files that are **no** longer needed to **satisfy backup retention policies**
  - By default, reports which files are obsolete under the **currently configured retention policy**. 默认针对当前政策
  - can generate reports of files that are obsolete according to **different retention policies** by using `REDUNDANCY` or `RECOVERY WINDOW` **retention policy** options.

`Enterprise Manager Cloud Control:`

- Graphical, customizable interface

---

---
