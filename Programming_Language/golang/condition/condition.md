# Golang - Condition

[Back](../index.md)

- [Golang - Condition](#golang---condition)
  - [`if` Statement](#if-statement)
  - [`if else` Statement](#if-else-statement)
  - [`else if` Statement](#else-if-statement)
  - [Nested `if` Statement](#nested-if-statement)
  - [`switch` Statement](#switch-statement)
  - [Multi-case `switch` Statement](#multi-case-switch-statement)

---

## `if` Statement

- Syntax

```go
if condition {
  // code to be executed if condition is true
}
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	x := 20
	y := 18
	if x > y {
		fmt.Println("x is greater than y") //x is greater than y
	}
}

```

---

## `if else` Statement

- syntax

```go
if condition {
  // code to be executed if condition is true
} else {
  // code to be executed if condition is false
}
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	temperature := 14
	if temperature > 15 {
		fmt.Println("It is warm out there")
	} else {
		fmt.Println("It is cold out there") // It is cold out there
	}
}

```

---

## `else if` Statement

- Syntax

```go
if condition1 {
   // code to be executed if condition1 is true
} else if condition2 {
   // code to be executed if condition1 is false and condition2 is true
} else {
   // code to be executed if condition1 and condition2 are both false
}
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	a := 14
	b := 14
	if a < b {
		fmt.Println("a is less than b.")
	} else if a > b {
		fmt.Println("a is more than b.")
	} else {
		fmt.Println("a and b are equal.") // a and b are equal.
	}
}

```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	x := 30
	if x >= 10 {
		fmt.Println("x is larger than or equal to 10.") // x is larger than or equal to 10.
	} else if x > 20 {
		fmt.Println("x is larger than 20.")
	} else {
		fmt.Println("x is less than 10.")
	}
}

```

---

## Nested `if` Statement

- Syntax

```go
if condition1 {
   // code to be executed if condition1 is true
  if condition2 {
     // code to be executed if both condition1 and condition2 are true
  }
}
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	num := 20
	if num >= 10 {
		fmt.Println("Num is more than 10.") // Num is more than 10.
		if num > 15 {
			fmt.Println("Num is also more than 15.") // Num is also more than 15.
		}
	} else {
		fmt.Println("Num is less than 10.")
	}
}

```

---

## `switch` Statement

- Syntax

```go
switch expression {
case x:
   // code block
case y:
   // code block
case z:
...
default:
   // code block
}
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	day := 4

	switch day {
	case 1:
		fmt.Println("Monday")
	case 2:
		fmt.Println("Tuesday")
	case 3:
		fmt.Println("Wednesday")
	case 4:
		fmt.Println("Thursday") // Thursday
	case 5:
		fmt.Println("Friday")
	case 6:
		fmt.Println("Saturday")
	case 7:
		fmt.Println("Sunday")
	}
}

```

---

## Multi-case `switch` Statement

- Syntax

```go
switch expression {
case x,y:
   // code block if expression is evaluated to x or y
case v,w:
   // code block if expression is evaluated to v or w
case z:
...
default:
   // code block if expression is not found in any cases
}
```

- Example

```go
package main

import (
	"fmt"
)

func main() {
	day := 5

	switch day {
	case 1, 3, 5:
		fmt.Println("Odd weekday") // Odd weekday
	case 2, 4:
		fmt.Println("Even weekday")
	case 6, 7:
		fmt.Println("Weekend")
	default:
		fmt.Println("Invalid day of day number")
	}
}

```
