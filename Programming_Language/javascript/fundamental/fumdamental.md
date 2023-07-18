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

[TOP](#javascript---fundamental)
