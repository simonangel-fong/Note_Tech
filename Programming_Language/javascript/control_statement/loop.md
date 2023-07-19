# Javascript - Loop statement

[Back](../index.md)

- [Javascript - Loop statement](#javascript---loop-statement)
  - [Loop](#loop)
  - [`for` Loop](#for-loop)
    - [Loop Scope](#loop-scope)
  - [`for in` Loop](#for-in-loop)
  - [`for of` Loop](#for-of-loop)
  - [`while` Loop](#while-loop)
  - [`do while` Loop](#do-while-loop)
  - [The `break` \& `continue` Statement](#the-break--continue-statement)
  - [Label Code Block](#label-code-block)

---

## Loop

- `Loops` can execute a block of code a number of times.

- different kinds of loops:

  - `for`: loops through a block of **code** a number of times
  - `for/in`: loops through the **properties** of an object
  - `for/of`: loops through the **values** of an iterable object
  - `while`: loops through a block of code while a specified **condition** is true
  - `do/while`: also loops through a block of code while a specified **condition** is true

---

## `for` Loop

- The for statement creates a loop with 3 optional expressions.

```js
for (expression 1; expression 2; expression 3) {
  // code block to be executed
}
```

- **Expression 1**

  - optional
  - executed (**one** time) **before** the execution of the code block.
  - can initiate many values in expression 1 (separated by comma)
  - can omit expression 1

- **Expression 2**

  - optional
  - defines the **condition for executing** the code block.
  - If expression 2 returns `true`, the loop will **start** over again.
  - If it returns `false`, the loop will **end**.
  - If omit expression 2, must provide a `break` inside the loop. Otherwise the loop will never end.

- **Expression 3**
  - optional
  - executed (**every** time) **after** the code block has been executed.

---

### Loop Scope

```js
console.log("\n-------- for loop --------\n");
var x = 1;
for (var x = 0; x < 10; x++) {
  // some codes
}
console.log("x=", x); //x= 10

var y = 1;
for (let y = 0; y < 10; y++) {
  // some codes
}
console.log("y=", y); //y= 1
```

- In the first example, using `var`, the variable declared in the loop **redeclares** the variable outside the loop.

- In the second example, using `let`, the variable declared in the loop does **not redeclare** the variable outside the loop.

- When `let` is used to declare the y variable in a loop, the y variable will **only be visible within the loop**.

---

## `for in` Loop

- The JavaScript `for in` statement loops through the **properties** of an Object

- Syntax

```js
for (key in object) {
  // code block to be executed
}
```

- Loop object's properties

```js
console.log("\n-------- for in loop --------\n");
const person = { fname: "John", lname: "Doe", age: 25 };

for (let key in person) {
  console.log(key, person[key]);
}
// fname John
// lname Doe
// age 25
```

- Loop array's index

```js
console.log("\n-------- for in loop --------\n");
const numbers = [45, 4, 9, 16, 25];

for (let index in numbers) {
  console.log(index, numbers[index]);
}
// 0 45
// 1 4
// 2 9
// 3 16
// 4 25
```

---

## `for of` Loop

- The JavaScript `for of` statement loops through the **values** of an iterable object.

- It lets you loop over iterable data structures such as

  - Arrays,
  - Strings,
  - Maps,
  - NodeLists,
  - and more

- Syntax

```js
for (variable of iterable) {
  // code block to be executed
}
```

- `variable`:

  - For every iteration the value of the next property is assigned to the variable.
  - Variable can be declared with const, let, or var.

- `iterable`:

  - An object that **has iterable properties**.

- **Loop array**:

```js
console.log("\n-------- for of loop --------\n");
const cars = ["BMW", "Volvo", "Mini"];

for (let c of cars) {
  console.log(c);
}

// BMW
// Volvo
// Min
```

- **Loop string**:

```js
console.log("\n-------- for of loop --------\n");
let language = "JavaScript";

for (let c of language) {
  console.log(c);
}

// J
// a
// v
// a
// S
// c
// r
// i
// p
// t
```

---

## `while` Loop

- The `while` loop loops through a block of code as long as a specified **condition is true**.

- If forget to increase the variable used in the condition, the loop **will never end**.

- Syntax

```js
while (condition) {
  // code block to be executed
}
```

- Example:

```js
console.log("\n-------- while loop --------\n");
let i = 0;
while (i < 10) {
  console.log(i);
  i++;
}
// 0
// 1
// 2
// 3
// 4
// 5
// 6
// 7
// 8
// 9
```

---

## `do while` Loop

- The `do while` loop is a variant of the while loop. This loop will **execute the code block once**, before checking if the condition is true, then it will repeat the loop as long as the condition is true.

- Do not forget to increase the variable used in the condition, otherwise the loop will never end!

- Syntax

```js
do {
  // code block to be executed
} while (condition);
```

---

## The `break` & `continue` Statement

- The `break` statement can be used to **jump out of a loop**.

- The `continue` statement breaks one iteration (in the loop), if a specified condition occurs, and continues with the next iteration in the loop.

---

## Label Code Block

- To label JavaScript statements you precede the statements with a label name and a colon:

- The `break` and the `continue` statements are the only JavaScript statements that can "jump out of" a code block.

- Syntax:

```js
label: {
    // some codes
};


break labelname;

continue labelname;
```

- Example

```js
console.log("\n-------- lable + break --------\n");
const cars = ["BMW", "Volvo", "Saab", "Ford"];
list: {
  console.log(cars[0]);
  console.log(cars[1]);
  break list;
  console.log(cars[2]);
  console.log(cars[3]);
}

//BMW
// Volvo
```

- Summary

  - The `break` statement, without a label reference, can only be used to **jump out of a `loop` or a `switch`**.

  - With a label reference, the `break` statement can be used to **jump out of any code block**

  - The `continue` statement (with or without a label reference) can only be used to **skip one loop iteration**.

---

[TOP](#javascript---loop-statement)
