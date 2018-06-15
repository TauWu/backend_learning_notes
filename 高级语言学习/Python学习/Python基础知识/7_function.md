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
```

### 给函数参数添加元信息

### 返回多个值的函数

### 定义有默认参数的函数

### 定义匿名或内联函数

### 匿名函数捕捉变量值

### 减少可调用对象的参数的个数

### 将单方法的类转换成函数

### 待额外状态信息的回调函数

### 内联回调函数

### 访问闭包中定义的变量