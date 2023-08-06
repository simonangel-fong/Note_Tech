# Django - URL Dispatcher

[Back](../index.md)

- [Django - URL Dispatcher](#django---url-dispatcher)
  - [`URLconf`](#urlconf)
  - [How Django processes a request](#how-django-processes-a-request)
  - [What the URLconf searches against](#what-the-urlconf-searches-against)
  - [Sample `URLconf`](#sample-urlconf)
  - [`urls.py`](#urlspy)
  - [URL namespaces](#url-namespaces)
    - [Example: Namespace](#example-namespace)
    - [Example: Admin page](#example-admin-page)

---

## `URLconf`

- `URLconf` / `URL configuration`:
  - a Python module to design URLs for an app
  - a mapping between URL path expressions to Python functions(views).

---

## How Django processes a request

- When a user requests a page from a Django-powered site, this is the algorithm the system follows to determine which Python code to execute:
  - 1. Django determines the **root URLconf** module to use.
    - Ordinarily, this is the value of the `ROOT_URLCONF` setting, but if the incoming HttpRequest object has a urlconf attribute (set by middleware), its value will be used in place of the `ROOT_URLCONF` setting.
  - 2. Django loads that Python module and looks for the **variable urlpatterns**.
    - This should be a sequence of `django.urls.path()` and/or `django.urls.re_path()` instances.
  - 3. Django runs through each URL pattern, **in order**, and **stops at the first one** that matches the requested `URL`, matching against `path_info`.
  - 4. Once one of the URL patterns **matches**, Django imports and **calls the given view**, which is a Python function (or a class-based view).
    - The view gets passed the following **arguments**:
      - An instance of **HttpRequest**.
      - If the matched URL pattern contained **no named groups**, then the matches from the regular expression are provided as **positional arguments**.
      - The **keyword arguments** are made up of any named parts matched by the path expression that are provided, overridden by any arguments specified in the optional kwargs argument to `django.urls.path()` or `django.urls.re_path()`.
  - 5.  If **no URL pattern matches**, or if **an exception is raised** during any point in this process, Django invokes an appropriate `error-handling` view.

---

## What the URLconf searches against

- The `URLconf` searches against the **requested URL**, as a normal Python string.

- This does **not include** `GET` or `POST` parameters, or the **domain name**.

  - For example, in a request to `https://www.example.com/myapp/`, the URLconf will look for `myapp/`.

  - In a request to `https://www.example.com/myapp/?page=3`, the URLconf will look for `myapp/`.

- The URLconf **doesn’t look at the request method**.
  - In other words, all request methods – `POST`, `GET`, `HEAD`, etc. – will be **routed to the same** function for the same URL.

---

## Sample `URLconf`

```py
from django.urls import path

from . import views

urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    path("articles/<int:year>/", views.year_archive),
    path("articles/<int:year>/<int:month>/", views.month_archive),
    path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
]
```

- Notes:

  - To **capture a value** from the URL, use **angle brackets**. eg: `<int:year>`
  - Captured values can optionally **include a converter type**.
    - For example, use `<int:name>` to capture an integer parameter.
    - If a converter isn’t included, **any string**, excluding a / character, is matched.
    - There’s **no need to add a leading slash**, because every URL has that.
      - For example, it’s `articles`, not `/articles`.

- Example requests:

  - A request to `/articles/2005/03/` would match the third entry in the list. Django would call the function `views.month_archive(request, year=2005, month=3)`.
  - `/articles/2003/` would match the first pattern in the list, not the second one, because the patterns are tested in order, and the first one is the first test to pass. Here, Django would call the function `views.special_case_2003(request)`.
  - `/articles/2003/03/building-a-django-site/` would match the final pattern. Django would call the function `views.article_detail(request, year=2003, month=3, slug="building-a-django-site")`.
  - `/articles/2003` would not match any of these patterns, because **each pattern requires that the URL end with a slash**.

---

## `urls.py`

- a `.py` file to store URLconf variable `urlpatterns`.

- `urlpatterns` should be a sequence of `path()` and/or `re_path()` instances.

---

## URL namespaces

- `URL namespaces`
  - allow to uniquely reverse named URL patterns even if **different applications use the same URL names**. 
  - It’s a good practice for third-party apps to always use namespaced URLs.

- A URL namespace comes in two parts:
  - `application namespace`
    - the name of the application that is being deployed.
    - Every instance of a single application will have the same application namespace.

  - `instance namespace`
    - identifies a specific instance of an application
    - should be unique across your entire project.
    - The instance namespce for the default instance of an application can be the same as the application namespace.

- Namespaced URLs:
  -  specified using the `:` operator. 
     -  `'admin:index'`: indicates a namespace of 'admin', and a named URL of 'index'.
  -  Namespaces can also be nested.
     -  `'sports:polls:index'`: look for a pattern named 'index' in the namespace 'polls' that is itself defined within the top-level namespace 'sports'.

- 常见错误:
  - 引号内多余的空格: `' app_name:url'` , `'app_name:url '`, `'app_name :url'`, or `'app_name: url'`都不能匹配`'app_name:url'`

- Application namespaces of included URLconfs can be specified using `app_name = '<app_name>'`

---

### Example: Namespace

- `urls.py` at the project level

```py
# both url refering to the same urls.py file. 
# But due to the defferent namespace, urls have different prefix.
path('employee/', include("EmpApp.urls",namespace="employee")),
path('department/', include("EmpApp.urls",namespace="department")),
```

- `urls.py` within EmpApp application

```py
app_name = "EmpApp"

urlpatterns = [
    path("", view=views.emp_list, name="index"),
    path("emp/list/", view=views.emp_list, name="emp_list"),
    path("emp/update/<int:emp_id>", view=views.emp_update, name="emp_update"),

    path("dept/list/", view=views.dept_list, name="dept_list"),
    path("dept/update/<int:dept_id>", view=views.dept_update, name="dept_update"),
]
```

- Template:

```html
<!-- 
  Using `employee:url`, to reverese the url as '/employee/'.
  Then further into '/employee/emp/list/
 -->
<a href="-/ url 'employee:emp_list' -\">List</a>

<!-- 
  Using `department:url`, to reverese the url as '/department/'.
  Then further into '/department/dept/list/
 -->
<a href="-/ url 'department:dept_list' -\">List</a>


<!-- 
  EmpApp is an application namespace which defined in the EmpApp's urls.py.
  Djnago locate this url file to find emp_detail url
 -->
<a href="-/ url 'EmpApp:emp_detail' emp.id -\">Edit</a>
```

---

### Example: Admin page

- Admin page can be call by
  - Using the row url: 
    - `<a href='/admin/'>Admin</a>`
  - Using namespace`admin`:
    -  `<a href='-/ url 'admin:index' -\'>Admin</a>`

---

[TOP](#django---url-dispatcher)
