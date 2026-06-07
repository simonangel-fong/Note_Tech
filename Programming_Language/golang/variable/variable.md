# Golang - Variable

[Back](../index.md)

- [Golang - Variable](#golang---variable)
	- [Variable](#variable)
		- [Types](#types)
	- [Declaring (Creating) Variables](#declaring-creating-variables)
		- [Lab: Variable Declaration With Initial Value](#lab-variable-declaration-with-initial-value)
		- [Lab: Variable Declaration Without Initial Value](#lab-variable-declaration-without-initial-value)
		- [Lab: Value Assignment After Declaration](#lab-value-assignment-after-declaration)
		- [Lab: `var` vs `:=`](#lab-var-vs-)
		- [Lab: Multiple Variable Declaration](#lab-multiple-variable-declaration)
		- [Lab: Go Variable Declaration in a Block](#lab-go-variable-declaration-in-a-block)
	- [Constants](#constants)

---

## Variable

- `Variables`
  - containers for storing data values.

- Naming Rules
  - A variable name must **start with** a _letter_ or an _underscore character (\_)_
  - A variable name **cannot start with** a _digit_
  - A variable name can only contain _alpha-numeric characters_ and _underscores (a-z, A-Z, 0-9, and \_ )_
  - Variable names are **case-sensitive** (age, Age and AGE are three different variables)
  - There is **no limit on the length** of the variable name
  - A variable name cannot contain spaces
  - The variable name cannot be any Go keywords
- Naming techniques
  - Camel Case: `myVariableName = "John"`
  - Pascal Case: `MyVariableName = "John"`
  - Snake Case: `my_variable_name = "John"`

---

### Types

| Go Type Class | Common Type      | Example Declaration        | Zero Value (Default)    |
| ------------- | ---------------- | -------------------------- | ----------------------- |
| Textual       | `string`         | `var msg string`           | "" (Empty string)       |
| Numeric       | `int`            | `var count int`            | 0                       |
| Numeric       | `float64`        | `var price float64`        | 0.0                     |
| Boolean       | `bool`           | `var is_checked bool`      | false                   |
| Composite     | `struct`         | `var user UserStruct`      | All inner fields zeroed |
| Reference     | `[]int (Slice)`  | `var nums []int`           | nil                     |
| Reference     | `map[string]int` | `var cache map[string]int` | nil                     |

---

## Declaring (Creating) Variables

- `var` keyword
  - `var variablename type = value`

- `:=` sign
  - `variablename := value`
  - `Type inference`
    - the **type** of the variable is **inferred from the value**
    - the **compiler decides** the type of the variable, based on the value.

- `var` vs `:=`

| var                                                              | :=                                                                                                  |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Can be used inside and outside of functions                      | Can only be used inside functions                                                                   |
| Variable declaration and value assignment can be done separately | Variable declaration and value assignment cannot be done separately (must be done in the same line) |

---

### Lab: Variable Declaration With Initial Value

```go
package main

import (
	"fmt"
)

func main() {
	var student1 string = "John" //type is string
	var student2 = "Jane"        //type is inferred
	x := 2                       //type is inferred

	fmt.Println(student1) // John
	fmt.Println(student2) // Jane
	fmt.Println(x)        // 2
}
```

---

### Lab: Variable Declaration Without Initial Value

```go
package main

import (
	"fmt"
)

func main() {
	var a string
	var b int
	var c bool

	fmt.Println(a) //
	fmt.Println(b) // 0
	fmt.Println(c) // false
}

```

---

### Lab: Value Assignment After Declaration

```go
package main

import (
	"fmt"
)

func main() {
	var student1 string
	student1 = "John"

	fmt.Println(student1) // John
}

```

---

### Lab: `var` vs `:=`

```go
package main

import (
	"fmt"
)

var a int     // declare without value
var b int = 2 // declare with value
var c = 3

func main() {
	a = 1 // assign value

	fmt.Println(a) // 1
	fmt.Println(b) // 2
	fmt.Println(c) // 3
}
```

---

### Lab: Multiple Variable Declaration

```go
package main

import (
	"fmt"
)

func main() {
	var a, b, c, d int = 1, 3, 5, 7

	fmt.Println(a) // 1
	fmt.Println(b) // 3
	fmt.Println(c) // 5
	fmt.Println(d) // 7

	var e, f = 6, "Hello"
	g, h := 7, "World!"

	fmt.Println(e) // 6
	fmt.Println(f) // Hello
	fmt.Println(g) // 7
	fmt.Println(h) // World!
}

```

---

### Lab: Go Variable Declaration in a Block

```go
package main

import (
	"fmt"
)

func main() {
	var (
		a int
		b int    = 1
		c string = "hello"
	)

	fmt.Println(a) // 0
	fmt.Println(b) // 1
	fmt.Println(c) // hello
}

```

---

## Constants

