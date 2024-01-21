# Oracle DBA 1 - Connecting to Oracle Database Instance

[Back](../index.md)

- [Oracle DBA 1 - Connecting to Oracle Database Instance](#oracle-dba-1---connecting-to-oracle-database-instance)
  - [Connecting to an Oracle Database Instance](#connecting-to-an-oracle-database-instance)
    - [Connecting to CDB by using operating system authentication](#connecting-to-cdb-by-using-operating-system-authentication)
    - [Connecting to PDBs by using Easy Connect Systax in SQL\*Plus](#connecting-to-pdbs-by-using-easy-connect-systax-in-sqlplus)
  - [Disconnecting from the database instance](#disconnecting-from-the-database-instance)
  - [Oracle Tools](#oracle-tools)
  - [SQL\*Plus](#sqlplus)
    - [Calling a SQL Script from SQL\*Plus](#calling-a-sql-script-from-sqlplus)
    - [Calling SQL\*Plus from a Shell Script](#calling-sqlplus-from-a-shell-script)

---

## Connecting to an Oracle Database Instance

- Connection:

  - the physical communication pathway between a client process and a database instance.
  - connect client applications to **database instances**, _not databases_.

- `User session`
  - a **logical entity** that represents **the state of the current user login** to the database instance.
  - lasts from the time the user is authenticated by database instance until the time the user disconnects or exits the client application.

---

### Connecting to CDB by using operating system authentication

```sh
# System authentication does not require user ID, password
#   if supply one, it is totally ignored
# Connection is based on the user at the OS level.
#   However, it is important to identify as whom a user logges into the operating system. Connection will be mapped through the OS user.
sqlplus / as sysdba
# slash "/" here identify to connect to the OS.
# sysdba: the role as whom the current user acts
#           the owner of the databse with the highest previlige.
# the current operating system user must be a member of the privileged OSDBA group

# A safe way to log in using a paricular user name and pwd
sqlplus # then sql prompt will show up for user name and pwd.
```

- Rules:

  - User who try to login must be on the same machine as the database instance.
  - The current OS user must be a member of privileged **OSDBA** group.

- it is not safe to use command: `sqlplus user_id/pwd`, because user id and pwd will show in the command, which is not safe.

### Connecting to PDBs by using Easy Connect Systax in SQL\*Plus

```sql

connect username/pwd@host_name:port/service_name
```

- Support `TCP` protocol only (no `SSL`)

- Syntax:

  - SQL

```sql
CONNECT username/password@host_name:port/service_name
```

- SQLPLUS

```sh
sqlplus username/password@host_name:port/service_name
```

- Arguements:
  - `host_name`:
    - where the listener is running at
  - `port`: optional
    - where listener is listening at
    - default: 1521
  - `service_name`: optional
    - the service of a particular databse to perform work.
    - default: identical with host name.

---

## Disconnecting from the database instance

```sql
EXIT
```

- Disconnect:
  - end all sessions in database instance memory.

---

## Oracle Tools

- Tools:
  - SQL\*Plus:
    - a command-line tool to access a database.
  - SQL Developer:
    - GUI tool
    - **PDB only**
  - SQL Developer Command Line (SQLcl)
  - Database Configuration Assistant (DBCA):
    - GUI tool to create db
  - Oracle Enterprise Manager Database Express (EM Express):
    - GUI tool for admin tasks on one target
    - **PDB only**
  - Oracle Enterprise Manager Cloud Control:
    - GUI tool for admin tasks on multiple targets
    - **PDB only**
  - Oracle Management Cloud Database Express (OMX):
    - GUI tool for admin tasks
  - Listener Control
  - Oracle Net Configuration Assistant
  - Oracle Net Manager
  - ADR Command Interpeter
  - SQL\*Loader
  - Oracle Data Pump Import
  - Oracle Data Pump Export

---

## SQL\*Plus

- `SQL*Plus`

  - a command-line program used to submit SQL and PL/SQL statements to Oracle database.
  - installed with Oracle database
  - located in `ORACLE_HOME/bin` directory.

---

### Calling a SQL Script from SQL\*Plus

- Option 1: call script when first invoke SQL\*Plus

```sh
sqlplus username/pwd@host_name @script.sql
```

- Option 2: call script inside a SQL\*Plus session

```sql
@script.sql
```

---

### Calling SQL\*Plus from a Shell Script

```sh
sqlplus username/pwd <<EOF
select count(*) from employees;
update employees set salary = salary*1.10;
commit;
quit
EOF
```

---

[TOP](#oracle-dba-1---connecting-to-oracle-database-instance)
