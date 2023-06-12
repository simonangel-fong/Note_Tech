class Stack(object):
    def __init__(self):
        self.items = []

    def push(self, obj):
        self.items.append(obj)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)


print("\n--------Create--------\n")
s = Stack()

print("isEmpty\t", s.isEmpty())     # isEmpty  True


print("\n--------Add--------\n")

s.push(1)
s.push("two")

print("peek\t", s.peek())               # peek     two
print("size\t", s.size())               # size     2
print("isEmpty\t", s.isEmpty())         # isEmpty  False


print("\n--------Remove--------\n")

print("pop\t", s.pop())                 # pop      two
print("pop\t", s.pop())                 # pop      1

print("size\t", s.size())               # size     0
print("isEmpty\t", s.isEmpty())         # isEmpty  True
