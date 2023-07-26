# Python - List Methods

[Back](../index.md)

- [Python - List Methods](#python---list-methods)
  - [Constuctor](#constuctor)
    - [`list(iterable)`](#listiterable)
  - [Manipulate Element](#manipulate-element)
    - [`append(elmnt)`](#appendelmnt)
    - [`insert(pos, elmnt)`](#insertpos-elmnt)
    - [`pop(pos)`](#poppos)
    - [`remove(elmnt)`](#removeelmnt)
    - [`clear()`](#clear)
  - [`copy()`: Copy List](#copy-copy-list)
  - [Find element](#find-element)
    - [`count(value)`: Count element](#countvalue-count-element)
    - [`index(elmnt)`](#indexelmnt)
  - [Concatenating](#concatenating)
    - [`+` Operator](#-operator)
    - [`extend(iterable)`](#extenditerable)
  - [Sort](#sort)
    - [`sort(reverse, key)`](#sortreverse-key)
    - [`reverse()`](#reverse)

---

## Constuctor

### `list(iterable)`

- creates a list object.

- Parameter
  - `iterable`: **Optional**. A sequence, collection or an iterator object

```py
print("\n--------- list() --------\n")

# must be iterable
# x_list = list(1)  # TypeError: 'int' object is not iterable
# x_list = list(1, 2)  # TypeError: set expected at most 1 argument, got 2

# empty set
x_list = list()
print(x_list)    # []

# from tuple
x_list = list(('apple', 'banana', 'cherry'))
print(x_list)    # ['apple', 'banana', 'cherry']

# from list
x_list = list(['apple', 'banana', 'cherry'])
print(x_list)    # ['apple', 'banana', 'cherry']

# from set
x_list = list({'apple', 'banana', 'cherry'})
print(x_list)    # ['apple', 'banana', 'cherry'], order is random

```

---

## Manipulate Element

### `append(elmnt)`

- appends **an element** to the end of the list.

- Parameter
  - `elmnt`: Required. An element of any type (string, number, object etc.)

```py
print("\n-------- append(elmnt) --------\n")

xlist = ["apple", "banana", "cherry"]
xlist.append("watermelon")
print(xlist)    # ['apple', 'banana', 'cherry', 'watermelon']

xlist = ["apple", "banana", "cherry"]
xlist.append(["watermelon", "ff"])   # can append a list
print(xlist)    # ['apple', 'banana', 'cherry', ['watermelon', 'ff']]

```

---

### `insert(pos, elmnt)`

- inserts the specified value at the specified position.

- Parameter
  - `pos`: Required. A number specifying in which position to insert the value
  - `elmnt`: Required. An element of any type (string, number, object etc.)

```py
print("\n-------- list.insert(pos, elmnt) --------\n")

x_list = ['apple', 'banana', 'cherry']

x_list.insert(1, "orange")
print(x_list)   # ['apple', 'orange', 'banana', 'cherry']

x_list.insert(100, "mango")
print(x_list)   # ['apple', 'orange', 'banana', 'cherry', 'mango']

# x_list.insert(1, "orange", "mango") # TypeError: insert expected 2 arguments, got 3
```

---

### `pop(pos)`

- removes the element at the specified position.

- Parameter

  - `pos`: Optional. A number specifying the position of the element you want to remove, default value is `-1`, which returns the last item

- Return
  - the removed value.

```py
print("\n-------- list.pop(pos) --------\n")

x_list = ['apple', 'banana', 'cherry', 'orange', 'mango']

print(x_list.pop())  # mango
print(x_list)   # ['apple', 'banana', 'cherry', 'orange']

print(x_list.pop(0))  # apple
print(x_list)   # ['banana', 'cherry', 'orange']

# print(x_list.pop(100))  # IndexError: pop index out of range

```

---

### `remove(elmnt)`

- removes the **first occurrence** of the element with the specified value.

- Parameter
  - `elmnt`: Required. Any type (string, number, list etc.) The element you want to remove

```py
print("\n-------- list.remove(elmnt) --------\n")

x_list = ['apple', 'banana', 'cherry', 'orange']

print(x_list.remove("apple"))   # None
print(x_list)  # ['banana', 'cherry', 'orange', 'mango']

# print(x_list.remove("mango"))   # ValueError: list.remove(x): x not in list
# print(x_list.remove())   # TypeError: list.remove() takes exactly one argument (0 given)
```

---

### `clear()`

- removes all the elements from a list.

```py
print("\n-------- list.clear() --------\n")

fruits = ["apple", "banana", "cherry"]
fruits.clear()
print(fruits)  # []
```

---

## `copy()`: Copy List

- returns a copy of the specified list.

```py
print("\n-------- list.copy() --------\n")

fruits = ["apple", "banana", "cherry"]
x = fruits.copy()
print(x)  # ['apple', 'banana', 'cherry']

# deep copy
x[0] = 'mango'
print(fruits)   # ['apple', 'banana', 'cherry']
print(x)  # ['mango', 'banana', 'cherry']
```

---

## Find element

### `count(value)`: Count element

- returns the number of elements with the specified value.

- Parameter
  - value: Required. Any type (string, number, list, tuple, etc.). The value to search for.

```py
print("\n-------- list.count(value) --------\n")

x_list = ["apple", "banana", "cherry", "banana"]

print(x_list.count("mango"))  # 0
print(x_list.count("cherry"))  # 1
print(x_list.count("banana"))  # 2
```

---

### `index(elmnt)`

- returns **the position at the first occurrence** of the specified value.

- Parameter
  - `elmnt`: Required. Any type (string, number, list, etc.). The element to search for

```py
print("\n-------- list.index(elmnt) --------\n")

x_list = ['apple', 'banana', 'cherry', 'cherry']

print(x_list.index("banana"))   # 1
print(x_list.index("cherry"))   # 2
# print(x_list.index("mango"))   # ValueError: 'mango' is not in list

```

---

## Concatenating

### `+` Operator

```py
x_list = ['Ford', 'Mitsubishi']
y_list = ['BMW', 'VW']
x_list = x_list + y_list

print(x_list)  # ['Ford', 'Mitsubishi', 'BMW', 'VW']
```

---

### `extend(iterable)`

- adds the specified list elements (or any iterable) to the end of the current list.

- Parameter
  - `iterable`: Required. Any iterable (list, set, tuple, etc.)

```py
print("\n-------- list.extend(iterable) --------\n")

x_list = ['apple', 'banana', 'cherry']
y_list = (1, 4, 5, 9)

print(x_list.extend(y_list))  # None
print(x_list)  # ['apple', 'banana', 'cherry', 1, 4, 5, 9]
```

---

## Sort

### `sort(reverse, key)`

- sorts the list ascending by default.

- Parameter
  - `reverse`: Optional. `reverse=True` will sort the list descending. Default is `reverse=False`.
  - `key`: Optional. A function to specify the sorting criteria(s)

```py
print("\n-------- list.sort(reverse=True|False, key=myFunc) --------\n")

x_list = ['Ford', 'Mitsubishi', 'BMW', 'VW']

x_list.sort()
print(x_list)   # ['BMW', 'Ford', 'Mitsubishi', 'VW']

x_list.sort(reverse=True)
print(x_list)   # ['VW', 'Mitsubishi', 'Ford', 'BMW']
```

- Using Function

```py

x_list = ['Ford', 'Mitsubishi', 'BMW', 'VW']


def sortby_len(e):
    return len(e)


x_list.sort(key=sortby_len)
print(x_list)   # ['VW', 'BMW', 'Ford', 'Mitsubishi']


def sortby_name(e):
    return e['year']


y_list = [
    {'car': 'Ford', 'year': 2005},
    {'car': 'Mitsubishi', 'year': 2000},
    {'car': 'BMW', 'year': 2019},
    {'car': 'VW', 'year': 2011}
]

y_list.sort(key=sortby_name)
print(y_list)
# [{'car': 'Mitsubishi', 'year': 2000}, {'car': 'Ford', 'year': 2005}, {'car': 'VW', 'year': 2011}, {'car': 'BMW', 'year': 2019}]

```

---

### `reverse()`

- reverses the sorting order of the elements.

```py
print("\n-------- list.reverse() --------\n")

x_list = ['apple', 'banana', 'cherry', 'orange']

x_list.reverse()
print(x_list)   # ['orange', 'cherry', 'banana', 'apple']

```

---

[TOP](#python---list-methods)
