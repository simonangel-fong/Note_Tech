# Django - Meta

[Back](../index.md)

- [Django - Meta](#django---meta)
  - [Meta](#meta)
  - [Meta options](#meta-options)
  - [`_Meta`](#_meta)
    - [Attributes](#attributes)
    - [Methods](#methods)
    - [Example: Get Fields Info](#example-get-fields-info)

---

## Meta

- `Meta`:
  - the Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table), or human-readable singular and plural names (verbose_name and verbose_name_plural).
- None are required, and adding `class Meta` to a model is completely optional.

---

## Meta options

- Meta

| Meta Opt              | Description                                         |
| --------------------- | --------------------------------------------------- |
| `db_table`            | name of the database table                          |
| `verbose_name`        | A human-readable name for the object                |
| `verbose_name_plural` | The plural name for the object                      |
| `abstract`            | Wheter the current model is an abstract base class. |
| `db_table_comment`    | comment on the database table                       |
| `label`               | read-only, returns `app_label.object_name`          |
| `label_lower`         | read-only, returns `app_label.object_name`          |

- Contraint

| Meta Opt          | Description                                      |
| ----------------- | ------------------------------------------------ |
| `constraints`     | A list of constraints                            |
| `unique_together` | Sets of field names that must be unique together |

- index

| Meta Opt         | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `indexes`        | A list of indexes                                     |
| `index_together` | Sets of field names that, taken together, are indexed |
| `db_tablespace`  | name of the database tablespace                       |

- Order

| Meta Opt        | Description                                                 |
| --------------- | ----------------------------------------------------------- |
| `ordering`      | order by                                                    |
| `get_latest_by` | name(s) of a field for `latest()` and `earliest()` methods. |

---

## `_Meta`

- `_meta`:
  - a class provide access to meta data of models

### Attributes

```py
from EmpApp.models import Employee

# print(type(Employee.objects))   # <class 'django.db.models.manager.Manager'>
# print(Employee.objects.all())

# Some attributes of -meta
print(Employee._meta)                       # EmpApp.employee
print(Employee._meta.app_label)             # EmpApp
print(Employee._meta.apps)
# <django.apps.registry.Apps object at 0x0000024530DD1C70>
print(Employee._meta.model)                 # <class 'EmpApp.models.Employee'>
print(Employee._meta.db_table)              # EmpApp_employee
print(Employee._meta.verbose_name)          # employee
print(Employee._meta.model_name)            # employee
print(Employee._meta.object_name)           # Employee
print(Employee._meta.constraints)           # []
print(Employee._meta.fields)
# (<django.db.models.fields.BigAutoField: id>,
# <django.db.models.fields.CharField: first_name>,
# <django.db.models.fields.CharField: last_name>,
# <django.db.models.fields.EmailField: email>)
```

---

### Methods

| Methods                 | Description                                  |
| ----------------------- | -------------------------------------------- |
| `get_field(field_name)` | Returns the field instance with a fiel name. |
| `get_fields()`          | Returns a tuple of fields                    |

```py
from EmpApp.models import Employee

print(Employee._meta.get_field("first_name"))       # EmpApp.Employee.first_name
[print(type(f)) for f in Employee._meta.get_fields()]
# <class 'django.db.models.fields.BigAutoField'>
# <class 'django.db.models.fields.CharField'>
# <class 'django.db.models.fields.CharField'>
# <class 'django.db.models.fields.EmailField'>
```

---

### Example: Get Fields Info 

```py
from EmpApp.models import Employee

def initiate_dict(model):
  '''initiate a dict based on a model'''
    return dict.fromkeys([f.attname for f in model._meta.get_fields()])

print(initiate_dict(Employee))  # {'id': None, 'first_name': None, 'last_name': None, 'email': None}


def datatype_conversion(dict_data, Model):
    data = dict_data

    for field in Workout._meta.fields:                  #_meta.fields返回所有字段名
        # print(field.get_internal_type())
        if field.get_internal_type() == "DecimalField":     #get_internal_type()返回字段类型，是字符串
            data[field.attname] = float(data[field.attname])
        if field.get_internal_type() == "IntegerField":
            data[field.attname] = int(data[field.attname])
    return data
```

---

[TOP](#django---meta)
