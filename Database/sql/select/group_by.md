# SQL - Group By

[Back](../index.md)

- [SQL - Group By](#sql---group-by)
  - [`GROUP BY` Statement](#group-by-statement)
  - [`HAVING` statement: Filter aggregate result](#having-statement-filter-aggregate-result)

---

## `GROUP BY` Statement

- `GROUP BY`

  - allow to aggregate data and apply function per some category.
  - `GROUP BY` 语句用于结合聚合函数，根据一个或多个列对结果集进行分组。
  - `GROUP BY` 解决的是 Group function 不能和列名共同 Query 的问题. 如果没有 GROUP BY, Group function 只能在 Query 中返回单一结果; 适用了 Group BY, 则 Group function 可以和列名结合返回多列多行结果.
  - **作用**: Group BY 支出分组的依据, Group function 是在各个分组进行计算. 输出结果是在分组指明的列名的字段中逐行列出结果.

- Syntax

```SQL
SELECT category_col_1, category_col_2, aggregate_function(data_col)
FROM tb_name
WHERE condition
# the order doesn't matter
# category column can be function, eg: DATE(payment_date)
GROUP BY category_col_1, category_col_2
ORDER BY aggregate_function(data_col)
LIMIT num

-- JOIN情况下的Group By
SELECT a.col1, b.col2 SUM(a.col * a.col) "Alias"  --列出结果需要的列名和多列函数
FROM tbA a JOIN tbB b ON (a.colcommon = b.colcommon) --指出联结的条件
GROUP BY a.col1, b.col2  --指出需要分组的列名,注意该处col1和col2必须列出,因为他们都在SELECT语句中出现
ORDER BY a.col1, b.col2; --排序
```

- `GROUP BY` clause
  - must appear right after a `FROM` or `WHERE` statement.
  - Column aliases cannot be used in the `GROUP BY` clause. 别名不能再 GROUP BY 语句中出现.
- In `SELECT` statement, columns must either have an aggregate function or be in the `GROUP BY` call. select 中的列名, 要么适用于聚合函数,要么在 GROUP BY 中声明.

- **Categorical Column**

  - the column applied to `GROUP BY`
  - non-continuous
  - aggregate function will apply to each category in Categorical Column.

- `ORDER BY`
  - reference the entire function to sort result

---

## `HAVING` statement: Filter aggregate result

- `HAVING` statement

  - filter an aggregation.
  - **restrict groups** returned by a query

- Syntax:

```SQL
SELECT category_col_1, category_col_2, aggregate_function(column_name)
FROM tb_name
WHERE condition
GROUP BY category_col_1, category_col_2
HAVING aggregate_function(column_name) operator value
ORDER BY aggregate_function(data_col)
LIMIT num
```

- `Having` condition

  - must be an aggregation function 必须是聚合函数
  - can be a different aggregation function 可以是与列不相同的聚合函数
  - 不能使用别名, 因为别名在`HAVING`之后执行.
  - example:

  ```sql
  SELECT customer_id
  , SUM(amount)   # SUM aggregation function
  FROM payment
  GROUP BY customer_id
  HAVING COUNT(amount)  > 40    # COUNT aggregation function
  ORDER BY 2 DESC;
  ```

- **对比: `HAVING` vs `WHERE`**

  - The `WHERE` clause restricts the records that will **appear in the query**.
    - the `WHERE` clause cannot contain any **grouping functions**. where 不能使用聚合函数
  - The `HAVING` clause will **specify which groups** will be displayed in the results. The `HAVING` clause is a `WHERE` clause for groups
    - Having 可以使用聚合函数
  - 在 SQL 中增加 HAVING 子句原因是，WHERE 关键字无法与聚合函数一起使用。HAVING 子句可以让我们筛选分组后的各组数据。

- **使用**:

  - 如果同时涉及筛选条件, 分组, 分组条件时, 三个语句的顺序:

    1. `WHERE`
    2. `GROUP`
    3. `HAVING`

  - 计算顺序:

    - The `WHERE` clause filters the data **before grouping**, whereas the `HAVING` clause filters the groups **after** the grouping occurs. 先 where 过滤, 再 having 过滤
    - 性能问题 efficiency: 虽然 where 和 having 都能限制条件,但如果将条件放在 having,则会对全部的结果进行聚合函数再筛选,增加额外运算.

  - 思考思路:
    1. 是否需要筛选 - `WHERE`;
    2. 是否需要使用聚合函数 - `GROUP BY`;
    3. 是否需要对分组进行限制 - `HAVING`;

---

[TOP](#sql---group-by)
