# HTML - Form

[Back](./index.md)

- [HTML - Form](#html---form)
  - [`<form>` Element](#form-element)

---

## `<form>` Element

- An HTML `<form>s` is used to collect user input. The user input is most often sent to a server for processing.

- Syntax

```html
<form></form>
```

- Attribute

| Attribute | Description                                              |
| --------- | -------------------------------------------------------- |
| `name`    | the name of the form                                     |
| `action`  | the action to be performed when the form is submitted    |
| `method`  | the HTTP method to be used when submitting the form data |
| `target`  | ndicates where to display the response                   |

- `Method` Attribute

  - `GET`:

    - Appends the form data to the **URL**, in **name/value pairs**
    - **NEVER use GET to send sensitive data**! (the submitted form data is visible in the URL!)
    - The length of a URL is **limited** (2048 characters)
    - Useful for form submissions where a user wants to bookmark the result
    - GET is good for **non-secure data**, like query strings in Google

  - `POST`:
    - Appends the form data **inside the body of the HTTP request** (the submitted form data is not shown in the URL)
    - POST has **no size limitations**, and can be used to send large amounts of data.
    - Form submissions with POST **cannot be bookmarked**

- `Target` Attribute

| Value       | Description                                                   |
| ----------- | ------------------------------------------------------------- |
| `_self`     | The response is displayed in the same frame (this is default) |
| `_blank`    | The response is displayed in a new window or tab              |
| `_parent`   | The response is displayed in the parent frame                 |
| `_top`      | The response is displayed in the full body of the window      |
| `framename` | The response is displayed in a named iframe                   |

---

[TOP](#html---form)
