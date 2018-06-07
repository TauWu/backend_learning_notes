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

# 自带排序方法 采用排序方式（堆排序）
from heapq import heapify, heappop
print(nums)
heapify(nums)
print(nums)     # 最小堆
print(heappop(nums))
print(heappop(nums))
print(heappop(nums))
print(heappop(nums))
# yield返回结果

# 实现一个优先级排序队列 - FIFO
# 这个队列的每次pop操作总是返回优先级最高的那个元素

import heapq

class PriorityQueue:

    def __init__(self):
        self._queue = list()
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Item:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item => {!r}'.format(self.name)     # !r format的引用模式

queue = PriorityQueue()
queue.push(Item('test1'), 1)
queue.push(Item('test2'), 5)
queue.push(Item('test3'), 2)
queue.push(Item('test4'), 3)
queue.push(Item('test5'), 1)
queue.push(Item(Item('test5')), 1)
queue.push(Item(6), 2)

while True:
    try:
        print(queue.pop())
    except Exception:
        break

# 字典的key映射多个值
from collections import defaultdict

pairs = zip(
    ['a','b','a','b'],[1,1,(2,3,3),4]
)

mutildict = defaultdict(list)
for k, v in pairs:
    mutildict[k].append(v)

print(mutildict)

# 有序字典
# 内部维系着另一个双向链表，使用的时候需要考虑空间占用
from collections import OrderedDict

d = OrderedDict()
d['Test1'] = '1'
d['Test2'] = 'a'
d['Test3'] = 'b'
for k in d:
    print(k, d[k])

import json
print(json.dumps(d))

# 字典运算
# 涉及到字典的键值反转

prices = {
    "Test1":1,
    "Test2":10,
    "Test3":5,
    "Test4":2    
}

price_tmp = zip(prices.values(), prices.keys())

# zip函数生成了一个迭代器，所以只能被函数调用一次，这里不能使用price_tmp
print(min(zip(prices.values(), prices.keys())))
print(max(zip(prices.values(), prices.keys())))

# 查找两个字典的相同点 - 数据的计算
prices1 = {
    "Test1":1,
    "Test2":1,
    "Test4":2    
}

print(prices.keys() & prices1.keys())
print(prices.keys() - prices1.keys())
print(prices.items() & prices1.items())

# 过滤字典值
print({
    key:prices[key] for key in prices.keys() - {'Test1'}
})

# 怎样在一个序列上面保持元素顺序的同时消除重复的值？
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

a = [1,2,3,4,5,12,1,1,1,2,21,2,3,5,12,3]
print(list(dedupe(a)))                  # list包裹下的迭代器可以直接变为列表

# 切片命名
s = slice(1,5)
print(a[s])
del a[s]
print(a)

# 获取序列中出现最多的元素
from collections import Counter
word_counter = Counter(a)
top = word_counter.most_common(3)
print(top)

# 通过某个关键字排序一个字典列表 类似于数据库的order by操作
rows = [
    {'fname':'Test1','lanme':'test1','uid':1},
    {'fname':'Test2','lanme':'test2','uid':4},
    {'fname':'Test3','lanme':'test3','uid':2},
    {'fname':'Test4','lanme':'test2','uid':3},
    {'fname':'Test5','lanme':'test5','uid':3}
]

print(sorted(
    rows, key=lambda r : (r['uid'], r['fname'])
))

# 排序不支持原生比较的对象
class User:

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        '''__repr__ 打印格式
        '''
        return 'User => {}'.format(self.user_id)

users = [
    User(1), User(12), User(21), User(13)
]
print(users)
print(sorted(users, key=lambda u:u.user_id))

# 过滤序列元素
# 1 - 列表推导式
raw_list = [1,3,4,1,3,2,-1,2,-21,23,-32]
print("RAW:", raw_list)
print("RAW > 0:", [n for n in raw_list if n > 0])
# 2 - 生成器表达式
iter = (n for n in raw_list if n > 0)
print([n for n in iter])
print(list(iter))           # 这里需要注意两点 1：iter已经迭代完了所以第二次应该是空列表，2：第一种相对来说比较省内存
# 3 - filter函数
def lagger_than_zero(val):
    if val > 0:
        return True
    else:
        return False
print(list(filter(lagger_than_zero, raw_list))) # filter函数构建出一个生成器，获得的结果需要用list获取数据。

# 字典中提取子集
raw_dict = {
    'Test1':1,
    'Test2':-1,
    'Test3':3,
    'Test4':-2
}
print({k:v for k,v in raw_dict.items() if v > 0})
raw_key_list = ['Test1', 'Test4']
print({k:v for k,v in raw_dict.items() if k not in raw_key_list})

# 生成器表达式
nums = [1,2,3,4,5]
print(sum(n*n for n in nums))
print(sum([n*n for n in nums]))
# 第一种方式不需要生成一个临时的list，更省内存

# 合并字典
a = dict(x=1,y=2)
b = dict(x=3,z=4)

# ChainMap合并
from collections import ChainMap
c = ChainMap(a,b)
print(c)
print(c['x'], c['y'], c['z'])

# update合并
b.update(a)
print(b)