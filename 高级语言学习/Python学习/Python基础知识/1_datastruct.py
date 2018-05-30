#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  
# DataStruct
# Chapter 1 from Python CookBook
#


# 赋值语句解压赋值
name, _, sex = ['Tau', 22, 'Male']
print(name, sex)

# 解压可迭代对象赋值给多个对象
# 解压赋值的可迭代对象数量多于变量数的解决方案
product, *price, num = ['Apple', 11, 12, 13, 14, 15, 100]
print(product, price, num)

# 上述迭代设计
# Python并不适合迭代调用，仅做演示
def sum(items):
    head, *tails = items
    return head + sum(tails) if tails else head

print(sum([1,2,3,4,5,6,7,8,9]))

# deque队列容器
from collections import deque

queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)
queue.appendleft(4)
print(queue)
queue.pop()
print(queue)
queue.popleft()
print(queue)

# 查找列表中最大/小的几个元素
from heapq import nlargest, nsmallest
nums = [1,31,41,21,2,3,4,5,4,3,2,3,4,6,4,2,32,5,33]
print(nlargest(4,nums), nsmallest(4,nums))

price_info = [
    {'name':'Apple1', 'price':10.1},
    {'name':'Apple2', 'price':12.9},
    {'name':'Apple3', 'price':13.6},
    {'name':'Apple4', 'price':14.2},
    {'name':'Apple5', 'price':12.0}
]

print(nsmallest(3, price_info, key=lambda s:s['price']))
print(nlargest(3, price_info, key=lambda s:s['price']))

# 自带排序方法
from heapq import heapify
heapify(nums)
print(nums)