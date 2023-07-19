# JavaScript - Error

[Back](../index.md)

- [JavaScript - Error](#javascript---error)
  - [Errors](#errors)
  - [`throw` Statement](#throw-statement)
  - [`try catch`](#try-catch)
  - [`finally` Statement](#finally-statement)
  - [`Error` Object](#error-object)
    - [Error Name Values](#error-name-values)

---

## Errors

- `Errors` can be

  - coding errors made by the programmer,
  - errors due to wrong input,
  - and other unforeseeable things.

- JavaScript will **throw an exception (throw an error).**:
  - When an `error` occurs, JavaScript will normally stop and generate an error message.
  - JavaScript will actually create an `Error` object with **two properties**: `name` and `message`.

---

## `throw` Statement

- The `throw` statement **creates a custom error**.
- If you use `throw` together with `try` and `catch`, you can control program flow and generate custom error messages.

- Syntax:

```js
throw `stringMessage`;
throw 500;
```

---

## `try catch`

- `try` statement

  - defines a code block to **run** (to try).

- `catch` statement

  - defines a code block to **handle any error**.

- `try` and `catch` come **in pairs**.

- Syntax:

```js
try {
  //   Block of code to try
} catch (err) {
  //   Block of code to handle errors
}
```

---

## `finally` Statement

The `finally` statement defines a code block to run regardless of the result.

```js
Syntax;
try {
  //   Block of code to try
} catch (err) {
  //   Block of code to handle errors
} finally {
  //   Block of code to be executed regardless of the try / catch result
}
```

---

## `Error` Object

- JavaScript has a built-in `error` object that provides **error information** when an **error occurs**.

- The `error` object provides two useful properties:
  - name
  - message.

| Property  | Description                 |
| --------- | --------------------------- |
| `name`    | an error name               |
| `message` | an error message (a string) |

---

### Error Name Values

- Six different values can be returned by the error name property:

| Error Name       | Description                                  |
| ---------------- | -------------------------------------------- |
| `EvalError`      | An error has occurred in the eval() function |
| `RangeError`     | A number "out of range" has occurred         |
| `ReferenceError` | An illegal reference has occurred            |
| `SyntaxError`    | A syntax error has occurred                  |
| `TypeError`      | A type error has occurred                    |
| `URIError`       | An error in encodeURI() has occurredds       |

- `RangeError`: a number that is **outside the range of legal values**.
- `ReferenceError`: a variable that has **not been declared**
- `SyntaxError`: code with a **syntax error**.
- `TypeError`: a value that is outside the range of expected types.
- `URIError`: illegal characters in a URI function:

---

[TOP](#javascript---error)
