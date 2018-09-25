# -*- coding: utf-8 -*-

import numpy as np
import datetime
import matplotlib.pyplot as plot

i2 = np.eye(2)      # 生成一个单位矩阵
print(i2)
i = i2.real.astype(int)
np.savetxt('eye.log', i)

# c和v分别是csv文件中第1列和第3列的数据列表
c, v = np.loadtxt('data.csv', delimiter=',', usecols=(1,3), unpack=True)

vmap = np.average(c, weights=v) # VMAP 加权平均值， v为权重值

print("vmap:", vmap)

mean = np.mean(c)   # MEAN 计算算术平均值

print("mean:", mean)

t = np.arange(len(c))
twap = np.average(c, weights=t) # TWAP 时间加权平均值 （最近的价格重要性更大）
print("twap:", twap)

# 获取数据文件中的最值
print("c.max:", np.max(c))
print("c.min:", np.min(c))
print("v.max:", np.max(v))
print("v.min:", np.min(v))


# 获取数据文件中的极差（最大值和最小值之差）
print("c.ptp", np.ptp(c))
print("v.ptp", np.ptp(v))

# 获取数据文件的中位数
print("c.median:", np.median(c))
## 对中位数结果的检查
N = len(c)
sort = np.msort(c)
print("c.median.check:", (sort[int(N/2)] + sort[int((N-1)/2)])/2)

# 计算方差
## 方差的定义是 各个数据与所有数据的算术平均值 之差 的绝对值的平方和除以个数（与概率论中的说法不完全一致）
print("c.var:", np.var(c))
print("v.var:", np.var(v))
print("c.var.check:", np.mean((c - c.mean())**2))

## ！！！ 本方法对本数据样本没有参考意义仅仅作为演示
# diff返回一个由相邻的数组元素从差值构成的数组
print("c.diff:", np.diff(sort))
print("c.std:", np.std(np.diff(sort) / sort [:-1]))

# 所有的数据取对数
print("c.log:", np.log(c))  # 一般需要检查正数

# where函数 获取返回值的范围
print("c.where c < 3000", np.where(c < 3000))  # 返回数值小于3k的索引

def get_date(d):
    return datetime.datetime.strptime(str(d)[2:-1], r'%Y.%m.%d').date().weekday()

dates, prices = np.loadtxt('data.csv', usecols=(8, 1), delimiter=',', converters={8:get_date}, unpack=True)            # 获取文件中日期并全部转换成星期

print(dates)

# 计算分组平均值， 分组个数（以日期为维度）
averages = np.zeros(7)      # 创建一个空的numpy数组
counts = np.zeros(7)
for i in range(0,7):
    indices = np.where(dates==i)
    value = np.take(prices, indices)
    avgs = np.mean(value)
    lens = np.size(indices)
    print("Day:", i, "Count:", lens, "Average:", avgs)
    averages[i] = avgs
    counts[i] = lens

print("价格最大平均值", averages.max(), "周几", averages.argmax())
print("价格最小平均值", averages.min(), "周几", averages.argmin())
print("数量最小平均值", counts.max(), "周几", counts.argmax())
print("数量最小平均值", counts.min(), "周几", counts.argmin())

# 简单移动平均线
c = np.loadtxt("data.csv", delimiter=',', usecols=1, unpack=True)
N = 5
weights = np.ones(N)/N  # 生成权重
sma = np.convolve(weights, c)[N-1:-N+1]    # 取出运算结果中间长度为N的数组，这部分是卷积运算时完全覆盖的部分
t = np.arange(N-1, len(c))

# 绘制曲线
plot.plot(t, c[N-1:], lw=1.0)
plot.plot(t, sma, lw=2.0)
plot.show()

# 指数移动平均线
N = 5
weights = np.exp(np.linspace(-1.,0.,N)) # 设置权重，其中linspace函数返回一个 指定范围内 指定个数 均匀分布的数组
weights /= weights.sum()
ema = np.convolve(weights, c)[N-1:-N+1]

# 绘制曲线
plot.plot(t, c[N-1:], lw=1.0)
plot.plot(t, ema, lw=2.0)
plot.show()

# 布林带
## 定义详见文档
devs = list()
C = len(c)

for i in range(N-1, C):
    if i+N < C:
        dev = c[i:i+N]
    else:
        dev = c[-N:]
    
    averages = np.zeros(N)
    averages.fill(sma[i-N-1])
    dev = dev -averages
    dev = dev ** 2
    dev = np.sqrt(np.mean(dev))
    devs.append(dev)

devs = 2*np.array(devs)
up = sma + devs
low = sma - devs
c1 = c[N-1:]

plot.plot(t, c1, lw=1.0)
plot.plot(t, sma, lw=2.0)
plot.plot(t, up, lw=3.0)
plot.plot(t, low, lw=4.0)
plot.show()

