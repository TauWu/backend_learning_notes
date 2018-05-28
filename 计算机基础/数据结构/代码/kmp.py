# -*- coding: utf-8 -*-
# KMP模式匹配算法

def get_next(str_s):
    for ids in range(1, len(str_s)):
        idp = 0
        for p in str_s:
            if str_s[-ids-idp] == p:
                idp -= 1
                if ids+idp == 0:
                    yield len(str_s) - ids
                continue
            break
    yield 1

def get_next_num(str_s):
    '''计算偏移量
    '''
    next_list = [ids for ids in get_next(str_s)]
    if len(next_list) > 1: return next_list[1]
    return 1

def kmp(str_s, str_p):
    id_p = 0
    while True:
        p = 0
        for ids in range(len(str_s)):
            if str_s[ids] == str_p[id_p+p]:
                p += 1
                if ids+1 == len(str_s):
                    return True, id_p
                continue
            else:
                id_p += get_next_num(str_s[:ids])
                if id_p + len(str_s) > len(str_p):
                    return False, -1
                break


if __name__ == "__main__":
    print(kmp("abcabc", "eabeabcababcab"))