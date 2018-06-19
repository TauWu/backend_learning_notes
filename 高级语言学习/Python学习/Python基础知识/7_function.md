# Function
## 函数

### 可接受任意数量参数的函数
如果想要构造一个可接受任意数量参数的函数，可以使用 * 参数来定义该函数：
```py
def avg(first, *others):
    return (first + sum(others)) / (1 + len(others))

print(avg(1,2))         # 1.5
print(avg(1,2,3,4,5))   # 3
```
为了接受任意数量的关键字参数，可以使用以 ** 开头的参数定义函数：
```py
def foo(attr1, attr2, **attrs):
    print(attr1, attr2, attrs)

foo(1, 2, n=1, m=2)     # 1 2 {'n':1,'m':2}
```
综上所述，\*args 和 \*\*kwargs 分别是第一章介绍的压缩和字典参数。要求 \*args 只能放在最后一个位置参数后面，\*\*kwargs 只能放在最后一个参数后面。

### 只接受关键字参数的函数
将强制关键字参数放到某个 * 参数或者单个 * 后面就能达到函数的某些参数强制使用关键字参数传递的效果。
```py
def recv(maxsize, *, block):
    pass

recv(1024, True)            # TypeError
recv(1024, block=True)      # Success
```
利用这个特性，可以达到以下的函数实现效果：
```py
def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

mininum(1, 2, 3, -4, 5)             # Return -4
mininum(1, 2, 3, -4, 5, clip=0)     # Return 0
```
这样使用的好处在于，如果函数调用者对本函数不是那么熟悉，直接传递前面几个参数并不会影响到他所想要的最终的结果的值。

### 给函数参数添加元信息
使用函数参数注解可以很好的提示程序员怎样正确的使用这个函数。例如：
```py
def add(x:int, y:int) -> int:
    return x+y
```
Python 解释器并不会对它有任何的语义，但是这种写法会对程序员较为友好（相当于静态语言）。函数注解存储在函数的 \_\_annotations\_\_ 属性中。注解的使用方法有很多（比如本方法或者注释说明），本处的作用主要还是文档。

### 返回多个值的函数
```py
def foo():
    return 1, 2

a, b = foo()
```

### 定义有默认参数的函数
```py
def foo(a, b=10):
    return a+b
foo(1)      # 11
foo(1,2)    # 3
```
这里需要注意的一点是，带有的默认参数，应当是常量的值而不应当是一个变量，以防止对默认参数的改变造成不必要的麻烦。

### 定义匿名或内联函数
将简单的单行函数用 lambda 表达式代替的手法，即为匿名函数：
```py
add = lambda x, y: x+y
add(2, 3)               # 5
add('hello', 'world')   # hello world
```
上述匿名函数的作用和下面的函数一致：
```py
def add(x, y):
    return x+y
```
lambda 表达式的典型使用场景是排序或者数据 reduce 等。

### 匿名函数捕捉变量值
**这里涉及到一个新手常跳的坑**，观察以下代码和结果：
```py
x = 10
a = lambda y: x+y
x = 20
b = lambda y: x+y
a(10)   # 30
b(10)   # 30
```
其中的原因是 x 在这里是一个自由变量，在运行的时候才会绑定值，因此返回的结果会随着 x 的改变而变化。如果想要匿名函数在定义的时候就捕获到值，可以参考以下写法：
```py
x = 10
a = lambda y, x=x: x+y
x = 20
b = lambda y, x=x: x+y
a(10)   # 20
b(10)   # 30
```

