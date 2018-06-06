# heap_sort.py
#
# Heap Sort 堆排序算法
# Author:   Tau
# Date:     2018-06-06
#

class Node():
    
    def __init__(self, data, left, right):
        self.data = data
        self.left_child = left
        self.right_child = right

class Tree():

    res = list()
    
    @staticmethod
    def preorder_traversal(d):

        if d.data is not None:
            if d.left_child is None:
                Tree.res.append(d.data)
            else:
                Tree.preorder_traversal(d.left_child)

            Tree.res.append(d.data)

            if d.right_child is None:
                Tree.res.append(d.data)
            else:
                Tree.preorder_traversal(d.right_child)

    @staticmethod
    def inorder_traversal(d):

        if d.data is not None:

            if d.left_child is None:
                Tree.res.append(d.data)
            else:
                Tree.preorder_traversal(d.left_child)

            Tree.res.append(d.data)

            if d.right_child is None:
                Tree.res.append(d.data)
            else:
                Tree.preorder_traversal(d.right_child)
        
    @staticmethod
    def postorder_traversal(d):

        if d.data is not None:
            if d.left_child is None:
                Tree.res.append(d.data)
            else:
                Tree.preorder_traversal(d.left_child)

            Tree.res.append(d.data)
            
            if d.right_child is None:
                Tree.res.append(d.data)
            else:
                Tree.preorder_traversal(d.right_child)
            
def trans_list_to_tree(num_list):
    '''将列表转换为完全二叉树
    '''
    node_list = list()
    idx = 0
    for num in num_list:
        node = Node(num, Node(None, None, None), Node(None, None, None))
        node_list.append(node)
        if idx >= 1:
            if idx%2 == 1:
                node_list[int(idx/2)].left_child = node
            elif idx%2 == 0:
                node_list[int(idx/2)-1].right_child = node
        idx += 1
    return node_list

if __name__ == "__main__":
    
    tree_data = trans_list_to_tree([
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        11,12,13,14,15,16,17,18,19,20,
        21,22,23,24,25,26,27,28,29,30,
        31,32,33,34,35,36,37,38,39,40
    ])
    Tree.preorder_traversal(tree_data[0])
    print(Tree.res, '\n')
    Tree.res=list()
    Tree.inorder_traversal(tree_data[0])
    print(Tree.res, '\n')
    Tree.res=list()
    Tree.postorder_traversal(tree_data[0])
    print(Tree.res, '\n')