# Python - Boolean

[Back](../index.md)

- [Python - Boolean](#python---boolean)
  - [`bool()` function](#bool-function)
  - [all() function](#all-function)
  - [any() function](#any-function)

---

- Booleans represent one of two values: `True` or `False`.

## `bool()` function

- `bool()`:evaluate any value, and give `True` or `False` in return,

- Almost any value is evaluated to `True` if it has some sort of content.

- Any string is `True`, **except empty strings**.

- Any number is `True`, **except 0**.

- Any `list`, `tuple`, `set`, and `dictionary` are `True`, **except empty ones**.

```py
# String
print("\n--------String--------\n")
print(bool("Hello"))    # True
print(bool(" "))    # True
print(bool(""))    # False


# Number
print("\n--------Number--------\n")
print(bool(15))     # True
print(bool(0.1))     # False
print(bool(0))     # False
print(bool(0.0))     # False
x, y = 100, 0
print(bool(x*y))     # False


# list
print("\n--------List--------\n")
print(bool(list()))     # False
print(bool([]))     # False
print(bool(["a"]))     # True


# tuple
print("\n--------Tuple--------\n")
print(bool(tuple()))     # False
print(bool(()))     # False
print(bool(("a")))     # True

# set
print("\n--------Set--------\n")
print(bool(set()))     # False
print(bool({}))     # False
print(bool(set([0, 1, 2, 3, 4])))     # True
print(bool({"a"}))     # True


# dict
print("\n--------Dict--------\n")
print(bool(dict()))     # False
print(bool({}))     # False
print(bool({"year": 1980}))     # True


# object
print("\n--------Object--------\n")


class myclass01():
    def __len__(self):
        return 0


myobj = myclass01()
print(bool(myobj))  # False


class myclass02():
    def __len__(self):
        return 1


myobj = myclass02()
print(bool(myobj))  # True


# function
print("\n--------function--------\n")


def myfunction():
    return True


print(myfunction())     # True


# isinstance()
print("\n--------isinstance() function--------\n")
x = 200
print(isinstance(x, int))       # True
print(isinstance(x, float))       # False


# others
print("\n--------others--------\n")
print(bool(False))     # False
print(bool(None))     # False

```

---

## all() function

- `all(iterable)`:
  - returns True if **all items** in an iterable are `True`, otherwise it returns `False`.
  - If the iterable object is **empty**, the all() function also returns `True`.
- Parameter
  - iterable: An iterable object (list, tuple, dictionary)
  - When used on a dictionary, the all() function checks if all the keys are true, not the values.

```py
print("\n--------all()--------\n")

print("\n--------list--------")
print(all([]))                  # True
print(all([0, 1, 1]))           # False
print(all([1, 1, 1]))           # True

print("\n--------tuple--------")
print(all(()))                  # True
print(all((1, True, False)))    # False
print(all((1, True, True)))     # True

print("\n--------set--------")
print(all({}))                  # True
print(all({0, 1, 0}))           # False
print(all({1, 1, True}))        # False

print("\n--------dict--------")
print(all(dict()))                      # True
print(all({0: "Apple", 1: "Orange"}))   # False
print(all({1: "Apple", 2: "Orange"}))   # True
```

---

## any() function

- `all(iterable)`:
- returns True if **any item** in an iterable are `True`, otherwise it returns `False`.
- If the iterable object is **empty**, the any() function will return `False`.
- Parameter
  - iterable: An iterable object (list, tuple, dictionary)
  - When used on a dictionary, the any() function checks if any of the **keys** are true, not the values.

```py
print("\n--------any()--------\n")

print("\n--------list--------")
print(any([]))                  # False
print(any([0, 1, 1]))           # True
print(any([0, 0, 0]))           # False

print("\n--------tuple--------")
print(any(()))                  # True
print(any((1, True, False)))    # False
print(any((0, False, False)))   # False

print("\n--------set--------")
print(any({}))                  # False
print(any({0, 1, True}))        # True
print(any({0, 0, False}))       # False

print("\n--------dict--------")
print(any(dict()))                      # False
print(any({0: "Apple", 1: "Orange"}))   # True
print(any({0: "Apple", 0: "Orange"}))   # False
```

---

[TOP](#python---boolean)
