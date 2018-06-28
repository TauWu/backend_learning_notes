# Class and Object
## 类和对象

### 改变对象的字符串显示
改变一个实例的字符串表示可以通过重定义它的 \_\_str()\_\_ 和 \_\_repr()\_\_ 方法。
```py
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return 'Pair({0.x!s}, {0.y!s})'.format(self)
```
- \_\_str()\_\_ 体现:print() 函数
- \_\_repr()\_\_ 体现:交互式解释器内容

### 自定义字符串的格式化
```py
_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
    }

class Date:
    def __init__(self, y, m, d):
        self.y = y
        self.m = m
        self.d = d

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

d = Date(2018, 12, 31)
print(format(d, 'mdy'))     # 12/31/2018
print('The date is {:ymd}'.format(d)) # The date is 2018-12-31
```

### 让对象支持上下文管理协议
为了让一个对象兼容 with 语句，需要实现 \_\_enter\_\_() 方法和 \_\_exit()\_\_ 方法。
```py
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:

    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RunTimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None
```
这个类的关键特点在于它表示了一个网络连接，但是初始化的时候并不会做任何事情（比如它并没有建立一个连接）。连接的建立和关闭是使用 with 语句自动完成。
```py
from functools import partial

conn = LazyConnect(('www.baidu.com', 80))
with conn as s:
    # conn.__enter__()
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.baidu.com')
    s.send(b'\r\n')
    s.send(b''.join(iter(partial(s.recv, 8192), b'')))
    # conn.__exit__()
```
编写上下文管理器的主要原理是你的代码会放到 with 语句中执行。当出现 with 语句的时候，对象的 \_\_enter()\_\_ 方法会被触发，它返回的值会被赋值给 as 声明的变量，然后 with 语句块里面的代码开始执行。最后 \_\_exit()\_\_ 方法会被触发进行清理工作。这样的操作在使用到锁的情况下会比较常见，生成一个锁需要在执行结束后去除锁，否则会引起死锁的问题。
<p></p>
在 contextmanager 模块中有一个标准的上下文管理方案模板。

### 创建大量对象时节省内存的方法
通过给类添加 \_\_slots\_\_ 属性可以极大的减少实例所占用的内存，在创建大量的对象时可以节省内存。但是，**定义完 \_\_slots\_\_ 属性后不能再给实例添加新的属性，而且普通类的一些特性也没有办法实现比如继承。**
```py
# 这并不是一个很值得使用的功能
class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
```

### 在类中封装属性名
Python 中并没有像 C++ 那样的对“私有数据”的一个概念，一般通过约定的规范来达到这个目的。比如 __ 代表私有（private）变量/方法，_ 代表保护（protected）变量/方法。

### 创建可管理的属性
自定义某个属性的方法是将它定义为一个 property。
```py
class Person:

    def __init__(self, first_name):
        self.first_name = first_name
    
    @property                                       # getter 函数
    def first_name(self):
        return self._first_name

    @property.setter                                # setter 函数
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Excepted a string")
        self._first_name = value

    @property.deleter                               # deleter 函数
    def first_name(self):
        raise AttributeError("Error")

p = Person("Name")
print(p.first_name)     # Name
p.first_name = 4        # Excepted a string
del p.first_name        # Error
```
NOTE：关于在 \_\_init()\_\_ 方法中设置了 self.first_name 而不是 self.\_first\_name 的原因是，希望在初始化的时候就调用这个 property。

### 调用父类方法
为了调用父类（超类）方法，可以使用 super() 函数，比如：
```py
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()      # call parent spam()
```
super() 函数的另一个常见用法是在 \_\_init()\_\_ 方法中确保父类被正确的初始化：
```py
class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __init__(self):
        super.__init__()
        self.y = 1
```
super() 的另外用法常见在覆盖 Python 的特殊方法中，比如：
```py
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # Delegate attr lookup to internal obj
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # Delegate attr assignment
    def __setattr__(self, name, value):
        if name.startswith('-'):
            super().__setattr__(name, value)    # call origin __setattr__
        else:
            setattr(self._obj, name, value)
```

### 子类中扩展 property
```py
class Person:

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self.name

    @property.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Excepted a string.')
        self._name = value

    @property.deleter
    def name(self):
        raise AttributeError('Error')

class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('delete name')
        super(SubPerson, SubPerson).name.__delete__(self)

sp = SubPerson('Test')      # Setting name to Test
print(sp.name)              # Getting name \n Test
sp.name = 'New Test'        # Setting name to NewTest
sp.name = 10                # Excepted a string
```
如果仅仅只想扩展 property 的某一个方法，可以这样写：
```py
class SubPerson(Person):

    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name
```
实际上，property 是 getter、setter 和 deleter 方法的集合，而不是单个方法，因此在继承时候就需要考虑是要修改其中的一部分还是所有的三个方法。

### 创建新的类或实例属性
通过**描述器类**的形式定义新建的类或实例的功能。
```py
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Excepted an int.')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]
```
一个描述器就是一个实现了三个核心的属性访问操作 get、set、delete 的类，

### 使用延迟计算属性
`略`没啥意义

### 简化数据结构的初始化
`略`没啥意义

### 定义接口或者抽象基类
`略`没啥意义

### 实现数据模型的类型约束
希望定义某些在属性赋值上面有限制的数据结构，需要在对某些实例属性赋值时进行检查。所以需要自定义赋值函数，这种情况最好使用描述器。
```py
class Descriptor:

    def __init__(self, name=None, **opts):
        self.name = name
        for k, v in opts.items:
            setattr(self, k, v)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

class Type(Descriptor):
    excepted_type = None

    def __set__(self, instance, value):
        if not isinstance(value, self.excepted_type):
            raise TypeError("excepted " + str(self.excepted_type))
        super().__set__(instance, value)

class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise TypeError("missing size option")
        super().__init__(instance, value)

class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        self.name = name
        for k, v in opts.items:
            setattr(self, k, v)
```

### 实现自定义容器
`略`没啥意义

### 属性的代理访问
代理是一种编程模式，它将某个操作转移给另外一个对象来实现。最简单的形式如下：
```py
class A:
    def spam(self, x):
        pass
    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()
    
    def spam(self, x):
        return self._a.spam(x)
    def foo(self):
        return self._a.foo()
```
如果某一个类中有很多方法需要代理，可以使用 \_\_getattr()\_\_ 方法处理：
```py
class B2:
    def __init__(self):
        self._a = A

    def bar(self):
        pass

    def __getattr__(self, name):
        return getattr(self._a, name)
```
代理类一般是类继承的替代方法。另外 \_\_getattr()\_\_ 方法只会对暴露在外部的公共方法进行代理，而不会代理 **私有和保护** 的方法。

### 在类中定义多个构造器
```py
import time

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_month, t.tm_day)

a = Date(2012, 12, 21)
b = Data.today()
```
类方法的一个主要用途就是定义多个构造器，接收 class 作为第一个参数 cls。这个类被用来创建并返回最终的实例。

### 创建不调用 init 方法的实例
`略`没啥意义

### 利用 Mixins 扩展类的功能


### 实现状态对象或者状态机

### 通过字符串调用对象方法

### 实现访问者模式

### 不用递归实现访问者模式

### 循环引用数据结构的内存管理

### 让类支持比较等操作

### 创建缓存实例