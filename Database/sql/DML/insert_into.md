# SQL - Insert Row

[Back](../index.md)

- [SQL - Insert Row](#sql---insert-row)
  - [`INSERT INTO`](#insert-into)
    - [Example](#example)
  - [`INSERT INTO SELECT`](#insert-into-select)

---

## `INSERT INTO`

- Allow to add in rows to a table.

- Syntax

```sql
-- add a row into specific columns
INSERT INTO tb_name (col_1, col_2)
VALUES(value_1, value_2);

-- add multiple rows into specific columns
INSERT INTO tb_name (col_1, col_2)
VALUES(value_1, value_2),
(value_3, value_4);


-- add multiple rows into all columns
-- the value list must match all column
INSERT INTO tb_name
VALUES(value_1, value_2),
(value_3, value_4);
```

- `SERIAL` columns do not need to be provided a value.

---

### Example

```sql
-- insert data into table account
INSERT INTO account (username, password, email, created_on)
VALUES ('Jose', 'passsword', 'jose@mail.com', CURRENT_TIMESTAMP);

-- insert data into table job
INSERT INTO job (job_name)
VALUES  ('Astronaut')
,   ('Student')
,   ('President');

-- insert data into table account_job
INSERT INTO account_job(user_id, job_id, hire_date)
VALUES	(1,1,CURRENT_TIMESTAMP);

-- error code, because it violates the references constraint
-- INSERT INTO account_job(user_id, job_id, hire_date)
-- VALUES	(10,10,CURRENT_TIMESTAMP);
```

---

## `INSERT INTO SELECT`

- Insert values from another table

- Syntax:

```sql
INSERT INTO tb_1 (col_1, col_2)
SELECT col_1, col_2
FROM tb_2
WHERE condition;
```

---

[TOP](#sql---insert-row)
