# JavaScript - Function

[Back](../index.md)

- [JavaScript - Function](#javascript---function)
  - [Function](#function)
    - [Argument and Function Scope](#argument-and-function-scope)
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

### Argument and Function Scope

- 函数体中变量引用的是 local 还是 global?

  - 先在引用包括实参内的 local 变量;
  - 如果不存在相同变量名的 local 变量, 则在全局 global 变量中寻找.

- 如果函数定义了实参但引用时没有赋值时, 实参是 `undefined`.
- 但变量引用的 global 时, 对变量的改变影响的是 global, 即函数结束后该 global 变量值被改变.

- 实参 argument 是值引用, 即复制一个实参副本
  - 如果实参是 literal value, 直接复制值.
    - 由于 literal value 是不可变的, 所以不存在改变 literal value.
    - 实参值的改变, 只在函数体内有效, 不影响被传递的变量.
  - 如果实参是 reference, 也是复制值. 只不过复制的是地址值.
    - 由于 reference 是可变, 所以对 reference 的改变可能会影响到函数之外.
    - 实参值的改变(是指实参引用的地址值改变), 只在函数体内有效, 不影响原来 reference 的对象.

```js
console.log(
  "\n-------- function scope/argument: literal value argument --------\n"
);
var x = "5";
var y = "5";

function test(x) {
  x = 10; //先在local寻找, 找到参数
  y = 10; //local没有y, 所以引用global, 即改变y的值, 也影响到函数体外.
}

test(); //该处相对于声明了local变量x, 但没有赋值; 但在函数中赋值为5.
console.log(x, y); //5 10, global x 没有引用; y被引用并改变,所以是10

test(x); //该处将global x的值复制到local x.
console.log(x, y); // 5 10, 方法体中对local x的改变只作用于方法体中, 不影响global x.

console.log(
  "\n-------- function scope/argument: reference type argument --------\n"
);

var obj = {};
function testObj(obj) {
  console.log(obj);
  if (typeof obj === "object") {
    obj["name"] = "a";
  }
}

testObj(); //该处形参obj被声明, 但没有赋值, 所以是undefined
console.log(obj); // {}, 形参obj是local变量, 只在方法体中有效,不影响global obj

testObj(obj); // 因为obj是对象, 是reference type; 该处将global obj的地址复制到形参obj
console.log(obj); // { name: 'a' }, 由于方法体引用global obj 的地址并进行修改, 其效果影响global obj

var obj = {};
function testObjLocal(obj) {
  obj = { a: 9 };
}
testObjLocal(obj);
console.log(obj); //{}, 该处形参obj引用global obj, 但方法体实际上将形参的obj引用为新的对象, 不再是global obj. 而且形参的作用域在方法体内. 所以global obj没有影响.
```

---

## Arrow Function

- Syntax:

```js
// arrow function with body and return
const funName = (paraList) => {
  // function body
  return returnVal;
};

// arrow function that only returns value
const funName = () => returnVal; //without parameters
const funName = (paraList) => returnVal; //with parameters

// call arrow function
funName();


// High-Order Function: Function that excepts other functions as arguments
const funName = (paraFun) = {
  paraFun();
  return returnVale;
}

const argFun = (para)={
  // function body
  return returnVal;
}

// call high-order function with named function
funName(argFun);

// call high-order function with anonymous function
funName(()=>{
  // anonymous function body
})

```

- `this`:
  - With arrow functions the `this` keyword always represents the **object that defined the arrow function**.

```js
const obj = {
  name: "John",
  call: () => {
    console.log(this); //{}
    return this.name;
  },
  yell: function () {
    console.log(this); //{ name: 'John', call: [Function: call], yell: [Function: yell] }
    return this.name;
  },
};

console.log(obj.call()); //undefined
console.log(obj.yell()); //John
```

---

[TOP](#javascript---function)
