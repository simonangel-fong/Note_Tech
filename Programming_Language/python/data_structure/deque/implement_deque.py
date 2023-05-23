class Deque(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def AddFront(self, obj):
        self.items.insert(0, obj)

    def addRear(self, obj):
        self.items.append(obj)

    def removeFront(self):
        return self.items.pop(0)

    def removeRear(self):
        return self.items.pop()


print("\n--------Create--------\n")
d = Deque()

print("isEmpty\t", d.isEmpty())         # isEmpty  True


print("\n--------Add--------\n")

d.addRear(1)
d.AddFront("two")

print("size\t", d.size())               # size     2
print("isEmpty\t", d.isEmpty())         # isEmpty  False


print("\n--------Remove--------\n")

print("removeFront\t", d.removeFront())     # removeFront      two
print("removeRear\t", d.removeRear())       # removeRear       1

print("size\t", d.size())                   # size     0
print("isEmpty\t", d.isEmpty())             # isEmpty  True
