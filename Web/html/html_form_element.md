# HTML - Form Element

[Back](./index.md)

- [HTML - Form Element](#html---form-element)
  - [`<select>` Element](#select-element)
  - [`<textarea>` Element](#textarea-element)
  - [`<fieldset>` and `<legend>` Elements](#fieldset-and-legend-elements)

---

## `<select>` Element

- The `<select>` element defines a drop-down list.

- Syntax:

```html
<label for="cars">Choose a car:</label>
<select id="cars" name="cars">
  <option value="volvo" selected>Volvo</option>
  <option value="saab">Saab</option>
  <option value="fiat">Fiat</option>
  <option value="audi">Audi</option>
</select>
```

- Attribute
  - `selected`:
    - By default, the first item in the drop-down list is selected.
    - To define a pre-selected option
  - `size`:
    - specify the number of visible values
  - `multiple`:
    - allow the user to select more than one value

---

## `<textarea>` Element

- defines a multi-line input field (a text area)

- Syntax:

```html
<textarea name="message" rows="10" cols="30">
The cat was playing in the garden.
</textarea>
```

- Attributes:

  - `rows`: specifies the **visible number of lines** in a text area.

  - `cols`: specifies the **visible width** of a text area.

---

## `<fieldset>` and `<legend>` Elements

- The `<fieldset>` element is used to **group** related data in a form.

- The `<legend>` element defines **a caption** for the `<fieldset>` element.

- Syntax

```html
<form action="/action_page.php">
  <fieldset>
    <legend>Personalia:</legend>
    <label for="fname">First name:</label><br />
    <input type="text" id="fname" name="fname" value="John" /><br />
    <label for="lname">Last name:</label><br />
    <input type="text" id="lname" name="lname" value="Doe" /><br /><br />
    <input type="submit" value="Submit" />
  </fieldset>
</form>
```

---

[TOP](#html---form-element)
