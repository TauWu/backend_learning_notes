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


### 将单方法的类转换成函数

### 待额外状态信息的回调函数

### 内联回调函数

### 访问闭包中定义的变量