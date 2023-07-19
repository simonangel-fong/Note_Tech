# JavaScript Object

[Back](../index.md)

- [JavaScript Object](#javascript-object)
  - [Object Definition](#object-definition)
    - [Create an Object](#create-an-object)
  - [Properties](#properties)
    - [Accessing properties](#accessing-properties)
    - [Loops through properties](#loops-through-properties)
    - [Adding New Properties](#adding-new-properties)
    - [Deleting Properties](#deleting-properties)
  - [Nested Objects](#nested-objects)
  - [Methods](#methods)
    - [Access an object method](#access-an-object-method)
    - [Adding a Method to an Object](#adding-a-method-to-an-object)
  - [Object Constructor](#object-constructor)
  - [JavaScript Objects are Mutable](#javascript-objects-are-mutable)
  - [Prototype Inheritance](#prototype-inheritance)
    - [`prototype` Property](#prototype-property)
  - [Trick](#trick)

---

## Object Definition

- `Object`

  - a collection of **named values**

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

### Create an Object

- There are different ways to create new objects:

  - Create a single object, using an **object literal**.
  - Create a single object, with the keyword `new`.
  - Define an object **constructor**, and then create objects of the constructed type.
  - Create an object using `Object.create()`.

```js
console.log("\n-------- Object: create --------\n");

// Using an Object Literal
const person1 = {
  firstName: "John",
  lastName: "Doe",
  age: 50,
  eyeColor: "blue",
};
console.log(person1);

// creates an empty JavaScript object, and then adds 4 properties
const person2 = {};
person2.firstName = "John";
person2.lastName = "Doe";
person2.age = 50;
person2.eyeColor = "blue";
console.log(person2);

// Using the JavaScript Keyword new
const person3 = new Object();
person3.firstName = "John";
person3.lastName = "Doe";
person3.age = 50;
person3.eyeColor = "blue";
console.log(person3);
```

---

## Properties

- The **name:values pairs** in JavaScript objects are called `properties`.
- access object properties:
  - `objectName.propertyName`
  - `objectName["propertyName"]`

---

### Accessing properties

```js
objectName.property;
objectName["property"];
objectName[expression]; // The expression must evaluate to a property name.
```

---

### Loops through properties

- Using `for...in` statement

```js
for (let variable in object) {
  // code to be executed
}
```

- Using `Object.values()` to return all properties' values

```js
const person = {
  name: "John",
  age: 30,
  city: "New York",
  hello: () => "hello",
};

console.log(Object.values(person)); //[ 'John', 30, 'New York', [Function: hello] ]
```

- Using `JSON.stringify()` to convert properties and values to a string, except method.

```js
const person = {
  name: "John",
  age: 30,
  city: "New York",
  hello: () => "hello",
};

console.log(JSON.stringify(person)); //{"name":"John","age":30,"city":"New York"}
```

---

### Adding New Properties

```js
objectName.newProperty = value;
```

---

### Deleting Properties

- Using `delete` operator.

```js
delete objectName.property;
delete person["property"];
```

---

## Nested Objects

```js
myObj = {
  name: "John",
  age: 30,
  cars: {
    car1: "Ford",
    car2: "BMW",
    car3: "Fiat",
  },
};

console.log(myObj.cars.car2); //BMW
console.log(myObj.cars["car2"]); //BMW
console.log(myObj["cars"]["car2"]); //BMW
```

---

## Methods

- `Methods` are **actions** that can be performed on objects.
- A `method` is a `function` stored as a **property**.
- Methods are functions stored as object properties.

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

---

### Access an object method

```js
objectName.methodName();
```

- If you access a method without the () parentheses, it will return the **function definition**.

---

### Adding a Method to an Object

```js
objectName.methodName = function {
  // method body
};
```

---

## Object Constructor

- Syntax

```js
// define
function objectName(para, para, ...){
  this.propertyName = para;
  this.propertyName = para;
  ...
}

// call
const obj = new objectName(arg, arg, ...);
```

- Built-in JavaScript Constructors
  JavaScript has built-in constructors for native objects:

  - `new String()`: A new String object
  - `new Number()`: A new Number object
  - `new Boolean()`: A new Boolean object
  - `new Object()`: A new Object object
  - `new Array()`: A new Array object
  - `new RegExp()`: A new RegExp object
  - `new Function()`: new Function object
  - `new Date()`: A new Date object

- Example:

```js
console.log("\n-------- Object: constructor --------\n");

function Person(first, last, age, eye) {
  this.firstName = first;
  this.lastName = last;
  this.age = age;
  this.eyeColor = eye;
}

const myFather = new Person("John", "Doe", 50, "blue");
const myMother = new Person("Sally", "Rally", 48, "green");

console.log(myFather);
// Person {
//   firstName: 'John',
//   lastName: 'Doe',
//   age: 50,
//   eyeColor: 'blue'
// }
console.log(myMother);
// Person {
//   firstName: 'Sally',
//   lastName: 'Rally',
//   age: 48,
//   eyeColor: 'green'
// }
```

---

## JavaScript Objects are Mutable

- Objects are mutable: They are **addressed by reference**, not by value.

- If person is an object, the following statement will not create a copy of person:

```js
const person = {
  firstName: "John",
  lastName: "Doe",
  age: 50,
  eyeColor: "blue",
};

const x = person;
x.age = 10; // Will change both x.age and person.age

console.log(person); //{ firstName: 'John', lastName: 'Doe', age: 10, eyeColor: 'blue' }
```

- The object `x` is not a copy of person. It is person. Both `x` and person are the same object.

- Any changes to `x` will also change person, because `x` and person are the same object.

---

## Prototype Inheritance

- All JavaScript objects **inherit properties and methods from a prototype**:

  - `Date` objects inherit from `Date.prototype`
  - `Array` objects inherit from `Array.prototype`
  - `Person` objects inherit from `Person.prototype`

- The `Object.prototype` is on the top of the prototype inheritance chain:

- `Date` objects, `Array` objects, and `Person` objects inherit from `Object.prototype`.

---

### `prototype` Property

- allows to add new properties and methods to object constructors
- Only modify your own prototypes. Never modify the prototypes of standard JavaScript objects.

```js
console.log("\n-------- Object: constructor --------\n");

function Person(fname, lname) {
  this.firstName = fname;
  this.lastName = lname;
}

const p1 = new Person("John", "Doe");
console.log(p1.age); //undefined
// console.log(p1.fullname()); //TypeError: p1.fullname is not a function

Person.prototype.age = 18;
Person.prototype.name = function () {
  return this.firstName + " " + this.lastName;
};

const p2 = new Person("Join", "Wick");
console.log(p1.age); //18
console.log(p1.name()); //John Doe
```

- 注意, 以上 name 方法的定义不能使用 arrow function, 因为此时 this 指代的是 global, 返回的是 undefined.

---

## Trick

- Check if the object
  - check if it is `undefined`
  - then check if it is `null`

```js
if (typeof myObj !== "undefined" && myObj !== null) {
  // operate object
}
```

---

[TOP](#javascript-object)
