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

