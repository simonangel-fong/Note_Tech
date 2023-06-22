# SQL - JOIN

[Back](../index.md)

- [SQL - JOIN](#sql---join)
  - [`JOIN` Statement](#join-statement)
  - [`CROSS JOIN`:Cartesian Join 笛卡尔连接](#cross-joincartesian-join-笛卡尔连接)
  - [`INNER JOIN`](#inner-join)
    - [`Equality Join`](#equality-join)
    - [Non-Equality Joins](#non-equality-joins)
  - [`OUTER JOIN`](#outer-join)
    - [`FULL OUTER JOIN`](#full-outer-join)
    - [`LEFT OUTER JOIN`](#left-outer-join)
    - [`RIGHT OUTER JOIN`](#right-outer-join)
  - [Self-Joins](#self-joins)
  - [Join Three or More Tables](#join-three-or-more-tables)

---

## `JOIN` Statement

- `JOIN`:

  - combine data from multiple tables, based on a related column between them.

- Types of Joins

![sql-join](./pic/sql-join.png)

---

## `CROSS JOIN`:Cartesian Join 笛卡尔连接

- `CROSS JOIN`

  - In a **`Cartesian Join`** (also called a `Cartesian Product`笛卡尔乘积 or a `Cross Join`), each record in the first table is matched with a record from the second table

- Syntax:

```SQL

-- Traditional Method
SELECT table1.column1 , table1.column2, table2.column1...
FROM table1, table2;


-- Cross Join
SELECT table1.column1 , table1.column2, table2.column1...
FROM table1
CROSS JOIN table2;

```

- Every row of one table is joined to every row of the second table. So it joins every row with every possible combination of records. 总数是两个集合元素个数的乘积.

- In the absence of a `WHERE` condition the `CARTESIAN JOIN` will behave like a `CARTESIAN PRODUCT` 原因是缺少 where 语句.

- In the presence of `WHERE` condition this `JOIN` will function like a `INNER JOIN`有 where 语句时,相当于内联结.

- Generally speaking, Cross join is similar to an `inner join` where the join-condition will always evaluate to `True`. 相当于特殊的内联.

---

## `INNER JOIN`

- `INNER JOIN`

  - return the result set of matched data in both tables.
  - Returns records that have matching values in both tables. 返回两表匹配的值,相当于交集 intersection.

![inner_join](./pic/join_inner_join.gif)

---

### `Equality Join`

- The most common type of join used in the workplace uses two or more tables with **equivalent data stored in a common column**. 原因是两表存在相等值在共同列.

- A **common column** is a column with equivalent data that exists in two or more tables.

- Syntax

```sql
-- Equality Join
-- Traditional Method
SELECT table1.column1, table2.column2, ...
FROM table1, table2
WHERE table1.common_col = table2.common_col;

-- JOIN ON
SELECT *
FROM tb_1
INNER JOIN tb_2
ON tb_1.col_match = tb_2.col_match;

```

- The order of tables does not matter.

  - Only applied in `INNER JOIN`

- `JOIN` == `INNER JOIN`

- When performing , a row is returned if there was a corresponding record in each table queried.

- The **Equality Join**, **Non-Equality Join** and **Self-Joins** are all classified as **inner joins** because records are only <u>returned if a match is found in each table</u>内联结是指返回匹配的数据. 不匹配的不会返回.

- The default keyword `INNER` can be included with the `JOIN` keyword to specify that only the records having a matching row in the corresponding table should be returned in the results. 可以使用关键字`INNER`.

- 进行`SELECT JOIN`时, 无论是哪种方法,都要在**列名 column name**前标明标明**表名 table name**, 避免报错. 特别是对**共同列 common column**.

- `SELECT JOIN`可以使用表别名 table alias.

---

### Non-Equality Joins

- `Non-Equality Joins`

  - A **non-equality join** is used when the related columns cannot be joined through an <u>equal sign</u>. 不是相等值

  - Instead of finding a **column-to-column match**, you use the `non-equality join` to determine whether the weight of the item falls between the minimum and maximum **ranges** of the columns. 不是行-行匹配,是范围的匹配.

- Syntax:

```sql
-- Non-Equality Joins
-- Traditional Method
SELECT A.column1, B.column2, ...
FROM table1 A, table2 B
WHERE A.common_col BETWEEN B.max_col AND B.min_col;

-- JOIN ON
SELECT A.column1, B.column2, ...
FROM table1 A INNER JOIN table2 B
ON A.common_col BETWEEN B.max_col AND B.min_col;

```

---

## `OUTER JOIN`

- `OUTER JOIN`

  - allow to specify how to deal with data **only present in one** of the tables being joined.

---

### `FULL OUTER JOIN`

- `FULL OUTER JOIN`

  - Returns all records when there is a match in either left or right table. 显示左右表所有数据.
  - Returns **all records** when there is a match in _either left or right table_. 显示左右表所有数据.

![full_join](./pic/join_full_join.gif)

- Syntax

```sql
-- return any data in both table, non-matched data filled by null
SELECT tb_1.col, tb_2.col
FROM tb_1
FULL OUTER JOIN tb_2
ON tb_1.col_match = tb_2.col_match


-- return unique data in both table, except intersection
-- 即排除重合的集合, 是inner join的逆命题
SELECT *
FROM tb_1
FULL OUTER JOIN tb_2
ON tb_1.col_match = tb_2.col_match
WHERE tb_1.id IS null
OR tb_2.id IS null;


```

---

### `LEFT OUTER JOIN`

- `LEFT OUTER JOIN`

  - presents the records in the left table and, if matched, the records in the right table. Otherwise, fill with `null`.
  - Returns **all records** from the **left** table, and the _matched records_ from the _right table_. 显示所有左表,和匹配的右表记录.

![left_join](./pic/join_left_join.gif)

- Syntax

```sql
-- present all data in the left table
-- present match data in the right table
SELECT *
FROM tb_1       -- tb_1 is the left table
LEFT OUTER JOIN tb_2
ON tb_1.col_match = tb_2.col_match;

SELECT *
FROM tb_1
LEFT JOIN tb_2      -- LEFT JOIN = LEFT OUTER JOIN
ON tb_1.col_match = tb_2.col_match;

-- return unique data in the left table
SELECT *
FROM tb_1
LEFT OUTER JOIN tb_2
ON tb_1.col_match = tb_2.col_match
WHERE tb_2.id IS null;

```

- The table **order matters**:
  - The table after `FROM` is the left table.

---

### `RIGHT OUTER JOIN`

- `RIGHT (OUTER) JOIN`：
  - Returns **all records** from the **right table**, and the _matched records_ from the _left table_. 显示所有右表,和匹配的左表记录.

![right_join](./pic/join_right_join.gif)

- 不常用, 因为和左联结相通. 一般使用左联结.

- Syntax:

```SQL

SELECT A.column, B.column...
FROM table1 A Right OUTER JOIN table2 B
ON A.common_col = B.common_col;

```

---

## Self-Joins

- `Self-Join`

  - a query in which a table is joined itself.
  - used to compare values in a column of rows within the same table.
  - Applied when the data in a table references other data stored in the **same table**. 引用相同表.

  - necessary to use an alias; Otherwise table names would be ambiguous.

- Syntax:

```SQL
-- Self-Join
-- Traditional Method
SELECT A.column1, A.column2, ...
FROM table1 A, table1 B --自联结, 两个表名相同
WHERE A.common_ref = B.common_id;

-- JOIN ON
SELECT A.column1, B.column2, ...
FROM table1 A
INNER JOIN table1 B
ON A.common_ref = B.common_id
AND A.id !=B.id;

```

- 注意:
  - 一般 self-join 都会发生相同行的配对, 例如 film 表的 self-join, 找出有相同 length 的 title 列. 此时第一个配对的是相同的 title, 这个应该排除.所以可以在 ON 中使用`f1.film_id != f2.film_id`

---

## Join Three or More Tables

- Syntax:

```sql
-- Traditional Method
SELECT A.column, B.column, C.column, ...
FROM table1 A, table2 B, table3 C
WHERE A.common_col1 = B.common_col1 -- 联结表A和表B
AND B.common_col2 = C.common_col2; -- 联结表A和表B

-- JOIN Method
SELECT A.column, B.column, C.column
FROM table1 A JOIN table2 B
ON A.common_col1 = B.common_col1 --联结不同表
JOIN talbe3 C
ON B.common_col2 = C.common_col2 --联结不同表
WHERE condition; --筛选条件

```

---

[TOP](#sql---join)
