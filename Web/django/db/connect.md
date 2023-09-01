# Django - Database

[Back](../index.md)

- [Django - Database](#django---database)
  - [`settings.py` variables](#settingspy-variables)
  - [MySQL DB](#mysql-db)

---

## `settings.py` variables

- `DATABASES`
    - Default: `{}` (Empty dictionary)
    - A dictionary containing the settings for all databases to be used with Django. It is a nested dictionary whose contents map a database alias to a dictionary containing the options for an individual database.

- The `DATABASES` setting **must** configure a **default** database; any number of additional databases may also be specified.

```py
# default
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",
    }
}
```

- Options

| Options                       | Description                                      | Default |
| ----------------------------- | ------------------------------------------------ | ------- |
| `ENGINE`                      | The database backend to use.                     | `''`    |
| `HOST`                        | The host to use                                  | `''`    |
| `NAME`                        | The name of the database to use.                 | `''`    |
| `PASSWORD`                    | The password to use                              | `''`    |
| `PORT`                        | The port to use                                  | `''`    |
| `OPTIONS`                     | Extra parameters to use                          | `{}`    |
| `ATOMIC_REQUESTS`             | Wether wrap each view in a transaction.          | `False` |
| `AUTOCOMMIT`                  | Wether automatically commit transcation          | `True`  |
| `CONN_MAX_AGE`                | The lifetime of a database connection            | `0`     |
| `CONN_HEALTH_CHECKS`          | health check before connections are reused       | `False` |
| `TIME_ZONE`                   | the time zone for this database connection       | `None`  |
| `DISABLE_SERVER_SIDE_CURSORS` | Wether to disable the use of server-side cursors | `False` |
| `USER`                        | The username to use                              | `''`    |
| `TEST`                        | A dictionary of settings for test databases      | `{}`    |

- `ENGINE`: built-in db backends
  - `'django.db.backends.postgresql'`
  - `'django.db.backends.mysql'`
  - `'django.db.backends.sqlite3'`
  - `'django.db.backends.oracle'`

---

## MySQL DB

- `mysqlclient` is a native driver. It’s the recommended choice.
  - `pip install mysqlclient`

- Connection settings are used in this order:

  1. OPTIONS.
  2. NAME, USER, PASSWORD, HOST, PORT
  3. MySQL option files.

---

[Top](#django---database)

