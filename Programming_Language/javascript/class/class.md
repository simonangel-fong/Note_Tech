# JavaScript - Class

[Back](../index.md)

- [JavaScript - Class](#javascript---class)
  - [Class](#class)
  - [Object Methods](#object-methods)
  - [Getters and Setters](#getters-and-setters)
  - [Static class methods](#static-class-methods)
  - [Class Inheritance](#class-inheritance)

---

## Class

- JavaScript Classes are **templates** for JavaScript Objects.

- **Define a class**

  - Use the keyword `class` to create a class.
  - Always add a method named `constructor()`

- **Using a Class**

  - When you have a class, you can use the class to create objects

- **Hoisting**
  - Unlike functions, and other JavaScript declarations, class declarations are not hoisted.
  - That means that you **must declare a class before** you can use it.

| Keyword   | Description                         |
| --------- | ----------------------------------- |
| `extends` | Extends a class (inherit)           |
| `static`  | Defines a static method for a class |
| `super`   | Refers to the parent class          |

---

## Object Methods

- `constructor`

  - used to initialize object properties
  - executed automatically when a new object is created
  - If do not define a constructor method, JavaScript will add an empty constructor method.

- **Class methods** are created with the same syntax as object methods.

- **Example**

```js
console.log("\n-------- Class --------\n");

class Car {
  constructor(name, year) {
    this.name = name;
    this.year = year;
  }
  age() {
    const date = new Date();
    return date.getFullYear() - this.year;
  }
}

const myCar = new Car("Ford", 2014);

for (let p in myCar) {
  console.log(p, myCar[p]);
}
// name Ford
// year 2014

console.log("age", myCar.age()); //age 9
```

---

## Getters and Setters

- Use the `get` and `set` keywords, to add **getters** and **setters** in the class,

- getter

  - even if the getter is a method, you **do not use parentheses** when you want to get the property value.

- setter
  - To use a setter, use the same syntax as when you set a property value, **without parentheses**

```js
console.log("\n-------- Class: getter and setter --------\n");

class Car {
  constructor(brand) {
    this.carname = brand;
  }
  get cnam() {
    return this.carname;
  }
  set cnam(x) {
    this.carname = x;
  }
}

const myCar = new Car("Ford");

console.log(myCar.carname); //Ford

console.log(myCar.cnam);

myCar.cnam = "BMW"; //Ford
console.log(myCar.cnam); //BMW
```

---

## Static class methods

- Static class methods are defined on the **class itself**.
- You cannot call a `static` method on an object, only on an object class.
- If you want to use the myCar object inside the static method, you can **send it as a parameter**.

```js
console.log("\n-------- Class: static method --------\n");

class Car {
  constructor(brand) {
    this.carname = brand;
  }
  static hello() {
    return "Hello";
  }
}

const myCar = new Car("Ford");

// console.log(myCar.hello()); //raise an error.
console.log(Car.hello()); //Hello
console.log(Car.hello(myCar)); //Hello
```

---

## Class Inheritance

- Inheritance is useful for **code reusability**: reuse properties and methods of an existing class when you create a new class.

- To create a class inheritance, use the `extends` keyword.

- A class created with a class inheritance inherits all the methods from another class.

- `super`

  - refers to the parent class.
  - gets access to the parent's properties and methods.

- `super()`
  - call the parent's `constructor` method

```js
console.log("\n-------- Class: inheritance --------\n");

class Car {
  constructor(brand) {
    this.carname = brand;
  }
  present() {
    return "I have a " + this.carname;
  }
}

class Model extends Car {
  constructor(brand, mod) {
    super(brand);
    this.model = mod;
  }
  show() {
    return this.present() + ", it is a " + this.model;
  }
}

let myCar = new Model("Ford", "Mustang");

console.log(myCar.present());
console.log(myCar.show());
```

---

[TOP](#javascript---class)
