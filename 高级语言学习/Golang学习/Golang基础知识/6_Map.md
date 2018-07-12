# Map

## 概念
map 是引用类型，声明的方式一般如下：

```go
var map1 map[string]int
cap := 20   // 容量 20
map2 := make(map[string][]int, cap)
```

## k-v 操作

- 判断键值对是否存在
```go
// 因为 Go 中的 key 不存在的情况下返回的 value 会是零值
if _, ok := map1[key1];ok {
    // 存在
}
```
- 删除一个键值对
```go

delete(map1, key1)
// 如果 key 不存在也不会报错
```
相对于 Python 中的字典，Go 中对 Map 数据类型的操作显得更为友好。

## 遍历 Map
```go
for idx, val := range map1 {

}
```