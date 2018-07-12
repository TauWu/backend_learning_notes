package main

import "fmt"

type A struct {
	ax, ay int
	x      int
	y      int
}

type B struct {
	A
	bx, by float32
	x      int
	y      string
}

func main() {
	b := B{A{1, 2, 3, 4}, 5.0, 6.0, 7, "8"}
	fmt.Println(b.ax, b.ay, b.bx, b.by)
	fmt.Println(b.A)
	fmt.Println(b.x, b.y, b.A.x, b.A.y)
}
