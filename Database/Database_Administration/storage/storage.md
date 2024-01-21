# DBA - Storage

[Back](../index.md)

- [DBA - Storage](#dba---storage)
  - [Database Storage Architecture](#database-storage-architecture)
  - [Oracle Managed Files](#oracle-managed-files)

---

## Database Storage Architecture

- The files that **comprise an Oracle database** are as follows:

  - `Control files`:

    - Each **database** has **one unique** `control file` that contains **data about the database** itself (that is, **physical database structure information**).
    - **Multiple copies** may be maintained to protect against total loss.
    - It can also contain **metadata related to backups**.
    - The control file is critical to the database.
      - **Without** the control file, the database **cannot be opened**.

  - A control file is a small binary file that records the physical structure of the database and includes:

    - The **database name**
    - Names and locations of associated **datafiles** and online **redo log files**
    - The **timestamp** of the database **creation**
    - The current **log sequence number**
    - **Checkpoint** information

  - `Data files`: `.dbf`

    - They contain the **user or application data** of the database, as well as **metadata** and the **data dictionary**.
    - A `tbspace` cannot exist without data file
      - Must have at least one data file.

  - `Online redo log files`:

    - They allow for **instance recovery** of the database.
    - If the database server crashes and does not lose any data files, the instance can recover the database with the information in these files.

- The following additional files are used during the operation of the database:

  - `Initialization parameter file`:

    - Is used to define h**ow the instance is configured** when it starts up

  - `Password file`:

    - Allows users using the `SYSDBA`, `SYSOPER`, `SYSBACKUP`, `SYSDG`, `SYSKM`, and `SYSASM` roles to **connect** remotely to the instance and perform administrative tasks

  - `Backup files`:
    - Are used for database recovery.
    - You typically restore a backup file when a media failure or user error has damaged or deleted the original file.

---

## Oracle Managed Files

- `Oracle Managed Files (OMF)`

  - **eliminates** the need for you to **directly** manage the operating system files in an Oracle database. - specify operations in terms of **database objects** rather than file names.

- The database internally uses standard file system interfaces to create and delete files as needed for the following database structures:

  - Tablespaces
  - Redo log files
  - Control files
  - Archived logs
  - Block change tracking files
  - Flashback logs
  - RMAN backups

- A database can have a **mixture** of Oracle-managed and Oracle-unmanaged files.

  - The **file system directory** specified by either of these parameters must already exist; the database does not create it. 文件夹先存在
  - The directory must also have **permissions** for the database to create the files in it. 文件夹有权限

- In Oracle Database `Cloud Service`, `OMF` is enabled by **default**

---

[TOP](#dba---storage)
