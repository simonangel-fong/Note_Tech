# JavaScript - String Method

[back](../index.md)

- [JavaScript - String Method](#javascript---string-method)
  - [Cheapsheet](#cheapsheet)
  - [Extracting Character](#extracting-character)
    - [Property Access, `charAt()`, `charCodeAt()`](#property-access-charat-charcodeat)
  - [Extracting Text](#extracting-text)
    - [`slice()`](#slice)
    - [`substring()`](#substring)
  - [Searching](#searching)
    - [`includes()`](#includes)
    - [`startsWith()`](#startswith)
    - [`endsWith()`](#endswith)
    - [`indexOf()`, `lastIndexOf()`](#indexof-lastindexof)
    - [`search()`](#search)
    - [`match()`](#match)
    - [`matchAll()`](#matchall)
  - [Replacing](#replacing)
    - [`replace()`](#replace)
    - [`replaceAll()`](#replaceall)
  - [Concatenating](#concatenating)
    - [`concat()`](#concat)
  - [Converting Case](#converting-case)
    - [`toLowerCase()`, `toUpperCase()`](#tolowercase-touppercase)
  - [Trimming](#trimming)
    - [`trim()`, `trimStart()`, `trimEnd()`](#trim-trimstart-trimend)
  - [Padding](#padding)
    - [`padStart()`, `padEnd()`](#padstart-padend)
  - [Converting Data Type](#converting-data-type)
    - [`split()`: String to Array](#split-string-to-array)
    - [`valueOf()`: Object to String](#valueof-object-to-string)

---

## Cheapsheet

- **Extracting Character**

| Method              | Description                                                       |
| ------------------- | ----------------------------------------------------------------- |
| `string[index]`     | returns the character at a specified index (position) in a string |
| `charAt(index)`     | returns the character at a specified index (position) in a string |
| `charCodeAt(index)` | returns the unicode of the character at a specified index         |

- **Extracting Text**

| Method                  | Description                   |
| ----------------------- | ----------------------------- |
| `slice(start, end)`     | extracting a part of a string |
| `substring(start, end)` | extracting a part of a string |

- **Searching**

| Method                             | Description                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| `includes(target, start_index)`    | returns true if a string contains a specified value.                             |
| `startsWith(target, start_index)`  | returns true if a string begins with a specified value.                          |
| `endsWith(target, start_index)`    | returns true if a string ends with a specified string.                           |
| `indexOf(target, start_index)`     | returns the index of (position of) the first occurrence of a string in a string  |
| `lastIndexOf(target, start_index)` | returns the index of the last occurrence of a specified text in a string         |
| `search(target)`                   | returns the position of the match                                                |
| `match(target)`                    | returns an array containing the results of matching a string against a string    |
| `matchAll(target)`                 | returns an iterator containing the results of matching a string against a string |

- **Replacing**

| Method                        | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `replace(matched, target)`    | replaces a specified value with another value in a string |
| `replaceAll(matched, target)` | replaces all value with another value                     |

- **Concatenating**

| Method             | Description               |
| ------------------ | ------------------------- |
| `concat(str, str)` | joins two or more strings |

- **Converting Case**

| Method          | Description                             |
| --------------- | --------------------------------------- |
| `toUpperCase()` | A string is converted to **upper** case |
| `toLowerCase()` | A string is converted to **lower** case |

- **Trimming & Padding**

| Method                  | Description                                         |
| ----------------------- | --------------------------------------------------- |
| `trim()`                | removes whitespace from both sides of a string      |
| `trimStart()`           | removes whitespace only from the start of a string. |
| `trimEnd()`             | removes whitespace only from the end of a string    |
| `padStart(length, str)` | pads a string with another string                   |
| `padEnd(length, str)`   | pads a string with another string                   |

- **Converting Data Type**

| Method             | Description                                 |
| ------------------ | ------------------------------------------- |
| `split(separator)` | splits a string into an array of substrings |
| `String.valueOf()` | convert a string object into a string       |

---

## Extracting Character

### Property Access, `charAt()`, `charCodeAt()`

```js
// charAt(), charCodeAt(), Property Access
console.log("\n--- Property Access, charAt(), charCodeAt() ---\n");

var text1 = "Microsoft";

console.log(text1[0]); //M
console.log(text1[1]); //i
console.log(text1[-1]); //undefined

console.log(text1.charAt(0)); //M
console.log(text1.charAt(1)); //i
console.log(text1.charAt(-1)); //""

console.log(text1.charCodeAt(0)); //77
console.log(text1.charCodeAt(1)); //105
console.log(text1.charCodeAt(-1)); //NaN
```

---

## Extracting Text

### `slice()`

```js
var text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// slice(start, [end])
// end: exclusive
console.log("\n--- slice(start, [end]) ---\n");

//slice out the rest of the string
console.log(text.slice(2)); //CDEFGHIJKLMNOPQRSTUVWXYZ
//If a parameter is negative, the position is counted from the end of the string.
console.log(text.slice(-2)); //YZ
console.log(text.slice(1, 2)); //B
console.log(text.slice(1, 3)); //BC
console.log(text.slice(-3, -1)); //XY
```

---

### `substring()`

- `substring()` is similar to slice().

- The difference is that start and end values less than 0 are treated as 0 in `substring()`.

```js
// substring(start, end)
console.log("\n--- substring(start, end) ---\n");

//substring out the rest of the string
console.log(text.substring(2)); //CDEFGHIJKLMNOPQRSTUVWXYZ
// substring cannot be negative
console.log(text.substring(-2)); //ABCDEFGHIJKLMNOPQRSTUVWXYZ
console.log(text.substring(1, 2)); //B
console.log(text.substring(1, 3)); //BC
// substring cannot be negative
console.log(text.substring(-3, -1)); //""
```

---

## Searching

### `includes()`

```js
// includes()
console.log("\n--- includes() ---\n");

// includes(searchvalue, start)
// Parameter    Description
// searchvalue  Required. The string to search for.
// start	      Optional. The position to start from. Default value is 0.
// Return       Description
// A boolean.	  strue if the string contains the value, otherwise false.

var text = "Please locate where 'locate' occurs!";

console.log(text.includes()); //false
console.log(text.includes("")); //true
console.log(text.includes("locate")); //true
console.log(text.includes("locate", 32)); //false
console.log(text.includes("Locate")); //false
```

---

### `startsWith()`

```js
// startsWith()
console.log("\n--- startsWith() ---\n");

// startsWith(searchValue, start)
// Parameter      Description
// searchValue    Required. The string to search for.
// start	        Optional. Start position. Default is 0.
// Return     Description
// A boolean	Returns true if the string starts with the value. Otherwise it returns false.

var text = "Please locate where 'locate' occurs!";

console.log(text.startsWith()); //false
console.log(text.startsWith("")); //true
console.log(text.startsWith("Please")); //true
console.log(text.startsWith("please")); //false
console.log(text.startsWith("locate", 7)); //true
```

---

### `endsWith()`

```js
// endsWith()
console.log("\n--- endsWith() ---\n");

// endsWith(searchvalue, length)
// Parameter	  Description
// searchvalue	Required. The string to search for.
// length	      Optional. The length of the string to search. Default value is the length of the string.
// Return       Description
// A boolean	  true if the string ends with the value, otherwise false.

var text = "Please locate where 'locate' occurs!";

console.log(text.endsWith()); //false
console.log(text.endsWith("")); //true
console.log(text.endsWith("occurs!")); //true
console.log(text.endsWith("occurS!")); //false
console.log(text.endsWith("locate", 13)); //true
console.log(text.endsWith("locate", 27)); //true
```

---

### `indexOf()`, `lastIndexOf()`

- returns the index (position) the first/last occurrence

```js
// indexOf(), lastIndexOf()
console.log("\n--- indexOf()---\n");

// indexOf(searchvalue, start)
// Parameter	  Description
// searchvalue  Required.The string to search for.
// start        Optional. The position to start from (default is 0).
// Return       Description
// A number	    The first position where the search-value occurs. -1 if it never occurs.

var text = "Please locate where 'locate' occurs!";
console.log(text.indexOf()); //-1
console.log(text.indexOf("")); //0
console.log(text.indexOf("locate")); //7
console.log(text.indexOf("locate", 8)); //21

console.log("\n--- lastIndexOf ---\n");

// lastIndexOf(searchvalue, start)
// Parameter	  Description
// searchvalue	Required. The string to search for.
// start	      Optional. The position where to start. Default value is string length.
// Return       Description
// A number	The position where the search-value occurs. -1 if it never occurs.

var text = "Please locate where 'locate' occurs!";
console.log(text.lastIndexOf()); //-1
console.log(text.length); //0
console.log(text.lastIndexOf("")); //36, the length of the string
console.log(text.lastIndexOf("locate")); //21
console.log(text.lastIndexOf("locate", 8)); //8
```

---

### `search()`

```js
// search()
console.log("\n--- search() ---\n");

// The search() method cannot take a second start position argument.
// The indexOf() method cannot take powerful search values (regular expressions).

// search(searchValue)
// Parameter    Description
// searchValue	Required. The search value. A regular expression (or a string that will be converted to a regular expression).
// Return       Description
// A number   	The position of the first match. -1 if no match.
var text = "Please locate where 'locate' occurs!";

console.log(text.search()); //0
console.log(text.search("locate")); //7
console.log(text.search("Locate")); //-1
console.log(text.search(/locate/)); //7
console.log(text.search(/Locate/)); //-1
console.log(text.search(/Locate/i)); //7
console.log(text.search(/locate/g)); //7
console.log(text.search(/Locate/g)); //-1
console.log(text.search(/Locate/gi)); //7
```

---

### `match()`

```js
// match()
console.log("\n--- match() ---\n");

// match(match)
// Parameter    Description
// match        Required. The search value. A regular expression (or a string that will be converted to a regular expression).
// Return             Description
// An array or null   An array containing the matches. null if no match is found.

// If a regular expression does not include the g modifier (global search), match() will return only the first match in the string.

var text = "Please locate where 'locate' occurs!";
console.log(text.match());
// [
//     '',
//     index: 0,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
console.log(text.match("locate"));
// [
//     'locate',
//     index: 7,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
console.log(text.match(/locate/));
// [
//     'locate',
//     index: 7,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
console.log(text.match(/locate/g)); //[ 'locate', 'locate' ]
console.log(text.match(/Locate/gi)); //[ 'locate', 'locate' ]
```

---

### `matchAll()`

```js
// matchAll()
console.log("\n--- matchAll() ---\n");

// matchAll(regexp)
// Parameter	Description
// regexp      Required. A regular expression object
// Return                Description
// An iterable object    An array containing the matches. null if no match is found.

var text = "Please locate where 'locate' occurs!";

console.log(text.matchAll("locate")); //Object [RegExp String Iterator] {}
console.log(Array.from(text.matchAll("locate")));
//[
// [
//     'locate',
//     index: 7,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ],
//   [
//     'locate',
//     index: 21,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
// ]
// If the parameter is a regular expression, the global flag (g) must be set, otherwise a TypeError is thrown.
console.log(Array.from(text.matchAll(/locate/g)));
// [
//     [
//       'locate',
//       index: 7,
//       input: "Please locate where 'locate' occurs!",
//       groups: undefined
//     ],
//     [
//       'locate',
//       index: 21,
//       input: "Please locate where 'locate' occurs!",
//       groups: undefined
//     ]
//   ]
```

---

## Replacing

### `replace()`

- The `replace()` method returns a new string, and does not change the string it is called on.

- By default, the `replace()` method replaces only **the first** match.

```js
// replace(matched, target)
console.log("\n--- replace(matched, target) ---\n");

var text = "Microsoft, Microsoft, Microsoft";

//replace the first matched
console.log(text.replace("Microsoft", "W3Schools")); //W3Schools, Microsoft, Microsoft
//replace the all matched
console.log(text.replace(/Microsoft/g, "W3Schools")); //W3Schools, W3Schools, W3Schools

//replace() method is case sensitive
console.log(text.replace("MICROSOFT", "W3Schools")); //Microsoft, Microsoft, Microsoft
// To replace case insensitive, use a regular expression with an /i flag (insensitive)
console.log(text.replace(/MICROSOFT/i, "W3Schools")); //W3Schools, Microsoft, Microsoft
console.log(text.replace(/MICROSOFT/gi, "W3Schools")); //W3Schools, W3Schools, W3Schools
```

---

### `replaceAll()`

```js
// replaceAll(matched, target)
// replaceAll() does not work in Internet Explorer.
console.log("\n--- replaceAll(matched, target) ---\n");

var text = "Microsoft, Microsoft, Microsoft";
//replace the all matched
console.log(text.replaceAll("Microsoft", "W3Schools")); //W3Schools, W3Schools, W3Schools
// If the parameter is a regular expression, the global flag (g) must be set set, otherwise a TypeError is thrown.
console.log(text.replaceAll(/MICROSOFT/gi, "W3Schools")); //W3Schools, W3Schools, W3Schools
// console.log(text.replaceAll(/MICROSOFT/i, "W3Schools")); //TypeError: String.prototype.replaceAll called with a non-global RegExp argument
```

---

## Concatenating

### `concat()`

```js
// concat([str])
console.log("\n--- concat([str]) ---\n");

var text1 = "Microsoft, Microsoft, Microsoft";
var text2 = "Google, Google, Google";
var text3 = "Apple, Apple, Apple";
console.log(text1.concat(text2, text3)); //Microsoft, Microsoft, MicrosoftGoogle, Google, GoogleApple, Apple, Apple
console.log(text1.concat(", ", text2, ", ", text3)); //Microsoft, Microsoft, Microsoft, Google, Google, Google, Apple, Apple, Apple
console.log(text1.concat(" ", text2)); //Microsoft, Microsoft, Microsoft Google, Google, Google
```

---

## Converting Case

### `toLowerCase()`, `toUpperCase()`

```js
// toLowerCase(), toUpperCase()
console.log("\n--- toLowerCase(), toUpperCase() ---\n");

var text = "Microsoft, Microsoft, Microsoft";
console.log(text.toLowerCase()); //microsoft, microsoft, microsoft
console.log(text.toUpperCase()); //MICROSOFT, MICROSOFT, MICROSOFT
```

---

## Trimming

### `trim()`, `trimStart()`, `trimEnd()`

```js
// trim(), trimStart(), trimEnd()
console.log("\n--- trim(), trimStart(), trimEnd() ---\n");

var text1 = "       Microsoft          ";

console.log(text1.trim() + ";"); //Microsoft;
console.log(text1.trimStart() + ";"); //Microsoft          ;
console.log(text1.trimEnd() + ";"); //       Microsoft;
```

---

## Padding

### `padStart()`, `padEnd()`

```js
// padStart(), padEnd()
console.log("\n--- padStart(), padEnd() ---\n");

var text1 = "Microsoft";

console.log(text1.padStart(5, "*")); //Microsoft;
console.log(text1.padStart(15, "*")); //******Microsoft
console.log(text1.padStart(15, "word")); //wordwoMicrosof
console.log(text1.padEnd(5, "*")); //Microsoft;
console.log(text1.padEnd(15, "*")); //Microsoft******
console.log(text1.padEnd(15, "word")); //Microsoftwordwo
```

---

## Converting Data Type

### `split()`: String to Array

```js
// split()
console.log("\n--- split() ---\n");

var text1 = "Microsoft,Google,Apple";

console.log(text1.split()); //[ 'Microsoft,Google,Apple' ]
console.log(text1.split("|")); //[ 'Microsoft,Google,Apple' ]
console.log(text1.split(",")); //[ 'Microsoft', 'Google', 'Apple' ]
// If the separator is "", the returned array will be an array of single characters:
console.log(text1.split(""));
//[
// 'M', 'i', 'c', 'r', 'o',
// 's', 'o', 'f', 't', ',',
// 'G', 'o', 'o', 'g', 'l',
// 'e', ',', 'A', 'p', 'p',
// 'l', 'e'
//   ]
```

---

### `valueOf()`: Object to String

```js
// valueOf()
console.log("\n--- valueOf() ---\n");

// valueOf()
// used to convert a string object into a string.
// Type	      Description
// A string	  The primitive value of the string.

var text = new String("Hello World!");
console.log(text.valueOf()); //Hello World!
```

---

[TOP](#javascript-string-method)
