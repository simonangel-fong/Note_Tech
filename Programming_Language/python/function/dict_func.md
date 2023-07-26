# Python - Dictionary Method

[Back](../index.md)

- [Python - Dictionary Method](#python---dictionary-method)
  - [Construcor](#construcor)
    - [`dict(keyword arguments)`](#dictkeyword-arguments)
    - [`dict.fromkeys(keys, value)`](#dictfromkeyskeys-value)
  - [Manipulate item](#manipulate-item)
    - [`setdefault(keyname, value)`](#setdefaultkeyname-value)
    - [`update(iterable)`](#updateiterable)
    - [`pop(keyname, defaultvalue)`](#popkeyname-defaultvalue)
    - [`popitem()`](#popitem)
    - [`clear()`](#clear)
  - [Access Items](#access-items)
    - [`get(keyname, value)`](#getkeyname-value)
    - [`items()`](#items)
    - [`keys()`](#keys)
    - [`values()`](#values)
  - [Copy Dict](#copy-dict)
    - [`copy()`](#copy)

---

## Construcor

### `dict(keyword arguments)`

- creates a dictionary.

- Parameter
  - `keyword arguments`: Optional. As many keyword arguments you like, separated by comma: key = value, key = value ...

```py
print("\n--------- dict(keyword arguments) --------\n")

empty_dict = dict()
print(empty_dict)   # {}

x_dict = dict(brand="BMW", model="X5", year="1990")
print(x_dict)   # {'brand': 'BMW', 'model': 'X5', 'year': '1990'}
```

---

### `dict.fromkeys(keys, value)`

- returns a dictionary with the specified keys and the specified value.

- Parameter
  - `keys`: Required. An iterable specifying the **keys** of the new dictionary
  - `value`: Optional. The value for **all** keys. Default value is `None`

```py
print("\n--------- dict.fromkeys(keys, value) --------\n")

key_list = ("brand", "model", "year")

x_dict = dict.fromkeys(key_list)    # using None as default value
print(x_dict)   # {'brand': None, 'year': None}

x_dict = dict.fromkeys(key_list, "")
print(x_dict)   # {'brand': '', 'year': ''}

default_value = "unknown"
x_dict = dict.fromkeys(key_list, default_value)
print(x_dict)   # {'brand': 'unknown', 'model': 'unknown', 'year': 'unknown'}
```

---

## Manipulate item

### `setdefault(keyname, value)`

- returns the value of the item with the specified key.

- Parameter
  - `keyname`: Required. The **keyname** of the item you want to return the value from
  - `value`: Optional. If the key exist, this parameter has no effect. If the key does not exist, this value becomes the key's value. Default value `None`.

```py
print("\n--------- dictionary.setdefault(keyname, value) --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

print(car.setdefault("model", "Bronco"))
# Mustang, the default value is not appled when the key exists.

print(car)  # {'brand': 'Ford', 'model': 'Mustang', 'year': 1964}


print(car.setdefault("color", "white"))  # white
print(car)
# {'brand': 'Ford', 'model': 'Mustang', 'year': 1964, 'color': 'white'}
```

---

### `update(iterable)`

- inserts the specified items to the dictionary.

  - if the key does not exist, insert the new key-value pair.
  - Otherwise, update the value of the existing key.

- Parameter
  - `iterable`: A dictionary or an iterable **object with key value pairs**, that will be inserted to the dictionary

```py
print("\n--------- dictionary.update(iterable) --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# must be the dictionary type

# car.update("year") # ValueError: dictionary update sequence element #0 has length 1; 2 is required
# car.update("year", 1990) # TypeError: update expected at most 1 argument, got 2
# car.update(("year", 1990)) # ValueError: dictionary update sequence element #0 has length 4; 2 is required
# car.update({"year", 1990}) # TypeError: cannot convert dictionary update sequence element #0 to a sequence

car.update({"year": 1990})  # default value will not apply when the key exists.
print(car)  # {'brand': 'Ford', 'model': 'Mustang', 'year': 1990}

car.update({"color": "white"})
print(car) # {'brand': 'Ford', 'model': 'Mustang', 'year': 1990, 'color': 'white'}
```

---

### `pop(keyname, defaultvalue)`

- removes the specified item from the dictionary.

- Parameter

  - `keyname`: Required. The **keyname** of the item you want to remove
  - `defaultvalue`: Optional. A value to return **if the specified key do not exist.** If this parameter is not specified, and the no item with the specified key is found, an **error** is raised

- Return
  - The value of the removed item

```py
print("\n--------- dictionary.pop(keyname, defaultvalue) --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

print(car.pop("brand"))  # Ford
print(car.pop("model", "Model A"))
# Mustang, default is no applied when the key exists
print(car)  # {'year': 1964}

print(car.pop("price", 15000))  # 15000
print(car)  # {'year': 1964}
```

---

### `popitem()`

- removes the item that was **last** inserted into the dictionary.

- Return
  - The removed item

```py
print("\n--------- dictionary.popitem() --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

print(car.popitem())    # ('year', 1964)
```

---

### `clear()`

- removes all the elements from a dictionary.

```py
print("\n--------- dictionary.clear() --------\n")

x_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

x_dict.clear()
print(x_dict)   # {}
```

---

## Access Items

### `get(keyname, value)`

- returns the value of the item with the specified key.

- Parameter
  - `keyname`: Required. The keyname of the item you want to return the value from
  - `value` Optional. A value to return **if the specified key does not exist**. Default value `None`

```py
print("\n--------- dictionary.get(keyname, value) --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

print(car.get("model"))     # Mustang
print(car.get("model", "Model A"))
# Mustang, default value is not applied when the key exists.
print(car.get("price", 15000))  # 15000
```

---

### `items()`

- returns a `dict_items` object. The view object contains the `key-value` pairs of the dictionary, as tuples in a list.

```py
print("\n--------- dictionary.items() --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

xItems = car.items()

print(type(xItems))  # <class 'dict_items'>
# dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 1964)])
print(xItems)
[print(itm) for itm in xItems]
# ('brand', 'Ford')
# ('model', 'Mustang')
# ('year', 1964)

[print(itm[0], itm[1]) for itm in xItems]
# brand Ford
# model Mustang
# year 1964

# pionter
car.update({'color': 'white'})
# dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 1964), ('color', 'white')])
print(xItems)
```

---

### `keys()`

- returns a `dict_keys` object. The view object contains the keys of the dictionary, as a list.

```py
print("\n--------- dictionary.keys() --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

xItems = car.keys()

print(type(xItems))  # <class 'dict_keys'>
print(xItems)  # dict_keys(['brand', 'model', 'year'])

[print(itm, ':', car[itm]) for itm in xItems]
# brand : Ford
# model : Mustang
# year : 1964

# pointer
car.update({"color": "white"})
print(xItems)   # dict_keys(['brand', 'model', 'year', 'color'])
```

---

### `values()`

- returns a `dict_values` object that contains the values of the dictionary, as a list.
- It is a pointer: when the dict is updated, the existing `dict_values` object will update as well.

```py
print("\n--------- dictionary.values() --------\n")

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

val_itm = car.values()

print(type(val_itm))    # <class 'dict_values'>
print(val_itm)    # dict_values(['Ford', 'Mustang', 1964])

# a pointer
car.update({"color":"white"})

print(val_itm)    # dict_values(['Ford', 'Mustang', 1964, 'white'])
```

---

## Copy Dict

### `copy()`

- returns a copy of the specified dictionary.

```py
print("\n--------- dictionary.copy() --------\n")

x_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# deep copy
y_dict = x_dict.copy()

y_dict["brand"] = "BMW"
y_dict["model"] = "X5"

print(x_dict)   # {'brand': 'Ford', 'model': 'Mustang', 'year': 1964}
print(y_dict)   # {'brand': 'BMW', 'model': 'X5', 'year': 1964}
```

---

[TOP](#python---dictionary-method)
