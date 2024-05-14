# `RMAN` - Configuration

[Back](../../index.md)

- [`RMAN` - Configuration](#rman---configuration)
  - [Configuration](#configuration)

---

## Configuration

```sql
-- Sets the retention policy for backups to a recovery window of 7 days,
--      RMAN will retain backups from the last 7 days, allowing recovery to any point within this time frame.
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;

-- Sets the default device type for backups to disk,
--      ensuring all backups without a specified device type default to disk for storage.
CONFIGURE DEFAULT DEVICE TYPE TO DISK;

-- Enables automatic backup of the control file,
--      creating a backup each time a backup is made or when structural changes occur.
CONFIGURE CONTROLFILE AUTOBACKUP ON;

-- Configures the format for disk backups,
--      storing files in the specified directory and naming them with date, unique ID, session, and piece number.
CONFIGURE CHANNEL DEVICE TYPE DISK FORMAT '/u03/backup/orcl/backup%d_DB_%u_%s_%p';


-- Configures the DISK device type to create backups as image copies,
--      which are exact copies of data files and control files, rather than backup sets.
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO COPY;

```

---

[TOP](#rman---configuration)
