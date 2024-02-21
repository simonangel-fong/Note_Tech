# Loader

[Back](./index.md)

---

## Lab

- Sys create user

```sql
-- Task: create user
ALTER SESSION SET "_ORACLE_SCRIPT"=true;

DROP USER loader CASCADE;

CREATE USER loader
IDENTIFIED BY loader
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON users;

GRANT connect, resource TO loader;

```

---

- user create tb

```sql
-- create tb as loader

--
DROP TABLE AGENTS2;

CREATE TABLE AGENTS2 (
  AgentID NUMBER PRIMARY KEY,
  FirstName VARCHAR2(30),
  LastName VARCHAR2(30),
  HireDate DATE,
  BirthDate DATE,
  Gender VARCHAR2(10),
  WorkPhone VARCHAR2(20),
  CellPhone VARCHAR2(20),
  HomePhone VARCHAR2(20),
  Title VARCHAR2(20),
  TaxID VARCHAR2(20),
  LicenseID VARCHAR2(20),
  LicenseDate DATE,
  LicenseExpire DATE,
  LicenseStatusID NUMBER
);




select * from Agents2;


```

---

- Create ctl: `03loader_ctl.ctl`

```sh
load data
  infile 'Agents.csv'
  into table Agents2
  fields terminated by "," optionally enclosed by "'"
  (
    AgentID,
    FirstName,
    LastName,
    HireDate,
    BirthDate,
    Gender,
    WorkPhone,
    CellPhone,
    HomePhone,
    Title,
    TaxID,
    LicenseID,
    LicenseDate,
    LicenseExpire,
    LicenseStatusID
  )

```

---

- execute load

```sh
sqlldr loader/loader@orcl control=03loader_ctl.ctl
```

---

[TOP](#loader)
