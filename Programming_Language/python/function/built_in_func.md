# Python - Built-in Function

[Back](../index.md)

- [Python - Built-in Function](#python---built-in-function)
  - [Iterable Item](#iterable-item)
    - [`iter(object, sentinel)`](#iterobject-sentinel)
    - [`len(object)`](#lenobject)
    - [`next(iterable, default)`](#nextiterable-default)
    - [`all(iterable)`](#alliterable)
    - [`any(iterable)`](#anyiterable)
    - [`range(start, stop, step)`](#rangestart-stop-step)
    - [`enumerate(iterable, start)`](#enumerateiterable-start)
    - [`filter(function, iterable)`](#filterfunction-iterable)
    - [`map(function, iterables)`](#mapfunction-iterables)
    - [`zip([iterator])`](#zipiterator)
    - [`slice(start, end, step)`](#slicestart-end-step)
    - [`reversed(sequence)`](#reversedsequence)
    - [`sum(iterable, start)`](#sumiterable-start)
  - [Number Function](#number-function)
    - [`abs(n)`](#absn)
    - [`round(number, digits)`](#roundnumber-digits)
    - [`max()`](#max)
    - [`min()`](#min)
    - [`pow(x, y, z)`](#powx-y-z)
  - [Data Type Function](#data-type-function)
    - [`bool(object)`](#boolobject)
    - [`chr(number)`](#chrnumber)
    - [`float(value)`](#floatvalue)
  - [String Function](#string-function)
    - [`format(value, format)`](#formatvalue-format)
    - [`input(prompt)`](#inputprompt)
  - [Object Function](#object-function)
    - [`id(object)`](#idobject)
    - [`dir(object)`](#dirobject)
    - [`vars(object)`](#varsobject)
    - [`isinstance(object, type)`](#isinstanceobject-type)
    - [`issubclass(object, subclass)`](#issubclassobject-subclass)
    - [`hasattr(object, attribute)`](#hasattrobject-attribute)
    - [`getattr(object, attribute, default)`](#getattrobject-attribute-default)
    - [`setattr(object, attribute, value)`](#setattrobject-attribute-value)
    - [`delattr(object, attribute)`](#delattrobject-attribute)
  - [Code Function](#code-function)
    - [`eval(expression, globals, locals)`](#evalexpression-globals-locals)
    - [`exec(object, globals, locals)`](#execobject-globals-locals)
  - [File Function](#file-function)
    - [`open(file, mode)`](#openfile-mode)

---

## Iterable Item

### `iter(object, sentinel)`

- returns an iterator object.

- Parameter
  - `object`: Required. An iterable object
  - `sentinel`: Optional. If the object is a callable object the iteration will stop when the returned value is the same as the sentinel

```py
print("\n--------- iter(object, sentinel) --------\n")

x_iter = iter(["apple", "banana", "cherry"])

print(next(x_iter))     # apple
print(next(x_iter))     # banana
print(next(x_iter))     # cherry
# print(next(x_iter))     # StopIteration
```

---

### `len(object)`

- returns the number of items in an object.
- When the object is a string, the len() function returns the number of characters in the string.

- Parameter Description
  - `object`: Required. An object. Must be a sequence or a collection

```py
print("\n--------- len(object) --------\n")

print(len(["apple", "banana", "cherry"]))  # 3
print(len("Hello"))  # 5
```

---

### `next(iterable, default)`

- returns the **next item** in an iterator.

  - add a default return value, to return if the **iterable has reached to its end**.

- Parameter
  - `iterable`: Required. An iterable object.
  - `default`: Optional. An default value to return if the iterable has reached to its end.

```py
print("\n--------- next(iterable, default) --------\n")

x_list = iter(["apple", "banana", "cherry"])
print(next(x_list, "end"))      # apple
print(next(x_list, "end"))      # banana
print(next(x_list, "end"))      # cherry
print(next(x_list, "end"))      # end
print(next(x_list, "end"))      # end
```

---

### `all(iterable)`

- returns `True` if all items in an iterable are true, otherwise it returns `False`.

- If the iterable object is **empty**, the `all()` function also returns `True`.

- Parameter
  - `iterable`: An iterable object (list, tuple, dictionary)

```py
print("\n--------- all(iterable) --------\n")

# string list
print(all(["none", "str", "list"]))  # True
print(all(["", "str", "list"]))  # False

# num list
print(all([1, 1, 1]))  # True
print(all([0, 1, 1]))  # False

# boolean list
print(all([True, True, True]))  # True
print(all([False, True, True]))  # False

# set
print(all({-1, 1, 2}))  # True
print(all({0, 1, 2}))  # False

# dict, check all keys
print(all({1: "Apple", 2: "Orange"}))  # True
print(all({0: "Apple", 1: "Orange"}))  # False
```

---

### `any(iterable)`

- returns `True` if **any** item in an iterable are true, otherwise it returns `False`.
- If the iterable object is **empty**, the `any()` function will return `False`.

```py
print("\n--------- any(iterable) --------\n")

# false object
print(any([False, 0, "", [], (), set(), dict()]))  # False

# string list
print(any(["", "str", ""]))  # True
print(any(["", "", ""]))  # False

# num list
print(any([0, 1, 0]))  # True
print(any([0, 0, 0]))  # False

# boolean list
print(any([False, True, False]))  # True
print(any([False, False, False]))  # False

# set
print(any({0, 1}))  # True
print(any({0, None, ""}))  # False

# dict, check any keys
print(any({0: "Apple", 1: "Orange"}))  # True
print(any({0: "Apple"}))  # False
```

---

### `range(start, stop, step)`

- returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and stops before a specified number.

- Parameter
  - `start`: Optional. An integer number specifying at which position to start. Default is `0`
  - `stop`: Required. An integer number specifying at which position to stop, **exclusive**.
  - `step`: Optional. An integer number specifying the incrementation. Default is `1`

```py
print("\n--------- range(start, stop, step) --------\n")

for num in range(3):
    print(num)
# 0
# 1
# 2


for num in range(1, 4):
    print(num)
# 1
# 2
# 3

for num in range(1, 4, 2):
    print(num)
# 1
# 3

for num in range(3, 0, -1):
    print(num)
# 3
# 2
# 1
```

---

### `enumerate(iterable, start)`

- takes a collection (e.g. a tuple) and returns it as an enumerate object.

  - adds a counter as the key of the enumerate object.

- Parameter
  - `iterable`: An iterable object
  - `start`: A Number. Defining the start number of the enumerate object. Default 0

```py
print("\n--------- enumerate(iterable, start) --------\n")

x_list = ('apple', 'banana', 'cherry')

for index, itm in enumerate(x_list):
    print(index, itm)
# 0 apple
# 1 banana
# 2 cherry

for index, itm in enumerate(x_list, 10):
    print(index, itm)
# 10 apple
# 11 banana
```

---

### `filter(function, iterable)`

- returns an iterator(`filter object`) where the items are filtered through a function to test if the item is accepted or not.

- Parameter
  - `function`: A Function to be run for each item in the iterable
  - `iterable`: The iterable to be filtered

```py
print("\n--------- filter(object, globals, locals) --------\n")

ages = [5, 12, 17, 18, 24, 32]


def over18(x):
    if x < 18:
        return False
    else:
        return True


print(type(filter(over18, ages)))   # <class 'filter'>

[print(itm) for itm in filter(over18, ages)]
# 18
# 24
# 32
```

---

### `map(function, iterables)`

- return a `map` object.
- executes a specified function for each item in an iterable. The item is sent to the function as a parameter.

- Parameter
  - `function`: Required. The function to execute for each item
  - `iterable`: Required. A sequence, collection or an iterator object. You can send as many iterables as you like, just make sure the function has one parameter for each iterable.

```py
print("\n--------- map(function, iterables) --------\n")


def xFunc(n):
    return len(n)


mObj = map(xFunc, ('apple', 'banana', 'cherry'))
print(type(mObj))  # <class 'map'>

print([itm for itm in mObj])   # [5, 6, 6]


def yFunc(a, b):
    return a + " " + b


mObj = map(yFunc, ('apple', 'banana', 'cherry'),
           ('orange', 'lemon', 'pineapple'))
print([itm for itm in mObj])
# ['apple orange', 'banana lemon', 'cherry pineapple']

```

---

### `zip([iterator])`

- returns a `zip` object
- If the passed iterators have different lengths, the iterator with the **least items** decides the length of the new iterator.

- Parameter
  - `[iterator]`: Iterator objects that will be joined together

```py
print("\n--------- zip([iterator]) --------\n")

x_list = ("John", "Charles", "Mike")
y_list = ("Jenny", "Christy", "Monica")

print(type(zip(x_list, y_list)))    # <class 'zip'>

[print(x, y) for x, y in zip(x_list, y_list)]
# John Jenny
# Charles Christy
# Mike Monica

# shorter list decide the len
x_list = ("John", "Charles", "Mike")
y_list = ("Jenny", "Christy", "Monica", "Vicky")
[print(x, y) for x, y in zip(x_list, y_list)]
# John Jenny
# Charles Christy
# Mike Monica
```

---

### `slice(start, end, step)`

- returns a `slice` object.

- Parameter
  - `start`: Optional. An integer number specifying at which position to start the slicing. Default is 0
  - `end`: An integer number specifying at which position to end the slicing
  - `step`: Optional. An integer number specifying the step of the slicing. Default is 1

```py
print("\n--------- slice(start, end, step) --------\n")

nums = ("a", "b", "c", "d", "e", "f", "g", "h")
print(slice(2))  # slice(None, 2, None)
print(nums[slice(2)])  # ('a', 'b')

print(slice(3, 5))  # slice(3, 5, None)
print(nums[slice(3, 5)])  # ('d', 'e')

print(slice(0, 8, 3))  # slice(0, 8, 3)
print(nums[slice(0, 8, 3)])  # ('a', 'd', 'g')
```

---

### `reversed(sequence)`

- returns a reversed iterator object `list_reverseiterator`.

- Parameter
  - `sequence`: Required. Any iterable object

```py
print("\n--------- reversed(sequence) --------\n")

x_list = [1, 3, 5, 4, 2]
y_list = reversed(x_list)

print(type(x_list))  # <class 'list'>
print(x_list)   # [1, 3, 5, 4, 2]

print(type(y_list))  # <class 'list_reverseiterator'>
print(y_list)   # <list_reverseiterator object at 0x000001B0634310D0>

for itm in y_list:
    print(itm)
# 2
# 4
# 5
# 3
# 1
```

---

### `sum(iterable, start)`

- returns a number, the sum of all items in an iterable.

- Parameter
  - `iterable`: Required. The sequence to sum
  - `start`: Optional. A value that is added to the return value

```py
print("\n--------- sum(iterable, start) --------\n")

nums = (1, 2, 3, 4, 5)
print(sum(nums))    # 15
print(sum(nums, 7))  # 22
```

---

## Number Function

### `abs(n)`

- returns the **absolute value** of the specified number.

```py
print("\n--------- abs(n) --------\n")

print(abs(0))   # 0
print(abs(-7.25))   # 7.25
print(abs(7.25))    # 7.25
```

---

### `round(number, digits)`

- returns a floating point number that is a rounded version of the specified number, with the specified number of decimals.

- The default number of decimals is `0`, meaning that the function will return the nearest integer.

- Parameter
  - `number`: Required. The number to be rounded
  - `digits`: Optional. The number of decimals to use when rounding the number. Default is `0`

```py
print("\n--------- round(number, digits) --------\n")

print(round(5.76543))   # 6
print(round(5.76543, 2))   # 5.77
```

---

### `max()`

- returns the item with the **highest value**, or the item with the highest value in an iterable.
  - If the values are strings, an alphabetically comparison is done.

```py
print("\n--------- max() --------\n")

print(max(5, 10))   # 10
print(max("Mike", "John", "Vicky"))  # Vicky
print(max(1, 5, 3, 9))      # 9
```

---

### `min()`

- returns the item with the **lowest** value, or the item with the lowest value in an iterable.
  - If the values are strings, an alphabetically comparison is done.

```py
print("\n--------- min() --------\n")

print(min(5, 10))   # 5
print(min("Mike", "John", "Vicky"))  # John
print(min(1, 5, 3, 9))      # 1
```

---

### `pow(x, y, z)`

- returns the value of x to the power of y (xy).

  - If a third parameter is present, it returns x to the power of y, modulus z.

- Parameter
  - `x`: A number, the base
  - `y`: A number, the exponent
  - `z`: Optional. A number, the modulus

```py
print("\n--------- pow(x, y, z) --------\n")

print(pow(4, 3))    # 64
print(pow(4, 3, 5))    # 4
```

---

## Data Type Function

### `bool(object)`

- returns the boolean value of a specified object.

- The object will always return `True`, unless:

  - `[]`, `()`, `{}`
  - `False`
  - `0`
  - `None`

- Parameter
  - `object`: Any object, like `String`, `List`, `Number` etc.

```py
print("\n--------- bool(object) --------\n")

print(bool(0))  # False
print(bool(""))  # False
print(bool([]))  # False
print(bool(()))  # False
print(bool({}))  # False
print(bool(None))  # False
print(bool(False))  # False
```

---

### `chr(number)`

- returns the character that represents the specified unicode.

- Parameter
  - `number`: An integer representing a valid Unicode code point

```py
print("\n--------- chr(number) --------\n")

print(chr(13))  # Enter
print(chr(16))  # Shift
print(chr(17))  # Ctrl
print(chr(18))  # Alt
print(chr(27))  # ESC
print(chr(48))  # 0
print(chr(97))  # a
```

---

### `float(value)`

- converts the specified value into a floating point number.

- Parameter
  - `value`: A number or a string that can be converted into a floating point number

```py
print("\n--------- float(value) --------\n")

# num
print(float(3))  # 3.0
print(float(3.00000))  # 3.0

# str
print(float("3"))  # 3.0
print(type(float("3")))  # <class 'float'>
print(float("3.25"))  # 3.25
print(type(float("3.25")))  # <class 'float'>

# print(float(""))  # ValueError: could not convert string to float: ''
```

---

## String Function

### `format(value, format)`

- formats a specified value into a specified format.

- Parameter

  - `value`: A value of any format
  - `format`: The format you want to format the value into.

- **Legal values**

| Value | Description                                                       |
| ----- | ----------------------------------------------------------------- |
| `<`   | Left aligns the result (within the available space)               |
| `>`   | Right aligns the result (within the available space)              |
| `^`   | Center aligns the result (within the available space)             |
| `=`   | Places the sign to the left most position                         |
| `+`   | Use a plus sign to indicate if the result is positive or negative |
| `-`   | Use a minus sign for negative values only                         |
| ` `   | Use a leading space for positive numbers                          |
| `,`   | Use a comma as a thousand separator                               |
| `_`   | Use a underscore as a thousand separator                          |
| `b`   | Binary format                                                     |
| `c`   | Converts the value into the corresponding unicode character       |
| `d`   | Decimal format                                                    |
| `e`   | Scientific format, with a lower case e                            |
| `E`   | Scientific format, with an upper case E                           |
| `f`   | Fix point number format                                           |
| `F`   | Fix point number format, upper case                               |
| `g`   | General format                                                    |
| `G`   | General format (using a upper case E for scientific notations)    |
| `o`   | Octal format                                                      |
| `x`   | Hex format, lower case                                            |
| `X`   | Hex format, upper case                                            |
| `n`   | Number format                                                     |
| `%`   | Percentage format                                                 |

```py
print("\n--------- format(value, format) --------\n")

print(format(255, 'x'))  # ff
print(format(0.5, '%'))  # 50.000000%
```

---

### `input(prompt)`

- allows user input.

- Parameter
  - `prompt`: A String, representing a default message before the input.

```py
print("\n--------- input(prompt) --------\n")

name = input('Enter your name:\n')
print('Hello, ' + name)
```

---

## Object Function

### `id(object)`

- returns a unique id for the specified object.

- The id is the object's memory address

- Parameter
  - `object`: Any object, String, Number, List, Class etc.

```py
print("\n--------- id(object) --------\n")

x_tp = ('apple', 'banana', 'cherry')
print(id(x_tp))     # 2332518031552
```

---

### `dir(object)`

- returns a `enumerate object` object that contains all properties and methods of the specified object, without the values, including built-in properties which are default for all object.

- Parameter
  - `object`: The object you want to see the valid attributes of

```py
print("\n--------- dir(object) --------\n")


class Person:
    name = "John"
    age = 36
    country = "Norway"


[print(pop) for pop in dir(Person)]
# __class__
# __delattr__
# __dict__
# __dir__
# __doc__
# __eq__
# __format__
# __ge__
# __getattribute__
# __gt__
# __hash__
# __init__
# __init_subclass__
# __le__
# __lt__
# __module__
# __ne__
# __new__
# __reduce__
# __reduce_ex__
# __repr__
# __setattr__
# __sizeof__
# __str__
# __subclasshook__
# __weakref__
# age
# country
# name
```

---

### `vars(object)`

- returns the `__dict__` attribute of an object.
- The `__dict__` attribute is a dictionary containing the object's **changeable attributes**.

- Parameter Description
  - `object`: Any object with a `__dict__` attribute

```py
print("\n--------- vars(object) --------\n")


class Person:
    name = "John"
    age = 36
    country = "norway"


[print(k, ":", v) for k, v in vars(Person).items()]
# __module__ : __main__
# name : John
# age : 36
# country : norway
# __dict__ : <attribute '__dict__' of 'Person' objects>
# __weakref__ : <attribute '__weakref__' of 'Person' objects>
# __doc__ : None

```

---

### `isinstance(object, type)`

- returns `True` if the specified object is of the specified type, otherwise `False`.

- Parameter
  - `object`: Required. An object.
  - `type`: A type or a class, or a tuple of types and/or classes

```py
print("\n--------- isinstance(object, type) --------\n")

# int
print(isinstance(5, int))   # True

# a type tuple
print(isinstance("Hello", (float, int, str, list, dict, tuple)))  # True

# object


class xObj:
    name = "John"


obj = xObj()
print(isinstance(obj, xObj))    # True
```

---

### `issubclass(object, subclass)`

- returns `True` if the specified object is a **subclass** of the specified object, otherwise `False`.

- Parameter
  - `object`: Required. An object.
  - `subclass`: A class object, or a tuple of class objects

```py
print("\n--------- issubclass(object, subclass) --------\n")


class superObj:
    age = 36


class subObj(superObj):
    name = "John"
    age = superObj.age


print(issubclass(subObj, superObj))  # True
```

---

### `hasattr(object, attribute)`

- returns `True` if the specified object has the specified attribute, otherwise `False`.

- Parameter
  - `object`: Required. An object.
  - `attribute`: The name of the attribute you want to check if exists

```py
print("\n--------- hasattr(object, attribute) --------\n")


class Person:
    name = "John"
    age = 36
    country = "Norway"


print(hasattr(Person, 'age'))   # True
print(hasattr(Person, 'page'))   # False
```

---

### `getattr(object, attribute, default)`

- returns the value of the specified attribute from the specified object.

- Parameter
  - `object`: Required. An object.
  - `attribute`: The name of the attribute you want to get the value from
  - `default`: Optional. The value to return if the attribute does not exist

```py
print("\n--------- getattr(object, attribute, default) --------\n")


class Person:
    name = "John"
    age = 36
    country = "Norway"


print(getattr(Person, 'age'))   # 36
print(getattr(Person, 'page', 'my message'))   # my message
```

---

### `setattr(object, attribute, value)`

- sets the value of the specified attribute of the specified object.

- Parameter
  - `object`: Required. An object.
  - `attribute`: Required. The name of the attribute you want to set
  - `value`: Required. The value you want to give the specified attribute

```py
print("\n--------- setattr(object, attribute, value) --------\n")


class Person:
    name = "John"
    age = 36
    country = "Norway"


print(getattr(Person, 'age'))   # 36

setattr(Person, 'age', 40)
print(getattr(Person, 'age'))   # 40
```

---

### `delattr(object, attribute)`

- delete the specified attribute from the specified object.

- Parameter
  - `object`: Required. An object.
  - `attribute`: Required. The name of the attribute you want to remove

```py
print("\n--------- delattr(object, attribute) --------\n")


class Person:
    name = "John"
    age = 36
    country = "Norway"


print(hasattr(Person, "age"))   # True

delattr(Person, 'age')
print(hasattr(Person, "age"))   # False
```

---

## Code Function

### `eval(expression, globals, locals)`

- evaluates the specified expression, if the expression is a legal Python statement, it will be executed.

- Parameter
  - `expression`: A String, that will be evaluated as Python code
  - `globals`: Optional. A dictionary containing global parameters
  - `locals`: Optional. A dictionary containing local parameters

```py
print("\n--------- eval(expression, globals, locals) --------\n")

x = 'print(55)'
eval(x) # 55
```

---

### `exec(object, globals, locals)`

- executes the specified Python code.
- accepts large blocks of code, unlike the `eval()` function which only accepts a single expression

- Parameter
  - `object`: A String, or a code object
  - `globals`: Optional. A dictionary containing global parameters
  - `locals`: Optional. A dictionary containing local parameters

```py
print("\n--------- exec(object, globals, locals) --------\n")

code = 'name = "John"\nprint(name)'
exec(code)  # John
```

---

## File Function

### `open(file, mode)`

- opens a file, and returns it as a file object.

- Parameter

  - `file`: The path and name of the file
  - `mode`: A string, define which mode to open the file in

- Mode:

| Mode | Description                                                                      |
| ---- | -------------------------------------------------------------------------------- |
| `r`  | Read - Default value. Opens a file for reading, error if the file does not exist |
| `a`  | Append - Opens a file for appending, creates the file if it does not exist       |
| `w`  | Write - Opens a file for writing, creates the file if it does not exist          |
| `x`  | Create - Creates the specified file, returns an error if the file exist          |

| Mode | Description                        |
| ---- | ---------------------------------- |
| `t`  | Text - Default value. Text mode    |
| `b`  | Binary - Binary mode (e.g. images) |

```py
print("\n--------- open(file, mode) --------\n")

f = open("test.txt", "r")
print(f.read())
# fsdfsdfsdf
# sdfsdf
# dsf
# sdfsdff
# sdfsdfsdf
```

---

[TOP](#python---built-in-function)
