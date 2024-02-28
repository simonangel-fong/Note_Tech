# DBA - Physical Storage Architecture: Control File

[Back](../../index.md)

- [DBA - Physical Storage Architecture: Control File](#dba---physical-storage-architecture-control-file)
  - [Control File](#control-file)
  - [Use of Control Files](#use-of-control-files)
  - [Multiple Control Files](#multiple-control-files)
  - [Control File Structure](#control-file-structure)

---

## Control File

- The database `control file`:
  - is a small **binary file** associated with **only one database**.
  - Each database has one unique control file, although multiple identical copies are permitted. 虽然可以有多份, 但一一对应.

## Use of Control Files

- `control file`

  - used to to **locate** `database files` and to **manage the state** of the database generally.

- `control file` **contains**:

  - The `database name` and `database unique identifier (DBID)`
  - The time stamp of database **creation**
  - Information about `data files`, `online redo log files`, and `archived redo log files`
  - `Tablespace` information
  - `RMAN` backups

- **purposes:**

  - It contains information required **to open the database**.
  - The control file **tracks structural changes** to the database.
    - e.g., when an administrator adds, renames, or drops a data file or online redo log file, the database **updates** the `control file` to reflect this change.
  - It contains `metadata` that must be accessible **when the database is not open**.
    - e.g., information required **to recover the database**, including `checkpoints`. A checkpoint indicates the `SCN` in the redo stream where instance recovery would be required to begin. Every committed change before a checkpoint SCN is guaranteed to be saved on disk in the data files. At least every three seconds the checkpoint process records information in the control file about the checkpoint position in the online redo log.

- Oracle Database reads and writes to the control file continuously during database use and **must be available for writing whenever the database is open**.
  - e.g., **recover** a database involves reading from the control file the names of all the data files contained in the database.
  - e.g., Other operations, such as **adding** a data file, **update** the information stored in the control file.

---

## Multiple Control Files

- Oracle Database **enables multiple, identical** `control files` to be open **concurrently** and written to the same database.

  - By multiplexing a control file on different disks, the database can achieve **redundancy** and thereby **avoid a single point of failure**.

- If a `control file` **becomes unusable**, then the database `instance` **fails** when it attempts to access the damaged control file.

  - When other current control file copies **exist**, then you can **remount** the database and open it **without media recovery**.

- If **all** `control files` of a database are **lost**, however, then the database `instance` **fails** and `media recovery` is **required**.
  - Media recovery is not straightforward if an older backup of a control file must be used because a current copy is not available.

---

## Control File Structure

- `section` of Control File:

  - Each section is a set of records about an aspect of the database.
    - e.g., one section in the control file tracks data files and contains a set of records, one for each data file.
  - Each section is stored in **multiple logical control file blocks**.
  - Records can **span** blocks within a `section`.

- types of records:

  - `Circular reuse records`

    - contains noncritical information that is **eligible to be overwritten** if needed.
    - When all available record slots are **full**, the database either **expands** the control file to make room for a new record or **overwrites** the oldest record.
    - e.g., records about `archived redo log` files and `RMAN backups`.

  - `Noncircular reuse records`
    - contains critical information that **does not change often** and **cannot be overwritten**.
      - e.g., include `tablespaces`, `data files`, `online redo log files`, and `redo threads`. Oracle Database never reuses these records unless the corresponding object is dropped from the tablespace.

- **only** the database can modify the information in the control file.

- Reading and writing the `control file blocks` is **different** from reading and writing `data blocks`.

  - For the control file, Oracle Database **reads and writes directly** from the disk to the `program global area (PGA)`.
  - Each process allocates a certain amount of its **PGA memory** for control file blocks.

- Views:`V$DATABASE`

  - to view the information stored in the control file

---

[TOP](#dba---physical-storage-architecture-control-file)
