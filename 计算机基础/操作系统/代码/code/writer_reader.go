// Work On Linux: go build -o writer_reader.x -ldflags "-s -w" writer_reader.go && ./writer_reader.x
package main

import (
	"time"
	"fmt"
)

// 上锁
func pMutex(mutex *int64) (*int64, error){
	var(
		err error
	)
	if *mutex != 0{
		*mutex = 0
		return mutex, nil
	}else{
		err = fmt.Errorf("操作已被锁定！")
		return mutex, err
	}
}

// 释放锁
func vMutex(mutex *int64) (*int64, error){
	var(
		err error
	)
	if *mutex != 1{
		*mutex = 1
		return mutex, nil
	}else{
		err = fmt.Errorf("锁定已被解除！")
		return mutex, err
	}
}

// 写操作
func Write(writeMutex *int64)(*int64, error){
	var(err error)
	if writeMutex, err = pMutex(writeMutex); err!= nil{
		return writeMutex, err
	}else{
		fmt.Println("*****开始进行写操作！")
		time.Sleep(time.Second)
		if writeMutex, err = vMutex(writeMutex); err != nil{
			return writeMutex, err
		}
	}
	return writeMutex, nil
}

type ReadMutex struct{
	WriteMutex *int64
	CountMutex *int64
	RCount *int64
}

// 读操作（读者优先）
func Read(readMutex *ReadMutex) (*ReadMutex, error){
	var(
		err error
	)
	
	// 读者阅读前判断
	// 上锁修改写状态
	if readMutex.WriteMutex, err = pMutex(readMutex.WriteMutex); err != nil{
		goto END
	}
	fmt.Println("写上锁成功！")
	// 上锁修改Count状态
	if readMutex.CountMutex, err = pMutex(readMutex.CountMutex); err!= nil{
		goto END
	}
	fmt.Println("计数上锁成功！")
	
	fmt.Println("读者计数互斥修改开始～")
	if *readMutex.RCount == 0{
		*readMutex.RCount ++
		fmt.Println("读者计数互斥修改结束～")
	}else{
		err = fmt.Errorf("读者计数互斥修改失败！")
		goto END
	}

	if readMutex.CountMutex, err = vMutex(readMutex.CountMutex); err!= nil{
		goto END
	}
	fmt.Println("计数释放锁成功！")

	fmt.Println("*****读者阅读开始～")
	time.Sleep(time.Second)
	fmt.Println("*****读者阅读结束～")

	// 上锁修改Count状态
	if readMutex.CountMutex, err = pMutex(readMutex.CountMutex); err!= nil{
		goto END
	}
	fmt.Println("计数上锁成功！")
	
	fmt.Println("读者计数互斥修改开始～")
	if *readMutex.RCount != 0{
		*readMutex.RCount --
		fmt.Println("读者计数互斥修改结束～")
	}else{
		err = fmt.Errorf("读者计数互斥修改失败！")
		goto END
	}

	if readMutex.CountMutex, err = vMutex(readMutex.CountMutex); err!= nil{
		goto END
	}
	fmt.Println("计数释放锁成功！")

	if readMutex.WriteMutex, err = vMutex(readMutex.WriteMutex); err != nil{
		goto END
	}
	fmt.Println("写释放锁成功！")

END:
	return readMutex, err
}

func main(){
	var (
		err error
	)
	writeMutex := new(int64)
	countMutex := new(int64)
	rCount := new(int64)
	readMutex := &ReadMutex{
		WriteMutex: writeMutex,
		CountMutex: countMutex,
		RCount:rCount,
	}

	*writeMutex= 1
	*countMutex = 1
	*rCount = 0

	writeMutex, err = Write(writeMutex)
	if err != nil{
		goto FAILED
	}
	fmt.Println("*****写操作完成！")

	fmt.Println("读操作开始！")
	readMutex,err = Read(readMutex)
	if err != nil{
		goto FAILED
	}
	fmt.Printf("读操作完成！ %+v \n", *readMutex.CountMutex)

	return

FAILED:
	fmt.Println("发生错误！", err)
}