### 减少可调用对象的参数的个数
functools 中的 partial() 方法能固定某些参数并返回一个 callable 对象。这个新的 callable 对象接受未赋值的参数，然后根据之前已经赋值过的参数合并起来，最后将所有的参数一起传递给原始函数。
```py
from functools import partial

def spam(a, b, c, d):
    print(a, b, c, d)

s1 = partial(spam, 1)
s1(2, 3, 4)             # 1 2 3 4
s2 = partial(spam, d=42)
s2(1, 2, 3)             # 1 2 3 42
s3 = partial(spam, 1, 2, d=42)
s3(15)                  # 1 2 15 42
```
本函数功能主要是解决不兼容代码一起工作的问题，以下为示例：
- 1. 点序列到指定点的距离排序问题
```py
points = [
    (1, 2), (3, 4), (5, 6), (7, 8)
]

import math

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

pt = (4, 3)

points.sorted(key=partial(distance, pt))
print(points)
# [(3, 4), (1, 2), (5, 6), (7, 8)] 实现了距离 (4, 3) 点最近的升序排序
```
- 2. 微调其他库函数使用的回调函数的参数
```py
# 当给 apply_async() 提供回调函数时，通过使用 partial() 传递额外的 logging 参数。而 multiprocessing 模块对此一无所知。

def output_result(result, log=None):
    if log is not None:
        log.debug("Got:%r", result)

def add(x, y):
    return x + y

if __name__ == "__main__":
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    p = Pool()
    p.apply_async(add, (3, 4), callback=partial(output_result, log=log))
    p.close()
    p.join()
```

### 将单方法的类转换成函数
使用闭包将单方法的类转换为函数
```py
# 单方法的类写法
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.formate_map(kwargs))

# 闭包写法
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# 调用

test = UrlTemplate('http://www.test.com/s?date={date}&file={file}')
test = urlTemplate('http://www.test.com/s?date={date}&file={file}')

for line in test(date="2018", file="csv"):
    print(line.decode('utf-8'))
    
```

### 待额外状态信息的回调函数
如果代码中需要依赖到回调函数的使用（比如事件处理器、等待后台任务完成后的回调等），并且你还需要让回调函数拥有额外的状态值。
```py
def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

def print_result(result):
    print('Got:', result)

def add(x, y):
    return x + y

apply_async(add, ('Hello', 'World'), callback=print_result)
# Got: HelloWorld
```
为了让灰调函数访问到外部信息，通常使用的方法包括：绑定类的方法，使用闭包实现类的功能和使用协程。
- 1. 绑定类的方法替代简单函数
```py
class ResultHandler:

    def __init__(self):
        self.idx = 0

    def hander(self, result):
        self.idx += 1
        print('[{}] Got:{}'.format(self.idx, result))

r = ResultHandler()
apply_async(add, ('Hello', 'World'), callback=r.handler)
# [1] Got: HelloWorld
apply_async(add, (1, 2), callback=r.handler)
# [2] Got: 3
```
- 2. 使用闭包代替类
```py
def make_handler():
    idx = 0
    def handler(result):
        nonlocal idx            # nonlocal 声明本变量会被回调函数变更
        idx += 1
        print('[{}] Got:{}'.format(idx, result))
    return handler

handler = make_handler()
apply_async(add, ('Hello', 'World'), callback=handler)
# [1] Got: HelloWorld
apply_async(add, (1, 2), callback=handler)
# [2] Got: 3

```
- 3. 使用协程
```py
def make_handler():
    idx = 0
    while True:
        result = yield
        idx += 1
        print('[{}] Got:{}'.format(idx, result))

handler = make_handler()
next(handler)  # Advance to the yield
apply_async(add, ('Hello', 'World'), callback=handler.send)
# [1] Got: HelloWorld
apply_async(add, (1, 2), callback=handler.send)
# [2] Got: 3
```

### 内联回调函数
```py
from queue import Queue
from functools import wraps

def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def inlined_async(func):
    @warps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
        return wrapper

def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (1, 2))
    print(r)
    r = yield Async(add, ('Hello', 'World'))
    print(r)
    for n in range(3):
        r = yield Async(add, (n, n))
        print(r)
# 3
# HelloWorld
# 2
# 4
# 6
```
本例中使用生成器函数的主要原因是，生成器函数中出现的暂停与需要实现的中断操作其实是类似的。具体来说就是 yield 操作会使一个生成器函数产生一个值并暂停，接下来调用的 \_\_next\_\_() 或 send() 方法又会让它从暂停的地方继续执行。

### 访问闭包中定义的变量
```py
def sample():
    n = 0
    def func():
        print('n=', n)
    def get_n():
        return n
    def set_n():
        nonlocal n
        n = value

    func.get_n = get_n
    func.set_n = set_n
    return func

f = sample()
f()             # 0
f.set_n(10)
f()             # n= 10
f.get_n()       # 10
```