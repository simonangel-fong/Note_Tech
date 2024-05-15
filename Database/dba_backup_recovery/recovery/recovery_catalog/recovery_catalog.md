# Recovery - Catalog

[Back](../../index.md)

- [Recovery - Catalog](#recovery---catalog)
  - [Recovery Catalog](#recovery-catalog)
    - [Pros and Cons](#pros-and-cons)
    - [`Control File` vs `Catalog`](#control-file-vs-catalog)
  - [Creating a Recovery Catalog](#creating-a-recovery-catalog)
    - [Configuring the Recovery Catalog Database](#configuring-the-recovery-catalog-database)
    - [Creating the Recovery Catalog Owner](#creating-the-recovery-catalog-owner)
    - [Creating the Recovery Catalog](#creating-the-recovery-catalog)
  - [Lab: Create a Recovery Catalog](#lab-create-a-recovery-catalog)

---

## Recovery Catalog

- The RMAN repository data is

  - always stored in the `control file` of the target database.
  - can also, additionally, be stored in a **separate database** in a `recovery catalog`.

---

- `recovery catalog`

  - preserves **backup information** in a separate database, which is useful in the event of a lost control file.

![diagram_recovery_catalog01](./pic/diagram_recovery_catalog01.png)

- **RMAN** propagates information about target database into the `recovery catalog` from the target database's `control file` after any operation that updates the repository and also before certain operations, including:

  - `database structure`,
  - `archived redo logs`,
  - `backup sets`,
  - `data file copies`

- 是 RMAN 更新目标信息; 从 cf 提取; 时机:任何更新之后; 文件: 结构, log, bs, copy

- **Prerequisites**: 前设:同时连接两个实例
  - For information propagation to take place, the RMAN client must be connected to both
    - the `target database instance`
    - the `catalog database instance`

---

### Pros and Cons

Benefits

- Stores **more historical information** than the `control file`
  - `CF` has finite space for records of backup activities.
  - enables you to perform a **recovery that goes back further** in time than the history in the control file.
- Enables you to use RMAN-stored **scripts**
- Enables you to **create customized reports** for all registered targets
  - A **single** `recovery catalog` is able to store information for **multiple** target databases. 一对多
  - the backup and recovery information for all registered targets is contained in one place, allowing you to create customized reports by connecting as the recovery catalog owner and querying the various RC views.
  - Note: `Enterprise Manager Cloud Control` also enables you to view backup information for **multiple** databases **without** the use of a recovery catalog.
- Enables you to use the `KEEP FOREVER` clause of the `BACKUP` command
  - Usage of `KEEP FOREVER` clause can create a backup that is retained for a different period of time from that specified by the configured `retention policy`.
- Allows you to **list** the `data files` and `tablespaces` that are or were in the target database at a given time
  - The `REPORT SCHEMA` command **lists** the tablespaces and data files in the target database.
  - If you add the option of `AT [time |scn|logseq]`, you can see the information at some time in the past.
  - You can use the `AT` option **only** if you are using a recovery catalog.
- Enables you to restore and recover following the **loss** of the `control file` because it preserves RMAN repository **metadata**

Disadvantage of `recovery catalog`

- need to manage and back up **another database**

---

### `Control File` vs `Catalog`

- `Control File`:
  - Default
  - Simpler administration
  - simple backup management requirements
- `recovery catalog`:
  - longer backup retention.
  - when you use RMAN in a Data Guard configuration
  - **Replicates** `control file` data
  - Stores more backup **history**
  - Services **many** targets
  - Stores RMAN **scripts**
  - Provides more **protection** options for **metadata**

---

## Creating a Recovery Catalog

To create a recovery catalog, perform the following three steps:

1. Configure the **database** in which you want to store the recovery catalog.
2. Create the recovery catalog **owner**.
3. Create the **recovery catalog**.

![diagram_recovery_catalog02](./pic/diagram_recovery_catalog02.png)

---

### Configuring the Recovery Catalog Database

- Allocate space for the recovery catalog.

  - Consider:
    - **Number of databases** supported by the recovery catalog
      - amount of **space** required by the recovery catalog schema depends on the number of databases monitored by the catalog.
    - **Number** of `archived redo log files` and **backups recorded**
      - The space increases as the number of archived redo log files and backups for each database increases.
    - Use of RMAN-stored scripts
      - space must be allocated for those scripts.

- Create a `tablespace` for the `recovery catalog`, which will be designated as the **default** tablespace for the **recovery catalog owner**.

```sql
-- request 15 MB for each database registered in the recovery catalog.
CREATE TABLESPACE rcat_ts DATAFILE <data file name> SIZE 15M;
```

---

### Creating the Recovery Catalog Owner

- Create the recovery catalog **owner**.
  - user as the recovery catalog owner
  - Set the default `tablespace` for this user to the tablespace you created for the recovery catalog.
  - provide `UNLIMITED` **quota** on this tablespace for the user.
- Grant the `RECOVERY_CATALOG_OWNER` **role**.
  - `RECOVERY_CATALOG_OWNER` role:
    - provides privileges for the owner of the recovery catalog.
    - includes:
      - `CREATE SESSION`
      - `ALTER SESSION`
      - `CREATE CLUSTER`
      - `CREATE DATABASE LINK`
      - `CREATE PROCEDURE`
      - `CREATE SEQUENCE`
      - `CREATE SYNONYM`
      - `CREATE TRIGGER`
      - `CREATE TYPE`
      - `CREATE TABLE`
      - `CREATE VIEW`

```sql
CREATE USER rcowner IDENTIFIED BY rcpass
TEMPORARY TABLESPACE temp
DEFAULT TABLESPACE rcat_ts
QUOTA UNLIMITED ON rcat_ts;

GRANT recovery_catalog_owner TO rcowner;
```

---

### Creating the Recovery Catalog

- After creating the catalog owner, use the RMAN `CREATE CATALOG` command to **create the catalog tables** in the **default** `tablespace` of the `catalog owner`.

Note: As with any database, if the `ORACLE_SID` environment variable is set to the `SID` for the `recovery catalog database`, there is no need to supply the service name in the `CONNECT` statement.

```sql
-- Connect to the recovery catalog database as the catalog owner:
-- rman
CONNECT CATALOG username/password@net_service_name

-- Execute the CREATE CATALOG command:
CREATE CATALOG;
```

---

## Lab: Create a Recovery Catalog

- In this lab, it should use a differenct database instance that has a different ORACLE_SID, as the recovery catalog.
  - to make it simple, this lab uses only one database instance but different pdb.

```sql
-- create a pdb as a rcat
CREATE PLUGGABLE DATABASE rcat
  ADMIN USER rcatadmin IDENTIFIED BY welcome
  ROLES = (dba)
  DEFAULT TABLESPACE users
  DATAFILE '/u01/app/oracle/oradata/ORCL/RCAT/users01.dbf'
  SIZE 250M
  AUTOEXTEND ON
  FILE_NAME_CONVERT = ('/u01/app/oracle/oradata/ORCL/pdbseed/',
                       '/u01/app/oracle/oradata/ORCL/RCAT/');

-- update tnsname
```

- create tbsp and user

```sql
-- Connect to rcat
CONNECT sys@rcat as sysdba;

-- Create default tbsp for rcat
CREATE TABLESPACE rcat_ts
DATAFILE '/u01/app/oracle/oradata/ORCL/RCAT/rcat01.dbf'
SIZE 15M
REUSE;

-- create user
CREATE USER rcowner IDENTIFIED BY welcome
DEFAULT TABLESPACE rcat_ts
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON rcat_ts;

-- grant role
GRANT recovery_catalog_owner TO rcowner;
```

- Connect with RMAN

```sql
-- connect with catalog
CONNECT CATALOG rcowner@rcat

-- build catalog
CREATE CATALOG;
```

![lab_recovery_catalog](./pic/lab_recovery_catalog01.png)

---

[TOP](#recovery---catalog)
