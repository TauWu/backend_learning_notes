# 用 Pythonic 方式来思考

## 1. 确认自己使用的 Python 版本

没啥好讲的，主要 Python 2 跟 Python 3 有一部分语法的区别。

## 2. 遵循 PEP8 风格指南

1. 使用空格来表示缩进，而不要使用 tab

```py
def foo():
    pass
```

2. 和语法有关的每一层缩进都用 4 个空格表示

```py
def foo():
    print("4 spaces")
```

3. 每行的字符数不该超过 79 个
4. 对于占据多行的长表达式来说，除了首行之外的其余各行都应该在通常的缩进级别上再加上四个空格
```py
def foo():
    print(1111111111111111111111111111, 1111111111,
        "前面有 8 个空格", 222222
    )
```

5. 文件中的函数和类之间应该用两个空行隔开
6. 在同一个类中，各个方法之间应该用一个空行隔开


```py
class Cls():

    def __init__():
        pass

    def foo():
        pass


def foo():
    pass
    
```

7. 在使用下标取值的时候，不要在中括号两边加空格

```py
print(ls_sample[1])
```

8. 为变量赋值的时候，等号左右应当有且只有一个空格隔开

```py
x = ls_sample[1]
```

9. 函数、变量及属性名应该用长蛇命名： sample_name

```py
sample_name = 1
self.sample_name = 2
```

10. 类里面受保护的实例属性，命名开头应该是一个短下划线： _sample_name

```py
class Cls:
    def _sample_func(self):
        self._sample_name = 1
```

11. 类里面私有的实例属性，命名开头应该是两个短下划线： __sample_name

```py
class Cls:
    def __sample_func(self):
        self.__sample_name = 1
```

12. 类和异常的命名应当是大驼峰： SampleName

```py
class SampleCls:
    def foo():
        SampleEror = ValueError()  
```

13. 模块级别的常量应当是全部大写字母拼写，然后单词之间用下划线： SAMPLE_NAME

```py
SAMPLE_NAME = "SAMPLEvalue"
```

14. 类中的实例方法（instance method），首个参数应该是 self，以表示对象自身

```py
class Cls:
    def foo(self):
        self.x = 1
```

15. 类方法（class method）的首个参数，应该命名为 cls，以表示该类本身

```py
class Cls:
    def foo(cls):
        pass
```

16. 采用内联形式的否定词，而不要把否定词放在整个表达式的前面，应该是 if a is not b 而不是 if not a is b

```py
if a is not b:
    pass
```

17. 不要通过检测长度的方法判断 somelist 是否为 [] 或者 '' 或者空值，应该采用 if not somelist 而不是 if len(somelist) != 0

```py
ls = []
if not ls:
    pass
```

18. 检测 somelist 是否为 '[1]' 或者 'hi' 等非空值时，也应如此，if somelist 语句会默认的把值判断为 True

```py
ls = [1]
if ls:
    pass
```

19. 不要编写单行的 if 语句，for 循环，while 循环及 except 语句，而应该把这些语句分成多行来书写，以示清晰

```py
if True:
    pass
```

20. import 语句应该总是放在文件开头

```py
import a

class Cls:
    def foo():
        pass
```

21. 引用模块的时候，总是应该使用绝对名称，而不是应该根据当前模块的路径来使用相对名称。

```py
from a import b
```

22. 文件中的那些 import 语句应该按顺序划分成三个部分，分别表示标准库模块、第三方模块、自用模块。在每个部分中，各 import 语句应该按照模块的字母顺序排列

```py
import time

import redis

import mymodule
```
