# Data Type

[Back](../index.md)

- [Data Type](#data-type)
  - [Built-in Data Types](#built-in-data-types)
  - [Set and Get Data Type](#set-and-get-data-type)
  - [Casting](#casting)

---

## Built-in Data Types

- Variables can store data of different **types**, and different **types** can do different **things**.

- Python has the following data types built-in by default, in these categories:

- 4 built-in data types in Python used to store collections of data:
  - `List` is a collection which is **ordered** and **changeable**. Allows **duplicate** members.
  - `Tuple` is a collection which is **ordered** and **unchangeable**. Allows **duplicate** members.
  - `Set` is a collection which is **unordered**, **unchangeable**, and **unindexed**. **No duplicate** members.(but can remove and/or add items)
  - `Dictionary` is a collection which is **ordered** and **changeable**. **No duplicate** members.

| Categories     | Built-in Data Type                 |
| -------------- | ---------------------------------- |
| Text Type      | `str`                              |
| Numeric Types  | `int`, `float`, `complex`          |
| Boolean Type   | `bool`                             |
| Binary Types   | `bytes`, `bytearray`, `memoryview` |
| None Type      | `NoneType`                         |
| Sequence Types | `list`, `tuple`, `range`           |
| Mapping Type   | `dict`                             |
| Set Types      | `set`, `frozenset`                 |

---

## Set and Get Data Type

- In Python, the data type is set **when you assign a value to a variable**.

- `type()` Function:

  - returns the type of the specified object

- `isinstance()` Function:
  - returns True if the specified object is of the specified type, otherwise False.
  - If the type parameter is a tuple, this function will return True if the object is one of the types in the tuple.

```py

# Text Type
print("\n--------str--------")
x = "Hello World"           # str
print(x)                    # Hello World
print(type(x))              # <class 'str'>
print(isinstance(x, str))   # True


# Numeric Types
print("\n--------int--------")
x = 20                      # int
print(x)                    # 20
print(type(x))              # <class 'int'>
print(isinstance(x, int))   # True

print("\n--------float--------")
x = 20.5                    # float
print(x)                    # 20.5
print(type(x))              # <class 'float'>
print(isinstance(x, float))  # True


print("\n--------complex--------")
x = 1j                          # complex
print(x)                        # 1j
print(type(x))                  # <class 'complex'>
print(isinstance(x, complex))   # True


# Sequence Types
print("\n--------list--------")
x = ["apple", "banana", "cherry"]   # list
print(x)                            # ['apple', 'banana', 'cherry']
print(type(x))                      # <class 'list'>
print(isinstance(x, list))          # True


print("\n--------tuple--------")
x = ("apple", "banana", "cherry")   # tuple
print(x)                            # ("apple", "banana", "cherry")
print(type(x))                      # <class 'tuple'>
print(isinstance(x, tuple))         # True


print("\n--------range--------")
x = range(6)                    # range
print(x)                        # range(0, 6)
print(type(x))                  # <class 'range'>
print(isinstance(x, range))     # True


# Mapping Type
print("\n--------dict--------")
x = {"name": "John", "age": 36}     # dict
print(x)                            # {'name': 'John', 'age': 36}
print(type(x))                      # <class 'dict'>
print(isinstance(x, dict))          # True


# Set Types
print("\n--------set--------")
x = {"apple", "banana", "cherry"}   # set
print(x)                            # {'cherry', 'banana', 'apple'}
print(type(x))                      # <class 'set'>
print(isinstance(x, set))           # True


print("\n--------frozenset--------")
x = frozenset({"apple", "banana", "cherry"})    # frozenset
# frozenset({'cherry', 'apple', 'banana'})
print(x)
print(type(x))                                  # <class 'frozenset'>
print(isinstance(x, frozenset))                 # True


# Boolean Type
print("\n--------bool--------")
x = True                    # bool
print(x)                    # True
print(type(x))              # <class 'bool'>
print(isinstance(x, bool))  # True


# Binary Types
print("\n--------bytes--------")
x = b"Hello"                    # bytes
print(x)                        # b'Hello'
print(type(x))                  # <class 'bytes'>
print(isinstance(x, bytes))     # True


print("\n--------bytearray--------")
x = bytearray(5)                    # bytearray
print(x)                            # bytearray(b'\x00\x00\x00\x00\x00')
print(type(x))                      # <class 'bytearray'>
print(isinstance(x, bytearray))     # True


print("\n--------memoryview--------")
x = memoryview(bytes(5))            # memoryview
print(x)                            # <memory at 0x0000017D55987DC0>
print(type(x))                      # <class 'memoryview'>
print(isinstance(x, memoryview))    # True


# None Type
print("\n--------NoneType--------")
x = None                            # NoneType
print(x)                            # None
print(type(x))                      # <class 'NoneType'>
# print(isinstance(x, NoneType))    # NameError: name 'NoneType' is not defined

```

---

## Casting

- use the constructor functions

```py

print("\n--------str()--------")
x =str(2.5)
print(x)  # 2.5
print(type(x))  # <class 'str'>


print("\n--------int()--------")
x =int("2")
print(x)  # 2
print(type(x))  # <class 'int'>


print("\n--------float()--------")
x =float("2.5")
print(x)  # 2.5
print(type(x))  # <class 'float'>


print("\n--------complex()--------")
x =complex("1j")
print(x)  # 1j
print(type(x))  # <class 'complex'>


print("\n--------list()--------")
x =list(("apple", "banana", "cherry"))
print(x)  # ['apple', 'banana', 'cherry']
print(type(x))  # <class 'list'>


print("\n--------tuple()--------")
x =tuple(["apple", "banana", "cherry"])
print(x)  # ('apple', 'banana', 'cherry')
print(type(x))  # <class 'tuple'>


print("\n--------range()--------")
x =range(6)
print(x)  #range(0, 6)
print(type(x))  # <class 'range'>


print("\n--------dict()--------")
x =dict(name="John", age=36)
print(x)  #{'name': 'John', 'age': 36}
print(type(x))  # <class 'dict'>


print("\n--------set()--------")
x =set(("apple", "banana", "cherry"))
print(x)  #{'apple', 'banana', 'cherry'}
print(type(x))  # <class 'set'>


print("\n--------frozenset()--------")
x =frozenset(("apple", "banana", "cherry"))
print(x)  #frozenset({'banana', 'cherry', 'apple'})
print(type(x))  # <class 'frozenset'>


print("\n--------frozenset()--------")
x =frozenset(("apple", "banana", "cherry"))
print(x)  #frozenset({'banana', 'cherry', 'apple'})
print(type(x))  # <class 'frozenset'>


print("\n--------bool()--------")
x =bool(5)
print(x)  #True
print(type(x))  # <class 'bool'>


print("\n--------bytes()--------")
x =bytes(5)
print(x)  #b'\x00\x00\x00\x00\x00'
print(type(x))  # <class 'bytes'>


print("\n--------bytearray()--------")
x =bytearray(5)
print(x)  #bytearray(b'\x00\x00\x00\x00\x00')
print(type(x))  # <class 'bytearray'>


print("\n--------memoryview()--------")
x =memoryview(bytes(5))
print(x)  #<memory at 0x000002ADF8767DC0>
print(type(x))  # <class 'memoryview'>

```

---

[TOP](#data-type)
