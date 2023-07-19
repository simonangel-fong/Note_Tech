# JavaScript - Array

[Back](../index.md)

- [JavaScript - Array](#javascript---array)
  - [Array](#array)
    - [Creating an Array](#creating-an-array)
    - [Accessing Array Elements](#accessing-array-elements)
    - [Changing an Array Element](#changing-an-array-element)
    - [Adding New Elements](#adding-new-elements)
  - [`.length`:Length of Array](#lengthlength-of-array)
  - [Looping Array Elements](#looping-array-elements)

---

## Array

- `Array`:

  - a special variable, which can hold more than one value.

- Arrays are **a special type of objects**.

  - `typeof array_name` returns `object`

- Array can have variables of different data types.

  ```js
  myArray[0] = Date.now;
  myArray[1] = myFunction;
  myArray[2] = myCars;
  ```

- The Difference Between Arrays and Objects
  - In JavaScript, arrays use **numbered indexes**.
  - In JavaScript, objects use **named indexes**.

---

### Creating an Array

- Using `const`
  - It defines a **constant reference to** an array.
  - Because of this, we can still change the elements of a constant array.

- Syntax

```js
// Using an array literal
const array_name = [item1, item2, ...];

// create an empty array, and then provide the elements
const array_name = [];
array_name[0]= item1;
array_name[1]= item2;
array_name[2]= item3;

// Using Array object
const array_name = new Array(item1, item2, ...);

```

---

### Accessing Array Elements

- Syntax

```js
// access an item
let var_name = array_name[index];
array_name[0]; //the first item
array_name[-1]; //the last item

// Access the Full Array
let var_name = array_name;
```

- Array indexes start with 0.
- the full array can be accessed by referring to the array name.

---

### Changing an Array Element

- Syntax

```js
array_name[index] = value;
```

---

### Adding New Elements

- Using the `push()` method

```js
console.log("\n-------- Array: .push() --------\n");

const fruits = ["Banana", "Orange", "Apple"];
fruits.push("Lemon"); // Adds a new element (Lemon) to fruits

console.log(fruits); //[ 'Banana', 'Orange', 'Apple', 'Lemon' ]
```

- Using the `length` property and index

```js
console.log("\n-------- Array: [length] --------\n");

const fruits = ["Banana", "Orange", "Apple"];
fruits[fruits.length] = "Lemon"; // Adds a new element (Lemon) to fruits

console.log(fruits); //[ 'Banana', 'Orange', 'Apple', 'Lemon' ]
```

---



---

## `.length`:Length of Array

```js
const fruits = ["Banana", "Orange", "Apple", "Mango"];
let length = fruits.length; //4
```

---

## Looping Array Elements

- Using `for` loop

```js
console.log("\n-------- Array: for loop --------\n");
const fruits = ["Banana", "Orange", "Apple", "Mango"];

for (let i = 0; i < fruits.length; i++) {
  console.log(i, fruits[i]);
}
// 0 Banana
// 1 Orange
// 2 Apple
// 3 Mango
```

- Using `.forEach()` function

```js
console.log("\n-------- Array: .forEach() --------\n");
const fruits = ["Banana", "Orange", "Apple", "Mango"];

fruits.forEach((ele) => {
  console.log(ele);
});
// Banana
// Orange
// Apple
// Mango
```

---

[TOP](#javascript---array)
