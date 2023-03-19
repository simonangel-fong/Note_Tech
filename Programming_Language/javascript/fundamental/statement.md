# JavaScript Statement

[Back](../index.md)

- [JavaScript Statement](#javascript-statement)
  - [Statement](#statement)
  - [Semicolons `;`](#semicolons-)
  - [White Space](#white-space)
  - [Line Length and Line Breaks](#line-length-and-line-breaks)
  - [Code Blocks](#code-blocks)
  - [Keywords](#keywords)

---

## Statement

- A **computer program** is a list of "instructions" to be "executed" by a computer.
  In a programming language, these programming instructions are called **statements**.

- A **JavaScript program** is a list of programming **statements**.

  - The statements are executed, one by one, in the same order as they are written.
  - **JavaScript programs** (and **JavaScript statements**) are often called `JavaScript code`.

- **JavaScript statements** are composed of:
  - Values,
  - Operators,
  - Expressions,
  - Keywords,
  - and Comments.

---

## Semicolons `;`

- Semicolons **separate** JavaScript statements.

  - Add a semicolon at the end of each executable statement.

- Ending statements with semicolon is **not required**, but **highly recommended**.

- When separated by semicolons, multiple statements **on one line** are allowed

```js
a = 5; b = 6; c = a + b;
```
---

## White Space

- JavaScript **ignores multiple spaces**. You can add white space to your script to make it more readable.
- A good practice is to put spaces around operators ( = + - * / ).

---

## Line Length and Line Breaks

- For best readability, programmers often like to avoid code lines longer than 80 characters.
- If a JavaScript statement does not fit on one line, the best place to break it is after an operator.

```js
document.getElementById("demo").innerHTML =
"Hello Dolly!";
```
---

## Code Blocks

- JavaScript statements can be **grouped together in code blocks**, inside **curly brackets** `{`...`}`.

  - The purpose of code blocks is to define statements **to be executed together**.

---

## Keywords

- JavaScript keywords are reserved words. Reserved words cannot be used as names for variables.

---

[TOP](#javascript-statement)
