# insert_sort.py
#
# Insert Sort 插入排序算法
# Author:   Tau
# Date:     2018-06-04
#

def insert_once(sorted_list, elem):
    '''insert_once
    插入排序的一次插入操作
    params:
        sorted_list：已排序列表
        elem：待插入元素
    returns:
        sorted_list：已排序列表
    '''

    sorted_list.append(elem)
    
    for i in range(0, len(sorted_list)):
        if sorted_list[i] > elem:
            sorted_list[-1] = sorted_list[i]
            sorted_list[i] = elem
            elem = sorted_list[-1]

    print("DEBUG:", sorted_list)
    return sorted_list

def insert_sort(unsorted_list):
    '''insert_sort
    插入排序操作
    params：
        unsorted_list：未排序序列
    returns:
        sorted_list:已排序序列
    '''
    for i in range(1, len(unsorted_list)):
        unsorted_list[:i+1] = insert_once(unsorted_list[:i], unsorted_list[i])
    return unsorted_list

def insert_once_half(sorted_list, elem):
    '''insert_once_half
    插入排序的一次插入操作
    params:
        sorted_list：已排序列表
        elem：待插入元素
    returns:
        sorted_list：已排序列表
    '''
    low = 0
    high = len(sorted_list)

    while True:
        m = int((high - low) / 2) + low
        if high - low <= 1:
            break
        if sorted_list[m] >= elem:
            high = m
            continue
        elif sorted_list[m] < elem:
            low = m
            continue
        else:
            raise RuntimeError("运行错误")

    sorted_list.insert(m+1, elem)
    print("DEBUG:", high, low, m+1, sorted_list)
    return sorted_list

def insert_sort_half(unsorted_list):
    '''insert_sort
    插入排序操作
    params：
        unsorted_list：未排序序列
    returns:
        sorted_list:已排序序列
    '''
    for i in range(1, len(unsorted_list)):
        unsorted_list[:i+1] = insert_once_half(unsorted_list[:i], unsorted_list[i])
    return unsorted_list

if __name__ == "__main__":
    print(
        insert_sort_half([0,4,1,6,6,8,1,16,27,18,7,2,22,1,32]),
        insert_sort([0,4,1,6,6,8,1,16,27,18,7,2,22,1,32])
    )