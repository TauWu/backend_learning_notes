# quick_sort.py
#
# Quick Sort 快速排序算法
# Author:   Tau
# Date:     2018-06-05
#

sorted_list = list()

def quick_sort(unsorted_list):
    '''quick_sort
    params:
        unsorted_list:乱序序列
    returns:
        一棵有序的树
    '''
    
    if len(unsorted_list) >= 1:
        cursor = unsorted_list[0]
        upper_list = list()
        down_list = list()
        for ele in unsorted_list[1:]:
            if ele <= cursor:
                down_list.append(ele)
            else:
                upper_list.append(ele)
        res_down = quick_sort(down_list)
        res_upper = quick_sort(upper_list)
        return res_down, cursor, res_upper

def display_tree(quick_sort_res):
    '''display_tree
        有序树的中序遍历
    '''
    left_son = quick_sort_res[0]
    root = quick_sort_res[1]
    right_son = quick_sort_res[2]
    if left_son:
        display_tree(left_son)
    sorted_list.append(root)
    if right_son:
        display_tree(right_son)
        

if __name__ == "__main__":
    display_tree(quick_sort([2,4,2,4,6,2,34,23,23,43,12]))
    print(sorted_list)