class Node:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def traverse(root, output=None):
    if output == None:
        output = []

    if root != None:
        if root.left != None:
            traverse(root.left, output)

        output.append(root.val)

        if root.right != None:
            traverse(root.right, output)

    return output


def trimBST(node, minVal, maxVal, last=None):

    if last == None:
        last = node
    # base case: node == None

    # recursive case
    if node != None:
        if minVal < node.val < maxVal:
            if not (node in [last.left, last.right]):  # 如果不是相邻
                if node.val < last.val:
                    last.left = node
                else:
                    last.right = node
            last = node
        else:
            last.left = last.right = None
        trimBST(node.left, minVal, maxVal, last)
        trimBST(node.right, minVal, maxVal, last)


root = Node(5, Node(3, right=Node(4)), Node(6, right=Node(7)))

sort_list = traverse(root)
print(sort_list)

trimBST(root, 3, 7)

# root = Node()
sort_list = traverse(root)
print(sort_list)
