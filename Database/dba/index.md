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

- Oracle Database Architecture

- [Database Instance](./instance/instance/instance.md)
  - [Startup](./instance/startup/startup.md)
    - [Lab: Startup](./instance/startup/lab.md)
  - [Shutdown](./instance/shutdown/shutdown.md)
    - [Lab: Shutdown mode](./instance/shutdown/lab.md)

- Memory
  - [System Global Area (SGA)](./memory/sga/sga.md)



---

- control file

```sql
SELECT name FROM v$controlfile;
SELECT is_recovery_dest_file FROM v$controlfile;
SELECT block_size FROM v$controlfile;
SELECT file_size_blks FROM v$controlfile;
SELECT con_id FROM v$controlfile;
SELECT name, block_size, file_size_blks FROM v$controlfile;
```


---

[TOP](#oracle-database-administration-workshop)
