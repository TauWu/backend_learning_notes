# -*- coding: utf-8 -*-
# 冒泡排序算法

UnSortedList = [
    12, 13, 14, 15,
    1,  1,  2,  20,
    58, 27, 41, 33
]

def bubble_sort(unsorted_list):
    '''bubble_sort
    Main Function includes many tries of single function.
    '''
    res, res_list = bubble_sort_single(unsorted_list)
    idx = 1
    while True:
        print("Result of [%d] try is: %s."%(idx, res_list))
        res, res_list = bubble_sort_single(res_list)
        idx += 1
        if res:
            break
    print("Final result is %s."%res_list)


def bubble_sort_single(temp_list):
    '''bubble_sort_single
    Scan the list from params, and return a scaned list.
    '''
    bubble_sort_res = True
    for idx in range(len(temp_list)-1):
        res, temp_list = scan_single(temp_list, idx)
        if not res:
            bubble_sort_res = False
    return bubble_sort_res, temp_list


def scan_single(temp_list, idx):
    '''scan_single
    Scan the single element from list, return the temp list and the result.
    '''
    if idx >= len(temp_list) - 1 :
        raise ValueError("The idx for scan function is lagger than the length of list.")

    res = True
    if temp_list[idx] > temp_list[idx+1]:
        temp_list = swap(temp_list, idx, idx+1)
        res = False
    return res, temp_list

def swap(temp_list, idx, idy):
    '''swap
    Swap the elements between idx and idy.
    '''
    elex = temp_list[idx]
    eley = temp_list[idy]
    temp_list[idx] = eley
    temp_list[idy] = elex
    return temp_list

if __name__ == "__main__":
    bubble_sort(UnSortedList)