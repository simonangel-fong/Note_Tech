# JavaScript Functions

[Back](../index.md)

- [JavaScript Functions](#javascript-functions)
  - [Function](#function)

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

- Function **parameters** are listed inside the parentheses `()` in the function definition. 形参

- Function **arguments** are the <u>values received by the function</u> when it is invoked.实参

- Inside the function, the arguments (the parameters) behave as **local variables**.

  - Local variables can only be accessed from **within the function**.

- **Return**:

  - When JavaScript reaches a return statement, the function will **stop executing**.
  - Since local variables are only recognized inside their functions, variables with the **same name** can be used in different functions.
  - Local variables are **created** when a function **starts**, and **deleted** when the function is **completed**.

- **reuse code**:
  - Define the code once, and use it many times.
  - use the same code many times with different arguments, to produce different results.
- **Return function object**:
  - Accessing a function without `()` will **return the function object** instead of the function result.

```js
function toCelsius(fahrenheit) {
  return (5 / 9) * (fahrenheit - 32);
}

document.getElementById("demo").innerHTML = toCelsius(77); //return calculated result;
document.getElementById("demo").innerHTML = toCelsius(); //return: function toCelsius(f) { return (5/9) * (f-32); }
```

---

[TOP](#javascript-functions)
