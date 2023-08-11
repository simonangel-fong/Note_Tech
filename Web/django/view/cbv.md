# Django - Class-based views

[Back](../index.md)

- [Django - Class-based views](#django---class-based-views)
  - [Class-based View](#class-based-view)
  - [Usage of generic views](#usage-of-generic-views)
    - [Example: `View`](#example-view)
  - [Handling forms](#handling-forms)
  - [Decorating class-based views](#decorating-class-based-views)
    - [Decorating in URLconf](#decorating-in-urlconf)
    - [Decorating the class](#decorating-the-class)
  - [CRUD](#crud)
    - [Example: CRUD](#example-crud)
      - [Create](#create)
      - [Detail](#detail)
      - [Update](#update)
      - [Delete](#delete)

---

## Class-based View

- `view`:
  - a callable which takes a request and returns a response.

- Django provides **base view classes** and all views inherit from the `View` class, which handles linking the view into the URLs, HTTP method dispatching and other common features.

- `RedirectView` provides a **HTTP redirect**.
- `TemplateView` extends the base class to make it also **render a template**.

---

## Usage of generic views

1. Passing pass attributes into the `as_view()` method when the view **is called in URLconf**.
   - It will override attributes set on the class.

   ```py
   # urls.py
   from django.urls import path
   from django.views.generic import TemplateView   # calling generic TemplateView

   urlpatterns = [
       path("about/", TemplateView.as_view(template_name="about.html")),   # passing attributes
   ]
   ```

2. Inheriting from an existing view and override attributes  or methods. Then add `as_view()` when called in URLconf

   ```py
   # some_app/views.py
   from django.views.generic import TemplateView

   class AboutView(TemplateView):
       template_name = "about.html"     # overriding template_name attribute
   ```

   ```py
   # urls.py
   from django.urls import path
   from some_app.views import AboutView

   urlpatterns = [
       path("about/", AboutView.as_view()),     
   ]
   ```

---

### Example: `View`

```py
# views.py
from django.http import HttpResponse
from django.views import View


class GreetingView(View):
    greeting = "Good Day"       # create an attribute
    
    # define get method to handle HTTP GET
    # identical to:
    # if request.method == "GET":
    #     return HttpResponse("result")
    def get(self, request):     
        return HttpResponse(self.greeting)


# urls.py
from django.urls import path
from myapp.views import MyView

urlpatterns = [
    path("about/", GreetingView.as_view(greeting="G'day")),
]
```

---

## Handling forms

- Using function-based view

```py
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyForm


def myview(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect("/success/")
    else:
        form = MyForm(initial={"key": "value"})

    return render(request, "form_template.html", {"form": form})
```

- Using class-based view

```py
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm       # import a cutomized form class


class MyFormView(View):
    form_class = MyForm     # assign form class
    initial = {"key": "value"}      # define initial for form class
    template_name = "form_template.html"    # define template for render

    # define a get method
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    # define a post method
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect("/success/")

        return render(request, self.template_name, {"form": form})
```

---

## Decorating class-based views

### Decorating in URLconf

- Example:

```py
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from .views import VoteView

urlpatterns = [
    path("about/", login_required(TemplateView.as_view(template_name="secret.html"))),
    path("vote/", permission_required("polls.can_vote")(VoteView.as_view())),
]
```

---

### Decorating the class

- The class definition need to be decorated, using `method_decorator` decorator.
  - apply the decorator to the `dispatch()` method of the class.

- Example:

1. Decorate the dispatch method
   ```py
   from django.contrib.auth.decorators import login_required
   from django.utils.decorators import method_decorator
   from django.views.generic import TemplateView


   class ProtectedView(TemplateView):
       template_name = "secret.html"

       @method_decorator(login_required)   # decorating the dispatch method
       def dispatch(self, *args, **kwargs):
           return super().dispatch(*args, **kwargs)
   ```

2. Decorate the class
   ```py
   @method_decorator(login_required, name="dispatch")
   class ProtectedView(TemplateView):
       template_name = "secret.html"
   ```

3. Multiple Decorators

    ```py
    decorators = [never_cache, login_required]

    @method_decorator(decorators, name="dispatch")
    class ProtectedView(TemplateView):
        template_name = "secret.html"

    @method_decorator(never_cache, name="dispatch")
    @method_decorator(login_required, name="dispatch")
    class ProtectedView(TemplateView):
        template_name = "secret.html"
    ```

---

## CRUD

- `CRUD`:
  - stands for Create Retrieve Update Delete

- Django provides Class-base Views for CRUD:
  - `CreateView`
  - `UpdateView`
  - `DeleteView`

---

### Example: CRUD

#### Create

- `views.py`

```py
class CompanyCreateView(CreateView):
    model = Company

    # fields attribute: A list of names of fields.
    fields = ["name",]

    # "template_name" attribute: The full name of a template
    #       Default: "app/model_form.html"
    # template_name = "CBVApp/com_add.html"
    
    # "success_url" attribute: The URL to redirect to when the form is successfully processed.
    # Default: the url set in model's get_absolute_url()
```

- `urls.py`

```py
app_name = "CBVApp"

urlpatterns = [
    # some urls
    path('create/', view=CompanyCreateView.as_view(), name="com_create"),
    # some urls
    ]
```

- templates: entry

```html
<a href="-/ url 'CBVApp:com_create' \-">Add New Company</a>
```

- templates: form

```html
-/ extends "layout/base.html" \- 
-/ block main \-
<h1>
  -/ if not form.instance.pk \- 
    Create Company 
  -/ else \- 
    Update Company 
  -/ endif \-
</h1>
<form method="post">
  -/ csrf_token \-
  --form.as_div--
  <button type="submit">
    Submit
  </button>
</form>
-/ endblock \-

```

---

#### Detail


- `views.py`

```py
class CompaneyDetailView(DetailView):
    model = Company

    # "context_object_name" attribute:  the name of the list object in the context
    #       Default: "model_detail"
    context_object_name = "company_info"
    template_name = "CBVApp/com_info.html"
```

- `urls.py`

```py
app_name = "CBVApp"

urlpatterns = [
    # DetailView requires pk as argument
    path('?<int:pk>/', view=CompaneyDetailView.as_view(), name="com_info"),
]
```

- template: entry

```html
<a href="--company.get_absolute_url--"> --company.name-- </a>
```

- template: form

```html
-/ extends "layout/base.html" \- 
-/ block main \-

<h1>Company Detail</h1>

-/ if not company_info \-
    <p>No Company Data</p>
-/ else \-
    <p><b>Company Name</b>--company_info--</p>

    <h2>Employees</h2>
    -/ if not company_info.employees \-
        <p>No Employee Data</p>
    -/ else \-

      <ul>
      -/ for emp in company_info.employees.all \-
        <li>--emp--</li>
      -/ endfor \-
      </ul>

    -/ endif \-


    <a href="-/ url 'CBVApp:com_list' \-">Back</a>
    <a href="-/ url 'CBVApp:com_update' pk=company_info.pk \-">Update</a>
    <a href="-/ url 'CBVApp:com_delete' pk=company_info.pk \-">Delete</a>
-/ endif \- 

-/ endblock \-
```

---

#### Update

- `views.py`

```py
class CompanyUpdateView(UpdateView):
    model = Company
    fields = ["name",]

    # "template_name" attribute: The full name of a template
    #       Default: "app/model_form.html"

    # "success_url" attribute: The URL to redirect to when the form is successfully processed.
    # Default: the url set in model's get_absolute_url()
```

- `urls.py`

```py
urlpatterns = [
    # UpdateView requires pk as argument
    path('update/<int:pk>', view=CompanyUpdateView.as_view(), name="com_update"),
]
```

- template: entry

```html
<a href="-/ url 'CBVApp:com_update' pk=company_info.pk \-">Update</a>
```

- template: form
  - reuse create form

---

#### Delete

- `views.py`

```py
class CompanyDeleteView(DeleteView):
    model = Company

    # "success_url" attribute: The URL to redirect to when the form is successfully processed.
    #   Default: For deletion, it usually redirects to the list url
    success_url = reverse_lazy("CBVApp:com_list")
```

- `urls.py`

```py
urlpatterns = [
    # DeleteView requires pk as argument
    path('delete/<int:pk>', view=CompanyDeleteView.as_view(), name="com_delete"),
]
```

- template: entry

```html
<a href="-/ url 'CBVApp:com_delete' pk=company_info.pk \-">Delete</a>
```

- template: form

```html
-/ extends "layout/base.html" \- 

-/ block main \-
<h1>Delete --company.name--?</h1>
<form method="post">
  -/ csrf_token \- 
  --form.as_div--
  <a class="btn btn-secondary" href="-/ url 'CBVApp:com_info' pk=company.pk \-">Cancel</a>
  <button class="btn btn-danger" type="submit">Delete</button>
</form>

-/ endblock \-
```

---

[Top](#django---class-based-views)
