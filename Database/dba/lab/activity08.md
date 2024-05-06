# Lab 17-1: Repairing Block Corruption

[Back](../index.md)

- [Lab 17-1: Repairing Block Corruption](#lab-17-1-repairing-block-corruption)
  - [Exercise 24-1: Restore and Recover the `USERS` Tablespace](#exercise-24-1-restore-and-recover-the-users-tablespace)
  - [Exercise 24-5: Restore the control file from an AutoBackup](#exercise-24-5-restore-the-control-file-from-an-autobackup)
  - [Exercise 24-6: Create a Replacement Tempfile for the TEMP Tablespace](#exercise-24-6-create-a-replacement-tempfile-for-the-temp-tablespace)

---

## Exercise 24-1: Restore and Recover the `USERS` Tablespace

- In this exercise, the datafile for the `USERS` **tablespace** was accidentally deleted by the system administrator.
- Restore and recover the tablespace while the database is still open for access to the other tablespaces.
- It is assumed that previous exercises have been completed.

---

- restore tbsp

```sql
rman target=sys@orclpdb

-- 1. Connect to RMAN and take the USERS tablespace offline.
-- using rman
sql "alter tablespace users offline immediate";
-- Any users trying to access the tablespace while it is offline will receive a message
-- select * from sales_data;

-- 2. Restore the USERS tablespace.
-- rman
restore tablespace users;

-- 3. Recover the USERS tablespace to apply the archived and online redo log files.
recover tablespace users;

-- 4. Bring the USERS tablespace back online.
sql "alter tablespace users online";


-- 5. Confirm that users can once again access the USERS tablespace.
-- in plus sql
SELECT * FROM sales_data;
```

---

- Restore datafile

```sql
ALTER DATABASE datafile df_name offline;
alter database datafile '/u01/app/oracle/oradata/ORCL/orclpdb/users01.dbf' offline;

RESTORE datafile df_name;
RESTORE datafile '/u01/app/oracle/oradata/ORCL/orclpdb/users01.dbf';

RECOVER datafile df_name;
RESTORE datafile '/u01/app/oracle/oradata/ORCL/orclpdb/users01.dbf';

ALTER DATABASE datafile df_name online;
alter database datafile '/u01/app/oracle/oradata/ORCL/orclpdb/users01.dbf' online;
```

---

## Exercise 24-5: Restore the control file from an AutoBackup

- In this exercise, all copies of the controlfile were accidentally deleted by an overly eager system administrator trying to free up disk space. Restore and recover the database with a controlfile restored from a controlfile and spfile autobackup

```sql
-- 1. Identify the controlfile locations where all copies of the controlfile used to reside.
SHOW PARAMETER control_files;

-- 2. Use an operating system command to delete all copies of the controlfile.
rm -f /u01/app/oracle/oradata/ORCL/control01.ctl /u01/app/oracle/oradata/ORCL/control02.ctl

-- 3. Shut down the instance (if it is not already down) and reopen it in NOMOUNT mode.
-- sqlplus
CONNECT / as sysdba
shutdown immediate
startup force nomount

-- 3. Start RMAN and restore the controlfile from autobackup to the original locations
-- shell
rman target /

-- rman
RESTORE CONTROLFILE FROM autobackup;

-- 5. Mount the database, recover the database (to synchronize the datafiles with the restored controlfile), and open the database with RESETLOGS.
-- rman
ALTER DATABASE mount;
RECOVER DATABASE;
ALTER DATABASE open resetlogs;
```

---

## Exercise 24-6: Create a Replacement Tempfile for the TEMP Tablespace

- In this exercise, the tempfile for the `TEMP` **tablespace** was accidentally deleted, so you must create another tempfile to replace it while the database is still running.

```sql
-- 1. Identify the name of the tempfile for the TEMP tablespace
SELECT file#, name FROM v$tempfile;

-- 2. Create a new tempfile with a different name for the TEMP tablespace
ALTER TABLESPACE temp add tempfile
'/u01/app/oracle/oradata/ORCL/orclpdb/temp02.dbf'
size 25m;

-- 3. Drop the previous tempfile. This will update only the controlfile because the original tempfile is missing
ALTER TABLESPACE temp drop tempfile
'/u01/app/oracle/oradata/ORCL/orclpdb/temp01.dbf';

-- 4. Confirm that the TEMP tablespace contains only the newly created tempfile
SELECT file#, name FROM v$tempfile;
```

---

[TOP](#lab-17-1-repairing-block-corruption)
