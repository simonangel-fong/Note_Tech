# Django Library - `django-debug-toolbar`

[Back](../index.md)

- [Django Library - `django-debug-toolbar`](#django-library---django-debug-toolbar)
  - [Django Debug Toolbar](#django-debug-toolbar)
    - [Intall](#intall)
    - [Prerequisites](#prerequisites)
    - [Install the App](#install-the-app)
    - [Add the URLs](#add-the-urls)
    - [Add the Middleware](#add-the-middleware)
    - [Configure Internal IPs](#configure-internal-ips)

---

## Django Debug Toolbar

- A library for debut django.
- ref: https://django-debug-toolbar.readthedocs.io/en/latest/

---

### Intall
  
```sh
$ python -m pip install django-debug-toolbar
```

---

### Prerequisites

1. Ensure that 'django.contrib.staticfiles' is in your INSTALLED_APPS setting, and configured properly:
2. Ensure that your `TEMPLATES` setting contains a `DjangoTemplates` backend whose `APP_DIRS` options is set to `True`
```py
# settings.py
INSTALLED_APPS = [
    "django.contrib.staticfiles",
]

STATIC_URL = "static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]
```

---

### Install the App

```py
INSTALLED_APPS = [
    "debug_toolbar",
]
```

---

### Add the URLs

```py
from django.urls import include, path

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),  # __debug__ can be any url prefix that do not clash with URLConfs.
]
```

---

###  Add the Middleware

```py
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
```

---

### Configure Internal IPs

```py
INTERNAL_IPS = [
    "127.0.0.1",        # debut message will display on this url.
]
```

---

[Top](#django-library---django-debug-toolbar)
