package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

func request(x int) {
	tm := 1e4 * rand.Intn(10)
	time.Sleep(time.Duration(tm))
	fmt.Printf("request %v succeed. Wait: %v\n", x, tm)
}

func main() {
	m := 20
	var wg sync.WaitGroup

	for i := 0; i < m; i++ {
		wg.Add(1)
		go func(i int) {
			fmt.Println("inner i ...", i)
			request(i)
			wg.Done()
		}(i)
	}

	wg.Wait()

	fmt.Println("over")

}
