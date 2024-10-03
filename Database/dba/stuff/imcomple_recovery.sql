-- 

-- drop
ALTER SESSION SET container=cdb$root;
ALTER PLUGGABLE DATABASE orclpdb CLOSE;
DROP PLUGGABLE DATABASE orclpdb INCLUDING DATAFILES;

CREATE PLUGGABLE DATABASE orclpdb
  ADMIN USER orclpdbadmin IDENTIFIED BY welcome  -- Create a new user
  ROLES = (dba)     -- privilege: give dba role to the new user
  DEFAULT TABLESPACE users  -- create a new tbsp,
    -- create a df for users tbsp,
    DATAFILE '/u01/app/oracle/oradata/ORCL/orclpdb/users01.dbf'
    -- assign size
    SIZE 250M
    -- auto extend size
    AUTOEXTEND ON
  -- convert the file name from the seed dir to the new pdb dir
  FILE_NAME_CONVERT = ('/u01/app/oracle/oradata/ORCL/pdbseed/',
                       '/u01/app/oracle/oradata/ORCL/orclpdb/');

---------- Installing the HR Schema

ALTER SESSION SET container=orclpdb;
show con_name

ALTER PLUGGABLE DATABASE orclpdb OPEN;
SELECT name, open_mode 
FROM v$pdbs;

-- create hr schema
CREATE USER hr IDENTIFIED BY welcome;
GRANT CREATE SESSION, resource TO hr;

-- Create tables
-- @?/demo/schema/human_resources/hr_main.sql
-- $ORACLE_HOME/demo/schema/log


--------- create tbsp

alter session set container=orclpdb;
show user
show con_name

-- CLEANUP from previous run
DROP USER bar CASCADE;
DROP TABLESPACE bartbs INCLUDING CONTENTS AND DATAFILES;

-- Create tablespace
CREATE TABLESPACE bartbs
DATAFILE '/u01/backup/orcl/orclpdb/bartbs.dbf' SIZE 10M REUSE
SEGMENT SPACE MANAGEMENT MANUAL;

-- Create user
CREATE USER BAR IDENTIFIED BY pass4BAR
DEFAULT TABLESPACE bartbs
QUOTA UNLIMITED ON bartbs;

GRANT CREATE SESSION TO BAR;

-- create table and populate
-- be sure table is at least 2 blocks long
CREATE TABLE BAR.barcopy
TABLESPACE bartbs
AS SELECT * FROM HR.EMPLOYEES;

INSERT INTO BAR.BARCOPY
SELECT * FROM BAR.BARCOPY;

INSERT INTO BAR.BARCOPY
SELECT * FROM BAR.BARCOPY;

------ update table
show con_name

UPDATE BAR.BARCOPY SET salary = salary+1;
COMMIT;
ALTER SYSTEM FLUSH BUFFER_CACHE;

--------- switch log
show con_name

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

EXEC DBMS_LOCK.SLEEP(1.5);
alter session set container=cdb$root;
ALTER SYSTEM SWITCH LOGFILE;
alter session set container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
Commit;

select salary from BAR.BARCOPY
where rownum = 1;
ALTER SYSTEM FLUSH BUFFER_CACHE;

------- remove archivelog

select 'rm "'||name||'"'
from v$archived_log
where (sequence#, resetlogs_id) =
(select sequence# - 2, resetlogs_id from v$archived_log
where first_time = (select distinct (max(first_time)) from v$archived_log));

-------- scn
ARCHIVE LOG LIST

show con_name

alter session set container=orclpdb;

SELECT NAME, DBID, CURRENT_SCN, LOG_MODE, OPEN_MODE 
FROM V$DATABASE;

select sequence#, first_change#, first_time, status 
from v$archived_log 
where sequence# = 8 
and name is not null;

------- confirm
alter session set container=orclpdb;
select salary from bar.barcopy where rownum < 2;

select salary from BAR.BARCOPY
where rownum = 1;

alter session set container=cdb$root;

ALTER SESSION SET CONTAINER=orclpdb;
SELECT NAME, DBID, CURRENT_SCN, LOG_MODE, OPEN_MODE FROM
V$DATABASE ;

show pdbs

SELECT salary 
FROM bar.barcopy 
WHERE rownum = 1;