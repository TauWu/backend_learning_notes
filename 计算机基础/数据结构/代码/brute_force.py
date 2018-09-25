# -*- coding: utf-8 -*-
# BF模式匹配算法

def Index(str_s, str_p):
    idx = 0                 # 记录匹配到哪一个字符
    max_idx = len(str_p)
    ids = 0                 # 记录匹配上的字符个数
    max_ids = len(str_s)
    for idx in range(0, max_idx):
        idp = 0
        if idx > max_idx - max_ids:
            return False, -1
        for ids in range(0, max_ids):
            if str_p[idx+idp] == str_s[ids]:
                idp += 1
                # 运行到与子串长度相同的情况
                if ids+1 == max_ids:
                    return True, idx
                continue
            else:
                break

if __name__ == "__main__":
    print(Index("abc","abc12bsda"))