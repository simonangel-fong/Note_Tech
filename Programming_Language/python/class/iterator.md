# Python - Iterators

[Back](../index.md)

- [Python - Iterators](#python---iterators)
  - [Iterators](#iterators)
    - [Create an Iterator](#create-an-iterator)
    - [StopIteration](#stopiteration)

---

## Iterators

- An `iterator` is an object that **contains a countable number of values.**

  - An iterator is an object that can be iterated upon, meaning that it can traverse through all the values.

- Technically, in Python, an iterator is an object which **implements the iterator protocol**, which consist of the methods `__iter__()` and `__next__()`.

- **Iterator vs Iterable**

  - `Lists`, `tuples`, `dictionaries`, and `sets` are all **iterable objects**. They are **iterable containers** which you can get an iterator from.
  - All these objects have a `iter()` method which is used to **get an iterator**
  - `strings` are iterable objects, and can return an `iterator`.

- **Looping Through an Iterator**
  - The `for` loop actually creates an `iterator object` and executes the `next()` method for each loop.

```py

print("\n--------Iterator--------\n")
xTuple = ("apple", "banana", "cherry")
yIter = iter(xTuple)

print(next(yIter))          # apple
print(next(yIter))          # banana
print(next(yIter))          # cherry


xStr = "banana"
xIter = iter(xStr)

print(next(xIter))          # b
print(next(xIter))          # a
print(next(xIter))          # n
print(next(xIter))          # a
print(next(xIter))          # n
print(next(xIter))          # a


print("\n--------Loop--------\n")
xlist=[1,2,3,4]
iter = iter(xlist)      # get an iterator
for x in iter:          # executes the `next()` method for each loop
    print (x, end=" ")

```

---

### Create an Iterator

- implement the methods `__iter__()` and `__next__()` to an object.

- `__iter__()`: do initialization, and always return the **iterator object** itself.

- ``__next__()`: do operations, and must return the **next item** in the sequence.

```py
print("\n--------Create an Iterator--------\n")


class XIterator:
    def __iter__(self):
        self.a = 0
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x


xIter = XIterator()
iter = iter(xIter)      # get an iterator

print(next(iter))
print(next(iter))
print(next(iter))
print(next(iter))
print(next(iter))
print(next(iter))
print(next(iter))
print(next(iter))
print(next(iter))

```

---

### StopIteration

- To prevent the iteration to go on forever, we can use the `StopIteration` statement, without which the iteration keep going on forever.

  - StopIteration 异常用于标识迭代的完成，防止出现无限循环的情况，

- In the **next**() method, we can add a terminating condition to raise an error if the iteration is done a specified number of times.

```py
print("\n--------Create an Iterator--------\n")


class XIterator:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 20:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration


xIter = XIterator()
iter = iter(xIter)

for x in iter:
    print(x)        # 1-20

```

---

[TOP](#python---iterators)
