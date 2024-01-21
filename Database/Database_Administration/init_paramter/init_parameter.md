# DBA - Initialization Parameters

[Back](../index.md)

- [DBA - Initialization Parameters](#dba---initialization-parameters)
  - [Initialization Parameter Files](#initialization-parameter-files)
    - [Server parameter file (SPFILE)](#server-parameter-file-spfile)
    - [Text initialization parameter file (PFILE)](#text-initialization-parameter-file-pfile)
  - [Initialization Parameters](#initialization-parameters)
    - [Types of Initialization Parameters](#types-of-initialization-parameters)
    - [Values of paramter](#values-of-paramter)
  - [List parameters](#list-parameters)
    - [`SHOW PARAMETER` Command](#show-parameter-command)
    - [Query views](#query-views)
  - [Modifying Initialization Parameters](#modifying-initialization-parameters)

---

## Initialization Parameter Files

- When you **start** a `database instance`, it **reads** `instance configuration parameters (initialization parameters)` from an `initialization parameter file (parameter file)`.

- On most platforms, parameter files are stored in the `$ORACLE_HOME/dbs` directory by default.

- You can use one of the following **types** of `parameter files` to start your `database instance`:
  - Server parameter file (SPFILE)
  - Text initialization parameter file (PFILE)

---

### Server parameter file (SPFILE)

- `Server parameter file (SPFILE)`:

  - a **binary** file that is **written** to and **read** by the database server. 可读可写
  - **automatically created** for you by Database Configuration Assistant (DBCA) when you create a CDB.
    - It **resides** on the server on which the Oracle instance is running.

- You **can't edit** it manually.
- An `SPFILE` is preferred over a PFILE

  - because you can change initialization parameters with `ALTER SYSTEM` commands in SQL\*Plus, and the **changes persist** when you shut down and start up the `database instance`. 实例可以改变且改变持续.
  - It also provides a basis for **self-tuning** by Oracle Database.

- The default name of the SPFILE, which is automatically sought at startup, is `SPFILE<SID>.ora`.

---

### Text initialization parameter file (PFILE)

- `Text initialization parameter file (PFILE)`:

  - a **text** file containing parameter values in **name/value pairs**, which the database server can read to start the `database instance`. 只读取

- Unlike an SPFILE, the database server **cannot write** to and **alter** a PFILE.

  - Therefore, to change parameter values in a PFILE and make them persist during shutdown and startup, you must **manually edit** the `PFILE` in a text editor and **restart** the `database instance` to refresh the parameter values. 只能手动改变,然后重启才刷新新变量值.

- Sample PFILE:

  - named `init.ora` in the default directory for parameter files.
  - inclued within the installation

- Create a PFILE:

  - use sample file **as a starting point for a PFILE**
  - create a PFILE from the SPFILE.

- To apply:
  - save your PFILE as `init<SID>.ora` in the default directory, the database server will **automatically use** it if an SPFILE is not available.
  - If you save the PFILE under a different name, you'll need to **specify it** during startup.

---

## Initialization Parameters

- Purpose of the Initialization parameters (parameters)

  - set database **limits**,
  - set databasewide **defaults**,
  - specify **files and directories**,
  - and affect **performance**.

- Minimum parameter of a parameter file:
  - The parameter file must, at a **minimum**, specify the `DB_NAME` parameter.
  - All other parameters have **default values**.

---

### Types of Initialization Parameters

- Types

  - basic
  - advanced

- `basic parameters`

  - To get **reasonable performance** from the database, in the majority of cases, you'll need to set and tune only the **30** or so `basic parameters`.
  - An example of a basic parameter is `SGA_TARGET`, which specifies the **total memory size** of **all SGA** components.

- `advanced parameters`

  - In rare situations, you'll need to modify one or more of the **300** or so `advanced parameters` to achieve **optimal performance**.
  - And example of an advanced parameter is `DB_CACHE_SIZE`, which specifies the **size** of the default **buffer pool**.

---

### Values of paramter

- `Derived Parameters`: calculated

  - Some parameters are derived, meaning their **values are calculated from the values** of other parameters.
  - Normally, you shouldn't alter values for derived parameters.

    - For example, the default value of the `SESSIONS` parameter is derived from the value of the `PROCESSES` parameter.

  - But if you do, the value that you specify **overrides** the calculated value.

    - If the value of `PROCESSES` changes, the default value of `SESSIONS` changes as well, unless you override it with a specified value.

- Parameter Values That **Depend on the OS**: OS dependent
  - Some parameter values or value ranges **depend on the host operating system**.
    - For example, the `DB_FILE_MULTIBLOCK_READ_COUNT` parameter specifies the **maximum number of blocks** that are read in one I/O operation during a sequential scan; this parameter is platform dependent.
    - The size of those blocks, which is set by `DB_BLOCK_SIZE`, has a default value that depends on the operating system.

---

## List parameters

- **Query** `V$PARAMETER` for an initialization parameter to learn whether you can make:

  - Session-level changes (`ISSES_MODIFIABLE` column)
  - System-level changes (`ISSYS_MODIFIABLE` column)
  - PDB-level changes (`ISPDB_MODIFIABLE` column)

```sql
SELECT name,value,isses_modifiable,issys_modifiable, ispdb_modifiable
FROM v$parameter
```

- Ways to view paramters:
  - `SHOW PARAMETER` Command
  - query views

---

### `SHOW PARAMETER` Command

- Syntax:

```sql
`SHOW PARAMETER p_name`
```

- Return parameter's **name**, **data type** and **default value**
- Return information about parameters whose names contain the word in the `p_name`.模糊查询

---

### Query views

- Views:

  - `V$PARAMETER`
  - `V$PARAMETER2`
  - `V$SPPARAMETER`
  - `V$SYSTEM_PARAMETER`
  - `V$SYSTEM_PARAMETER2`

- Example:

```sql
SELECT name, default_value FROM v$parameter
WHERE name = 'allow_global_dblinks';
```

---

## Modifying Initialization Parameters

- Tools to modify

  - Use `EM Express`
  - `SQL\*Plus` (`ALTER SESSION` or `ALTER SYSTEM`).

- Limitation:

  - **Increasing the values** of parameters may **improve** your system’s **performance**, but increasing most parameters **also increases the SGA size**.

    - A larger SGA can **improve** database performance up to a point.
    - An SGA that is **too large** can **degrade** performance if it is swapped in and out of memory.
    - You should set **operating system parameters** that control `virtual memory` working areas with the SGA size in mind. The **operating system configuration** can also **limit** the maximum size of the SGA.

- Whether is modifiable:

  - The `ISSES_MODIFIABLE` column value tells you whether you **can change** the parameter for your **current session** (`TRUE`) or not (`FALSE`) by using the `ALTER SESSION` command.

```sql
SELECT name,value,isses_modifiable,issys_modifiable
FROM v$parameter
```

- `SCOPE` clause within the `ALTER SYSTEM` command:

  - tell the system **where to update** the **system-level parameter**
    - `MEMORY`
    - `SPFILE`
    - `BOTH`

```sql
ALTER SYSTEM SET
p_name=p_value
SCOPE=SPFILE;
```

- Use the `DEFERRED` keyword to set or modify the value of the parameter **for future sessions** that connect to the database.

```sql
ALTER SYSTEM SET
parameter_name = value
DEFERRED
```

- You can change some parameters **at the session level**, but not all.
- Changes are applied to your current session immediately (dynamically) and expire when you end your session.
- Parameters with a value of TRUE are referred to as session-level parameters.
  - Example: `SQL> ALTER SESSION SET NLS_DATE_FORMAT ='mon dd yyyy'`;

---

[TOP](#dba---initialization-parameters)
