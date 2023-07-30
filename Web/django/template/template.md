# Django - Template

[Back](../index.md)

- [Django - Template](#django---template)
  - [Template](#template)
  - [Template Structure](#template-structure)
    - [App Level](#app-level)
    - [Project Level](#project-level)
  - [Template Error](#template-error)
  - [Django template language](#django-template-language)
    - [Variables](#variables)
    - [Tags](#tags)
    - [Filters](#filters)
    - [Comments](#comments)

---

## Template

- A `template` contains the **static parts** of the desired HTML output as well as some special syntax describing how **dynamic content** will be inserted.

---

## Template Structure

- Two main ways to organize template structure in Django:

  - 1. the default app-level way
  - 2. a custom project-level approach.

- When Django loads template, it will look for the `TEMPLATES` variable in the `settings.py`

  - By default, `DIRS` key is an empty list and the `APP_DIRS` is `True`. Then Djanto will look for `templates` folder within each app foler.
  - If `DIRS` key is a list of paths, Django will look for `templates` folder in those paths. No matter the value of `APP_DIRS`.
  - If `DIRS` key is an empty list and `APP_DIRS` is `False`, django will return a `TemplateDoesNotExist` error.

- The default Django template loader will try to load the template from the **project-level directory first**. In other words, `DIRS` is searched before `APP_DIRS`.

---

### App Level

- By default, the Django template loader will look within each app for a templates folder.
- But to avoid namespace issues, a folder with the app name should be created below the app level template folder.

- **Approach**

  1. Creates a new folder with the name of `template`.
  2. Creates a new folder with the name of `<app_name>` under the the template folder.
  3. Creates html files within the `<app_name>` folder

- **Strucure**:

  - `manage.py`
  - `<proj_name>/`: folder for project

    - `__init__.py`
    - `settings.py`
    - `urls.py`
    - `wsgi.py`

  - `<app_name>/`: folder for application

    - `__init__.py`
    - `admin.py`
    - `apps.py`
    - `models.py`
    - `tests.py`
    - `views.py`
    - `templates/`: folder for templates
      - `<app_name>/`: folder repeating app name to prevent namespace issues
        - `.html`: html files

- **Setings.py**
  - No additional update for `TEMPLATES` variable in `settings.py`
    ```py
    TEMPLATES = [
        {
            'DIRS': [],     # by default, DIRS is an empty list
            'APP_DIRS': True,   # True when settings.py file is created. But default value is False.
        },
    ]
    ```

---

### Project Level

- It's often more convenient to have all the templates in one place rather than hunting for them within multiple apps.

- **`Settings.py`**: Update the `DIRS` config under `TEMPLATES`.

  ```py
  # settings.py
  TEMPLATES = [
      {
          'DIRS': [Path(BASE_DIR, 'templates'),],   # locate the templates folder under the BASE_DIR.
          'APP_DIRS': True,
      },
  ]
  ```

- **Strucure**:

  - `manage.py`

  - `<proj_name>/`: folder for project

    - `__init__.py`
    - `settings.py`
    - `urls.py`
    - `wsgi.py`

  - `<app_name>/`: folder for application

    - `__init__.py`
    - `admin.py`
    - `apps.py`
    - `models.py`
    - `tests.py`
    - `views.py`

  - `templates/`: folder for templates
    - `<app_name>/`: folder repeating app name to prevent namespace issues
      - `.html`: html files

---

## Template Error

- `TemplateDoesNotExist at /`:
  - folder
    - templates folder incorrect.
    - app folder below the templates folder incorrect.
  - `settings.py`
    - `INSTALLED_APPS` does not include the application
    - the `APP_DIRS` key of `TEMPLATES` is `False`, but the `DIRS` key is empty list or incorrect.
  - `view.py`
    - `template_name` value in `render` function incorrect.

---

## Django template language

- A Django template is a text document or a **Python string marked-up** using the Django template language.

- A template is rendered with a context. Rendering replaces variables with their values, which are looked up in the context, and executes tags. Everything else is output as is.

- The syntax of the Django template language involves four constructs:
  - Variables

---

### Variables

- `variable`:

  - outputs a value from the context, which is a dict-like object mapping keys to values.

- Variables are surrounded by `{{` and `}}` like this:

- Examples:

```django
{{ my_dict.key }}
{{ my_object.attribute }}
{{ my_list.0 }}
```

---

### Tags

- `Tags`

  - provide arbitrary **logic** in the rendering process.

- Tags are surrounded by { % % } like this

- Examples:

```django
__ csrf_token __

__ cycle 'odd' 'even' __    <!-- accept arguments -->

<!-- if -->
__ if user.is_authenticated __
  Hello, {{ user.username }}.
__ endif __
```

---

### Filters

- `Filters`:

  - transform the values of variables and tag arguments.

- Examples:

```django
{{ django|title }}

<!-- take an argument -->
{{ my_date|date:"Y-m-d" }}
```

---

### Comments

- `Comments`
- A `__ comment __` tag provides multi-line comments.

- Examples:

```django
{# this won't be rendered #}
```

---

[TOP](#django---template)
