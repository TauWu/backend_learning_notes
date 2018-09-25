# File and IO
## 文件和IO

### 读写文本数据
```py
with open("text.txt", "rt", encoding="utf-8") as f:
    pass
```

### 打印输出到文件中
```py
with open("text.log", "wt") as f:
    print("Test log", file=f)
```

### 使用其它分隔符或打印终止符打印
```py
print('abcd', 1234, sep=',', end='\t')

row = ('abcd', 1234, 'bcda', 3)
print(','.join(str(x) for x in row))
print(*row, sep=",")
```

### 读写字节数据
```py
with open("text.bin", "rb") as f:
    pass
```

### 文件不存在时才写入
本操作可以避免覆盖已经写入的文件。
```py
with open("text.txt", "xt") as f:
    pass
```

### 字符串的IO操作
可以使用 io.StringIO() 和 io.BytesIO() 类来创建类文件对象操作字符串数据。比如：
```py
s = io.StringIO()
s.write('Hello World')
print('This is a test', file=s)
print(s.getvalue())
# Hello WorldThis is a test\n
s = io.StringIO('Hello\nWorld\n')
print(s.read(4))
# Hell
print(s.read())
# d\nWorld\n
```
StringIO 只能用于文本，如果需要对二进制文件进行操作，需要使用 io.BytesIO() 代替。

### 读写压缩文件
使用 gzip 或者 bz2 模块进行操作，基本也是使用 *.open() 方法进行读写操作。

### 固定大小记录的文件迭代
```py
from functools import partial

RECORD_SIZE = 32

with open('file.dat', 'rb') as f:
    records = iter(paertial(f.read, RECORD_SIZE), b'')
    pass
```

### 文件路径名的操作
使用 os.path 模块来进行文件名称和路径的操作。
```py
import os
import time

os.path.exists('/etc/passwd')                               # 文件是否存在
os.path.isdir('/etc')                                       # 是否是目录
os.path.islink('/usr/bin/python')                           # 是否是软链接
os.path.realpath('/usr/bin/python')                         # 链接指向
os.path.getsize('/etc/passwd')                              # 大小
time.ctime(os.path.getmtime('/etc/passwd'))                 # 修改时间
os.listdir('/etc')                                          # 目录文件列表
```