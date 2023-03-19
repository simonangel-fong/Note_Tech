# JavaScript Variable

[Back](../index.md)

- [JavaScript Variable](#javascript-variable)
  - [Declaration](#declaration)
  - [Identifiers](#identifiers)
  - [`let`](#let)
    - [Redeclaring Variables](#redeclaring-variables)
    - [Hoisting](#hoisting)
  - [`const`](#const)
    - [Redeclaring](#redeclaring)
    - [Block Scope](#block-scope)
    - [Hoisting](#hoisting-1)

---

## Declaration

- Syntax:

```js
// Using var
var variable_name;

// Using let
let variable_name;

// Using const
const constant_name;

// declare many variables in one statement.
let person = "John Doe", carName = "Volvo", price = 200;

// A declaration can span multiple lines:
let person = "John Doe",
carName = "Volvo",
price = 200;

```

- After the declaration, the variable has **no value** (technically it is `undefined`).

- When to Use JavaScript `var`?

  - Always declare JavaScript variables with `var`,`let`, or `const`.
  - The `var` keyword is used in all JavaScript code from 1995 to 2015.
  - The `let` and `const` keywords were added to JavaScript in 2015.
  - If you want your code to run **in older browsers**, you must use `var`.

- `const`: the value of the variable **cannot change**.
- `let`: the value of the variable **can be changed**.

- It's a good programming practice to declare all variables **at the beginning of a script**.

- If you `re-declare` a JavaScript variable declared with var, it will **not lose its value**.
  - You cannot re-declare a variable declared with `let` or `const`.

```html
<p id="demo"></p>

<script>
  var carName = "Volvo";
  var carName;
  document.getElementById("demo").innerHTML = carName; //show Volvo
</script>
```

---

## Identifiers

- All JavaScript variables must be **identified** with **unique** names.

- These unique <u>names</u> are called **identifiers**.

- The general rules for constructing names for variables (unique identifiers) are:

  - Names can contain letters, digits, underscores, and dollar signs.
  - Names must **begin with** a letter.
  - Names can also **begin with** `$` and `_` (but we will not use it in this tutorial).
  - Names are **case sensitive** (y and Y are different variables).
  - **Reserved words** (like JavaScript keywords) cannot be used as names.

- **Dollar Sign `$`**: Since JavaScript treats a dollar sign as a letter, identifiers containing `$` are valid variable names.
- - Using the dollar sign is not very common in JavaScript, but professional programmers often use it as an alias for the **main function in a JavaScript library**.

  - In the JavaScript library jQuery, for instance, the main function `$` is used to select HTML elements. In jQuery `$("p");` means "select all p elements".

```js
let $ = "Hello World";
let $$$ = 2;
let $myMoney = 5;
```

- **Underscore (\_)**: Since JavaScript treats underscore as a letter, identifiers containing `_` are valid variable names.
  - Using the underscore is not very common in JavaScript, but a convention among professional programmers is to use it as **an alias for "private (hidden)" variables&**.

---

## `let`

- Variables defined with let **cannot be Redeclared**.

- Variables defined with let must be **Declared before use**.

- Variables defined with let **have Block Scope**.
  - Variables declared inside a `{` `}` block **cannot be accessed from outside** the block

```js
let x = "John Doe";

let x = 0; // SyntaxError: 'x' has already been declared

var x = "John Doe";

var x = 0; // Redeclared
```

- Variables declared with the `var` keyword can NOT have block scope.
  - Variables declared inside a { } block can be accessed from outside the block.

```js
{
  let x = 2;
}
// x can NOT be used here

{
  var x = 2;
}
// x CAN be used here
```

---

### Redeclaring Variables

- Redeclaring a JavaScript variable with `var` is **allowed** anywhere in a program.

- With `let`, redeclaring a variable in the same block is **NOT allowed**.
- Redeclaring a variable with let, in another block, **IS allowed**.

```js
var x = 10;
// Here x is 10

{
  var x = 2; //redeclare using var
  // Here x is 2
}

// Here x is 2. The value will be changed in the block

// ----------------------------
let x = 10;
// Here x is 10

{
  let x = 2; //redeclare using let
  // Here x is 2
}

// Here x is 10. The value outside the block will not be affected by the block.
```

---

### Hoisting

- Variables defined with `var` are hoisted to the top and **can be initialized at any time**.

- Variables defined with `let` are also hoisted to the top of the block, but **not initialized**.
  - Meaning: Using a let variable before it is declared will result in a `ReferenceError`.

```html
<p id="demo"></p>

<script>
  try {
    carName = "Saab";
    let carName = "Volvo";
  } catch (err) {
    document.getElementById("demo").innerHTML = err; //ReferenceError: Cannot access 'carName' before initialization
  }
</script>
```

---

## `const`

- Variables defined with const **cannot be Redeclared**.

- Variables defined with const **cannot be Reassigned**.

- Variables defined with const **have Block Scope**.

- `const` variables **must be assigned** a value when they are declared

- It does **not define a constant value**. It defines a **constant reference** to a value.即不一定是值不能变,而是指向的对象不能变,而对象的值可以变.

  - Because of this you can NOT:

    - Reassign a constant value
    - Reassign a constant array
    - Reassign a constant object

  - But you CAN:
    - Change the elements of constant array
    - Change the properties of constant object

- **Constant Arrays**:

```html
<p id="demo"></p>

<script>
  // Create an Array:
  const cars = ["Saab", "Volvo", "BMW"];

  // Change an element:
  cars[0] = "Toyota";

  // Add an element:
  cars.push("Audi");

  // Display the Array:
  document.getElementById("demo").innerHTML = cars;

  // cars = ["Toyota", "Volvo", "Audi"];    // ERROR: redeclare
</script>
```

- **Constant Objects**

```html
<p id="demo"></p>

<script>
  // Create an object:
  const car = { type: "Fiat", model: "500", color: "white" };

  // Change a property:
  car.color = "red";

  // Add a property:
  car.owner = "Johnson";

  // Display the property:
  document.getElementById("demo").innerHTML = "Car owner is " + car.owner;

  // car = {type:"Volvo", model:"EX60", color:"red"};    // ERROR: redeclare
</script>
```

---

### Redeclaring

- Redeclaring an existing `var` or `let` variable to `const`, in the same scope, is **not allowed**.
- Reassigning an existing `const` variable, in the same scope, is **not allowed**.

```js
var x = 2; // Allowed
const x = 2; // Not allowed

{
  let x = 2; // Allowed
  const x = 2; // Not allowed
}

{
  const x = 2; // Allowed
  const x = 2; // Not allowed
}
```

---

### Block Scope

```js
const x = 10;
// Here x is 10

{
  const x = 2;
  // Here x is 2
}

// Here x is 10
```

---

### Hoisting

- Variables defined with const are also hoisted to the top, but **not initialized**.
  - Meaning: Using a const variable before it is declared will result in a `ReferenceError`.

```html
<p id="demo"></p>

<script>
  try {
    alert(carName);
    const carName = "Volvo";
  } catch (err) {
    document.getElementById("demo").innerHTML = err; //ReferenceError: Cannot access 'carName' before initialization
  }
</script>
```

---

[TOP](#javascript-variable)
