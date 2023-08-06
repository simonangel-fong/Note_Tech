# Django - Authentication Views

[Back](../index.md)

- [Django - Authentication Views](#django---authentication-views)
  - [Authentication Views](#authentication-views)
    - [`django.contrib.auth.views` Module](#djangocontribauthviews-module)
  - [Built-in forms](#built-in-forms)
  - [Authentication data in templates](#authentication-data-in-templates)
  - [Managing users in the admin](#managing-users-in-the-admin)

---

## Authentication Views

- Django provides several views that you can use for handling login, logout, and password management.
- Django provides **no default template** for the authentication views. Developer should create templates for the views.

- Url
    - `django.contrib.auth.urls`

  ```py
  urlpatterns = [
      path("accounts/", include("django.contrib.auth.urls")),
  ]
  ```

---

### `django.contrib.auth.views` Module

- List of Authentication View

| View Class                  | Patterns                           | Name                      |
| --------------------------- | ---------------------------------- | ------------------------- |
| `LoginView`                 | `accounts/login/`                  | `login`                   |
| `LogoutView`                | `accounts/logout/`                 | `logout`                  |
| `PasswordChangeView`        | `accounts/password_change/`        | `password_change`         |
| `PasswordChangeDoneView`    | `accounts/password_change/done/`   | `password_change_done`    |
| `PasswordResetView`         | `accounts/password_reset/`         | `password_reset`          |
| `PasswordResetDoneView`     | `accounts/password_reset/done/`    | `password_reset_done`     |
| `PasswordResetCompleteView` | `accounts/reset/<uidb64>/<token>/` | `password_reset_confirm`  |
| `PasswordResetCompleteView` | `accounts/reset/done/`             | `password_reset_complete` |

- Method

| Method              | Description                                                              |
| ------------------- | ------------------------------------------------------------------------ |
| `logout_then_login` | Log out the user if they are logged in. Then redirect to the login page. |
| `redirect_to_login` | Redirect the user to the login page, passing the given 'next' page.      |

---

- Example of login.html

```html
-/ extends "base.html" \-

-/ block content \-

-/ if form.errors \-
<p>Your username and password didn't match. Please try again.</p>
-/ endif \-

-/ if next \-
    -/ if user.is_authenticated \-
    <p>Your account doesn't have access to this page. To proceed,
    please login with an account that has access.</p>
    -/ else \-
    <p>Please login to see this page.</p>
    -/ endif \-
-/ endif \-

<form method="post" action="-/ url 'login' \-">
-/ csrf_token \-
<table>
<tr>
    <td>-- form.username.label_tag --</td>
    <td>-- form.username --</td>
</tr>
<tr>
    <td>-- form.password.label_tag --</td>
    <td>-- form.password --</td>
</tr>
</table>

<input type="submit" value="login">
<input type="hidden" name="next" value="-- next --">
</form>

{# Assumes you set up the password_reset view in your URLconf #}
<p><a href="-/ url 'password_reset' \-">Lost password?</a></p>

-/ endblock \-
```

---

## Built-in forms

- built-in forms located in `django.contrib.auth.forms`


| Form                      | Description                                                            |
| ------------------------- | ---------------------------------------------------------------------- |
| `AdminPasswordChangeForm` | changes a user’s password **in the admin interface**                   |
| `UserChangeForm`          | change a user’s information and permissions **in the admin interface** |
| `AuthenticationForm`      | logs a user in.                                                        |
| `PasswordChangeForm`      | allows a user to change their password.                                |
| `PasswordResetForm`       | generates and emails a one-time use link to reset a user’s password.   |
| `SetPasswordForm`         | lets a user change their password without entering the old password.   |
| `UserCreationForm`        | creates a new user.                                                    |

---

## Authentication data in templates

- The currently logged-in **user** and their **permissions** are made available in the template context

---

- `user`
  - either a `User` instance or an `AnonymousUser` instance, is stored in the template variable -- user --:

- Example

  ```html
  -/ if user.is_authenticated \-
      <p>Welcome, -- user.username --. Thanks for logging in.</p>
  -/ else \-
      <p>Welcome, new user. Please log in.</p>
  -/ endif \-
  ```

---

- `perms`
    -  the template variable storing currently logged-in user’s permissions

- Example:

  ```html
  <!-- if the logged-in user has any permissions in the foo app -->
  -/ if perms.foo -\

  <!-- if the logged-in user has the permission foo.add_vote -->
  -/ if perms.foo.add_vote \-


  <!-- complete example of checking permissions in a template -->
  -/ if perms.foo \-
      <p>You have permission to do something in the foo app.</p>
      -/ if perms.foo.add_vote \-
          <p>You can vote!</p>
      -/ endif \-
      -/ if perms.foo.add_driving \-
          <p>You can drive!</p>
      -/ endif \-
  -/ else \-
      <p>You don't have permission to do anything in the foo app.</p>
  -/ endif \-

  <!-- look permissions up by -/ if in \- statements -->
  -/ if 'foo' in perms \-
      -/ if 'foo.add_vote' in perms \-
          <p>In lookup works, too.</p>
      -/ endif \-
  -/ endif \-
  ```

---

## Managing users in the admin

- Require both `django.contrib.admin` and `django.contrib.auth` be install
- Django admin site provides a convenient way to view and manage users, groups, and permissions.
  
---

[TOP](#django---authentication-views)
