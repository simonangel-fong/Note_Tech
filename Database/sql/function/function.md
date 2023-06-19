# SQL - Function

[Back](../index.md)

- [SQL - Function](#sql---function)
  - [Aggregate Functions](#aggregate-functions)
  - [`COUNT()`](#count)

---

## Aggregate Functions

- `Aggregate Functions`

  - Aggregate functions compute **a single result** from a **set of input values**.
  - only applied to `SELECT` clause or `HAVING` clause.

- Common Aggregate Functions
  - `AVG()`: average value
  - `COUNT()`: number of values
  - `MAX()`: maximum value
  - `MIN()`: minimum value
  - `SUM()`: sum of all values

---

## `COUNT()`

- `COUNT` function returns the number of input rows that match a specific condition of a query.

```sql
# return number of all rows in a table.
SELECT COUNT(*) FROM tb_name;

# return number of rows in a column.
SELECT COUNT(col_name) FROM tb_name;

# return number of unique values in a column.
SELECT COUNT(DISTINCT(col_name)) FROM tb_name;

```

---

[TOP](#sql---function)
