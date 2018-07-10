package main

import (
	"fmt"
)

func main() {
	var (
		aList [5]int
		bList = []int{1, 2}
		cList = []int{1: 1, 4: 2}
		dList = new([]int)
	)
	fmt.Println(aList, bList, cList, dList)
	dList = &cList
	fmt.Println(*dList)
	ChangeListValue(cList)
	fmt.Println(cList, dList)
	ChangeListValueP(dList)
	fmt.Println(cList, dList)
}

func ChangeListValue(list []int) {
	list[0] = 10
}

func ChangeListValueP(list *[]int) {
	(*list)[0] = 20
}
