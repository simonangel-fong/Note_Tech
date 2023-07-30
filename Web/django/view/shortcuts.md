# Django - `shortcuts` package

[Back](../index.md)

- [Django - `shortcuts` package](#django---shortcuts-package)
  - [`django.shortcuts` package](#djangoshortcuts-package)
  - [`render()`](#render)
  - [`redirect()`](#redirect)
  - [`get_object_or_404()`](#get_object_or_404)
  - [`get_list_or_404()`](#get_list_or_404)

---

## `django.shortcuts` package

- `django.shortcuts` package
  - collects helper functions and classes that “span” multiple levels of MVC.
  - In other words, these functions/classes introduce controlled coupling for convenience’s sake.

---

## `render()`

- Combines a given **template** with a given **context dictionary** and **returns an HttpResponse object** with that rendered text.

- Syntax:

```py
render(request, template_name, context=None, content_type=None, status=None, using=None)¶
```

- Parameter:

  - `request`: Required.
    - The request object used to generate this response.
  - `template_name`: Required.
    - The full name of a template to use or sequence of template names.
  - `context`: Optional.
    - A dictionary of values to add to the template context.
    - By default, this is an empty dictionary.
    - If a value in the dictionary is callable, the view will call it just before rendering the template.
  - `content_type`: Optional.
    - The MIME type to use for the resulting document.
    - Defaults to `'text/html'`.
  - `status`: Optional.
    - The status code for the response.
    - Defaults to 200.
  - `using`: Optional
    - The `NAME` of a template engine to use for loading the template.

- Example:

  ```py
  from django.shortcuts import render

  def my_view(request):
    # View code here...
    return render(
        request,
        "myapp/index.html",
        {
            "foo": "bar",
        },
        content_type="application/xhtml+xml",
    )
  ```

---

## `redirect()`

- Returns an `HttpResponseRedirect` to the appropriate URL for the arguments passed.

- Syntax:

  ```py
  redirect(to, *args, permanent=False, **kwargs)
  ```

- Parameter can be:

  - A model:
    - the model’s `get_absolute_url()` function will be called.
  - A view name, possibly with arguments:
    - `reverse()` will be used to reverse-resolve the name.
  - An absolute or relative URL
    - will be used as-is for the redirect location.

- By default issues a **temporary redirect**; pass `permanent=True` to issue a **permanent redirect**.

- Examples:

```py
from django.shortcuts import redirect

# By passing some object; that object’s get_absolute_url() method will be called to figure out the redirect URL
def my_view(request):
    obj = MyModel.objects.get(...)
    return redirect(obj)


# By passing the name of a view and optionally some positional or keyword arguments; the URL will be reverse resolved using the reverse() method:
def my_view(request):
    return redirect("some-view-name", foo="bar")

# By passing a hardcoded URL to redirect to
def my_view(request):
    return redirect("/some/url/")
```

---

## `get_object_or_404()`

- Calls `get()` on a given model manager, but it raises `Http404` instead of the model’s `DoesNotExist` exception.

- Syntax:

```py
get_object_or_404(klass, *args, **kwargs)
```

- Parameter:

  - `klass`:
    - A Model class, a Manager, or a QuerySet instance from which to get the object.
  - `*args`:
    - `Q objects.`
  - `**kwargs`
    - Lookup parameters, which should be in the format accepted by `get()` and `filter()`.

- Exmaple:

```py
from django.shortcuts import get_object_or_404


def my_view(request):
    obj = get_object_or_404(MyModel, pk=1)

# equivalent to
def my_view(request):
    try:
        obj = MyModel.objects.get(pk=1)
    except MyModel.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
```

---

## `get_list_or_404()`

- Returns the result of `filter()` on a given model manager cast to a list, raising `Http404` if the resulting list is empty.

- Syntax:

```py
get_list_or_404(klass, *args, **kwargs)
```

- Parameter:

  - `klass`:
    - A Model class, a Manager, or a QuerySet instance from which to get the object.
  - `*args`:
    - `Q objects.`
  - `**kwargs`
    - Lookup parameters, which should be in the format accepted by `get()` and `filter()`.

- Example:

```py
from django.shortcuts import get_list_or_404


def my_view(request):
    my_objects = get_list_or_404(MyModel, published=True)

# equivalent to
def my_view(request):
    my_objects = list(MyModel.objects.filter(published=True))
    if not my_objects:
        raise Http404("No MyModel matches the given query.")
```

---

[TOP](#django---shortcuts-package)
