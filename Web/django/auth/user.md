# Django - User Object

[Back](../index.md)

- [Django - User Object](#django---user-object)
  - [User objects](#user-objects)
    - [Creates users](#creates-users)
    - [Creates superusers](#creates-superusers)
    - [Changing passwords](#changing-passwords)
    - [Authenticating users](#authenticating-users)
  - [`User`](#user)
    - [`models.UserManager`](#modelsusermanager)
    - [Example](#example)
  - [`AnonymousUser`](#anonymoususer)

---


## User objects

- `User` objects
  - represent the people interacting with site 
  - enable things like restricting access, registering user profiles, associating content with creators etc.
  - the core of the authentication system. 

- Only one class of user exists in Django’s authentication framework, i.e., `'superusers'` or admin `'staff'` users are just user objects with special attributes set, not different classes of user objects.

- The primary attributes of the default user are:
  - username
  - password
  - email
  - first_name
  - last_name

---

### Creates users

- Using `create_user()`

  ```py
  from django.contrib.auth.models import User

  user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
  # At this point, user is a User object that has already been saved
  # to the database.
  ```

---

### Creates superusers

- CLI

  ```sh
  py manage.py createsuperuser --username=joe --email=joe@example.com
  ```

- A promt for password will be prompted.
- After you enter one, the user will be created immediately. 
- If you leave off the `--username` or -`-email` options, it will prompt you for those values.

---

### Changing passwords

- CLI

  ```sh
  manage.py changepassword user_name 
  ```

- Using `set_password`

  ```py
  from django.contrib.auth.models import User

  u = User.objects.get(username="john")
  u.set_password("new password")
  u.save()
  ```

---

### Authenticating users

- Using `authenticate()` to verify a set of credentials.
  - Returns
    - a `User` object if the credentials are valid
    - `None` if the credentials aren’t valid

```py
from django.contrib.auth import authenticate

user = authenticate(username="john", password="secret")
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials
```



---

## `User`

- Package:
  - `django.contrib.auth.models`

- **Fields**

| Fields             | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `username`         | Required. < 150 characters                             |
| `password`         | Required. Raw passwords can be arbitrarily long        |
| `first_name`       | Optional. < 150 characters. (`blank=True`)             |
| `last_name`        | Optional. < 150 characters. (`blank=True`)             |
| `email`            | Optional. Email address (`blank=True`)                 |
| `groups`           | Many-to-many relationship to **Group**                 |
| `user_permissions` | Many-to-many relationship to **Permission**            |
| `is_staff`         | Whether this user can access the admin site            |
| `is_active`        | whether this user account should be considered active. |
| `is_superuser`     | whether this user has all permissions                  |
| `last_login`       | A datetime of the user’s last login.                   |
| `date_joined`      | when the account was created.                          |

- **Attributes**

| Attributes         | Description                                    |
| ------------------ | ---------------------------------------------- |
| `is_authenticated` | Read-only. if the user has been authenticated. |
| `is_anonymous`     | Read-only. if the user has been authenticated. |

- **Methods**

| Methods                        | Description                                                          |
| ------------------------------ | -------------------------------------------------------------------- |
| `get_username()`               | the username for the user.                                           |
| `get_full_name()`              | the first_name plus the last_name.                                   |
| `get_short_name()`             | the first_name.                                                      |
| `set_password(raw_password)`   | Sets the user’s password                                             |
| `check_password(raw_password)` | if the given raw string is the correct password for the user.        |
| `set_unusable_password()`      | Marks the user as having no password set.                            |
| `has_usable_password()`        | if `set_unusable_password()` has been called for this user.          |
| `get_user_permissions()`       | a set of permission strings that the user has directly               |
| `get_group_permissions()`      | a set of permission strings that the user has, through their groups. |
| `get_all_permissions()`        | a full set of permission strings that the user has                   |
| `has_perm(perm)`               | if the user has the specified permission                             |
| `has_perms(perm_list)`         | if the user has each of the specified permissions                    |
| `has_module_perms(package)`    | if the user has any permissions in the given package                 |
| `email_user()`                 | Sends an email to the user.                                          |


---

### `models.UserManager`


- **`objects` attribure:**

  - the default name of `UserManager` instance, the interface through which Django models take database query operations.
  - used to retrieve the instances from the database.

    ```py
    type(User.objects)
    # django.contrib.auth.models.UserManager
    ```

- **Methods**

| Method                       | Description                                        |
| ---------------------------- | -------------------------------------------------- |
| `create_user(username)`      | Creates, saves and returns a User.                 |
| `create_superuser(username)` | Creates, saves and returns a Superuser.            |
| `with_perm(perm)`            | Returns users that have the given permission perm. |

---


### Example

```py
# py manage.py shell
user = User.objects.create_user('john',"lennon@thebeatles.com", 'johnpassword')
user                                    # <User: john>
user.username                           # 'john'
user.email                              # lennon@thebeatles.com'
user.is_authenticated                   # True
user.is_anonymous                       # False
user.get_username()                     # 'john'
user.check_password('johnpassword')     # True
user.get_all_permissions()              # set()
```




---

## `AnonymousUser`

- Package:
  - `django.contrib.auth.models.AnonymousUser`

- `AnonymousUser` is a class that implements the `User` interface, with these differences:
  - `id` is always `None`.
  - `username` is always the empty string.
  - `get_username()` always returns the empty string.
  - `is_anonymous` is `True`
  - `is_authenticated` is `False`
  - `is_staff` and `is_superuser` are always `False`.
  - `is_active` is always `False`.
  - `groups` and `user_permissions` are always empty.
  - `set_password()`, `check_password()`, `save()` and `delete()` raise `NotImplementedError`.

- In practice, developer probably won’t need to use `AnonymousUser` objects on your own, but they’re used by web requests.

---

[TOP](#django---user-object)
