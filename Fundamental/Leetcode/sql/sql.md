# SQL

[back](../../index.md)

- [SQL](#sql)
  - [Query Unique rows](#query-unique-rows)
  - [集合](#集合)

---

## Query Unique rows

- with the smallest id

```sql
-- query the unique rows

DROP TABLE employees;

CREATE TABLE employees(
  id int
, email VARCHAR(20)
);

INSERT INTO employees VALUES (
  1
, 'abc@def.com'
);

INSERT INTO employees VALUES (
  2
, '123@456.com'
);

INSERT INTO employees VALUES (
  3
, 'abc@def.com'
);

INSERT INTO employees VALUES (
  4
, 'xyz@svw.com'
);

INSERT INTO employees VALUES (
  5
, 'xyz@svw.com'
);

-- +------+-------------+
-- | id   | email       |
-- +------+-------------+
-- |    1 | abc@def.com |
-- |    2 | 123@456.com |
-- |    3 | abc@def.com |
-- +------+-------------+

-- query unique rows

SELECT MIN(id)
, email
FROM employees
GROUP BY email;

-- +---------+-------------+
-- | MIN(id) | email       |
-- +---------+-------------+
-- |       1 | abc@def.com |
-- |       2 | 123@456.com |
-- |       4 | xyz@svw.com |
-- +---------+-------------+
-- 3 rows in set (0.00 sec)

-- query duplicate rows
SELECT *
FROM employees
WHERE email IN (
    SELECT email
    FROM employees
    GROUP BY email
    HAVING COUNT(email) > 1
  );

-- +------+-------------+
-- | id   | email       |
-- +------+-------------+
-- |    1 | abc@def.com |
-- |    3 | abc@def.com |
-- |    4 | xyz@svw.com |
-- |    5 | xyz@svw.com |
-- +------+-------------+
-- 4 rows in set (0.00 sec)

--  query additional duplicate rows
SELECT *
FROM employees
WHERE id NOT IN (
    SELECT MIN(id)
    FROM employees
    GROUP BY email
  );

-- +------+-------------+
-- | id   | email       |
-- +------+-------------+
-- |    3 | abc@def.com |
-- |    5 | xyz@svw.com |
-- +------+-------------+
-- 2 rows in set (0.00 sec)

-- delete duplicate rows
-- 使用cross join, 如果没有重复则email与id都相等,
-- 如果重复, 则email相等时, id不相等;
-- 注意, 删除时,条件时id>id, 因为如果是<>, 则会删除所有,只留下不重复
-- 当是<时, 只会保留id较大的行
-- 注意: 需要明示是delete e1,因为self join有两个表,mysql需要明确是删除哪一个.
DELETE E1 FROM EMPLOYEES E1 CROSS JOIN EMPLOYEES E2
WHERE
  E1.EMAIL = E2.EMAIL
  AND E1.ID > E2.ID;
```

---

## 集合

```sql

```

---

[TOP](#sql)
