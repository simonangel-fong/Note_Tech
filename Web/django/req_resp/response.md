# Django - Response objects

[Back](../index.md)

- [Django - Response objects](#django---response-objects)
  - [`HttpResponse` Objects](#httpresponse-objects)
    - [`HttpResponse` Class](#httpresponse-class)
    - [`HttpResponse` subclasses](#httpresponse-subclasses)
  - [`JsonResponse` Objects](#jsonresponse-objects)
  - [`StreamingHttpResponse` Objects](#streaminghttpresponse-objects)
  - [`FileResponse` objects](#fileresponse-objects)

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

[TOP](#django---request-and-response-objects)
