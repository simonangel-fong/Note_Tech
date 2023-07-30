# Django - Request Objects

[Back](../index.md)

- [Django - Request Objects](#django---request-objects)
  - [Overview: Request and response objects](#overview-request-and-response-objects)
  - [`HttpRequest` Objects](#httprequest-objects)
    - [Attributes](#attributes)
    - [Methods](#methods)
  - [`QueryDict` Objects](#querydict-objects)

---

## Overview: Request and response objects

- Django uses `request` and `response` objects to pass state through the system.

- When a page is requested, Django creates an `HttpRequest` object that contains metadata about the request.
- Django maps the requested url to specific view.
- Then Django loads the appropriate view, passing the `HttpRequest` as the **first argument** to the view function.
- Each view is responsible for returning an `HttpResponse` object.

- request >> url >> view >> Response

- `HttpRequest` and `HttpResponse` objects are defined in the `django.http` module.

---

## `HttpRequest` Objects

- `HttpRequest` objects are created automatically by Django.

### Attributes

- All attributes should be considered **read-only**, unless stated otherwise.

| Attributes       | Description                                                                            |
| ---------------- | -------------------------------------------------------------------------------------- |
| `scheme`         | the scheme of the request (http or https usually)                                      |
| `body`           | The raw HTTP request body as a bytestring (data like binary images, XML)               |
| `path`           | the full path to the requested page, except the scheme, domain, or query string.       |
| `method`         | the HTTP method used in the request. `"GET"`, `"POST"`                                 |
| `encoding`       | the current encoding used to decode form submission data                               |
| `content_type`   | the MIME type of the request                                                           |
| `content_params` | key/value parameters included in the `CONTENT_TYPE` header                             |
| `GET`            | A `QueryDict` object containing all given `HTTP GET` parameters.                       |
| `POST`           | A `QueryDict` object containing all given `HTTP POST` parameters                       |
| `COOKIES`        | A dictionary containing all cookies                                                    |
| `FILES`          | A dictionary-like object containing all uploaded files.                                |
| `META`           | A dictionary containing all available `HTTP` **headers**.                              |
| `headers`        | A case insensitive, dict-like object that provides access to all HTTP-prefixed headers |

- Available headers depend on the client and server. Here are some examples:

  - `CONTENT_LENGTH`: The length of the request body (as a string).
  - `CONTENT_TYPE`: The MIME type of the request body.
  - `HTTP_ACCEPT`: Acceptable content types for the response.
  - `HTTP_ACCEPT_ENCODING`: Acceptable encodings for the response.
  - `HTTP_ACCEPT_LANGUAGE`: Acceptable languages for the response.
  - `HTTP_HOST`: The HTTP Host header sent by the client.
  - `HTTP_REFERER`: The referring page, if any.
  - `HTTP_USER_AGENT`: The client’s user-agent string.
  - `QUERY_STRING`: The query string, as a single (unparsed) string.
  - `REMOTE_ADDR`: The IP address of the client.
  - `REMOTE_HOST`: The hostname of the client.
  - `REMOTE_USER`: The user authenticated by the web server, if any.
  - `REQUEST_METHOD`: A string such as "GET" or "POST".
  - `SERVER_NAME`: The hostname of the server.
  - `SERVER_PORT`: The port of the server (as a string).

---

### Methods

| Method                   | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| `get_host()`             | Returns the host of the request                                          |
| `get_port()`             | Returns the port of the request                                          |
| `get_full_path()`        | Returns the path, plus an appended query string                          |
| `build_absolute_uri()`   | Returns the absolute URI form of location.                               |
| `get_signed_cookie(key)` | Returns a cookie value for a signed cookie                               |
| `is_secure()`            | Returns True if the request is secure(made with `HTTPS`)                 |
| `accepts(mime_type)`     | Returns True if the request Accept header matches the mime_type argument |
| `read(size=None)`        | read an HttpRequest instance                                             |
| `readline()`             | read an HttpRequest instance                                             |
| `readlines()`            | read an HttpRequest instance                                             |
| `__iter__()`             | read an HttpRequest instance                                             |

---

## `QueryDict` Objects

- In an `HttpRequest` object, the `GET` and `POST` attributes are **instances** of `django.http.QueryDict`, a dictionary-like class customized to deal with multiple values for the same key.
- The `QueryDicts` at `request.POST` and `request.GET` will be **immutable** when accessed in a normal request/response cycle.
- To get a **mutable** version you need to use `QueryDict.copy()`.

| Method          | Description                                            |
| --------------- | ------------------------------------------------------ |
| `.get(key)`     | Returns a list of the data with the requested key.     |
| `.getlist(key)` | Returns a mutable copy of the object.                  |
| `.items()`      | Return an iterable object with all key-value pairs     |
| `.lists()`      | Like items, except it includes all values for each key |
| `.values()`     | Return an iterable object with all values              |
| `.copy()`       | Returns a mutable copy of the object.                  |
| `.dict()`       | Returns a `dict` representation of `QueryDict`         |
| `.urlencode()`  | Returns a string of the data in query string format.   |

---

[TOP](#django---request-and-response-objects)
