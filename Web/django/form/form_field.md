# Django - Form Field

[Back](../index.md)

- [Django - Form Field](#django---form-field)
  - [`Field` Class](#field-class)
    - [Built-in Field class](#built-in-field-class)
    - [Relationships Fields](#relationships-fields)
  - [`BoundField` Class](#boundfield-class)
  - [Widget Class](#widget-class)
  - [Built-in widgets](#built-in-widgets)

---


## `Field` Class

- defining the fields of the unbound form

| Arguements/Method | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `clean(value)`    | Valiate a value or raise `ValidationError`             |
| `required`        | By default, the value is required                      |
| `label`           | specify the “human-friendly” label                     |
| `label_suffix`    | specify suffic appended after any label name           |
| `initial`         | specify the initial value                              |
| `widget`          | specify a Widget                                       |
| `help_text`       | specify descriptive text                               |
| `error_messages`  | messages that the field will raise.                    |
| `disabled`        | disables a form field                                  |
| `has_changed()`   | if the field value has changed from the initial value. |

---

### Built-in Field class

- String

| Class                   | Widget       |
| ----------------------- | ------------ |
| `CharField`             | `TextInput`  |
| `EmailField`            | `EmailInput` |
| `GenericIPAddressField` | `TextInput`  |
| `JSONField`             | `Textarea`   |
| `RegexField`            | `TextInput`  |
| `SlugField`             | `TextInput`  |
| `URLField`              | `URLInput`   |
| `UUIDField`             | `TextInput`  |

- Date Time

| Class           | Widget          |
| --------------- | --------------- |
| `DateField`     | `DateInput`     |
| `DateTimeField` | `DateTimeInput` |
| `DurationField` | `TextInput`     |
| `TimeField`     | `TimeInput`     |
-  Number

| Class          | Widget        |
| -------------- | ------------- |
| `IntegerField` | `NumberInput` |
| `DecimalField` | `NumberInput` |
| `FloatField`   | `NumberInput` |
- Selector

| Class                      | Widget              |
| -------------------------- | ------------------- |
| `BooleanField`             | `CheckboxInput`     |
| `NullBooleanField`         | `NullBooleanSelect` |
| `ChoiceField`              | `Select`            |
| `MultipleChoiceField`      | `SelectMultiple`    |
| `FilePathField`            | `Select`            |
| `TypedChoiceField`         | `Select`            |
| `TypedMultipleChoiceField` | `SelectMultiple`    |

- File

| Class        | Widget               |
| ------------ | -------------------- |
| `FileField`  | `ClearableFileInput` |
| `ImageField` | `ClearableFileInput` |

---

### Relationships Fields 

| Class                      | Widget           |
| -------------------------- | ---------------- |
| `ModelChoiceField`         | `Select`         |
| `ModelMultipleChoiceField` | `SelectMultiple` |

---

## `BoundField` Class

- Used to display HTML or access attributes for a single field of a Form instance.

| Attribute      | Description                                             |
| -------------- | ------------------------------------------------------- |
| `auto_id`      | HTML ID attribute.                                      |
| `data`         | the data for this BoundField.                           |
| `errors`       | error message                                           |
| `field`        | The form Field instance from class                      |
| `form`         | The Form instance this BoundField is bound to.          |
| `help_text`    | The help_text of the field.                             |
| `html_name`    | HTML name attribute.                                    |
| `id_for_label` | the ID of this field of label tag                       |
| `initial`      | retrieve initial data for a form field                  |
| `is_hidden`    | if this BoundField’s widget is hidden.                  |
| `label`        | The label of the field.                                 |
| `name`         | The name of this field                                  |
| `widget_type`  | the lowercased class name of the wrapped field’s widget |

| Method          | Description                                    |
| --------------- | ---------------------------------------------- |
| `__str__()`     | displays the HTML for this field.              |
| `as_hidden()`   | set type as `hidden`                           |
| `as_widget()`   | render in a given widget                       |
| `css_classes()` | return the class name or adds additional class |
| `label_tag()`   | Renders a label tag for the form field         |
| `legend_tag()`  | render the label with `<legend>` tags          |
| `value()`       | render the raw value of this field             |

---

## Widget Class

- Construct a Widget

- Syntax:
    - `Widget(attrs=None)`

- Example:
  ```py
  # example:
  name = forms.TextInput(attrs={"size": 10, "title": "Your name"})
  ```

---

## Built-in widgets

- String & Number

| Widgets         | HTML                      |
| --------------- | ------------------------- |
| `TextInput`     | `<input type="text">`     |
| `NumberInput`   | `<input type="number">`   |
| `EmailInput`    | `<input type="email">`    |
| `URLInput`      | `<input type="url">`      |
| `PasswordInput` | `<input type="password">` |
| `HiddenInput`   | `<input type="hidden">`   |
| `DateInput`     | `<input type="text">`     |
| `DateTimeInput` | `<input type="text">`     |
| `TimeInput`     | `<input type="text">`     |
| `Textarea`      | `<textarea></textarea>`   |

- Selector and checkbox

| Widgets                  | HTML                         |
| ------------------------ | ---------------------------- |
| `CheckboxInput`          | `<input type="checkbox">`    |
| `Select`                 | `<select><option></select>`  |
| `NullBooleanSelect`      | `<select><option></select>`  |
| `SelectMultiple`         | `<select multiple></select>` |
| `RadioSelect`            | `<input type="radio">`       |
| `CheckboxSelectMultiple` | `<input type="checkbox">`    |

- File upload

| Widgets              | HTML                  |
| -------------------- | --------------------- |
| `FileInput`          | `<input type="file">` |
| `ClearableFileInput` | `<input type="file">` |

- Composite widgets

| Widgets                     | Description                                  |
| --------------------------- | -------------------------------------------- |
| `MultipleHiddenInput`       | multiple hidden widgets for fields           |
| `SplitDateTimeWidget`       | `DateInput` and `TimeInput`                  |
| `SplitDateTimeWidget`       | `DateInput` and `TimeInput`                  |
| `SplitHiddenDateTimeWidget` | but uses HiddenInput for both date and time. |
| `SelectDateWidget`          | `Select` widgets:  month, day, and year.     |

---

[TOP](#django---form-field)
