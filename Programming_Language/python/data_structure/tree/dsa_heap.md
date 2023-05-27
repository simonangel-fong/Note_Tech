# DSA - Heap

[Back](../../index.md)

- [DSA - Heap](#dsa---heap)
  - [Heap](#heap)
  - [Binary heap](#binary-heap)
  - [Heap Operation](#heap-operation)
    - [Insert](#insert)
    - [Extract](#extract)
    - [Heap implementation in Python](#heap-implementation-in-python)

---

- 总结:
  - 本质上是 binary tree
  - 作用和目的:
    - 实现 priority queue
  - 实现方法:
    - 使用 list
    - 利用父子节在数组 index 上的关系

---

## Heap

- `Heap`
  - a specialized **tree-based data structure** which is essentially an **almost `complete binary tree`** that satisfies the heap property.
- The heap is **one maximally efficient implementation** of `priority queue`.
- However, a `heap` is **not a sorted structure**; it can be regarded as being **partially ordered**.
- A heap is a useful data structure when it is necessary to **repeatedly remove the object with the highest (or lowest) priority**, or when insertions need to be interspersed with **removals of the root node**.
- max heap
  - , for any given node C, if P is a parent node of C, then the key (the value) of P is greater than or equal to the key of C.
- `min heap`, the key of P is less than or equal to the key of C.[2] The node at the "top" of the heap (with no parents) is called the root node.

- A **common implementation of a heap** is the `binary heap`, in which the tree is a binary tree (see figure).
- Heaps are also crucial in several efficient `graph algorithms` such as Dijkstra's algorithm.

- When a heap is a complete binary tree, it has a smallest possible height—a heap with N nodes and a branches for each node always has loga N height.

---

## Binary heap

- `Binary Heaps`

  - a **heap data structure** that takes the form of a **binary tree**.
  - a common way of implementing priority queues.
  - allow us both enqueue and dequeue items **in O(logn)**.

- A `binary heap` is defined as a binary tree **with two additional constraints**:

  - **Shape property**:

    - a binary heap is a `complete binary tree`
    - all **levels** of the tree, except possibly the last one (deepest) are **fully filled**, and, if the **last level** of the tree is not complete, the nodes of that level are **filled from left to right**.

  - **Heap property**:
    - the **key** stored in each node is either greater than or equal to (≥) or less than or equal to (≤) the keys in the node's **children**, according to some total order.

- `max-heap`

  - a heap where the _parent key_ is **greater than or equal to (≥)** the _child keys_

- `min heap`

  - a heap where _parent key_ is **less than or equal to (≤)** the _child keys_

---

## Heap Operation

- Both the insert and remove operations modify the heap to **conform to the shape property first**, by adding or removing from the **end** of the heap.
- Then the heap property is restored by **traversing up or down** the heap.
- Both operations take `O(log n)` time.

---

### Insert

- To add an element to a heap, we can perform this algorithm:

  - 1. Add the element to the **bottom level** of the heap at the **leftmost** open space.
  - 2. **Compare** the added element with its parent; if they are in the correct order, stop.
  - 3. If not, **swap** the element with its parent and return to the previous step.

- Steps 2 and 3, which restore the heap property by comparing and possibly swapping a node with its parent, are called the `up-heap` operation (also known as bubble-up, percolate-up, sift-up, trickle-up, swim-up, heapify-up, or cascade-up).

- The number of operations required **depends only on the number of levels** the new element must rise to satisfy the heap property.
  - Thus, the insertion operation has a **worst-case time complexity** of `O(log n)`.
  - For a random heap, and for repeated insertions, the insertion operation has an **average-case complexity** of `O(1)`.

---

### Extract

- The procedure for deleting the root from the heap while retaining the heap property is as follows:

  - 1. **Replace** the root of the heap with the **last** element on the **last level**.
  - 2. **Compare** the new root with its children; if they are in the correct order, stop.
  - 3. If not, **swap** the element with one of its children and return to the previous step.

- Steps 2 and 3, which **restore the heap property** by comparing and possibly swapping a node with one of its children, are called the `down-heap` (also known as bubble-down, percolate-down, sift-down, sink-down, trickle down, heapify-down, cascade-down, extract-min or extract-max, or simply heapify) operation.

- In the **worst case**, the new root has to be swapped with its child on each level until it reaches the bottom level of the heap, meaning that the delete operation has a **time complexity relative to the height of the tree**, or `O(log n)`.

---

### Heap implementation in Python

- A small complete binary tree stored in an **array**

- No space is required for pointers; instead, the **parent** and **children** of each node can be found **by arithmetic on array indices**.
- 因为 min-heap 的定义, **任意 parent 都等于或小于其后代**.

- **Start index**: `1`

  - Index of array in Python is starts with `0`.
  - However, starting with `1` make it easier to determine the left child of each node, that is 2,4,8, ..., 2i.

- **Initial internal Array**: `arr = [0]`

  - reason as above

- **Size**: `len(array)`

  - since the actual index start with `1`

- For a given current node: `arr[i]`

  - **Children**: `arr[2i]` and `arr[2i+1]`

    - Condition when current node is a leaf, without child: `arr[2i]>size`
    - Condition when it only has one child: `arr[2i] == size`
    - Condition when it has two children: `arr[2i+1] <= size`

  - **Parent**: `arr[i//2]`

    - Condition when its parent is **Root**: `[i//2]=0`
    - Condition when its parent is not **Root**: `[i//2]>0`

- For a array with given length `n`:

  - **Root**: `arr[1]`
  - **Last leaf**: `arr[n]`
  - **Last parent**: `arr[n//2]`

- `heap-up`:

  - to restore the **heap property** by comparing and possibly swapping a node with its parent
  - happen when inserting a new node and with one side of binary heap
  - 因为只需要判定二叉堆的一侧, 所以向上迭代时, 步长是 i//2, 即寻找当前 node 的父 node 即可, 直到当前 node 是 root, 即 i//2>0

  ```py
  while i//2>0: # loop before root
    # swap operation

    i//2 # step
  ```

- `heap-down`:

  - to **restore the heap property** by comparing and possibly swapping a node with one of its children
  - happen when deleting the root and replace with the last node, or building a binary heap with an unordered list.
  - 删除时是 swap root, 所以 wost case 是全部都要换.
  - 对任意 node`arr[i]`, 需要检查的从自身到最后一个 parent node, 即 2\*i >size.
  - 由于 swap 只可能发生于 children 中的最小值, 所以需要找出最小值的 child, 并将该 child 作为下个迭代对象.

  ```py
  i = 1 # root
  while 2*i >size: # until last parent node
    # find min_node
    i = min_node # pass min_node for the next iteration
  ```

- **build heap**

  - build from an unorder array
  - need to check each parent whether it is less than its children, 所以需要对所有 parent 进行 heap-down.(如果是已排序的, 则无需检查)
  - 实际上对每个 parent 都进行 heap-down

  ```py
  i = len(para_list)//2 # get the index of the last parent
  while i>0: # loop until root
    heap_down(i) # heap down from the current parent

    i -=1  # step is 1, means step is 2 in the term of n

  ```

```py
class binary_heap(object):

    def __init__(self):
        self.heap_array = [0]  # start with 0 make it easy to implement
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def getSize(self):
        return self.size

    def insert(self, item):
        self.heap_array.append(item)
        self.size += 1
        self.heap_up(self.size)

    def heap_up(self, index):

        # loop from the lastest parent until root
        while index//2 > 0:

            # if child < parent, then swap
            if self.heap_array[index] < self.heap_array[index//2]:
                temp = self.heap_array[index]
                self.heap_array[index] = self.heap_array[index // 2]
                self.heap_array[index//2] = temp

            index = index//2  # update index with next parent for next iteration

    def extract(self):
        root_val = self.heap_array[1]

        self.heap_array[1] = self.heap_array[self.size]  # swap with the last
        self.size -= 1
        self.heap_array.pop()
        self.heap_down(1)           # heap down from the top
        self.heap_down(self.size)

        return root_val

    def heap_down(self, index):
        # loop children util leaf
        while (index * 2) < self.size:

            # get the index of min child
            min_index = self.get_minChild(index)

            # compare currunt parent with min child, then swap
            if self.heap_array[index] > self.heap_array[min_index]:

                temp = self.heap_array[index]
                self.heap_array[index] = self.heap_array[min_index]
                self.heap_array[min_index] = temp

            index = min_index  # set current parent as min child after swap for next iteration

    def get_minChild(self, index):
        '''invoke this function provided that current node has at least one child'''

        # if current node only has left child, then return left child
        if index * 2 == self.size:
            return index*2
        # if has two child, compare, then return min child
        else:
            if self.heap_array[2*index] < self.heap_array[2*index + 1]:
                return 2*index
            else:
                return 2*index + 1

    def create_heap(self, para_list):
        self.size = len(para_list)
        self.heap_array = [0] + para_list

        # get the last parent
        last_parent = self.size // 2

        # loop parents until root
        while last_parent > 0:
            # for each parent, heap down
            self.heap_down(last_parent)
            last_parent -= 1


print("\n--------create binary heap--------\n")

bh = binary_heap()
print(bh.heap_array)            # [0]

bh.create_heap([9, 7, 5, 4, 2])

print(bh.heap_array)            # [0, 2, 4, 5, 9, 7]

bh.insert(11)
bh.insert(1)
print(bh.heap_array)            # [0, 1, 4, 2, 9, 7, 11, 5]

print(bh.extract())
print(bh.heap_array)            # [0, 2, 4, 5, 9, 7, 11]

print(bh.getSize())             # 6

```

---

[TOP](#dsa---heap)
