# jQuery - DOM Method

[Back](./index.md)

- [jQuery - DOM Method](#jquery---dom-method)
  - [Content Method](#content-method)
  - [Attribute Method](#attribute-method)
  - [DOM Manipulation](#dom-manipulation)
  - [DOM Filter](#dom-filter)
  - [Tree Traversal](#tree-traversal)
  - [Data Storage](#data-storage)
  - [Collection Manipulation](#collection-manipulation)

---

## Content Method

| Method              | Description                    |
| ------------------- | ------------------------------ |
| `.text()`           | Get the combined text contents |
| `.text(text)`       | Set text content               |
| `.html()`           | Get the HTML contents          |
| `.html(htmlString)` | Set HTML content               |
| `.val()`            | Get the value                  |
| `.val(value)`       | Set the value                  |

---

## Attribute Method

- **General Attribute**

| Method                    | Description                         |
| ------------------------- | ----------------------------------- |
| `.attr(attribute)`        | Get attribute for the first element |
| `.attr(attribute, value)` | Set attribute                       |
| `.removeAttr(attribute)`  | Remove an attribute from element    |

- **Class Attribute**

| Method                | Description                                |
| --------------------- | ------------------------------------------ |
| `.hasClass(class)`    | `true` if the class is assigned to element |
| `.toggleClass(class)` | Add or remove class from mateched elements |
| `.addClass(class)`    | Adds class(es) to mateched elements        |
| `.removeClass(class)` | Remove class from mateched elements        |
| `.removeClass()`      | Remove all classes from mateched elements  |

- **Style Properties**

| Method                  | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| `.css(property)`        | Get the computed style properties for the first element |
| `.css(property, value)` | Set one CSS properties                                  |
| `.css({properties})`    | Set more CSS properties                                 |

---

## DOM Manipulation

| Method                      | Description                                        |
| --------------------------- | -------------------------------------------------- |
| `.clone()`                  | Create a deep copy                                 |
| `.prepend(html/selector)`   | Insert content to the beginning of current element |
| `.prependTo(target)`        | Insert current element to the beginning of target  |
| `.append(html/selector)`    | Insert content to the end of current element       |
| `.appendTo(target)`         | Insert current element to the end of target        |
| `.after(html/selector)`     | Insert content after current element               |
| `.before(html/selector)`    | Insert content before current element              |
| `.insertAfter(target)`      | Insert current element after target                |
| `.insertBefore(target)`     | Insert current element before target               |
| `.wrap(wrappingElement)`    | Wrap an HTML structure in wrappingElement          |
| `.unwrap()`                 | Remove the parents of element                      |
| `.wrapAll(wrappingElement)` | Wrap an HTML structure around all elements         |
| `.remove()`                 | Remove elements                                    |
| `.empty()`                  | Remove all child nodes                             |
| `.replaceWith(newContent)`  | Replace element with new content                   |
| `.replaceAll(target)`       | Replace target with element.                       |
| `.get()`                    | Retrieve all elements                              |
| `.get(index)`               | Retrieve one element by index                      |
| `.index(html/selector)`     | Retrieve index of the first element                |
| `.toArray()`                | Retrieve elements as an array.                     |

---

## DOM Filter

| Method              | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| `.is(selector)`     | return `true` if at least one of elements matches selector  |
| `.has(selector)`    | Selects descendants that has selector                       |
| `.eq(index)`        | Selects the index-th element                                |
| `.even()`           | Selects elements with an even index                         |
| `.odd()`            | Selects elements with an odd index                          |
| `.first()`          | Selects the first element                                   |
| `.last()`           | Selects the last element                                    |
| `.filter(selector)` | Filter element with selector                                |
| `.not()`            | Returns elements that do not match a certain criteria       |
| `.map(callback)`    | Producing a new jQuery object containing the return values. |
| `.slice(start,end)` | Slice elements                                              |

---

## Tree Traversal

| Method               | Description                                     |
| -------------------- | ----------------------------------------------- |
| `.parent()`          | Get the parent                                  |
| `.parents()`         | Get the ancestors                               |
| `.children()`        | Get the children                                |
| `.siblings()`        | Get the siblings                                |
| `.prev()`            | Get the immediately preceding sibling           |
| `.prevAll()`         | Get all preceding siblings                      |
| `.next()`            | Get the immediately following sibling           |
| `.nextAll()`         | Get all following siblings                      |
| `.find(selector)`    | Get the descendants that matches the selector   |
| `.closest(selector)` | Get the first element that matches the selector |

---

## Data Storage

| Method             | Description                       |
| ------------------ | --------------------------------- |
| `.data(key)`       | Return arbitrary data             |
| `.data(key,value)` | Store arbitrary data with element |
| `.removeData(key)` | Remove data                       |
| `.removeData()`    | Removes all values.               |

---

## Collection Manipulation

| Method            | Description                  |
| ----------------- | ---------------------------- |
| `.each(function)` | Iterate over a jQuery object |

---



[TOP](#jquery---method)
