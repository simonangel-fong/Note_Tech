# DBA - User

[Back](../../index.md)

- [DBA - User](#dba---user)
  - [Change password](#change-password)
  - [Unlock a user account](#unlock-a-user-account)

---

## Change password

```sql
# Connect as dba
CONNECT sys as sysdba;

# Alter user's passwords
ALTER USER user_name IDENTIFIED BY "new_password";

```

---

## Unlock a user account

```sql
select username from all_users where username = 'HR';    # confirm hr user exist.
ALTER USER hr ACCOUNT UNLOCK;   # unlock the account
ALTER USER hr IDENTIFIED BY "hr";   # set a new pwd

CONNECT hr/hr@orclpdb;    # Connect using hr

SELECT table_name FROM user_tables;
```

![lab_unlock_user](./pic/lab_unlock_user.png)

- Configure connection in SQL developer

![lab_unlock_user](./pic/lab_unlock_user02.png)

- Query

![lab_unlock_user](./pic/lab_unlock_user03.png)

---

[TOP](#dba---user)
