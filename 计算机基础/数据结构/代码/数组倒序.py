# -*- coding: utf-8 -*-
# 数组倒序
import time

RawList = [
    1, 2, 3, 
    4, 5, 6, 
    7, 8, 9
]

def timer(func):
    def _func(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        print("Function Name:%s Time:%.12fs"%(func.__name__, t2-t1))
        return res
    return _func

@timer
def reverse_os(raw_list):
    return raw_list[::-1]

@timer
def reverse_usr(raw_list):
    N = len(raw_list)
    for i in range(N/2):
        tmp1 = raw_list[i]
        tmp2 = raw_list[N-1-i]
        raw_list[i] = tmp2
        raw_list[N-1-i] = tmp1
    return raw_list

if __name__ == "__main__":
    print(reverse_os(RawList))
    print(reverse_usr(RawList))