# Javascript - `this`

[Back](../index.md)

- [Javascript - `this`](#javascript---this)
  - [`this`](#this)
  - [Explicit Function Binding](#explicit-function-binding)

---

## `this`

- The `this` keyword refers to different objects depending on how it is used:

  | Location              | Refer to                        |
  | --------------------- | ------------------------------- |
  | Alone                 | global object                   |
  | function              | global object                   |
  | function(strict mode) | undefined                       |
  | event handlers        | element that received the event |
  | object method         | object                          |

- **Alone**: `global object`

  - Because this is running in the global scope.
  - In a browser window the global object is `[object Window]`.

- In a function definition, this refers to the **"owner"** of the function.

  - **Default**: `global object`

    - In a browser window the global object is `[object Window]`

  - **Strict**: `undefined`

    - does not allow default binding

  - **Object Method**: `object`

---

## Explicit Function Binding

- The `call()` and `apply()` methods are predefined JavaScript methods.

  - They can both be used to call an object method with another object as argument.

```js
//call()
const person1 = {
  fullName: function () {
    return this.firstName + " " + this.lastName;
  },
};

const person2 = {
  firstName: "John",
  lastName: "Doe",
};

let x = person1.fullName.call(person2);

console.log(x); //John Doe
//解析: person1的fullname定义了匿名函数
//调用时, 使用call()将person2传递给this

//bind(): this keyword set to the provided value
const person = {
  firstName: "John",
  lastName: "Doe",
  fullName: function () {
    return this.firstName + " " + this.lastName;
  },
};

const member = {
  firstName: "Hege",
  lastName: "Nilsen",
};

let fullName = person.fullName.bind(member);
//解析: fullName是匿名函数,不是object的方法,所以this不是指代object
//使用bind()将this指代为参数, 即member
//bind()的用处, 当object是异步时, 直接使用this指代object本身会发生返回undefined的情况. 此时使用object.property.bind(object), 因为object是参数,所以会等待到object完全加载时, 才传入到this, 以此解决异步返回undefined的情况.
```

---

[TOP](#javascript---this)
