# External Table

[Back](./index.md)

- [External Table](#external-table)
  - [Ex tb](#ex-tb)

---

## Ex tb

- Create user as sys

```sql
-- external tb

ALTER SESSION SET "_ORACLE_SCRIPT"=true;

--create user
DROP USER ext_user CASCADE;

--CREATE USER ext_user
--IDENTIFIED BY ext_user
--DEFAULT TABLESPACE users
--TEMPORARY TABLESPACE temp
--QUOTA UNLIMITED ON users;

CREATE USER ext_user
IDENTIFIED BY ext_user;

-- create directory
DROP directory ext_dir;

CREATE OR REPLACE DIRECTORY ext_dir
AS '/home/oracle/ext_dir';

GRANT connect, resource to ext_user;
GRANT read, write ON DIRECTORY ext_dir TO ext_user;
```

---

- Create table as created user

```sql

--create ext_tb
CREATE TABLE ext_tb(
    DEPARTMENT_ID NUMBER NOT NULL,
    DEPTNAME VARCHAR2 (25),
    DEPTDESC VARCHAR2 (100),
    DEPTIMAGE VARCHAR2 (30)
)
ORGANIZATION EXTERNAL(
    TYPE ORACLE_LOADER
    DEFAULT DIRECTORY ext_dir
    ACCESS PARAMETERS (
        RECORDS DELIMITED BY NEWLINE
        FIELDS TERMINATED BY ','
        MISSING FIELD VALUES ARE NULL
        (
            DEPARTMENT_ID CHAR(2),
            DEPTNAME CHAR(25),
            DEPTDESC CHAR(100),
            DEPTIMAGE CHAR(30)
        )
    )
    LOCATION ('Dept.csv')
)
REJECT LIMIT UNLIMITED;


SELECT * FROM ext_tb;

```

---

[TOP](#external-table)
