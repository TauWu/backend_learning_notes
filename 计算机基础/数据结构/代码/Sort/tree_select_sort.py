# tree_select_sort.py
#
# Tree Select Sort 树型选择排序算法
# Author:   Tau
# Date:     2018-06-06
#

def get_min(unsorted_list):
    raw = unsorted_list[:]
    # print("RAW DEBUG:", raw)
    if len(raw) <= 1:
        return raw
    while True:
        idx = 0
        for idx in range(0, int(len(unsorted_list)/2)):
            if unsorted_list[2*idx] > unsorted_list[2*idx+1]:
                unsorted_list[idx] = unsorted_list[2*idx+1] 
            else:
                unsorted_list[idx] = unsorted_list[2*idx]
        if len(unsorted_list)%2 == 0:
            unsorted_list = (unsorted_list[:int(len(unsorted_list)/2)])
        else:
            unsorted_list[idx+1] = unsorted_list[-1]
            unsorted_list = (unsorted_list[:int(len(unsorted_list)/2)+1])
        print("DEBUG:", unsorted_list)
        if len(unsorted_list) <= 1:
            break
    posi = raw.index(unsorted_list[0],0)
    raw[posi] = raw[0]
    raw[0] = unsorted_list[0]
    # print("RAW DEBUG:", posi, raw)
    return raw

def tree_select_sort(unsorted_list):
    for idx in range(0, len(unsorted_list)):
        unsorted_list[idx:] = get_min(unsorted_list[idx:])
    return unsorted_list

if __name__ == "__main__":
    sort_iter = tree_select_sort(
        [12,231,12,23,2,13,123,24,123,123,42,12,31,42,123,41]
    )
    print("RES:", sort_iter)