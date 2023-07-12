# HTML - Input

[Back](./index.md)

- [HTML - Input](#html---input)
  - [`<label>` element](#label-element)
  - [`<input>` element](#input-element)

---

## `<label>` element

- The `<label>` element defines a label for several form elements.

- Attribute

  - `for`: The **for attribute** of the `<label>` tag should be equal to the **id attribute** of the `<input>` element to bind them together.

```html
<label for="fname">First name:</label>
<input type="text" id="fname" name="fname" />
```

---

## `<input>` element

- Type

| Attribute        | Description                                      |
| ---------------- | ------------------------------------------------ |
| `text`           | a single-line text input field                   |
| `search`         | a search field behaves like a regular text field |
| `email`          | an e-mail address input field                    |
| `url`            | a URL address input field                        |
| `number`         | a numeric input field                            |
| `tel`            | a telephone numbe input field                    |
| `password`       | a password field                                 |
| `button`         | a button                                         |
| `submit`         | a button to submit form data                     |
| `image`          | an image as a submit button                      |
| `reset`          | a button to reset all form values                |
| `radio`          | a radio button                                   |
| `checkbox`       | a checkbox                                       |
| `color`          | a color picker                                   |
| `date`           | a date picker for a date                         |
| `week`           | a date picker for a week and year                |
| `month`          | a date picker for a month and year               |
| `time`           | a time picker to select a time (no time zone)    |
| `datetime-local` | a date picker for a date and time(no time zone)  |
| `file`           | a file picker                                    |
| `hidden`         | a hidden input field (not visible to a user)     |
| `range`          | a slider control for a numeric value in a range  |

- Attribute

| Attribute     | Description                                           |
| ------------- | ----------------------------------------------------- |
| `value`       | an initial value for an input field                   |
| `placeholder` | a short hint that describes the expected value        |
| `multiple`    | Whether more than one value is allowed                |
| `autofocus`   | Whether an input field should automatically get focus |

- Input Restrictions

| Restrictions | Description                                             |
| ------------ | ------------------------------------------------------- |
| `checked`    | Whether an input field should be pre-selected           |
| `disabled`   | Whether an input field should be disabled               |
| `max`        | the **maximum value** for an input field                |
| `maxlength`  | the **maximum number of character** for an input field  |
| `min`        | the minimum value for an input field                    |
| `pattern`    | a regular expression to check the input value against   |
| `readonly`   | Whether an input field is read only (cannot be changed) |
| `required`   | Whether an input field is required (must be filled out) |
| `size`       | the visible width (in characters) of an input field     |
| `step`       | the legal number intervals for an input field           |

---

[TOP](#html---input)
