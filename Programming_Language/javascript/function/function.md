# JavaScript - Function

[Back](../index.md)

- [JavaScript - Function](#javascript---function)
  - [Function](#function)
  - [Arrow Function](#arrow-function)

---

## Function

- A JavaScript function is a block of code designed **to perform a particular task**.

- Syntax:

```js
function name(parameter1, parameter2, parameter3) {
  // code to be executed
}
```

- **Function names**:

  - contain letters, digits, underscores, and dollar signs (same rules as variables).

- **Parameters/Arguments**:

  - Function **parameters** are listed inside the parentheses `()` in the function definition. 形参
  - Function **arguments** are the <u>values received by the function</u> when it is invoked.实参

- **Function Scope**

  - Inside the function, the arguments (the parameters) behave as **local variables**.
  - Local variables can only be accessed from **within the function**.
  - Local variables are **created** when a function **starts**, and **deleted** when the function is **completed**.
  - Since local variables are only recognized inside their functions, variables with the **same name** can be used in different functions.

- **Return**:

  - When JavaScript reaches a return statement, the function will **stop executing**.

- **reuse code**:

  - Define the code once, and use it many times.
  - use the same code many times with different arguments, to produce different results.

- **Return function object**:
  - Accessing a function without `()` will **return the function object** instead of the function result.

```js
function toCelsius(fahrenheit) {
  return (5 / 9) * (fahrenheit - 32);
}

console.log(toCelsius); //[Function: toCelsius]
console.log(toCelsius(77)); //25
console.log(toCelsius()); //NaN
```

---

## Arrow Function

- Syntax:

```js
// the function has only one statement
const fun1 = () => returnValue; // not para
const fun2 = (para, para) => computeResult; // arguements

//
const fun3 = (para, para) => {
  // function code
  return computeResult;
};
```

- `this`:
  - With arrow functions the `this` keyword always represents the **object that defined the arrow function**.

---

[TOP](#javascript---function)
