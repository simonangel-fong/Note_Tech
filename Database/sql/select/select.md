# SQL - Select Statement

[Back](../index.md)

- [SQL - Select Statement](#sql---select-statement)
  - [Select Statement: Query Data](#select-statement-query-data)
    - [Good Practice](#good-practice)
  - [`SELECT DISTINCT`: Return unique data](#select-distinct-return-unique-data)
  - [`SELECT WHERE`: Filter returned rows](#select-where-filter-returned-rows)
    - [Comparison Operators](#comparison-operators)
    - [Logical Operators](#logical-operators)
    - [`BETWEEN` Operator](#between-operator)
    - [`IN` Operator](#in-operator)
    - [`LIKE` and `ILIKE` Opeartor](#like-and-ilike-opeartor)
  - [`ORDER BY`: Sort Rows](#order-by-sort-rows)
  - [`LIMIT`: Limits number of returned rows](#limit-limits-number-of-returned-rows)

---

## Select Statement: Query Data

- Syntax:

```sql
SELECT column_name FROM table_name;     # query a column
SELECT col1, col2 FROM table_name;      # query columns
SELECT * FROM table_name;               # query all columns


```

---

### Good Practice

- Do your best to query only the needed columns.
- It is **not good practice to use asterisk(\*)** in the SELECT statement,
  - since it will automatically query everything, which increases traffic between the database server and the application, slowing down the retrielval of results.

---

## `SELECT DISTINCT`: Return unique data

- The `DISTINCT` keyword can be used to return only the **unique values in a column**.

- Syntax:

```sql
SELECT DISTINCT col_name FROM tb_name;

# use parethesis to clarify the column to which the DISTINCT is being applied.
SELECT DISTINCT(col_name)  FROM tb_name;
```

---

## `SELECT WHERE`: Filter returned rows

- `WHERE` statement
  - specifies conditions on columns for the rows to be returned.
  - The conditions are used to filter the rows returned from the `SELECT` statement.

```sql
SELECT col FROM tb_name WHERE conditions;
```

### Comparison Operators

---

### Logical Operators

- To combine multiple comparison operators

---

### `BETWEEN` Operator

- `BETWEEN` Operator

  - can be used to match a value against a range of values.
  - value `BETWEEN` low `AND` high
  - same as `value >= low AND value <= high`
  - the value is **inclusive**.

- Can combine `BETWEEN` with the `NOT`

  - `NOT BETWEEN low AND high`
  - same as `value < low AND value > high`

- Can work with date:
  - `BETWEEN YYYY-MM-DD AND YYYY-MM-DD`
  - Date also include timestamp information.
    - a datetime starts at `0:00`
    - 因为是 inclusive, 所以处理日期时需要注意是否包含.

---

### `IN` Operator

- `IN` Operator

  - checks whether a value is included in a list of multiple options.

- Syntax:

```sql
SELECT col
FROM tb
WHERE col IN (value_1, value_2);            # inclusive


SELECT col
FROM tb
WHERE col NOT IN (value_1, value_2);        # exclusive
```

---

### `LIKE` and `ILIKE` Opeartor

- `LIKE` Opeartor:

  - performs pattern matching against string data with `wildcard characters`.

- `Wildcard characters`

  - Percent `%`: matches any **sequence** of characters
  - Underscore `_`: matches any **singel** character

- `LIKE`: case-sensitive
- `ILIKE`: case-insensitive

```sql
SELECT * FROM customer
WHERE first_name LIKE 'J%';

SELECT * FROM customer
WHERE first_name LIKE '_her%';

SELECT * FROM customer
WHERE first_name NOT LIKE '_her%';
```

---

## `ORDER BY`: Sort Rows

- `ORDER BY`

  - used to sort rows based on a column value, in either ascending or descending order.

- Syntax

```sql
-- Ascending order
SELECT col_1, col_2 FROM tb_name ORDER BY col_1 ASC;

-- Descending order
SELECT col_1, col_2 FROM tb_name ORDER BY col_1 DESC;

-- Multiple order, Same order
SELECT col_1, col_2 FROM tb_name ORDER BY col_1, col_2;

-- Multiple order, Different order
SELECT col_1, col_2 FROM tb_name ORDER BY col_1 ASC, col_2 DESC;
```

- Order:

  - `ASC`: **Default**, Ascending order
  - `DESC`: Descending order

- 技术上, 可以在 order by 中对某列排序, 但该列不在 select 中返回. 但现实中很少出现.

---

## `LIMIT`: Limits number of returned rows

- `LIMIT`

  - limits the number of rows returned for a query.
  - useful to only view the top few rows to get an idea of the table layout.

- `LIMIT` is the last command to be executed. 最后才执行的语句.

```sql
SELECT col_1, col_2
FROM tb
WHERE condition
ORDER BY col_1
LIMIT num
```

---

[TOP](#sql---select-statement)
