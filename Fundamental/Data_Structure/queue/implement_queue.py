class Queue(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[0]

    def push(self, obj):
        self.items.append(obj)

    def pop(self):
        return self.items.pop(0)


print("\n--------Create--------\n")
s = Queue()

print("isEmpty\t", s.isEmpty())         # isEmpty  True


print("\n--------Add--------\n")

s.push(1)
s.push("two")             

print("peek\t", s.peek())               # peek     1
print("size\t", s.size())               # size     2
print("isEmpty\t", s.isEmpty())         # isEmpty  False


print("\n--------Remove--------\n")

print("pop\t", s.pop())                 # pop      1
print("pop\t", s.pop())                 # pop      two

print("size\t", s.size())               # size     0
print("isEmpty\t", s.isEmpty())         # isEmpty  True
