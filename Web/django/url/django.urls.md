# Django - `django.urls`

[Back](../index.md)

- [Django - `django.urls`](#django---djangourls)
  - [URLconfs functions](#urlconfs-functions)
    - [`path()`](#path)
    - [`re_path()`](#re_path)
    - [`include()`](#include)
  - [Utility functions](#utility-functions)
    - [`reverse()`](#reverse)

---

## URLconfs functions

### `path()`

- Returns an element for inclusion in urlpatterns.

- Syntax:

  - `path(route, view, kwargs=None, name=None)`

- Parameter:

  - `route`: a string containing a URL pattern
  - `view`: a view function / `django.urls.include()`
  - `kwargs`: additional arguments to the view function or method.
    - eg.: `{"foo": "bar"}`

- Example:

```py
from django.urls import include, path

urlpatterns = [
    path("index/", views.index, name="main-view"),
    path("bio/<username>/", views.bio, name="bio"),     # capture value passed to view
    path("blog/", include("blog.urls")),        # include()
]
```

---

### `re_path()`

- Returns an element for inclusion in urlpatterns.

- Syntax:

  - `re_path(route, view, kwargs=None, name=None)`

- Parameter:

  - `route`: a string with a regular expression
    - use raw string syntax (`r''`)
  - `view`: a view function / `django.urls.include()`
  - `kwargs`: additional arguments to the view function or method.
    - eg.: `{"foo": "bar"}`

- Example:

  ```py
  from django.urls import include, re_path

  urlpatterns = [
      re_path(r"^index/$", views.index, name="index"),
      re_path(r"^bio/(?P<username>\w+)/$", views.bio, name="bio"),
      re_path(r"^blog/", include("blog.urls")),
      ...,
  ]
  ```

---

### `include()`

- takes a full Python import path to another URLconf module that should be “included” in this place.

- Whenever Django encounters `include()`, it **chops off** whatever part of the URL matched up to that point and **sends the remaining string** to the included URLconf for further processing.

- Syntax:

  ```py
  include(pattern_list)
  include(module, namespace=None)
  include((pattern_list, app_namespace), namespace=None)
  ```

- Parameters:

  - `module`:URLconf module (or module name)
  - `namespace (str)`:Instance namespace for the URL entries being included
  - `pattern_list`:Iterable of path() and/or `re_path`() instances.
  - `app_namespace (str)`:Application namespace for the URL entries being included

- Example:

  ```py
  from django.urls import include, path

  urlpatterns = [
      path("community/", include("aggregator.urls")),   # module
      path("contact/", include("contact.urls")),
  ]
  ```

---

## Utility functions

### `reverse()`

- If **no match** can be made, **reverse()** raises a `NoReverseMatch` exception

- Syntax:

  - `reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)`

- Parameter:

  - `viewname`: can be a URL pattern name or the callable view object.
  - `urlconf`: the `URLconf` module containing the URL patterns to use for reversing.
    - By default, the `root URLconf` for the current thread is used.
  - `args`: URL arguments of list type
  - `kwargs`: URL arguments of dict type

- Example:

```py
# url
from news import views
path("archive/", views.archive, name="news-archive")

# above url can be reverse as follow:
reverse("news-archive")     # using the named URL

from news import views
reverse(views.archive)      # passing a callable object

# use case with redirect http
from django.urls import reverse
def myview(request):
    return HttpResponseRedirect(reverse("arch-summary", args=[1945]))   # using args to pass value

# using kwargs
reverse("admin:app_list", kwargs={"app_label": "auth"}) # '/admin/auth/'

```

---

[TOP](#django---djangourls)
