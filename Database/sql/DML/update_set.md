# SQL - Update Row

[Back](../index.md)

- [SQL - Update Row](#sql---update-row)
  - [`UPDATE SET`](#update-set)
    - [Example](#example)

---

## `UPDATE SET`

- Allow to change of values of the columns in a table.

- Syntax:

```sql
-- update records based on the condition
UPDATE tb_name
SET col_1 = val_1
    col_2 = val_2
WHERE condition;

-- update records based on another column
UPDATE tb_name
SET col_1 = col_2
WHERE condition;

-- update all records in a table
UPDATE tb_name
SET col_1 = val_1
    col_2 = val_2;

-- update record using another table's values.
UPDATE tb_A
SET tb_A.col = tb_B.col
FROM tb_B
WHERE tb_A.id = tb_B.id;

-- return affected rows
UPDATE tb_name
SET col_1 = val
RETURNING col_1, col_2
```

---

### Example

```sql
--
UPDATE account
SET last_login = CURRENT_TIMESTAMP
WHERE username = 'Jose'
RETURNING user_id, username, last_login;

-- update records based on created_on column
UPDATE account
SET last_login = created_on
WHERE username = 'Jose'
RETURNING user_id, username, last_login

-- UPDATE JOIN: update record using another values in another table
UPDATE account_job
SET hire_date = account.created_on
FROM account
WHERE account_job.user_id = account.user_id;
```

---

[TOP](#sql---update-row)
