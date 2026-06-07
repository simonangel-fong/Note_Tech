package main

import (
	"fmt"
)

func main() {
	var i, j int

	fmt.Print("Type two numbers: ")
	fmt.Scan(&i, &j)
	fmt.Println("Your numbers are:", i, "and", j)
	// Type two numbers: 43
	// 434
	// Your numbers are: 43 and 434
}
