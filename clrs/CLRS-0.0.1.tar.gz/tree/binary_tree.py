class Node(object):
    def __init__(self, key=None, parent=None, lchild=None, rchild=None):
        self.key = key
        self.lchild = lchild
        self.rchild = rchild
        self.parent = parent

    def __repr__(self):
        return "({key} {lchild} {rchild})".format(key=self.key, lchild=self.lchild, rchild=self.rchild)


def _tree_search(node, key):
    if node == None or key == node.key:
        return node
    if key < node.key:
        return _tree_search(node.lchild, key)
    else:
        return _tree_search(node.rchild, key)


def _inorder_tree_walk(node):
    if node:
        return _inorder_tree_walk(node.lchild) + [node.key] + _inorder_tree_walk(node.rchild)
    else:
        return []


class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    def __repr__(self):
        return self.root.__repr__()

    def insert(self, node):
        y = None
        x = self.root
        while x:
            y = x
            if node.key < x.key:
                x = x.lchild
            else:
                x = x.rchild
        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.lchild = node
        else:
            y.rchild = node

    def successor(self, node):
        if node.rchild:
            node = node.rchild
            while node.lchild:
                node = node.lchild
            return node
        y = node.parent
        while y and node == y.rchild:
            node = y
            y = y.parent
        return y


    def delete(self, node):
        if node.lchild == None or node.rchild == None:
            y = node
        else:
            y = self.successor(node)
        if y.lchild:
            x = y.lchild
        else:
            x = y.rchild
        if x:
            x.parent = y.parent
        if y.parent == None:
            self.root = x
        elif y == y.parent.lchild:
            y.parent.lchild = x
        else:
            y.parent.rchild = x
        if y != node:
            node.key = y.key
        return y

    def inorder_tree_walk(self):
        return _inorder_tree_walk(self.root)

    def search(self, key):
        return _tree_search(self.root, key)

    def minimum(self):
        node = self.root
        while node.lchild:
            node = node.lchild
        return node

    def maximum(self):
        node = self.root
        while node.rchild:
            node = node.rchild
        return node


if __name__ == '__main__':
    import random

    tree = BinarySearchTree()
    N = 10
    array = list(range(N))
    random.shuffle(array)
    for i in array:
        tree.insert(Node(i))
    print(tree)
    tree.delete(tree.search(2))
    print(tree.inorder_tree_walk())