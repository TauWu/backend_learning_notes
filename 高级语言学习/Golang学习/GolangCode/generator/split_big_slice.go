package main

import "fmt"

const N = 3

func GeneratorShortList(bigSlice []int) chan []int {
	ret := make(chan []int)

	go func() {
		for i := 0; i < len(bigSlice); i += N {
			if i+N < len(bigSlice) {
				ret <- bigSlice[i : i+N]
			} else {
				ret <- bigSlice[i : len(bigSlice)-1]
			}
		}
		close(ret)
	}()

	return ret
}

func main() {
	longList := []int{1, 2, 1, 2, 1, 3, 2, 43, 1, 2, 2, 1, 3, 1, 2, 4, 2}
	for i := range GeneratorShortList(longList) {
		fmt.Println(i)
	}
}
