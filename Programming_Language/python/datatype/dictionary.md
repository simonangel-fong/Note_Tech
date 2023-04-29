# Python - Dictionary

[Back](../index.md)

- [Python - Dictionary](#python---dictionary)
  - [Dictionary](#dictionary)
    - [Dictionary Methods](#dictionary-methods)
    - [Create a dictionary](#create-a-dictionary)
    - [Access Items](#access-items)
    - [Add Dictionary Items](#add-dictionary-items)
    - [Change Item Value](#change-item-value)
    - [Remove Dict Items](#remove-dict-items)
  - [Check if Key Exists: `in`](#check-if-key-exists-in)
  - [Loop Dictionaries](#loop-dictionaries)
  - [Copy Dictionaries](#copy-dictionaries)
  - [Nested Dictionaries](#nested-dictionaries)
  - [`fromkeys()`](#fromkeys)
  - [`setdefault()`](#setdefault)

---

## Dictionary

- `Dictionaries` are used to store data values **in key:value pairs**.

  - A `dictionary` is a collection which is **ordered**, **changeable** and do **not allow duplicates**.
  - Dictionaries are written with **curly brackets**, and have keys and values.

- `Dictionary` items are presented in **key:value pairs**, and can be referred to by using the **key name**.

- **Ordered**

  - When we say that dictionaries are **ordered**, it means that the items have a **defined order**, and that **order will not change**.
  - **Unordered** means that the items does **not have a defined order**, cannot refer to an item **by using an index**.

- **Changeable**

  - Dictionaries are **changeable**, meaning that we can <u>change, add or remove items</u> after the dictionary has been created.

- **Duplicates Not Allowed**

  - Dictionaries **cannot have two items with the same key**

- **Data Types**
  - The **values** in dictionary items can be of **any data type**.

---

### Dictionary Methods

- Create Dict

  | Method       | Description                                            |
  | ------------ | ------------------------------------------------------ |
  | `dict()`     | Returns a dictionary                                   |
  | `fromkeys()` | Returns a dictionary with the specified keys and value |

- Access Items

  | Method     | Description                                               |
  | ---------- | --------------------------------------------------------- |
  | `get()`    | Returns the value of the specified key                    |
  | `items()`  | Returns a list containing a tuple for each key value pair |
  | `keys()`   | Returns a list containing the dictionary's keys           |
  | `values()` | Returns a list of all the values in the dictionary        |

- Add Items

  | Method         | Description                                                                                                 |
  | -------------- | ----------------------------------------------------------------------------------------------------------- |
  | `update()`     | Updates the dictionary with the specified key-value pairs                                                   |
  | `setdefault()` | Returns the value of the specified key. If the key does not exist: insert the key, with the specified value |

- Change Items

  | Method         | Description                                                                                                 |
  | -------------- | ----------------------------------------------------------------------------------------------------------- |
  | `update()`     | Updates the dictionary with the specified key-value pairs                                                   |
  | `setdefault()` | Returns the value of the specified key. If the key does not exist: insert the key, with the specified value |

- Remove Items

  | Method      | Description                                  |
  | ----------- | -------------------------------------------- |
  | `pop()`     | Removes the element with the specified key   |
  | `popitem()` | Removes the last inserted key-value pair     |
  | `clear()`   | Removes all the elements from the dictionary |

- Copyt Items

  | Method   | Description                      |
  | -------- | -------------------------------- |
  | `copy()` | Returns a copy of the dictionary |

---

### Create a dictionary

- 1. curly brackets + key-value paires

- 2. `dict()` Constructor

```py
# create a list

print("\n--------Create a Dictionary--------\n")
xdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964,       # will be rewritten, not allow to duplicate
    "year": 2020
}
print(xdict)            # {'name': 'John', 'age': 36, 'country': 'Norway'}


xdict = dict(name="John", age=36, country="Norway")
print(xdict)            # {'name': 'John', 'age': 36, 'country': 'Norway'}

xdict = dict()
print(type(xdict))      # <class 'dict'>
print(xdict)            # {}

xdict = {}
print(type(xdict))      # <class 'dict'>
print(xdict)            # {}

```

---

### Access Items

- access the items of a dictionary by referring to its **key name**, inside **square brackets**.

- `get()`: return the value of a specific key.

- `keys()`: return a list of **all the keys** in the dictionary.

  - returns a `dict_keys` object.

  - any changes done to the dictionary will be reflected in the keys list.

- `values()`: return a list of **all the values** in the dictionary.

  - any changes done to the dictionary will be reflected in the values list.

- `items()` return each item in a dictionary, as tuples in a list.
  - changes done to the dictionary will be reflected in the items list.

```py
print("\n--------Access Items--------\n")

print("\n--------[key_name]--------\n")
# by key_name
xdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
value = xdict["model"]
print(value)            # Mustang


print("\n--------.get('key_name')--------\n")
# get()
xdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
value = xdict.get("model")
print(value)            # Mustang


print("\n--------.keys():dict_keys--------\n")
xdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
keys = xdict.keys()
print(keys)                    # dict_keys(['brand', 'model', 'year'])
print(type(keys))              # <class 'dict_keys'>
# print(keys[0])                 # TypeError: 'dict_keys' object is not subscriptable
# print(keys["brand"])           # TypeError: 'dict_keys' object is not subscriptable

for k in keys:
    print(k)
# brand
# model
# year

print(list(keys)[0])           # brand

xdict["year"] = 2020
keys = xdict.keys()
# value list updated: dict_keys(['brand', 'model', 'year'])
print(keys)

xdict["color"] = "red"
keys = xdict.keys()
# value list updated: dict_keys(['brand', 'model', 'year', 'color'])
print(keys)


print("\n--------.values():dict_values--------\n")
xdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
values = xdict.values()
print(values)                    # dict_values(['Ford', 'Mustang', 1964])
print(type(values))              # <class 'dict_values'>
# print(values[0])                 # TypeError: 'dict_values' object is not subscriptable
# print(values["brand"])           # TypeError: 'dict_values' object is not subscriptable

for i in values:
    print(i)
# Ford
# Mustang
# 1964

print(list(values)[0])           # Ford

xdict["year"] = 2020
values = xdict.values()
# value list updated: dict_values(['Ford', 'Mustang', 2020])
print(values)

xdict["color"] = "red"
values = xdict.values()
# value list updated: dict_values(['Ford', 'Mustang', 2020, 'red'])
print(values)


print("\n--------.items():dict_items--------\n")
xdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
items = xdict.items()
# dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 1964)])
print(items)
print(type(items))              # <class 'dict_items'>
# print(items[0])                 # TypeError: 'dict_items' object is not subscriptable
# print(items["brand"])           # TypeError: 'dict_items' object is not subscriptable

for i in items:
    print(i)
# ('brand', 'Ford')
# ('model', 'Mustang')
# ('year', 1964)

print(list(items)[0])           # ('brand', 'Ford')

xdict["year"] = 2020
items = xdict.items()
# value list updated: dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 2020)])
print(items)

xdict["color"] = "red"
items = xdict.items()
# value list updated: dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 2020), ('color', 'red')])
print(items)

```

---

### Add Dictionary Items

- using a new **index key** and assigning a **value**

- `update()`: update the dictionary with the items from a given argument.
  - If the item does **not exist**, the item will be **added**.
  - The argument must be a dictionary, or an iterable object with key:value pairs.

```py

print("\n--------Add Items--------\n")
# using key name
xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
xDict["color"] = "red"
# {'brand': 'Ford', 'model': 'Mustang', 'year': 1964, 'color': 'red'}
print(xDict)


# update()
xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
xDict.update({"color": "red"})
# {'brand': 'Ford', 'model': 'Mustang', 'year': 1964, 'color': 'red'}
print(xDict)

```

---

### Change Item Value

- change the value of a specific item by referring to its **key name**

- `update()`: update the dictionary with the items from the given argument.
  - The argument must be a `dictionary`, or an iterable object with **key:value pairs**.

```py

print("\n--------Change Item Value--------\n")
# using key name
xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
xDict["year"] = 2018

print(xDict)    # {'brand': 'Ford', 'model': 'Mustang', 'year': 2018}


# update()
xDict.update({"year": 2020})

print(xDict)    # {'brand': 'Ford', 'model': 'Mustang', 'year': 2020}
```

---

### Remove Dict Items

- `pop()`: removes the item with the specified key name
- `popitem()`: removes the last inserted item
- `del` keyword removes the item with the specified key name
- `clear()`: empties the dictionary

```py
print("\n--------Remove Items--------\n")
# pop()
xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
remove_value = xDict.pop("model")
print(remove_value)                 # Mustang
print(xDict)                        # {'brand': 'Ford', 'year': 1964}


# popitem
xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
remove_item = xDict.popitem()
print(remove_item)                  # ('year', 1964)
print(xDict)                        # {'brand': 'Ford', 'model': 'Mustang'}


# del
xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

del xDict["model"]
print(xDict)                        # {'brand': 'Ford', 'year': 1964}

del xDict
# print(xDict)                        # NameError: name 'xDict' is not defined


# clear()
xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
xDict.clear()
print(xDict)                        # {}
```

---

## Check if Key Exists: `in`

```py
xDict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
if "model" in xDict:
  print("Yes, 'model' is one of the keys in the xDict dictionary")

```

---

## Loop Dictionaries

- `for in` loop

```py

print("\n--------for in loop--------\n")

xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# loop keys
for x in xDict:
    print(x)
# brand
# model
# year

for x in xDict.keys():
    print(x)
# brand
# model
# year


# loop values
for x in xDict:
    print(xDict[x])
# Ford
# Mustang
# 1964

for x in xDict.values():
    print(x)
# Ford
# Mustang
# 1964


# loop items
for x in xDict.items():
    print(x)
# ('brand', 'Ford')
# ('model', 'Mustang')
# ('year', 1964)

for x, y in xDict.items():
    print(x, y)
# brand Ford
# model Mustang
# year 1964
```

---

## Copy Dictionaries

- cannot copy a dictionary simply by typing `dict2 = dict1`, because: dict2 will only be a **reference to** dict1, and changes made in dict1 will automatically also be made in dict2.

- `copy()`: make a copy of a dictionary
- `dict()`: make a new dictionary from an existing dictionary

```py

print("\n--------Copy dict: copy()--------\n")

xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
yDict = xDict.copy()

xDict.update({"year": 2020})

print(xDict)            # {'brand': 'Ford', 'model': 'Mustang', 'year': 2020}
print(yDict)            # {'brand': 'Ford', 'model': 'Mustang', 'year': 1964}


print("\n--------Copy dict: dict()--------\n")

xDict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
yDict = dict(xDict)

xDict.update({"year": 2020})

print(xDict)            # {'brand': 'Ford', 'model': 'Mustang', 'year': 2020}
print(yDict)            # {'brand': 'Ford', 'model': 'Mustang', 'year': 1964}
```

---

## Nested Dictionaries

- A `dictionary` can contain dictionaries, this is called nested dictionaries.

- **Access Items in Nested Dictionaries**
  - To access items from a nested dictionary, you use the name of the dictionaries, **starting with the outer dictionary**.

```py

print("\n--------Nested Dictionary--------\n")

xDict = {
    "child1": {
        "name": "Emil",
        "year": 2004
    },
    "child2": {
        "name": "Tobias",
        "year": 2007
    },
    "child3": {
        "name": "Linus",
        "year": 2011
    }
}
# {'child1': {'name': 'Emil', 'year': 2004}, 'child2': {'name': 'Tobias', 'year': 2007}, 'child3': {'name': 'Linus', 'year': 2011}}
print(xDict)

child1 = {
    "name": "Emil",
    "year": 2004
}
child2 = {
    "name": "Tobias",
    "year": 2007
}
child3 = {
    "name": "Linus",
    "year": 2011
}

xDict = {
    "child1": child1,
    "child2": child2,
    "child3": child3
}
# {'child1': {'name': 'Emil', 'year': 2004}, 'child2': {'name': 'Tobias', 'year': 2007}, 'child3': {'name': 'Linus', 'year': 2011}}
print(xDict)


print("\n--------Access inner value--------\n")

print(xDict["child2"]["name"])  # Tobias

```

---

## `fromkeys()`

- `fromkeys()`: returns a dictionary with the specified keys and the specified value

- `dict.fromkeys(keys, value)`
  - `keys`: Required. An iterable specifying the keys of the new dictionary
  - `value`: Optional. The value for all keys. Default value is None

```py
print("\n--------fromkeys()--------\n")
keys = ('key1', 'key2', 'key3')
xDict = dict.fromkeys(keys)

print(xDict)     # {'key1': None, 'key2': None, 'key3': None}


xDict = dict.fromkeys(('key1',), 'value1')
xDict = dict.fromkeys(('key2',), 'value2')

print(xDict)     # {'key2': 'value2'}

```

---

## `setdefault()`

- `setdefault()`: returns the value of the item with the specified key.

  - If the key does not exist, insert the key, with the specified value

- `.setdefault(keyname, value)`
  - `keyname`: Required. The keyname of the item you want to return the value from
  - `value`: Optional.
    - If the key exist, this parameter has no effect.
    - If the key does not exist, this value becomes the key's value
    - Default value None

```py

print("\n--------setdefault()--------\n")
car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# If the key exist, this parameter has no effect.
x = car.setdefault("model", "Bronco")

print(x)    # Mustang


car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# If the key does not exist, this value becomes the key's value
x = car.setdefault("color", "white")

print(x)    # white
```

---

[TOP](#python---dictionary)
