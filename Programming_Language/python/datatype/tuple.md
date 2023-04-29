# Python - Tuple

[Back](../index.md)

- [Python - Tuple](#python---tuple)
  - [Tuple](#tuple)
    - [Tuple Method](#tuple-method)
    - [Create a tuple](#create-a-tuple)
    - [Access Items](#access-items)
    - [Change Tuple Values](#change-tuple-values)
    - [Add Items](#add-items)
    - [Remove Items](#remove-items)
    - [Unpack](#unpack)
  - [Check if Item Exists:`in`](#check-if-item-existsin)
  - [Loop Tuple](#loop-tuple)
  - [Join Tuple](#join-tuple)
  - [count()](#count)
  - [index()](#index)

---

## Tuple

- `Tuples`: to store multiple items in a single variable.

- A tuple is a **collection** which is **ordered** and **unchangeable**.

- Tuples are written with **round brackets**.

- **Tuple Items**

  - Tuple items are **ordered**, **unchangeable**, and allow **duplicate** values.
  - Tuple items are **indexed**, the first item has index [0], the second item has index [1] etc.

- **Ordered**

  - order will **not change**.

- **Unchangeable**

  - cannot **change, add or remove** items after the tuple has been created.

- **Allow Duplicates**

  - can have items with the same value

- **Tuple Length**
  - `len()` function: how many items a tuple has

---

### Tuple Method

| Method    | Description                                                                             |
| --------- | --------------------------------------------------------------------------------------- |
| `count()` | Returns the number of times a specified value occurs in a tuple                         |
| `index()` | Searches the tuple for a specified value and returns the position of where it was found |

---

### Create a tuple

- 1. round brackets

- 2. `tuple()` Constructor

- To create a tuple with only one item, you have to add a comma after the item, otherwise Python will not recognize it as a tuple.

  ```py
  print("\n--------Create a tuple--------\n")

  # round-brackets
  xtuple = ("apple", "banana", "cherry")
  print(xtuple)   # ('apple', 'banana', 'cherry')

  # tuple() Constructor
  xtuple = tuple(("apple", "banana", "cherry"))  # note the double round-brackets
  print(xtuple)   # ('apple', 'banana', 'cherry')

  xtuple = ("apple",)
  print(type(xtuple))  # <class 'tuple'>

  # NOT a tuple
  xtuple = ("apple")
  print(type(xtuple))  # <class 'str'>
  ```

- Tuple items can be of **any data type**.

  ```py
  tuple1 = ("apple", "banana", "cherry")  # string
  tuple2 = (1, 5, 7, 9, 3)                # number
  tuple3 = (True, False, False)           # boolean
  tuple1 = ("abc", 34, True, 40, "male")  #  can contain different data types

  ```

- **type()**

  ```py
  xtuple = ("apple", "banana", "cherry")
  print(type(xtuple))     # <class 'tuple'>
  ```

---

### Access Items

- access tuple items by referring to the index number, inside square brackets

```py
print("\n--------Access Items--------\n")
# Access Items
xtuple = ("apple", "banana", "cherry")
print(xtuple[0])  # apple
print(xtuple[1])  # banana
# print(xtuple[3])  # Error: IndexError: list index out of range

# Negative Indexing
print(xtuple[-1])  # cherry
print(xtuple[-2])  # banana

# Range of Indexes
xtuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(xtuple[2:5])   # ['cherry', 'orange', 'kiwi']
print(xtuple[:5])   # exclusive ['apple', 'banana', 'cherry', 'orange', 'kiwi']
print(xtuple[5:])   # inclusive ['melon', 'mango']

# Range of Negative Indexes
xtuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(xtuple[-4:-1])  # ['orange', 'kiwi', 'melon']


```

---

### Change Tuple Values

- Once a tuple is created, you **cannot change** its values. Tuples are unchangeable, or immutable as it also is called.

- Change Tuple Values: can convert the `tuple` into a `list`, change the `list`, and convert the `list` back into a `tuple`.

```py
xtuple = ("apple", "banana", "cherrylist")
ylist = list(xtuple)
ylist[1] = "kiwi"
xtuple = tuple(ylist)

print(xtuple)   # ('apple', 'kiwi', 'cherrylist')

```

---

### Add Items

1. Convert into a list: `tuple` -> `list` -> `tuple`.

2. Add tuple to a tuple. create a new tuple with the item(s), and add it to the existing tuple.

```py

xtuple = ("apple", "banana", "cherrylist")
ylist = list(xtuple)
ylist.append("kiwi")
xtuple = tuple(ylist)

print(xtuple)   # ('apple', 'banana', 'cherrylist', 'kiwi')


xtuple = ("apple", "banana", "cherry")
ylist = ("orange",)
xtuple += ylist

print(xtuple)   # ('apple', 'banana', 'cherry', 'orange')

```

---

### Remove Items

1. Convert into a list: `tuple` -> `list` -> `tuple`.
2. delete the tuple completely

```py
xtuple = ("apple", "banana", "cherry")
ylist = list(xtuple)
ylist.remove("apple")
xtuple = tuple(ylist)

print(xtuple)   # ('banana', 'cherry')

xtuple = ("apple", "banana", "cherry")
del xtuple
print(xtuple)  # NameError: name 'xtuple' is not defined

```

---

### Unpack

- `unpacking`: Python allowed to extract the values back into variables.

  - Note: The <u>number</u> of variables **must match** the <u>number</u> of values in the tuple, if not, you must use an **asterisk** to collect the remaining values as a list.

  - If the number of variables is **less than** the number of values, it raises ValueError: too many values to unpack.

  - If the number of variables is **less than** the number of values, can add an `*` to the variable name and the values will be assigned to the variable as a list

  - If the number of variables is **more than** the number of values, it raises ValueError: not enough values to unpack.

```py
print("\n------Unpacking------\n")

print("\n------Equal------\n")
# number of variables must match number of items
fruits = ("apple", "banana", "cherry")
(green, yellow, red) = fruits

print(green)    # apple
print(yellow)   # banana
print(red)      # cherry

print("\n------Less than------\n")

#  if number of variables is less than number of items, Error
fruits = ("apple", "banana", "cherry")
# (green, yellow) = fruits    # ValueError: too many values to unpack (expected 2)

#  if number of variables is less than number of items, should Asterisk
fruits = ("apple", "banana", "cherry")
(green, *yellow) = fruits
print(green)    # apple
print(yellow)   # ['banana', 'cherry']


fruits = ("apple", "mango", "papaya", "pineapple", "cherry")
(green, *tropic, red) = fruits
print(green)    # apple
print(tropic)   # ['mango', 'papaya', 'pineapple']
print(red)      # cherry

print("\n------More than------\n")
fruits = ("apple", "banana", "cherry")
# ValueError: not enough values to unpack (expected 4, got 3)
(green, yellow, red, grey) = fruits


```

---

## Check if Item Exists:`in`

```py
xlist = ("apple", "banana", "cherry")
if "apple" in xlist:
    print("Yes, 'apple' is in the fruits list")
```

---

## Loop Tuple

- `for in` loop

- `for in range(len())` loop

- `while` Loop

```py

print("\n--------for in loop--------\n")
# for in loop
xtuple = ("apple", "banana", "cherry")
for x in xtuple:
    print(x)


print("\n--------for in range loop--------\n")
# for in range(len())
xtuple = ("apple", "banana", "cherry")
for i in range(len(xtuple)):     # [0, 1, 2]
    print(xtuple[i])


print("\n--------While Loop--------\n")
# While Loop
xtuple = ("apple", "banana", "cherry")
i = 0
while i < len(xtuple):   # 可以用于判断是否进入循环
    print(xtuple[i])
    i = i + 1

```

---

## Join Tuple

- `+` operator
- `*` operator

```py
print("\n--------Join tuple--------\n")
tuple1 = ("a", "b", "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3)   # ('a', 'b', 'c', 1, 2, 3)


fruits = ("apple", "banana", "cherry")
mytuple = fruits * 3

# ('apple', 'banana', 'cherry', 'apple', 'banana', 'cherry', 'apple', 'banana', 'cherry')
print(mytuple)
```

---

## count()

- `count()`: Returns the number of times a specified value occurs in a tuple

- **Parameter**
  - `value`: Required. The item to search for

```py
print("\n--------count()--------\n")
xlist = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)

num = xlist.count(5)

print(num)  # 2

```

---

## index()

- `index()`: finds the first occurrence of the specified value.

  - The index() method **raises an exception** if the value is not found.

- Parameter:
  - `value`: Required. The item to search for

```py
print("\n--------index()--------\n")
thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)

x = thistuple.index(8)

print(x)    # 3

```

---

[TOP](#python---tuple)
