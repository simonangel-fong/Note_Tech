# JavaScript String

[Back](../index.md)

- [JavaScript String](#javascript-string)
  - [String](#string)
    - [Escape Character](#escape-character)
    - [Breaking Long Code Lines](#breaking-long-code-lines)
    - [Strings as Objects](#strings-as-objects)
  - [Length](#length)
  - [Method](#method)
  - [Search Method](#search-method)
  - [Template Literals](#template-literals)

---

## String

- A JavaScript string is zero or more characters written inside quotes.

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

### Breaking Long Code Lines

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
y == z; // false
y === z; // false
```

---

## Length

- use the built-in length property

- Example:

```js
let text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let length = text.length;
```

---

## Method

[String example](string_method.md)

| Method                        | Description                                                       |
| ----------------------------- | ----------------------------------------------------------------- |
| `slice(start, end)`           | extracting a part of a string                                     |
| `substring(start, end)`       | extracting a part of a string                                     |
| `replace(matched, target)`    | replaces a specified value with another value in a string         |
| `replaceAll(matched, target)` | replaces all value with another value                             |
| `toUpperCase()`               | A string is converted to **upper** case                           |
| `toLowerCase()`               | A string is converted to **lower** case                           |
| `concat(str, str)`            | joins two or more strings                                         |
| `trim()`                      | removes whitespace from both sides of a string                    |
| `trimStart()`                 | removes whitespace only from the start of a string.               |
| `trimEnd()`                   | removes whitespace only from the end of a string                  |
| `padStart(length, str)`       | pads a string with another string                                 |
| `padEnd(length, str)`         | pads a string with another string                                 |
| `charAt(index)`               | returns the character at a specified index (position) in a string |
| `charCodeAt(index)`           | returns the unicode of the character at a specified index         |
| `string[index]`               | returns the character at a specified index (position) in a string |
| `split(separator)`            | returns the character at a specified index (position) in a string |
| `String.valueOf()`            | convert a string object into a string                             |

---

## Search Method

[String example](string_method.md)

| Method                             | Description                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| `indexOf(target, start_index)`     | returns the index of (position of) the first occurrence of a string in a string  |
| `lastIndexOf(target, start_index)` | returns the index of the last occurrence of a specified text in a string         |
| `search(target)`                   | returns the position of the match                                                |
| `match(target)`                    | returns an array containing the results of matching a string against a string    |
| `matchAll(target)`                 | returns an iterator containing the results of matching a string against a string |
| `includes(target, start_index)`    | returns true if a string contains a specified value.                             |
| `startsWith(target, start_index)`  | returns true if a string begins with a specified value.                          |

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
