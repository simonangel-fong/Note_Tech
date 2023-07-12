# HTML - List

[Back](./index.md)

[TOC]

---

## Unordered Lists

- **Example**

<ul>
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>

```html
<ul>
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>
```

---

### List Item Marker

The CSS `list-style-type` property is used to define the style of the list item marker.<br>原点样式

| Value  | Description                                         |
| ------ | --------------------------------------------------- |
| disc   | Sets the list item marker to a bullet (default)方框 |
| circle | Sets the list item marker to a circle 圈            |
| square | Sets the list item marker to a square               |
| none   | The list items will not be marked 无 bullet point   |

- Example:

<!-- style is attribute, value is that followed equal sign -->
<ul style="list-style-type: square;">
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>

```html
<!-- style is attribute, value is that followed equal sign -->
<ul style="list-style-type: square;">
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>
```

---

## Ordered Lists

The HTML `<ol>` tag defines an ordered list. An ordered list can be numerical or alphabetical.<br>可以是数字或字母

### The Type Attribute

| Value    | Description                                                      |
| -------- | ---------------------------------------------------------------- |
| type="1" | The list items will be numbered with **numbers** (default)       |
| type="A" | The list items will be numbered with **uppercase letters**       |
| type="a" | The list items will be numbered with **lowercase letters**       |
| type="I" | The list items will be numbered with **uppercase roman numbers** |
| type="i" | The list items will be numbered with **lowercase roman numbers** |

---

[TOP](#html---list)
