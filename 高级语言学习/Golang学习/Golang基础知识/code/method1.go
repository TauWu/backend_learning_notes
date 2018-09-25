package main

import (
	"fmt"
)

type List []int

func (l List) Len() int        { return len(l) }
func (l *List) Append(val int) { *l = append(*l, val) }

func main() {
	// 值
	var lst List
	lst.Append(1)
	lst.Append(3)
	fmt.Printf("%v (len: %d)\n", lst, lst.Len()) // [1] (len: 1)

	// 指针
	plst := new(List)
	plst.Append(2)
	plst.Append(4)
	fmt.Printf("%v (len: %d)\n", plst, plst.Len()) // &[2] (len: 1)
}
