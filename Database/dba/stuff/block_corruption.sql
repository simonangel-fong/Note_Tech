
-- create the `BC` user, the `BCTBS` tablespace, and the `BCCOPY` table.
ALTER SESSION SET container=orclpdb;
show con_name
ALTER DATABASE open;
show pdbs

-- CLEANUP from previous run
DROP USER bc CASCADE;
DROP TABLESPACE bctbs INCLUDING CONTENTS AND DATAFILES;

-- Create tablespace
CREATE TABLESPACE bctbs
DATAFILE '/u01/app/oracle/oradata/ORCL/orclpdb/bctbs01.dbf'
SIZE 10M REUSE
SEGMENT SPACE MANAGEMENT MANUAL;

-- Create user
CREATE USER bc IDENTIFIED BY pass4BC
DEFAULT TABLESPACE bctbs
QUOTA UNLIMITED ON bctbs;

GRANT CREATE SESSION TO bc;

-- create table and populate
-- be sure table is at least 2 blocks long
CREATE TABLE bc.bccopy
TABLESPACE bctbs
AS SELECT * FROM HR.EMPLOYEES;

INSERT INTO bc.bccopy
SELECT * FROM bc.bccopy;

INSERT INTO bc.bccopy
SELECT * FROM bc.bccopy;

--  confirm table has been created
SELECT salary
FROM bc.bccopy
WHERE rownum = 1;

-------- update the table
ALTER SESSION SET container=orclpdb;
show con_name
UPDATE bc.bccopy SET salary = salary+1;
COMMIT;

-- confirm
SELECT salary
FROM bc.bccopy
WHERE rownum = 1;

-------- -- Find the file and block numbers
ALTER SESSION SET container=orclpdb;
-- Find the file and block numbers
SELECT DISTINCT
   MIN(DBMS_ROWID.ROWID_RELATIVE_FNO(rowid)) as FILE_NO,
   MIN(DBMS_ROWID.ROWID_BLOCK_NUMBER(rowid)) as BLOCK_NO
FROM bc.bccopy;

ALTER SYSTEM FLUSH BUFFER_CACHE;

-------- Query the table after corruption.

SELECT *
FROM bc.bccopy;

-------- list block corruption

SELECT * 
FROM V$DATABASE_BLOCK_CORRUPTION;

SELECT * FROM V$DIAG_INFO;

-------- confirm block recovery

alter session set container = orclpdb;
-- query after recovery
SELECT salary
FROM BC.BCCOPY
WHERE rownum = 1;

-------- cleanup

ALTER SESSION SET container=orclpdb;
DROP USER bc CASCADE;
DROP TABLESPACE bctbs INCLUDING CONTENTS AND DATAFILES;


------- 
show parameter DB_BLOCK_CHECKING;
show parameter DB_BLOCK_CHECKSUM;
