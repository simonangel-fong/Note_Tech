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
