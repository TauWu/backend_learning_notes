package main

import (
	"fmt"
)

func defer1() error {
	err := fmt.Errorf("ERROR out1")

	defer func() {
		err = fmt.Errorf("ERROR defer1")
	}()

	err = fmt.Errorf("ERROR func1")
	return err
}

func defer2() (err error) {

	defer func() {
		err = fmt.Errorf("ERROR defer2")
		fmt.Println("debug", err)
	}()
	err = fmt.Errorf("ERROR func2")

	return err
}

func defer3() error {
	var (
		err error
	)

	defer func() {
		err = fmt.Errorf("ERROR defer3")
	}()

	err = fmt.Errorf("ERROR func3")
	return err

}

func main() {

	fmt.Println(defer1()) // ERROR func1
	fmt.Println(defer2()) // ERROR defer2
	fmt.Println(defer3()) // ERROR func3

}
