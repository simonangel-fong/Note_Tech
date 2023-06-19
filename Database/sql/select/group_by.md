# SQL - Group By Statement

[Back](../index.md)

- [SQL - Group By Statement](#sql---group-by-statement)
  - [`GROUP BY` Statement](#group-by-statement)
  - [`HAVING` statement: Filter aggregate result](#having-statement-filter-aggregate-result)

---

## `GROUP BY` Statement

- `GROUP BY`

  - allow to aggregate data and apply function per some category.

```SQL
SELECT category_col_1, category_col_2, aggregate_function(data_col)
FROM tb_name
WHERE condition
# the order doesn't matter
# category column can be function, eg: DATE(payment_date)
GROUP BY category_col_1, category_col_2
ORDER BY aggregate_function(data_col)
LIMIT num
```

- `GROUP BY` clause

  - must appear right after a `FROM` or `WHERE` statement.

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

- Syntax

```SQL
SELECT category_col_1, category_col_2, aggregate_function(data_col)
FROM tb_name
WHERE condition
GROUP BY category_col_1, category_col_2
HAVING condition    # filter aggregate result
ORDER BY aggregate_function(data_col)
LIMIT num
```

- The aggregation function is executed after the `GROUP BY` statement, if applied, which is executed after the `WHERE` statement.

  - The `WHERE` statement can't be used to filter data based on the aggregate result, since it executes before aggregation function.
  - `Having` statement is executed after the aggregation function, and thus **can filter the aggregate result**.

- `Having` condition

  - must be an aggregation function 必须是聚合函数
  - can be a different aggregation function 可以是与列不相同的聚合函数
  - example:

  ```sql
  SELECT customer_id
  , SUM(amount)   # SUM aggregation function
  FROM payment
  GROUP BY customer_id
  HAVING COUNT(amount)  > 40    # COUNT aggregation function
  ORDER BY 2 DESC;
  ```

---

[TOP](#sql---group-by)
