# -*- coding: utf-8 -*-
# 两个排序数组的中位数

# 给定两个大小为 m 和 n 的有序数组 nums1 和 nums2 。
# 请找出这两个有序数组的中位数。要求算法的时间复杂度为 O(log (m+n)) 。
# 示例 1:
# nums1 = [1, 3]
# nums2 = [2]
# 中位数是 2.0
# 示例 2:
# nums1 = [1, 2]
# nums2 = [3, 4]
# 中位数是 (2 + 3)/2 = 2.5

def find_median_sorted_arrays(nums1, nums2):
    len1 = len(nums1)
    len2 = len(nums2)
    posi_c = (len1 + len2) / 2
    posi_a = int((posi_c) / 2)
    posi_b = int((posi_c) / 2)
    delta = nums1[posi_a] - nums2[posi_b]
    times = 0
    while True:
        times += 1
        print(times, "**", posi_a, posi_b, '=>',nums1[posi_a] ,nums2[posi_b])
        if times > 10:
            break

        if delta > 0:
            posi_b += int((posi_a+1) / 2)
            posi_a -= int((posi_a+1) / 2)
        else:
            posi_a += int((posi_b+1) / 2)
            posi_b -= int((posi_b+1) / 2)
        
        if delta < nums1[posi_a] - nums2[posi_b]:
            return nums1[posi_a] ,nums2[posi_b]
        else:
            delta = nums1[posi_a] - nums2[posi_b]

if __name__ == "__main__":
    find_median_sorted_arrays([1,13,31,41,51],[1,2,3,5,6,9,10])