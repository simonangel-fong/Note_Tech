# jQuery - Ajax

[Back](./index.md)

- [jQuery - Ajax](#jquery---ajax)
  - [Ajax](#ajax)
    - [HTTP Request: GET vs. POST](#http-request-get-vs-post)
  - [Ajax Method](#ajax-method)
  - [Helping Method](#helping-method)

---

## Ajax

- `AJAX` = Asynchronous JavaScript and XML.

  - loading data in the background and display it on the webpage, without reloading the whole page.

---

### HTTP Request: GET vs. POST

- Two commonly used methods for a request-response between a client and server are: `GET` and `POST`.

  - `GET`: Requests data from a specified resource
  - `POST`: Submits data to be processed to a specified resource

---

## Ajax Method

| Ajax             | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `$.ajax(url)`    | Perform an asynchronous HTTP (Ajax) request                      |
| `$.get(url)`     | Load data from the server using a HTTP GET request.              |
| `$.getJSON(url)` | Load JSON-encoded data from the server using a GET HTTP request. |
| `$.post(url)`    | Send data to the server using a HTTP POST request.               |
| `.load(url)`     | Load data into element                                           |

---

## Helping Method

| Method              | Description                                            |
| ------------------- | ------------------------------------------------------ |
| `.serialize()`      | Creates a text string in standard URL-encoded notation |
| `.serializeArray()` | Creates a JavaScript array of objects                  |

---

[TOP](#jquery---ajax)
