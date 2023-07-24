# jQuery - Event

[Back](./index.md)

- [jQuery - Event](#jquery---event)
  - [Event](#event)
    - [Document Loading](#document-loading)
    - [Event Handler Attachment](#event-handler-attachment)

---

## Event

- `Event`

  - All the different visitors' actions that a web page can respond to

- Syntax:

```js
$(selector).eventName(function () {});
```

---

### Document Loading

| Event Method          | Event Description        |
| --------------------- | ------------------------ |
| `$(document).ready()` | document is fully loaded |

---

### Event Handler Attachment

| Event Method          | Event Description                       |
| --------------------- | --------------------------------------- |
| `.on(event, handler)` | Attach an event handler function        |
| `.on(eventsObject)`   | Attach multiple event handler functions |
| `.off(events)`        | Remove an event handler                 |
| `.trigger(eventType)` | Execute all handlers                    |

```js
// add an event handler
$(selector).on("eventName", function () {
  //   code block
});

// add multiple event handlers, event name without quotation
$(selector).on({
  eventName1: function () {
    //event1 code
  },
  eventName2: function () {
    //event2 code
  },
});
```

---

[TOP](#jquery---event)
