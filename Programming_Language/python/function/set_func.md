# Python - Set Method

[Back](../index.md)

- [Python - Set Method](#python---set-method)
  - [Constructor](#constructor)
    - [`set(iterable)`](#setiterable)
  - [Manipulate Elements](#manipulate-elements)
    - [`add(elmnt)`](#addelmnt)
    - [`update(set)`](#updateset)
    - [`pop()`](#pop)
    - [`discard(value)`](#discardvalue)
    - [`remove(item)`](#removeitem)
    - [`clear()`](#clear)
  - [Copy a Set](#copy-a-set)
    - [`copy()`](#copy)
  - [Relationship](#relationship)
    - [`isdisjoint(set)`](#isdisjointset)
    - [`issubset(set)`](#issubsetset)
    - [`<` Operator: if Subset](#-operator-if-subset)
    - [`issuperset(set)`](#issupersetset)
    - [`>` Operator: if Superset](#-operator-if-superset)
    - [`intersection([set])`](#intersectionset)
    - [`&` Operator: intersection](#-operator-intersection)
    - [`intersection_update([set])`](#intersection_updateset)
    - [`difference(set)`](#differenceset)
    - [`-` Operator: difference](#--operator-difference)
    - [`difference_update(set)`](#difference_updateset)
    - [`symmetric_difference(set)`](#symmetric_differenceset)
    - [`symmetric_difference_update(set)`](#symmetric_difference_updateset)
    - [`union([set])`](#unionset)
    - [`|` Operator: Union Sets](#-operator-union-sets)

---

## Constructor

### `set(iterable)`

- creates a set object.

- Parameter
  - `iterable`: **Optional**. A sequence, collection or an iterator object

```py
print("\n--------- set() --------\n")

# must be iterable
# x_set = set(1)  # TypeError: 'int' object is not iterable
# x_set = set(1, 2)  # TypeError: set expected at most 1 argument, got 2

# empty set
x_set = set()
print(x_set)    # set()

# from tuple
x_set = set(('apple', 'banana', 'cherry'))
print(x_set)    # {'apple', 'banana', 'cherry'}

# from list
x_set = set(['apple', 'banana', 'cherry'])
print(x_set)    # {'apple', 'banana', 'cherry'}
```

---

## Manipulate Elements

### `add(elmnt)`

- adds an element to the set.

  - If the element already exists, the `add()` method does not add the element.

- Parameter
  - `elmnt`: Required. The element to add to the set

```py
print("\n-------- set.add(elmnt) --------\n")

x_list = {"apple", "banana", "cherry"}

x_list.add("apple")
print(x_list)  # {'cherry', 'banana', 'apple'}

x_list.add("mango")
print(x_list)  # {'banana', 'mango', 'apple', 'cherry'}
```

---

### `update(set)`

- updates the current set, by adding items from another set (or any other iterable).

- Parameter
  - `set`: Required. The iterable insert into the current set

```py
print("\n-------- set.update(set) --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

x_set.update(y_set)
print(x_set)  # {'banana', 'apple', 'microsoft', 'google', 'cherry'}
print(y_set)  # {'apple', 'google', 'microsoft'}
```

---

### `pop()`

- removes a **random** item from the set.

- Return
  - the removed item.

```py
print("\n-------- set.pop() --------\n")

x_set = {"apple", "banana", "cherry"}

print(x_set.pop())  # banana
print(x_set)    # {'cherry', 'apple'}
```

---

### `discard(value)`

- removes the specified item from the set.
- difference between `remove()` and `discard()`:

  - `remove()` method will raise an error if the specified item does not exist
  - `discard()` method will not.

- Parameter:
  - `value`: Required. The item to search for, and remove

```py
print("\n-------- set.discard(value) --------\n")

x_list = {"apple", "banana", "cherry"}

x_list.discard("banana")
print(x_list)   # {'apple', 'cherry'}
```

---

### `remove(item)`

- removes the specified element from the set.

- Difference between `discard()` and `remove()`

  - `remove()`: raise an error if the specified item does not exist
  - `discard()` method will not.

- Parameter
  - `item`: Required. The item to search for, and remove

```py
print("\n-------- set.remove(item) --------\n")

x_set = {"apple", "banana", "cherry"}

print(x_set.remove("banana"))  # None
print(x_set)    # {'cherry', 'apple'}
```

---

### `clear()`

- removes all elements in a set.

```py
print("\n-------- set.clear() --------\n")

x_list = {"apple", "banana", "cherry"}

x_list.clear()
print(x_list)  # set()
```

---

## Copy a Set

### `copy()`

- copies the set.

```py
print("\n-------- set.copy() --------\n")

x_list = {"apple", "banana", "cherry"}

y_list = x_list.copy()
print(x_list)  # {'cherry', 'apple', 'banana'}
print(y_list)  # {'cherry', 'apple', 'banana'}

# deep copy
y_list.remove("apple")
print(x_list)  # {'cherry', 'apple', 'banana'}
print(y_list)  # {'cherry', 'banana'}
```

---

## Relationship

### `isdisjoint(set)`

- returns `True` if none of the items are present in both sets, otherwise it returns `False`.

  - `True` if intersection of both sets doesnot exist.

- Parameter
  - `set`: Required. The set to search for equal items in

```py
print("\n-------- set.isdisjoint(set) --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}
z_set = {"meta", "twitter", "Tiktok"}

print(x_set.isdisjoint(y_set))  # False
print(x_set.isdisjoint(z_set))  # True
```

---

### `issubset(set)`

- returns `True` if all items in the set exists in the specified set, otherwise it returns `False`.

- Parameter
  - `set`: Required. The set to search for equal items in

```py
print("\n-------- set.issubset(set) --------\n")

x_set = {"f", "e", "d", "c", "b", "a"}
y_set = {"a", "b", "c"}
z_set = set()
w_set = {1, 2}

print(x_set.issubset(x_set))  # True
print(y_set.issubset(x_set))  # True
print(z_set.issubset(x_set))  # True
print(w_set.issubset(x_set))  # False
```

---

### `<` Operator: if Subset

```py
print("\n--------- < Operator --------\n")

xSet = {"apple", "banana"}
ySet = {"apple", "banana", "cherry"}


print(xSet < xSet)      # False, 自身不是自身的子集
print(xSet < ySet)      # True
print(ySet < xSet)      # False
```

---

### `issuperset(set)`

- returns `True` if all items in the specified set exists in the original set, otherwise it returns `False`.

- Parameter
  - `set`: Required. The set to search for equal items in

```py
print("\n-------- set.issuperset(set) --------\n")

x_set = {"f", "e", "d", "c", "b", "a"}
y_set = {"a", "b", "c"}
z_set = set()
w_set = {1, 2}

print(x_set.issuperset(x_set))  # True
print(x_set.issuperset(y_set))  # True
print(x_set.issuperset(z_set))  # True
print(x_set.issuperset(w_set))  # False
```

---

### `>` Operator: if Superset

```py
print("\n--------- > Operator --------\n")

xSet = {"apple", "banana", "cherry"}
ySet = {"apple", "banana"}

print(xSet > xSet)      # False
print(xSet > ySet)      # True
print(ySet > xSet)      # False
```

---

### `intersection([set])`

- returns a set that contains only items that exist in both sets, or in all sets if the comparison is done with more than two sets.

- Parameter
  - `set`: Required. The set(s) to search for equal items in. Separate the sets with a comma

```py
print("\n-------- set.intersection([set]) --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

# print(x_set.intersection(None))    # TypeError: 'NoneType' object is not iterable

print(x_set.intersection(set()))    # set()
print(x_set.intersection(list()))   # set()
print(x_set.intersection(["banana", "mango"]))   # {'banana'}

print(x_set.intersection(y_set))    # {'apple'}

x = {"a", "b", "c"}
y = {"c", "d", "e"}
z = {"f", "g", "c"}

print(x.intersection(y, z))     # {'c'}
```

---

### `&` Operator: intersection

```py
print("\n-------- & operator: intersection --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

print(x_set & y_set)
# {'apple'}

x = {"a", "b", "c"}
y = {"f", "d", "c"}
z = {"c", "d", "e"}

print(x & y & z)    # {'c'}
```

---

### `intersection_update([set])`

- removes the items that is not present in both sets (or in all sets if the comparison is done between more than two sets).

  - keep the identical items only.

- Difference between `intersection_update()` and `intersection()`:

  - `intersection()`: returns a new set, without the unwanted items.
  - `intersection_update()`: removes the unwanted items from the original set.

- Parameter
  - `set`: Required. The set(s) to search for equal items in. Separate the sets with a comma

```py
print("\n-------- set.intersection_update([set]) --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

# TypeError: 'NoneType' object is not iterable
# print(x_set.intersection_update(None))

print(x_set.intersection_update(set()))
print(x_set)    # set()


x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

x_set.intersection_update(y_set)
print(x_set)    # {'apple'}
print(y_set)    # {'google', 'apple', 'microsoft'}

x = {"a", "b", "c"}
y = {"c", "d", "e"}
z = {"f", "g", "c"}

x.intersection_update(y, z)
print(x)     # {'c'}
print(y)     # {'e', 'd', 'c'}
print(z)     # {'g', 'c', 'f'}

```

---

### `difference(set)`

- returns a set that contains the **difference** between two sets.

  - the element in current set that is not contained in the target set.

- Parameter
  - `set`: Required. The set to check for differences in

```py
print("\n-------- set.difference(set) --------\n")

x_list = {"apple", "banana", "cherry"}
y_list = {"google", "microsoft", "apple"}

print(x_list.difference(x_list))  # set()

print(x_list.difference(y_list))  # {'banana', 'cherry'}
print(y_list.difference(x_list))  # {'microsoft', 'google'}
```

---

### `-` Operator: difference

```py
print("\n-------- '-' Operator --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

print(x_set - x_set)  # set()
print(x_set - y_set)    # {'cherry', 'banana'}
print(y_set - x_set)    # {'microsoft', 'google'}
```

---

### `difference_update(set)`

- removes the items that exist in both sets.

  - keep the **different items** only.

- Difference between `difference_update()` and `difference()`:

  - `difference()` returns a new set, without the unwanted items
  - `difference_update()` removes the unwanted items from the original set.

- Parameter:
  - `set`: Required. The set to check for differences in

```py
print("\n-------- set.difference_update(set) --------\n")

x_list = {"apple", "banana", "cherry"}
y_list = {"google", "microsoft", "apple"}

x_list.difference_update(y_list)
print(x_list)   # {'banana', 'cherry'}
print(y_list)   # {'google', 'apple', 'microsoft'}
```

---

### `symmetric_difference(set)`

- returns a set contains a mix of items that are not present in both sets.

  - returns no identical items in both sets.

- Parameter
  - `set`: Required. The set to check for matches in

```py
print("\n-------- set.symmetric_difference(set) --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

print(x_set.symmetric_difference(y_set))
# {'google', 'microsoft', 'cherry', 'banana'}

print(y_set.symmetric_difference(x_set))
# {'google', 'microsoft', 'cherry', 'banana'}
```

---

### `symmetric_difference_update(set)`

- updates the original set by replacing identical items in both sets with different items.

- Parameter
  - `set`: Required. The set to check for matches in

```py
print("\n-------- set.symmetric_difference_update(set) --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

x_set.symmetric_difference_update(y_set)
print(x_set)    # {'cherry', 'banana', 'microsoft', 'google'}
print(y_set)    # {'google', 'microsoft', 'apple'}
```

---

### `union([set])`

- returns a set that contains all items from the original set, and all items from the specified set(s).

- Parameter
  - `set1`: Required. The iterable to unify with

```py
print("\n-------- set.union([set]) --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

print(x_set.union(y_set))
# {'apple', 'banana', 'microsoft', 'google', 'cherry'}

x = {"a", "b", "c"}
y = {"f", "d", "a"}
z = {"c", "d", "e"}

print(x.union(y, z))    # {'e', 'b', 'd', 'f', 'c', 'a'}
```

---

### `|` Operator: Union Sets

```py
print("\n-------- | operator --------\n")

x_set = {"apple", "banana", "cherry"}
y_set = {"google", "microsoft", "apple"}

print(x_set | y_set)
# {'google', 'microsoft', 'cherry', 'banana', 'apple'}

x = {"a", "b", "c"}
y = {"f", "d", "a"}
z = {"c", "d", "e"}

print(x | y | z)    # {'e', 'a', 'b', 'f', 'd', 'c'}
```

---

[TOP](#python---set-method)
