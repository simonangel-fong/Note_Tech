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
    - [Virtual Private Catalog](./recovery/virtual_private_catalog/virtual_private_catalog.md)
  - [Instance Failure & `Instance Recovery`](./recovery/recovery_instance/recovery_instance.md)
  - [File Loss](./recovery/recovery_file_loss/recovery_file_loss.md)
    - [Media Recovery: `Complete Recovery` vs `Point-in-Time Recovery`](./recovery/recovery_media/recovery_media.md)
    - [`Complete Recovery`](./recovery/recovery_complete/recovery_complete.md)
      - [`NOARCHIVELOG` Mode](./recovery/recovery_complete_noarchivelog/recovery_complete_noarchivelog.md)
      - [`ARCHIVELOG` Mode - CDB](./recovery/recovery_complete_cdb/recovery_complete_cdb.md)
      - [`ARCHIVELOG` Mode - PDB](./recovery/recovery_complete_pdb/recovery_complete_pdb.md)
      - [Using Image Copy](./recovery/recovery_complete_copy/recovery_complete_copy.md)
    - [`Point-in-Time Recovery`](./recovery/recovery_pitr/recovery_pitr.md)
      - [`Incomplete Recovery`(`DBPITR`)](./recovery/recovery_dbpitr/recovery_dbpitr.md)
      - [`PITR` in PDB](./recovery/recovery_pdbpitr/recovery_pdbpitr.md)
      - [`Tablespace point-in-time recovery`(`TSPITR`)](./recovery/recovery_tspitr/recovery_tspitr.md)
      - [`Table point-in-time recovery` (`TPITR`)](./recovery/recovery_tpitr/recovery_tpitr.md)
  - [Block Corruption & `Block Media Recovery`](./recovery/recovery_block/recovery_block.md)
  - Recovery Additional Database Files
    - [`Server Parameter File` & `Control File`](./recovery/recovery_spf_cf/recovery_spf_cf.md)
    - [`NOLOGGING` Database Objects](./recovery/recovery_nolog/recovery_nolog.md)
    - [`Redo Log`](./recovery/recovery_redolog/recovery_redolog.md)
    - [Re-creating Password File](./recovery/recovery_pwd_file/recovery_pwd_file.md)

---

- [`Flashback`](./flashback/flashback/flashback.md)
  - [`Flashback Query`](./flashback/flashback_query/flashback_query.md)
  - [`Flashback Version Query`](./flashback/flashback_version_query/flashback_version_querys.md)
  - [`Flashback Table`](./flashback/flashback_table/flashback_table.md)
  - [`Flashback Transaction Query`](./flashback/flashback_tran_query/flashback_tran_query.md)
  - [`Flashback Transaction Backout`](./flashback/flashback_tran_backout/flashback_tran_backout.md)
  - [`Flashback Drop` & Recycle Bin](./flashback/flashback_drop/flashback_drop.md)
  - [`Flashback Data Archives`](./flashback/flashback_archive/flashback_archive.md)
  - [`Flashback Database`](./flashback/flashback_database/flashback_database.md)

---

- [PDB Snapshots](./pdb_snapshot/pdb_snapshot/pdb_snapshot.md)
- [Database Duplication](./db_duplication/db_duplication/db_duplication.md)
  - [Backup-Based Duplicate Database](./db_duplication/backup_duplicate/backup_duplicate.md)

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
