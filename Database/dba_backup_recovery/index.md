# Oracle DBA2 - Backup and Recovery

[All Notes](../../index.md)

---

- [Overview](./fundamemtal/fundamemtal.md)
- [Recoverability](./recoverability/recoverability.md)

  - [`Fast Recovery Area`](./recoverability/fra/fra.md)
  - [Multiplexing `Control Files`](./recoverability/muli_cf/muli_cf.md)
  - [Multiplexing `Redo Log Files`](./recoverability/muli_redolog/muli_redolog.md)
  - [Enable `Archived Redo Log Files`](./recoverability/archive_redolog/archive_redolog.md)

- [Backup](./backup/backup/backup.md)

  - [Backup Strategy](./backup/backup_strategy/backup_strategy.md)

    - [`Whole Database Backup` and `Partial Database Backup`](./backup/backup_whole_partial/backup_whole_partial.md)
    - [`Full Backup` and `Incremental Backup`](./backup/backup_full_incremental/backup_full_incremental.md)
      - [Block Change Tracking](./backup/backup_bct/backup_bct.md)
    - Backup Additional Database Files
      - [Control File](./backup/backup_cf/backup_cf.md)
      - [Archive Log Files](./backup/backup_archivelog/backup_archivelog.md)

  - [Backup Channels and Devices](./backup/backup_device/backup_device.md)
  - [Retention Policy](./backup/backup_retention_policy/backup_retention_policy.md)

    - [Archival Backups](./backup/backup_archival/backup_archival.md)

  - Backup File

    - [`Backup Sets` and `Image Copies`](./backup/backup_backupset_imagecopy/backup_backupset_imagecopy.md)
    - [Backups Compression](./backup/backup_compress/backup_compress.md)
    - [Multisection for Very Large Files](./backup/backup_multisection/backup_multisection.md)
    - [Duplexing Backup Sets](./backup/backup_duplex/backup_duplex.md)
    - [Proxy Copies](./backup/backup_proxy_copy/backup_proxy_copy.md)

  - Backing Up Backup File
    - [Backing Up `Backupset` and `Image Copy`](./backup/backup_backup/backup_backup.md)
    - [Backing up Recovery Data](./backup/backup_recovery_data/backup_recovery_data.md)

---

- [`Recovery Manager (RMAN)`](./rman/rman/rman.md)

  - [Connect](./rman/rman_connect/rman_connect.md)
  - [Configuration](./rman/rman_conf/rman_conf.md)

  - [Catelog](./rman/rman_catalog/rman_catalog.md)
  - [Reporting](./rman/rman_reporting/rman_reporting.md)
  - [Backups Commands](./rman/rman_backup_command/rman_backup_command.md)

---

Create multisection backups of very large files
Create proxy copies

Create duplexed backup sets

Create archival backups

DBA1

- [oraenv](./oraenv/oraenv.md)
