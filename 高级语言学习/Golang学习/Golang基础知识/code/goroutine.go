package main

import (
	"fmt"
	"time"
)

func main() {
	ch := make(chan int)

	go func() {
		ch <- 5
	}()

	go func() {
		fmt.Printf("******1 %v", <-ch)
		ch <- 20
	}()

	time.Sleep(1e9)
	fmt.Printf("*****2 %v", <-ch) // 这是在主线程中阻塞的，run until complete

	// <-ch	// This code will cause `deadlock`.
	// 构建具有缓冲区的 channel， 如果通道有缓冲区，则该通道为非阻塞通道。
	// value = 0 -> sync, unbuffered
	// value > 0 -> async, buffered
	buf := 100
	ch1 := make(chan string, buf)

	go func() {
		ch1 <- "test1"
		ch1 <- "test2"
	}()

	go func() {
		for {
			fmt.Printf("******3%s", <-ch1)
		}
	}()

	time.Sleep(1e9)

}
