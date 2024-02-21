# Subquery

[Back](./index.md)

---

## Lab

```sql
-- join sales person
SELECT c.first_name || ' ' || c.last_name AS "Customers"
FROM usa_customers c
JOIN usa_sales_persons sp
ON c.sales_pers_id = sp.sales_pers_id
WHERE sp.first_name IN ('Andrew', 'John');

-- Subquery saleperson
SELECT first_name||' '||last_name "Name"
FROM usa_customers
WHERE sales_pers_id IN (
    SELECT sales_pers_id
    FROM usa_sales_persons
    WHERE first_name IN ('John', 'Andrew')
);

-- join city
SELECT c.first_name || ' ' || c.last_name AS "Customers"
FROM usa_customers c
JOIN usa_cities ci
ON c.city_id = ci.city_id
WHERE ci.city IN ('Dallas','San Francisco');

-- subquery city
SELECT first_name||' '||last_name "Name"
FROM usa_customers
WHERE city_id IN (
    SELECT city_id
    FROM usa_cities
    WHERE city IN ('Dallas','San Francisco')
);

```

---

[TOP](#subquery)
