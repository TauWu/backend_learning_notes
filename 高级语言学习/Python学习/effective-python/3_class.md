# 类与继承

作为一门面向对象的编程语言，Python 提供了多态、继承、封装等各种面向对象的特性。

## 22. 尽量用辅助类来维护程序的状态，而不要用字典和元组

尽管 Python 的 dict 基本上可以实现大多数的数据结构，但是为了代码含义的明了以及子功能扩展的方便，应当尽量多的拆分出类。例如有一个 Student 的类，包含了学生的种种科目的成绩和评语，应当新建一个 Subject 类存放科目信息而不是在 Student 内的一个 grade 的内部变量中赋值。

不要使用包含其他字典的字典，也不要使用过长的元组。

如果容器中包含简单而又不可变的数据，可以优先使用 namedtuple 来表示，后期再修改为一个完整的类。

保存内部状态的字典如果变的比较复杂就该考虑拆分一个新的类出来。


## 23. 简单的接口应该接受函数，而不是类的实例

Python 中有很多内置的 API，都允许调用者传入函数以定制其行为。API 在执行的时候，会通过执行这些 hook 函数回调函数内的代码。其他的编程语言中会用抽象类来定义 hook，然而在 Python 中，很多挂钩只是无状态的函数，这些函数有明确的参数和返回值。用函数作为挂钩会比较适合，因为它们能很容易表达出这个挂钩的功能，而且定义它们也要比定义类要简单的多。Python 中的函数之所以能够充当 hook，主要的原因是 **Python 中的函数也是一个一级对象**，也就是说 Python 中的函数可以像其他值一样被传值和引用。

Python 中的类和方法都可以像一级类一样引用，因此它们和其他类型的对象一样可以放在表达式中。

通过调用名为 `__call__` 的方法，可以将类的实例像调用函数一样被调用。

如果需要用函数来表达状态，可以定义一个新的类，通过实现 `__call__` 方法，而不要定义带状态的闭包。

```py
class CountMissing(object):
    
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return 0

current = {'green':12, 'blue':3}
increments = [('red', 1),('blue', 12),('orange', 4)]

counter = CountMissing()
result = defaultdict(counter, current)
for k, amount in increments:
    result[k] += amount

assert counter.count == 2
```

### 24. 以 @classmethod 形式的多态去通用地构建对象

在 Python 中不仅对象支持多态，类也支持多态。多态使继承体系中的多个类都能以各自所独有的方式来实现某个方法。这些类都满足相同的接口或者继承自相同的抽象类，但是却有着不同的功能。

详情见[代码](./code/3-24.py)

上述代码可能要表达的意思是，使用 classmethod 可以避免初始化类，创造不必要的实例对象。

### 25. 用 super 初始化父类

初始化父类的传统方式，实在子类里面用子类实例直接调用父类的 `__init__` 方法。

```py
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 0)
```

这种方式对于简单的继承体系中是可行的吗，但是会在很多情况出现问题。

如果子类受到了多重继承的影响，直接调用超类的 `__init__` 方法，会产生无法预知的行为。

在子类调用 `__init__` 的问题之一，是它的调用顺序并不固定。例如：

```py
class TimesTwo(object):
    def __init__(self):
        self.value *= 2

class PlusFive(object):
    def __init__(self):
        self.value += 5

class ChildOne(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = ChildOne(5)
print(foo.value) # 15 => 5 * 2 + 5

class ChildTwo(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = ChildTwo(5)
print(foo.value) # 15
```

由于在 ChildTwo `__init__` 方法中，没有修改超类构造器的调用顺序，所以最终的结果还是 15。

还有一个问题发生在钻石继承中，如果子类继承自两个单独的超类，而那两个超类又继承自同一个公共基类，便构成一个钻石继承体系。这种继承会使钻石顶部的类执行多次 `__init__` 方法，从而产生一些奇怪的问题。

```py
class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5

class PlusTwo(NyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2

class ChildThree(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

foo = ChildThree(5)
print(foo.value) # 7 => 5 * 5 -> 5 + 2
```

在 ChildThree 的 `__init__` 方法中执行 `PlusTwo.__init__` 的时候，将里面 value 变量的值重新赋值为 5 了一次。

上述问题解决方法是使用内置的 super 函数，保证钻石顶部的那个公共基类的 `__init__` 方法只被调用一次。

```py
class TimesFive(MyBaseClass):
    def __init__(self, value):
        super(TimesFive, self).__init__(value)
        self.value *= 5

class PlusTwo(MyBaseClass):
    def __init__(self, value):
        super(PlusTwo, self).__init__(value)
        self.value += 2

class ChildFour(TimesFive, PlusTwo):
    def __init__(self, value):
        super().__init__(value)  # 以上两种 Python2 Python3 中都可以有用，但是本行只能在 Python3 中生效。

foo = ChildFour(5)
print(foo.value)    # 35 => ( 5 + 2 ) * 5 调用栈的顺序是 先入后出。
```

综上，为了避免会发生钻石继承重复初始化的问题，应该尽量使用 super 函数。
