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

if __name__ == "__main__":
    print(
        insert_sort([6,4,3,12,32,3,12,43,12,4,21,5,1])
    )