# Django - Setting

[Back](../index.md)

- [Django - Setting](#django---setting)
  - [URL](#url)
    - [`ROOT_URLCONF`](#root_urlconf)
  - [Models](#models)
    - [`INSTALLED_APPS`](#installed_apps)
  - [Templates](#templates)
    - [`TEMPLATES`](#templates-1)
      - [`BACKEND`](#backend)
      - [`NAME`](#name)
      - [`DIRS`](#dirs)
      - [`APP_DIRS`](#app_dirs)
      - [`OPTIONS`](#options)
  - [Static Files](#static-files)
    - [`STATIC_ROOT`](#static_root)
    - [`STATIC_URL`](#static_url)
    - [`STATICFILES_DIRS`](#staticfiles_dirs)
  - [Authentication](#authentication)

---

## URL

### `ROOT_URLCONF`

- A string representing the full Python import path to your root URLconf, for example "mydjangoapps.urls".
- Can be overridden on a per-request basis by setting the attribute urlconf on the incoming HttpRequest object.

- Default:
  ```py
  ROOT_URLCONF = '<proj_name>.urls'
  ```

---

## Models

### `INSTALLED_APPS`

- A list of strings designating **all applications** that are enabled in this Django installation. Each string should be a dotted Python path to:

  - an application configuration class (preferred), or
  - a package containing an application.

- If the app is not included in `INSTALLED_APPS` variable, it will cause `TemplateDoesNotExist` error.

---

## Templates

### `TEMPLATES`

- A list containing the settings for all template engines to be used with Django. Each item of the list is a dictionary containing the options for an individual engine.

- Default: `[]` (Empty list)

---

#### `BACKEND`

- The template backend to use. The built-in template backends are:

  - `django.template.backends.django.DjangoTemplates`
  - `django.template.backends.jinja2.Jinja2`

---

#### `NAME`

- The alias for this particular template engine.
- Aliases must be unique across all configured template engines.

- It defaults to the name of the module defining the engine class.

- Default: Not defined

---

#### `DIRS`

- Directories **where the engine should look for template source files**, in search order.

- Default: [] (Empty list)

---

#### `APP_DIRS`

- Whether the engine should look for template source files inside installed applications.
- The default `settings.py` file created by `django-admin startproject` sets `'APP_DIRS': True`.
- Default: `False`

---

#### `OPTIONS`

- Extra parameters to pass to the template backend. Available parameters vary depending on the template backend.
- Default: `{}` (Empty dict)

---

## Static Files

Settings for `django.contrib.staticfiles`.

### `STATIC_ROOT`

- The **absolute path to the directory** where `collectstatic` will collect static files for deployment.

- Default: `None`

- Example:
  ```py
  STATIC_ROOT = '/var/www/example.com/static/'
  ```

---

### `STATIC_URL`

- URL to use when referring to static files located in `STATIC_ROOT`.
- Default: `None`
- Example:

  ```py
  STATIC_URL = "static/"    # Default
  STATIC_URL = "http://static.example.com/"
  ```

---

### `STATICFILES_DIRS`

- defines a list of the additional locations the for global static file.

- Default: `[]` (Empty list)

- Example:

  ```py
  STATICFILES_DIRS = [
    "/home/special.polls.com/polls/static",
    "/home/polls.com/polls/static",
    "/opt/webfiles/common",
  ]
  ```

- **Prefixes (optional)**

  - refers to files in one of the locations with an additional **namespace**, a prefix in the `(prefix, path)` tuples can be optionally provided.
  - Example:
    ```py
    STATICFILES_DIRS = [
      # ...
      ("downloads", "/opt/webfiles/stats"),
    ]
    ```

---

## Authentication

| Variable              | Description                                        |
| --------------------- | -------------------------------------------------- |
| `LOGIN_REDIRECT_URL`  | the url where requests are redirected after login  |
| `LOGIN_URL`           | the url where requests are redirected for login    |
| `LOGOUT_REDIRECT_URL` | the url where requests are redirected after logout |

---

[TOP](#django---setting)
