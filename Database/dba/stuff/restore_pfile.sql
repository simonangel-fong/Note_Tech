
--------- setup user and tbsp
ALTER SESSION SET container=orclpdb;
show con_name

-- CLEANUP from previous run
DROP USER bar CASCADE;
DROP TABLESPACE bartbs INCLUDING CONTENTS AND DATAFILES;

-- Create tablespace
CREATE TABLESPACE bartbs
DATAFILE '/u01/app/oracle/oradata/ORCL/orclpdb/bartbs.dbf' SIZE 10M
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

-------- update the table
ALTER SESSION SET container=orclpdb;
UPDATE BAR.BARCOPY SET salary = salary+1;
COMMIT;

alter pluggable database open;
select * from BAR.BARCOPY;

-------- confirm

alter session set container=orclpdb;
alter pluggable database open;

select * from BAR.BARCOPY;


------ cleanup
ALTER SESSION SET container=orclpdb;

-- CLEANUP from previous run
DROP USER bar CASCADE;
DROP TABLESPACE bartbs INCLUDING CONTENTS AND DATAFILES;

SELECT * 
FROM V$PWFILE_USERS;

--------- 

alter session set container=orclpdb;

-- create tb bar101
create table bar.bar101
as select * from BAR.BARCOPY;

ALTER TABLE BAR.BAR101
add (address_line1 VARCHAR2(200), address_line2 VARCHAR2(200));

-- create tb bar102
create table bar.bar102
as select * from BAR.BARCOPY;

ALTER TABLE BAR.BAR102
add (address_line1i VARCHAR2(200), address_line2 VARCHAR2(200));

-- drop tb bar102
drop table BAR.BAR102;

-- create new tb bar102
create table bar.bar102
as select * from BAR.BARCOPY;

ALTER TABLE BAR.BAR102
add (location_id NUMBER(12));

-- drop tb bar102
drop table bar.bar102;

-- drop tb bar101
drop table bar.bar101;

-- create new tb bar102
create table bar.bar102
as select * from BAR.BARCOPY;

ALTER TABLE BAR.BAR102 add (photo BLOB);

-------- 

SHOW RECYCLEBIN

select original_name, object_name, droptime
from dba_recyclebin
where owner ='BAR';

BIN$GYdu7BtlD3fgYyUAqMCkFg==$0
BIN$GYdu7BtgD3fgYyUAqMCkFg==$0
BIN$GYdu7BtqD3fgYyUAqMCkFg==$0

SELECT location_id
FROM BAR."BIN$GYdu7BtlD3fgYyUAqMCkFg==$0"
WHERE rownum = 1;

FLASHBACK TABLE BAR."BIN$GYdu7BtlD3fgYyUAqMCkFg==$0"
TO BEFORE DROP
RENAME TO BAR102A;

select *
from BAR.BAR102A
where rownum = 1;

---------

ALTER SESSION set container=orclpdb;

DROP USER bar CASCADE;
DROP TABLESPACE bartbs INCLUDING CONTENTS AND DATAFILES PURGE DBA_RECYCLEBIN;

PURGE RECYCLEBIN;
SHOW RECYCLEBIN;


--------

SELECT *
FROM   user_tables
WHERE  table_name = 'BARDEPT'
AND tablespace_name = 'BARTBS';