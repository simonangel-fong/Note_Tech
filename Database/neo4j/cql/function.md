# Cypher - Function

[Back](../index.md)

- [Cypher - Function](#cypher---function)
  - [Function](#function)
  - [Count()](#count)
  - [String Function](#string-function)

---

## Function

| Function  | Description              |
| --------- | ------------------------ |
| `count()` | count the number of rows |

---

## Count()

```cypher
// count the number of rows
MATCH (n { name: 'A' })-->(x)
RETURN n, count(*)

// Group COUNT
Match(n{name: "India", result: "Winners"})-[r]-(x)
RETURN type (r), count(*)
// return type and number of relationships
```

---

## String Function

| Function      | Description                                             |
| ------------- | ------------------------------------------------------- |
| `UPPER()`     | change all letters into upper case letters.             |
| `LOWER()`     | change all letters into lower case letters.             |
| `SUBSTRING()` | get substring of a given string.                        |
| `Replace()`   | replace a substring with a given substring of a string. |

---

[TOP](#cypher---function)
