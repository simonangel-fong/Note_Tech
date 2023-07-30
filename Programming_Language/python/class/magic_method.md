# Python - Magic Method

[Back](../index.md)

- [Python - Magic Method](#python---magic-method)
  - [Magic Method](#magic-method)
  - [`__contains__()`](#__contains__)
  - [`__iter__()`](#__iter__)
  - [`__setitem__()` \& `__getitem__()`](#__setitem__--__getitem__)
  - [`__delitem__()`](#__delitem__)
  - [`__len__()`](#__len__)

---

## Magic Method

- `Magic method`
  - It provides a simple way to **make objects behave like built-in types**, which means one can avoid counter-intuitive or nonstandard ways of performing basic operators.

---

## `__contains__()`

- `__contains__()`
  - The **`in` membership operator** of Python implicitly calls the `__contains__` method. We can
  - used to determine **if an element is contained in an object's attributes.**

```py
class Method:

    # Calling the __init__ method and initializing the attributes
    def __init__(self, attribute):
        self.attribute = attribute

    # Calling the __contains__ method
    def __contains__(self, attribute):
        return attribute in self.attribute


# Creating an instance of the class
instance = Method([4, 6, 8, 9, 1, 6])

# Checking if a value is present in the container attribute
print("4 is contained in ""attribute"": ", 4 in instance)   # True
print("5 is contained in ""attribute"": ", 5 in instance)   # False
```

---

## `__iter__()`

- `__iter__()`
  - provide a generator object
  - can leverage the `iter()` and `next()` methods.

```py
class Method:
    def __init__(self, start_value, stop_value):
        self.start = start_value
        self.stop = stop_value

    def __iter__(self):
        for num in range(self.start, self.stop + 1):
            yield num ** 2


# Creating an instance
instance = iter(Method(3, 8))
print(next(instance))       # 9
print(next(instance))       # 16
print(next(instance))       # 25
print(next(instance))       # 36
print(next(instance))       # 49
print(next(instance))       # 64
```

---

## `__setitem__()` & `__getitem__()`

- `__getitem__()` and `__setitem__()`
  - these methods are **used only in indexed attributes** like arrays, dictionaries, lists e.t.c.
  - Instead of directly accessing and manipulating class attributes, it provides such methods, so these attributes can be modified only by its own instances and thus implements abstraction.
  - Instead of making class attributes as public, these methods make them private, provide validation that only correct values are set to the attributes and the only correct caller has access to these attributes.

```py
class record:

    def __init__(self):
        self.record = {}

    def __getitem__(self, key):
        if key in self.record:
            return self.record[key]
        else:
            return None

    def __setitem__(self, key, newvalue):
        self.record[key] = newvalue


rec = record()

rec['fname'] = 'John'
rec['lname'] = 'Wick'

print(rec['fname'])     # John
print(rec['lname'])     # Wick
print(rec['age'])       # None
```

---

## `__delitem__()`

- `__delitem__()`
  - can use the expression `del` to delete indexed attributes

```py
class record:

    def __init__(self, dict):
        self.dict = dict

    def __len__(self):
        return len(self.dict)

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return None

    def __delitem__(self, key):
        if key in self.dict:
            del self.dict[key]


aList = {'fname': 'John'}
rec = record(aList)

print(len(rec))           # 1
print(rec['fname'])       # John

rec['fname'] = 'Winston'
rec['lname'] = 'Wick'
print(rec['fname'])       # Winston
print(rec['lname'])       # Wick

del rec['fname']
print(rec['fname'])       # None
print(rec['lname'])       # Wick
```

---

## `__len__()`

- `__len__()`
  - used to implement the `len()` function in Python
  - It finally returns an integer value that is greater than or equal to zero as it represents the length of the object for which it is called.
  - Returns: Returns a **non negative integer**.

```py
class record:

    def __init__(self, arr):
        self.record = arr

    def __len__(self):
        return len(self.record)


aList = [0, 1, 2, 3, 4]
rec = record(aList)

print(len(rec))     # 5

```

---

[Top](#python---magic-method)
