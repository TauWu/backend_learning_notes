# -*- coding: utf-8 -*-
# 无重复字符的最长子串

# 给定一个字符串，找出不含有重复字符的最长子串的长度。
# 示例：
# 给定 "abcabcbb" ，没有重复字符的最长子串是 "abc" ，那么长度就是3。
# 给定 "bbbbb" ，最长的子串就是 "b" ，长度是1。
# 给定 "pwwkew" ，最长子串是 "wke" ，长度是3。请注意答案必须是一个子串，"pwke" 是 子序列  而不是子串。

def length_of_longest_substring(s):
    max_length = 0
    # sub_str_list = list()
    for idx in range(0, len(s)):
        sub_str_list = list()
        length = 0
        
        while True:
            try:
                if s[length+idx] not in sub_str_list:
                    sub_str_list.append(s[length+idx])
                    length += 1
                else:
                    break

            except Exception:
                break

            if max_length < length:
                max_length = length    
    return max_length

if __name__ == "__main__":
    print(length_of_longest_substring("c"))