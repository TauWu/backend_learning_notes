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