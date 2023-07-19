# Javascript - JSON

[Back](../index.md)

- [Javascript - JSON](#javascript---json)
  - [JSON](#json)
  - [`JSON.parse()`: JSON string to JS object](#jsonparse-json-string-to-js-object)
  - [`JSON.stringify()`: JS object into string](#jsonstringify-js-object-into-string)

---

## JSON

- `JSON`

  - `JavaScript Object Notation`
  - a lightweight data interchange format for storing and transporting data.

- `JSON` is often used when data is sent from a server to a web page.

- **Syntax Rules**
  - Data is in `name/value` pairs
  - Data is separated by **commas**
  - **Curly braces** hold objects
  - **Square brackets** hold arrays

---

## `JSON.parse()`: JSON string to JS object

```js
let json_str =
  '{ "employees" : [' +
  '{ "firstName":"John" , "lastName":"Doe" },' +
  '{ "firstName":"Anna" , "lastName":"Smith" },' +
  '{ "firstName":"Peter" , "lastName":"Jones" } ]}';

const json_obj = JSON.parse(json_str);

console.log(json_obj);
// {
//   employees: [
//     { firstName: 'John', lastName: 'Doe' },
//     { firstName: 'Anna', lastName: 'Smith' },
//     { firstName: 'Peter', lastName: 'Jones' }
//   ]
// }
console.log(typeof json_obj); //object
```

---

## `JSON.stringify()`: JS object into string

```js
const obj = { name: "John", age: 30, city: "New York" };
const json_str = JSON.stringify(obj);

console.log(json_str); //{"name":"John","age":30,"city":"New York"}
console.log(typeof json_str); //string
```

---

[TOP](#javascript---json)
