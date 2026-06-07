# Golang - Function

[Back](../index.md)

- [Golang - Function](#golang---function)
	- [Function](#function)
	- [Recursion Functions](#recursion-functions)

---

## Function

- a **block of statements** that can be **used repeatedly** in a program.
- be executed only by a call to the function

- Syntax

```go
func <name>(param1 type, param2 type, param3 type) type {
  // code to be executed
  return output
}
```

- Example

```go
package main

import (
	"fmt"
)

func myFunction(x int, y int) (result int) {
	result = x + y
	return
}

func main() {
	fmt.Println(myFunction(1, 2)) // 3
}

```

---

## Recursion Functions

A function is **recursive** if it **calls itself** and reaches a stop condition.

- example

```go
package main

import (
	"fmt"
)

func testcount(x int) int {
	if x == 11 {
		return 0
	}
	fmt.Println(x)
	return testcount(x + 1)
}

func main() {
	testcount(1)
	// 1
	// 2
	// 3
	// 4
	// 5
	// 6
	// 7
	// 8
	// 9
	// 10
}

```

- example 2

```go
package main

import (
	"fmt"
)

func factorial_recursion(x float64) (y float64) {
	if x > 0 {
		y = x * factorial_recursion(x-1)
	} else {
		y = 1
	}
	return
}

func main() {
	fmt.Println(factorial_recursion(4)) // 24
}

```

---
