# Revovery - File Loss

[Back](../../index.md)

- [Revovery - File Loss](#revovery---file-loss)
  - [File Loss](#file-loss)

---

## File Loss

- File loss can be caused by:

  - **User error**
    - An administrator may inadvertently delete or copy over a necessary file.
  - **Application error**
    - An application or script can also have a logic error in it, as it processes database files, resulting in a lost or damaged file.
  - **Media failure**
    - A **disk drive or controller may fail** fully or partially and introduce corruption into files or even cause a total loss of files.

- `noncritical file`:

  - one that the database and most applications **can operate without**.
  - e.g., if the database loses one multiplexed redo log file, there are still other redo log file copies that can be used to keep the database open and available.

- **loss** of a `noncritical file`

  - does **not** cause the database to **crash**
  - but can **impair** the functioning of the database
  - e.g.,
    - The **loss of an index tablespace** can cause applications and queries to **run much slower**, or even make the application **unusable**, if the indexes were used to enforce constraints.
    - The **loss of an online** redo log group, as long as it is not the current online log group, can
      cause database operations to be **suspended** until new log files are generated.

- **loss** of a `noncritical file` can be addressed by:
  - **Creating** a **new** file
  - **Rebuilding** the file
  - **Recovering** the lost or damaged file

---

[TOP](#revovery---file-loss)
