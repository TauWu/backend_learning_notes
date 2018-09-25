#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  
# Nums and DateTime
# Chapter 3 from Python CookBook
#

# 数字的四舍五入
# 保留x位小数
print(round(1.22, 1))
print(round(1.23333, 2))
print(round(-1.227, 2))
print(round(1008611, -3))
# 当一个值处在两个边界的时候，round函数返回离它最近的偶数
print(round(2.5))
print(round(1.5))

# 指定精度输出
x = 1.23456
print("Result is {:0.3f}".format(x))

# 浮点数的陷阱
# 底层CPU和IEEE 754标准通过自己的浮点单位去执行算术时的特征。由于Python的浮点数数据类型使用底层表示存储数据，因此以下的情况无法避免。
y = 0.12345
print(x+y)
# Decimal模块 - 更精确的数据、可能会有一定的性能损耗
from decimal import Decimal, localcontext
a = Decimal('1.123312')
b = Decimal('2.342132123')
# localcontext 设置输出的精度的有效范围
with localcontext() as ctx:
    ctx.prec = 3
    print(a+b)
print(a+b)

# 非十进制输出
print(bin(31))
print(oct(31))
print(hex(31))
print(format(31,'b'))
print(format(31,'o'))
print(format(31,'x'))

# Python指定八进制数的限制
import os
os.chmod('README.MD', 777)          # 错误写法
os.chmod('README.MD', 0o777)        # 正确写法

#TODO 字节到大整数的打包和解包

# 复数的运算和处理
ai = complex(1,2)
bi = 3+4j
print(ai, bi, ai.conjugate(), bi.conjugate())

import cmath
print(cmath.sin(ai))
print(cmath.sqrt(-1))               # 此处使用math.sqrt将会报错

import numpy as np
a = np.array(
    [1+1j,2-2j,3+4j,5-1j]
)
print(a)
print(a+2)
print(np.sin(a))


# 无穷大和NaN
print(float('inf'))
print(float('-inf'))
print(float('nan'))

# 分数表示与计算
from fractions import Fraction
a = Fraction(1,2)
b = Fraction(20,16)
c = 0.75
print(a, b, a+b, a/b, float(a), Fraction(*c.as_integer_ratio()))

# 大型数组计算 - numpy库
# 底层实现中，numpy数组使用了C或Fortran语言的机制分配内存（new delete）
import numpy as np
ax = np.array([1,2,3,4])
ay = np.array([1,2,3,4])
print(ax, ay, ax+ay, ax+2, ax*2, ax*ay, np.sqrt(ax))

def foo(x):
    return 3*x**2 - 2*x + 7
print(foo(ax))

print(np.zeros(shape=[10000,10000], dtype=float))

# 矩阵和线性代数运算
m = np.matrix([[1,2,3],[3,2,1],[0,1,3]])
n = np.matrix([[1,2,3]])
print('原矩阵Origin\n', m, '\n转置矩阵Transpose\n', m.T, '\n逆矩阵\n', m.I, '\n两矩阵的积\n', n*m)

# 更多的numpy操作
from numpy.linalg import det, eigvals, solve
# Determinant, Eigenvalues
print(det(m), eigvals(m))

# 随机选择 random模块
import random
a = [1,2,3,4,5,6,7,8]
print("1st:", random.choice(a))
print("2nd:", random.choice(a))
print("1st:", random.sample(a,2))
print("2nd:", random.sample(a,3))
random.shuffle(a)
print("shuffle:", a)
# random模块使用 Mersenne Twister 算法计算生成随机数（类似C语言中的伪随机数），但是可以通过提供不同的种子来达到生成随机数的目的。
random.seed(1234)
print(random.randint(0,13))
import ssl
print(ssl.RAND_bytes(10))       # 密码学中会用到的随机生成方法

# 基本的日期和时间的转换
# 为了执行不同时间单位的转换和计算，需要使用datetime模块。为了表示一个时间块，可以创建一个timedelta实例。
from datetime import timedelta, datetime
a = timedelta(days=2,hours=10)
b = timedelta(days=1)
a_t = datetime(2018, 12, 1)
b_t = datetime(2017, 10, 12)
print(a+b, a.total_seconds()/3600, a_t-b_t, a_t+a)
# 为了执行更加附加的日期操作，可以使用 dateutil 模块
from dateutil.relativedelta import relativedelta
print(a_t+relativedelta(months=1))
print(relativedelta(a_t, b_t))

# 字符串转化为日期
text = '2018-12-01 12:12:13'
text_t = datetime.strptime(text,"%Y-%m-%d %H:%M:%S")
print(text_t, text_t-a_t, datetime.strftime(a_t, "%Y/%m/%d"))
# ATTENTION: strptime()的性能比较差，在已知确切格式的情况下，可以考虑直接当做字符串处理
def parse_time(s):
    y_s, m_s, d_s = s.split('-')
    return datetime(int(y_s), int(m_s), int(d_s))