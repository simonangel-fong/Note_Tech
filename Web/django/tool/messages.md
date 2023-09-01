# Django - Messages

[Back](../index.md)

- [Django - Messages](#django---messages)
  - [Enabling messages](#enabling-messages)
  - [Message](#message)
    - [Message levels](#message-levels)
    - [Message tags](#message-tags)
    - [Message class](#message-class)
  - [Usage](#usage)
    - [Template](#template)
    - [Views](#views)
    - [Class-based views: `SuccessMessageMixin`](#class-based-views-successmessagemixin)

---

## Enabling messages

- To enable message functionality, by default, the following should be contained in `settings.py`:
  - `INSTALLED_APPS`: 
    - `'django.contrib.messages'`
  - `MIDDLEWARE`: 
    - `'django.contrib.sessions.middleware.SessionMiddleware'` 
    - `'django.contrib.messages.middleware.MessageMiddleware'`. Should be after SessionMiddleware.
  - `TEMPLATES`'s `'context_processors'` option:
    - `'django.contrib.messages.context_processors.messages'`

---

## Message

### Message levels

- `django.contrib.messages` module

| Constant  | Purpose                                                                               | Value |
| --------- | ------------------------------------------------------------------------------------- | ----- |
| `DEBUG`   | Development-related messages, will be ignored (or removed) in a production deployment | 10    |
| `INFO`    | Informational messages for the user                                                   | 20    |
| `SUCCESS` | An action was successful                                                              | 25    |
| `WARNING` | A failure did not occur but may be imminent                                           | 30    |
| `ERROR`   | An action was not successful or some other failure occurred                           | 40    |

---

### Message tags

- `Message tags`:
  - a string representation of the message level plus any extra tags that were added directly in the view.
- Tags are stored in a string and are separated by spaces.

| Level Constant | Tag     |
| -------------- | ------- |
| `DEBUG`        | debug   |
| `INFO`         | info    |
| `SUCCESS`      | success |
| `WARNING`      | warning |
| `ERROR`        | error   |

- To change the default tags for a message level (either built-in or custom), set the `MESSAGE_TAGS` setting to a dictionary containing the levels you wish to change.

```py
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.INFO: "",
    50: "critical",
}
```

---

### Message class

- Attributes

| Attributes   | Description                                                            |
| ------------ | ---------------------------------------------------------------------- |
| `message`    | The actual text of the message                                         |
| `level`      | An integer describing the type of the message.                         |
| `level_tag`  | The string representation of the level.                                |
| `extra_tags` | A string containing custom tags for this message, separated by spaces. |
| `tags`       | A string combining all the message’s tags separated by spaces.         |

---

## Usage

### Template

- Even if there is only one message, should still iterate over the messages sequence, because otherwise the message storage will not be cleared for the next request.

```html
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li {% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```

- `DEFAULT_MESSAGE_LEVELS` variable: a mapping of the message level names to their numeric value

```html
{% if message.level == DEFAULT_MESSAGE_LEVELS.ERROR %}Important: {% endif %}
```

---

### Views

- **Adding a message**

```py
from django.contrib import messages

# using add_message
messages.add_message(request, messages.INFO, "Hello world.")    

# shortcut
messages.debug(request, "%s SQL statements were executed." % count)
messages.info(request, "Three credits remain in your account.")
messages.success(request, "Profile details updated.")
messages.warning(request, "Your account expires in three days.")
messages.error(request, "Document deleted.")
```

- Getting a message from request

```py
from django.contrib.messages import get_messages

storage = get_messages(request)
for message in storage:
    do_something_with_the_message(message)
```

- Adding extra message tags

```py
messages.add_message(request, messages.INFO, "Over 9000!", extra_tags="dragonball")
messages.error(request, "Email box full", extra_tags="email")
```

---

### Class-based views: `SuccessMessageMixin`

- `SuccessMessageMixin`:
  - a class adding a success message attribute to FormView based classes

- `SuccessMessageMixin` should be place before `CreateView`.

```py
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreateView(SuccessMessageMixin, CreateView):
    model = Author
    success_url = "/success/"
    success_message = "%(name)s was created successfully"   # %(field_name)s syntax.
```

---


[TOP](#django---messages)
