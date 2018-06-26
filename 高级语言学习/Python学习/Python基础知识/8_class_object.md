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
```

### 让对象支持上下文管理协议

### 创建大量对象时节省内存的方法

### 在类中封装属性名

### 创建可管理的属性

### 调用父类方法

### 子类中扩展 property

### 创建新的类或实例属性

### 使用延迟计算属性

### 简化数据结构的初始化

### 定义接口或者抽象基类

### 实现数据模型的类型约束

### 实现自定义容器

### 属性的代理访问

### 在类中定义多个构造器

### 创建不调用 init 方法的实例

### 利用 Mixins 扩展类的功能

### 实现状态对象或者状态机

### 通过字符串调用对象方法

### 实现访问者模式

### 不用递归实现访问者模式

### 循环引用数据结构的内存管理

### 让类支持比较等操作

### 创建缓存实例