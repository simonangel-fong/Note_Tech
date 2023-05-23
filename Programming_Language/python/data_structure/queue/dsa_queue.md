# DSA - Queue

[Back](../../index.md)

- [DSA - Queue](#dsa---queue)
  - [Queue](#queue)
  - [Implement Queue in Python](#implement-queue-in-python)
  - [Problem: Queue](#problem-queue)
    - [Implement a Queue](#implement-a-queue)

---

## Queue

- `Queue`

  - an ordered collection of items where the addition of new items happens at one end, called the `rear`, and the removal of existing items occurs at the other end, commonly called the `front`.
  - As an element **enters** the queue it starts **at the rear** and makes its way toward the front, waiting until that time when it is the next element to be removed.

- The **most recently added item** in the queue must **wait at the end** of the collection. The item that has been in the collection **the longest** is **at the front**.

- `First-in first-out (FIFO)`
  - **first-come first-served**

![queue](./pic/queue.png)

- `Enqueue`

  - The term describes when a new item is **added to the rear** of the queue.

- `Dequeue`
  - The term describes removing the front item from the queue.

---

## Implement Queue in Python

```py
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

```

---

## Problem: Queue

### Implement a Queue

It's very common to be asked to implement a Queue class! The class should be able to do the following:

- Check if Queue is Empty
- Enqueue
- Dequeue
- Return the size of the Queue

[Implement a Queue](./problem_implement_queue.ipynb)

---

[TOP](#dsa---queue)
