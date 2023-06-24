# SQL - Modify Table

[Back](../index.md)

- [SQL - Modify Table](#sql---modify-table)
  - [`ALTER TABLE`](#alter-table)
  - [Rename a table](#rename-a-table)
  - [Change Column](#change-column)
  - [Change Constraint](#change-constraint)
    - [Example](#example)

---

## `ALTER TABLE`

- Allow for changes to an existing table structure:

  - adding, droping, or renaming columns
  - change a column's data type
  - Set DEFAULT values for a column
  - Add CHECK constraints
  - Rename table

---

## Rename a table

- Syntax:

```sql
-- rename a table
ALTER TABLE tb_name
RENAME TO new_tb_name;

```

---

## Change Column

```sql
-- rename a column
ALTER TABLE tb_name
RENAME COLUMN old_col_name TO new_col_name;

-- Adding Columns
ALTER TABLE tb_name
ADD COLUMN new_col_name datetype;

-- drop single column
ALTER TABLE tb_anem
DROP COLUMN col_name;

-- drop multipl column
ALTER TABLE tb_anem
DROP COLUMN col_1
DROP COLUMN col_2;

-- remove all dependencies
ALTER TABLE tb_name
DROP COLUMN col_name CASCADE;

-- check existence before dropping
ALTER TABLE tb_name
DROP COLUMN IF EXISTS col_name;
```

- `DROP COLUMN`

  - Allow for complete removal of a column in a table.

  - In PostgreSQL, this will also automatically remove all of its indexes and constraints involving the column.

  - However, it will not remove columns used in views, triggers, or stored procedures without the additional CASCADE clause.

---

## Change Constraint

```sql
-- add constraints
ALTER TABLE tb_name
ALTER COLUMN col_name
ADD CONSTRAINT constraint_name;

-- set default
ALTER TABLE tb_name
ALTER COLUMN col_name
SET DEFAULT value

-- drop default
ALTER TABLE tb_name
ALTER COLUMN col_name
DROP DEFAULT;

-- set Not null
ALTER TABLE tb_name
ALTER COLUMN col_name
SET NOT NULL;

-- drop Not null
ALTER TABLE tb_name
ALTER COLUMN col_name
DROP NOT NULL;


```

---

### Example

```sql
CREATE TABLE information(
	info_id	SERIAL PRIMARY KEY,
	title	VARCHAR(500)	NOT NULL,
	person	VARCHAR(50)		NOT NULL UNIQUE
)

-- rename table
ALTER TABLE information
RENAME TO new_info;

-- rename a column
ALTER TABLE new_info
RENAME COLUMN person TO people;

-- drop column
ALTER TABLE new_info
DROP COLUMN IF EXISTS people;
```

---

[TOP](#sql---modify-table)
