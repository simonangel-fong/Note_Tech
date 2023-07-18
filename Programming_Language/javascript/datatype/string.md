# JavaScript - String

[Back](../index.md)

- [JavaScript - String](#javascript---string)
  - [String](#string)
    - [Escape Character](#escape-character)
    - [String: Multiple lines text](#string-multiple-lines-text)
    - [Strings as Objects](#strings-as-objects)
  - [String Length: `length `](#string-length-length-)
  - [Template Literals](#template-literals)

---

## String

- A JavaScript string is zero or more characters written inside quotes.

  - used to store and manipulate text.
  - single or double quotes
  - use quotes inside a string, as long as they don't match the quotes surrounding the string

---

### Escape Character

- use the backslash escape character.

| Code | Result | Description          |
| ---- | ------ | -------------------- |
| `\'` | '      | Single quote         |
| `\"` | "      | Double quote         |
| `\\` | \      | Backslash            |
| `\b` |        | Backspace            |
| `\f` |        | Form Feed            |
| `\n` |        | New Line             |
| `\r` |        | Carriage Return      |
| `\t` |        | Horizontal Tabulator |
| `\v` |        | Vertical Tabulator   |

- Example:

```javascript
let text = 'We are the so-called "Vikings" from the north.';
let text = "It's alright.";
let text = "The character \\ is called backslash.";
```

---

### String: Multiple lines text

- A safer way to break up a string, is to use string addition.

```js
document.getElementById("demo").innerHTML = "Hello Dolly!";

// The \ method is not the preferred method. It might not have universal support.
// Some browsers do not allow spaces behind the \ character.
document.getElementById("demo").innerHTML =
  "Hello \
Dolly!";

document.getElementById("demo").innerHTML = "Hello " + "Dolly!";
```

---

### Strings as Objects

- Normally, JavaScript strings are primitive values, created from literals.

- Strings can also be defined as objects with the keyword `new`.

  - Do not create Strings objects.
  - The `new` keyword complicates the code and **slows down** execution speed.
  - String objects can produce unexpected results.

- Comparing two JavaScript objects **always returns false**.

```js
let x = "John"; // x is a string
let y = new String("John"); // y is an object
x == y; // true
x === y; // false

let z = new String("John"); // z is an object
y == z; // false Comparing two JavaScript objects always returns false.
y === z; // false
```

---

## String Length: `length `

- use the built-in length property

- Example:

```js
let text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let length = text.length;
```

---

## Template Literals

- **Back-Tics Syntax**:
  - `Template Literals` use back-ticks (``) rather than the quotes ("") to define a string
  - With template literals, you can use both **single and double quotes** inside a string
  - Template literals allows multiline strings

```js
var text = `Hello World!`;
var text = `He's often called "Johnny"`;
var text = `The quick
brown fox
jumps over
the lazy dog`;
```

- **Interpolation**:
  - `Template literals` provide an easy way to interpolate variables and expressions into strings. The method is called `string interpolation`, automatic replacing of variables with real values
  - `Variable Substitutions`: Template literals allow **variables** in strings

```js
var firstName = "John";
var lastName = "Doe";

var text = `Welcome ${firstName}, ${lastName}!`;
```

- `Expression Substitution`: Template literals allow **expressions** in strings:

```js
let price = 10;
let VAT = 0.25;

let total = `Total: ${(price * (1 + VAT)).toFixed(2)}`;
```

- Example: HTML Templates

```js
let header = "Templates Literals";
let tags = ["template literals", "javascript", "es6"];

let html = `<h2>${header}</h2><ul>`;
for (const x of tags) {
  html += `<li>${x}</li>`;
}

html += `</ul>`;
```

---

[TOP](#javascript-string)
