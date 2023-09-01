# Django - Permissions and Groups

[Back](../../index.md)

- [Django - Permissions and Groups](#django---permissions-and-groups)
  - [Permission](#permission)
    - [`Permission` Class](#permission-class)
  - [Groups](#groups)
    - [`Group` Class](#group-class)

---

## Permission

- When `django.contrib.auth` is listed in `INSTALLED_APPS` setting, it will ensure that four default permissions – `add`, `change`, `delete`, and `view` – are created for each Django model defined in one of your installed applications.

- Default permissions for models will be created when `manage.py migrate` is run. 

- The `Permission` model is **rarely accessed directly**.

- Methods to check whether a user has these permissions on an application.
  - add: `user.has_perm('foo.add_bar')`
  - change: `user.has_perm('foo.change_bar')`
  - delete: `user.has_perm('foo.delete_bar')`
  - view: `user.has_perm('foo.view_bar')`

- Emxaple

```py
from django.contrib.auth import authenticate

user = authenticate(username="admin_name", password="admin_pwd")
user.has_perm("EmpApp.add_employee")
# True
user.get_all_permissions()
# {'EmpApp.add_department',
#  'EmpApp.add_employee',
#  'EmpApp.change_department',
#  'EmpApp.change_employee',
#  'EmpApp.delete_department',
#  'EmpApp.delete_employee',
#  'EmpApp.view_department',
#  'EmpApp.view_employee',
#  'admin.add_logentry',
#  'admin.change_logentry',
#  'admin.delete_logentry',
#  'admin.view_logentry',
#  'auth.add_group',
#  'auth.add_permission',
#  'auth.add_user',
#  'auth.change_group',
#  'auth.change_permission',
#  'auth.change_user',
#  'auth.delete_group',
#  'auth.delete_permission',
#  'auth.delete_user',
#  'auth.view_group',
#  'auth.view_permission',
#  'auth.view_user',
#  'contenttypes.add_contenttype',
#  'contenttypes.change_contenttype',
#  'contenttypes.delete_contenttype',
#  'contenttypes.view_contenttype',
#  'sessions.add_session',
#  'sessions.change_session',
#  'sessions.delete_session',
#  'sessions.view_session'}
```

---

### `Permission` Class

- Module:
  - `django.contrib.auth.models`

- Fields

| Fields         | Description                                                     |
| -------------- | --------------------------------------------------------------- |
| `name`         | Required. <= 255 characters                                     |
| `content_type` | Required. A reference to the django_content_type database table |
| `codename`     | Required. <= 100 characters                                     |

- Methods
  - Permission objects have the standard data-access methods like any other Django model.

---

## Groups

- `Groups`
  - a convenient way to categorize users to give them some label, or extended functionality.
  - A user in a group **automatically has the permissions granted** to that group.

---

### `Group` Class

- Module:
  - `django.contrib.auth.models`

- Fields

| Fields        | Description                      |
| ------------- | -------------------------------- |
| `name`        | Required. <= 150 characters      |
| `permissions` | Many-to-many field to Permission |

- Example:

```py
group.permissions.set([permission_list])
group.permissions.add(permission, permission, ...)
group.permissions.remove(permission, permission, ...)
group.permissions.clear()
```

---

[TOP](#django---permissions-and-authorization)
