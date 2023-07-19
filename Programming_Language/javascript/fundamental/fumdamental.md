# Javascript - Fundamental

[Back](../index.md)

- [Javascript - Fundamental](#javascript---fundamental)
  - [Statement](#statement)
  - [Comment](#comment)
  - [Syntax](#syntax)
    - [Values](#values)
    - [Identifiers / Names](#identifiers--names)
    - [Keywords](#keywords)
    - [Operators](#operators)
    - [Expressions](#expressions)
  - [Scope](#scope)
    - [Block Scope](#block-scope)
    - [Function scope](#function-scope)
    - [Global Scope](#global-scope)
    - [The Lifetime of JavaScript Variables](#the-lifetime-of-javascript-variables)
  - [Hoisting](#hoisting)
  - [Strict Mode: `use strict`](#strict-mode-use-strict)
  - [Debugging](#debugging)

---

## Statement

- A **computer program** is a list of "instructions" to be "executed" by a computer.
  In a programming language, these programming instructions are called **statements**.

- A **JavaScript program** is a list of programming **statements**.

  - The statements are executed, one by one, in the same order as they are written.
  - **JavaScript programs** (and **JavaScript statements**) are often called `JavaScript code`.

- **JavaScript statements** are composed of:

  - Values,
  - Operators,
  - Expressions,
  - Keywords,
  - and Comments.

- **Semicolons `;`**

  - Semicolons **separate** JavaScript statements.
  - Add a semicolon at the end of each executable statement.
  - Ending statements with semicolon is **not required**, but **highly recommended**.
  - When separated by semicolons, multiple statements **on one line** are allowed

  ```js
  a = 5;
  b = 6;
  c = a + b;
  ```

- **White Space**

  - JavaScript **ignores multiple spaces**. You can add white space to your script to make it more readable.
  - A **good practice** is to put spaces around operators ( = + - \* / ).

- **Line Length and Line Breaks**

  - For best readability, programmers often like to avoid code lines longer than 80 characters.
  - If a JavaScript statement does not fit on one line, the best place to break it is after an operator.

- **Code Blocks**

  - JavaScript statements can be **grouped together in code blocks**, inside **curly brackets** `{`...`}`.

  - The purpose of code blocks is to define statements **to be executed together**.

---

## Comment

- the JavaScript statements that are ignored and not "executed".
  - Single Line Comments: `//`
  - Multi-line Comments: `/*  */`

---

## Syntax

- `JavaScript syntax`

  - the set of rules, how JavaScript programs are constructed:

- **Case Sensitive**

  - All JavaScript identifiers are **case sensitive**.

- **Character Set**

  - JavaScript uses the **Unicode** character set.
  - Unicode covers (almost) all the characters, punctuations, and symbols in the world.

---

### Values

- The JavaScript syntax defines two types of values:

  - `Literal`: Fixed value
  - `Variable`: Variable values

- **Literal**

  - Syntax rules for fixed values:

    1. Numbers are written with or without decimals.
    2. Strings are text, written **within double or single quotes**.

- **Variables**

  - In a programming language, variables are used to **store data values**.
  - JavaScript uses the keywords `var`, `let` and const to declare variables.
  - An **equal sign** is used to **assign values to variables**.

---

### Identifiers / Names

- `Identifiers` are JavaScript names.

- `Identifiers` are used to name `variables` and `keywords`, and `functions`.

- A JavaScript name must **begin with**:

  - A letter (A-Z or a-z)
  - A dollar sign (`$`)
  - Or an underscore (`_`)
  - Subsequent characters may be letters, digits, underscores, or dollar signs.
  - Numbers are **not allowed** as the first character in names.
  - Hyphens are not allowed in JavaScript. They are reserved for subtractions.

- **Camel Case**

  ```js
  // Underscore
  first_name, last_name, master_card, inter_city;

  // Upper Camel Case (Pascal Case)
  FirstName, LastName, MasterCard, InterCity;

  // Lower Camel Case
  firstName, lastName, masterCard, interCity;
  ```

---

### Keywords

- JavaScript keywords are **reserved words**.
- **Reserved words cannot be used as names for variables**.

---

### Operators

- JavaScript uses **arithmetic operators** ( + - \* / ) to compute values.

- JavaScript uses an **assignment operator** ( = ) to assign values to variables:

---

### Expressions

- `expression`
  - a combination of values, variables, and operators, which computes to a value.
  - The **computation** is called an `evaluation`.
  - The values can be of **various types**, such as numbers and strings.

---

## Scope

- `Scope`:

  - determines the **accessibility (visibility)** of variables.

- JavaScript has 3 types of scope:
  - `Block` scope
  - `Function` scope
  - `Global` scope

---

### Block Scope

- `var` keyword can **NOT have block scope**.

  - Variables declared inside a `{ }` block **can** be accessed from outside the block.

  ```js
  {
    var x = 10;
  }
  console.log(x); //10
  ```

- `let` and `const` provide Block Scope in JavaScript.

  - Variables **declared inside** a `{ }` block **cannot be accessed from outside** the block.

  ```js
  {
    let x = 10;
    const y = 9;
  }
  console.log(x); // ReferenceError: x is not defined
  console.log(y); // ReferenceError: y is not defined
  ```

---

### Function scope

Function Arguments

- `Local variables`

  - Variables declared within a JavaScript function, become **LOCAL** to the function.

- `Local variables` have `Function Scope`.

  - only be accessed from **within** the function.
  - not accessible (visible) from **outside** the function.
  - Each function creates a **new** scope.
    - `Local variables` are **created** when a function **starts**, and **deleted** when the function is **completed**.
  - `var`, `let` and `const` are quite similar when declared inside a function.
  - `Function arguments (parameters)` work as `local variables` inside functions.

- Since local variables are only recognized inside their functions, variables with the **same name** can be used in different functions.

```js
function myFunction() {
  var carName = "Volvo"; // Function Scope
}
function myFunction() {
  let carName = "Volvo"; // Function Scope
}
function myFunction() {
  const carName = "Volvo"; // Function Scope
}
```

---

### Global Scope

- `Global Variables`

  - A variable declared outside a function, becomes **GLOBAL**.
  - can be accessed from **anywhere** in a JavaScript program.

- Variables declared **Globally** (outside any function) have `Global Scope`.

  - All scripts and functions on a web page can access it.
  - Variables declared with `var`, `let` and `const` are quite similar when declared outside a block.They all have `Global Scope`.

- **Automatically Global**

  - If you assign a value to a variable that **has not been declared**, it will automatically become a GLOBAL variable.
  - In "Strict Mode", undeclared variables are **not** automatically global.

  ```js
  myFunction();

  // code here can use carName

  function myFunction() {
    carName = "Volvo";
    //This code example will declare a global variable carName, even if the value is assigned inside a function.
  }
  ```

- **Global Variables in HTML**

  - With JavaScript, the `global scope` is the **JavaScript environment**.
  - In HTML, the `global scope` is the **window object**.
  - Global variables defined with the `var` keyword belong to the **window object**.
  - Global variables defined with the `let` keyword do **not** belong to the window object
  - **Do NOT** create `global variables` unless you intend to.
    - global variables (or functions) can overwrite window variables (or functions).
    - Any function, including the window object, can overwrite global variables and functions.

---

### The Lifetime of JavaScript Variables

- The lifetime of a JavaScript variable **starts** when it is **declared**.
- Function (local) variables are **deleted** when the function is **completed**.
- In a web browser, global variables are **deleted** when you **close** the browser window (or tab).

---

## Hoisting

- `Hoisting`

  - JavaScript's default behavior of **moving all declarations to the top** of the current scope (to the top of the current script or the current function).

- In JavaScript, a variable can be **declared after** it has been used.
- In other words; a variable can be **used before** it has been declared.
- JavaScript in `strict mode` does **not allow**variables to be used if they are not declared.

- `var` variable can be used before declared

  ```js
  x = 5; // Assign 5 to x
  console.log(x); //5

  var x; // Declare x
  ```

- Using a `let` variable before declared will result in a `ReferenceError`.

  ```js
  x = 5; //ReferenceError: Cannot access 'x' before initialization
  let x; // Declare x
  ```

- Using a `const` variable before declared will result in a `ReferenceError`.

  ```js
  x = 5;  //SyntaxError: Missing initializer in const declaration
  const x; // Declare x
  ```

---

## Strict Mode: `use strict`

- `use strict`

  - Defines that JavaScript code should be executed in "strict mode".

- **Declaring Strict Mode**

- adding "use strict"; to the **beginning** of a script or a function
-
- Declared at the beginning of a script

  - it has global scope (all code in the script will execute in strict mode).

```js
"use strict";
// x = 3.14; // ReferenceError: x is not defined

myFunction();

function myFunction() {
  y = 3.14; // ReferenceError: y is not defined
}
```

- Declared inside a function
  - it has local scope (only the code inside the function is in strict mode):

```js
x = 3.14; // This will not cause an error.
myFunction();

function myFunction() {
  "use strict";
  y = 3.14; // ReferenceError: y is not defined
}
```

- **Not allowed**
  - Using a variable/object, **without declaring**
  - **Deleting** a variable (or object)
  - **Deleting** a function
  - Duplicating a **parameter name**
  - Octal numeric literals
  - Octal escape characters
  - Writing to a read-only property
  - Writing to a get-only property
  - Deleting an undeletable property
  - `eval`, `arguments`,`with` cannot be used as a variable
  - `eval()` is not allowed to create variables in the scope from which it was called.
  - `this`
    - The `this` keyword refers to the object that called the function.
    - If the object is not specified, functions in strict mode will return `undefined`.

---

## Debugging

- `code debugging`

  - Searching for (and fixing) errors in programming code

- `debugger` Keyword
  - stops the execution of JavaScript, and calls (if available) the debugging function.

```html
<script>
  let x = 15 * 5;
  debugger; // stop execution
  console.log(x);
</script>
```

---

[TOP](#javascript---fundamental)
