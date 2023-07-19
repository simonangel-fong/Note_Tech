# JavaScript - Number Method

[Back](../index.md)

- [JavaScript - Number Method](#javascript---number-method)
  - [Cheapsheet](#cheapsheet)
  - [Converting Data Type](#converting-data-type)
    - [`.toString()`](#tostring)
    - [`.valueOf()`](#valueof)
    - [`Number(value)`](#numbervalue)
    - [`parseInt(value)`](#parseintvalue)
    - [`parseFloat(value)`](#parsefloatvalue)
  - [Converting Precision](#converting-precision)
    - [`.toExponential(decimalValue)`](#toexponentialdecimalvalue)
    - [`.toFixed(decimalValue)`](#tofixeddecimalvalue)
    - [`.toPrecision(length)`](#toprecisionlength)
  - [Number Object Method](#number-object-method)
    - [`Number.isInteger()`](#numberisinteger)
    - [`Number.isSafeInteger()`](#numberissafeinteger)
    - [`Number.parseFloat()`](#numberparsefloat)
    - [`Number.parseInt()`](#numberparseint)

---

## Cheapsheet

- Converting Data Type

| Method         | Description                                             |
| -------------- | ------------------------------------------------------- |
| `.toString()`  | Returns a number as a string                            |
| `.valueOf()`   | Returns a number as a number                            |
| `Number()`     | Returns a number converted from its argument.           |
| `parseFloat()` | Parses its argument and returns a floating point number |
| `parseInt()`   | Parses its argument and returns a whole number          |

- Converting Precision

| Method                         | Description                                        |
| ------------------------------ | -------------------------------------------------- |
| `.toExponential(decimalValue)` | Returns a number written in exponential notation   |
| `.toFixed(decimalValue)`       | Returns a number written with a number of decimals |
| `.toPrecision(length)`         | Returns a number written with a specified length   |

- Number Object Method

| Method                   | Description                                    |
| ------------------------ | ---------------------------------------------- |
| `Number.isInteger()`     | Returns true if the argument is an integer     |
| `Number.isSafeInteger()` | Returns true if the argument is a safe integer |
| `Number.parseFloat()`    | Converts a string to a number                  |
| `Number.parseInt()`      | Converts a string to a whole number            |

---

## Converting Data Type

### `.toString()`

```js
console.log("\n--- toString() ---\n");

// toString()
// returns a number as a string.
// All number methods can be used on any type of numbers (literals, variables, or expressions)
console.log((123).toString()); //123, literals

var x = 123;
console.log(x.toString()); //123, variables
console.log((100 + 23).toString()); //123, expressions
```

---

### `.valueOf()`

```js
console.log("\n--- valueOf() ---\n");

// valueOf()
// returns a number as a number

console.log((123).valueOf()); //123, literal
console.log((100 + 23).valueOf()); //123, expression

var x = 123;
console.log(x.valueOf()); //123, variable
console.log(typeof x.valueOf()); //number
```

---

### `Number(value)`

```js
console.log("\n--- Number(value) ---\n");

// Number()
// Returns a number converted from its argument.
// If the number cannot be converted, NaN (Not a Number) is returned.

console.log(Number(true)); //1
console.log(Number(false)); //0
console.log(Number("10")); //10
console.log(Number(" 10")); //10
console.log(Number("10 ")); //10
console.log(Number(" 10 ")); //10
console.log(Number("10.33")); //10.33
console.log(Number("10,33")); //NaN
console.log(Number("10 33")); //NaN
console.log(Number("John")); //NaN

// The Date() method returns the number of milliseconds since 1.1.1970.
console.log(Number(new Date("1970-01-01"))); //0
console.log(Number(new Date("2017-09-30"))); //1506729600000
console.log(Number(new Date())); //the number of milliseconds todate
```

---

### `parseInt(value)`

```js
console.log("\n--- parseInt(value) ---\n");

// parseInt()
// Parses its argument and returns a whole number
// If the number cannot be converted, NaN (Not a Number) is returned.

console.log(parseInt("-10")); //-10
console.log(parseInt("-10.33")); //-10
console.log(parseInt("10")); //10
console.log(parseInt("10.33")); //10
console.log(parseInt("years 10")); //NaN

// Only the first number is returned
console.log(parseInt("10 20 30")); //10
console.log(parseInt("10 years")); //10
```

---

### `parseFloat(value)`

```js
console.log("\n--- parseFloat(value) ---\n");

// parseFloat()
// parses a string and returns a number. Spaces are allowed.
// Only the first number is returned

console.log(parseFloat("10")); //10
console.log(parseFloat("10.33")); //10.33
console.log(parseFloat("10 20 30")); //10
console.log(parseFloat("10 years")); //10
console.log(parseFloat("years 10")); //NaN
```

---

## Converting Precision

### `.toExponential(decimalValue)`

```js
console.log("\n--- toExponential(decimalValue) ---\n");

// toExponential(decimalValue)
// returns a string, with a number rounded and written using exponential notation.

// Parameter      Descriptions
// decimalValue   optional, the number of characters behind the decimal point
var x = 9.656;
console.log(x.toExponential()); //9.656e+0
console.log(x.toExponential(2)); //9.66e+0
console.log(x.toExponential(4)); //9.6560e+0
console.log(x.toExponential(6)); //9.656000e+0
```

---

### `.toFixed(decimalValue)`

```js
console.log("\n--- toFixed(decimalValue) ---\n");

// toFixed()
// returns a string, with the number written with a specified number of decimals
var x = 9.656;
console.log(x.toFixed()); //10
console.log(x.toFixed(0)); //10
console.log(x.toFixed(2)); //9.66
console.log(x.toFixed(4)); //9.6560
console.log(x.toFixed(6)); //9.656000
```

---

### `.toPrecision(length)`

```js
console.log("\n--- toPrecision(length) ---\n");

// toPrecision(length)
// returns a string, with a number written with a specified length

// Parameter Descriptions
// decimalValue a specified number of decimals

var x = 9.656;
console.log(x.toPrecision()); //9.656
console.log(x.toPrecision(1)); //1e+1
console.log(x.toPrecision(2)); //9.7
console.log(x.toPrecision(4)); //9.656
console.log(x.toPrecision(6)); //9.65600
```

---

## Number Object Method

### `Number.isInteger()`

```js
console.log("\n--- Number.isInteger() ---\n");

// Number.isInteger()
// returns true if the argument is an integer.
console.log(Number.isInteger(10)); //true
console.log(Number.isInteger(10.5)); //false
```

---

### `Number.isSafeInteger()`

```js
console.log("\n--- Number.isSafeInteger() ---\n");

// Number.isSafeInteger()
// returns true if the argument is a safe integer.
// A safe integer is an integer that can be exactly represented as a double precision number.
// Safe integers are all integers from -(253 - 1) to +(253 - 1).
// This is safe: 9007199254740991. This is not safe: 9007199254740992.
console.log(Number.isSafeInteger(10)); //true
console.log(Number.isSafeInteger(12345678901234567890)); //false
```

---

### `Number.parseFloat()`

```js
console.log("\n--- Number.parseFloat() ---\n");

// Number.parseFloat()
// parses a string and returns a number.
// Spaces are allowed. Only the first number is returned.
// If the number cannot be converted, NaN (Not a Number) is returned.
console.log(Number.parseFloat("10")); //10
console.log(Number.parseFloat("10.33")); //10.33
console.log(Number.parseFloat("10 20 30")); //10
console.log(Number.parseFloat("10 years")); //10
console.log(Number.parseFloat("years 10")); //NaN
```

---

### `Number.parseInt()`

```js
console.log("\n--- Number.parseInt() ---\n");

// Number.parseInt()
// parses a string and returns a whole number.
// Spaces are allowed. Only the first number is returned.
// If the number cannot be converted, NaN (Not a Number) is returned.
console.log(Number.parseInt("-10")); //-10
console.log(Number.parseInt("-10.33")); //-10
console.log(Number.parseInt("10")); //10
console.log(Number.parseInt("10.33")); //10
console.log(Number.parseInt("10 20 30")); //10
console.log(Number.parseInt("10 years")); //10
console.log(Number.parseInt("years 10")); //NaN
```

---

[TOP](#javascript---number-method)
