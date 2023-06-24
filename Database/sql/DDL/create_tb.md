# SQL - Create Table

[Back](../index.md)

- [SQL - Create Table](#sql---create-table)
	- [`CREATE TABLE`](#create-table)
		- [Example](#example)

---

## `CREATE TABLE`

- Syntax

```sql
CREATE TABLE tb_name (
    col_name datatype col_constraint,
    col_name datatype col_constraint,
    table_constraint
) INHERITS existing_tb_name;
```

---

### Example

```sql
-- create account table
DROP TABLE account;
CREATE TABLE account(
	user_id		SERIAL 			PRIMARY KEY,		-- primary key
	username	VARCHAR(50)		UNIQUE NOT NULL,	-- unique
	password	VARCHAR(50)		NOT NULL,			-- not null
	email 		VARCHAR(250)	UNIQUE NOT NULL,
	created_on	TIMESTAMP	    NOT NULL,
	last_login	TIMESTAMP
);


CREATE TABLE job(
	job_id		SERIAL 			PRIMARY KEY,
	job_name	VARCHAR(200)	UNIQUE NOT NULL
);


CREATE TABLE account_job(
	user_id		INTEGER		REFERENCES account(user_id),	-- foreign key
	job_id		INTEGER		REFERENCES job(job_id),
	hire_date	TIMESTAMP
);
```

---

[TOP](#sql---create-table)
