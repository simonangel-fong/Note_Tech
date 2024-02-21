# Merge

[Back](./index.md)

- [Merge](#merge)
  - [Create user](#create-user)
  - [MERGE Statement](#merge-statement)

---

## Create user

- SYS create user

```sql
-- Task: create user
ALTER SESSION SET "_ORACLE_SCRIPT"=true;

--DROP USER week6_n01555914 CASCADE;

CREATE USER week6_n01555914
IDENTIFIED BY week6_n01555914
QUOTA UNLIMITED ON users;

GRANT connect, resource TO week6_n01555914;
```

---

## MERGE Statement

- user to merge

```sql
-- run script

SELECT productname
FROM a2_product
WHERE productname LIKE 'E%';

MERGE INTO a2_product t
USING (
    SELECT idproduct, productname
    FROM a2_product
    WHERE productname LIKE 'E%'
) s
ON (t.idproduct = s.idproduct)
WHEN MATCHED THEN
    UPDATE SET
        t.productname = s.productname || '-E';

SELECT idproduct, productname
FROM a2_product
WHERE productname LIKE 'E%';

ROLLBACK;

SELECT idproduct, productname
FROM a2_product
WHERE productname LIKE 'E%';







```

---

[TOP](#merge)
