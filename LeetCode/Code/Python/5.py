# -*- coding: utf-8 -*-
# 最长回文子串

# 给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为1000。

# 示例 1：
# 输入: "babad"
# 输出: "bab"
# 注意: "aba"也是一个有效答案。
# 示例 2：
# 输入: "cbbd"
# 输出: "bb"

def longest_palindrome(s):
    max_length = 0
    max_str = str()
    for idx in range(0, len(s)):
        for idy in range(0, len(s[idx:])+1):
            strs = s[idx:idx+idy]
            length = get_length_of_str(strs)
            if max_length < length:
                max_length = length
                max_str = strs
    return max_str

def get_length_of_str(s):
    length = len(s)
    while True:
        if len(s) <= 1:
            break
        if s[0] == s[-1]:
            s = s[1:-1]
        else:
            return 0
    return length
    
if __name__ == "__main__":
    # 本处代码可能需要优化
    s = longest_palindrome("abababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababa")
    print(s)