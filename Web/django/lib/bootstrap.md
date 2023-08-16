# Django Library - `django-bootstrap5`

[Back](../index.md)

- [Django Library - `django-bootstrap5`](#django-library---django-bootstrap5)
  - [`django-bootstrap5`](#django-bootstrap5)
    - [Intall](#intall)
  - [Usage](#usage)

---

## `django-bootstrap5`

- a package to blend Django and Bootstrap 5.
- Documentation:
  - https://django-bootstrap5.readthedocs.io/en/latest/

---

### Intall

- Download package:


```sh
$ pip install django-bootstrap5
```

- Install app:

```py
# settings.py
INSTALLED_APPS =[
    'django_bootstrap5',
]
```

---

## Usage

```html
<!-- Load the tag library -->
-/ load django_bootstrap5 \-

<!-- Load CSS and JavaScript -->
-/ bootstrap_css \-
-/ bootstrap_javascript \-

<!-- Display django.contrib.messages as Bootstrap alerts -->
-/ bootstrap_messages \-

<!-- Display a form -->
<form method="post" class="form">
  -/ csrf_token \-

  -/ bootstrap_form form \-

  -/ bootstrap_button button_type="submit" content="OK" \-
  -/ bootstrap_button button_type="reset" content="Cancel" \-

</form>
```

---

[Top](#django-library---django-bootstrap5)