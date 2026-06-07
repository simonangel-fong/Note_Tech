# Go Maps

[Back](../index.md)

- [Go Maps](#go-maps)
  - [Maps](#maps)
    - [make() Function](#make-function)
  - [Map Elements](#map-elements)
  - [Check For Specific Elements in a Map](#check-for-specific-elements-in-a-map)
  - [Maps Are References](#maps-are-references)
  - [Iterate Over Maps](#iterate-over-maps)

---

## Maps

- `Maps` are used to store data values in `key:value` pairs.
- A map is an **unordered** and **changeable** collection that does not allow duplicates.
- The **length** of a map is the **number** of its elements.
  - the len() function.
- The **default value** of a map is `nil`.
- Maps hold references to an underlying `hash table`.
- Allowed Key Types
  - Booleans
  - Numbers
  - Strings
  - Arrays
  - Pointers
  - Structs
  - Interfaces (as long as the dynamic type supports equality)
- Invalid key types are:
  - Slices
  - Maps
  - Functions
- Allowed Value Types
  - The map values can be **any type**.

---

- Syntax

```go
var a = map[KeyType]ValueType{key1:value1, key2:value2,...}
b := map[KeyType]ValueType{key1:value1, key2:value2,...}

// empty map
var a map[KeyType]ValueType
```

- example

```go
package main

import (
	"fmt"
)

func main() {
	var a = map[string]string{"brand": "Ford", "model": "Mustang", "year": "1964"}
	b := map[string]int{"Oslo": 1, "Bergen": 2, "Trondheim": 3, "Stavanger": 4}

	fmt.Printf("a\t%v\n", a) // a       map[brand:Ford model:Mustang year:1964]
	fmt.Printf("b\t%v\n", b) // b       map[Bergen:2 Oslo:1 Stavanger:4 Trondheim:3]
}

```

- Example: empty map

```go
package main

import (
	"fmt"
)

func main() {
	var a = make(map[string]string)
	var b map[string]string

	fmt.Println(a == nil) // false
	fmt.Println(b == nil) // true
}

```

---

### make() Function

- Syntax

```go
var a = make(map[KeyType]ValueType)
b := make(map[KeyType]ValueType)
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	var a = make(map[string]string) // The map is empty now
	a["brand"] = "Ford"
	a["model"] = "Mustang"
	a["year"] = "1964"
	// a is no longer empty
	b := make(map[string]int)
	b["Oslo"] = 1
	b["Bergen"] = 2
	b["Trondheim"] = 3
	b["Stavanger"] = 4

	fmt.Printf("a\t%v\n", a) // a       map[brand:Ford model:Mustang year:1964]
	fmt.Printf("b\t%v\n", b) // b       map[Bergen:2 Oslo:1 Stavanger:4 Trondheim:3]
}

```

---

## Map Elements

```go
// access map elements
value = map_name[key]

// Updating or adding an elements are done by
map_name[key] = value

// Removing elements
delete(map_name, key)
```

---

## Check For Specific Elements in a Map

- syntax

```go
val, ok :=map_name[key]
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	var a = map[string]string{"brand": "Ford", "model": "Mustang", "year": "1964", "day": ""}

	val1, ok1 := a["brand"] // Checking for existing key and its value
	val2, ok2 := a["color"] // Checking for non-existing key and its value
	val3, ok3 := a["day"]   // Checking for existing key and its value
	_, ok4 := a["model"]    // Only checking for existing key and not its value

	fmt.Println(val1, ok1) // Ford true
	fmt.Println(val2, ok2) // false
	fmt.Println(val3, ok3) //  true
	fmt.Println(ok4)       // true
}

```

---

## Maps Are References

- Maps are references to `hash tables`.
- If two map variables refer to the same hash table, **changing** the content of one variable **affect** the content of the other.

```go
package main

import (
	"fmt"
)

func main() {
	var a = map[string]string{"brand": "Ford", "model": "Mustang", "year": "1964"}
	b := a

	fmt.Println(a) //map[brand:Ford model:Mustang year:1964]
	fmt.Println(b) //map[brand:Ford model:Mustang year:1964]

	b["year"] = "1970"
	fmt.Println("After change to b:")

	fmt.Println(a) //map[brand:Ford model:Mustang year:1970]
	fmt.Println(b) //map[brand:Ford model:Mustang year:1970]
}

```

---

## Iterate Over Maps

```go
package main

import (
	"fmt"
)

func main() {
	a := map[string]int{"one": 1, "two": 2, "three": 3, "four": 4}

	for k, v := range a {
		fmt.Printf("%v : %v, ", k, v)
		// one : 1, two : 2, three : 3, four : 4,
	}
}

```

---
