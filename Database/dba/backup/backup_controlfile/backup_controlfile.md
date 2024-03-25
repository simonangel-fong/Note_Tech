# Back up Control File

[Back](../../index.md)

- [Back up Control File](#back-up-control-file)
  - [Lab: Back Up the Control File to a Trace File](#lab-back-up-the-control-file-to-a-trace-file)
  - [Lab: Recreate Control Files using a Trace File](#lab-recreate-control-files-using-a-trace-file)
  - [Lab: Back Up Additional Database Files](#lab-back-up-additional-database-files)
  - [Lab: Back Up Archive Log Files](#lab-back-up-archive-log-files)
  - [Lab: Create an Archival Backup](#lab-create-an-archival-backup)

---

## Lab: Back Up the Control File to a Trace File

```sql
sqlplus / as sysdba
SELECT name FROM v$controlfile;
ALTER DATABASE BACKUP controlfile TO trace;
exit
```

---

## Lab: Recreate Control Files using a Trace File

- view the code in the trace file

```sh
cd $ORACLE_BASE/diag/rdbms/orcl/orcl/trace
ls
tail alert_orclcdb.log   # find trace file's path
cat orclcdb_ora_8708.trc # view trace file
# Copy the code
# Complete database recovery:
#   NORESETLOG
# Incomplete database recovery:
#   RESETLOG
```

---

- Create a sql script

```sh
cd ~
vi ControlFileBackup.sql
```

- Plaste the code in the script
  - Example

```sql
STARTUP NOMOUNT
CREATE CONTROLFILE REUSE DATABASE "ORCL" NORESETLOGS  ARCHIVELOG
    MAXLOGFILES 16
    MAXLOGMEMBERS 3
    MAXDATAFILES 1024
    MAXINSTANCES 8
    MAXLOGHISTORY 292
LOGFILE
  GROUP 1 '/u01/app/oracle/oradata/ORCL/redo01.log'  SIZE 200M BLOCKSIZE 512,
  GROUP 2 '/u01/app/oracle/oradata/ORCL/redo02.log'  SIZE 200M BLOCKSIZE 512,
  GROUP 3 '/u01/app/oracle/oradata/ORCL/redo03.log'  SIZE 200M BLOCKSIZE 512
-- STANDBY LOGFILE
DATAFILE
  '/u01/app/oracle/oradata/ORCL/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbseed/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbseed/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/users01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbseed/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/orclpdb/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/orclpdb/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/orclpdb/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/orclpdb/users01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdb1/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdb1/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdb1/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdb1/users01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbtest/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbtest/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbtest/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbtest/users01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod1/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod1/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod1/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod1/users01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod2/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod2/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod2/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/prod2/users01.dbf',
  '/u01/app/oracle/oradata/ORCL/PDB10/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/PDB10/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/PDB10/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/PDB10/users01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbts/system01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbts/sysaux01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbts/undotbs01.dbf',
  '/u01/app/oracle/oradata/ORCL/pdbts/users01.dbf'
CHARACTER SET AL32UTF8
;
-- Commands to re-create incarnation table
-- Below log names MUST be changed to existing filenames on
-- disk. Any one log file from each branch can be used to
-- re-create incarnation records.
-- ALTER DATABASE REGISTER LOGFILE '/u01/app/oracle/product/19.0.0/dbhome_1/dbs/arch1_1_1005785759.dbf';
-- ALTER DATABASE REGISTER LOGFILE '/u01/app/oracle/product/19.0.0/dbhome_1/dbs/arch1_1_1154813339.dbf';
-- Recovery is required if any of the datafiles are restored backups,
-- or if the last shutdown was not normal or immediate.
RECOVER DATABASE
-- All logs need archiving and a log switch is needed.
ALTER SYSTEM ARCHIVE LOG ALL;
-- Database can now be opened normally.
ALTER DATABASE OPEN;
-- Open all the PDBs.
ALTER PLUGGABLE DATABASE ALL OPEN;
-- Commands to add tempfiles to temporary tablespaces.
-- Online tempfiles have complete space information.
-- Other tempfiles may require adjustment.
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/temp01.dbf'
     SIZE 33554432  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "PDB$SEED";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/pdbseed/temp012023-12-05_21-31-11-761-PM.dbf'
     SIZE 37748736  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "ORCLPDB";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/orclpdb/temp01.dbf'
     SIZE 135266304  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "PDB1";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/pdb1/temp012023-12-05_21-31-11-761-PM.dbf'
     SIZE 134217728  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "PDBTEST1";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/pdbtest/temp01.dbf'
     SIZE 135266304  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "PROD1";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/prod1/temp012023-12-05_21-31-11-761-PM.dbf'
     SIZE 37748736  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "PROD2";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/prod2/temp012023-12-05_21-31-11-761-PM.dbf'
     SIZE 37748736  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "PDB10";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/PDB10/temp012023-12-05_21-31-11-761-PM.dbf'
     SIZE 135266304  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "PDBTS";
ALTER TABLESPACE TEMP ADD TEMPFILE '/u01/app/oracle/oradata/ORCL/pdbts/temp012023-12-05_21-31-11-761-PM.dbf'
     SIZE 135266304  REUSE AUTOEXTEND ON NEXT 655360  MAXSIZE 32767M;
ALTER SESSION SET CONTAINER = "CDB$ROOT";
-- End of tempfile additions.

```

---

- Startup run the script control file

```sh

```

---

## Lab: Back Up Additional Database Files

- Create a custom directory

```sh
mkdir -p /home/oracle/backup/orclcdb
```

```sql
sqlplus / as sysdba
ALTER database backup controlfile TO trace AS '/home/oracle/backup/orclcdb/control.sql';
exit

```

---

- View trace file

```sh
cat /home/oracle/backup/orclcdb/control.sql
```

---

## Lab: Back Up Archive Log Files

- Log in RMAN as `SYSBACKUP`

```sh
rman target "'/ as sysbackup'"
```

- Back up archive log files and delete the files after the backup completes

```sql
run {
    allocate channel "CH1" DEVICE TYPE DISK FORMAT '/home/oracle/backup/orclcdb/%U';
    backup archivelog all delete all input;
}
exit
```

---

## Lab: Create an Archival Backup

- login RMAN

```sh
rman target "'/ as sysbackup'"
```

- In the RMAN

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
BACKUP AS COPY DATABASE KEEP FOREVER;
-- fails
-- because the KEEP FOREVER requires the use of a recovery catalog

BACKUP AS COPY DATABASE KEEP UNTIL TIME 'SYSDATE+365';
-- error
-- By default, it uses Fast Recovery Area
--  The KEEP option cannot be written to this area.
--  Otherwise, the area will quickly run out of space.

BACKUP DATABASE FORMAT '/home/oracle/backup/%U' TAG keep_db_tag KEEP UNTIL TIME 'SYSDATE+365';

-- open the database after backup
ALTER DATABSE OPEN;

-- Delete obsolete backups.
DELETE obsolete;
-- enter YES if prompt.

```

---

[TOP](#back-up-control-file)
