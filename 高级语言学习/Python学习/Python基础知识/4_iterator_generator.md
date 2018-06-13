# Iteration and Generator
## 迭代器和生成器

### 手动遍历迭代器
手动调用 *next()* 函数来遍历迭代器，并在代码中捕获 StopIteration 异常。
```py
def iter():
    with open('/etc/passwd') as f:
        try:
            while True:
                line = next(f)
                print(line, end="")
        except StopIteration:
            pass
```
通常来说，StopIteration 即作为迭代器的终点。不过在调用 *next()* 函数的时候，可以指定终点的标记如：
```py
line = next(f, None)
```

### 代理迭代
当你构建了一个自定义的容器对象，内部包含有列表等可迭代对象，如果你想直接在这个新的容器对象中执行迭代操作，实际的操作是定义一个 *\_\_iter\_\_()* 方法，将迭代操作代理到容器内部的对象上去。
```py
class Node:

    def __init__(self, value):
        self._value = value
        self._children = list()

    def __repr__(self):
        return 'Node => {!r}'.format(self._value)

    def add_child(self, node):
        self._child.append(node)

    def __iter__(self):
        return iter(self._children)    # 这里的 iter 采用的现成的迭代取值方法

if __name__ == "__main__":
    root = Node(0)
    c1 = Node(1)
    c2 = Node(3)
    root.add_child(c1)
    root.add_child(c2)
    for ch in root:
        print(ch)
```

### 使用生成器创建迭代
函数中带有 `yield` 的都是生成器，它的特征是它只会响应迭代操作中的 *next()* 操作。鉴于我们在正常使用中会使用for循环迭代，因此基本上不用担心迭代过程中出现的异常。

### 实现迭代器协议
构建一个支持迭代操作的自定义对象，最简单的办法是使用一个生成器函数。
```py
class Node:

    def __init__(self, value):
        self._value = value
        self._children = list()

    def __repr__(self):
        return 'Node => {!r}'.format(self._value)

    def add_child(self, node):
        self._child.append(node)

    def __iter__(self):
        return iter(self._children)    # 这里的 iter 采用的现成的迭代取值方法

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()
```

### 反向迭代
反向迭代一个序列，可以使用系统内置的 *reversed()* 函数。
```py
a = [1,2,3,4,5,6]
for x in reversed(a):
    print(x)
```
针对自定义的对象，如果对象的数量可以确定或者对象实现了 *\_\_reversed\_\_()* 的方法，则可以直接反向迭代。否则，必须要将该对象转换为 `list` 方可。这里需要注意的是 **如果可迭代对相关非常大，将会占用非常多的内存。**
<p></p>

通过 *\_\_reversed\_\_()* 的方法实现的方法：
```py
class CountDown:

    def __init__(self, start):
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1

# 本操作更节省内存
for rr in reversed(CountDown(10)):
    print(rr)

for rr in CountDown(10):
    print(rr)

```

### 带有外部状态的生成器函数
如果你想定义一个生成器函数，但是它会调用某个你想暴露给用户使用的外部状态值。具体做法是可以将它实现为一个类，然后把生成器函数放到 *\_\_iter()\_\_* 中去：
```py
from collections import deque

class linehistory:

    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()
```
为使用这个类，可以将它当做普通的生成器函数。然而由于可以创建一个实例对象，于是可以访问内部属性值，比如 `history` 属性或者 *`clear()`* 方法。使用代码如下：
```py
with open('README.MD') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')
```

### 迭代器切片
标准的切片操作不能进行一个由迭代器生成的切片对象，实际操作中可以使用 *itertools.islice()* 函数来针对迭代器或生成器的切片操作。
- 不能实现的做法：
```py
def count(n):
    while True:
        yield n
        n += 1

c = count(0)
print(c[10:20])

# >>> TypeError: 'generator' object is not subscriptable
```
- 正确实现的做法：
```py
import itertools
for x in itertools.islice(c, 10, 20):
    print(x)
```
迭代器和生成器因为不能确定长度，所以并不能执行标准的切片操作。函数 *islice()* 返回一个可以生成指定元素的迭代器，它通过遍历并丢弃直到切片开始索引的位置的指定数量的元素。**注意， *islice()* 函数会消耗迭代器中的数据，需要考虑迭代器的迭代不可逆**。如果需要再次访问，可以将其存放到列表中。

