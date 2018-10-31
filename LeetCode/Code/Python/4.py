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
    m = len(nums1)
    n = len(nums2)

    if m > n :
        m, n, nums1, nums2 = n, m, nums2, nums1

    imin, imax, half = 0, m, int((m+n+1)/2)

    while imin <= imax:

        i = int((imin+imax)/2)
        j = half - i

        if i<n and nums2[j-1] > nums1[i]:
            print("****", i, imin, imax, nums2[j-1], nums1[i])
            imin = i + 1
        elif i<m and nums1[i-1] > nums2[j]:
            print(">>>>", i, imin, imax, nums1[i-1], nums2[j])
            imax = i - 1
        else:

            if i == 0: max_of_left = nums2[j-1]
            elif j == 0: max_of_left = nums1[i-1]
            else: max_of_left = max(nums1[i-1], nums2[j-1])

            print(max_of_left)

            if (m+n)%2 == 1:
                return max_of_left

            if i == m: min_of_right = nums2[j]
            elif j == n: min_of_right = nums1[j]
            else: min_of_right = min(nums1[i], nums2[j])

            print(min_of_right)
            return (max_of_left + min_of_right) / 2.0

if __name__ == "__main__":
    res = find_median_sorted_arrays([1,13,31,41,51],[1,2,3,5,6,9,10])
    print(res)