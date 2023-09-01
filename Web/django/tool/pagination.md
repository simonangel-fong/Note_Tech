# Django - Pagination

[Back](../index.md)

- [Django - Pagination](#django---pagination)
  - [`Paginator` class](#paginator-class)
  - [`Page` class](#page-class)
  - [Exceptions](#exceptions)
  - [Using `ListView`](#using-listview)
  - [Using Paginator in a view function](#using-paginator-in-a-view-function)

---

## `Paginator` class

- Pagination use the `Paginator` class

- **Constructor**

```py
Paginator(object_list, per_page, orphans=0, allow_empty_first_page=True)
# object_list: 
```

- Parameter:

| Parameter    | Description                                                        |
| ------------ | ------------------------------------------------------------------ |
| `ELLIPSIS`   | A translatable string used as a substitute for elided page numbers |
| `count`      | The total number of **objects**, across all pages.                 |
| `num_pages`  | The total number of **pages**.                                     |
| `page_range` | A 1-based range iterator of page numbers,                          |


- **Attributes**

| Attribute                | Description                                                |
| ------------------------ | ---------------------------------------------------------- |
| `object_list`            | Required. A list of sliceable object                       |
| `per_page`               | Required. The maximum number of items to include on a page |
| `orphans`                | The maximum number of items on last page                   |
| `allow_empty_first_page` | Whether the first page can to be empty                     |

- **Methods**

| Method                          | Description                                           |
| ------------------------------- | ----------------------------------------------------- |
| `get_page(number)`              | Returns a `Page` object with the given 1-based index  |
| `page(number)`                  | Returns a `Page` object with the given 1-based index. |
| `get_elided_page_range(number)` | Returns a 1-based list of page numbers                |

---

## `Page` class

- **Constructor**

- A page acts like a sequence of `Page.object_list` when using `len()` or iterating it directly.

```py
Page(object_list, number, paginator)
# object_list: 
```

- **Methods**:

| Method                   | Description                                                |
| ------------------------ | ---------------------------------------------------------- |
| `has_next()`             | Returns True if there’s a next page.                       |
| `has_previous()`         | Returns True if there’s a previous page.                   |
| `has_other_pages()`      | Returns True if there’s a next or previous page.           |
| `next_page_number()`     | Returns the next page number.                              |
| `previous_page_number()` | Returns the previous page number.                          |
| `start_index()`          | Returns the 1-based index of the first object on the page. |
| `end_index()`            | Returns the 1-based index of the last object on the page.  |

- **Attributes**

| Attribute     | Description                            |
| ------------- | -------------------------------------- |
| `object_list` | The list of objects on this page.      |
| `number`      | The 1-based page number for this page. |
| `paginator`   | The associated Paginator object.       |

---

## Exceptions

| Exception          | Description                                                                  |
| ------------------ | ---------------------------------------------------------------------------- |
| `InvalidPage`      | Raised when a paginator is passed an invalid page number.                    |
| `PageNotAnInteger` | Raised when page() is given a value that isn’t an integer.                   |
| `EmptyPage`        | Raised when page() is given a valid value but no objects exist on that page. |

---

## Using `ListView`

- Using the `paginate_by` attribute to define maximum items per page.

- Example:


```py
# Blog/views.py
class ListBlog(ListView):
    # limits the number of objects per page, adds a paginator and page_obj to the context.
    paginate_by = 4
    model = Blog
```

```html
<!-- display objects on current page -->
<ul class="list-group">
  {% for blog in page_obj %}
  <li class="list-group-item">
    <a href="{% url 'Blog:detail' blog.pk %}">{{blog.title|upper}}</a>
  </li>
  {% endfor %}
</ul>
<!-- pagination -->
<nav aria-label="Page navigation d-flex">
  <ul class="pagination">
    <li class="page-item me-auto">
      <a class="nav-link disabled" aria-disabled="true">
        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
      </a>
    </li>
    {% if page_obj.has_previous %}
    <li class="page-item">
      <a class="page-link" href="?page=1">&laquo; </a>
    </li>
    <li class="page-item">
      <a class="page-link" href="?page={{ page_obj.previous_page_number }}"
        >Previous</a
      >
    </li>
    {% endif %}

    <li class="page-item active" aria-current="page">
      <span class="page-link">{{ page_obj.number }}</span>
    </li>

    {% if page_obj.has_next %}
    <li class="page-item">
      <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
    </li>
    <li class="page-item">
      <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">
        &raquo;
      </a>
    </li>
    {% endif %}
  </ul>
</nav>

```

---

## Using Paginator in a view function

- Example:

```py
# Blog/views.py
from django.core.paginator import Paginator

def listing(request):
    contact_list = Blog.objects.all()
    paginator = Paginator(contact_list, 5)  # Creates a paginator

    page_number = request.GET.get("page")   # Get the page number from request
    page_obj = paginator.get_page(page_number)  # Creates a page object
    return render(request, "Blog/blog_list.html", {"page_obj": page_obj}) # return the page object
```

```html
<!-- display objects on current page -->
<ul class="list-group">
  {% for blog in page_obj %}
  <li class="list-group-item">
    <a href="{% url 'Blog:detail' blog.pk %}">{{blog.title|upper}}</a>
  </li>
  {% endfor %}
</ul>

<!-- pagination -->
<ul class="nav pagination d-flex justify-content-between">
  {% if page_obj.has_previous %}
  <li class="page-item">
    <a class="nav-link" aria-current="page" href="?page=1">&laquo; first</a>
  </li>
  <li class="page-item">
    <a class="nav-link" href="?page={{ page_obj.previous_page_number }}"
      >previous</a
    >
  </li>
  {% endif %}
  <li class="nav-item mx-auto">
    <a class="nav-link disabled" aria-disabled="true">
      {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}
    </a>
  </li>
  {% if page_obj.has_next %}
  <li class="nav-item">
    <a class="nav-link" href="?page={{ page_obj.next_page_number }}"> next </a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="?page={{ page_obj.paginator.num_pages }}">
      last &raquo;
    </a>
  </li>
  {% endif %}
</ul>

```



---

[TOP](#django---pagination)

