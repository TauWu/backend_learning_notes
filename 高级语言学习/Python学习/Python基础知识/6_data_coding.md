# Data and Coding
## 数据编码和处理

### 读写 csv 文件
csv 文件为`逗号分隔符文件`，指定逗号作为每一项数据的分隔符，存储维护一个类似表格的文件。对于 Python 来说，一般用 csv 库解决它的读写问题。
- 读 csv 文件
<p></p>

将 csv 文件中的数据读取为一个元组的序列：
```py
import csv

with open("data.csv") as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)   # 取第一行数据，一般而言第一行是标题
    for row in f_csv:
        pass                # row：数据行，是一个列表，通过下标取数据。
```
下标访问数据可能会引起混淆，可以考虑使用命名元组。
```py
from collections import namedtuple

with open("data.csv") as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)
```
以上的操作后允许你使用 row.Name 来对元素进行访问。假设文件第一行第一列为 id，则可以通过 row.id 取到第一列的数据。另一种做法是将数据读到一个字典序列中去，代码如下：
```py
import csv

with open("data.csv") as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print(row["id"])
```
- 写 csv 文件
写 csv 文件仍然可以使用 csv 模块，但是在写入之前需要创建一个 writer 对象才可以写入。
    - 针对 rows 为 tuple：
    ```py
    headers = ['id', 'name']
    rows = [
        (1,"a"), (2,"b"), (3,"c")
    ]
    with open("data.csv", "w") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    ```
    - 针对 rows 为 dict：
    ```py
    headers = ['id', 'name']
    rows = [
        {"id":1,"name":"a"}, {"id":2,"name":"b"}, {"id":3,"name":"c"}
    ]
    with open("data.csv", "w") as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
    ```

### 读写 json 数据
JSON(JavaScript Object Notation) 文件是当前比较流行的数据传输格式，读写 json 数据主要用到内置模块 json。json 编码支持的基本数据类型包括 None, bool, int, float, str，以及包含这些类型的 list, tuple 和 dict。另外，优雅的打印可以使用 pprint 模块代替 print 函数。
```py
import json
from pprint import pprint

json_str = """
{"name":"a", "id":1, "object":{"number":"1a"}}
"""

json_data = json.loads(json_str)
pprint(json_data, json_data["object"])

json_str = json.dumps(json_data)
print(json_str)
```

### 解析简单的 XML 数据
解析 XML 数据可能用到的模块是 xml.etree.ElementTree 或 lxml

### 增量式解析大型的 XML 文件
`略`

### 将字典转换为 XML
`略`

### 解析和修改 XML
`略`

### 利用命名空间解析 XML 文档
`略`

### 与关系型数据库的交互
`略`

### 编码和解码十六进制数
`略`

### 编码和解码 base64 数据
`略`

### 读写二进制数组数据
`略`

### 读取可嵌套和可变长二进制数据
`略`

### 数据的累加和统计操作
`略`
