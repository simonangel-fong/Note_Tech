# Oracle Database Administration Workshop

[All Note](../../index.md)

---

- Exame:

  - [Oracle Database Administration I Exam Number: 1Z0-082](https://education.oracle.com/oracle-database-administration-i/pexam_1Z0-082)

- Online Course:
  - Udemy: [Oracle Database Administration Workshop ( 12c and Higher)](https://www.udemy.com/course/oracle-database-administration-certified-associate-1z0-072/)

---

## Catelog

- [Intro](./intro/itro.md)
- [Local Virtual Machine](./local_vm/vm.md)

- [Net Services Architecture](./net/net/net.md)

  - [Listener](./net/listener/listener.md)
  - [TNS Name](./net/tnsname/tnsname.md)
  - [Login `SQLP\*LUS`](./net/EZCONNECT/EZCONNECT.md)

- Oracle Database Architecture

- [Database Instance](./instance/instance/instance.md)

  - [Startup](./instance/startup/startup.md)
    - [Lab: Startup](./instance/startup/lab.md)
  - [Shutdown](./instance/shutdown/shutdown.md)
    - [Lab: Shutdown mode](./instance/shutdown/lab.md)

- [Memory Structures](./memory/memory/memory.md)

  - [System Global Area (SGA)](./memory/sga/sga.md)
    - [Database Buffer Cache](./memory/buffer_cache/buffer_cache.md)
    - [Redo Log Buffer](./memory/redo_log_buffer/redo_log_buffer.md)
    - [Shared Pool](./memory/shared_pool/shared_pool.md)
    - [Large Pool](./memory/large_pool/large_pool.md)
    - [Java Pool](./memory/java_pool/java_pool.md)
    - [Fixed SGA](./memory/fixed_sga/fixed_sga.md)
  - [Program Global Area (PGA)](./memory/pga/pga.md)
  - [User Global Area (UGA)](./memory/uga/uga.md)

- [Process Architecture](./process/process/process.md)

  - [Client Processes](./process/client_processes/client_processes.md)
  - [Server Processes](./process/server_processes/server_processes.md)
  - [Background Processes](./process/bg_processes/bg_processes.md)
  - [Slave Processes](./process/slave_processes/slave_processes.md)

- Storage Structures

  - [Physical Storage Structures](./phy_storage/phy_storage/phy_storage.md)
    - [Data File](./phy_storage/data_file/data_file.md)
    - [Control File](./phy_storage/control_file/control_file.md)
    - [Online Redo Log](./phy_storage/online_redo_log/online_redo_log.md)
  - [Logical Storage Structures](./log_storage/log_storage/log_storage.md)
    - Data Blocks
    - Extents
    - Segments
    - Tablespaces

- [Pluggable Database](./pluggable_db/pluggable_db/pluggable_db.md)
- User Management

  - [Alter user](./user/user/user.md)

- [Miscellaneous](./misc/misc.md)

---

- DBA2
  - [Backup](./backup/backup/backup.md)

---

```sql
SELECT name FROM v$controlfile;
SELECT is_recovery_dest_file FROM v$controlfile;
SELECT block_size FROM v$controlfile;
SELECT file_size_blks FROM v$controlfile;
SELECT con_id FROM v$controlfile;
SELECT name, block_size, file_size_blks FROM v$controlfile;
```

---

## Lab: get the database name

- Command to return database name
  - Method 01:
    - check the tnsname.ora
  - Method 02:
    - Return the processes name to which Oracle listens.

```sh
# check for the presence of Oracle System Monitor (SMON) processes.
# ps -ef: Lists information about all currently running processes in a detailed format.
# grep smon: Searches for lines containing the string "smon" in the output
# grep -v grep:  ensures that the grep process used for searching is not included in the results.
ps -ef | grep smon
ps -ef | grep smon | grep -v grep
```

---

[TOP](#oracle-database-administration-workshop)
