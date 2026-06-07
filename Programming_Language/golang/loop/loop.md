# Golang - Loop

[Back](../index.md)

- [Golang - Loop](#golang---loop)
	- [`for` Loop](#for-loop)
	- [`continue` Statement](#continue-statement)
	- [`break` statement](#break-statement)
	- [Nested Loops](#nested-loops)
	- [Range Keyword](#range-keyword)

---

## `for` Loop

- Syntax

```go
for statement1; statement2; statement3 {
   // code to be executed for each iteration
}
```

- **statement1**: Initializes the loop **counter value**.
- **statement2**: Evaluated for each loop iteration. If it evaluates to `TRUE`, the loop **continues**. If it evaluates to `FALSE`, the loop `ends`.
- **statement3**: Increases the loop **counter value**.

- Example

```go
package main

import (
	"fmt"
)

func main() {
	for i := 0; i <= 100; i += 10 {
		fmt.Println(i)
		// 0
		// 10
		// 20
		// 30
		// 40
		// 50
		// 60
		// 70
		// 80
		// 90
		// 100
	}
}

```

---

## `continue` Statement

- used to **skip** one or more iterations in the loop.
- then con**tinues with the next** iteration in the loop.

```go
package main

import (
	"fmt"
)

func main() {
	for i := 0; i < 5; i++ {
		if i == 3 {
			continue
		}
		fmt.Println(i)
		// 0
		// 1
		// 2
		// 4
	}
}

```

## `break` statement

- used to **terminate** the loop execution.

```go
package main

import (
	"fmt"
)

func main() {
	for i := 0; i < 5; i++ {
		if i == 3 {
			break
		}
		fmt.Println(i)
		// 0
		// 1
		// 2
	}
}

```

## Nested Loops

```go
package main

import (
	"fmt"
)

func main() {
	adj := [2]string{"big", "tasty"}
	fruits := [3]string{"apple", "orange", "banana"}

	for i := 0; i < len(adj); i++ {
		for j := 0; j < len(fruits); j++ {
			fmt.Println(adj[i], fruits[j])
			// big apple
			// big orange
			// big banana
			// tasty apple
			// tasty orange
			// tasty banana
		}
	}
}

```

---

## Range Keyword

- `range` keyword is used to **iterate through the elements** of an `array`, `slice` or `map`.
- It returns both the **index** and the **value**.

- Syntax

```go
for index, value := range array|slice|map {
   // code to be executed for each iteration
}
```

- example

```go
package main

import (
	"fmt"
)

func main() {
	fruits := [3]string{"apple", "orange", "banana"}

	for idx, val := range fruits {
		fmt.Printf("%v\t%v\n", idx, val)
		// 0       apple
		// 1       orange
		// 2       banana
	}
}

```
