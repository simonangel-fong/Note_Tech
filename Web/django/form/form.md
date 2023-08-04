# Django - Form

[Back](../index.md)

- [Django - Form](#django---form)
  - [HTTP methods: `GET` and `POST`](#http-methods-get-and-post)
  - [Django Form class](#django-form-class)
    - [Bound and unbound form instances](#bound-and-unbound-form-instances)
    - [Looping over the form’s fields](#looping-over-the-forms-fields)
    - [Rendering fields manually](#rendering-fields-manually)
  - [Example: Building a form in Django](#example-building-a-form-in-django)
  - [`Form` Class](#form-class)

---

## HTTP methods: `GET` and `POST`

- **`GET` Method**

  - the method used to request data from a specified resource.
  - the query string (name/value pairs) is sent in the URL of a `GET` request

- `GET requests`

  - can be cached
  - are only used to request data (not modify)
  - remain in the browser history
  - can be bookmarked
  - **should never** be used when dealing with **sensitive data**
  - have length restrictions
  - Data is visible to everyone in the URL

- **`POST` Method**

  - the method used to send data to a server to create/update a resource.
  - The data sent to the server with `POST` is stored in the request **body** of the `HTTP` request

- `POST requests`:

  - are never cached
  - do not remain in the browser history
  - cannot be bookmarked
  - have no restrictions on data length
  - Data is not displayed in the URL

---

## Django Form class

- Ref:

  - https://docs.djangoproject.com/en/4.2/topics/forms/#building-a-form

- A form class’s fields

  - map to HTML form **`<input>` elements**.
  - manage form **data** and perform **validation** when a form is submitted.
  - is represented to a user in the browser as an **HTML “widget”**

- `Widgets`:

  - the Django’s representation of an HTML input element.
  - handles the rendering of the HTML
  - Each form field has a corresponding Widget class, which in turn corresponds to an HTML form widget

- Field data:
  - Whatever the data submitted with a form, once it has been successfully **validated** by calling `is_valid()`, the **validated form data** will be in the `form.cleaned_data` dictionary.
  - This data will have **been nicely converted into Python types** for you.

---

### Bound and unbound form instances

- `unbound form`:

  - a form that has no data associated with it.
  - When rendered to the user, it will be **empty** or will contain **default values**.
  - it cannot do validation

- `bound form`

  - the form has submitted data, and hence can be used to tell if that data is valid.
  - If an **invalid bound form** is rendered, it can include inline **error messages** telling the user what data to correct.

- The form’s `is_bound` attribute will tell whether a form has data bound to it or not.

---

### Looping over the form’s fields

- When using the same HTML for each of your form fields, duplicate code can be reduced by looping through each field in turn using a ** for ** loop:

```html
__ for field in form __
<div class="fieldWrapper">
  __ field.errors __ __ field.label_tag __ __ field __ __ if field.help_text __
  <p class="help">__ field.help_text|safe __</p>
  __ endif __
</div>
__ endfor __
```

---

### Rendering fields manually

- Form fields can be unpacked manually by using `__ form.field_name __`.
- Error message for each field is available by using `__form.field_name.errors__`

- `forms.py`:

```py
from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
```

```html
__ form.non_field_errors __
<!--  the template lookup for errors on each field. -->
<div class="fieldWrapper">
  __ form.subject.errors __
  <label for="__ form.subject.id_for_label __">Email subject:</label>
  __ form.subject __
</div>
<div class="fieldWrapper">
  __ form.message.errors __
  <label for="__ form.message.id_for_label __">Your message:</label>
  __ form.message __
</div>
<div class="fieldWrapper">
  __ form.sender.errors __
  <label for="__ form.sender.id_for_label __">Your email address:</label>
  __ form.sender __
</div>
<div class="fieldWrapper">
  __ form.cc_myself.errors __
  <label for="__ form.cc_myself.id_for_label __">CC yourself?</label>
  __ form.cc_myself __
</div>
```

## Example: Building a form in Django

- `forms.py`

```py
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
```

- `views.py`

```py
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "name.html", {"form": form})
```

- `name.html`

```html
<form action="/your-name/" method="post">
  __ csrf_token __ __ form __
  <input type="submit" value="Submit" />
</form>
```

---

## `Form` Class

- **Constructor**

| Method/Attribute          | Description                                |
| ------------------------- | ------------------------------------------ |
| `form_name()`             | Constructs an unbound form                 |
| `form_name(data)`         | Constructs an bound form                   |
| `get_initial_for_field()` | Returns the initial data for a form field. |
| `is_bound`                | Whether a form is bounded.                 |
| `initial`                 | Declare the initial value of form fields   |
| `fields`                  | access the fields of Form instance         |

- **Validate Data**

| Method/Attribute         | Description                                                             |
| ------------------------ | ----------------------------------------------------------------------- |
| `clean()`                | Implement custom validation for fields                                  |
| `is_valid()`             | Run validation and return a boolean                                     |
| `errors`                 | Returns errors in a dictionary.                                         |
| `errors.as_data()`       | Returns errors with original `ValidationError` instances.               |
| `errors.as_json()`       | Returns errors serialized as `JSON`.                                    |
| `errors.get_json_data()` | Returns errors as a dictionary suitable for JSON                        |
| `add_error()`            | Ads errors to specific fields                                           |
| `has_error()`            | Whether a field has an error                                            |
| `non_field_errors()`     | the list of errors not associated with any particular field             |
| `cleaned_data`           | Return a dictionary contains only the valid fields defined in the Form, |
| `error_css_class`        | CSS class name for field error                                          |
| `required_css_class`     | CSS class name for required field                                       |

- **Checking which form data has changed**

| Method/Attribute | Description                                                       |
| ---------------- | ----------------------------------------------------------------- |
| `has_changed()`  | check if the form data has been changed from the initial data.    |
| `changed_data`   | Returns a list of the names of the fields that have been changed. |

```py
# exmaple:

f = ContactForm(request.POST, initial=data)
if f.has_changed():
    print("The following fields changed: %s" % ", ".join(f.changed_data))
f.changed_data
```

- **Rending**

| Method/Attribute      | Description                                      |
| --------------------- | ------------------------------------------------ |
| `render()`            | The render method is called                      |
| `get_context()`       | Return the template context                      |
| `template_name`       | The name of the template rendered                |
| `template_name_label` | The template used to render a field’s `<label>`, |
| `auto_id`             | control `<label>` tags nor `id` attributes       |
| `label_suffix`        | append a string after any `<label>` tags name    |

- **Output styles**

| Output options | Description                |
| -------------- | -------------------------- |
| `as_div`       | wrapped in `<div>` tags.   |
| `as_table`     | wrapped in `<table>` tags. |
| `as_p`         | wrapped in `<p>` tags.     |
| `as_ul`        | wrapped in `<ul>` tags.    |

---

[TOP](#django---form)
