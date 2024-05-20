# Oracle DBA2 - Backup and Recovery

[All Notes](../../index.md)

---

- [Overview](./fundamemtal/fundamemtal.md)
- [Recoverability](./recoverability/recoverability.md)

  - [`Fast Recovery Area`](./recoverability/fra/fra.md)
  - [Multiplexing `Control Files`](./recoverability/muli_cf/muli_cf.md)
  - [Multiplexing `Redo Log Files`](./recoverability/muli_redolog/muli_redolog.md)
  - [Enable `Archived Redo Log Files`](./recoverability/archive_redolog/archive_redolog.md)

---

- [Backup](./backup/backup/backup.md)

  - [Backup Strategy](./backup/backup_strategy/backup_strategy.md)

    - [`Cold Backup` and `Hot Backup`](./backup/backup_cold_hot/backup_cold_hot.md)
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

  - [Tuning Backup Performance](./backup/backup_tuning/backup_tuning.md)

---

- [Restore and Recovery](./recovery/recovery/recovery.md)
  - [Recovery Catalog](./recovery/recovery_catalog/recovery_catalog.md)
  - Instance Failure
    - [Instance Recovery](./recovery/recovery_instance/recovery_instance.md)
  - [File Loss](./recovery/recovery_file_loss/recovery_file_loss.md)
    - [Media Recovery: `Complete Recovery` vs `Point-in-Time Recovery`](./recovery/recovery_media/recovery_media.md)
    - [`Complete Recovery`](./recovery/recovery_complete/recovery_complete.md)
      - [`NOARCHIVELOG` Mode](./recovery/recovery_complete_noarchivelog/recovery_complete_noarchivelog.md)
      - [`ARCHIVELOG` Mode - CDB](./recovery/recovery_complete_cdb/recovery_complete_cdb.md)
      - [`ARCHIVELOG` Mode - PDB](./recovery/recovery_complete_pdb/recovery_complete_pdb.md)
      - [Using Image Copy](./recovery/recovery_complete_copy/recovery_complete_copy.md)

---

- [`Recovery Manager (RMAN)`](./rman/rman/rman.md)

  - [Connect](./rman/rman_connect/rman_connect.md)
  - [Configuration](./rman/rman_conf/rman_conf.md)

  - [Catelog](./rman/rman_catalog/rman_catalog.md)
  - [Reporting](./rman/rman_reporting/rman_reporting.md)
  - [Backups Commands](./rman/rman_backup_command/rman_backup_command.md)
  - [Stored Scripts](./rman/rman_script/rman_script.md)

  - [Diagnosis](./rman/rman_diagnosis/rman_diagnosis.md)
    - [`Automatic Diagnostic Repository (ADR)`](./rman/rman_diagnosis_adr/rman_diagnosis_adr.md)
    - [Data Failure & `Data Recovery Advisor`](./rman/rman_diagnosis_dra/rman_diagnosis_dra.md)

---

DBA1

- [oraenv](./oraenv/oraenv.md)
