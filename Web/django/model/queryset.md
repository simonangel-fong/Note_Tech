# Django - QuerySet

[Back](../index.md)

- [Django - QuerySet](#django---queryset)
  - [QuerySet](#queryset)
  - [Methods: `SELECT WHERE`](#methods-select-where)
    - [Field Lookup](#field-lookup)
    - [Operators](#operators)
  - [Methods:`CRUD`](#methodscrud)
  - [Methods: Function](#methods-function)
    - [Aggregation functions](#aggregation-functions)

---

## QuerySet

- `QuerySet`

  - represents **a collection of objects** from your database.
  - It can have zero, one or many filters.
  - In SQL terms, a **QuerySet** equates to a `SELECT` statement

- `Filter`

  - Filters narrow down the query results based on the given parameters.
  - a **filter** is a limiting clause such as `WHERE` or `LIMIT`.

- QuerySet can acqured by model’s `Manager`.

- Operation:
  - Iteration: `for in`
  - Asynchronous iteration: `async for`
  - Slicing: `queryset[:]`
  - `repr()`
  - `len()`
  - `list()`: `list(QuerySet)`
  - `bool()`: `if model.objects.filter():`

---

## Methods: `SELECT WHERE`

| Method                | Description                                                             | SQL                       |
| --------------------- | ----------------------------------------------------------------------- | ------------------------- |
| `all()`               | Returns a copy of the current QuerySet                                  | `SELECT *`                |
| `contains()`          | Returns True if the QuerySet contains obj                               | `WHERE EXISTS()`          |
| `filter()`            | Return QuerySet matching lookup parameters.                             | `WHERE`                   |
| `exclude()`           | Return QuerySet **not** matching lookup parameters.                     | `WHERE NOT`               |
| `order_by()`          | Return QuerySet ordered by the ordering tuple                           | `ORDER BY`                |
| `reverse()`           | Return QuerySet reversed the order                                      | `ORDER BY DESC`           |
| `dates()`             | Return QuerySet evaluated a list of `datetime.date` objects             |                           |
| `datetimes()`         | Return QuerySet evaluated a list of `datetime.datetime` objects         |                           |
| `distinct()`          | Return QuerySet eliminated duplicate rows                               | `SELECT DISTINCT`         |
| `union()`             | combine the results of two or more QuerySets.                           | `UNION`                   |
| `select_related()`    | Selecting additional related-object data in foreign-key relationships   | `JOIN`                    |
| `intersection()`      | Return the shared elements of two or more QuerySets                     | `INNER JOIN`              |
| `difference()`        | keep only elements present in one but not in other                      | `LEFT JOIN WHERE IS NULL` |
| `select_for_update()` | Returns a queryset that will lock rows until the end of the transaction | `SELECT ... FOR UPDATE`   |
| `values()`            | Return QuerySet contains dictionaries                                   |                           |
| `values_list()`       | Return QuerySet contains tuples                                         |                           |
| `none()`              | Return an empty queryset                                                |                           |
| `extra()`             | Return QS using a complex `WHERE` clause                                |                           |
| `raw()()`             | Returns a queryset using a raw SQL query                                |                           |

---

### Field Lookup

- `Field lookups`

  - how to specify conditions of an SQL `WHERE` clause.
  - They’re specified as keyword arguments to the QuerySet methods `filter()`, `exclude()` and `get()`.

- Basic lookups keyword arguments take the form:

  - `field__lookuptype=value`. (That’s a double-underscore)

| Lookup type   | Description                                | SQL              |
| ------------- | ------------------------------------------ | ---------------- |
| `isnull`      | IS NULL test                               | `WHERE IS NULL`  |
| `exact`       | Exact match                                |                  |
| `iexact`      | Case-insensitive exact match               |                  |
| `contains`    | containment test                           | `LIKE %value%`   |
| `icontains`   | Case-insensitive containment test.         | `ILIKE %value%`  |
| `in`          | In a given iterable                        | `IN ()`          |
| `gt`          | Greater than                               | `WHERE >`        |
| `gte`         | Greater than or equal to.                  | `WHERE >=`       |
| `lt`          | Less than.                                 | `WHERE <`        |
| `lte`         | Less than or equal to.                     | `WHERE <=`       |
| `startswith`  | starts-with.                               | `LIKE 'value%'`  |
| `istartswith` | Case-insensitive starts-with.              | `ILIKE 'value%'` |
| `endswith`    | ends-with.                                 | `LIKE '%value'`  |
| `iendswith`   | Case-insensitive ends-with.                | `ILIKE '%value'` |
| `range`       | Range test (inclusive)                     | `BETWEEN AND`    |
| `regex`       | regular expression match                   |                  |
| `iregex`      | Case-insensitive regular expression match. |                  |

- **Datetime**

| Lookup type | Description           | SQL                                     |
| ----------- | --------------------- | --------------------------------------- |
| `date`      | an exact date match   |                                         |
| `year`      | an exact year match   | `BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` |
| `month`     | an exact month match  | `BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` |
| `day`       | an exact day match    |                                         |
| `week`      | week number match     |                                         |
| `week_day`  | week day match        |                                         |
| `quarter`   | quarter match         |                                         |
| `time`      | time match            |                                         |
| `hour`      | an exact hour match   |                                         |
| `minute`    | an exact minute match |                                         |
| `second`    | an exact second match |                                         |

---

### Operators

| Operators | Description            | SQL         |
| --------- | ---------------------- | ----------- | ---------- |
| `&`       | Combines two QuerySets | `WHERE AND` |
| `         | `                      | OR          | `WHERE OR` |
| `^`       | XOR                    | `WHERE XOR` |

---

## Methods:`CRUD`

| Method               | Description                                                               | SQL           |
| -------------------- | ------------------------------------------------------------------------- | ------------- |
| `get()`              | Returns a matching **object**                                             |               |
| `first()`            | Returns the first **object** of QS                                        |               |
| `latest()`           | Returns the last **object**                                               |               |
| `earliest()`         | Returns the earliest **object**                                           |               |
| `latest()`           | Returns the latest **object**                                             |               |
| `create()`           | Creates and saves an object. == `save(force_insert=True)`                 | `INSERT INTO` |
| `get_or_create()`    | `get()` if exists; Otherwise, `create()`. Returns `(object, created)`.    | `INSERT INTO` |
| `bulk_create()`      | Inserts the provided list of objects. Returns created objects as a list   |               |
| `update()`           | Performs an SQL update query. Return the number of rows matched           | `UPDATE SET`  |
| `update_or_create()` | `update()` if exists; Otherwise, `create()`. Returns `(object, created)`. | `UPDATE SET`  |
| `bulk_update()`      | updates the given fields. Returns the number of objects updated           |               |
| `delete()`           | Performs an SQL delete query.                                             | `DELETE FROM` |

---

## Methods: Function

| Method        | Description                                       | SQL        |
| ------------- | ------------------------------------------------- | ---------- |
| `exists()`    | Returns True if the QuerySet contains any results |            |
| `count()`     | Returns the number of objects                     | `COUNT()`  |
| `aggregate()` | Returns a dictionary of aggregate values          | `GROUP BY` |

---

### Aggregation functions

| Aggregation  | Description                      |
| ------------ | -------------------------------- |
| `Avg()`      | Returns the mean value           |
| `Count()`    | Returns the number of objects    |
| `Max()`      | Returns the maximum value        |
| `Min()`      | Returns the minimum value        |
| `StdDev()`   | Returns the standard deviation   |
| `Sum()`      | Returns the sum of all values    |
| `Variance()` | Returns the variance of the data |

---

[TOP](#django---queryset)
