# DBA - P file

[Back](../index.md)

---

- Usually use this command to create parameter file as a backup, which is the same as the parameter file for a database

```sql
CREATE pfile FROM spfile;
```

- Location of spfile

```sh
cd $ORACLE_HOME/dbs
ls
# db file: a binary file used for database.
# spileORL.ora
cat initORCL.ora
```

---

[TOP](#dba---p-file)
