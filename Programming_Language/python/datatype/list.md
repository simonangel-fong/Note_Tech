# Python List

[Back](../index.md)

- [Python List](#python-list)
  - [List](#list)
    - [List Methods](#list-methods)
    - [Create a list](#create-a-list)
    - [Access Items](#access-items)
    - [Add List Items](#add-list-items)
    - [Change Item Value](#change-item-value)
    - [Remove List Items](#remove-list-items)
  - [Check if Item Exists:`in`](#check-if-item-existsin)
  - [Loop Lists](#loop-lists)
  - [List Comprehension](#list-comprehension)
  - [Sort List](#sort-list)
    - [Sort List Alphanumerically](#sort-list-alphanumerically)
    - [Customize Sort Function](#customize-sort-function)
    - [Reverse Order](#reverse-order)
  - [Copy Lists](#copy-lists)
  - [Join Two Lists](#join-two-lists)
  - [count()](#count)
  - [index()](#index)

---

## List

- `List`: to store multiple items in a single variable.

- List items are **ordered**, **changeable**, and **allow duplicate** values.

- **Ordered**

  - Items have a defined order, and that order will not change.
  - If you add new items to a list, the new items will be **placed at the end** of the list.

- **Changeable**

  - items in a list can be changed, added, and removed after it has been created.

- **Allow Duplicates**

  - Since lists are indexed, lists can have items with the same value.
  - example: `xlist = ["apple", "banana", "cherry", "apple", "cherry"]`

- **Data Types**
  - List items can be of **any data type**.
  - A list can contain **different data types**
    - `xlist = ["abc", 34, True, 40, "male"]`

---

### List Methods

| Method      | Description                                                                  |
| ----------- | ---------------------------------------------------------------------------- |
| `append()`  | Adds an element at the end of the list                                       |
| `clear()`   | Removes all the elements from the list                                       |
| `copy()`    | Returns a copy of the list                                                   |
| `count()`   | Returns the number of elements with the specified value                      |
| `extend()`  | Add the elements of a list (or any iterable), to the end of the current list |
| `index()`   | Returns the index of the first element with the specified value              |
| `insert()`  | Adds an element at the specified position                                    |
| `pop()`     | Removes the element at the specified position                                |
| `remove()`  | Removes the item with the specified value                                    |
| `reverse()` | Reverses the order of the list                                               |
| `sort()`    | Sorts the list                                                               |

---

### Create a list

- 1. square brackets

- 2. `list()` Constructor

```py
# create a list

print("\n--------Create a List--------\n")
# using square brackets
xlist = ["apple", "banana", "cherry"]
print(xlist)

# create an empty list and initiate
xlist = []  # create empty list, len=0
# xlist[1] = "apple"  #IndexError: list assignment index out of range
xlist.insert(1, "apple")    # insert a value into index 1
xlist.append("banana")      # append a value to the end
xlist.extend(["cherry"])    # extend a list to the end
print(xlist)    # ['apple', 'banana', 'cherry']


# using list() constructor
xlist = list(("apple", "banana", "cherry"))  # note the double round-brackets
print(xlist)


xlist = list()  # create empty list, len=0
# xlist[1] = "apple"  #IndexError: list assignment index out of range
xlist.insert(1, "apple")    # insert a value into index 1
xlist.append("banana")      # append a value to the end
xlist.extend(["cherry"])    # extend a list to the end
print(xlist)    # ['apple', 'banana', 'cherry']

```

---

### Access Items

- List items are **indexed** and can access them by referring to the **index number**

  - The first item has index `0`.

- **Negative Indexing**: start from the end

  - `-1` refers to the **last item**

- **Range of Indexes**

  - can specify a **range of indexes** by specifying where to start and where to end the range. When specifying a range, the return value will be a **new list** with the specified items.
  - The search will start at the first index-**inclusive**, and end at the last index-**exclusive**.
  - By leaving out the **start value**, the range will **start at the first item**.
    - `xlist[:last_index]`==`xlist[0:last_index]`
  - By leaving out the **end value**, the range will go on to the **end of the list**.
    - `xlist[fist_index:]`==`xlist[fist_index:len(xlist)]`

- **Range of Negative Indexes**
  - Specify negative indexes if you want to start the search from the end of the list.

```py
print("\n--------Access Items--------\n")
# Access Items
xlist = ["apple", "banana", "cherry"]
print(xlist[0])  # apple
print(xlist[1])  # banana
# print(xlist[3])  # Error: IndexError: list index out of range

# Negative Indexing
print(xlist[-1])  # cherry
print(xlist[-2])  # banana

# Range of Indexes
xlist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(xlist[2:5])   # ['cherry', 'orange', 'kiwi']
print(xlist[:5])   # exclusive ['apple', 'banana', 'cherry', 'orange', 'kiwi']
print(xlist[5:])   # inclusive ['melon', 'mango']

# Range of Negative Indexes
xlist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(xlist[-4:-1])  # ['orange', 'kiwi', 'melon']

```

---

### Add List Items

- `insert()`: To insert a new list item, without replacing any of the existing value

- `append()`: add an item to the end of the list

- `extend()`: To append elements from another list to the current list
  - can add any iterable object (tuples, sets, dictionaries etc)

```py
print("\n--------Add Items:Insert()--------\n")
xlist = ["apple", "banana", "cherry"]
xlist.insert(2, "watermelon")
print(xlist)    # ['apple', 'banana', 'watermelon', 'cherry']

xlist = ["apple", "banana", "cherry"]
xlist.insert(2, ["watermelon","ff"])   # can insert a list
print(xlist)    # ['apple', 'banana', ['watermelon', 'ff'], 'cherry']


print("\n--------Add Items:Append()--------\n")
xlist = ["apple", "banana", "cherry"]
xlist.append("watermelon")
print(xlist)    # ['apple', 'banana', 'cherry', 'watermelon']

xlist = ["apple", "banana", "cherry"]
xlist.append(["watermelon","ff"])   # can append a list
print(xlist)    # ['apple', 'banana', 'cherry', ['watermelon', 'ff']]


print("\n--------Add Items:Extend()--------\n")
xlist = ["apple", "banana", "cherry"]
ylist = ["mango", "pineapple", "papaya"]
xlist.extend(ylist)     # extend a list
print(xlist)    # ['apple', 'banana', 'cherry', 'mango', 'pineapple', 'papaya']

xlist = ["apple", "banana", "cherry"]
ytuple = ("kiwi", "orange")
xlist.extend(ytuple)    # extend a tuple
print(xlist)    # ['apple', 'banana', 'cherry', 'kiwi', 'orange']

xlist = ["apple", "banana", "cherry"]
yset = {"kiwi", "orange"}
xlist.extend(yset)    # extend a set
print(xlist)    # ['apple', 'banana', 'cherry', 'kiwi', 'orange']

xlist = ["apple", "banana", "cherry"]
ydict = {"fruit1":"kiwi", "fruit2":"orange"}
xlist.extend(ydict)    # extend a dict
print(xlist)    # [['apple', 'banana', 'cherry', 'fruit1', 'fruit2']


```

---

### Change Item Value

- If insert **more items than** replace, the new items will be inserted where specified, and the remaining items will move accordingly

- If you insert less items than you replace, the new items will be inserted where you specified, and the remaining items will move accordingly
- Note: The **length of the list will change** when the number of items inserted does not match the number of items replaced.

```py
print("\n--------Change Item Value--------\n")
# Change one item value
xlist = ["apple", "banana", "cherry"]
xlist[1] = "blackcurrant"   # change item value
print(xlist)    # ['apple', 'blackcurrant', 'cherry']

# Change a Range of Item Values
# 1. 插入item数与index一致
xlist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
xlist[1:3] = ["blackcurrant", "watermelon"]     # 3 is exclusive,
print(xlist)    # ['apple', 'blackcurrant', 'watermelon', 'orange', 'kiwi', 'mango']

# 2. 插入item数大于index, 原有的顺延, 长度变长
xlist = ["apple", "banana", "cherry"]
xlist[1:2] = ["blackcurrant", "watermelon"]     # 2 is exclusive, oversize
print(xlist)    # ['apple', 'blackcurrant', 'watermelon', 'cherry']

# 3. 插入item数小于index, 原有的缩进, 长度变短
xlist = ["apple", "banana", "cherry"]
xlist[1:3] = ["watermelon"]
print(xlist)    # ['apple', 'watermelon']

```

---

### Remove List Items

- `remove()`: removes the specified item.
- `pop()`: removes the specified index.
  - If do not specify the index, the pop() method removes the last item.
- `del` keyword also removes the specified index
  - del keyword can also delete the list completely.
- `clear()`: empties the list. The list still remains, but it has no content.

```py
print("\n--------Remove Items:remove()--------\n")
xlist = ["apple", "banana", "cherry"]
xlist.remove("banana")
print(xlist)    # ['apple', 'cherry']


print("\n--------Remove Items:pop()--------\n")
xlist = ["apple", "banana", "cherry"]
xlist.pop()
print(xlist)    # ['apple', 'banana']

xlist = ["apple", "banana", "cherry"]
xlist.pop(1)
print(xlist)    # ['apple', 'cherry']


print("\n--------Remove Items:del--------\n")
xlist = ["apple", "banana", "cherry"]
del xlist[1]
print(xlist)    # ['apple', 'cherry']

xlist = ["apple", "banana", "cherry"]
del xlist
# print(xlist)    # NameError: name 'xlist' is not defined


print("\n--------Remove Items:clear()--------\n")
xlist = ["apple", "banana", "cherry"]
xlist.clear()
print(xlist)    # []

```

---

## Check if Item Exists:`in`

```py
xlist = ["apple", "banana", "cherry"]
if "apple" in xlist:
  print("Yes, 'apple' is in the fruits list")
```

---

## Loop Lists

- `for in` loop

- `for in range(len())` loop

- `while` Loop

  - Use the len() function to determine the length of the list, then start at 0 and loop your way through the list items by referring to their indexes.

```py

print("\n--------for in loop--------\n")
# for in loop
xlist = ["apple", "banana", "cherry"]
for x in xlist:
    print(x)


print("\n--------for in range loop--------\n")
# for in range(len())
xlist = ["apple", "banana", "cherry"]
for i in range(len(xlist)):     # [0, 1, 2]
    print(xlist[i])


print("\n--------While Loop--------\n")
# While Loop
xlist = ["apple", "banana", "cherry"]
i = 0
while i < len(xlist):   # 可以用于判断是否进入循环
    print(xlist[i])
    i = i + 1

```

---

## List Comprehension

- Syntax

`newlist = [expression for item in iterable if condition == True]`

- **Condition**
  - The condition is like a **filter** that only accepts the items that valuate to `True`.
  - The condition is **optional** and can be omitted
- **Iterable**
  - The iterable can be any **iterable object**, like a `list`, `tuple`, `set` etc.
- **Expression**
  - The expression is the **current item** in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list.
  - The expression can also **contain conditions**, not like a filter, but as a way to **manipulate the outcome**.

```py

print("\n--------List Comprehension--------\n")
print("\n--------Condition--------\n")
# regular
xlist = ["apple", "banana", "cherry", "kiwi", "mango"]
ylist = []
for x in xlist:
  if "a" in x:
    ylist.append(x)
print(ylist)


# condition
xlist = ["apple", "banana", "cherry", "kiwi", "mango"]
ylist = [x for x in xlist if "a" in x]
print(ylist)


print("\n--------iterable Object:list--------\n")
# copy a list
xlist = ['apple', 'banana', 'cherry']
ylist = [x for x in xlist]
print(ylist)


print("\n--------iterable Object:tuple--------\n")
# copy a tuple
xlist = ("apple", "banana", "cherry")
ylist = [x for x in xlist]
print(ylist)    # ['apple', 'banana', 'cherry']


print("\n--------iterable Object:dictionary--------\n")
# copy a dictionary
xlist = {"fruit01":"apple", "fruit02":"banana","fruit03": "cherry"}
ylist = [x for x in xlist]
print(ylist)    # ['fruit01', 'fruit02', 'fruit03']


print("\n--------iterable Object:set--------\n")
# copy a set
xlist = {"apple", "banana", "cherry"}
ylist = [x for x in xlist]
print(ylist)    # ['apple', 'banana', 'cherry']


print("\n--------iterable Object:range()--------\n")
# copy a range()
xlist = range(10)
ylist = [x for x in xlist]
print(ylist)    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print([x for x in range(10) if x <5])   # [0, 1, 2, 3, 4]


print("\n--------expression--------\n")
# expression
xlist = ["apple", "banana", "cherry"]
[print(x) for x in xlist]
# apple
# banana
# cherry

ylist = [x.upper() for x in xlist]
print(ylist)    # ['APPLE', 'BANANA', 'CHERRY']

ylist = ['hello' for x in xlist]    # set same item for a list of the same len
print(ylist)    # ['hello', 'hello', 'hello']

xlist = ["apple", "banana", "cherry"]
ylist = [x if x != "banana" else "orange" for x in xlist]
print(ylist)    # ['apple', 'orange', 'cherry'] 一般使用三目算式

```

---

## Sort List

### Sort List Alphanumerically

- List objects have a `sort()` method that will **sort the list alphanumerically**, ascending, by default.
- To sort descending, use the keyword argument `reverse = True`.

```py

print("\n--------sort()--------\n")

xlist = ["orange", "mango", "kiwi", "pineapple", "banana"]
xlist.sort()
print(xlist)    # ['banana', 'kiwi', 'mango', 'orange', 'pineapple']

xlist = [100, 50, 65, 82, 23]
xlist.sort()
print(xlist)    # [23, 50, 65, 82, 100]

print([100, 50, 65, 82, 23].sort()) # None注意: 因为sort是没有返回值

print("\n--------sort(): descend--------\n")
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist) # ['pineapple', 'orange', 'mango', 'kiwi', 'banana']


thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse = True)
print(thislist)     # [100, 82, 65, 50, 23]

```

---

### Customize Sort Function

- using the keyword argument `key = function`.

  - The function will return a number that will be used to sort the list (the lowest number first), 即按照 function 的返回排序

- **case-insensitive sort** function: use str.lower as a key function

  - By default the `sort()` method is case sensitive, resulting in all <u>capital</u> letters being sorted **before** <u>lower case</u> letters

```py
# Customize Sort Function
print("\n--------sort(): key= function--------\n")


def myfunc(n):
    return abs(n - 50)


xlist = [100, 50, 65, 82, 23]
xlist.sort(key=myfunc)
print(xlist)    # [50, 65, 23, 82, 100]

xlist = [100, 50, 65, 82, 23]
xlist.sort(key=myfunc, reverse=True)
print(xlist)    # [100, 82, 23, 65, 50]


print("\n---------case-insensitive sort--------\n")
xlist = ["banana", "Orange", "Kiwi", "cherry"]
xlist.sort()
print(xlist)    # ['Kiwi', 'Orange', 'banana', 'cherry']

xlist = ["banana", "Orange", "Kiwi", "cherry"]
xlist.sort(key=str.lower)
print(xlist)    # ['banana', 'cherry', 'Kiwi', 'Orange']
```

---

### Reverse Order

- `reverse()`: reverses the **current sorting order** of the elements

```py
xlist = ["banana", "Orange", "Kiwi", "cherry"]
xlist.reverse()
print(xlist)    # ['cherry', 'Kiwi', 'Orange', 'banana']

```

---

## Copy Lists

- cannot copy a list simply by typing `list2 = list1`, because: list2 will only be a **reference to** list1, and changes made in list1 will automatically also be made in list2.

- use the built-in List method `copy()`.
- Another way to make a copy is to use the built-in method `list()`.
- List Comprehension.`[x for x in xlist]`

```py
print("\n---------Copy list--------\n")
xlist = ["apple", "banana", "cherry"]
ylist = xlist
xlist[0] = "orange"
print(xlist)    # ['orange', 'banana', 'cherry']
print(ylist)    # ['orange', 'banana', 'cherry']
print(xlist is ylist)   # True, reference


print("\n---------copy()--------\n")
xlist = ["apple", "banana", "cherry"]
ylist = xlist.copy()
xlist[0] = "orange"
print(xlist)    # ['orange', 'banana', 'cherry']
print(ylist)    # ['apple', 'banana', 'cherry']
print(xlist is ylist)   # False


print("\n---------list()--------\n")
xlist = ["apple", "banana", "cherry"]
ylist = list(xlist)
xlist[0] = "orange"
print(xlist)    # ['orange', 'banana', 'cherry']
print(ylist)    # ['apple', 'banana', 'cherry']
print(xlist is ylist)   # False


print("\n---------List Comprehension--------\n")
xlist = ["apple", "banana", "cherry"]
ylist = [x for x in xlist]
xlist[0] = "orange"
print(xlist)    # ['orange', 'banana', 'cherry']
print(ylist)    # ['apple', 'banana', 'cherry']
print(xlist is ylist)   # False

```

---

## Join Two Lists

- `+` operator
- `for`+`append()`: appending all the items from list2 into list1
- `extend()`

```py
print("\n---------Join lists--------\n")

list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

print("\n---------Join lists:+--------\n")
list3 = list1 + list2
print(list3)    # ['a', 'b', 'c', 1, 2, 3]


print("\n---------Join lists:for append()--------\n")
for x in list2:
    list1.append(x)

print(list1)    # ['a', 'b', 'c', 1, 2, 3]

# 经典错误
list3 = list1.append(list2)
print(list3)    # None, append 参数不能是集合


print("\n---------Join lists:extend()--------\n")
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

list1.extend(list2)
print(list1)        # ['a', 'b', 'c', 1, 2, 3]

```

---

## count()

- `count()`: eturns the number of elements with the specified value.
  - Parameter: value
    **Required**. Any type (string, number, list, tuple, etc.). The value to search for.

```py
points = [1, 4, 2, 9, 7, 8, 9, 3, 1]
x = points.count(9)
print(x)    # 2


fruits = ['apple', 'banana', 'cherry']
x = fruits.count("cherry")
print(x)    # 1
```

---

## index()

- `index()`: Returns the index of the first element with the specified value

  - Parameter: elmnt
    Required. Any type (string, number, list, etc.). The element to search for
  - The index() method only returns **the first occurrence** of the value.

- 注意, 如果没有查找对象,则抛出异常.
-

```py
fruits = ['apple', 'banana', 'cherry']
print(fruits.index("cherry"))   # 2
# print(fruits.index(["cherry"]))   # ValueError: ['cherry'] is not in list
# ValueError: ['banana', 'cherry'] is not in list
# print(fruits.index(['banana', 'cherry']))

fruits = ['apple', ['banana', 'cherry']]
# ValueError: ['banana', 'cherry'] is not in list
print(fruits.index(['banana', 'cherry']))   # 1


fruits = [4, 55, 64, 32, 16, 32]
# print(fruits.index(1))  # ValueError: 1 is not in list
print(fruits.index(32))     # 3
```

---

[TOP](#python-list)
