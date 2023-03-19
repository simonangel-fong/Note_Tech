# JavaScript BigInt

[Back](../index.md)

- [JavaScript BigInt](#javascript-bigint)
  - [BigInt](#bigint)
  - [Create BigInt](#create-bigint)
  - [BigInt Decimals](#bigint-decimals)

---

## BigInt

- JavaScript `BigInt` variables are used to store big integer values that are **too big** to be represented by a normal JavaScript Number.

---

## Create BigInt

- To create a BigInt, append n to the end of an integer or call BigInt().

```js
var x = 9999999999999999n;
var y = BigInt(1234567890123456789012345);

console.log(typeof x); //bigint
console.log(typeof y); //bigint
```

## BigInt Decimals

- A `BigInt` can not have decimals.

```js
var x = 5n;
// var y = x / 2; // Error: Cannot mix BigInt and other types, use explicit conversion.

var y = Number(x) / 2;
console.log(y); //2.5
```

---

[TOP](#javascript-bigint)
