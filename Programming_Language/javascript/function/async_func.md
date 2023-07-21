# JavaScript - Asynchronous Function

[Back](../index.md)

- [JavaScript - Asynchronous Function](#javascript---asynchronous-function)
  - [Asynchronous](#asynchronous)
  - [Callbacks Function](#callbacks-function)
    - [`setTimeout()`: 典型回调函数](#settimeout-典型回调函数)
  - [Promise](#promise)
    - [Chaining](#chaining)
    - [Parallel Promises: `all()`](#parallel-promises-all)
    - [Mixed Promises](#mixed-promises)
  - [`async`/`await`](#asyncawait)

---

## Asynchronous

- **Function Sequence**

  - JavaScript functions are executed in the sequence **they are called**.

- `asynchronous operation`:

  - allows the computer to “move on” to other tasks while waiting for the asynchronous operation to complete.

- `Asynchronous programming`:

  - time-consuming operations don’t have to bring everything else in our programs to a halt.
  - With `asynchronous programming`, JavaScript programs can start long-running tasks, and continue **running other tasks in paralell**.
  - `asynchronus programmes` are **difficult to write and difficult to debug**.

- `blocking`:
  - the browser can appear to be frozen when a web app runs in a browser and it executes an intensive chunk of code without **returning control** to the browser.
  - the browser is blocked from continuing to handle user input and perform other tasks until the web app returns control of the processor

---

## Callbacks Function

- `Callback`:

  - a function passed as an **argument** to another function
  - a way to handle asynchronous executing by **passing function as an argument** to the asynchronous function.
  - A callback function can run **after** another function has finished

- Standard contract: error-first, callback-last

  - `(callback) => callback(data)`
  - `(args, callback) => callback(err, data)`

- `Callback functions`: functions that are passed as a parameter to another function.

- 特征: 以回调函数为参数
- 效果: 回调函数将在本函数执行后执行.

- Example:

```js
list = ["apple", "banana", "cherry"];

// define a asynchronous function
const logEach = (arr, cb) => {
  arr.map((row) => {
    cb(row);
  });
};

// call the asynchronous function
// by defining an anonymous function as callback function
logEach(list, (data) => {
  console.log(data);
});

// apple
// banana
// cherry
```

---

### `setTimeout()`: 典型回调函数

- `setTimeout()`:

  - sets a timer and <u>executes a callback function</u> **after** the timer expires.

- Syntax:

```js
setTimeout(call_back_function, milliseconds, [param]);
```

- Parameter:

- `call_back_function`:
  - Function to be executed after a specific seconds
  - 需要是函数名称,或是匿名函数(function 或=>),不能直接是代码(console.log())
- `milliseconds`: 1000 = 1 second
- `param`: a list of parameter to be passed into the call back function

- **Example 1**:

```js
console.log("\n-------- setTimeout --------\n");
// Error: callback function must be funtion(a named function or anonymous function), not codes
// setTimeout(console.log("SetTimeout"), 1000);
const cbFunc = (data) => {
  console.log(data);
};

setTimeout(cbFunc, 1000, "SetTimeout"); // SetTimeout;

setTimeout(cbFunc, 1000, "SetTimeout", "Hi"); // SetTimeout;
// "Hi" will not pass because callback function defined with only one parameter
```

- **Example 2**:

```js
console.log("\n-------- setTimeout --------\n");

// define a function used as callback function latter
const cbFunc = (data) => {
  console.log(data);
};

// define an asynchronous function using setTimeout() and callback function
const main = (cb, str) => {
  setTimeout(cb, 1000, str);
};

// call asynchronous function
main(cbFunc, "hello");
```

- **经典题型**

  ```js
  // Q: 执行顺序
  console.log("1");
  setTimeout(() => console.log("2"), 1000);
  console.log("3");

  /*
  1
  3
  2
  */

  // Q: 执行顺序
  console.log("1");
  setTimeout(() => console.log("2"), 0);
  console.log("3");

  // 注意: 即使是0秒,也会延后执行, 因为setTimeout是macroStack, 会take time
  /*
  1
  3
  2
  */
  ```

---

## Promise

- `Promise`:

  - objects that represent the eventual outcome of an asynchronous operation 代表最后的结果.

- **Promise object state**

  - `Pending`: The initial state-the operation has not completed yet.
  - `Fulfilled/Resolved`: The operation has **completed successfully**, and the promise now has a **resolved value**.
  - `Rejected`: The operation has **failed**, and the promise has a reason for the failure. This reason is usually an Error of some kind.

- **Syntax**

```js
// create a promise
let myPromise = new Promise((resolve, reject) => {
  // Promise code here
  //resolve(data);
  //reject(new Error());
});

// call a promise
myPromise.then(() => {}).catch(() => {});
```

- Example: 经典问题

```js
console.log("\n-------- Promise --------\n");

const waitSecond = (ms) =>
  new Promise((resolve) => {
    setTimeout(resolve, ms);
  });

console.log("1");
waitSecond(100)
  .then(() => {
    console.log("2");
  })
  .then(() => {
    console.log("3");
  });
console.log("4");

// 1
// 4
// 2
// 3
```

---

### Chaining

- Separated control flow for success and fail.
- `.then()`: performs operations on a fulfilled promise object and returns a new value.
- `.catch()`: handles any anticipated promise rejections and throws an error.
- `.finally()`: executes without regard to whether the promise was fulfilled or rejected.

```js
console.log("\n-------- Promise --------\n");

// Promise
const delaySecond = (sec) =>
  new Promise((resolve) => {
    console.log("delay second:", sec);
    setTimeout(resolve, sec, sec); //the seconde sec passes it to resolve function
  });

delaySecond(1000)
  .then((data) => delaySecond(data)) //data will be 1000 because setTimeout in delaySecond() pass sec to resolve function
  .then((data) => delaySecond(data))
  .then((data) => delaySecond(data))
  .finally(() => console.log("End"));

// delay second: 1000
// delay second: 1000
// delay second: 1000
// delay second: 1000
// End
```

---

### Parallel Promises: `all()`

- `all()`: returns a new Promise that can be accessed as an **array of resolved values** of fulfulled Promises.
  - return: **an array of resolved values**.

```js
// all()
const xFunc = (x) => x / 100;
const yFunc = (y) => y / 1000;

const sum = (arr) =>
  new Promise((resolve) => {
    const s = arr.reduce((acc, item) => acc + item, 0);
    resolve(s);
  });

Promise.all([xFunc(3000), yFunc(3000)])
  .then((data) => sum(data))
  .then(console.log); //33
```

---

### Mixed Promises

```js
console.log("\n-------- Promise: mix --------\n");

const delaySecond = (sec) =>
  new Promise((resolve) => {
    console.log("delay second:", sec);
    setTimeout(resolve, sec, sec);
  });

const xFunc = (x) => x / 100;
const yFunc = (y) => y / 1000;

const sum = (arr) =>
  new Promise((resolve) => {
    console.log(arr); // display result array of Promise.all()
    const s = arr.reduce((acc, item) => acc + item, 0);
    resolve(s);
  });

// delay 2 second, then wait until xFunc and yFunc finish, then sum, then log
delaySecond(2000)
  .then((data) => Promise.all([xFunc(data), yFunc(data)]))
  .then((data) => sum(data))
  .then((data) => console.log(data));

// delay second: 2000
// [ 20, 2 ]
// 22
```

---

## `async`/`await`

- a new syntax for using promises

- `async`
  - keyword to mark function as asynchronous. Such function will
    **return Promise**
- `await`

  - can be used **inside async functions only**.
  - an operator that is used to wait for resolves value of a promise.
    所以使用 await 时, 其后的必须时 promise

- Problems of callbacks, Promise, async/await:

  - Nesting and syntax
  - Different contacts
  - Not cancellable, no timeouts
  - Complexity and Performance

- **Example: Chain**

```js
console.log("\n-------- async/await --------\n");

// define a promise
const delaySecond = (sec) =>
  new Promise((resolve) => {
    console.log("delay second:", sec);
    setTimeout(resolve, sec, sec); // the second sec passes to resolve function, eventually is the result of the await function
  });

// define an async function
const mainChain = async (ms) => {
  const ms1 = await delaySecond(ms);
  const ms2 = await delaySecond(ms1); //using the result of previous delaySecond
  const ms3 = await delaySecond(ms2);
  console.log("End");
};

// call the async function
mainChain(2000);

// delay second: 2000
// delay second: 2000
// delay second: 2000
// End
```

- **Example: All()**

```js
console.log("\n-------- async/await: all() --------\n");

const xFunc = (x) => x / 100;
const yFunc = (y) => y / 1000;

const sum = (arr) =>
  new Promise((resolve) => {
    const s = arr.reduce((acc, item) => acc + item, 0);
    resolve(s);
  });

// define an async using await and Promise.all()
const mainAll = async (ms) => {
  const arr = await Promise.all([xFunc(ms), yFunc(ms)]);
  console.log(arr);
  const sumArr = await sum(arr);
  console.log(sumArr);
};

// call async function
mainAll(3000);

// [ 30, 3 ]
// 33
```

- **Example: mix**

```js
console.log("\n-------- async/await: mix --------\n");

const xFunc = (x) => x / 100;
const yFunc = (y) => y / 1000;

// define a promise function
const delaySecond = (sec) =>
  new Promise((resolve) => {
    console.log("delay second:", sec);
    setTimeout(resolve, sec, sec); // the second sec passes to resolve function, eventually is the result of the await function
  });

// define a promise function
const sum = (arr) =>
  new Promise((resolve) => {
    console.log(arr);
    const s = arr.reduce((acc, item) => acc + item, 0);
    resolve(s);
  });

// define an async function
const mainMix = async (ms) => {
  const sec = await delaySecond(ms);
  const arr = await Promise.all([xFunc(sec), yFunc(sec)]);
  const sumArr = await sum(arr);
  console.log(sumArr);
};

// call async function
mainMix(2000);

// delay second: 2000
// [ 20, 2 ]
// 22
```

---

[TOP](#javascript---asynchronous-function)