### 跳过可迭代对象的初始部分
使用 itertools 模块中的 *itertools.dropwhile()* 函数可以丢弃原有序列中函数返回 False 之前的所有元素，然后遍历后面的所有元素。
```py
from itertools import dropwhile

with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')
```
> 使用 *islice()* 和 *dropwhile()* 函数主要是为了避免冗余的代码。
> ```py
> with open ('/etc/passwd') as f:
>    while True:
>        line = next(f, '')
>        if not line.startwith('#'):
>             break
>```
如果需求是过滤 /etc/passwd 文件中的所有注释行，则该代码的写法如下：
```py
with open('/etc/passwd') as f:
    lines = (line for line in f if not line.startwith("#"))
    for line in lines:
        print(line, end='')
```

### 序列上的索引值迭代
内置的 *enumerate()* 函数可以用来同时跟踪索引值和元素。
```py
sample = ['a', 'b', 'c']
for idx, val in enumerate(sample, 0):   # 从 0 开始计数，0 为默认值可以不填
    print(idx, val)

# 0   a
# 1   b
# 2   c
```
使用 *enumerate()* 函数可以避免以下写法：
```py
sample = ['a', 'b', 'c']
idx = 0
for val in sample:
    print(idx, val)
    idx += 0
```
或者
```py
idx_list = [0, 1, 2]
for idx, val in zip(idx_list, sample):
    print(idx, val)
```

### 同时迭代多个序列
同时迭代多个序列，可以考虑使用 zip() 函数。 zip() 函数会生成一个可返回元组 (x,y) 的迭代器，一旦某个序列迭代到了尾部，则迭代宣告结束。
> 如果按照长的序列为迭代终点，可以使用 itertools.zip_longest() 方法来同时迭代。

### 不同集合上元素的迭代
使用 itertools.chain() 方法可以将两次迭代的操作简化。
```py
from itertools import chain
a = [1,2,3]
b = [6,7,8]
for x in chain(a, b):
    print(x)
# 1
# 2
# 3
# 6
# 7
# 8
```
对比以下写法：
```py
for x in a+b:
    print(x)
```
使用 chain() 一方面可以不限制 a 列表和 b 列表的类型一致，另一方面没有合并的操作将会节省内存占用。

### 创建数据处理管道
如果有大量数据需要处理但不能一次性将它放入到内存中，使用生成器函数便能实现管道机制。使用迭代器可以仅仅使用很小一部分的内存而且效率并不会有很大影响。

### 展开嵌套的序列
如果想将一个多层嵌套的序列展开成一个单层列表，可以写一个包含 yield from 语句的递归生成器来解决。如：
```py
from collections import Iterable

def flatten(items, ignore_type=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_type):
            yield from flatten(x)
        else:
            yield x

items = [1,2,3,[1,2,3,[1,2,3,[1,2,3]]]]

for x in flatten(items):
    print(x)                    # 打印结果是展开的序列  
```
ignore_type 主要是防止将可被迭代的类似字符串的类型继续迭代。 yield from 在协程和并发编程中会有更多的应用。

###　迭代器替代 while 实现无限循环
常见的死循环代码为：
```py
def foo():
    flag = True
    while flag:
        flag = func()
```
使用 iter() 函数代替的方案：
```py
def foo():
    for x in iter(lambda: func(), False):
        pass
```
iter 函数可以接受一个可选的 callable 对象和一个标记结尾作为输入参数。当以这种方式执行的时候，会创建一个迭代器，这个迭代器会不断调用 callable 对象直到返回值和标记值相等为止。本例中的 lambda 函数创建了一个无参的 callable 对象。