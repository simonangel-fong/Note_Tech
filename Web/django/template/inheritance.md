# Django - Template inheritance

[Back](../index.md)

- [Django - Template inheritance](#django---template-inheritance)
  - [Template Inheritance](#template-inheritance)
  - [Example: Template Inheritance](#example-template-inheritance)

---

## Template Inheritance

- `Template inheritance`

  - allows to build a base “skeleton” template that contains all the common elements of site and defines blocks that child templates can override.

- `base template`

  - a html template defines an HTML skeleton document

- `child templates`:

  - a html template to fill the empty blocks with content.

- `block tag`:

  - defines blocks that child templates can fill in.
  - indicates the template engine that a child template may override those portions of the template.

- `extends tag`:

  - identifies the parent template
  - indicates the template engine that this template inherits from a base template

- When a tag is not defined by the children templates, the content in base template will apply.

- When the content of the block from the parent template is needed in child template, the tag `{{ block.super }}` can be used.

---

## Example: Template Inheritance

- `base.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="style.css" />
    <title>__ block title __ My amazing site__ endblock __</title>
  </head>

  <body>
    <div id="sidebar">
      __ block sidebar __
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/blog/">Blog</a></li>
      </ul>
      __ endblock __
    </div>

    <div id="content">__ block content __ __ endblock __</div>
  </body>
</html>
```

- `child.html`

```html
__ extends "base.html" __ __ block title __My amazing blog__ endblock __ __
block content __ __ for entry in blog_entries __
<h2>{{ entry.title }}</h2>
<p>{{ entry.body }}</p>
__ endfor __ __ endblock __
```

---

[TOP](#django---template-inheritance)
