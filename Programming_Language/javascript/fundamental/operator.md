# JavaScript - Operators

[Back](../index.md)

- [JavaScript - Operators](#javascript---operators)
  - [Arithmetic Operators](#arithmetic-operators)
  - [Assignment Operators](#assignment-operators)
    - [Logical Assignment Operators](#logical-assignment-operators)
  - [Comparison Operators](#comparison-operators)
  - [Logical Operators](#logical-operators)
  - [Type Operators](#type-operators)
  - [Bitwise Operators](#bitwise-operators)
  - [Conditional (Ternary) Operator](#conditional-ternary-operator)
  - [The Nullish Coalescing Operator (`??`)](#the-nullish-coalescing-operator-)
  - [`typeof` Operator](#typeof-operator)
  - [`delete` Operator](#delete-operator)
  - [The Spread Operator: `...`](#the-spread-operator-)
  - [The `in` Operator](#the-in-operator)
  - [The `instanceof` Operator](#the-instanceof-operator)

---

## Arithmetic Operators

| Operator | Description                  |
| -------- | ---------------------------- |
| `+`      | Addition                     |
| `-`      | Subtraction                  |
| `*`      | Multiplication               |
| `**`     | Exponentiation (ES2016)      |
| `/`      | Division                     |
| `%`      | Modulus (Division Remainder) |
| `++`     | Increment                    |
| `--`     | Decrement                    |

- Operators and Operands

  - The **numbers** (in an arithmetic operation) are called `operands`.

  - The **operation** (to be performed between the two operands) is defined by an `operator`.

- Remainder

  - The modulus operator (`%`) returns the division remainder.
  - In arithmetic, the division of two integers produces a **quotient** and a **remainder**.
  - In mathematics, the result of a **modulo operation** is the **remainder** of an arithmetic division.

- **Incrementing**

  - The increment operator (`++`) increments numbers.

  ```javascript
  let x = 5;
  x++;
  let z = x; //x=6
  ```

- **Decrementing**

  - The decrement operator (`--`) decrements numbers.

- **Exponentiation**

  - The exponentiation operator (`**`) raises the first operand to the power of the second operand.

- **Precedence**

  - Operator precedence describes the **order** in which operations are performed in an arithmetic expression.

---

## Assignment Operators

| Operator | Example   | Same As      |
| -------- | --------- | ------------ |
| `=`      | `x = y`   | `x = y`      |
| `+=`     | `x += y`  | `x = x + y`  |
| `-=`     | `x -= y`  | `x = x - y`  |
| `*=`     | `x *= y`  | `x = x * y`  |
| `/=`     | `x /= y`  | `x = x / y`  |
| `%=`     | `x %= y`  | `x = x % y`  |
| `**=`    | `x **= y` | `x = x ** y` |

---

### Logical Assignment Operators

| Operator | Example | Same As          |
| -------- | ------- | ---------------- | ---------- | ------------------ |
| `&&=`    | x &&= y | x = x && (x = y) |
| `        |         | =`               | x \|\| = y | x = x \|\| (x = y) |
| `??=`    | x ??= y | x = x ?? (x = y) |

---

## Comparison Operators

| Operator | Description                       |
| -------- | --------------------------------- |
| `==`     | equal to                          |
| `===`    | equal value and equal type        |
| `!=`     | not equal                         |
| `!==`    | not equal value or not equal type |
| `>`      | greater than                      |
| `<`      | less than                         |
| `>=`     | greater than or equal to          |
| `<=`     | less than or equal to             |
| `?`      | ternary operator                  |

---

## Logical Operators

| Operator | Description |
| -------- | ----------- | --- | ---------- |
| `&&`     | logical and |
| `        |             | `   | logical or |
| `!`      | logical not |

---

## Type Operators

| Operator     | Description                                                |
| ------------ | ---------------------------------------------------------- |
| `typeof`     | Returns the type of a variable                             |
| `instanceof` | Returns true if an object is an instance of an object type |

---

## Bitwise Operators

- Bit operators work on 32 bits numbers.

- Any numeric operand in the operation is converted into a 32 bit number. The result is converted back to a JavaScript number.

| Operator | Description          | Example | Same as     | Result | Decimal |
| -------- | -------------------- | ------- | ----------- | ------ | ------- | ---- | ---- | --- |
| `&`      | AND                  | 5 & 1   | 0101 & 0001 | 0001   | 1       |
| `        | `                    | OR      | 5           | 1      | 0101    | 0001 | 0101 | 5   |
| `~`      | NOT                  | ~ 5     | ~0101       | 1010   | 10      |
| `^`      | XOR                  | 5 ^ 1   | 0101 ^ 0001 | 0100   | 4       |
| `<<`     | left shift           | 5 << 1  | 0101 << 1   | 1010   | 10      |
| `>>`     | right shift          | 5 >> 1  | 0101 >> 1   | 0010   | 2       |
| `>>>`    | unsigned right shift | 5 >>> 1 | 0101 >>> 1  | 0010   | 2       |

---

## Conditional (Ternary) Operator

- The conditional operator assigns a value to a variable based on a condition.

- Syntax:

```js
variablename = condition ? value1 : value2;
```

---

## The Nullish Coalescing Operator (`??`)

- The `??` operator returns the first argument if it is not nullish (null or undefined).
- Otherwise it returns the second argument.

- Syntax:
  - `arg1 ?? arg2`

---

## `typeof` Operator

- The `typeof` operator returns the type of a variable, object, function or expression.

| Target      | `typeof`  |
| ----------- | --------- |
| `undefined` | undefined |
| `NaN`       | number    |
| `null`      | object    |
| Array       | object    |
| Date        | object    |

---

## `delete` Operator

- The `delete` operator **deletes a property** from an object from an object.

- The `delete` operator is designed to be used on object properties. It has no effect on variables or functions.

---

## The Spread Operator: `...`

- The `...` operator expands an iterable into more elements.
- The `...` operator can be used to **expand an iterable into more arguments** for function calls.

---

## The `in` Operator

- The `in` operator returns `true` **if a property is in** an object, otherwise `false`.

```js
console.log("\n-------- in Operator --------\n");

const person = { firstName: "John", lastName: "Doe", age: 50 };

console.log("firstName" in person); //true
console.log("age" in person); //true
console.log("address" in person); //false
```

---

## The `instanceof` Operator

- The `instanceof` operator returns `true` if an object is an instance of a specified object.

```js
console.log("\n-------- instanceof Operator --------\n");

const cars = ["Saab", "Volvo", "BMW"];

console.log(cars instanceof Array); // true
console.log(cars instanceof Object); // true
console.log(cars instanceof String); // false
console.log(cars instanceof Number); // false

function Person(fname, lname) {
  this.firstName = fname;
  this.lastName = lname;
}

class Car {
  constructor(brand) {
    this.carname = brand;
  }
}

const p1 = new Person("John", "Doe");
const car = new Car("Ford");

console.log(p1 instanceof Person); //true
console.log(car instanceof Person); //false
console.log(car instanceof Car); //true
console.log(p1 instanceof Car); //false
```

---

[TOP](#javascript-operators)
