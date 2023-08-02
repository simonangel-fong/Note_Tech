# Django - Model

[Back](../index.md)

- [Django - Model](#django---model)
  - [Model](#model)
  - [Migration](#migration)
  - [Example: Create model and migrate](#example-create-model-and-migrate)
    - [Create model class: `models.py`](#create-model-class-modelspy)
    - [Register Model: `settings.py`](#register-model-settingspy)
    - [Create Migration Files: `makemigrations`](#create-migration-files-makemigrations)
    - [Update Database: `migrate`](#update-database-migrate)
    - [List Migrations Files(Opetional): `showmigrations`](#list-migrations-filesopetional-showmigrations)
    - [Prit SQL Code(Optional): `sqlmigrate `](#prit-sql-codeoptional-sqlmigrate-)
  - [`Model` Class](#model-class)
    - [Exception](#exception)
    - [Attributes](#attributes)
    - [Instance method](#instance-method)

---

## Model

- `model`:

  - a class used to contain essential fields and methods.
  - Each model class **maps** to a single table in the database.
  - a subclass of `django.db.models.Model` and each **field** of the model class **represents a database field (column)**.

- `Model` is defined in `models.py` file of each application package.

- **Primary key fields**

  - Each model requires **exactly one field** to have primary_key=True (either explicitly declared or automatically added).

    - By default, Django gives each model an auto-incrementing primary key.
    - If specify a custom primary key, specify `primary_key=True` on one of fields.
    - If one of fields is explicitly set `Field.primary_key`, django won’t add the automatic id column.

- **SQL**

  - Table Name:

    - automatically derived from some model metadata
    - can be overridden.

  - CREATE TABLE SQL:
    - Django uses SQL tailored to the database backend specified in settings file.

- **`objects` attribure:**

  - the default name of `Manager` instance, the interface through which Django models take database query operations.
  - used to retrieve the instances from the database.

- **Model Methods**
  - Define custom methods on a model to add custom “row-level” functionality to objects.
  - a valuable technique for keeping business logic in one place – the model.

---

## Migration

- `Migration`:

  - a way of applying changes that have been made to a model, into the database schema.

- Django creates a **migration file** inside the **migration folder** for each model to create the table schema, and each table is mapped to the model of which migration is created.

- Command to perform migration:

| Command          | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| `makemigrations` | create a migration py file for the tabled schema of a model.        |
| `migrate`        | create table according to the schema defined in the migration file. |
| `sqlmigrate`     | show a raw SQL query of the applied migration.                      |
| `showmigrations` | lists out all the migrations and their status.                      |

---

## Example: Create model and migrate

### Create model class: `models.py`

- Create a new class which inherits from `models.Model`

- `<app_name> / models.py`:

```py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
```

---

### Register Model: `settings.py`

- Register model into the `INSTALLED_APPS` inside `settings.py`.

- `settings.py`:

```py
INSTALLED_APPS = [
  #...
  'app_name',
  #...
]
```

---

### Create Migration Files: `makemigrations`

- Creates new migrations based on the changes detected to models.

- CLI:

```sh
# create migration files for all apps
$ py manage.py makemigrations

# create migrations files for a specific app
$ py manage.py makemigrations app_label1 app_label2 ...
```

---

### Update Database: `migrate`

- `migrate`
  - Synchronizes the database state with the current set of models and migrations.

```sh
$ py manage.py migrate [app_label] [migration_name]
```

---

### List Migrations Files(Opetional): `showmigrations`

- `showmigrations`

  - Shows all migrations in a project

- CLI:

```sh
# show migrations for all apps
$ py manage.py showmigrations

# show migrations for specific apps
$ py manage.py showmigrations [app_label]

# return:
# EmpApp
#  [X] 0001_initial
```

---

### Prit SQL Code(Optional): `sqlmigrate `

- `sqlmigrate `
  - Prints the SQL for the named migration.
  - This requires an active database connection, which it will use to resolve constraint names;

```sh
$ py manage.py sqlmigrate app_label migration_name
# app_label: the name of current application
# migration_name: the name of migration file


# example:
$ py manage.py sqlmigrate EmpApp 0001
# return:
# BEGIN;
# --
# -- Create model Employee
# --
# CREATE TABLE "EmpApp_employee" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(32) NOT NULL, "last_name" varchar(32) NOT NULL, "email" varchar(254) NOT NULL);
# COMMIT;
```

---

## `Model` Class

- `django.db.models.Model`

### Exception

| Exception                       | Description                          |
| ------------------------------- | ------------------------------------ |
| `Model.DoesNotExist`            | when an expected object is not found |
| `Model.MultipleObjectsReturned` | when multiple objects are found      |

---

### Attributes

| Attributes      | Description                       |
| --------------- | --------------------------------- |
| `Model.objects` | the default name of the `Manager` |

---

### Instance method

- Contructor

| Method            | Description                     |
| ----------------- | ------------------------------- |
| `Model(**kwargs)` | instantiatie a model without db |

- Refereshing Object

| Method                  | Description                               |
| ----------------------- | ----------------------------------------- |
| `refresh_from_db()`     | reload a model’s values from the database |
| `get_deferred_fields()` | return the attribute names of all fields  |

- Validating

| Method                   | Description                      |
| ------------------------ | -------------------------------- |
| `clean_fields()`         | validate all fields on model     |
| `clean()`                | custom model validation          |
| `validate_unique()`      | validates uniqueness constraints |
| `validate_constraints()` | validates all constraints        |
| `full_clean()`           | call the above methods           |

- Saving objects

| Method     | Description                                        |
| ---------- | -------------------------------------------------- |
| `save()`   | insert / udpate **an** object back to the database |
| `delete()` | deletes the object in the database                 |

- Helping Method

| Method                     | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| `__str__()`                | display a model instance                               |
| `__eq__()`                 | compare primary key value                              |
| `get_absolute_url()`       | return a HTTP string to refer to the object            |
| `get_field_name_display()` | returns the “human-readable” value of the choice field |

---

[TOP](#django---model)
