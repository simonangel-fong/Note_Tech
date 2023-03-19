# JavaScript Operators

[Back](../index.md)

- [JavaScript Operators](#javascript-operators)
  - [Arithmetic Operators](#arithmetic-operators)
    - [Operators and Operands](#operators-and-operands)
    - [Remainder](#remainder)
    - [Incrementing](#incrementing)
    - [Decrementing](#decrementing)
    - [Exponentiation](#exponentiation)
    - [Precedence](#precedence)
  - [Assignment Operators](#assignment-operators)
    - [Logical Assignment Operators](#logical-assignment-operators)
  - [Comparison Operators](#comparison-operators)
  - [Logical Operators](#logical-operators)
  - [Type Operators](#type-operators)
  - [Bitwise Operators](#bitwise-operators)

---

## Arithmetic Operators

| Operator | Description                  |
| -------- | ---------------------------- |
| `+`      | Addition                     |
| `-`      | Subtraction                  |
| `*`      | Multiplication               |
| `\*\*`   | Exponentiation (ES2016)      |
| `/`      | Division                     |
| `%`      | Modulus (Division Remainder) |
| `++`     | Increment                    |
| `--`     | Decrement                    |

### Operators and Operands

- The **numbers** (in an arithmetic operation) are called `operands`.

- The **operation** (to be performed between the two operands) is defined by an `operator`.

### Remainder

- The modulus operator (`%`) returns the division remainder.
- In arithmetic, the division of two integers produces a **quotient** and a **remainder**.
  - In mathematics, the result of a **modulo operation** is the **remainder** of an arithmetic division.

### Incrementing

The increment operator (`++`) increments numbers.

```javascript
let x = 5;
x++;
let z = x; //x=6
```

### Decrementing

The decrement operator (`--`) decrements numbers.

### Exponentiation

The exponentiation operator (`**`) raises the first operand to the power of the second operand.

### Precedence

Operator precedence describes the **order** in which operations are performed in an arithmetic expression.

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

[TOP](#javascript-operators)
