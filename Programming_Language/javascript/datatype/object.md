# JavaScript Object

[Back](../index.md)

- [JavaScript Object](#javascript-object)
  - [Object Definition](#object-definition)
  - [Properties](#properties)
  - [Methods](#methods)

---

## Object Definition

- The values are written as **name:value pairs** (name and value separated by a colon).

- It is a common practice to declare objects with the `const` keyword.

```js
const person = {
  firstName: "John",
  lastName: "Doe",
  age: 50,
  eyeColor: "blue",
};
```

---

## Properties

- The **name:values pairs** in JavaScript objects are called `properties`.
- access object properties:
  - `objectName.propertyName`
  - `objectName["propertyName"]`

---

## Methods

- `Methods` are **actions** that can be performed on objects.

- A `method` is a `function` stored as a **property**.

```js
const person = {
  firstName: "John",
  lastName: "Doe",
  id: 5566,
  fullName: function () {
    return this.firstName + " " + this.lastName; //this refers to the person object.
  },
};
```

- **Access an object method**:
  - `objectName.methodName()`
  - If you access a method without the () parentheses, it will return the **function definition**.

---

[TOP](#javascript-object)
