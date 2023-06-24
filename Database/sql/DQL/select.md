# SQL - Select Statement

[Back](../index.md)

- [SQL - Select Statement](#sql---select-statement)
  - [`SELECT FROM`](#select-from)
  - [Alias: Column 列别名](#alias-column-列别名)
    - [Using `AS`](#using-as)
    - [Using Space Character 使用空格](#using-space-character-使用空格)
  - [`||`: Concatenation operator](#-concatenation-operator)
  - [Select Arithmetic](#select-arithmetic)
  - [`SELECT DISTINCT`: Return unique data](#select-distinct-return-unique-data)
  - [`SELECT WHERE`: Filter returned rows](#select-where-filter-returned-rows)
    - [Comparison Operator 比较运算符](#comparison-operator-比较运算符)
    - [Calculation Expression](#calculation-expression)
    - [Logical Operators 逻辑运算符](#logical-operators-逻辑运算符)
    - [`BETWEEN AND` Operator](#between-and-operator)
    - [`IN` Operator](#in-operator)
    - [`LIKE` and `ILIKE` Opeartor](#like-and-ilike-opeartor)
    - [`IS NULL`](#is-null)
  - [`ORDER BY`: Sort Rows](#order-by-sort-rows)
  - [`LIMIT`: Limits number of returned rows](#limit-limits-number-of-returned-rows)
  - [Sub Query](#sub-query)
    - [`EXISTS` function](#exists-function)
  - [`UNION`](#union)

---

## `SELECT FROM`

- Syntax:

```SQL
-- Select all records
SELECT *
FROM table_name;

-- Select single field
SELECT col_name
FROM table_name;

-- Select multiple fields
SELECT col_name, col_name, ...
FROM table_name;
```

- **Argument**

  - The **asterisk character(`*`**) is used to indicate that all columns available are to be displayed.星号表示返回所有
  - The selecting **specific columns** in a SELECT statement.

- **Good practice**

  - It is best to enter your SQL command over several lines, beginning each line with a keyword making it clear and readable, and easier to debug 输入命令，建议分行，每一行由一个关键字起头,让代码清晰, 可读， 易于调试

  - Do your best to **query only the needed columns**.
    - It is **not good practice to use asterisk(\*)** in the SELECT statement,
    - since it will automatically query everything, which increases traffic between the database server and the application, slowing down the retrielval of results.

---

## Alias: Column 列别名

- if you want **alias name** contains any spaces or special symbols, you must enclose the alias in **double quotation marks**

### Using `AS`

- Syntax

```SQL
-- return column with the name of alias name
SELECT column_name AS alias_name
FROM table_name;
```

- `AS` operator gets executed at the very end of a query: that is, alias cannot be used inside a `WHERE` or `HAVING` clause.
  - Example
  ```sql
  SELECT customer_id
  , SUM(amount) AS total_spent
  FROM payment
  GROUP BY customer_id
  HAVING total_spent <100	--"total_spent" 不存在
  ```

---

### Using Space Character 使用空格

- Syntax

```SQL
-- return column with the name of alias name
SELECT column_name alias_name
FROM table_name;
```

---

## `||`: Concatenation operator

- **Concatenation**: Combining columns

- **Concatenation operator**连接运算符(Oracle): two vertical bars beside one another `||` 双竖杠

```SQL
-- combining two columns
SELECT field_name || field_name
FROM table_name

-- concatenate two columns with a space character
SELECT field_name || ' ' || field_name
FROM table_name

```

- a **string literal** was inserted into the output to put a blank space between the two fields

- All **string literals** are enclosed in single quotation marks, the single quotes have a space inside so I end up with a space in my result 单引号

---

## Select Arithmetic

- SQL 只能进行简单计算, 更复杂的计算应该使用 Python 等编程语言处理；

- Arithmetic operators 运算符号

| Operator | Operation |
| -------- | --------- |
| `+`      | Add       |
| `-`      | Subtract  |
| `*`      | Multiply  |
| `/`      | Divide    |

- Arithmetic operations follow the standard order of operations (BEDMAS, or PEMDAS if you learned either of these acronyms) 运算顺序,按照一般四则运算.

- Exponents are not supported, use multiplication 不支持指数计算，应该使用惩罚

- Arithmetic operators can be used in any clause of a SQL statement except the FROM clause

- Order of Operations 运算顺序: 四则运算

  - While Carry out calculation from left to right in an expression, any required multiplication and division operations are solved first;先乘除

  - While Carry out calculation from left to right in an expression, Addition and subtraction operations are solved after multiplication and division, again moving form left to right in the equation 后加减

  - To override this order of operations, parentheses are used to enclose a portion that should be calculated first 括号优先

---

## `SELECT DISTINCT`: Return unique data

- `SELECT DISTINCT`
  - The `DISTINCT` keyword can be used to return only the **unique values in a column**.
  - Remove duplicate items, any duplicate values are suppressed

```sql
SELECT DISTINCT col_name FROM tb_name;

# use parethesis to clarify the column to which the DISTINCT is being applied.
SELECT DISTINCT(col_name)  FROM tb_name;

-- Remove duplicate items by using DISTINCT
SELECT DISTINCT field_name, field_name
FROM table_name;

```

- **Application**

  - The `DISTINCT` keyword is applied to all columns listed in the SELECT statement. Select 语句提及字段都会使用，而不是最近的字段才会适用;

  - The `DISTINCT` keyword in a `SELECT` statement with multiple columns returns the records that are unique for all columns will be returned.多字段时，相当于比较数组。

---

## `SELECT WHERE`: Filter returned rows

- `WHERE` statement
  - specifies conditions on columns for the rows to be returned.
  - The conditions are used to filter the rows returned from the `SELECT` statement.
  - 不能使用别名, 因为别名在`WHERE`语句后才执行.

```sql
SELECT column_name
    ,column_name
    ,column_name
FROM table_name
WHERE column_name operator value;
```

- **Column name**

  - 注意: `WHERE`语句中的列名**不能是 alias**. 注意该特性与在高级 select 中使用 alias 相比较, 因为 alias 是最后输出时才执行的.

- Rule for value

  - value is **case sensitive.大小写敏感**
    注意: Oracle 不是大小写敏感，但 value 是大小写敏感;
    e.g.: `WHERE lname = 'SMITH'`和`WHERE lname = 'smith'`返回的结果是不同的;

  - Character Strings 字符串: Using **singel quotation mark**.
    The use of double quotation mark will raise an error of _invalid idetifier_.

- Date 日期: must be **enclosed in single quotation marks**.
  e.g.: `WHERE data = '2-Mar-22'`
  日期格式与 Date formate 设置有关.

- Number 数字: single quotation marks are **not required**
  The value in a **numeric column** is not required to be enclosed in single quotes.
  e.g.: `WHERE age = 10`

  - **Exception**: 特例
    When a column is defined as **Varchar2** but none of the values stored in this column contains any letters, in this case only, the value in WHERE clause is not required quotation mark. However, if one of the records in this field contained a letter, the omittion of single quotation makr would return an error.
    如果一个字符类型的列的所有数据都以数字储存，则 where 语句与数字类型语句要求相同，即无需单引号。但如果其中个数据有字母， 则无单引号的 where 语句会引起错误.

- **实践**：为避免引号引起的错误,建议搜索前使用`DESC table_name`查询表定义.

---

### Comparison Operator 比较运算符

| Operator    | Description              |
| ----------- | ------------------------ |
| `=`         | Equality, equal to       |
| `<>,!=, ^=` | Not equal to             |
| `>`         | Greater than             |
| `>=`        | Greater than or equal to |
| `<`         | Less than                |
| `<=`        | Less than or equal to    |

- A comparision operator indicates **how the data should relate to a given search value (benchmark)**.

- String: Seldom

  - 只需理解 SQL 可以进行字符串的比较，其比较的是字母顺序 alphabetical order.
  - 实践中少用；通常是使用不等于号用于筛选。

```sql
-- return a set of data where state name start later than given string "GA"
-- if it is <, it  means the state name start alphabetically earlier than the given string
SELECT firstname
    ,lastname
    ,state
FROM customers
WHERE state > 'GA';

```

- **实践**: 实践多用到不等号. 行业中通用是`<>`.

```sql

SELECT firstname
    ,lastname
    ,state
FROM customers
WHERE state <> 'GA';

```

---

### Calculation Expression

- WHERE 语句中，比较运算符两边可以是数学表达式;Arithmetic Expressions can be applied.

```sql
-- 注意:
-- 1. WHERE语句中的column_name列名可以是表达式；
-- 2. column_name不能用alias，下例中只能键入表达式，不能用别名profit
-- 3. value也可以是表达式。

SELECT title
    ,retail-cost AS profit
FROM books
WHERE retail-cost < cost*.2;

```

---

### Logical Operators 逻辑运算符

- To combine multiple comparison operators
- Order of the logical operator:

  1. Arithmetic operator: +-\*/%
  2. Comparison operator: <,>,=, like
  3. Logical operator(in order): NOT>>AND>>OR

- To change the order: parentheses 括号最先计算

```sql
WHERE (category = 'FAMILY LIFE')
OR (pubid = 4
AND cost > 15)

```

---

- `AND`

  | Clause                        | Both/Either          | Result  |
  | ----------------------------- | -------------------- | ------- |
  | `condition_A AND condition_B` | Both True            | `TRUE`  |
  | `condition_A AND condition_B` | Either or Both False | `FALSE` |

  - 若干指定列的 AND<>判断,相当于 NOT IN

  - 集合上,相当于 condition_A 和 condition_B 的**交集**the intersection of sets a and b

---

- `OR`

  | Clause                       | Both/Either         | Result  |
  | ---------------------------- | ------------------- | ------- |
  | `condition_A OR condition_B` | Either or Both True | `TRUE`  |
  | `condition_A OR condition_B` | Both False          | `FALSE` |

  - 若干指定列的 OR=判断,相当于 IN

  - 集合上,相当于 condition_A 和 condition_B 的**并集**the union of sets a and b

---

- `NOT`
  - reverse the meaning of a condition.取反

---

### `BETWEEN AND` Operator

- `BETWEEN AND` Operator

  - can be used to match a value against a range of values.
  - Return a set of data in a range between a given **low boudary** and a given **high boundary**, in stead of comparied with a given benchmark.

- Syntax

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name BETWEEN low_boudary AND high_boudary;
```

- **Practice**

  - same as `value >= low AND value <= high`
  - Boundaries must be specified in order.上下限值的位置不能调换,否则报错;
  - Begin and end points are **inclusive**.包含起始值

  - Can combine `BETWEEN` with the `NOT`

    - `NOT BETWEEN low AND high`
    - same as `value < low AND value > high`

  - Can work with date:

    - `BETWEEN YYYY-MM-DD AND YYYY-MM-DD`
    - Date also include timestamp information.
      - a datetime starts at `0:00`
    - 因为是 inclusive, 所以处理日期时需要注意是否包含.

  - Character String 字符串: Seldom 少用
    - 按照字母顺序 alphabetical order，返回开头为特定范围的结果,
    - 只需要了解可以这样比较即可，实践中少用；
    ```sql
    -- 返回开头为A-D
    SELECT title
        ,pubid
    FROM books
    WHERE title BETWEEN 'A' AND 'D';
    ```

---

### `IN` Operator

- `IN` Operator

  - Return a **set of data** matching a list of given benchmark
  - checks whether a value is included in a list of multiple options.

- Syntax:

```sql

SELECT column_name(s)
FROM table_name
WHERE column_name IN (value1,value2,...);

```

- **Practice**

  - The list of given benchmark must be enclosed in parentheses and separated by commas. 使用括号包围;多个给定值时用逗号分隔；

  - 给定的 value 必须完全匹配，包括字符串，数字，和日期.

- **Inclusive**: `IN`

  - 等价于一些列的`OR=`语句

  ```sql

  -- Equivalent

  SELECT title
      ,pubid
  FROM books
  WHERE pubid IN (1,3,5);

  SELECT title
      ,pubid
  FROM books
  WHERE pubid =1 OR pubid = 3 OR pubid = 5;

  ```

- **exclusive**:`NOT IN` 取反

  - Equivalence 等价于: 一系列的`AND<>`语句

  ```sql
  SELECT column_name(s)
  FROM table_name
  WHERE column_name NOT IN (v1,v2,...);

  SELECT column_name(s)
  FROM table_name
  WHERE column_name <> v1
  AND column_name <> v2 ;

  ```

---

### `LIKE` and `ILIKE` Opeartor

- `LIKE` Opeartor:

  - performs pattern matching against string data with `wildcard characters`.
  - To return a set of records matching given patterns

- `Wildcard characters`

| Wildcard | Description                                                        | Note                    |
| -------- | ------------------------------------------------------------------ | ----------------------- |
| `_`      | underscore 下划线, is used to represent **exactly one** character; | can't represent nothing |
| `%`      | percent 百分号, is used to represent **any number** of characters; | can represent nothing   |

- `LIKE`: case-sensitive
- `ILIKE`: case-insensitive

- Syntax:

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name LIKE pattern;
```

```sql
SELECT * FROM customer
WHERE first_name LIKE 'J%';

SELECT * FROM customer
WHERE first_name LIKE '_her%';

SELECT * FROM customer
WHERE first_name NOT LIKE '_her%';
```

- 常见:

```sql

%a  -- End with 'a'
a%  --Start with 'a'
%a% --Contain 'a'
_a_ --The string is composed of 3 characters with 'a' in the middle
_a  --The string is composed of 2 characters and ends with 'a'.
a_  --The string is composed of 2 characters and starts with 'a'.

```

- `Escape` 转义

  - LIKE 的 pattern 可以转义,以匹配通配符。
  - 使用关键字 `ESCAPE`
  - 允许用户自定义转义标识符 escape indicator，即紧跟 ESCAPE 后的字符,使用单引号包围。
  - 转义标识符不能是通配符，即不能是`_%`;
  - 只有转义标识符其后的通配符才会被转义 taken as literal %/\_ symbal，其他通配符不会被转义.

  - 例子:

  ```sql

  -- B here is escape indicator, the first character followed escape indicator escapes
  -- 该处B被声明为转义的标识
  SELECT *
  FROM testing
  WHERE tvalue LIKE 'B%__A%T' ESCAPE 'B'

  -- Return rows started with % and followed by any characters.
  SELECT *
  FROM testing
  WHERE tvalue LIKE '\%%' ESCAPE '\'

  ```

---

### `IS NULL`

- `NULL` values, representing that no value has been stored in particular field , can return unexpected results.

- `IS NULL` is used to search `NULL` values, while equal sign `=` can't be used

  - 不能使用等于号匹配 NULL 值.
  - 如果使用`field_name = NULL`,不会报错; 但不会返回任何行.Not returns no rows.
  - 比较的前提是非 null，所以<>不会涉及 null 值

- 字段中存在`NULL`值时，返回的数据使用`(null)`标识。

- 取反: `IS NOT NULL`. 不能使用`<>`。

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
SELECT col_1, col_2
FROM tb_name
ORDER BY col_1 ASC, col_2 DESC;
```

- `ORDER BY` clause is listed **at the end** of the `SELECT` statement.

- Column **alias**, if applied, can be used in `ORDER BY` clause. 可以使用别名

- Sort by column ordinals

  - 使用列序号 column ordinal
  - 列序号指是 SELECT 语句中的 field_name 的排序,序号**从 1 开始**。

- Order:

  - `ASC`: **Default**, Ascending order
    - Values are listed in the order of:
      - Blank and special characters 空白或特殊字符
      - Numeric values 数字
      - Character values 字符
      - NULL values
  - `DESC`: Descending order

- `NULL` value:

  - By default, nul values are **listed last**.
  - `NULLS FIRST`: Null values are listed first.
  - `NULLS LAST`: Null values are listed last.

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

## Sub Query

- `Sub query`

  - construct complex queries, performing a query on the result of another query.

```sql
SELECT *
FROM tb
WHERE (sub query)
```

- Sub query will be executed first since it is inside the parenthesis.

### `EXISTS` function

- test the existence of rows in a subquery.

- Syntax

```sql
SELECT col
FROM tb
WHERE EXISTS(
  SELECT col
  FROM tb
  WHERE condition
)
```

---

## `UNION`

- `UNION`

  - combines the result-set of two or more `SELECT` clause.
  - directly concatenate two results together.

- Syntax

```sql
SELECT col FROM tb_1
UNION
SELECT col FROM tb_2;
```

---

[TOP](#sql---select-statement)
