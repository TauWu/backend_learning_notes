# 函数

## 18. 用数量可变的位置参数减少视觉杂讯

首先看第一段代码：

```py
def foo(message, values):
    if not values:
        print(message)
    else:
        print("%s: %s"%(message, ",".join([str(v) for v in values])))

foo("my numbers are", [1,2,3])
# my numbers are: 1,2,3

foo("no numbers.", [])
# no numbers.
```

可以看出，第二次不输入 values 时的调用不是很优雅，而由于之前定义过 foo 函数必须要传 values 这个参数，因此只能按照这样的调用方法。为了避免这样没有意义的空 list 传入，可以使用 * 星号参数来避免掉第二次调用的空 list。修改后的代码如下：

```py
def foo(message, *values):
    if not values:
        print(message)
    else:
        print("%s: %s"%(message, ",".join([str(v) for v in values])))

foo("my numbers are", 1, 2, 3)
# my numbers are: 1,2,3

foo("no numbers.")
# no numbers.
```

对比以上两段代码，函数的定义部分只是在后面的参数加了个 *，函数的调用部分，第一个去掉了外面的列表框，第二个直接省略了后面的空列表。如果有一个现成的 list 变量作为实参调用函数，可以在变量名前面加 * 解包。

```py
a = [1,2,3]
foo("my numbers are", *a)
# my numbers are: 1,2,3
```

接受位置可变的位置参数，会带来以下两个问题：

1. 当使用位置参数传递给函数的时候，Python 总是会把列表转换为元组，这就意味着，如果是用带有 * 操作符的生成器作为参数，Python 会先整个迭代器完整的迭代一轮，如果这个数据量非常大的话，可能会导致程序崩溃。如果下面的代码 range 里面的数字很大，可能就会跑满内存。

```py
def gen():
    for i in range(10):
        yield i

def foo(*args):
    print(args)

it = gen()
foo(*it)
# (0,1,2,3,4,5,6,7,8,9)
```

2. 如果以后要给 foo 函数添加新的参数，一定要检查每一个地方的调用，因为使用了位置参数的函数，对调用函数的实参数量将不再敏感，执行的时候也不会抛错，最终返回的结果很有可能会与预期的并不相同，这样会让 bug 难以追踪。

## 19. 用关键字参数表达可选的行为

像大多数开发语言一样，调用函数的时候，一般会按照形参的位置传递参数。不仅如此，Python 还支持按照关键字来传送参数。

```py
foo("my numbers are:", 1, 2, 3)
foo(message="no number.")
```

像第二种这样，以赋值的形式将参数传递给函数的行为称为按照关键字传送参数。这样调用函数的时候需要注意：

1. 实参的位置可以不按照形参的顺序
2. 可以混用位置参数和关键字参数，但是位置参数必须全部在关键字参数之前
3. 每个参数只能使用一次

```py
def foo(a, b, c):
    print(a, b, c)

foo(1, 2, 3)
foo(1, 2, c=3)
foo(a=1, b=2, c=3)
foo(a=1, 2, 3) # 错误写法
foo(1, a=1, b=2, c=3) # 错误写法
```

使用关键字参数带来的好处：

1. 使用关键词参数会让读者在调用端看到函数的形参名，代码可读性更强
2. 可以在函数中提供默认值，有些时候，调用者只需要提供部分必传参数，其他的参数可以直接使用默认值即可，简化了很多代码
3. 相对于上一条中提供的扩展方法，可以在函数定义之后面对新的需求的时候传递新的参数，大大提升代码健壮性，可以举个例子：

```py
def foo(a, b, c, d="default"):
    print(a, b, c, d)

foo(1, 2, 3)    # 之前使用本函数的地方依然有效，会在使用 d 的地方用到默认值
foo(1, 2, 3, "test") # 会用 test 覆盖掉默认值，虽然这里可以传 int 类型的 4，但是为了避免读者产生不好的习惯，因此传的字符串
```

## 20. 使用 None 和文档字符串来描述具有动态默认值的参数

来看下面一段代码：

```py
def foo(message, when=datetime.now()):
    print("%s: %s" % (when, message))

foo("Hi!")
time.sleep(1)
foo("Hi again!")

# 2019-9-26 00:20:58.000000: Hi!
# 2019-9-26 00:20:58.000000: Hi again!
```

返回的结果跟预期却不一样，在程序 sleep 一秒以后，两次打印的时间确是一样的，这是因为，when=datetime.now() 只在函数定义的时候执行了一次，函数里面参数的默认值，会在 **模块加载的时候运行一次** 后固定。后面的值就固定不变了。想要达到预期效果，需要这样修改代码：


```py
def foo(message, when=None):
    when = datetime.now() if when is None else when
    print("%s: %s" % (when, message))

foo("Hi!")
time.sleep(1)
foo("Hi again!")

# 2019-9-26 00:20:58.000000: Hi!
# 2019-9-26 00:20:59.000000: Hi again!
```

再举一个比较经典的例子：

```py
def decode_1(data, default={}):
    try:
        return json.loads(data)
    except Exception:
        return default

data1 = decode_1("test")
data1["test"] = 1
data2 = decode_1("newtest")
data2["newtest"] = 2

print(data1)
print(data2)
# {"test":1, "newtest":2}
# {"test":1, "newtest":2}
```

默认值只会在加载模块的时候定义一次，所以最终导致的结果是所有以默认形式调用 decode_1 函数的代码都享用同一个 default 的字典，因此最终的值被篡改成意想不到的数值。

如果需要修改，可以参考以下写法：

```py
def decode(data, default=None):
    default = {} if default is None else default
    try:
        return json.loads(data)
    except Exception:
        return default
```

这个地方也有涉及到局部变量的作用域的问题。不仅是字典，列表也会出现同样的问题。因此对于以动态值作为实际默认值的关键字参数，应该把形式上的参数默认值改为 None，并在函数的文档字符串（注释）中描述该默认值对应的实际行为，并在函数体中对它赋值。
