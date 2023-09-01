# Django - Database Connection: `MySQL`

[Back](../index.md)

- [Django - Database Connection: `MySQL`](#django---database-connection-mysql)
  - [Prerequisites](#prerequisites)
  - [Create Database using SQL](#create-database-using-sql)
  - [Create Django Project](#create-django-project)
  - [Install `mysqlclient` Package](#install-mysqlclient-package)
  - [Run `migrate` Command](#run-migrate-command)
  - [Install `MySQL` in Linux](#install-mysql-in-linux)
  - [Create a Dedicated MySQL User and Granting Privileges](#create-a-dedicated-mysql-user-and-granting-privileges)
  - [Create Database](#create-database)


---

## Prerequisites

- MySQL server 5.7+ must be installed
- Python 3.0+ must be installed

---

## Create Database using SQL

```sql
CREATE DATABASE db_name;
```

---

## Create Django Project

- Configures database: `settings.py`

```py
DATABASES = {  
    # overrides the default db
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'db_name',  # db name 
        'USER': 'root',     
        'PASSWORD': 'your_password',  
        'HOST': '127.0.0.1',  
        'PORT': '3306',  
        'OPTIONS': {  
            # used to handle the invalid or missing values from being stored in the database by INSERT and UPDATE statements.
            # STRICT_TRANS_TABLES mode: If a value could not be inserted as given into a transactional table, abort the statement.
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }  
    }  
}  
```

---

## Install `mysqlclient` Package

- `mysqlclient`
  - the `Python` interface to `MySQL` that allows `Python` project to connect to the `MySQL` server.

```sh
pip install mysqlclient
```

---

## Run `migrate` Command

- Run the migrate command to create tables in the target database.
    - Django will automatically create the necessary tables such as `auth_group`, `auth_user`, `auth_permission`, etc. It will also create the tables which are defined in the `models.py` file.


```sh
# CLI
python manage.py migrate  
```

- To check outcome of migrate

```sql
/* mysql */
use db_name;
show tables;
```

---

## Install `MySQL` in Linux

- Install MySQL

```sh
sudo apt-get install mysql-server
```

- Set your password strength accordingly, included:
    - remove some anonymous users and the test database, 
    - disable remote root logins,
    - and load these new rules 

```sh
sudo mysql_secure_installation
```

---

##  Create a Dedicated MySQL User and Granting Privileges

- start the MySQL

```sh
# start MySQL service
sudo systemctl start mysql

# display status
systemctl status mysql.service
# ● mysql.service - MySQL Community Server
#      Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
#      Active: active (running) since Sat 2023-08-26 22:00:29 UTC; 2h 29min ago
#    Main PID: 35751 (mysqld)
#      Status: "Server is operational"
#       Tasks: 39 (limit: 1141)
#      Memory: 370.4M
#         CPU: 36.051s
#      CGroup: /system.slice/mysql.service
#              └─35751 /usr/sbin/mysqld
```

- started with MySQL go to the root directory

```sh
sudo mysql -u root
```

- Creating a dedicated database user

```sql
/* mysql */
/* 
1. Create a new user with username and host
    If the dedicated user can be access from Ubuntu System, host is 'localhost'.
 */
CREATE USER 'adam'@'localhost' IDENTIFIED BY '123456';


/* 
2. Grant new user the appropriate privileges

Grant all privileges on specified database.
Not recommanded:
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'LOCALHOST'; 
 */

/* Grant explicit privileges on all databases and tables */
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, INDEX, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'username'@'localhost' WITH GRANT OPTION;

/* 
3. Free up any memory that the server cached.
*/
FLUSH PRIVILEGES;

/* 
4. exit 
*/
exit;

```

---

## Create Database

```sql

/* 
new MySQL user can log in with PWD  
*/
mysql -u username -p


CREATE DATABASE database_name;
```

---

[TOP](#django---database-connection-mysql)
