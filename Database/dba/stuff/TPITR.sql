-------- Confirm configuration
show parameter compatible
show parameter db_recovery_file_dest

ALTER SESSION SET container=cdb$root;
SELECT NAME, LOG_MODE, OPEN_MODE
FROM V$DATABASE;

-------- Setup env

ALTER SESSION SET container=orclpdb;
show con_name

-- CLEANUP from previous run
DROP USER bar CASCADE;
DROP TABLESPACE bartbs INCLUDING CONTENTS AND DATAFILES;

-- Create tablespace
CREATE TABLESPACE bartbs
DATAFILE '/u01/app/oracle/oradata/ORCL/orclpdb/bartbs.dbf'
SIZE 10M REUSE SEGMENT SPACE MANAGEMENT MANUAL;

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

ALTER SESSION SET container=cdb$root;
ALTER SYSTEM SWITCH logfile;

ALTER SESSION SET container=orclpdb;
ALTER SYSTEM checkpoint;

-- confirm user and tbsp have been created
ALTER SESSION SET container=orclpdb;
SELECT TABLE_NAME, TABLESPACE_NAME, STATUS
FROM DBA_TABLES
WHERE OWNER = 'BAR';

-------- Create test table
-- drop existing tb
DROP TABLE BAR.test_table;

-- create tb
CREATE TABLE BAR.test_table
(
  NUM number(8),
  NAME varchar2(25),
  NOW  date
);

-- insert data
INSERT INTO BAR.test_table VALUES (1,'First test row',sysdate);
INSERT INTO BAR.test_table VALUES (2,'Second test row',sysdate);
INSERT INTO BAR.test_table VALUES (3,'Third test row',NULL);
commit;

ALTER SESSION SET container=cdb$root;
ALTER SYSTEM SWITCH logfile;
ALTER SESSION SET container=orclpdb;
ALTER SYSTEM checkpoint;

-- get the SCN!
SELECT NAME, CURRENT_SCN
FROM V$DATABASE;

-- confirm data
SELECT *
FROM BAR.TEST_TABLE;

-------- Purge test table
-- Query scn before purging
SELECT NAME, CURRENT_SCN
FROM V$DATABASE;

-- purge test table
drop table BAR.test_table purge;

-- confirm purge of table
SELECT table_name
FROM dba_tables
WHERE owner = 'BAR';

-- Query scn after purging
SELECT NAME, CURRENT_SCN
FROM V$DATABASE;

-- confirm recovery of table
SELECT *
FROM BAR.TEST_TABLE;

-------- Clear up

ALTER SESSION SET container=orclpdb;

-- CLEANUP from previous run
DROP USER bar CASCADE;
DROP TABLESPACE bartbs INCLUDING CONTENTS AND DATAFILES;