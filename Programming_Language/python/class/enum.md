# Python - Enum Class

[Back](../index.md)

- [Python - Enum Class](#python---enum-class)
  - [Enum class](#enum-class)
  - [Create and Access to Enum Class](#create-and-access-to-enum-class)
  - [Loop Enum](#loop-enum)
  - [List an Enum](#list-an-enum)
  - [Enum's Size: len()](#enums-size-len)
  - [Compare Enum Memebers](#compare-enum-memebers)

---

## Enum class

- `Enum` is the **class** in Python used for developing the enumerations.
  - 通常用于创建常量, 因为 Python 没有常量.
- `Enumeration` is the **set** of symbolic members or names which are **bounded to the constant and unique values**.

  - The members of the enumeration can be equated by using these symbolic names.
  - The enumeration can be repeated by itself over them.

- The members of the Enum class are called Enumeration, and also hashable.

  - Therefore, these members can be used for sets and dictionaries.

- The characteristics of the Enum class are:
  - The users can check the types of Enum by using the `type()` method.
  - By using the 'name' keyword, the users can display the name of the Enum.
  - The Enum is the evaluable string representation of the object known as `repr()`.

---

## Create and Access to Enum Class

- import enum file
- using inheritance `class enum_name(enum.Enum):`

```py
import enum
# we will use enum class for creating enumerations


class Weekdays(enum.Enum):
    Sunday = 1
    Monday = 2
    Tuesday = 3
    Wednesday = 4
    Thursday = 5
    Friday = 6
    Saturday = 7


# print the enum member as the string
print(Weekdays.Wednesday)           # Weekdays.Wednesday

# check the type of enum member
print(type(Weekdays.Wednesday))     # <enum 'Weekdays'>

# access member by name
print(Weekdays["Wednesday"])        # Weekdays.Wednesday
# access member by value
print(Weekdays(4))                  # Weekdays.Wednesday

# print the enum member as a repr object
print(repr(Weekdays.Wednesday))     # <Weekdays.Wednesday: 4>

# print name of enum member
print(Weekdays.Wednesday.name)      # Wednesday
print(Weekdays.Wednesday.value)     # 4
```

---

## Loop Enum

```py
# loop an enum object
for weekday in Weekdays:
    print(weekday)
# Weekdays.Sunday
# Weekdays.Monday
# Weekdays.Tuesday
# Weekdays.Wednesday
# Weekdays.Thursday
# Weekdays.Friday
# Weekdays.Saturday

```

---

## List an Enum

```py
# list all members
print(list(Days))
# [<Days.Sunday: 1>, <Days.Monday: 2>, <Days.Wednesday: 4>, <Days.Thursday: 5>, <Days.Saturday: 7>]

```

---

## Enum's Size: len()

```py
# get enum class's size
print(len(Weekdays))    # 7

```

---

## Compare Enum Memebers

```py
import enum
# we will use enum class for creating enumerations


class Days(enum.Enum):
    Sunday = 1
    Monday = 2
    Tuesday = 1
    Wednesday = 4
    Thursday = 5
    Friday = 4
    Saturday = 7


# 1==1
if Days.Sunday == Days.Tuesday:
    print('Match')  # Match
else:
    print('Do not Match')

# 2!=1
if Days.Monday != Days.Tuesday:
    print('Do not Match')  # Do not Match
else:
    print('Match')

# 4==4
if Days.Wednesday == Days.Friday:
    print('Match')  # Match
else:
    print('Do not Match')

# 5!=4
if Days.Thursday != Days.Friday:
    print('Do not Match')  # Do not Match
else:
    print('Match')

```

---

[TOP](#python---enum-class)
