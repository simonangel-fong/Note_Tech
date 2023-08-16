# Django - `manage.py` Command

[Back](../index.md)

- [Django - `manage.py` Command](#django---managepy-command)
  - [Command Syntax](#command-syntax)
  - [Debug](#debug)
  - [Project](#project)
  - [Migrations](#migrations)
  - [Authentication](#authentication)
  - [Static Files](#static-files)

---


## Command Syntax

```sh
django-admin <command> [options]
manage.py <command> [options]
py -m django <command> [options]
```

---

## Debug

| Command     | Description                                          |
| ----------- | ---------------------------------------------------- |
| `help`      | display usage information                            |
| `version`   | display the current Django version                   |
| `runserver` | Starts a lightweight development web server          |
| `shell`     | Starts the Python interactive interpreter.           |
| `dbshell`   | Runs the command-line client for the database engine |

---

## Project

| Command        | Description                                  |
| -------------- | -------------------------------------------- |
| `startapp`     | Creates a Django app directory structure     |
| `startproject` | Creates a Django project directory structure |

---

## Migrations

| Command          | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| `makemigrations` | create a migration py file for the tabled schema of a model.        |
| `migrate`        | create table according to the schema defined in the migration file. |
| `sqlmigrate`     | show a raw SQL query of the applied migration.                      |
| `showmigrations` | lists out all the migrations and their status.                      |

---

## Authentication

| Command           | Description                 |
| ----------------- | --------------------------- |
| `createsuperuser` | Creates a superuser account |

---

## Static Files

| Command         | Description                                   |
| --------------- | --------------------------------------------- |
| `collectstatic` | Collects the static files into `STATIC_ROOT`. |

---

[TOP](#django---managepy)
