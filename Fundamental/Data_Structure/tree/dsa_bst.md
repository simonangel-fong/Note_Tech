# DSA - Binary Search Tree

[Back](../index.md)

- [DSA - Binary Search Tree](#dsa---binary-search-tree)
  - [Binary Search Tree](#binary-search-tree)
  - [The complexity](#the-complexity)
  - [Implement in Python: Linked List](#implement-in-python-linked-list)
    - [Constructor](#constructor)
    - [Insert(): `O(log(n))`](#insert-ologn)
    - [Contains(): `O(log(n))`](#contains-ologn)
  - [Implement in Python: OOP](#implement-in-python-oop)

---

## Binary Search Tree

- `Binary Search Tree (BST)`

  - an ordered or sorted **binary tree**
  - a rooted binary tree data structure in which the value of **left** node must be **smaller** than the parent node, and the value of **right** node must be **greater** than the parent node.
  - This rule is applied **recursively** to the left and right subtrees of the root.

- **Advantages**
  - **Searching** an element in the Binary search tree is easy as we always have a hint that which subtree has the desired element.
  - As compared to array and linked lists, **insertion** and **deletion** operations are **faster** in BST.

---

## The complexity

We will see the time complexity for insertion, deletion, and searching operations in best case, average case, and worst case.

1. Time Complexity

   | Operations | Best case time complexity | Average case time complexity | Worst case time complexity |
   | ---------- | ------------------------- | ---------------------------- | -------------------------- |
   | Insertion  | O(log n)                  | O(log n)                     | O(n)                       |
   | Deletion   | O(log n)                  | O(log n)                     | O(n)                       |
   | Search     | O(log n)                  | O(log n)                     | O(n)                       |

Where 'n' is the number of nodes in the given tree.

- 推导: search()
  - 因为是每层二分, 所以最理想情况下(树是 perfect, full, complete)层数/搜索次数 O 有:`2^O -1 = n`
  - 对以上简化并取对数, `O(log(n))`.该处 log 的底是 2.
  - 对坏的情况是所有元素单边延续, 即实际上是 sll, 所以层数/搜索次数是`O(n)`

1. Space Complexity

   | Operations | Space complexity |
   | ---------- | ---------------- |
   | Insertion  | O(n)             |
   | Deletion   | O(n)             |
   | Search     | O(n)             |

The space complexity of all operations of Binary search tree is O(n).

---

对比

| Operation | SLL      | BST           |
| --------- | -------- | ------------- |
| insert()  | **O(1)** | O(log(n))     |
| lookup()  | O(n)     | **O(log(n))** |
| remove()  | O(n)     | **O(log(n))** |

---

## Implement in Python: Linked List

### Constructor

```py
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
```

---

### Insert(): `O(log(n))`

```py
 def insert(self, value):
   new_node = Node(value)
   if self.root is None:
      self.root = new_node
      return True
   temp = self.root
   while (True):
      if new_node.value == temp.value:
          return False
      if new_node.value < temp.value:
          if temp.left is None:
              temp.left = new_node
              return True
          temp = temp.left
      else:
          if temp.right is None:
              temp.right = new_node
              return True
          temp = temp.right
```

---

### Contains(): `O(log(n))`

```py
def contains(self, value):
   temp = self.root
   while (temp is not None):
      if value < temp.value:
          temp = temp.left
      elif value > temp.value:
          temp = temp.right
      else:
          return True
   return False
```

---

## Implement in Python: OOP

- 使用 OOP 方法

```py

class TreeNode:

    # 构造函数, 接受参数
    def __init__(self,key,val,left=None,right=None,parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    # 检查是否有 left child
    def hasLeftChild(self):
        return self.leftChild

    # 检查是否有 right child
    def hasRightChild(self):
        return self.rightChild

    # whether the current node is the left child of its parent
    # if current node is not root and it is the left node of its parent
    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    # whether the current node is the right child of its parent
    # if current node is not root and it is the right node of its parent
    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    # whether current is root
    # if parent is none
    def isRoot(self):
        return not self.parent

    # if has no child
    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    # has either child or both, retun true
    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    # whether has both
    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    # for given child, if child is not none, then bind child to current node.
    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

```

- Class to create BST

```py

class BinarySearchTree:

    # construct an empty bst
    def __init__(self):
        self.root = None
        self.size = 0

    # size
    def length(self):
        return self.size

    # can use len() function
    def __len__(self):
        return self.size

    # can use index to insert
    def __setitem__(self,k,v):
        self.put(k,v)

    # can use index to retrieve
    def __getitem__(self,key):
        return self.get(key)

    # can use 'in' operator
    def __contains__(self,key):
        if self._get(key,self.root):
            return True
        else:
            return False

    # can use 'del' expression
    def __delitem__(self,key):

        self.delete(key)


    # retrieve the value of a given key, from root
    def get(self,key):

        # if has root
        if self.root:

            # call _get to retieve node from root
            res = self._get(key,self.root)
            if res:
                return res.payload
            else:
                return None
        # if has no root, return none
        else:
            return None

    # retrieve value from current node
    def _get(self,key,currentNode):

        # base case: if the current Node is None,  return
        if not currentNode:
            return None
        # if equal, return current node
        elif currentNode.key == key:
            return currentNode
        # if less, recursive call left
        elif key < currentNode.key:
            return self._get(key,currentNode.leftChild)
        # if more, recursive call right
        else:
            return self._get(key,currentNode.rightChild)

    # insert a new key from the root
    def put(self,key,val):

        # if has root, then call _put() to insert key from root
        if self.root:
            self._put(key,val,self.root)

        # if has not root, create a Treenode as root, size increment
        else:
            self.root = TreeNode(key,val)
        self.size = self.size + 1

    # insert a new key from a current node
    def _put(self,key,val,currentNode):

        # if less, check whether has lef child
        #   - if has, recursively insert
        #   - if has no, create a new node, set its parent as current node
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                   self._put(key,val,currentNode.leftChild)
            else:
                   currentNode.leftChild = TreeNode(key,val,parent=currentNode)

        # if more, check whether has right child
        #   - if has, recursively insert
        #   - if has no, create a new node, set its parent as current node
        else:
            if currentNode.hasRightChild():
                   self._put(key,val,currentNode.rightChild)
            else:
                   currentNode.rightChild = TreeNode(key,val,parent=currentNode)

    # delete a node matching key
    def delete(self,key):

        # if has node other than root
        if self.size > 1:

            # find the node
            nodeToRemove = self._get(key,self.root)
            # if the node is not None
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size-1
            # if node is none, error
            else:
                raise KeyError('Error, key not in tree')
        # if only has root
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        # if is empty
        else:
            raise KeyError('Error, key not in tree')


    #
    def spliceOut(self):

        # if current node has no child
        if self.isLeaf():
            # if current node is parent's leftchild
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        # if has any child
        elif self.hasAnyChildren():
            # if has left child
            if self.hasLeftChild():
                # if it is left child of its parent
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                # if it is right child
                else:
                    self.parent.rightChild = self.leftChild
                    self.leftChild.parent = self.parent
        else:
            if self.isLeftChild():

                self.parent.leftChild = self.rightChild
            else:
                self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

    def findSuccessor(self):

        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:

                if self.isLeftChild():

                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ

    def findMin(self):

        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def remove(self,currentNode):

        if currentNode.isLeaf(): #leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren(): #interior

            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload

        else: # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:

                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                    currentNode.leftChild.payload,
                                    currentNode.leftChild.leftChild,
                                    currentNode.leftChild.rightChild)
            else:

                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                    currentNode.rightChild.payload,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild)


```

---

[TOP](#dsa---binary-search-tree)
