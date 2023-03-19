# JavaScript Data Types

[Back](../index.md)

- [JavaScript Data Types](#javascript-data-types)
  - [Data Types](#data-types)
  - [JavaScript Types are Dynamic](#javascript-types-are-dynamic)
  - [Strings](#strings)
  - [Numbers](#numbers)
  - [Exponential Notation](#exponential-notation)
  - [BigInt](#bigint)
  - [Boolean](#boolean)
  - [Arrays](#arrays)
  - [Objects](#objects)
  - [typeof Operator](#typeof-operator)
  - [Undefined](#undefined)

---

## Data Types

- JavaScript has 8 Datatypes

  1. String
  2. Number
  3. Bigint
  4. Boolean
  5. Undefined
  6. Null
  7. Symbol
  8. Object

- The Object Datatype

  1. An object
  2. An array
  3. A date

- A JavaScript variable can hold **any type of data**.

```js
// Numbers:
let length = 16;
let weight = 7.5;

// Strings:
let color = "Yellow";
let lastName = "Johnson";

// Booleans
let x = true;
let y = false;

// Object:
const person = { firstName: "John", lastName: "Doe" };

// Array object:
const cars = ["Saab", "Volvo", "BMW"];

// Date object:
const date = new Date("2022-03-25");
```

- When adding a number and a string, JavaScript will treat the number as a string.

- JavaScript evaluates expressions from left to right. Different sequences can produce different results

```js
let x = 16 + "Volvo"; //16Volvo

let x = "Volvo" + 16; //Volvo16

let x = 16 + 4 + "Volvo"; // 20Volvo

let x = "Volvo" + 16 + 4; // Volvo164
```

---

## JavaScript Types are Dynamic

- JavaScript has **dynamic types**. This means that the same variable can be used to hold different data types.

```js
let x; // Now x is undefined
x = 5; // Now x is a Number
x = "John"; // Now x is a String
```

---

## Strings

- A string (or a text string) is a series of characters.
- Strings are written with quotes. You can use **single or double quotes**.

- You can use quotes inside a string, as long as they don't match the quotes surrounding the string.

```js
// Single quote inside double quotes:
let answer1 = "It's alright";

// Single quotes inside double quotes:
let answer2 = "He is called 'Johnny'";

// Double quotes inside single quotes:
let answer3 = 'He is called "Johnny"';
```

---

## Numbers

- All JavaScript numbers are stored as decimal numbers (**floating point**).

- Numbers can be written with, or without decimals

---

## Exponential Notation

- Extra large or extra small numbers can be written with scientific (exponential) notation.

```js
let y = 123e5; // 12300000
let z = 123e-5; // 0.00123
```

---

## BigInt

- All JavaScript numbers are stored in a a 64-bit floating-point format.

- JavaScript BigInt is a new datatype (2020) that can be used to store integer values that are too big to be represented by a normal JavaScript Number.

---

## Boolean

- Booleans can only have two values: true or false.

- Booleans are often used in conditional testing.

---

## Arrays

- JavaScript arrays are written with **square brackets**.

- Array items are **separated by commas**.

- Array indexes are zero-based, which means the first item is `[0]`, second is `[1]`, and so on.

```js
const cars = ["Saab", "Volvo", "BMW"];
```

---

## Objects

- JavaScript objects are written with curly braces `{}`.

- Object properties are written as `name:value` pairs, **separated by commas**.

```js
const person = {
  firstName: "John",
  lastName: "Doe",
  age: 50,
  eyeColor: "blue",
};
```

---

## typeof Operator

- The typeof operator returns the type of a variable or an expression.

```js
typeof ""; // Returns "string"
typeof "John"; // Returns "string"
typeof "John Doe"; // Returns "string"
typeof 0; // Returns "number"
typeof 314; // Returns "number"
typeof 3.14; // Returns "number"
typeof 3; // Returns "number"
typeof (3 + 4); // Returns "number"
```

---

## Undefined

- In JavaScript, a variable **without a value**, has the value `undefined`. The type is also undefined.
- Any variable can be emptied, by setting the value to undefined. The type will also be undefined.

```js
let car; // Value is undefined, type is undefined

let car = "Volvo";
car = undefined; //undefined
typeof car; //undefined
```

---

[TOP](#javascript-data-types)
