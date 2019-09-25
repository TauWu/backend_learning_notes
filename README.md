<!-- backend_learning_notes -->
# BACKEND_LEARNING_NOTES

后端学习笔记，本项目存放了一些我阅读有关的技术类的书籍和部分源码阅读的笔记整理。

涉及范围包括后端开发中的计算机学科基础知识、高级语言的基础知识、源码阅读笔记、数据库知识、数据挖掘知识等，同时也会涉及到一些具体生产场景中会遇到的一些实际问题。

## 项目基础信息
Basic info for this project.

ProjectName | Author | CreateDate | ChineseName
:-: | :-: | :-: | :-:
backend_learning_notes | TauWoo | 2018-05-21 | 后端编程学习笔记

## 项目目录

### 高级语言学习

#### Python学习

- [ ] :cookie: **[NumPy学习指南](./高级语言学习/Python学习/numpy笔记/NumPy学习指南)**:email: [Python数据分析基础教程：NumPy学习指南（第2版）.pdf](https://github.com/TauWu/backend_learning_notes/blob/master/%E9%AB%98%E7%BA%A7%E8%AF%AD%E8%A8%80%E5%AD%A6%E4%B9%A0/Python%E5%AD%A6%E4%B9%A0/numpy%E7%AC%94%E8%AE%B0/docs/Python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B%EF%BC%9ANumPy%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97%EF%BC%88%E7%AC%AC2%E7%89%88%EF%BC%89.pdf)
    > Numpy 是 Python 中的一种开源的数值计算扩展模块，该模块开源用来存储和计算大型矩阵，其效率要远远高于 Python 内部的嵌套列表的数据结构。目前较多的被应用在机器学习、数据挖掘等方面。
    - [x] [numpy基础](./高级语言学习/Python学习/numpy笔记/NumPy学习指南/Chapter2.py)
    - [x] [常用函数](./高级语言学习/Python学习/numpy笔记/NumPy学习指南/Chapter3.py)
    - [ ] 便捷函数
    - [ ] 矩阵和通用函数
    - [ ] 深入学习numpy模块
    - [ ] 专用函数
    - [ ] 质量控制
    - [ ] Matplotlib绘图
    - [ ] Scipy

- [ ] :cookie: [Python 基础知识](./高级语言学习/Python学习/Python基础知识/README.MD):email: [Python3 CookBook](http://python3-cookbook.readthedocs.io/zh_CN/latest/)
    > Python 是一门面向对象的程序设计语言，语法简洁更专注于解决问题而不是搞明白语言本身。Python 的标准库和第三方库足够强大到能完成很多其他语言实现不了或实现起来很麻烦的操作。但作为脚本语言，其运行速度相对于编译型的 C++/C/Java/Go 等语言来说，运行速度上相对较慢。
    
    - [x] [数据结构和算法](./高级语言学习/Python学习/Python基础知识/1_datastruct.py)
    - [x] [字符串和文本](./高级语言学习/Python学习/Python基础知识/2_strings.py)
    - [x] [数字日期和时间](./高级语言学习/Python学习/Python基础知识/3_nums_datetime.py)
    - [x] [迭代器与生成器](./高级语言学习/Python学习/Python基础知识/4_iterator_generator.md)
    - [x] [文件与IO](./高级语言学习/Python学习/Python基础知识/5_file_io.md)
    - [x] [数据编码和处理](./高级语言学习/Python学习/Python基础知识/6_data_coding.md)
    - [x] [函数](./高级语言学习/Python学习/Python基础知识/7_function.md)
    - [ ] [类与对象](./高级语言学习/Python学习/Python基础知识/8_class_object.md)
    - [ ] 元编程
    - [ ] 模块与包
    - [ ] 网络与web编程
    - [ ] 并发编程
    - [ ] 脚本编程与系统管理
    - [ ] 测试、调试和异常
    - [ ] C语言扩展
    
- [ ] :cookie: [Tornado](./高级语言学习/Python学习/Tornado):email: [Tornado](http://www.tornadoweb.org/en/stable/index.html)
    > Tornado is a Python web framework and asynchronmous networking libary. By using non-blocking network I/O, Tornado can scale to tens of thousands of open connections, making it ideal for long polling, WebSockets, and other applications that require a long-lived connection to each user.

    - [x] User's guide
    - [ ] Web framework
    - [ ] HTTP servers and clients
    - [ ] Asynchronous networking
    - [ ] Coroutines and concurrency
    - [ ] Integration with other services
    - [ ] Utilities
    - [ ] Frequently asked questions

- [ ] :cookie: [effective-python](./高级语言学习/Python学习/effective-python)
    > write pythonic code.

    - [ ] pythonic
    - [ ] function
    - [ ] class
    - [ ] metaclass and property
    - [ ] subprocess
    - [ ] inner model
    - [ ] co-coding
    - [ ] others

#### Golang 学习

- [x] :cookie: [Golang 基础知识](./高级语言学习/Golang学习/Golang基础知识/README.md):email: [The Way to Go](https://zengweigang.gitbooks.io/core-go/content/index.html)
    > Go 语言是一门年轻的编译型程序设计语言，相对于 C++ 的繁琐，它的语法更加简洁；相对于 JVM 的臃肿，它对虚拟机的依赖更小；相对于 Python 的缓慢，它作为编译语言可以秒杀一众解释型语言。Go 是一个相对更中规中矩的语言，没有明显的短板，用起来的感受和运行起来的感受都很均衡。同时，Go 也是第一个在语言级别实现协程 (goroutine) 的语言。
    
    - [x] [code](./高级语言学习/Golang学习/Golang基础知识/Code)
    - [x] [基础知识](./高级语言学习/Golang学习/Golang基础知识/1_基础知识.md)
    - [x] [基本结构和基本数据类型](./高级语言学习/Golang学习/Golang基础知识/2_基本结构和基本数据类型.md)
    - [x] [控制结构](./高级语言学习/Golang学习/Golang基础知识/3_控制结构.md)
    - [x] [函数](./高级语言学习/Golang学习/Golang基础知识/4_函数.md)
    - [x] [数组与切片](./高级语言学习/Golang学习/Golang基础知识/5_数组与切片.md)
    - [x] [Map](./高级语言学习/Golang学习/Golang基础知识/6_Map.md)
    - [x] [结构和方法](./高级语言学习/Golang学习/Golang基础知识/7_结构和方法.md)
    - [x] [接口和反射](./高级语言学习/Golang学习/Golang基础知识/8_接口和反射.md)
    - [x] [读写数据](./高级语言学习/Golang学习/Golang基础知识/9_读写数据.md)
    - [x] [错误处理及测试](./高级语言学习/Golang学习/Golang基础知识/10_错误处理及测试.md)
    - [x] [协程和通道](./高级语言学习/Golang学习/Golang基础知识/11_协程与通道.md)
    - [x] [Web 开发](./高级语言学习/Golang学习/Golang基础知识/12_网络.md)

#### Java学习

- [ ] :cookie: [Java 基础知识](./高级语言学习/Java学习/Java基础知识):email: 无
    > Java 是一门面向对象的语言，吸收了 C++ 的各种优点外，摈弃了 C++ 中难以理解的 多继承、指针 等概念。Java 具有简单性、面向对象、健壮性、分布式、可移植性和多线程等优点，可以编写桌面程序、后端服务、嵌入式系统等。

### 计算机基础

#### 计算机基础专业课

- [ ] :cookie: 计算机组成原理

- [x] :cookie: 数据结构
    - [x] [绪论](./计算机基础/数据结构/笔记/绪论.md)
    - [x] [线性表](./计算机基础/数据结构/笔记/线性表.md)
    - [x] [栈与队列](./计算机基础/数据结构/笔记/栈与队列.md)
    - [x] [串](./计算机基础/数据结构/笔记/串.md)
    - [x] [数组与广义表](./计算机基础/数据结构/笔记/数组与广义表.md)
    - [x] [树与二叉树](./计算机基础/数据结构/笔记/树与二叉树.md)
    - [x] [图](./计算机基础/数据结构/笔记/图.md)
    - [x] [查找](./计算机基础/数据结构/笔记/查找.md)
    - [x] [内部排序算法](./计算机基础/数据结构/笔记/内部排序.md) 

- [x] :cookie: 操作系统
    - [x] [操作系统概述](./计算机基础/操作系统/笔记/操作系统概述.md)
    - [x] [进程管理](./计算机基础/操作系统/笔记/进程管理.md)
    - [x] [内存管理](./计算机基础/操作系统/笔记/内存管理.md)
    - [x] [文件管理](./计算机基础/操作系统/笔记/文件管理.md)
    - [x] [输入输出（I/O）管理](./计算机基础/操作系统/笔记/输入输出（IO）管理.md)

- [ ] :cookie: 计算机网络
    - [x] [计算机网络概述](./计算机基础/计算机网络/计算机网络概述.md)
    - [x] [数据通信原理](./计算机基础/计算机网络/数据通信原理.md)
    - [ ] [计算机网络体系结构和协议](./计算机基础/计算机网络/计算机网络体系结构和协议.md)

#### 数学基础专业课

- [ ] :cookie: 微积分

- [ ] :cookie: 线性代数

- [ ] :cookie: 概率论与数理统计

- [ ] :cookie: 离散数学

- [ ] :cookie: 几何学

### 数据库与数据挖掘

- [ ] :cookie: [DataMining](./DataMining):email: [DataMiningConceptsAndTechniques.pdf](./DataMining/docs/DataMiningConceptsAndTechniques.pdf)
    - [ ] [notes](./DataMining/notes)

### `issues`实际应用场景中遇到的问题笔记

- [x] :cookie: [prepared_statement的糖和坑](./issues/数据库/prepared_statement的糖和坑.md)
- [x] :cookie: [链家上海Java工程师面经](./issues/面经/2018年5月29日链家上海Java工程师.md)

### [LeetCode](./LeetCode/README.md)

- [ ] :cookie: [Code](./LeetCode/Code)
