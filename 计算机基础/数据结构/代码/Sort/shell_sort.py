# shell_sort.py
#
# Shell Sort 希尔排序算法
# Author:   Tau
# Date:     2018-06-05
#

from insert_sort import insert_sort

def shell_sort_once(unsorted_list, add):
    '''shell_sort_once
    params:
        unsorted_list: 未排序列表
        add：本趟增量
    returns:
        unsorted_list：本轮返回结果
    '''
    for i in range(add):
        unsorted_list[i::add] = insert_sort(unsorted_list[i::add])
        print("SHELL DEBUG:", unsorted_list)
    return unsorted_list

def shell_sort(unsorted_list, add_list):
    '''shell_sort
    params：
        unsorted_list: 未排序列表
        add_list：增量列表
    returns:
        sorted_list：排序列表
    '''
    for add in add_list:
        unsorted_list = shell_sort_once(unsorted_list, add)
        
    return unsorted_list

if __name__ == "__main__":
    shell_sort([0,4,1,6,6,8,1,16,27,18,7,2,22,1,32], [6,3,1])