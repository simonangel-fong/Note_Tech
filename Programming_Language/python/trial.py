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
