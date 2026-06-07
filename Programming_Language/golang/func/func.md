# Golang - Function

[Back](../index.md)

- [Golang - Function](#golang---function)
  - [Function](#function)
  - [Output Functions](#output-functions)
    - [Formatting Verbs for `Printf()`](#formatting-verbs-for-printf)
    - [String Formatting Verbs](#string-formatting-verbs)
    - [Boolean Formatting Verbs](#boolean-formatting-verbs)
    - [Float Formatting Verbs](#float-formatting-verbs)

---

## Function

- `func <name>() <return_type>{}`

```go
func newCard() string {
    return "five of diamonds"
}

card := newCard()
```

---

## Output Functions

three functions to output text:

- `Print()`: prints its arguments with their default format.

```go
package main

import (
	"fmt"
)

func main() {
	var i, j string = "Hello", "World"

	fmt.Print(i, "\n")
	fmt.Print(j, "\n")
	// Hello
	// World

	fmt.Print(i, "\n", j)
	// Hello
	// World

	fmt.Print(i, " ", j)
	// Hello World

	var x, y = 10, 20
	fmt.Print(x, y)
	// 10 20
}

```

- `Println()`: whitespace is added between the arguments, and a newline is added at the end
- `Printf()`: formats its argument based on the given formatting verb and then prints them.

```go
package main

import (
	"fmt"
)

func main() {
	var i string = "Hello"
	var j int = 15

	fmt.Printf("i has value: %v and type: %T\n", i, i)
	fmt.Printf("j has value: %v and type: %T", j, j)
	// i has value: Hello and type: string
	// j has value: 15 and type: int
}

```

### Formatting Verbs for `Printf()`

- General Formatting Verbs

| Verb  | Description                            |
| ----- | -------------------------------------- |
| `%v`  | Prints the value in the default format |
| `%#v` | Prints the value in Go-syntax format   |
| `%T`  | Prints the type of the value           |
| `%%`  | Prints the % sign                      |

- Integer Formatting Verbs

| Verb   | Description                                |
| ------ | ------------------------------------------ |
| `%b`   | Base 2                                     |
| `%d`   | Base 10                                    |
| `%+d`  | Base 10 and always show sign               |
| `%o`   | Base 8                                     |
| `%O`   | Base 8, with leading 0o                    |
| `%x`   | Base 16, lowercase                         |
| `%X`   | Base 16, uppercase                         |
| `%#x`  | Base 16, with leading 0x                   |
| `%4d`  | Pad with spaces (width 4, right justified) |
| `%-4d` | Pad with spaces (width 4, left justified)  |
| `%04d` | Pad with zeroes (width 4)                  |

- example

```go
package main

import (
	"fmt"
)

func main() {
	var i = 15

	fmt.Printf("%b\n", i)   //1111
	fmt.Printf("%d\n", i)   // 15
	fmt.Printf("%+d\n", i)  // +15
	fmt.Printf("%o\n", i)   // 17
	fmt.Printf("%O\n", i)   // 0o17
	fmt.Printf("%x\n", i)   //f
	fmt.Printf("%X\n", i)   // F
	fmt.Printf("%#x\n", i)  // 0xf
	fmt.Printf("%4d\n", i)  //   15
	fmt.Printf("%-4d\n", i) // 15
	fmt.Printf("%04d\n", i) // 0015
}

```

---

### String Formatting Verbs

| Verb   | Description                                                 |
| ------ | ----------------------------------------------------------- |
| `%s`   | Prints the value as plain string                            |
| `%q`   | Prints the value as a double-quoted string                  |
| `%8s`  | Prints the value as plain string (width 8, right justified) |
| `%-8s` | Prints the value as plain string (width 8, left justified)  |
| `%x`   | Prints the value as hex dump of byte values                 |
| `% x`  | Prints the value as hex dump with spaces                    |

- Example

```go
package main

import (
	"fmt"
)

func main() {
	var txt = "Hello"

	fmt.Printf("%s\n", txt)   // Hello
	fmt.Printf("%q\n", txt)   // "Hello"
	fmt.Printf("%8s\n", txt)  //    Hello
	fmt.Printf("%-8s\n", txt) // Hello
	fmt.Printf("%x\n", txt)   // 48656c6c6f
	fmt.Printf("% x\n", txt)  // 48 65 6c 6c 6f
}

```

---

### Boolean Formatting Verbs

| Verb | Description                                                              |
| ---- | ------------------------------------------------------------------------ |
| `%t` | Value of the boolean operator in true or false format (same as using %v) |

- example

```go
package main

import (
	"fmt"
)

func main() {
	var i = true
	var j = false

	fmt.Printf("%t\n", i) // true
	fmt.Printf("%t\n", j) // false
}

```

---

### Float Formatting Verbs

| Verb    | Description                               |
| ------- | ----------------------------------------- |
| `%e`    | Scientific notation with 'e' as exponent  |
| `%f`    | Decimal point, no exponent                |
| `%.2f`  | Default width, precision 2                |
| `%6.2f` | Width 6, precision 2                      |
| `%g`    | Exponent as needed, only necessary digits |

- example

```go
package main

import (
	"fmt"
)

func main() {
	var i = 3.141

	fmt.Printf("%e\n", i)    // 3.141000e+00
	fmt.Printf("%f\n", i)    // 3.141000
	fmt.Printf("%.2f\n", i)  // 3.14
	fmt.Printf("%6.2f\n", i) //   3.14
	fmt.Printf("%g\n", i)    // 3.141
}

```
