# RMAN - Backup Commands

[Back](../../index.md)

- [RMAN - Backup Commands](#rman---backup-commands)
  - [Tag](#tag)
  - [ALL](#all)
  - [SPFILE](#spfile)
  - [Control File](#control-file)
  - [Datafile](#datafile)
  - [Pluggable Database](#pluggable-database)
  - [Archived Redo Log](#archived-redo-log)
  - [Tablespace](#tablespace)
  - [Incarnations](#incarnations)

---

## Tag

- `tag`

  - a human-readable symbolic name.
  - used to reference `backupset`, `image copy` or `control file copy`

- By default, tag automatically to all backupsets.
  - a format `TAGYYYYMMDDTHHMMSS`, where `YYYYMMDD` is a date and `HHMMSS` is a time of when taking the backup was started.

```sql
-- Tagging a backup with a specific name:
BACKUP DATABASE TAG 'your_custom_tag';

-- Tagging a backup of the SPFILE:
BACKUP SPFILE TAG 'spfile_tag';

-- Tagging a backup of archived redo logs:
BACKUP ARCHIVELOG ALL TAG 'archivelog_tag';

-- Tagging a backup of data files in a specific tablespace:
BACKUP TABLESPACE users TAG 'users_data_files_tag';

-- Tagging an image copy:
BACKUP AS COPY DATAFILE 1 TAG 'datafile_copy_tag';

-- Tagging a backup of the control file:
BACKUP CONTROLFILE TAG 'controlfile_tag';
```

---

## ALL

- List

```sql
-- List all backups
LIST BACKUP;
LIST BACKUP BY FILE;
LIST BACKUP SUMMARY;
LIST EXPIRED BACKUP SUMMARY;

-- List backup before a date
LIST BACKUP COMPLETED BEFORE 'SYSDATE - X'; -- replace X with the number of days

-- lists only disk copies
--    all datafile copies, control file copies, and archived logs
LIST COPY;

-- List all archived log
LIST ARCHIVELOG ALL;
```

- Delete all

```sql
-- Delete all backup sets
DELETE BACKUP;

-- Delete all image copies
DELETE COPY;

-- Delete all archived log
DELETE ARCHIVELOG ALL;
```

---

## SPFILE

- Backup

```sql
-- Create SPFILE backup as a backup set:
BACKUP SPFILE;
-- Create SPFILE backup as a backup set with a specific tag:
BACKUP SPFILE TAG <tag_name>;

-- Create SPFILE backup as a backup set:
BACKUP AS COPY SPFILE;    -- even though it seems to be copy, but as backup set actually.
```

- List

```sql
-- List all backup sets of the SPFILE:
LIST BACKUP OF SPFILE;
-- Filter backup set of SPFILE by key:
LIST BACKUPSET <key>;
```

- Delete

```sql
-- Delete all backup sets of the SPFILE:
DELETE BACKUP OF SPFILE;
-- Delete a backup set of the SPFILE by key:
DELETE BACKUPSET <key>;
```

---

-- Delete specific types of backups:
DELETE BACKUP OF DATAFILE; -- Deletes only data file backups.

---

## Control File

- Backup

```sql
-- Create control file backup as backup set
BACKUP CURRENT CONTROLFILE;
-- with tag
BACKUP CURRENT CONTROLFILE TAG = <tag_name>;
-- if autobackup if off
<backup_clause> INCLUDE CURRENT CONTROLFILE.

-- Create control file backup as image copy
BACKUP AS COPY CURRENT CONTROLFILE;
```

- List

```sql
-- List all backup sets of control cile
LIST BACKUP OF CONTROLFILE;
-- Filter backup sets of control file copy by key
LIST BACKUPSET <key>;

-- List all image copy of control file
LIST COPY OF CONTROLFILE;
-- Filter image copy of control file copy by key
LIST CONTROLFILECOPY <key>;
```

- Delete

```sql
-- Delete all backup set of control file
DELETE BACKUP OF CONTROLFILE;
-- Delete a backup set of control file by key
DELETE BACKUPSET <key>;

-- Delete all copies of control file
DELETE COPY OF CONTROLFILE;
-- Delete a copy of control file by key
DELETE CONTROLFILECOPY <key>;
```

---

## Datafile

- Backup

```sql
-- Create backup sets of datafile and control file
BACKUP DATABASE;
-- Create datafile backup as a backup set by file number
BACKUP AS BACKUPSET DATAFILE <file#>;
-- Create datafile backup as a backup set with a specific tag:
BACKUP AS BACKUPSET DATAFILE <file#> TAG <tag_name>;
-- Create datafile backup as a backup set by path
BACKUP AS BACKUPSET DATAFILE 'path';

-- Create image copies of datafile and control file
BACKUP AS COPY DATABASE;
-- Create datafile backup as an image copy:
BACKUP AS COPY DATAFILE <file#>;
-- Create datafile backup as an image copy with a specific tag:
BACKUP AS COPY DATAFILE <file#> TAG <tag_name>;
-- Create datafile backup as an image copy by path
BACKUP AS BACKUPSET DATAFILE 'path';
```

- List

```sql
-- List backup sets of all datafiles
LIST BACKUP OF DATABASE;
-- List backup set of a datafile by file number
LIST BACKUP OF DATAFILE <file#>;

-- List image copies of all datafiles
LIST DATAFILECOPY ALL;
-- List image copy by key
LIST DATAFILECOPY <key>;
-- List image copy by the name
LIST DATAFILECOPY '<datafile_image_copy_name>';
```

- Delete Datafile

```sql
-- Delete buckup set by key
DELETE BACKU <key>;
DELETE BACKUPSET <key>;
-- Delete backup set containing the datafile with a specific file number
DELETE BACKUP OF DATAFILE <file#>;

-- Delete all image copies of data file
DELETE DATAFILECOPY ALL;
-- Delete image copy by key
DELETE DATAFILECOPY <key>;
-- Delete image copy by the name
DELETE DATAFILECOPY '<datafile_image_copy_name>';
```

---

## Pluggable Database

- Backup

```sql
-- Create backup sets of pluggable database
BACKUP PLUGGABLE DATABASE 'cdb$root', pdb1;

-- Create image copy of pluggable database
BACKUP AS COPY PLUGGABLE DATABASE 'cdb$root', pdb1;
```

- List

```sql
-- List backup sets of pluggable database
LIST BACKUP OF PLUGGABLE DATABASE pdb1;   -- cannot list multiple

-- list image copy of pluggable database   -- cannot list multiple
LIST COPY OF PLUGGABLE DATABASE pdb1;
```

- Delete

```sql
-- Delete backup sets of pluggable database
DELETE BACKUP OF PLUGGABLE DATABASE pdb1;

-- Delete image copies of pluggable database
DELETE COPY OF PLUGGABLE DATABASE pdb1;
```

---

## Archived Redo Log

- Backup

```sql
-- Create backup sets of all archivelog
BACKUP ARCHIVELOG ALL;
-- Create backup sets of archivelog that not have been backed up once
BACKUP ARCHIVELOG ALL NOT BACKED UP 1 TIMES;
-- Create backup sets of archivelog and delete backed up archivelog
BACKUP ARCHIVELOG ALL DELETE INPUT;

BACKUP AS COPY ARCHIVELOG LIKE '%arc%';
```

- List

```sql
-- List backup sets of all archivelog
LIST BACKUP OF ARCHIVELOG ALL;

-- List image copies of all archivelog
LIST ARCHIVELOG ALL;
```

- Delete

```sql
-- Delete backup sets of all archivelog
DELETE BACKUP OF ARCHIVELOG ALL;
-- Delete backups completed before a certain date:
DELETE BACKUP COMPLETED BEFORE 'SYSDATE - X'; -- replace X with the number of days.
-- Delete backups with a specific backup tag:
DELETE BACKUP WHERE TAG = 'YOUR_TAG';

-- Delete image copies of all archivelog
DELETE ARCHIVELOG ALL;
```

---

## Tablespace

- Backup

```sql
-- Create backup sets of tablespace
BACKUP TABLESPACE <con_name>:<tablespace_name>;
-- for cdb container
BACKUP TABLESPACE 'cdb$root':users;
-- for pdb
BACKUP TABLESPACE pdb1:users;
-- multiple
BACKUP TABLESPACE pdb1:users, 'cdb$root':users;

-- Create image copies of tbsp
BACKUP AS COPY TABLESPACE pdb1:users, 'cdb$root':users;
```

- List

```sql
-- List backup sets of tablespace by name
LIST BACKUP OF TABLESPACE <con_name>:<tablespace_name>;
-- List backup sets of tablespace in current container by tbsp name
LIST BACKUP OF TABLESPACE <tablespace_name>;
-- for cdb container
LIST BACKUP OF TABLESPACE 'cdb$root':users;
-- for pdb
LIST BACKUP OF TABLESPACE pdb1:users;
-- multiple
LIST BACKUP OF TABLESPACE pdb1:users, 'cdb$root':users;
-- summary of backup sets
LIST BACKUP OF TABLESPACE pdb1:users, 'cdb$root':users SUMMARY;

-- List image copies of tbsp
LIST COPY OF TABLESPACE pdb1:users, 'cdb$root':users;
```

- Delete

```sql
-- Delete backup sets of tbsp
DELETE BACKUP OF TABLESPACE <con_name>:<tablespace_name>;
DELETE BACKUP OF TABLESPACE pdb1:users, 'cdb$root':users;

-- Delete image copies
DELETE COPY OF TABLESPACE pdb1:users, 'cdb$root':users;
```

---

## Incarnations

```sql
-- List database incarnations:
LIST INCARNATION;
```

---

[TOP](#dba---manage-backups)
