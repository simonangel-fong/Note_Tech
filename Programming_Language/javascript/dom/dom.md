# Javascript - DOM

[Back](../index.md)

- [Javascript - DOM](#javascript---dom)
  - [HTML DOM (Document Object Model)](#html-dom-document-object-model)
  - [Connect JS file](#connect-js-file)
  - [Document Object](#document-object)
  - [Element](#element)
    - [Find HTML Element](#find-html-element)
    - [DOM Navigation](#dom-navigation)
    - [Create Element](#create-element)
    - [Add Element](#add-element)
    - [Update Element](#update-element)
    - [Delete Elements](#delete-elements)
  - [Text Node](#text-node)
  - [Attribute](#attribute)
    - [Example: Randomly Changing Color](#example-randomly-changing-color)
  - [DOM Events](#dom-events)
    - [Common Events](#common-events)
    - [Event handlers](#event-handlers)
    - [Event Methods](#event-methods)
    - [Example: Prevent Submitting Form](#example-prevent-submitting-form)

---

## HTML DOM (Document Object Model)

- `HTML DOM`

  - a standard **object model and programming interface** for HTML
  - constructed as a tree of Objects.
  - a standard for how to get, change, add, or delete HTML elements.

- When a web page is loaded, the browser creates a `Document Object Model` of the page, storing all HTML tags as JS objects.

![Dom Tree](../pic/dom_tree.gif)

- In the DOM, all `HTML` elements are defined as **objects**.

---

## Connect JS file

- HTML

```html
<head>
  <script src="js_file.js"></script>
</head>
```

---

## Document Object

- `HTML DOM document object`

  - the owner of all other objects in web page.

- When accessing any element in an HTML page, always start with accessing the `document object`.

- important Document Attributes

| Attribute        | Description                        |
| ---------------- | ---------------------------------- |
| `document.URL`   | the actual URL of the website      |
| `document.body`  | everything inside of the body      |
| `document.head`  | everything in the head of the page |
| `documnet.links` | all the links on the page          |

- Ref:
  - https://developer.mozilla.org/en-US/docs/Web/API/Document

---

## Element

### Find HTML Element

| Method                                 | Description                                       |
| -------------------------------------- | ------------------------------------------------- |
| `document.getElementById(id)`          | Find an element by element id                     |
| `element.getElementsByTagName(name)`   | Find all descendant elements by tag name          |
| `element.getElementsByClassName(name)` | Find all descendant elements by class name        |
| `element.querySelector()`              | Find the first descendant element by CSS selector |
| `element.querySelectorAll(selector)`   | Find all descendant elements by CSS selector      |

- If the element is found, the method will return the element as an **object** (in element).
- If the element is not found, element will contain `null`.

---

### DOM Navigation

| Method                    | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| `element.hasChildNodes()` | Returns `true` if an element has any child nodes          |
| `element.contains(node)`  | Returns `true` if a node is a descendant of a node        |
| `element.parentNode`      | Returns the **parent** node of an element                 |
| `element.childNodes`      | Returns a **NodeList** of an element's child nodes        |
| `element.firstChild`      | Returns the **first** child node of an element            |
| `element.lastChild`       | Returns the **last** child node of an element             |
| `element.previousSibling` | Returns the **previous** node at the same node tree level |
| `element.nextSibling`     | Returns the **next** node at the same node tree level     |

---

### Create Element

| Method                         | Description             |
| ------------------------------ | ----------------------- |
| `document.createElement(type)` | creates an element node |

### Add Element

| Method                      | Description                                   |
| --------------------------- | --------------------------------------------- |
| `element.appendChild(node)` | Adds (appends) a new child node to an element |

---

### Update Element

| Method                                | Description                                       |
| ------------------------------------- | ------------------------------------------------- |
| `document.write()`                    | writes directly to an open (HTML) document stream |
| `element.innerHTML`                   | Sets or returns the content of an element         |
| `node.replaceChild(newnode, oldnode)` | Replaces a child node in an element               |

### Delete Elements

| Method                      | Description                          |
| --------------------------- | ------------------------------------ |
| `element.remove()`          | Removes an element from the DOM      |
| `element.removeChild(node)` | Removes a child node from an element |

---

## Text Node

| Method                          | Description                                                       |
| ------------------------------- | ----------------------------------------------------------------- |
| `document.createTextNode(text)` | Creates a Text node                                               |
| `element.innerText`             | Sets or returns the text content of a node and its descendants    |
| `element.textContent`           | Sets or returns the textual content of a node and its descendants |

## Attribute

| Property                            | Description                                                    |
| ----------------------------------- | -------------------------------------------------------------- |
| `element.style`                     | Sets or returns the value of the style attribute of an element |
| `element.hasAttribute(name)`        | Returns `true` if an element has a given attribute             |
| `element.getAttribute(name)`        | Returns the value of an element's attribute                    |
| `element.setAttribute(name, value)` | Sets or changes an attribute's value                           |
| `element.removeAttribute(name)`     | Removes an attribute from an element                           |

---

### Example: Randomly Changing Color

- **HTML Code**

```html
<body>
  <h1>Changing Color</h1>
  <script src="demo.js"></script>
  <script>
    console.log("url", document.URL);
    console.log("body", document.body);
    console.log("head", document.head);
    console.log("links", document.links);
  </script>
</body>
```

- **JS code**:

```js
const header = document.querySelector("h1"); //get the first h1 element

// generate a random color code
const randomColorCode = () => {
  let hexaChar = "0123456789ABCDEF";
  let colorCode = "#";
  for (let i = 0; i < 6; i++) {
    colorCode += hexaChar[Math.floor(Math.random() * 16)];
  }
  return colorCode;
};

// set an time interval to change color
setInterval(() => {
  header.style.color = randomColorCode();
}, 500);
```

---

## DOM Events

- `DOM Events` allow JavaScript to add `event listener` or `event handlers` to HTML elements.

### Common Events

- **Event Object Events**

| Event    | Occurs When                                |
| -------- | ------------------------------------------ |
| `change` | The content of a form element have changed |
| `input`  | An element gets user input                 |
| `submit` | A form is submitted                        |

- **Focus Events**

| Event   | Occurs When            |
| ------- | ---------------------- |
| `blur`  | An element loses focus |
| `focus` | An element gets focus  |

- **Input Events**

| Event   | Occurs When                                        |
| ------- | -------------------------------------------------- |
| `input` | The content (value) of an input element is changed |

- **Mouse Event**

| Event         | Occurs When                                |
| ------------- | ------------------------------------------ |
| `click`       | A user clicks on an element                |
| `contextmenu` | A user right-clicks on an element          |
| `dblclick`    | A user double-clicks on an element         |
| `mousedown`   | A mouse button is pressed over an element  |
| `mouseenter`  | The mouse pointer moves into an element    |
| `mouseleave`  | The mouse pointer moves out of an element  |
| `mousemove`   | The mouse pointer moves over an element    |
| `mouseout`    | The mouse pointer moves out of an element  |
| `mouseover`   | The mouse pointer moves onto an element    |
| `mouseup`     | A mouse button is released over an element |

- **Keyboard Events**

| Event      | Occurs When           |
| ---------- | --------------------- |
| `keydown`  | A user presses a key  |
| `keypress` | A user presses a key  |
| `keyup`    | A user releases a key |

---

### Event handlers

| Method                                                   | Description                                   |
| -------------------------------------------------------- | --------------------------------------------- |
| `document.getElementById(id).onclick = function(){code}` | Adding event handler code to an onclick event |
| `element.addEventListener(event, function, useCapture)`  | Attaches an event handler to an element       |
| `element.removeEventListener(event, function, capture)`  | Removes an event handler from an element.     |

- Example

```html
<div id="demo">mouse</div>

<script>
  const demo = document.querySelector("#demo");

  // mouse over
  demo.addEventListener("mouseover", function () {
    this.style.color = "red";
  });

  // mouse out
  demo.addEventListener("mouseout", function () {
    this.style.color = "black";
  });
  // click
  demo.addEventListener("click", function () {
    this.innerText = "Click";
  });

  // double click
  demo.addEventListener("dblclick", function () {
    this.innerText = "Double Click";
  });
</script>
```

---

### Event Methods

- Common Method

| Method                   | Description                                                 |
| ------------------------ | ----------------------------------------------------------- |
| `event.preventDefault()` | the default action that belongs to the event will not occur |

---

### Example: Prevent Submitting Form

```html
<form id="form" action="www.google.com" method="get">
  <p id="demo">Submit</p>
  <input type="text" name="search" id="search" />
  <input type="submit" value="Submit" />
</form>

<script>
  const form = document.querySelector("#form");
  const demo = document.querySelector("#demo");

  // mouse over
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    demo.innerText = "Submit prevented";
  });
</script>
```

---

[TOP](#javascript---dom)
