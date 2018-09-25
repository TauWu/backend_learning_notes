package main

import "fmt"

func f() (ret int) {
	defer func() {
		ret++
	}()
	// defer 会在函数执行完之前 或者 return 执行完之后执行。
	return 1
}
func main() {
	fmt.Println(f())
}
