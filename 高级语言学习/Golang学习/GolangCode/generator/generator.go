package main

import "fmt"

func GeneratorClosure() func() (ret int) {
	a := 0
	return func() (ret int) {
		a += 1
		ret = a
		return
	}
}

func GeneratorChan(n int) chan int {
	ret := make(chan int)

	go func() {
		a := 1
		for i := 0; i < n; i++ {
			ret <- a
			a = a + 1
		}
		close(ret)
	}()

	return ret
}

func main() {
	// closure
	next := GeneratorClosure()

	for i := 0; i < 20; i++ {
		fmt.Println(next())
	}

	//channel
	for i := range GeneratorChan(20) {
		fmt.Println(i)
	}

}
