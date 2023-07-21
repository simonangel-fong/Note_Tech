# Javascript - Conditional Statement

[Back](../index.md)

- [Javascript - Conditional Statement](#javascript---conditional-statement)
  - [Conditional Statement](#conditional-statement)
  - [`if` Statement](#if-statement)
  - [`else` Statement](#else-statement)
  - [`else if` Statement](#else-if-statement)
  - [`switch` Statement](#switch-statement)
    - [The `break` Keyword](#the-break-keyword)
    - [The `default` Keyword](#the-default-keyword)
    - [Shared Block](#shared-block)

---

## Conditional Statement

- `Conditional Statement`
  - used to perform different actions based on different conditions.

| Situation to execute   | Statement |
| ---------------------- | --------- |
| condition is `true`    | `if`      |
| condition is `false`   | `else`    |
| new condition          | `else if` |
| alternative conditiona | `switch`  |

---

## `if` Statement

- Use the `if` statement to specify a block of JavaScript code to be executed if a condition is `true`.

- Syntax

```js
if (condition) {
  //  block of code to be executed if the condition is true
}
```

---

## `else` Statement

- Use the `else` statement to specify a block of code to be executed if the condition is `false`.

```js
if (condition) {
  //  block of code to be executed if the condition is true
} else {
  //  block of code to be executed if the condition is false
}
```

---

## `else if` Statement

- Use the `else if` statement to specify a **new** condition if the **first** condition is `false`.

- Syntax

```js
if (condition1) {
  //  block of code to be executed if condition1 is true
} else if (condition2) {
  //  block of code to be executed if the condition1 is false and condition2 is true
} else {
  //  block of code to be executed if the condition1 is false and condition2 is false
}
```

---

## `switch` Statement

- Use the `switch` statement to select one of many code blocks to be executed.
- The `switch` expression is evaluated once. The value of the expression is compared with the values of each case.

  - If there is a match, the associated block of code is executed.
  - If there is no match, the default code block is executed.

- If **multiple** cases matches a case value, the **first** case is selected.

- If **no matching** cases are found, the program continues to the **default** label.

- If **no default** label is found, the program **continues** to the statement(s) after the switch.

- **Strict Comparison**

  - Switch cases use **strict comparison** (`===`).

  - The values must be of the **same type** to match.

  - A strict comparison can only be true if the operands are of the same type.

- Syntax:

```js
switch (expression) {
  case value1:
    // code block
    break;
  case value2:
    // code block
    break;
  default:
  // code block
}
```

---

### The `break` Keyword

- When JavaScript reaches a `break` keyword, it **breaks out** of the switch block. This will **stop** the execution inside the switch block.

- It is not necessary to break the last case in a switch block. The block breaks (ends) there anyway.

- **Note**: If you omit the break statement, the **next case will be executed** even if the evaluation does not match the case.

---

### The `default` Keyword

- The `default` keyword specifies the code to run if there is **no case match**.

- The `default` case does **not have to be the last case** in a switch block.
  - If `default` is not the last case in the switch block, remember to end the default case with a `break`.

```js
console.log("\n-------- switch --------\n");
switch (new Date().getDay()) {
  default:
    console.log("Weekday");
    break;
  case 6:
    console.log("Saturday");
    break;
  case 0:
    console.log("Sunday");
}
```

---

### Shared Block

- When multiple cases share a code block.

```js
console.log("\n-------- switch --------\n");
switch (new Date().getDay()) {
  case 4:
  case 5:
    console.log("Soon it is Weekend");
    break;
  case 0:
  case 6:
    console.log("It is Weekend");
    break;
  default:
    console.log("Looking forward to the Weekend");
}
```

---

[TOP](#javascript---conditional-statement)
