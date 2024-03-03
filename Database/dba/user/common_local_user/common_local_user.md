# DBA - Users: Common users VS Local users

[Back](../../index.md)

- [DBA - Users: Common users VS Local users](#dba---users-common-users-vs-local-users)
  - [Common Users VS Local Users](#common-users-vs-local-users)
    - [Lab: Query common users and local users](#lab-query-common-users-and-local-users)
    - [Lab: Create a common user](#lab-create-a-common-user)
    - [Lab: create a local user](#lab-create-a-local-user)

---

## Common Users VS Local Users

- `CDB common user`

  - a database account that is created **in the root container** and is **inherited by all PDBs** in the CDB, including future PDBs
  - **can not have the same name** as any `local user` across all the PDBs.
  - e.g., sys, system

- When creating a common user , but DBA need **user defined prefix** `C##`

  - e.g., `C##KHALED`

- The **user defined prefix** can be defined in **parameter** called `common_user_prefix`

![common_user_prefix](./pic/common_user_prefix.png)

---

- `Local user`
  - DB user created **in a specific PDB**
  - e.g., HR user in PDB orclpdb
  - can create same local account and password **in more than one PDB**
  - e.g.,:
    - HR user in PDB called pdb1,
    - HR user in PDB called pdb2,
    - HR user in PDB called pdb3

---

### Lab: Query common users and local users

- Connect using sql developer
- Open all pdb

```sql
show con_name

--make sure that all pluggable is opned
select con_id,name,open_mode from v$pdbs;

alter pluggable database all open;
```

- Query all users

```sql
# show all users in container and pdbs
select username,common,con_id from cdb_users
order by username;
```

![lab_common_user01](./pic/lab_common_user01.png)

> note: sys and sysbackup are database administrate account. The result shows they have both in root and pdb.

---

- Query common user
  - common users exist both in root and pdb (con_id)

```sql
select username,common,con_id from cdb_users
where common='YES'
order by username;

select distinct(username) from cdb_users
where common='YES';
```

![lab_common_user](./pic/lab_common_user02.png)

---

- Query local user

```sql
select username,common,con_id from cdb_users
where common='NO'
order by username;
```

![lab_local_user01.png](./pic/lab_local_user01.png)

---

### Lab: Create a common user

- show the common_user_prefix

```sql
SHOW PARAMETER common_user_prefix
#NAME               TYPE   VALUE
#------------------ ------ -----
#common_user_prefix string C##
```

- When in root, create a user without the prefix will return an error.

```sql
show con_name;
#CON_NAME
#------------------------------
#CDB$ROOT

CREATE USER t1 IDentified by t1;
```

![lab_common_user](./pic/lab_common_user03.png)

---

- Create a common user using prefix

```sql

CREATE USER C##t1 IDentified by welcome;

select distinct(username) from cdb_users
where common='YES';
```

![lab_common_user](./pic/lab_common_user04.png)

---

### Lab: create a local user

- change session to a pdb
- Create a local user

```sql

alter session set container=orclpdb;

show con_name;
#CON_NAME
#------------------------------
#ORCLPDB

create user t1 identified by t1;

select username,common,con_id from cdb_users
where common='NO'
order by username;
```

![lab_local_user](./pic/lab_local_user02.png)

---

[TOP](#dba---users-common-users-vs-local-users)
