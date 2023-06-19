class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None    # the pointer to the next node


class Linked_list(object):
    def __init__(self, value):
        new_node = Node(value)
        # By default, the head and tail of a LL is the first the node
        self.head = new_node
        self.tail = new_node

        self.length = 1

    def print_linked_list(self):

        # craete a temporary pointer and initiate by pointing to the head.
        temp = self.head

        # loop until the tail, whose next node is None.
        while temp is not None:
            print(temp.value)
            # update the temporary pointer by pointing to the next node.
            temp = temp.next

    def append(self, value):
        new_node = Node(value)

        # when the current linked list is empty, then update head and tail
        if self.head is None:
            self.head = new_node
            self.tail = new_node

        # when the current linked list is not empty, then update tail pointer
        else:
            self.tail.next = new_node   # update the next point of current tail node
            self.tail = new_node        # set the tail point as the new node

        self.length += 1

        return True

    def pop(self):

        # when LL is empty
        if self.length == 0:
            return None

        # when LL is not empty
        # initialize helping variables
        current = pre = self.head

        # loop LL until the current is the tail, whose next is None
        # when LL has only one node, that is head equal to tail, loop wont run
        while current.next:
            pre = current
            current = current.next

        self.tail = pre
        self.tail.next = None
        self.length -= 1     # update length

        # when LL has only one node, the length is 0, then set both head and tail as None
        if self.length == 0:
            self.head = None
            self.tail = None

        return current

    def prepend(self, value):

        new_node = Node(value)

        # when LL is empty, then set head and tail both as new node
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        # when LL is not empty, then update head
        else:
            new_node.next = self.head
            self.head = new_node

        self.length += 1

        return True

    def pop_first(self):
        # when LL is empty, then return None
        if self.length == 0:
            return None

        # when LL is not empty, then update head
        temp = self.head
        self.head = self.head.next  # when LL has only one node, head next = None
        temp.next = None
        self.length -= 1

        # when LL is empty after pop, set tail as None
        if self.length == 0:
            self.tail = None

        return temp

    def get(self, index):

        if index < 0:
            raise Exception("invalid index")

        if index >= self.length:
            raise Exception("index out of bound")

        current = self.head
        # 该处使用for loop, 是因为以上代码已经排除了非法index, 所以只需循环指定次数即可
        # 该处使用下划线, 是因为循环中不需要for loop的标记; 如果需要使用, 一般使用for i in range()
        for _ in range(index):
            current = current.next      # 因为range是exclusive, 所以最后的current所在的是index node的前一个node
        return current

    def set_value(self, index, value):
        # the invalid index will trigger exception in the get method
        current = self.get(index)
        current.value = value
        return True

    def insert(self, index, value):
        
        # when index is invalid
        if index < 0 or index > self.length:
            return False

        # when value is added at the beginning
        if index == 0:
            return self.prepend(value)
        
        # when value is added at the end
        if index == self.length:
            return self.append(value)
        
        # when value is added at neither the beginning nor the end
        new_node = Node(value)

        # get the previous node
        pre_node = self.get(index-1)

        new_node.next = pre_node.next       # set new node next
        pre_node.next = new_node            # set pre node next
        
        self.length +=1
        return True
    
    def remove(self, index):
        
        # when index is invalid
        if index < 0  or index >= self.length:
            return None

        # when value is added at the beginning
        if index == 0:
            return self.pop_first()
        
        # when value is added at the end
        if index == self.length-1:
            return self.pop()
        
        # the invalid index will trigger exception in the get() method
        # get the previous node
        pre_node = self.get(index-1)
        current = pre_node.next
        
        pre_node.next = current.next        # set pre node next
        current.next = None                 # set current node next

        self.length -=1

        return current
        

    def reverse(self):

        current = self.head
        prev = None
        while current is not None:

            temp_next = current.next
            current.next = prev
            
            prev = current
            current = temp_next

        self.head, self.tail = self.tail, self.head



        


ll = Linked_list(4)
ll.append(5)
ll.append(6)
ll.append(7)
ll.print_linked_list()

ll.reverse()
ll.print_linked_list()
