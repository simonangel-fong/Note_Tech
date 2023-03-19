# JavaScript Numbers

[back](../index.md)

- [JavaScript Numbers](#javascript-numbers)
  - [Number](#number)
  - [Integer Precision](#integer-precision)
  - [Floating Precision](#floating-precision)
  - [Adding Numbers and Strings](#adding-numbers-and-strings)
  - [Numeric Strings](#numeric-strings)
  - [NaN - Not a Number](#nan---not-a-number)
  - [Infinity](#infinity)
  - [Hexadecimal 十六进制](#hexadecimal-十六进制)
  - [Numbers as Objects](#numbers-as-objects)

---

## Number

- JavaScript has only one type of number. Numbers can be written with or without decimals.
- Extra large or extra small numbers can be written with scientific (exponent) notation

- Unlike many other programming languages, `JavaScript` **does not define different types of numbers**, like integers, short, long, floating-point etc.

- JavaScript numbers are **always stored as double precision floating point numbers**, following the international IEEE 754 standard.

- This format stores numbers **in 64 bits**, where the number (the fraction) is stored in bits 0 to 51, the exponent in bits 52 to 62, and the sign in bit 63

```js
let x = 123e5; // 12300000
let y = 123e-5; // 0.00123
```

---

## Integer Precision

- Integers (numbers without a period or exponent notation) are accurate up to **15 digits**.

- The maximum number of decimals is 17.

---

## Floating Precision

Floating point arithmetic is not always 100% accurate. it helps to multiply and divide:

```js
let x = (0.2 * 10 + 0.1 * 10) / 10;
```

---

## Adding Numbers and Strings

- `+` operator for both addition and concatenation.

| Operand 1st | Operand 2nd | Result        |
| ----------- | ----------- | ------------- |
| Number      | Number      | Number        |
| String      | String      | Concatenation |
| Number      | String      | Concatenation |
| String      | Number      | Concatenation |

---

## Numeric Strings

JavaScript will try to convert strings to numbers in all numeric operations:

```js
let x = "100";
let y = "10";
var z = x / y; //10
var z = x * y; //1000
var z = x - y; //90
var z = x + y; //"10010"
```

---

## NaN - Not a Number

- `NaN` is a JavaScript reserved word indicating that a number is **not a legal number**.

- `NaN` is a **number**: `typeof NaN` returns `number`.

- use the global JavaScript function `isNaN()` to find out if a value is a not a number

- If you use `NaN` in a mathematical operation, the result will also be `NaN` or be a concatenation.

```js
var x = 100 / "Apple";
console.log(x); //NaN
console.log(isNaN(x)); //true

var x = 100 / "10";
console.log(x); //10
console.log(isNaN(x)); //false

var x = NaN;
var y = 5;
console.log(x + y); //NaN

var x = NaN;
var y = "5";
console.log(x + y); //NaN5

console.log(typeof x); //number
```

---

## Infinity

- `Infinity` (or `-Infinity`) is the value JavaScript will return if you calculate a number **outside the largest possible number**.

- Division by 0 (zero) also generates `Infinity`.

- Infinity is a number.

```js
var x = 2;
while (x != Infinity) {
  // while (isFinite(x)) {
  console.log(x);
  x **= 2;
}
// 2
// 4
// 16
// 256
// 65536
// 4294967296
// 18446744073709552000
// 3.402823669209385e+38
// 1.157920892373162e+77
// 1.3407807929942597e+154

var y = 2 / 0;

console.log(isFinite(y)); //false
console.log(y == Infinity); //true
console.log(y); //Infinity

console.log(typeof Infinity); //number
```

---

## Hexadecimal 十六进制

- JavaScript interprets numeric constants as `hexadecimal` if they are **preceded by 0x**.

- By default, JavaScript displays numbers as base **10** decimals.

- But you can use the `toString()` method to output numbers from base **2 to base 36**.

- Hexadecimal is base 16. Decimal is base 10. Octal is base 8. Binary is base 2.

```js
var x = 0xff;

console.log(x); //255
console.log(x.toString(2)); //11111111
console.log(x.toString(8)); //377
console.log(x.toString(10)); //255
console.log(x.toString(16)); //ff
console.log(x.toString(32)); //7v
```

---

## Numbers as Objects

- numbers can also be defined as objects with the keyword `new`.

- Do not create Number objects.

- The `new` keyword complicates the code and slows down execution speed.

- Number Objects can produce unexpected results

```js
var x = 500;
var y = new Number(500);
var z = new Number(500);

console.log(x == y); //true
console.log(x === y); //false

console.log(y == z); //false
console.log(y === z); //false
```

---

[top](#javascript-string-method)
