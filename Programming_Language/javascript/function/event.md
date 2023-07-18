# JavaScript - Event

[Back](../index.md)

- [JavaScript - Event](#javascript---event)
  - [HTML Event](#html-event)
    - [Common HTML Events](#common-html-events)

---

## HTML Event

- `Event`:

  - an event which takes place in the DOM.
  - can be triggered by the user action.
  - can also be triggered programmatically.

- `Event Handler`

  - used to handle and verify user input, user actions, and browser actions

- Syntax

```html
<element event="some JavaScript" />

<!-- It is more common to see event attributes calling functions -->
<element event="function_name()" />
```

- Example:

```html
<!-- exmaple 1: inline script  -->
<p id="demo"></p>

<button onclick="document.getElementById('demo').innerHTML=Date()">
  The time is?
</button>

<!-- example 2: using function -->
<p id="demo"></p>
<button onclick="displayDate()">The time is?</button>

<script>
  function displayDate() {
    document.getElementById("demo").innerHTML = Date();
  }
</script>

<!-- example 2: using this. -->
<!-- Here this reference the element called by event, that is button. -->
<button onclick="this.innerHTML=Date()">The time is?</button>
```

---

### Common HTML Events

| Event         | Description                                        |
| ------------- | -------------------------------------------------- |
| `onchange`    | An HTML element has been changed                   |
| `onclick`     | The user clicks an HTML element                    |
| `onmouseover` | The user moves the mouse over an HTML element      |
| `onmouseout`  | The user moves the mouse away from an HTML element |
| `onkeydown`   | The user pushes a keyboard key                     |
| `onload`      | The browser has finished loading the page          |

---

[TOP](#javascript---event)
