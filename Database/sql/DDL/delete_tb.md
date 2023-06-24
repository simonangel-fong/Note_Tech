# SQL - DELETE TABLE

[Back](../index.md)

- [SQL - DELETE TABLE](#sql---delete-table)
  - [DROP TABLE (To Recyclebin)](#drop-table-to-recyclebin)

---

## DROP TABLE (To Recyclebin)

To remove a table from database.

- Syntax:

```sql

-- remove a given table to recyclebin
DROP TABLE tablename;

```

- Always exercise caution when deleting especially when it is a table.

- In addition, any index that has been created based on the table is also dropped.

- Any dropped table was permanently removed, and could only be recovered from backup.

---

[TOP](#sql---delete-table)
