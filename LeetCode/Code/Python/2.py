# -*- coding: utf-8 -*-
# 两数相加

# 给定两个非空链表来表示两个非负整数。位数按照逆序方式存储，它们的每个节点只存储单个数字。将两数相加返回一个新的链表。

# 你可以假设除了数字 0 之外，这两个数字都不会以零开头。

# 示例：

# 输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
# 输出：7 -> 0 -> 8
# 原因：342 + 465 = 807

class ListNode:

    def __init__(self, x):
        self.val = x
        self.next = None

def add_two_numbers(l1, l2):
    flag = 0
    l = ListNode(0)
    s = l
    while l1 is not None or l2 is not None:
        if l1 is None: l1 = ListNode(0)
        if l2 is None: l2 = ListNode(0)
            
        val = l1.val + l2.val + flag
        flag = 0
        
        if val > 9:
            val = val%10
            flag = 1

        if l1 is not None: l1 = l1.next
        if l2 is not None: l2 = l2.next

        node = ListNode(val)

        l.next = node
        l = l.next
    
    if flag == 1:
        l.next = ListNode(1)

    return s.next

def create_linklist(l):
    rl = ListNode(0)
    s = rl
    for val in l:
        rl.next = ListNode(val)
        rl = rl.next
    return s.next

if __name__ == '__main__':

    l1 = create_linklist([5])
    l2 = create_linklist([5])

    res = add_two_numbers(l1, l2)
    while res is not None:
        print(res.val, end=' ')
        res = res.next