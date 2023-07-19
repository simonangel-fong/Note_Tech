# JavaScript - Variable

[Back](../index.md)

- [JavaScript - Variable](#javascript---variable)
  - [Variable](#variable)
  - [Declaration](#declaration)
  - [Identifiers](#identifiers)
  - [`let`](#let)
    - [Redeclaring Variables](#redeclaring-variables)
    - [Hoisting](#hoisting)
  - [`const`](#const)
    - [Redeclaring](#redeclaring)
    - [Block Scope](#block-scope)
    - [Hoisting](#hoisting-1)
  - [Destructuring assignment](#destructuring-assignment)
    - [Unpack Array](#unpack-array)
    - [Unpack Object](#unpack-object)

---

## Variable

- `Variable`:

  - the container to store Data
    JavaScript Variables can be declared in 4 ways:

- Difference Between `var`, `let` and `const`

  | Keyword | Scope | Redeclare | Reassign | Hoisted | Binds this |
  | ------- | ----- | --------- | -------- | ------- | ---------- |
  | `var`   | No    | Yes       | Yes      | Yes     | Yes        |
  | `let`   | Yes   | No        | Yes      | No      | No         |
  | `const` | Yes   | No        | No       | No      | No         |

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

- It's a good programming practice to declare all variables **at the beginning of a script**.

- Keyword:

  - `const`: if the **value** should not be changed
  - `const`: if the **type** should not be changed (Arrays and Objects)
  - `let`: Only if const cannot be used.
  - `var`: Only if **MUST support old browsers**.

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

- **Use const when you declare**:

  - A new `Array`
  - A new `Object`
  - A new `Function`
  - A new `RegExp`

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

## Destructuring assignment

- `Destructuring assignment`
  - a JavaScript expression that unpacks values from arrays, or properties from objects, into distinct variables.

### Unpack Array

```js
// destructuring array
const arr = [1, 2, 3, 4];
const [a1, b1] = arr;
// console.log(a1); //1
// console.log(b1); //2

const [a2, b2, c2, d2, e2] = arr;
console.log(a2); //1
console.log(b2); //2
console.log(c2); //3
console.log(d2); //4
console.log(e2); //undefined

const [a3, b3, ...c3] = arr;
console.log(a3); //1
console.log(b3); //2
console.log(c3); //[ 3, 4 ]
```

### Unpack Object

```js
const obj01 = { b1: 2, a1: 1, c1: 3, d1: 4 };
const { a1, b1 } = obj01; //相当于 a=obj.a
// console.log(a1); //1
// console.log(b1); //2

const obj02 = { b3: 2, a2: 1, c2: 3, d2: 4 };
const { a2, b2, c2, d2, e2 } = obj02;
console.log(a2); //1
console.log(b2); //2
console.log(c2); //3
console.log(d2); //4
console.log(e2); //undefined, 因为 obj 没有 e2 的属性

const obj03 = { b3: 2, a3: 1, c3: 3, d3: 4 };
const { a3, b3, ...c3 } = obj03;
console.log(a3); //1
console.log(b3); //2
console.log(c3); //{ c3: 3, d3: 4 }

const obj04 = { b4: 2, a4: 1, c4: 3, d4: 4 };
const { a4: x, b4: y } = obj04; //相当于 x=obj04.a4
console.log(x); //1
console.log(y); //2
```

---

[TOP](#javascript---variable)
