# Python - Set

[Back](../index.md)

- [Python - Set](#python---set)
  - [Set](#set)
    - [Set Methods](#set-methods)
    - [Create a set](#create-a-set)
    - [Add Items](#add-items)
      - [`add()`: adds an element](#add-adds-an-element)
      - [`update()`: adding items from another iterable.](#update-adding-items-from-another-iterable)
    - [Remove Item](#remove-item)
      - [`discard(value)`](#discardvalue)
      - [`pop()`](#pop)
      - [`remove(item)`](#removeitem)
      - [`clear()`](#clear)
      - [`del` Operator](#del-operator)
  - [`copy()`: copies the set](#copy-copies-the-set)
  - [Loop Set](#loop-set)
  - [`in` Operator: Check if Item Exists](#in-operator-check-if-item-exists)

---

## Set

- Sets are used to store multiple items in a **single variable**.

- **Unordered**

  - the items in a set do **not have a defined order**.
  - the items cannot be referred to by index or key.

- **Unchangeable**

  - Set items cannot be changed after the set has been created.
  - Once a set is created, items can be removed and new items can be added.

- **Duplicates Not Allowed**

  - Sets cannot have two items with the same value.
  - The values `True` and `1` are considered the same value in sets, and are treated as duplicates.

  ```py
  xset = {"apple", "banana", "cherry", True, 1, 2}
  print(xset)     # {'apple', True, 2, 'banana', 'cherry'}
  ```

- **Data Types**

  - Set items can be of any data type.

  ```py
  xset = {"abc", 34, True, 40, "male"}
  print(xset)     # {True, 34, 'abc', 40, 'male'}
  ```

---

### Set Methods

- Create a Set

| Method  | Description  |
| ------- | ------------ |
| `set()` | return a set |

- Copy a Set

| Method   | Description               |
| -------- | ------------------------- |
| `set()`  | return a set              |
| `copy()` | Returns a copy of the set |

- Add items

| Method  | Description                |
| ------- | -------------------------- |
| `add()` | Adds an element to the set |

- Update items

| Method                          | Description                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------ |
| `update()`                      | Update the set with the union of this set and others                           |
| `difference_update()`           | Removes the items in this set that are also included in another, specified set |
| `intersection_update()`         | Removes the items in this set that are not present in other, specified set(s)  |
| `symmetric_difference_update()` | inserts the symmetric differences from this set and another                    |

- Remove items

| Method      | Description                           |
| ----------- | ------------------------------------- |
| `pop()`     | Removes an element from the set       |
| `remove()`  | Removes the specified element         |
| `discard()` | Remove the specified item             |
| `clear()`   | Removes all the elements from the set |

- Set calcuation

| Method                   | Description                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| `difference()`           | Returns a set containing the difference between two or more sets |
| `intersection()`         | Returns a set, that is the intersection of two other sets        |
| `isdisjoint()`           | Returns whether two sets have a intersection or not              |
| `issubset()`             | Returns whether another set contains this set or not             |
| `issuperset()`           | Returns whether this set contains another set or not             |
| `symmetric_difference()` | Returns a set with the symmetric differences of two sets         |
| `union()`                | Return a set containing the union of sets                        |

---

### Create a set

- 1. curly brackets.

- 2. `set()` Constructor

```py
# create a set

print("\n--------Create a Set--------\n")
# using curly brackets
xset = {"apple", "banana", "cherry"}
print(xset)     # {'apple', 'banana', 'cherry'}


# using set() constructor
xset = set(("apple", "banana", "cherry"))  # note the double round-brackets
print(xset)     # {'cherry', 'banana', 'apple'}
```

---

### Add Items

#### `add()`: adds an element

- `add()`: add **one item** to a set

```py
print("\n--------Add a Item:add()--------\n")
xlist = {"apple", "banana", "cherry"}
xlist.add("orange")
print(xlist)    # {'cherry', 'orange', 'apple', 'banana'}
```

---

#### `update()`: adding items from another iterable.

- `update()`: add **items** from another set into the current set.
  - does not have to be a set, it can be any **iterable object** (tuples, lists, dictionaries etc.).

```py
print("\n---------Add items: update()--------\n")
xset = {"apple", "banana", "cherry"}
yset = {"pineapple", "mango", "papaya"}
xset.update(yset)

print(xset)     # {'papaya', 'banana', 'apple', 'cherry', 'pineapple', 'mango'}

zset = xset.update(yset)
print(zset)     # None

# iterable object
xset = {"apple", "banana", "cherry"}
yset = ["pineapple", "mango", "papaya"]
xset.update(yset)

print(xset)     # {'papaya', 'banana', 'apple', 'cherry', 'pineapple', 'mango'}
```

---

### Remove Item

#### `discard(value)`

- remove an item in a set

  - If the item to remove does not exist, `discard()` will NOT raise an error.

```py
# .discard()
xset = {"apple", "banana", "cherry"}
xset.discard("banana")
print(xset)

xset.discard("banana")
xset.discard("banana")
```

---

#### `pop()`

- remove a random item

  - return value: the removed item.

```py
# .pop()
xset = {"apple", "banana", "cherry"}
x = xset.pop()            #
# x = xset.pop(1)           # TypeError: set.pop() takes no arguments (1 given)
# x = xset.pop("banana")    # TypeError: set.pop() takes no arguments (1 given)
print(xset)
print(x)                    # a random item removed from set
```

---

#### `remove(item)`

- remove an item in a set

  - If the item to remove does not exist, remove() will raise an error.

```py
# .remove()
xset = {"apple", "banana", "cherry"}
xset.remove("banana")
print(xset)

# xset.remove("banana")       # KeyError: 'banana'
```

---

#### `clear()`

- empties the set

```py
# clear()
xset = {"apple", "banana", "cherry"}
xset.clear()

print(xset)     # set()
```

---

#### `del` Operator

- delete the tuple completely

```py
# del
xset = {"apple", "banana", "cherry"}
del xset

# print(xset)     # NameError: name 'xset' is not defined
```

---

## `copy()`: copies the set

- copies the set

```py
x_set = {"apple", "banana", "cherry"}
y_set = x_set.copy()
print(y_set)    # {'banana', 'apple', 'cherry'}
```

---

## Loop Set

- `for in` loop

```py

print("\n--------for in loop--------\n")
# for in loop
xset = {"apple", "banana", "cherry"}
for x in xset:
    print(x)

```

---

## `in` Operator: Check if Item Exists

```py
xlist = {"apple", "banana", "cherry"}
if "apple" in xlist:
  print("Yes, 'apple' is in the fruits list")
```

---

[TOP](#python---set)
