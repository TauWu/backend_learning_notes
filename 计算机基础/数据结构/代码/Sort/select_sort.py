# select_sort.py
#
# Select Sort 直接选择排序算法
# Author:   Tau
# Date:     2018-06-06
#

def select_sort_once(unsorted_list, position):
    '''select_sort_once
    params:
        unsorted_list:总列表
        position:扫描位置
    returns:
        unsorted_list:总列表
    '''
    min = unsorted_list[position]
    min_idx = position
    for idx in range(position, len(unsorted_list)):
        if unsorted_list[idx] < min:
            min = unsorted_list[idx]
            min_idx = idx
    unsorted_list[min_idx] = unsorted_list[position]
    unsorted_list[position] = min
    print("DEBUG:", min_idx, unsorted_list)
    return unsorted_list

def select_sort(unsorted_list):
    '''select_sort
    parmas:
        unsorted_list
    returns:
        sorted_list
    '''
    for idx in range(0, len(unsorted_list)):
        unsorted_list = select_sort_once(unsorted_list, idx)
    return unsorted_list

if __name__ == "__main__":
    print(select_sort([
        2,3,1,2,31,2,321,21,34,12,2
        ]))