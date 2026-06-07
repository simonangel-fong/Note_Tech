# Golang - Array

[Back](../index.md)

- [Golang - Array](#golang---array)
	- [Array](#array)
		- [Syntax](#syntax)
	- [Array Initialization](#array-initialization)
	- [Slices](#slices)
		- [Lab: Slice](#lab-slice)
		- [Access, Change, Append and Copy Slices](#access-change-append-and-copy-slices)
		- [`copy()` function](#copy-function)

---

## Array

- `Arrays`
  - used to store **multiple values** of the **same type** in a **single variable**, instead of declaring separate variables for each value.

---

### Syntax

- Define

```go
// declare with var
var array_name = [length]datatype{values}
// length is inferred
var array_name = [...]datatype{values}

// declare with :=
array_name := [length]datatype{values}
// here length is inferred
array_name := [...]datatype{values}
```

- Access Elements of an Array
  - indexes start at 0.

---

- Example

```go
package main

import (
	"fmt"
)

func main() {
	// declare
	var arr1 = [3]int{1, 2, 3}
	arr2 := [5]int{4, 5, 6, 7, 8}
	var cars = [4]string{"Volvo", "BMW", "Ford", "Mazda"}

	fmt.Println(arr1)
	// [1 2 3]
	fmt.Println(arr2)
	// [4 5 6 7 8]

	fmt.Print(cars)
	// [Volvo BMW Ford Mazda]

	// access
	fmt.Println(arr1[0])
	// 1
	fmt.Println(arr2[1])
	// 5
	fmt.Println(cars[2])
	// Ford

	// Change Elements
	cars[2] = "Toyota"
	fmt.Println(cars)
	// [Volvo BMW Toyota Mazda]
}

```

---

## Array Initialization

If an array or one of its elements has **not been initialized** in the code, it is assigned the **default value of its type**.

```go
package main

import (
	"fmt"
)

func main() {
	arr1 := [5]int{}              //not initialized
	fmt.Println(arr1)
	// [0 0 0 0 0]
	// get array len
	fmt.Println(len(arr1))
	// 5

    arr2 := [5]int{1, 2}          //partially initialized
	fmt.Println(arr2)
	// [1 2 0 0 0]
	arr3 := [5]int{1, 2, 3, 4, 5} //fully initialized
	fmt.Println(arr3)
	// [1 2 3 4 5]

	str1 := [3]string{}
	fmt.Println(str1)
	// [  ]
	str2 := [3]string{"aaa"}
	fmt.Println(str2)
	// [aaa  ]
	str3 := [3]string{"aaa", "bbb", "ccc"}
	fmt.Println(str3)
	// [aaa bbb ccc]

	arr4 := [5]int{1: 10, 2: 40}
	fmt.Println(arr4)
	// [0 10 40 0 0]


}

```

---

## Slices

- `slices`
  - used to store **multiple values** of the **same type** in a single variable.
  - the length of a slice can grow and shrink

- Syntax

```go
slice_name := []datatype{values}

// create a slice by slicing an array
var myarray = [length]datatype{values} // An array
myslice := myarray[start:end] // A slice made from the array, exclusive end

// create a slice with make function
slice_name := make([]type, length, capacity)
```

- functions
  - `len()`: returns the **length** of the slice (the number of elements in the slice)
  - `cap()`: returns the **capacity** of the slice (the number of elements the slice **can grow** or shrink to)

---

### Lab: Slice

```go
package main

import (
	"fmt"
)

func main() {
	myslice1 := []int{}
	fmt.Println(myslice1)
	// []
	fmt.Println(len(myslice1))
	// 0
	fmt.Println(cap(myslice1))
	// 0

	myslice2 := []string{"Go", "Slices", "Are", "Powerful"}
	fmt.Println(myslice2)
	// [Go Slices Are Powerful]
	fmt.Println(len(myslice2))
	// 4
	fmt.Println(cap(myslice2))
	// 4
}
```

- Create slice from array

```go
package main

import (
	"fmt"
)

func main() {
	// array
	arr1 := [6]int{10, 11, 12, 13, 14, 15}
	// slice
	myslice := arr1[2:4]

	fmt.Printf("myslice = %v\n", myslice)
	// myslice = [12 13]
	fmt.Printf("length = %d\n", len(myslice))
	// length = 2
	fmt.Printf("capacity = %d\n", cap(myslice))
	// capacity = 4
}
```

```go
package main

import (
	"fmt"
)

func main() {
	myslice1 := make([]int, 5, 10)
	fmt.Printf("myslice1 = %v\n", myslice1)      // myslice1 = [0 0 0 0 0]
	fmt.Printf("length = %d\n", len(myslice1))   // length = 5
	fmt.Printf("capacity = %d\n", cap(myslice1)) // capacity = 10

	// with omitted capacity
	myslice2 := make([]int, 5)
	fmt.Printf("myslice2 = %v\n", myslice2)      // myslice2 = [0 0 0 0 0]
	fmt.Printf("length = %d\n", len(myslice2))   // length = 5
	fmt.Printf("capacity = %d\n", cap(myslice2)) // capacity = 5
}

```

---

### Access, Change, Append and Copy Slices

```go
slice_name = append(slice_name, element1, element2, ...)
```

```go
package main

import (
	"fmt"
)

func main() {
	prices := []int{10, 20, 30}

	fmt.Println(prices[0]) // 10

	prices[2] = 50
	fmt.Println(prices[2]) // 50

	myslice1 := []int{1, 2, 3, 4, 5, 6}
	fmt.Printf("myslice1 = %v\n", myslice1)      // myslice1 = [1 2 3 4 5 6]
	fmt.Printf("length = %d\n", len(myslice1))   // length = 6
	fmt.Printf("capacity = %d\n", cap(myslice1)) // capacity = 6

	myslice1 = append(myslice1, 20, 21)
	fmt.Printf("myslice1 = %v\n", myslice1)      // myslice1 = [1 2 3 4 5 6 20 21]
	fmt.Printf("length = %d\n", len(myslice1))   // length = 8
	fmt.Printf("capacity = %d\n", cap(myslice1)) // capacity = 12

	myslice2 := []int{4, 5, 6}
	myslice3 := append(myslice1, myslice2...)
	fmt.Printf("myslice3=%v\n", myslice3)      // myslice3=[1 2 3 4 5 6 20 21 4 5 6]
	fmt.Printf("length=%d\n", len(myslice3))   // length=11
	fmt.Printf("capacity=%d\n", cap(myslice3)) // capacity=12
}

```

---

### `copy()` function

- The `copy()` function creates a new underlying array with **only the required elements** for the slice.
  - `copy(dest, src)`

```go
package main

import (
	"fmt"
)

func main() {
	numbers := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
	// Original slice
	fmt.Printf("numbers = %v\n", numbers)       // numbers = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15]
	fmt.Printf("length = %d\n", len(numbers))   // length = 15
	fmt.Printf("capacity = %d\n", cap(numbers)) // capacity = 15

	// Create copy with only needed numbers
	neededNumbers := numbers[:len(numbers)-10]
	fmt.Println(neededNumbers) // [1 2 3 4 5]

	// create empty slice
	numbersCopy := make([]int, len(neededNumbers))
	fmt.Println(numbersCopy) // [0 0 0 0 0]

	// copies data
	copy(numbersCopy, neededNumbers)
	fmt.Printf("numbersCopy = %v\n", numbersCopy)   // numbersCopy = [1 2 3 4 5]
	fmt.Printf("length = %d\n", len(numbersCopy))   // length = 5
	fmt.Printf("capacity = %d\n", cap(numbersCopy)) // capacity = 5
}

```
