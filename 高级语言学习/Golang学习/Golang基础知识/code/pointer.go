package main

import (
	"fmt"
)

func main() {
	var (
		i  int = 5
		p  *int
		p1 **int
	)
	fmt.Printf("The Address: %p\n", &i)
	p = &i
	p1 = &p
	fmt.Printf("The Value: %d The Address: %p The Address: %p\n", *p, p, &p)
	fmt.Println(**p1) // 二级指针
}
