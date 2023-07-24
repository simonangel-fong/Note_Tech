# jQuery - Fundamental

[Back](./index.md)

- [jQuery - Fundamental](#jquery---fundamental)
  - [Syntax](#syntax)
  - [`$(document).ready()` / `$(function(){}`](#documentready--function)
  - [Selector](#selector)

---

## Syntax

- Basic syntax:

```js
$(selector).action();
```

- A `$` sign to define/access jQuery
- A `(selector)`` to "query (or find)" HTML elements
- A jQuery `action()` to be performed on the element(s)

---

## `$(document).ready()` / `$(function(){}`

- `$(document).ready()` / `$(function(){}`:
  - The **Document Ready Event**
  - prevent any jQuery code from running before the document is finished loading (is ready).
  - It is good practice to wait for the document to be fully loaded and ready before working with it.

---

## Selector

- Basic Selector

| Basic Selector                         | Description       |
| -------------------------------------- | ----------------- |
| `$("*")`                               | All Selector      |
| `$("#id")`                             | ID Selector       |
| `$("elementName")`                     | Element Selector  |
| `$(".className")`                      | Class Selector    |
| `$("selector1, selector2, selectorN")` | Multiple Selector |

- Attribute selector

| Selector                                                      | Description                                                                    |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `$("[attribute]")`                                            | Elements with attribute                                                        |
| `$("[attribute='value']")`                                    | Elements with attribute value **equal to** "value"                             |
| `$("[attribute!='value']")`                                   | Elements with attribute value **not equal to** "value"                         |
| `$("[attribute^='value']")`                                   | Elements with attribute value **starting with** "value"                        |
| `$("[attribute$='value']")`                                   | Elements with attribute value **ending with** "value"                          |
| `$("[attribute                                                | =value]")`                                                                     | Elements with attribute value **equal to** "value" or **starting with** "value" **followed by a hyphen** |
| `$("[attribute*='value']")`                                   | Elements with attribute value **containing** the word "value"                  |
| `$("[attribute~='value']")`                                   | Elements with attribute value **containing** a given word, delimited by spaces |
| `$("[attributeFilter1][attributeFilter2][attributeFilterN])"` | Multiple Attribute Selector                                                    |

- Child Filter

| Selector                                        | Description                                  |
| ----------------------------------------------- | -------------------------------------------- |
| `$(":only-child")`                              | elements that are the only child             |
| `$(":first-child")`                             | the first child                              |
| `$(":last-child")`                              | the last child                               |
| `$(":nth-child(index/even/odd/equation)")`      | the nth-child                                |
| `$(":nth-last-child(index/even/odd/equation)")` | the nth-child from the last element          |
| `$(":only-of-type")`                            | no siblings with the same element            |
| `$(":first-of-type")`                           | the first among siblings of the same element |
| `$(":last-of-type")`                            | the last among siblings of the same element  |
| `$(":nth-last-of-type(index/even/odd)")`        | the nth-child among siblings from the last   |
| `$(":nth-of-type(index/even/odd)")`             | the nth child among siblings                 |

- Hierarchy

| Filter                     | Description                                  |
| -------------------------- | -------------------------------------------- |
| `$("ancestor descendant")` | Selects all descendants of a given ancestor. |
| `$("parent > child")`      | Selects all direct child elements            |
| `$("prev + next")`         | Selects all next sibling elements            |
| `$("prev ~ siblings")`     | Selects all following sibling elements       |

- Content Filter

| Filter                 | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| `$(":not(selector)")`  | Selects elements that do not match                             |
| `$(":has(selector)")`  | Selects elements which contain at least one matched element.   |
| `$(":contains(text)")` | Selects elements that contain the specified text.              |
| `$(":empty")`          | Selects elements that have no children (including text nodes). |
| `$(":parent")`         | Selects elements that have at least one child node or text.    |

---

[TOP](#jquery---fundamental)
