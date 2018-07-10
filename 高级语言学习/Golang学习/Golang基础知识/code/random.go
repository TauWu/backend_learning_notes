package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {

	// 生成 10 个伪随机数
	for i := 0; i < 10; i++ {
		a := rand.Int()
		fmt.Printf("%d,", a)
	}

	fmt.Println("\n******\n")

	// 生成 10 个伪随机数
	for i := 0; i < 10; i++ {
		a := rand.Intn(8)
		fmt.Printf("%d,", a)
	}

	fmt.Println("\n******\n")

	// 利用时间纳秒作为种子生成随机数
	timens := int64(time.Now().Nanosecond())
	rand.Seed(timens)
	for i := 0; i <= 10; i++ {
		fmt.Printf("%2.f, ", 100*rand.Float32())
	}
}
