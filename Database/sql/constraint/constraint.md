# SQL - Constraint

[Back](../index.md)

- [SQL - Constraint](#sql---constraint)
  - [Constraint](#constraint)
  - [Primary Key: `SERIAL`](#primary-key-serial)
  - [Foreign Key: `REERENCES`](#foreign-key-reerences)
  - [`NOT NULL`](#not-null)
  - [`UNIQUE`](#unique)
  - [`CHECK`](#check)
  - [`EXCLUSION`](#exclusion)

---

## Constraint

- `Constraint`

  - the rules enfored on data columns on table.
  - used to prevent invalid data from being entered into the database, ensuring the accuracy and reliability of the data in the database.

- Type of constraints

  - `Column Constraints`: constrains the data in a column to adhere to certain conditions.

    - primary key
    - foregn key
    - Not null
    - unique
    - check
    - EXCLUSION

  - `Table Constraints`: applied to the entire table rather than to an individual column.
    - check
    - references

---

## Primary Key: `SERIAL`

- `Primary Key`

  - a column or a group of columns to identify a row **uniquely** in a table.

- `SERIAL`

  - In PostgreSQL, a sequence is a special kind of database object that generates a **sequence of integers**.
  - A sequence is often used as the primary key column in a table.

- Syntax:

```sql
CREATE TABLE tb_name(
  tb_id   SERIAL    PRIMARY KEY
);
```

---

## Foreign Key: `REERENCES`

- `Foreign Key`

  - a column or a group of columns in a table that **uniquely** identify a row **in another table**.
  - defined in a table that references to the primary key of the other table.
  - A table can have multiple foreign keys depending on its relationships with other tables.

- `Referencing table / Child table`

  - the table that contains the foreign key.

- `Referenced table / Parent table`

  - the table to which the foreign key references.

- `REERENCES`

  - Constrain the value stored in the column that must exist in a column in another table.

- Syntax:

```sql
CREATE TABLE tb_name(
  tb_id   SERIAL    PRIMARY KEY,
  f_key   INTEGER   REFERENCES ref_tb_name(pk_col)
);
```

---

## `NOT NULL`

- Ensure that all values

- Syntax:

```sql
CREATE TABLE tb_name(
  col_name    DATATYPE    NOT NULL
);
```

---

## `UNIQUE`

- Ensure that all values in a column are different.

- Syntax:

```sql
CREATE TABLE tb_name(
  col_name    DATATYPE    UNIQUE
);
```

---

## `CHECK`

- Ensure that all values in a column satify certain conditions.

- Allow to create more customized constraints that adhere to a certain condition.

- Syntax:

```sql
CREATE TABLE tb_name(
	col_name datatype CHECK(col_name > num)
)
```

---

## `EXCLUSION`

- Ensure that if any two rows are compared on the specified column or exmpression using the specified operator, not all of these comparisions will return TRUE.

---

[TOP](#sql---constraint)
