# DBA - Physical Storage Architecture: Data File

[Back](../../index.md)

- [DBA - Physical Storage Architecture: Data File](#dba---physical-storage-architecture-data-file)
  - [Data File](#data-file)
  - [Use of Data Files](#use-of-data-files)
  - [Permanent and Temporary Data Files](#permanent-and-temporary-data-files)
  - [Online and Offline Data Files](#online-and-offline-data-files)
  - [Data File Structure](#data-file-structure)
  - [Lab: Query Data file using Dictionary](#lab-query-data-file-using-dictionary)
  - [Lab: Query temp file](#lab-query-temp-file)

---

## Data File

- `data files`:
  - the structure where the data is stored.
  - Every Oracle database **must have at least one** data file.

---

## Use of Data Files

- Oracle Database **physically stores `tablespace` data** in `data files`. 存储表空间数据.

- Each `nonpartitioned schema object` and each `partition` of an object is stored in its own `segment`, which belongs to only one `tablespace`.

  - For example, the data for a **nonpartitioned table** is stored in a **single** `segment`.
  - `Segment` is stored in one `tablespace`.
  - 即 schema object 对应一个 segment; segment 对应唯一的 tbsp

- `TBSP` vs `data file`
  - Each `tablespace` consists of one or more `data files`. 一个 tbsp 对应一个或多个 df
  - The **data** for a database is collectively stored in the `data files` located in each tablespace of the database. 数据在 df 中.
  - A `segment` can span one or more `data files`, but it **cannot span multiple** `tablespaces`. segment 可以跨 df, 但不能跨 tbsp.
  - A database must have the `SYSTEM` and `SYSAUX` tablespaces.
    - Oracle Database automatically **allocates the first** `data files` of any database for the `SYSTEM` tablespace **during database creation**.创建时, 先创建 SYSTEM tbsp 的 df.
    - The `SYSTEM` tablespace contains the `data dictionary`, a set of tables that contains database metadata.
    - Typically, a database also has an `undo tablespace` and a `temporary tablespace` (usually named `TEMP`).

![df_vs_tbsp_diagram](./pic/df_vs_tbsp_diagram.png)

> - One tbsp
> - 2 DF: 一个 tbsp 可以多个 DF
> - segment:
>   - index 和 table 都是对象, 对应相应的 segment
>   - segment 可以跨 df
>   - segment 在一个 tbsp 之下.

---

## Permanent and Temporary Data Files

- Permanent Data Files

  - files designed to store objects(**persistent** `schema objects`) in **permanent** `tablespaces`.
  - 与 permanent tbsp 关联

- Temporary Data Files

  - files designed to store data in hash, sort, and other operations to manage **temporary** `tablespaces`
    - A **temporary** `tablespace` contains schema objects **only for the duration of a session**.
    - also **store result set data** when **insufficient space exists in memory**.

- `Temp files` vs `permanent data files`

  - **Permanent** database objects such as tables are **never stored** in `temp files`.
  - Temp files are always set to `NOLOGGING` mode
    - never have `redo` generated for them.
    - Media recovery **does not recognize** `temp files`.
  - **cannot** make a temp file **read-only**.
  - **cannot create** a temp file with the `ALTER DATABASE` statement.
  - When you create or resize temp files, they **are not always guaranteed allocation of disk space** for the file size specified.
    - On file systems such as Linux and UNIX, temp files are created as sparse files. In this case, disk blocks are allocated not at file creation or resizing, but as the blocks are accessed for the first time.

- Views:

|                          | TEMP             | Permenant        |
| ------------------------ | ---------------- | ---------------- |
| dynamic performance view | `V$TEMPFILE`     | `V$DATAFILE`     |
| data dictionary view     | `DBA_TEMP_FILES` | `DBA_DATA_FILES` |

- 永久归永久
- 暂时:
  - 不能存永久对象
  - 不能只读
  - 不使用 alter db 语句创建
  - nolog: 没有 redo;恢复时无法识别
  - 不保证使用磁盘空间.

---

## Online and Offline Data Files

- Every `data file` is either **online (available)** or **offline (unavailable)**.

- The database **cannot access** `offline data files` until they are brought online.离线 df 不能访问

  - can alter the availability of individual data files or temp files by taking them offline or bringing them online.可以改变状态.

- The database takes a data file offline **automatically** if the database **cannot write to it**.

- Reason to be taken offline:

  - perform offline backups
  - block corruption

- TBSP: offline/online

  - When a data file is taken offline in an online tablespace, the tablespace itself remains online. 其中一个 df 离线, 不影响 tbsp 在线状态
  - can make **all** `data files` of a tablespace temporarily unavailable by taking the `tablespace` itself offline. tbsp 离线, 全部 df 离线.

- Move df:
  - statement: `ALTER DATABASE MOVE DATAFILE`
  - can move an online data file from one physical file to another while the database is open and accessing the file.可以在打开并连线时移动.
  - purpose:
    - Move a tablespace **from one kind of storage to another**
    - Move data files that are **accessed infrequently** to lower cost storage
    - Make a tablespace **read-only** and move its data files to **write-once** storage, such as a `write once read many (WORM)` drive
    - Move a database into Oracle `ASM`

---

## Data File Structure

- `data file header`

  - contains **metadata** about the `data file`
    - e.g., its size and checkpoint SCN.
  - Each header contains
    - **an absolute file number**, which uniquely identifies the data file **within the database**,
    - **a relative file number**, which uniquely identifies a data file **within a tablespace.**
  - 绝对文件号: 在数据库中分别文件; 相对: 在 tbsp 中分别文件.

- creation of a data file for a tablespace

  - allocat the specified amount of **disk space** plus the **overhead** for the `data file header`.
  - the allocated disk space is formatted but contains **no** `user data`.
  - **reserves** the space to hold the data for future `segments` of the associated tablespace.

- As the data grows in a tablespace:

  - Oracle Database uses the free space in the data files to allocate `extents` for the `segment`.

- types of space in a data file:
  - `Extents` are
    - either **used**, which means they **contain segment data**,
    - or **free**, which means they are **available** for reuse.
  - `fragmented free space`
    - empty space that individually are not large enough to be reused for new data
    - Over time, updates and deletions of objects within a tablespace can create `fragmented free space`.

![space_in_df](./pic/space_in_df.png)

---

## Lab: Query Data file using Dictionary

- Connect to root
- open pdb

```sql

-- query the data files
/*
contains the actual users data, applications data, metadata.
( Tables, Rows, indexes ,procedures, views�)
If you lose Datafiles, you lose your database.
*/

show con_name;

select name,open_mode,con_id from v$pdbs;

--make sure pluggable is open
alter pluggable database orclpdb open;
```

- Query all data files using dictionary

```sql
select file_name,file_id,tablespace_name,con_id
from cdb_data_files;
```

![lab0101](./pic/lab0101.png)

![lab0101](./pic/lab0104.png)

---

- Query all data files using v$view
  - return includes the data files of seed pdb.

```sql
select file#,name, ts#,con_id
from V$DATAFILE
order by con_id;
```

![lab0101](./pic/lab0105.png)

---

- close pdb
- query using `cdb_`
  - return only the root data files, because `cdb_` only return openned database.

```sql
alter pluggable database orclpdb close;
select file_name,file_id,tablespace_name,con_id
from cdb_data_files
```

![lab0101](./pic/lab0106.png)

- Query using v$datafile.
  - return all data files, even if the database is closed.

```sql
select file#, name, ts#, con_id
from V$DATAFILE
order by con_id;
```

![lab0101](./pic/lab0107.png)

---

- Query using dba, only return the data file in the current container, which is cdb.

```sql
--same query but using dba , but here we dont have  con_id

select file_name,file_id,tablespace_name
from dba_data_files
```

![lab0101](./pic/lab0102.png)

---

- Change session to a pdb
- Query using dba, only return the data file in the current container, which is pdb.

```sql
--now let do
alter session set container=orclpdb

show con_name

select file_name,file_id,tablespace_name
from dba_data_files

```

![lab0101](./pic/lab0103.png)

---

- Close the pdb
- Query using `dba_`
  - return error, because `dba_` only return the opened pdb.

```sql
select file_name,file_id,tablespace_name
from dba_data_files;
```

![lab0101](./pic/lab0108.png)

- Query using v$ view
  - can return even the pdb is closed.
  - only return the pdb data files.

```sql
select file#,name, ts#,con_id
from V$DATAFILE
order by con_id;
```

![lab0101](./pic/lab0109.png)

---

---

## Lab: Query temp file

- A tempfile is a file that is part of an Oracle database.
  Tempfiles are used with TEMPORARY TABLESPACES

- Temporary tablespaces are used for special operations, particularly for sorting data results on disk and for hash joins in SQL. For SQL with millions of rows returned, the sort operation is too large for the RAM area and must occur on disk. The temporary tablespace is where this takes place

---

- Connect with root container
- open pdb

```sql
show con_name;
select name,open_mode,con_id from v$pdbs;

--make sure pluggable is open
alter pluggable database orclpdb open

```

- Query temp file both in root and pdbs using `cdb_`

```sql
select file_name,file_id,tablespace_name,con_id
from cdb_temp_files;
```

![lab0201](./pic/lab0201.png)

![lab02](./pic/lab0204.png)

---

- Query temp file only in root, using `dba_`

```sql
select file_name,file_id,tablespace_name
from dba_temp_files
```

![lab02](./pic/lab0202.png)

---

- Change session to a pdb
- Query the temp file only in pdb using `dba_`

```sql
alter session set container=orclpdb

show con_name

select file_name,file_id,tablespace_name
from dba_temp_files
```

![lab02](./pic/lab0203.png)

---

[TOP](#dba---physical-storage-architecture-data-file)
