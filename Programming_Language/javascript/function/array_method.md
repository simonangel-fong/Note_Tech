# Javascript - Array Method

[Back](../index.md)

- [Javascript - Array Method](#javascript---array-method)
  - [Cheapsheet](#cheapsheet)
  - [Keys and Values](#keys-and-values)
    - [`keys()`](#keys)
    - [`entries()`](#entries)
  - [Converting Data Type](#converting-data-type)
    - [`Array.from()`: to Array](#arrayfrom-to-array)
    - [`toString()`: to String](#tostring-to-string)
    - [`join()`: to String with a specified separator](#join-to-string-with-a-specified-separator)
  - [Manipulate Element](#manipulate-element)
    - [`pop()`](#pop)
    - [`push()`](#push)
    - [`shift()`](#shift)
    - [`unshift()`](#unshift)
    - [`delete` operator](#delete-operator)
    - [`splice()`](#splice)
  - [Concatenating](#concatenating)
    - [`concat()`](#concat)
    - [`flat(depth)`](#flatdepth)
    - [Spread Operator: `...`](#spread-operator-)
  - [Iterating \& Extracting](#iterating--extracting)
    - [`forEach()`](#foreach)
    - [`map()`](#map)
    - [`filter()`](#filter)
    - [`slice()`](#slice)
  - [Sorting element](#sorting-element)
    - [`sort()`](#sort)
      - [Sorting String Arrays](#sorting-string-arrays)
      - [Sorting Number Arrays](#sorting-number-arrays)
      - [Sorting Object Arrays](#sorting-object-arrays)
    - [`reverse()`](#reverse)
  - [Max/Min element](#maxmin-element)
  - [Searching element](#searching-element)
    - [`includes()`](#includes)
    - [`every()`](#every)
    - [`some()`](#some)
    - [`find()`](#find)
    - [`findIndex()`](#findindex)
    - [`indexOf()`](#indexof)
    - [`lastIndexOf()`](#lastindexof)
  - [Accumulating element](#accumulating-element)
    - [`reduce()`](#reduce)

---

## Cheapsheet

- Keys and Values

| Method      | Description                           |
| ----------- | ------------------------------------- |
| `keys()`    | the keys of the original array        |
| `entries()` | key/value pair Array Iteration Object |

- Converting Data Type

| Method         | Description                      | Callback |
| -------------- | -------------------------------- | -------- |
| `Array.from()` | Creates an array from an object  | Y        |
| `toString()`   | Converts an array to a string    |          |
| `join()`       | Joins all elements into a string |          |

- Manipulate Element

| Method            | Description                              |
| ----------------- | ---------------------------------------- |
| `pop()`           | Removes the last element                 |
| `push()`          | Adds new elements to the end of an array |
| `shift()`         | Removes the first element                |
| `unshift()`       | Adds new elements to the beginning       |
| `delete` operator | delete element                           |
| `splice()`        | Adds/Removes elements from an array      |

- Concatenating

| Method     | Description                            |
| ---------- | -------------------------------------- |
| `concat()` | Joins arrays                           |
| `flat()`   | Concatenates sub-array elements        |
| `...`      | expands an iterable into more elements |

- Iterating & Extracting

| Method      | Description                                               | Callback |
| ----------- | --------------------------------------------------------- | -------- |
| `forEach()` | Calls a function for each array element                   | Y        |
| `map()`     | Calls a function for each element and creates a new array | Y        |
| `filter()`  | Creates a new array with condition                        | Y        |
| `slice()`   | Selects a part of an array                                |          |

- Sorting element

| Method      | Description                        | Callback |
| ----------- | ---------------------------------- | -------- |
| `sort()`    | Sorts the elements                 | Y        |
| `reverse()` | Reverses the order of the elements |          |

- Searching element

| Method          | Description                                                         | Callback |
| --------------- | ------------------------------------------------------------------- | -------- |
| `includes()`    | Check if an array contains the specified element                    |          |
| `every()`       | Checks if every element in an array pass a test                     | Y        |
| `some()`        | Checks if any of the elements in an array pass a test               | Y        |
| `find()`        | Returns the value of the first element in an array that pass a test | Y        |
| `findIndex()`   | Returns the index of the first element in an array that pass a test | Y        |
| `indexOf()`     | Search the array for an element and returns its position            |          |
| `lastIndexOf()` | Search the array for an element and returns its last position       |          |

- Accumulating element

| Method     | Description                                     | Callback |
| ---------- | ----------------------------------------------- | -------- |
| `reduce()` | Reduce the values of an array to a single value | Y        |

---

## Keys and Values

### `keys()`

- returns an Array Iterator object with the **keys** of an array.
- does not change the original array.

- Syntax:

```js
array.keys();
```

- **Parameter**

  - None

- **Return Value**: `array`
  - An Array Iterator object containing the **keys** of an array.

```js
console.log("\n-------- Array: keys() --------\n");

const fruits = ["Banana", "Orange", "Apple", "Mango"];
const key_arr = fruits.keys();

console.log(key_arr); //Object [Array Iterator] {}

for (let k of key_arr) {
  console.log(k);
}
// 0
// 1
// 2
// 3
```

---

### `entries()`

- returns an Array Iterator object with key/value pairs
- does not change the original array.

- Syntax:

```js
array.entries();
```

- **Parameter**

  - None

- **Return Value**: `array`
  - An array like iterable with key/value pairs.

```js
console.log("\n-------- Array: entries() --------\n");

const fruits = ["Banana", "Orange", "Apple", "Mango"];
console.log(fruits.entries()); // Object [Array Iterator] {}

const k_v_arr = fruits.entries();

for (let row of k_v_arr) {
  console.log(row);
}
// [ 0, 'Banana' ]
// [ 1, 'Orange' ]
// [ 2, 'Apple' ]
// [ 3, 'Mango' ]
```

---

## Converting Data Type

### `Array.from()`: to Array

- `Array.from()` is a static property of the JavaScript Array object.
- returns an array from any object with a length property.
- returns an array from any iterable object.

- Syntax:

```js
Array.from(object, mapFunction, thisValue);
```

- **Parameter**

| Parameter     | Description                                         |
| ------------- | --------------------------------------------------- |
| `object`      | Required. The object to convert to an array.        |
| `mapFunction` | Optional. A map function to call on each item.      |
| `thisValue`   | Optional. A value to use as thisfor the mapFunction |

- **Return Value**: `array`
  - The values from the iterable object.

```js
console.log("\n-------- Array: Array.from() --------\n");

const text = "ABCDEFG";
console.log(Array.from(text)); // ["A", "B", "C", "D", "E", "F", "G"];
console.log(Array.from(text, (str) => str.concat(str))); // ["AA", "BB", "CC", "DD", "EE", "FF", "GG"];
```

---

### `toString()`: to String

```js
console.log("\n-------- Array: toString() --------\n");
const fruits = ["Banana", "Orange", "Apple", "Mango"];

// toString(): converts an array to a string of (comma separated) array values.
console.log(fruits.toString()); //Banana,Orange,Apple,Mango
```

---

### `join()`: to String with a specified separator

```js
console.log("\n-------- Array: join() --------\n");

// join(): joins all array elements into a string with a specified separator.
const fruits = ["Banana", "Orange", "Apple", "Mango"];
console.log(fruits.join()); //Banana,Orange,Apple,Mango
console.log(fruits.join("|")); //Banana|Orange|Apple|Mango
console.log(fruits.join("-ee-")); //Banana-ee-Orange-ee-Apple-ee-Mango
```

---

## Manipulate Element

### `pop()`

```js
console.log("\n-------- Array: pop() --------\n");

// pop():
// removes the last element from an array
// returns the value that was "popped out"
const fruits = ["Banana", "Orange", "Apple", "Mango"];
console.log(fruits.pop()); // Mango
console.log(fruits); // [ 'Banana', 'Orange', 'Apple' ]

console.log(fruits.pop()); // Apple
console.log(fruits.pop()); // Orange
console.log(fruits.pop()); // Banana
console.log(fruits); // []

console.log(fruits.pop()); // undefined
console.log(fruits); // []
```

---

### `push()`

```js
console.log("\n-------- Array: push(element) --------\n");

// push(): adds a new element to an array (at the end)
// Parameters   Description
// element      The element(s) to add to the end of the array
// Return       Description
// int          The new length property of the object
const fruits = ["Apple", "Banana"];
console.log(fruits.push()); // 2
console.log(fruits); // [ 'Apple', 'Banana' ]

console.log(fruits.push("Cherry")); // 3
console.log(fruits); // [ 'Apple', 'Banana', 'Cherry' ]

console.log(fruits.push("Date", "Eggplant")); // 5
console.log(fruits); // [ 'Apple', 'Banana', 'Cherry', 'Date', 'Eggplant' ]
```

---

### `shift()`

```js
console.log("\n-------- Array: shift() --------\n");

// shift(): removes the first array element and "shifts" all other elements to a lower index.
// Return       Description
// element      returns the value that was "shifted out"
const fruits = ["Apple", "Banana", "Cherry"];
console.log(fruits.shift()); // Apple
console.log(fruits); // [ 'Banana', 'Cherry' ]

console.log(fruits.shift()); // Banana
console.log(fruits.shift()); // Cherry
console.log(fruits); // []

console.log(fruits.shift()); // undefined
console.log(fruits); // []
```

---

### `unshift()`

```js
console.log("\n-------- Array: unshift() --------\n");

// unshift(): adds a new element to an array (at the beginning)
// Parameters   Description
// element      The element(s) to add to the beginning of the array
// Return       Description
// int          returns the new array length
const fruits = [];
console.log(fruits.unshift("Apple")); // 1
console.log(fruits); // [ 'Apple' ]

console.log(fruits.unshift("Banana", "Cherry")); // 3
console.log(fruits); //[ 'Banana', 'Cherry', 'Apple' ]
```

---

### `delete` operator

```js
console.log("\n-------- Array: delete operator --------\n");

// delete operator: delete element in array
// leaves undefined holes in the array.
const fruits = ["Apple", "Banana", "Cherry"];
delete fruits[0];
console.log(fruits); // [ <1 empty item>, 'Banana', 'Cherry' ]
console.log(fruits[0]); // undefined
```

---

### `splice()`

```js
console.log("\n-------- Array: splice() --------\n");

// splice(index, num, items): adds and/or removes array elements.
// Parameter    Description
// index        Required. The position to add/remove items. Negative value defines the position from the end of the array.
// num          Optional. Number of items to be removed.
// elements     Optional. New elements(s) to be added.
// Return       Description
// array        An array containing the removed items (if any).
const fruits = ["Apple", "Banana", "Cherry"];

// addition
console.log(fruits.splice(0, 0, "new first")); //[], due to addtion, not removal
console.log(fruits); // [ 'new first', 'Apple', 'Banana', 'Cherry' ]

console.log(fruits.splice(fruits.length, 0, "new last end")); //[], index to remove the last is length, not -1.
console.log(fruits); // [ 'new first', 'Apple', 'Banana', 'Cherry', 'new last end' ]

// removal
console.log(fruits.splice(0, 1)); // [ 'new first' ]
console.log(fruits); // [ 'Apple', 'Banana', 'Cherry', 'new last end' ]

console.log(fruits.splice(-1, 1)); // [ 'new last end' ]
console.log(fruits); // [ 'Apple', 'Banana', 'Cherry' ]

console.log(fruits.splice(-2, 2)); //[ 'Banana', 'Cherry' ]
console.log(fruits); // [ 'Apple' ]

// replace
console.log(fruits.splice(0, 1, "new apple", "new banana")); // [ 'Apple' ]
console.log(fruits); // [ 'new apple', 'new banana' ]

// replace all
console.log(fruits.splice(0, fruits.length, "Alpha", "Bravo", "Charlie")); // [ 'new apple', 'new banana' ]
console.log(fruits); // [ 'Alpha', 'Bravo', 'Charlie' ]
```

---

## Concatenating

### `concat()`

```js
console.log("\n-------- Array: concat(value) --------\n");

// concat(): creates a new array by merging (concatenating) existing arrays
// does not change the existing arrays. It always returns a new array.
// Parameter    Description
// value        Arrays and/or values to concatenate into a new array
// Return       Description
// array        A new Array instance.
const x_arr = ["Cecilie", "Lone"];
const y_arr = ["Emil", "Tobias", "Linus"];
const z_arr = ["Robin", "Morgan"];

const arr1 = x_arr.concat(y_arr);
console.log("x_arr", x_arr); // x_arr [ 'Cecilie', 'Lone' ]
console.log("y_arr", y_arr); // y_arr [ 'Emil', 'Tobias', 'Linus' ]
console.log("arr1", arr1); // arr1 [ 'Cecilie', 'Lone', 'Emil', 'Tobias', 'Linus' ]

const arr2 = x_arr.concat(y_arr, z_arr);
console.log("arr2", arr2);
// arr2 [
//     'Cecilie', 'Lone',
//     'Emil',    'Tobias',
//     'Linus',   'Robin',
//     'Morgan'
//   ]

const arr3 = x_arr.concat("Peter");
console.log("arr3", arr3); //arr3 [ 'Cecilie', 'Lone', 'Peter' ]
```

---

### `flat(depth)`

```js
console.log("\n-------- Array: flat() --------\n");

// flat(depth): concatenates sub-array elements.
// Parameter    Description
// depth        Optional. How deep a nested array should be flattened. Default is 1.
// Return       Description
// array        The flattened array.
const x_arr = [
  [1, 2],
  [3, 4],
  [5, 6],
];
console.log(x_arr.flat()); // [ 1, 2, 3, 4, 5, 6 ]

const y_arr = [1, 2, [3, [4, 5, 6], 7], 8];
console.log(y_arr.flat()); //[ 1, 2, 3, [ 4, 5, 6 ], 7, 8 ]
console.log(y_arr.flat(1)); //[ 1, 2, 3, [ 4, 5, 6 ], 7, 8 ]
console.log(y_arr.flat(2)); //[ 1, 2, 3, [ 4, 5, 6 ], 7, 8 ]
// [
//     1, 2, 3, 4,
//     5, 6, 7, 8
//   ]
```

---

### Spread Operator: `...`

The `...` operator expands an iterable into more elements.

```js
console.log("\n-------- Spread Operator --------\n");

const q1 = ["Jan", "Feb", "Mar"];
const q2 = ["Apr", "May", "Jun"];
const q3 = ["Jul", "Aug", "Sep"];
const q4 = ["Oct", "Nov", "May"];

const year = [...q1, ...q2, ...q3, ...q4];

console.log(year);
// [
//   "Jan",
//   "Feb",
//   "Mar",
//   "Apr",
//   "May",
//   "Jun",
//   "Jul",
//   "Aug",
//   "Sep",
//   "Oct",
//   "Nov",
//   "May",
// ];
```

---

## Iterating & Extracting

### `forEach()`

- calls a function for each element in an array.
- not executed for empty elements.

- Syntax:

```js
arr.forEach(function(currentValue, index, arr), thisValue);
```

- **Parameter**

| Parameter      | Description                                                                    |
| -------------- | ------------------------------------------------------------------------------ |
| `function()`   | Required. A function to run for each array element.                            |
| `currentValue` | Required. The value of the current element.                                    |
| `index`        | Optional. The index of the current element.                                    |
| `arr`          | Optional. The array of the current element.                                    |
| `thisValue`    | Optional. Default undefined. A value passed to the function as its this value. |

- Return: `undefined`

```js
console.log("\n-------- Array: forEach() --------\n");

const fruits = ["apple", "orange", "cherry"];

// using callback function
fruits.forEach(console.log);
// apple 0 [ 'apple', 'orange', 'cherry' ]
// orange 1 [ 'apple', 'orange', 'cherry' ]
// cherry 2 [ 'apple', 'orange', 'cherry' ]

// define a callback function
const cb = (itm) => console.log(itm);
fruits.forEach(cb);
// apple
// orange
// cherry

// using anonymous function
fruits.forEach((itm) => {
  console.log(itm);
});
// apple
// orange
// cherry

fruits.forEach((itm, index) => {
  console.log(index, itm);
});
// 0 apple
// 1 orange
// 2 cherry

fruits.forEach((itm, index, arr) => {
  console.log(index, itm, arr);
});
// 0 apple [ 'apple', 'orange', 'cherry' ]
// 1 orange [ 'apple', 'orange', 'cherry' ]
// 2 cherry [ 'apple', 'orange', 'cherry' ]

const numbers = [65, 44, 12, 4];

// get sum
let sum = 0;
numbers.forEach((itm) => {
  sum += itm;
});
console.log("Sum:", sum); //Sum: 125

// Min value
let minVal = Infinity;
numbers.forEach((itm) => {
  if (itm < minVal) {
    minVal = itm;
  }
});
console.log("Min:", minVal); //Sum: 4

// Multiply each element
numbers.forEach((itm, index, arr) => {
  arr[index] = itm * 10;
});
console.log(numbers); //[ 650, 440, 120, 40 ]
```

---

### `map()`

- creates a new array from calling a function for every array element.
- not execute the function for empty elements.
- not change the original array.

- Syntax:

```js
array.map(function(currentValue, index, arr), thisValue)
```

- **Parameter**

| Parameter      | Description                                                                      |
| -------------- | -------------------------------------------------------------------------------- |
| `function()`   | Required. A function to be run for each array element.                           |
| `currentValue` | Required. The value of the current element.                                      |
| `index`        | Optional. The index of the current element.                                      |
| `arr`          | Optional. The array of the current element.                                      |
| `thisValue`    | Optional. Default `undefined`. A value passed to the function as its this value. |

- Return: `array`
  - The results of a function for each array element.

```js
console.log("\n-------- Array: map() --------\n");
const num_sq = [4, 9, 16, 25];
console.log(num_sq.map(Math.sqrt)); //[ 2, 3, 4, 5 ]
console.log(num_sq.map((itm) => itm * 10)); //[ 40, 90, 160, 250 ]

const persons = [
  { firstname: "Malcom", lastname: "Reynolds" },
  { firstname: "Kaylee", lastname: "Frye" },
  { firstname: "Jayne", lastname: "Cobb" },
];

console.log(persons.map((itm) => [itm.firstname, itm.lastname].join(" ")));
// [ 'Malcom Reynolds', 'Kaylee Frye', 'Jayne Cobb' ]
```

---

### `filter()`

- creates a new array filled with elements that pass a test provided by a function.
- does not execute the function for empty elements.
- does not change the original array.

- Syntax:

```js
array.filter(function(currentValue, index, arr), thisValue)
```

- **Parameter**

| Parameter      | Description                                                                      |
| -------------- | -------------------------------------------------------------------------------- |
| `function()`   | Required. A function to be run for each array element.                           |
| `currentValue` | Required. The value of the current element.                                      |
| `index`        | Optional. The index of the current element.                                      |
| `arr`          | Optional. The array of the current element.                                      |
| `thisValue`    | Optional. Default `undefined`. A value passed to the function as its this value. |

- **Return Value**: `Array`
  - An array of elements that pass the test.
  - An empty array if no elements pass the test.

```js
console.log("\n-------- Array: filter() --------\n");

const ages = [32, 33, 16, 40];
const over30 = ages.filter((itm) => itm > 30);

console.log(over30); //[ 32, 33, 40 ]

const over50 = ages.filter((itm) => itm > 50);
console.log(over50); //[]
```

---

### `slice()`

- returns selected elements in an array, as a new array.
- selects from a given start, up to a (not inclusive) given end.
- does not change the original array.

- Syntax

```js
array.slice(start, end);
```

- **Parameter**

| Parameter | Description                                     |
| --------- | ----------------------------------------------- |
| `start`   | Optional. Start position. Default is 0.         |
| `end`     | Optional.End position. Default is last element. |

- Return: `Array`
  - A new array containing the selected elements.

---

## Sorting element

### `sort()`

- sorts the elements of an array.

- Syntax:

```js
arr.sort(compareFunction);
```

- **Overwrites** the original array.
- Default order: alphabetical and ascending order

- `compareFunction`: Optional
  - A function that defines a sort order.
- The function should return a negative, zero, or positive value, depending on the arguments.
  - `function(a, b){return a-b}`
- When the `sort()` function compares two values, it sends the values to the compare function, and sorts the values according to the returned (negative, zero, positive) value.

  - If the result is **negative, a is sorted before b**.
  - If the result is **positive, b is sorted before a**.
  - If the result is **0, no changes** are done with the sort order of the two values.
  - 可以理解为 a 是前项, b 是当前项.
    - `a-b <= 0`时, `a <= b`, 排序正确;
    - `0 < a-b`时, `b < a`, 排序颠倒;

- Return: The array with the items sorted.

#### Sorting String Arrays

- String elements are sorted in alphabetical and ascending order.

```js
console.log("\n-------- Array: sort() --------\n");

const fruits = ["Banana", "Orange", "Apple", "Mango"];

console.log(fruits.sort()); // [ 'Apple', 'Banana', 'Mango', 'Orange' ]
console.log(fruits); // [ 'Apple', 'Banana', 'Mango', 'Orange' ], overwrites the original array.
```

---

#### Sorting Number Arrays

- sorting numbers can produce incorrect results, due to the default alphabetical and ascending order.
- compareFunction helps.

```js
const points = [40, 100, 1, 5, 25, 10];
console.log(points.sort()); // [ 1, 10, 100, 25, 40, 5 ], incorrect due to alphabetical order

// ascending order
console.log(
  points.sort(function (a, b) {
    return a - b;
  })
); // [ 1, 5, 10, 25, 40, 100 ]

console.log("min value:", points[0]); // min value: 1
console.log("max value:", points[points.length - 1]); // max value: 100

// descending order
console.log(
  points.sort(function (a, b) {
    return b - a;
  })
); // [ 100, 40, 25, 10, 5, 1 ]
console.log("max value:", points[0]); // max value: 100
console.log("min value:", points[points.length - 1]); // min value: 1

// Sorting an Array in Random Order
console.log(points.sort(() => 0.5 - Math.random())); // [ 10, 25, 40, 100, 5, 1 ], different order for each output
```

---

#### Sorting Object Arrays

- Numeric property:

```js
const cars = [
  { type: "Volvo", year: 2016 },
  { type: "Saab", year: 2001 },
  { type: "BMW", year: 2010 },
];

console.log(cars.sort((a, b) => a.year - b.year));
// [
//   { type: "Saab", year: 2001 },
//   { type: "BMW", year: 2010 },
//   { type: "Volvo", year: 2016 },
// ];
```

- String property:
- 注意: compareFunction 最终判断的是正数还是负数, 不能是 true/false, 所以以下在判断大小于后以-1/1 返回.

```js
const cars = [
  { type: "Volvo", year: 2016 },
  { type: "Saab", year: 2001 },
  { type: "BMW", year: 2010 },
];

console.log(
  cars.sort((a, b) => {
    return a.type.toLowerCase() < b.type.toLowerCase() ? -1 : 1;
  })
);
// [
//   { type: 'BMW', year: 2010 },
//   { type: 'Saab', year: 2001 },
//   { type: 'Volvo', year: 2016 }
// ]
```

---

### `reverse()`

```js
console.log("\n-------- Array: reverse() --------\n");

// reverse():   reverses the order of the elements in an array.
// Return       Description
// array        The array after it has been reversed.
const fruits = ["Banana", "Orange", "Apple", "Mango"];

console.log(fruits.sort()); // [ 'Apple', 'Banana', 'Mango', 'Orange' ]
console.log(fruits.reverse()); // [ 'Orange', 'Mango', 'Banana', 'Apple' ]

const points = [40, 100, 1, 5, 25, 10];

// ascending order
console.log(
  points.sort(function (a, b) {
    return a - b;
  })
); // [ 1, 5, 10, 25, 40, 100 ]
console.log("reverse order:", points.reverse()); //reverse order: [ 100, 40, 25, 10, 5, 1 ]

// descending order
console.log(
  points.sort(function (a, b) {
    return b - a;
  })
); // [ 100, 40, 25, 10, 5, 1 ]
console.log("reverse order:", points.reverse()); //reverse order: [ 1, 5, 10, 25, 40, 100 ]
```

---

## Max/Min element

- Using `arr.sort()` + `arr[0]`

- Using `Math.max`

```js
console.log("\n-------- Array: Max/Min Value --------\n");

const points = [40, 100, 1, 5, 25, 10];

const max_value = (arr) => Math.max.apply(null, arr);
const min_value = (arr) => Math.min.apply(null, arr);

console.log("max:", max_value(points));
console.log("min:", min_value(points));
```

- Customized function:

```js
console.log("\n-------- Array: Max/Min Value --------\n");

const points = [40, 100, 1, 5, 25, 10];

const max_value = (arr) => {
  let max_value = -Infinity;
  for (itm of arr) {
    if (max_value < itm) {
      max_value = itm;
    }
  }
  return max_value;
};

const min_value = (arr) => {
  let min_value = Infinity;
  for (itm of arr) {
    if (itm < min_value) {
      min_value = itm;
    }
  }
  return min_value;
};

console.log("max_value:", max_value(points)); // max_value: 100
console.log("min_value:", min_value(points)); // min_value: 1
```

---

## Searching element

### `includes()`

- returns `true` if an array contains a specified value.
- returns `false` if the value is not found.
- is case sensitive.

- Syntax:

```js
array.includes(element, start);
```

- **Parameter**

| Parameter | Description                             |
| --------- | --------------------------------------- |
| `element` | Required. The value to search for.      |
| `start`   | Optional. Start position. Default is 0. |

- **Return Value**: `boolean`
  - `true` if the value is found, otherwise `false`.

```js
console.log("\n-------- Array: includes() --------\n");

const fruits = ["Banana", "Orange", "Apple", "Mango"];
console.log(fruits.includes("Orange")); // true
console.log(fruits.includes("Orange", 1)); // true, inclusive
console.log(fruits.includes("Orange", 2)); // false
```

---

### `every()`

- executes a function for each array element.

  - returns `true` if the function returns true **for all** elements.
  - returns `false` if the function returns false for one element.

- does not execute the function for empty elements.
- does not change the original array
- -Syntax:

```js
array.every(function(currentValue, index, arr), thisValue)
```

- **Parameter**

| Parameter      | Description                                                                      |
| -------------- | -------------------------------------------------------------------------------- |
| `function()`   | Required. A function to be run for each array element.                           |
| `currentValue` | Required. The value of the current element.                                      |
| `index`        | Optional. The index of the current element.                                      |
| `arr`          | Optional. The array of the current element.                                      |
| `thisValue`    | Optional. Default `undefined`. A value passed to the function as its this value. |

- Return: `Boolean`
  - `true` if all elements pass the test, otherwise `false`.

```js
console.log("\n-------- Array: every() --------\n");
const survey = [
  { name: "Steve", answer: "Yes" },
  { name: "Jessica", answer: "Yes" },
  { name: "Peter", answer: "Yes" },
  { name: "Elaine", answer: "No" },
];

let isSame = survey.every((itm, index, arr) => {
  if (index == 0) {
    return true;
  } else {
    return itm.answer === arr[index - 1].answer;
  }
});
console.log("isSame", isSame);

const ages = [32, 33, 12, 40];

let isOver18 = ages.every((itm) => itm >= 18);
console.log("isOver18", isOver18);
```

---

### `some()`

- checks if any array elements pass a test (provided as a callback function).

- executes the callback function once for each array element.
  - returns **true (and stops)** if the function returns `true` for one of the array elements.
  - returns `false` if the function returns **`false` for all** of the array elements.
- does not execute the function for empty array elements.
- does not change the original array.

- Syntax

```js
array.some(function(value, index, arr), this)
```

- **Parameter**

| Parameter      | Description                                                                      |
| -------------- | -------------------------------------------------------------------------------- |
| `function()`   | Required. A function to be run for each array element.                           |
| `currentValue` | Required. The value of the current element.                                      |
| `index`        | Optional. The index of the current element.                                      |
| `arr`          | Optional. The array of the current element.                                      |
| `thisValue`    | Optional. Default `undefined`. A value passed to the function as its this value. |

- Return: `boolean`
  - `true` if any of the aray elements pass the test, otherwise `false`.

```js
console.log("\n-------- Array: some() --------\n");
const numbers = [12, 16, 20, 4];

let isAdult = numbers.some((itm) => {
  console.log(itm);
  return itm > 18;
});

console.log(`isAdult`, isAdult); //isJuveniles true, stop at 20, not iterate all item
```

---

### `find()`

- executes a function for each array element.

  - returns the value of the first element that passes a test.
  - returns `undefined` if **no elements** are found.

- does not execute the function for empty elements.
- does not change the original array.

```js
array.find(function(currentValue, index, arr),thisValue)
```

- **Parameter**

| Parameter      | Description                                                                      |
| -------------- | -------------------------------------------------------------------------------- |
| `function()`   | Required. A function to be run for each array element.                           |
| `currentValue` | Required. The value of the current element.                                      |
| `index`        | Optional. The index of the current element.                                      |
| `arr`          | Optional. The array of the current element.                                      |
| `thisValue`    | Optional. Default `undefined`. A value passed to the function as its this value. |

- Return:
  - The value of the **first** element that pass the test. Otherwise it returns undefined.

```js
console.log("\n-------- Array: find() --------\n");

const ages = [4, 12, 20, 16];

let isAdult = ages.find((itm) => {
  console.log(itm);
  return itm > 18;
});

console.log(`isAdult`, isAdult); //isAdult 20, stop until 20
```

---

### `findIndex()`

- executes a function for each array element.

  - returns the index (position) of the first element that passes a test.
  - returns `-1` if no match is found.

- does not execute the function for empty array elements.
- does not change the original array.

- Syntax:

```js
array.findIndex(function(currentValue, index, arr), thisValue)
```

- **Parameter**

| Parameter      | Description                                                                      |
| -------------- | -------------------------------------------------------------------------------- |
| `function()`   | Required. A function to be run for each array element.                           |
| `currentValue` | Required. The value of the current element.                                      |
| `index`        | Optional. The index of the current element.                                      |
| `arr`          | Optional. The array of the current element.                                      |
| `thisValue`    | Optional. Default `undefined`. A value passed to the function as its this value. |

- **Return Value**: number
  - The index (position) of the first item found.
  - `-1 `if the item is not found.

```js
console.log("\n-------- Array: findIndex() --------\n");

const ages = [4, 12, 20, 16];

let isAdult = ages.findIndex((itm) => {
  console.log(itm);
  return itm > 18;
});

console.log(`isAdult`, isAdult); //isAdult 2, stop until 20
```

---

### `indexOf()`

- returns the first index (position) of a specified value.
  - returns -1 if the value is not found.
  - starts at a specified index and searches from left to right.
- By default the search starts at the first element and ends at the last.
- Negative start values counts from the last element (but still searches from left to right).

- Syntax:

```js
array.indexOf(item, start);
```

- **Parameter**

| Parameter | Description                                              |
| --------- | -------------------------------------------------------- |
| `item`    | Required. The value to search for.                       |
| `start`   | Optional. Where to start the search. Default value is 0. |

- **Return Value**: number
  - The index (position) of the first item found.
  - `-1 `if the item is not found.

```js
console.log("\n-------- Array: indexOf() --------\n");
const fruits = ["Banana", "Orange", "Apple", "Mango", "Apple"];

console.log(fruits.indexOf("")); //-1
console.log(fruits.indexOf("None")); //-1
console.log(fruits.indexOf("Apple")); //2
console.log(fruits.indexOf("Apple", 2)); //2, exclusive
console.log(fruits.indexOf("Apple", 3)); //4
```

---

### `lastIndexOf()`

- returns the last index (position) of a specified value.
  - returns -1 if the value is not found.
- The lastIndexOf() starts at a specified index and searches from right to left.
- By defalt the search starts at the last element and ends at the first.
- Negative start values counts from the last element (but still searches **from right to left**).

- Syntax:

```js
array.lastIndexOf(item, start);
```

- **Parameter**

| Parameter | Description                                              |
| --------- | -------------------------------------------------------- |
| `item`    | Required. The value to search for.                       |
| `start`   | Optional. Where to start the search. Default value is 0. |

- **Return Value**: number
  - The index (position) of the first item found.
  - `-1 `if the item is not found.

```js
console.log("\n-------- Array: lastIndexOf() --------\n");
const fruits = ["Banana", "Orange", "Apple", "Mango", "Apple"];

console.log(fruits.lastIndexOf("")); //-1;
console.log(fruits.lastIndexOf("None")); //-1
console.log(fruits.lastIndexOf("Apple")); //4
console.log(fruits.lastIndexOf("Apple", 1)); //-1
console.log(fruits.lastIndexOf("Apple", 4)); //4, inclusive
console.log(fruits.lastIndexOf("Apple", 10)); //4
console.log(fruits.lastIndexOf("Apple", -1)); //4
console.log(fruits.lastIndexOf("Apple", -3)); //2
```

---

## Accumulating element

### `reduce()`

- returns a single value: the function's accumulated result.

- works from left-to-right in the array.
- does not execute the function for empty array elements.
- does not reduce the original array.

-Syntax:

```js
array.reduce(function(total, currentValue, currentIndex, arr), initialValue)
```

- **Parameter**

| Parameter      | Description                                                                   |
| -------------- | ----------------------------------------------------------------------------- |
| `function()`   | Required. A function to be run for each array element.                        |
| `total`        | Required. The initialValue, or the previously returned value of the function. |
| `currentValue` | Required. The value of the current element.                                   |
| `index`        | Optional. The index of the current element.                                   |
| `arr`          | Optional. The array of the current element.                                   |
| `initialValue` | Optional. A value to be passed to the function as the initial value.          |

- Return:
  - The **accumulated result** from the last call of the callback function.

```js
console.log("\n-------- Array: reduce() --------\n");
const numbers = [15.5, 2.3, 1.1, 4.7];

const sumVal = numbers.reduce((acc, itm) => {
  return (acc += Math.round(itm));
}, 0);
console.log(sumVal); //24
```

---

---

[Top](#javascript---array-method)
