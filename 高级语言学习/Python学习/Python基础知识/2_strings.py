#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  
# Strings
# Chapter 2 from Python CookBook
#

# 使用多个界定符分割字符串
import re
line = 'sadas dsadf; dsadw dsadw,sdadas'
print(line.split(' '))
print(re.split(r'[;,\s]\s*', line))
print(re.split(r'(?:,|;|\s)\s*', line))

# 字符串开头或结尾匹配
filename = 'text.py'
print(filename.endswith('py'))

filelist = [
    'test.py', 'text.c', 'app.cpp', 'App.cs'
]
print([name for name in filelist if name.endswith(('.c', '.cpp'))])

# 采用shell通配符匹配文件
from fnmatch import fnmatch, fnmatchcase

print(fnmatch('foo.txt', '*.txt'))
print(fnmatch('foo.txt', 'f?o.txt'))
print([name for name in filelist if fnmatch(name, '?pp.*')])

# fnmatch对大小写的敏感与运行系统保持一致
# On Unix False
# On Windows True
print(fnmatch('foo.txt', '*.TXT'))

# 使用fnmatchchcase 来保证大小写一定敏感
# Tips 不仅仅在文件上面可以匹配

# 正则表达式 - 匹配
s = '12das231'
comp = re.compile(r'[0-9]+')
print(re.findall(r'([0-9]+)', s))       # 直接的方法调用
print(comp.findall(s))            # 预编译

# 正则表达式 - 替换
s = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
comp = re.compile(r'(\d+)/(\d+)/(\d+)')

# sub subn
print(comp.sub(r'\3年\1月\2日', s))
print(comp.subn(r'\3年\1月\2日', s))

# callback Func
def change(m):
    y = '{}年'.format(m.group(3))
    d = '{}-{}'.format(m.group(2), m.group(1))
    return '{}{}'.format(y, d)
print(comp.sub(change, s))

# 正则表达式 - 忽略大小写的文字替换
s = 'UPPER PY, lower py, Mixed Py'

def matchcase(word):

    def replace(m):
        
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word

    return replace

print(re.sub('py', 'cpp', s, flags=re.IGNORECASE))
print(re.sub('py', matchcase('cpp'), s, flags=re.IGNORECASE))       # sub的repl可以是替换规则，也可以是一个callback


# 正则表达式 - 非贪婪匹配
s = 'Test says: "yes.", Test1 says :"no."'
comp = re.compile(r'"(.*)"')
print("贪婪匹配", comp.findall(s))
comp = re.compile(r'"(.*?)"')
print("非贪婪匹配", comp.findall(s))

# 正则表达式 - 多行匹配
s = '''/* This is
 a comment*/'''

# 不能正确匹配
comp = re.compile(r'/\*(.*)\*/')
print(comp.findall(s))

# 能正确匹配（正则兼容，标记符号）
comp = re.compile(r'/\*((?:.|\n)*?)\*/')
print(comp.findall(s))
comp = re.compile(r'/\*(.*)\*/', re.DOTALL)
print(comp.findall(s))

# 删除文本中不必要的字符
s = 'Hello world\n'
print(s)
print(s.strip())
print(s.lstrip('H'))

# 字符串的对齐和填充
s = 'Hello'
print(s.center(19,'*'))
print(s.ljust(19,'?'))

#TODO 文字匹配模块代码