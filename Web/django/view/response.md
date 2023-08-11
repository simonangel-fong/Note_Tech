# Django - Response objects

[Back](../index.md)

- [Django - Response objects](#django---response-objects)
  - [`HttpResponse` Objects](#httpresponse-objects)
    - [`HttpResponse` Class](#httpresponse-class)
    - [`HttpResponse` subclasses](#httpresponse-subclasses)
  - [`JsonResponse` Objects](#jsonresponse-objects)
  - [`StreamingHttpResponse` Objects](#streaminghttpresponse-objects)
  - [`FileResponse` objects](#fileresponse-objects)
  - [`django.shortcuts` Module](#djangoshortcuts-module)
    - [`render()`](#render)
    - [`redirect()`](#redirect)
    - [`get_object_or_404()`](#get_object_or_404)
    - [`get_list_or_404()`](#get_list_or_404)

---

## `HttpResponse` Objects

- `HttpResponse` objects are applications' responsibility.
- Each view you write is responsible for instantiating, populating, and returning an `HttpResponse`.

---

### `HttpResponse` Class

- Instantiates an `HttpResponse` object with the given page content, content type, and headers.

- Syntax:

```py
HttpResponse(content=b'', content_type=None, status=200, reason=None, charset=None, headers=None)
```

- Parameter:
  - `content`:
    - the content of the response
    - string iterator, bytestring, memoryview, or string.
  - `content_type`:
    - the `MIME` type to fill the `HTTP Content-Type` header.
    - Default: `'text/html; charset=utf-8'`
  - `status`:
    - the HTTP status code for the response.
  - `reason`:
    - the HTTP response phrase.
  - `charset`:
    - the charset in which the response will be encoded.
  - `headers`:
    - a dict of HTTP headers for the response.

---

### `HttpResponse` subclasses

- Django includes a number of `HttpResponse` subclasses that handle different types of `HTTP` responses.
- Subclasses are in `django.http`.

| Subclass                          | Description                                    | Status code |
| --------------------------------- | ---------------------------------------------- | ----------- |
| `HttpResponseRedirect()`          | redirect to a target url                       | `302`       |
| `HttpResponsePermanentRedirect()` | returns a permanent redirect                   | `301`       |
| `HttpResponseNotModified()`       | a page hasn’t been modified since last request | `304`       |
| `HttpResponseBadRequest()`        | 400 status code.                               | `400`       |
| `HttpResponseNotFound()`          | 404 status code.                               | `404`       |
| `HttpResponseForbidden()`         | 403 status code.                               | `403`       |
| `HttpResponseNotAllowed()`        | 405 status code.                               | `405`       |
| `HttpResponseGone()`              | 410 status code.                               | `410`       |
| `HttpResponseServerError()`       | 500 status code.                               | `500 `      |

---

## `JsonResponse` Objects

- An `HttpResponse` subclass that helps to create a **JSON-encoded** response.
- Its default `Content-Type` header is set to `application/json`.

- Syntax:

```py
JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs)
```

- Parameter:

  - `data`:
    - json data
    - a dict instance
  - `encoder`:
    - the serializer to serialize the data
    - defaults: `django.core.serializers.json.DjangoJSONEncoder`
  - `safe`
    - boolean
    - defaults: `True`
    - If safe is `True` and a non-dict object is passed as the first argument, a `TypeError` will be raised.
    - If it’s set to `False`, any object can be passed for serialization (otherwise only dict instances are allowed).
  - `json_dumps_params`
    - a dictionary of keyword arguments to pass to the json.dumps() call used to generate the response.

- Example:

```py
from django.http import JsonResponse
response = JsonResponse({"foo": "bar"})   # a dict object
response = JsonResponse([1, 2, 3], safe=False)    #  a non-dict object
```

---

## `StreamingHttpResponse` Objects

- used to stream a response from Django to the browser.

- An example usage of `StreamingHttpResponse` under `WSGI` is streaming content when generating the response would **take too long or uses too much memory**.

---

## `FileResponse` objects

- `FileResponse` is a subclass of `StreamingHttpResponse` optimized for **binary files**.
- It uses `wsgi.file_wrapper` if provided by the `wsgi` server, otherwise it streams the file out in small chunks.

- Syntax:

```py
FileResponse(open_file, as_attachment=False, filename='', **kwargs)
```

- `open_file`:
  - the file-like content of response
  - accepts any file-like object with binary content in binary moded
- `as_attachment`: boolean

  - whether content as attechment.
  - If `as_attachment=True`, the `Content-Disposition` header is set to attachment, which asks the browser to offer the file to the user as a download. Otherwise, a `Content-Disposition` header with a value of inline (the browser default) will be set only if a filename is available.

- Example:

```py
from django.http import FileResponse
response = FileResponse(open("myfile.png", "rb"))
```

---


## `django.shortcuts` Module

- `django.shortcuts` Module
  - collects helper functions and classes that “span” multiple levels of MVC.
  - In other words, these functions/classes introduce controlled coupling for convenience’s sake.

---

### `render()`

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

### `redirect()`

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

### `get_object_or_404()`

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

### `get_list_or_404()`

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

[TOP](#django---request-and-response-objects)
