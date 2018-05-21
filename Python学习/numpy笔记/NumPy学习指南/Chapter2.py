# -*- coding: utf-8 -*-

from numpy import *

# 生成一个0-4的数组对象
a = arange(5)
print(a)
print(a.dtype)
print(a.shape)      # 返回每个维度的长度 【1*5】

# 创建二维数组
m = array([arange(3), arange(3), arange(3), [1,1,4]])
print(m)
print(m.shape)      # 返回每个维度的长度 【4*3】

print(m[3])         # 取值类似Python里的List
print(m[3,1:])

# 创建三维数组
t = arange(24).reshape(2, 3, 4) # 创建一个一维数组后将它重构成三维的
print(t.shape)
print(t)
print(t[0,:,0])
print(t[1,...])

# 创建自定义数据类型
t = dtype([('name', str, 40), ('numitems', int32), ('price', float32)])
print(t)
print(t['name'])
items = array([('Book1',42,3.14), ('Buffer',13,1.10)], dtype=t)
print(items)

# 数组的展开
print(t[...,0:1])
print(t[...,0:1].ravel())       # ravel返回一个数组的视图
print(t.flatten())              # flatten请求分配内存保存结果

# 改变数组的维度
t.shape = (4,6)
print(t)
s = t.transpose()                   # 数组的转置
print(s)
t.resize((2,12))                    # resize会直接修改所操作的数组
print(t)

# 数组的组合
# numpy数组有水平组合、垂直组合、深度组合等多种组合方式

a = arange(9).reshape(3,3) # 生成一个3*3数组
b = 3*a                    # 数组a的数乘

print(a)
print(b)

# 水平组合
c1 = hstack((a, b))
print(c1)                    # 类似数组分组合并的操作
c2 = concatenate((a, b), axis=1)
print(c2)

# 垂直组合
d1 = vstack((a,b))
print(d1)                    # 类似数组分组
d2 = concatenate((a,b), axis=0)
print(d2)

# 深度组合(将相同的元组作为参数传给dstack函数，即可完成数组的深度组合)
# 深度组合可以理解成Python中的zip函数？
e = dstack((a, b))
print(e)

# 列组合
b1 = arange(6).reshape(3, 2)
b2 = arange(3)
f1 = column_stack((a, b1))
f2 = hstack((a, b1))
print(f1)
print(f2)                           # 所以其实列组合跟hstack差不多，但是column_stack可以用来组合arrary

# 行组合
f3 = row_stack((a, b2))
f4 = vstack((a, b2))
print(f3)
print(f4)                           # 行组合和vstack功能很接近

print(f3==f4)                       # 判断两个行列式是否全等

## 数组的分割
# 水平分割，切线与水平线垂直
s1 = hsplit(a, 3)                 # 将数组沿着水平方向分割为三个相同大小的子数组
s2 = split(a, 3, axis=1)
print(s1)
print(s2)

# 垂直分割，切线与垂线垂直
s3 = vsplit(a, 3)
s4 = split(a, 3, axis=0)
print(s3)
print(s4)

# 深度分割，切线与高垂直，三维数组分割成三个小的三维数组
a2 = arange(27).reshape(3,3,3)
s5 = dsplit(a2, 3)
print(s5)

# 数组的属性
# shape: 形状
# dtype: 数据类型
# ndim：数组维度 或者数组轴个数
# size: 数组的总个数
# itemsize: 数组中元素在内存中占用字节数
# nbytes = itemsize*size 数组占用内存字节数
# T: 和transpose一样是数组转置的作用
# real: 数组的实部
# imag: 数组的虚部
# flat: 返回一个numpy.flatiter的对象，可以生成一个迭代器

# numpy数组转化成python数组
b = arange(9).reshape(3,3)
c = b.tolist()              # 转换成Python数组
print(c)
d = b.astype(complex)         # 转换成Python数组指定类型
print(d)