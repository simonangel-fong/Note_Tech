# Python Operator

[Back](../index.md)

- [Python Operator](#python-operator)
  - [Arithmetic Operator](#arithmetic-operator)
  - [Comparison Operator](#comparison-operator)
  - [Logical Operator](#logical-operator)
  - [Ternary Operator](#ternary-operator)
  - [Identity Operators](#identity-operators)
  - [Membership Operators](#membership-operators)
  - [Operator Precedence](#operator-precedence)

---

- Operators are used to **perform operations on variables and values**.

## Arithmetic Operator

| Operator | Name                  | Example  |
| -------- | --------------------- | -------- |
| `+`      | Addition              | x + y    |
| `-`      | Subtraction           | x - y    |
| `*`      | Multiplication        | x \* y   |
| `/`      | Division              | x / y    |
| `%`      | Modulus 取模(余数)    | x % y    |
| `**`     | Exponentiation        | x \*\* y |
| `//`     | Floor division 取整除 | x//y     |

---

## Comparison Operator

| Operator | Name                     | Example |
| -------- | ------------------------ | ------- |
| `==`     | Equal                    | x == y  |
| `!=`     | Not equal                | x != y  |
| `>`      | Greater than             | x > y   |
| `<`      | Less than                | x < y   |
| `>=`     | Greater than or equal to | x >= y  |
| `<=`     | Less than or equal to    | x <= y  |

---

## Logical Operator

| Operator | Description                                             | Example               |
| -------- | ------------------------------------------------------- | --------------------- |
| `and`    | Returns True if both statements are true                | x < 5 and x < 10      |
| `or`     | Returns True if one of the statements is true           | x < 5 or x < 4        |
| `not`    | Reverse the result, returns False if the result is true | not(x < 5 and x < 10) |

---

## Ternary Operator

```py
# Ternary operator
a, b = 10, 20
min = a if a < b else b
print(min)    # 10
```

---

## Identity Operators

- `Identity operator`: compare the objects, not if they are equal, but if they are **actually the same object**, with the **same memory location**.

| Operator | Description                                            | Example    |
| -------- | ------------------------------------------------------ | ---------- |
| `is`     | Returns True if both variables are the same object     | x is y     |
| `is not` | Returns True if both variables are not the same object | x is not y |

---

## Membership Operators

- `Membership operator` : test if a **sequence is presented in an object**.

| Operator | Description                                                                      | Example    |
| -------- | -------------------------------------------------------------------------------- | ---------- |
| `in`     | Returns True if a sequence with the specified value is present in the object     | x in y     |
| `not in` | Returns True if a sequence with the specified value is not present in the object | x not in y |

---

## Operator Precedence

| Operator                                                | Description                                           |
| ------------------------------------------------------- | ----------------------------------------------------- | ---------- |
| `()`                                                    | Parentheses                                           |
| `**`                                                    | Exponentiation                                        |
| `+x` `-x` `~x`                                          | Unary plus, unary minus, and bitwise NOT              |
| `*` `/` `//` `%`                                        | Multiplication, division, floor division, and modulus |
| `+` `-`                                                 | Addition and subtraction                              |
| `<<` `>>`                                               | Bitwise left and right shifts                         |
| `&`                                                     | Bitwise AND                                           |
| `^`                                                     | Bitwise XOR                                           |
| `                                                       | `                                                     | Bitwise OR |
| `==` `!=` `>` `>=` `<` `<=` `is` `is not` `in` `not in` | Comparisons, identity, and membership operators       |
| `not`                                                   | Logical NOT                                           |
| `and`                                                   | AND                                                   |
| `or`                                                    | OR                                                    |

---

[TOP](#python-operator)
