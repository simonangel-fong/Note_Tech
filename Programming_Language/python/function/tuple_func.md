# Python - Tuple Methods

[Back](../index.md)

- [Python - Tuple Methods](#python---tuple-methods)
  - [Constructor](#constructor)
    - [`tuple(iterable)`](#tupleiterable)
  - [Search](#search)
    - [`count(value)`](#countvalue)
    - [`index(value)`](#indexvalue)

---

## Constructor

### `tuple(iterable)`

- creates a tuple object.

- Parameter
  - `iterable`: **Optional**. A sequence, collection or an iterator object

```py
print("\n--------- tuple(iterable) --------\n")

# must be iterable
# x_list = tuple(1)  # TypeError: 'int' object is not iterable
# x_list = tuple(1, 2)  # TypeError: set expected at most 1 argument, got 2

# empty set
x_list = tuple()
print(x_list)    # ()

# from tuple
x_list = tuple(('apple', 'banana', 'cherry'))
print(x_list)    # ('apple', 'banana', 'cherry')

# from list
x_list = tuple(['apple', 'banana', 'cherry'])
print(x_list)    # ('apple', 'banana', 'cherry')

# from set
x_list = tuple({'apple', 'banana', 'cherry'})
print(x_list)    # ('cherry', 'apple', 'banana'), order is random
```

---

## Search

### `count(value)`

- returns the number of times a specified value appears in the tuple.

- Parameter
  - `value`: Required. The item to search for

```py
print("\n-------- tuple.count(value) --------\n")

x_tuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)

print(x_tuple.count(10))  # 0
print(x_tuple.count(5))  # 2
```

---

### `index(value)`

- finds the first occurrence of the specified value.
- raises an exception if the value is not found.

- Parameter
  - `value`: Required. The item to search for

```py
print("\n-------- tuple.count(value) --------\n")

x_list = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)

print(x_list.index(8))  # 3
# print(x_list.index(0)) # ValueError: tuple.index(x): x not in tuple
```

---

[TOP](#python---tuple-methods)
