package main

import (
	"fmt"
)

func main() {
	var (
		// 一般而言，\u 后面跟着长度为 4 的 Unicode 而 \U 后面跟着 长度为 8 的 Unicode 字符
		ch1 int = '\u0041'
		ch2 int = '\u03B2'
		ch3 int = '\U00101234'
	)

	fmt.Printf("%d - %d - %d\n", ch1, ch2, ch3) // integer
	fmt.Printf("%c - %c - %c\n", ch1, ch2, ch3) // character
	fmt.Printf("%X - %X - %X\n", ch1, ch2, ch3) // UTF-8 bytes
	fmt.Printf("%U - %U - %U\n", ch1, ch2, ch3) // UTF-8 code point
}
