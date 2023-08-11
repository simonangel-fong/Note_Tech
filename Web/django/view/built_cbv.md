# Django - Built-in class-based generic views

[Back](../index.md)

- [Django - Built-in class-based generic views](#django---built-in-class-based-generic-views)
  - [Base views](#base-views)
    - [`View` Class](#view-class)
    - [`TemplateView` Class](#templateview-class)
    - [`RedirectView` Class](#redirectview-class)
  - [Generic display views](#generic-display-views)
    - [`DetailView` Class](#detailview-class)
    - [`List Views` Class](#list-views-class)
  - [Editing views](#editing-views)
    - [`FormView` Class](#formview-class)
    - [`CreateView` Class](#createview-class)
    - [`UpdateView` Class](#updateview-class)
    - [`DeleteView` Class](#deleteview-class)

## Base views

- Module: `django.views.generic.base`

### `View` Class

- The base view class. All other class-based views inherit from this base class. 

- can be imported from `django.views`.

- Attributes

| Attributes          | Description                       |
| ------------------- | --------------------------------- |
| `http_method_names` | The list of available HTTP method |

- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `head()`                    |                                                                          |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |

---

### `TemplateView` Class

- Renders a given template

- Attributes

| Attributes                              | Description                                                    |
| --------------------------------------- | -------------------------------------------------------------- |
| `content_type`                          | The content type to use for the response                       |
| `extra_context`                         | A dictionary to include in the context.                        |
| `http_method_names`                     | The list of available HTTP method                              |
| `response_class [render_to_response()]` | The response class to be returned by render_to_response method |
| `template_engine`                       | The NAME of a template engine                                  |
| `template_name [get_template_names()]`  | The full name of a template to us                              |

- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `get_context_data()`        | a dictionary representing the template context                           |
| `get()`                     |                                                                          |
| `head()`                    |                                                                          |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |
| `render_to_response()`      | a self.response_class instance.                                          |

---

### `RedirectView` Class

- Redirects to a given URL.

- Attributes

| Attributes                 | Description                                                     |
| -------------------------- | --------------------------------------------------------------- |
| `http_method_names`        | The list of available HTTP method                               |
| `pattern_name`             | The name of the URL pattern to redirect to.                     |
| `permanent`                | Whether the redirect should be permanent.                       |
| `query_string`             | Whether to pass along the GET query string to the new location. |
| `url [get_redirect_url()]` | The URL to redirect to                                          |

- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `delete()`                  |                                                                          |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `put()`                     |                                                                          |
| `get()`                     |                                                                          |
| `head()`                    |                                                                          |
| `post()`                    |                                                                          |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |
| `options()`                 |                                                                          |

---

## Generic display views

### `DetailView` Class

- Module: `django.views.generic.detail`

- Attributes

| Attributes                                        | Description                                     |
| ------------------------------------------------- | ----------------------------------------------- |
| `content_type`                                    | The content type to use for the response        |
| `context_object_name [get_context_object_name()]` | the name of the variable to use in the context. |
| `extra_context`                                   | A dictionary to include in the context.         |
| `http_method_names`                               | The list of available HTTP method               |
| `model`                                           | The model that this view will display data for. |
| `pk_url_kwarg`                                    | The name of the URLConf keyword argument        |
| `query_pk_and_slug`                               |                                                 |
| `queryset [get_queryset()]`                       | A QuerySet that represents the objects.         |
| `response_class [render_to_response()]`           | The response class to be returned               |
| `slug_field [get_slug_field()]`                   | The name of the slug field                      |
| `slug_url_kwarg`                                  | The name of the URLConf slug keyword argument   |
| `template_engine`                                 | The NAME of a template engine                   |
| `template_name [get_template_names()]`            | The full name of a template to use              |
| `template_name_field`                             | The field on the current object instance        |
| `template_name_suffix`                            | The suffix to append to template name           |


- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `get()`                     |                                                                          |
| `head()`                    |                                                                          |
| `get_context_data()`        | a dictionary representing the template context                           |
| `get_object()`              | Returns the single object that this view will display.                   |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |
| `render_to_response()`      | a self.response_class instance.                                          |

---

### `List Views` Class

- Attributes

| Attributes                                        | Description                                                                      |
| ------------------------------------------------- | -------------------------------------------------------------------------------- |
| `allow_empty [get_allow_empty()]`                 | boolean, specify whether to display the page if no objects are available.        |
| `content_type`                                    | The content type to use for the response                                         |
| `context_object_name [get_context_object_name()]` | the name of the variable to use in the context.                                  |
| `extra_context`                                   | A dictionary to include in the context.                                          |
| `http_method_names`                               | The list of available HTTP method                                                |
| `model`                                           | The model that this view will display data for.                                  |
| `ordering [get_ordering()]`                       | A string or list of strings specifying the ordering                              |
| `paginate_by [get_paginate_by()]`                 | An integer specifying how many objects should be displayed per page              |
| `paginate_orphans [get_paginate_orphans()]`       | An integer specifying the number of “overflow” objects the last page can contain |
| `paginator_class`                                 | The paginator class to be used for pagination                                    |
| `queryset [get_queryset()]`                       | A QuerySet that represents the objects.                                          |
| `response_class [render_to_response()]`           | The response class to be returned                                                |
| `template_engine`                                 | The NAME of a template engine                                                    |
| `template_name [get_template_names()]`            | The full name of a template to use                                               |
| `template_name_suffix`                            | The suffix to append to template name                                            |

- Methods

| Methods                     | Description                                                                |
| --------------------------- | -------------------------------------------------------------------------- |
| `as_view()`                 | Returns a callable view that takes a request and returns a response        |
| `setup()`                   | Performs key view initialization                                           |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response.   |
| `get()`                     |                                                                            |
| `head()`                    |                                                                            |
| `get_context_data()`        | a dictionary representing the template context                             |
| `get_paginator()`           | Returns an instance of the paginator                                       |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported               |
| `paginate_queryset()`       | Returns a 4-tuple containing (paginator, page, object_list, is_paginated). |
| `render_to_response()`      | a self.response_class instance.                                            |

---

## Editing views

### `FormView` Class

- Attributes

| Attributes                              | Description                                                     |
| --------------------------------------- | --------------------------------------------------------------- |
| `content_type`                          | The content type to use for the response                        |
| `extra_context`                         | A dictionary to include in the context.                         |
| `form_class [get_form_class()]`         | The form class to instantiate.                                  |
| `http_method_names`                     | The list of available HTTP method                               |
| `initial [get_initial()]`               | A dictionary containing initial data for the form.              |
| `prefix [get_prefix()]`                 | The prefix for the generated form.                              |
| `response_class [render_to_response()]` | The response class to be returned                               |
| `success_url [get_success_url()]`       | The URL to redirect to when the form is successfully processed. |
| `template_engine`                       | The NAME of a template engine                                   |
| `template_name [get_template_names()]`  | The full name of a template to use                              |

- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `form_invalid()`            | Renders a response, providing the invalid form as context.               |
| `form_valid()`              | Redirects to get_success_url().                                          |
| `put()`                     |                                                                          |
| `get()`                     |                                                                          |
| `post()`                    |                                                                          |
| `get_context_data()`        | a dictionary representing the template context                           |
| `get_form()`                | Instantiate an instance of form_class                                    |
| `get_form_kwargs()`         | Build the keyword arguments required to instantiate the form.            |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |

---

### `CreateView` Class

- Attributes

| Attributes                                        | Description                                                      |
| ------------------------------------------------- | ---------------------------------------------------------------- |
| `content_type`                                    | The content type to use for the response                         |
| `context_object_name [get_context_object_name()]` | the name of the variable to use in the context.                  |
| `extra_context`                                   | A dictionary to include in the context.                          |
| `fields`                                          | A list of names of fields.                                       |
| `form_class [get_form_class()]`                   | The form class to instantiate.                                   |
| `http_method_names`                               | The list of available HTTP method                                |
| `initial [get_initial()]`                         | A dictionary containing initial data for the form.               |
| `model`                                           | The model that this view will display data for.                  |
| `pk_url_kwarg`                                    | The name of the URLConf keyword argument                         |
| `prefix [get_prefix()]`                           | The prefix for the generated form.                               |
| `query_pk_and_slug`                               |                                                                  |
| `queryset [get_queryset()]`                       | A QuerySet that represents the objects.                          |
| `response_class [render_to_response()]`           | The response class to be returned                                |
| `slug_field [get_slug_field()]`                   | The name of the field on the model that contains the slug.       |
| `slug_url_kwarg`                                  | The name of the URLConf keyword argument that contains the slug. |
| `success_url [get_success_url()]`                 | The URL to redirect to when the form is successfully processed.  |
| `template_engine`                                 | The NAME of a template engine                                    |
| `template_name [get_template_names()]`            | The full name of a template to use                               |
| `template_name_field`                             | The field on the current object instance                         |
| `template_name_suffix`                            | The suffix to append to template name                            |

- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `form_invalid()`            | Renders a response, providing the invalid form as context.               |
| `form_valid()`              | Redirects to get_success_url().                                          |
| `head()`                    |                                                                          |
| `put()`                     |                                                                          |
| `get()`                     |                                                                          |
| `post()`                    |                                                                          |
| `get_context_data()`        | a dictionary representing the template context                           |
| `get_form()`                | Instantiate an instance of form_class                                    |
| `get_form_kwargs()`         | Build the keyword arguments required to instantiate the form.            |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |
| `get_object()`              | Returns the single object that this view will display.                   |
| `render_to_response()`      | a self.response_class instance.                                          |

---

### `UpdateView` Class

- Attributes

| Attributes                                        | Description                                                      |
| ------------------------------------------------- | ---------------------------------------------------------------- |
| `content_type`                                    | The content type to use for the response                         |
| `context_object_name [get_context_object_name()]` | the name of the variable to use in the context.                  |
| `extra_context`                                   | A dictionary to include in the context.                          |
| `fields`                                          | A list of names of fields.                                       |
| `form_class [get_form_class()]`                   | The form class to instantiate.                                   |
| `http_method_names`                               | The list of available HTTP method                                |
| `initial [get_initial()]`                         | A dictionary containing initial data for the form.               |
| `model`                                           | The model that this view will display data for.                  |
| `pk_url_kwarg`                                    | The name of the URLConf keyword argument                         |
| `prefix [get_prefix()]`                           | The prefix for the generated form.                               |
| `query_pk_and_slug`                               |                                                                  |
| `queryset [get_queryset()]`                       | A QuerySet that represents the objects.                          |
| `response_class [render_to_response()]`           | The response class to be returned                                |
| `slug_field [get_slug_field()]`                   | The name of the field on the model that contains the slug.       |
| `slug_url_kwarg`                                  | The name of the URLConf keyword argument that contains the slug. |
| `success_url [get_success_url()]`                 | The URL to redirect to when the form is successfully processed.  |
| `template_engine`                                 | The NAME of a template engine                                    |
| `template_name [get_template_names()]`            | The full name of a template to use                               |
| `template_name_field`                             | The field on the current object instance                         |
| `template_name_suffix`                            | The suffix to append to template name                            |

- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `form_invalid()`            | Renders a response, providing the invalid form as context.               |
| `form_valid()`              | Redirects to get_success_url().                                          |
| `head()`                    |                                                                          |
| `put()`                     |                                                                          |
| `get()`                     |                                                                          |
| `post()`                    |                                                                          |
| `get_context_data()`        | a dictionary representing the template context                           |
| `get_form()`                | Instantiate an instance of form_class                                    |
| `get_form_kwargs()`         | Build the keyword arguments required to instantiate the form.            |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |
| `get_object()`              | Returns the single object that this view will display.                   |
| `render_to_response()`      | a self.response_class instance.                                          |

---

### `DeleteView` Class

- Attributes

| Attributes                                        | Description                                                      |
| ------------------------------------------------- | ---------------------------------------------------------------- |
| `content_type`                                    | The content type to use for the response                         |
| `context_object_name [get_context_object_name()]` | the name of the variable to use in the context.                  |
| `extra_context`                                   | A dictionary to include in the context.                          |
| `http_method_names`                               | The list of available HTTP method                                |
| `model`                                           | The model that this view will display data for.                  |
| `pk_url_kwarg`                                    | The name of the URLConf keyword argument                         |
| `query_pk_and_slug`                               |                                                                  |
| `queryset [get_queryset()]`                       | A QuerySet that represents the objects.                          |
| `response_class [render_to_response()]`           | The response class to be returned                                |
| `slug_field [get_slug_field()]`                   | The name of the field on the model that contains the slug.       |
| `slug_url_kwarg`                                  | The name of the URLConf keyword argument that contains the slug. |
| `success_url [get_success_url()]`                 | The URL to redirect to when the form is successfully processed.  |
| `template_engine`                                 | The NAME of a template engine                                    |
| `template_name [get_template_names()]`            | The full name of a template to use                               |
| `template_name_field`                             | The field on the current object instance                         |
| `template_name_suffix`                            | The suffix to append to template name                            |

- Methods

| Methods                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `as_view()`                 | Returns a callable view that takes a request and returns a response      |
| `setup()`                   | Performs key view initialization                                         |
| `dispatch()`                | accepts a request argument plus arguments, and returns an HTTP response. |
| `delete()`                  |                                                                          |
| `head()`                    |                                                                          |
| `get()`                     |                                                                          |
| `post()`                    |                                                                          |
| `get_context_data()`        | a dictionary representing the template context                           |
| `get_object()`              | Returns the single object that this view will display.                   |
| `http_method_not_allowed()` | the method to be called when an HTTP method is not supported             |
| `render_to_response()`      | a self.response_class instance.                                          |

---

[TOP](#django---built-in-class-based-generic-views)