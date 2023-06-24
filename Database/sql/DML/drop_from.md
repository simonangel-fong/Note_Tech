# SQL - Remove rows

[Back](../index.md)

- [SQL - Remove rows](#sql---remove-rows)
  - [`DELETE FROM`](#delete-from)
    - [Example](#example)

---

## `DELETE FROM`

- remove rows from a table.

```sql
-- remove row based on condition
DELETE FROM tb_name
WHERE condition
RETURNING col_1, col_2;

-- remove all records
DELETE FROM tb_name;


-- DELETE JOIN: remove rows based on another tables
DELETE FROM tb_A
USING tb_B
WHERE tb_A.id = tb_B.id;

```

---

### Example

```sql
DELETE FROM job
WHERE job_name = 'Student'
RETURNING job_id, job_name;
```

---

[TOP](#sql---remove-rows)
