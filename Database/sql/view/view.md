# SQL - View

[Back](../index.md)

- [SQL - View](#sql---view)
  - [View](#view)

---

## View

- `View`

  - a database object that is of a stored query.
  - a virtual table in database.
  - A view does not store data physically, but **simply stores the query**.

- Syntax

```sql
-- create or replace a view
CREATE OR REPLACE VIEW view_name AS
select_query;

-- query a view
SELECT * FROM view_name;

-- remove a view
DROP VIEW IF EXISTS view_name;

-- rename a view


```

- Example

```sql
CREATE OR REPLACE VIEW customer_info AS
SELECT first_name
, last_name
, address
, district
FROM customer
INNER JOIN address
ON customer.address_id = address.address_id;

ALTER VIEW customer_info
RENAME TO c_info;

SELECT * FROM c_info;

DROP VIEW IF EXISTS c_info;
```

---

[TOP](#sql---view)
