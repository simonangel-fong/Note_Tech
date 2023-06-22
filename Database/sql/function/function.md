# SQL - Function

[Back](../index.md)

- [SQL - Function](#sql---function)
  - [Group Function](#group-function)
    - [`SUM`](#sum)
    - [`AVG`](#avg)
    - [`COUNT`](#count)
    - [`MAX`](#max)
    - [`MIN`](#min)
    - [Nesting Group Functions](#nesting-group-functions)
  - [Datetime Function](#datetime-function)
    - [`EXTRACT()`](#extract)
    - [`AGE()`](#age)
  - [Mathematical Function](#mathematical-function)
  - [String Function](#string-function)
    - [`TO_CHAR()`](#to_char)

---

## Group Function

- `Group functions`
  - aka `multiple-row functions`, `aggregate functions`.
  - return <u>one result</u> **per group of rows** processed. 对每个组别的行返回一个结果.
  - The `GROUP BY` clause which is used to **identify groups**.
  - The `HAVING` clause which is used to **restrict groups**.

```sql

SELECT columnname, function(columnname) ...
FROM tablename
WHERE condition
GROUP BY columnname1, columnname2
HAVING group_condition;

```

- **Rules** for working with group functions:

  1. Use the `DISTINCT` keyword to include only **unique** values.
     The `ALL` keyword is the **default** and it instructs Oracle 12c to include all values **except nulls**.
  2. All group functions **ignore** `NULL` values except `COUNT(*)`. To include NULL values nest the NVL function within the group function. For example `SELECT MAX(NVL(shipdate, SYSDATE) – orderdate)` will substitute the system date for the shipping date of any order that has not been shipped

---

### `SUM`

- to calculate the **total amount** stored in a numeric field for a group of records. 计算一个数字字段的总量.

- Syntax:

```sql

-- 总计某字段的所有值之和, ALL是默认值, 可以省略.
SELECT SUM(ALL col1)
FROM tablename;

-- 总计某字段的唯一值之和
SELECT SUM(DISTINCT col1)
FROM tablename;

-- 先计算两列和, 再总计两列和
SELECT SUM(col1 + col2)
FROM tablename;

-- 可以用于join
SELECT SUM(a.col1 + b.col2)
FROM tableA a JOIN tableB b
ON (a.col1 BETWEEN b.col3 AND b.col4)
WHERE a.col2 IS NOT NULL;

```

- Optional:
  - `ALL`: Default, to include **multiple occurrences** of numeric values when totaling a field. 包含重复值计算和.
  - `DISTINCT`: to include only **unique** numeric values in its calculations.只包含唯一值计算和.

---

### `AVG`

- To calculates the **average of the numeric values** in a specific column. 计算某一列的均值.

- Syntax:

```sql

-- 总计某字段的所有值之均值, ALL是默认值, 可以省略.
SELECT AVG(ALL col1)
FROM tablename;

-- 总计某字段的唯一值之均值.
SELECT AVG(DISTINCT col1)
FROM tablename;

```

- 处理`NULL`值: `NVL`

  - 只计算 non `NULL` value.

  - 如果需要包含`NULL`值的, 先使用`NVL`函数将`NULL`值转为指定值(一般是 0).

```SQL
SELECT AVG(NVL(columnname, 0))
FROM tablename;
```

- 处理小数点: `ROUND`/`TRUNC`

```SQL
SELECT ROUND(AVG(NVL(col1, 0)))
FROM tablename;
```

---

### `COUNT`

1. Count the records that have **non-NULL values** in a specified field. 计算非空值.

2. Count the total records that meet a **specific condition**, including those **containing NULL values**. 给定条件下,计算空值.

```SQL

-- 总计某字段的所有值的个数, ALL是默认值, 可以省略. 此时只计算非空值.
SELECT COUNT(ALL col)
FROM tbname;

-- 计算唯一值的个数, 此时只计算非空值.
SELECT COUNT(DISTINCT col)
FROM tbname;

-- 计算某列是空值的个数
SELECT COUNT(*)  --注意, 括号中是星号, 不能是列名, 此时是计算所有符合条件的记录; 当是列名时,只计算非空值.
FROM tbname
WHERE colname IS NULL;  -- 列名在where语句中
-- WHERE colname IS NOT NULL;  --计算非空值个数的条件

-- 排除可能的空值方法: 使用NVL将空值转换,再计算个数
SELECT COUNT(NVL(colname,0))
FROM tbname;

```

---

### `MAX`

- returns the **largest value** stored in a specified column.

- Syntax:

```sql

-- 返回某字段的最大值, ALL是默认值, 可以省略.
SELECT MAX(ALL col1)
FROM tablename;

-- 返回某字段的唯一值的最大值
SELECT MAX(DISTINCT col1)
FROM tablename;

-- 先计算两列和, 再返回之和的最大自
SELECT MAX(col1 + col2)
FROM tablename;
```

- Non-numeric Data
  - 可以适用于非数字数据类型
    - 字符数据: Z>A
    - 日期数据: 较近的日期 the most recent date.

---

### `MIN`

- returns the **smallest value** in a specified column

- Syntax:

```sql

-- 返回某字段的最小值, ALL是默认值, 可以省略.
SELECT MIN(ALL col1)
FROM tablename;

-- 返回某字段的唯一值的最小值
SELECT MIN(DISTINCT col1)
FROM tablename;

-- 先计算两列和, 再返回之和的最小值
SELECT MIN(col1 + col2)
FROM tablename;

```

---

### Nesting Group Functions

- As with single-row functions, when group functions are nested, the inner function is resolved first. 内层先计算

- Unlike single-row functions that have no restriction on how many nesting levels can occur, group functions can only be nested to a depth of two.单行函数能无限嵌套,聚合函数最多只能嵌套在第二层.

  - Keep in mind that group functions can only be nested to only two levels

- A group function can also be nested inside a group function.相互嵌套`AVG(SUM(colname))`

- The query must include a GROUP BY clause 嵌套必须使用 GROUP BY
  - 难点:

```sql
-- 两层嵌套
SELECT AVG(SUM(quantity * paideach))
FROM orders o JOIN orderitems oi
ON o.order#=oi.order#
GROUP BY o.order#; --该处分组依据是order#, 则AVG是以order#的个数为除数, 如果换做其他列, 可能会因为NULL值而结果不同.

```

---

## Datetime Function

```sql
SELECT NOW()
SELECT TIMEOFDAY()
SELECT CURRENT_TIME
SELECT CURRENT_DATE
```

---

### `EXTRACT()`

- `EXTRACT()`
  - extract a sub-component of a date value
    - YEAR
    - MONTH
    - DAY
    - WEEK
    - QUARTER

```SQL
SELECT EXTRACT(YEAR FROM CURRENT_DATE);
SELECT EXTRACT(MONTH FROM CURRENT_DATE);
SELECT EXTRACT(DATE FROM CURRENT_DATE);
SELECT EXTRACT(QUARTER FROM CURRENT_DATE);
SELECT EXTRACT(DOW FROM CURRENT_DATE);    --weekday, sunday(0) to Saturday(6)
SELECT EXTRACT(HOUR FROM CURRENT_DATE);
SELECT EXTRACT(MINUTE FROM CURRENT_DATE);
SELECT EXTRACT(SECOND FROM CURRENT_DATE);
```

---

### `AGE()`

- `AGE()`

  - calculate and return the **current** age

```sql
SELECT AGE(datetime_col)
```

---

## Mathematical Function

- Documentation
  - https://www.postgresql.org/docs/12/functions-math.html

---

## String Function

- Documentation
  - https://www.postgresql.org/docs/13/functions-string.html

---

### `TO_CHAR()`

- `TO_CHAR()`

  - convert date types to text

- Documentation
  - https://www.postgresql.org/docs/13/functions-formatting.html

```sql
TO_CHAR(date_col,patern)
```

---

[TOP](#sql---function)
