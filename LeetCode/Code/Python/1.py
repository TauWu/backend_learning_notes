# -*- coding: utf-8 -*-
# 两数之和

# 给定一个整数数组和一个目标值，找出数组中和为目标值的两个数。
# 你可以假设每个输入只对应一种答案，且同样的元素不能被重复利用。
# 示例:
# 给定 nums = [2, 7, 11, 15], target = 9
# 因为 nums[0] + nums[1] = 2 + 7 = 9
# 所以返回 [0, 1]

def two_sum(nums, target):
    for idx, valx in enumerate(nums):
        for idy, valy in enumerate(nums[idx+1:]):
            if valx + valy == target:
                return idx, idx + idy + 1
    return -1, -1

if __name__ == "__main__":
    print(two_sum([0, 3, 0], 0))