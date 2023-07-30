# Python - String

[Back](../index.md)

- [Python - String](#python---string)
  - [Strings](#strings)
  - [Strings are Arrays](#strings-are-arrays)
  - [String: More than one line](#string-more-than-one-line)
  - [String Length: `len()`](#string-length-len)
  - [String Check: `in`](#string-check-in)
  - [String Slicing](#string-slicing)
  - [String Function](#string-function)
  - [String Concatenation](#string-concatenation)
  - [String Format](#string-format)
    - [str.format() Method](#strformat-method)
    - [F-string Method](#f-string-method)
  - [Escape Character](#escape-character)
  - [Prefix: `b""`, `r""`](#prefix-b-r)
  - [String Methods](#string-methods)

---

## Strings

- `Strings` in python are surrounded by either single quotation marks, or double quotation marks.

  - `'hello'` is the same as `"hello"`.

- **Multiline Strings**

```py
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""

print(a)

a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)
```

---

## Strings are Arrays

- Strings in Python are arrays of bytes representing unicode characters.

- However, Python does not have a character data type, a **single character** is simply a <u>string with a length of 1</u>.

```py
a = "Hello, World!"
print(a[0]) #H
print(a[1]) #e
print(a[len(a)-1]) #!

for x in a:
    print(x)

# H
# e
# !
# H
# e
# l
# l
# o
# ,

# W
# o
# r
# l
# d
# !
```

---

## String: More than one line

- Three quotational marks.

```py
xStr = ''' Hello,
    world'''

print(xStr)
#  Hello,
#     world
```

---

## String Length: `len()`

- To get the length of a string, use the `len()` function.

```py
a = "Hello, World!"
print(len(a))   #13
```

---

## String Check: `in`

- To check if a certain phrase or character is present in a string, we can use the keyword in.

```py
txt = "The best things in life are free!"

print("free" in txt)    # true
print("expensive" not in txt)   # true

if "free" in txt:
  print("Yes, 'free' is present.")

if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")
```

---

## String Slicing

- The first character has index `0`.
- The last character does not include.

```py
b = "Hello, World!"

print(b[0]) # H
print(b[0:1]) # H not inclusive
print(b[2:5]) # llo
print(b[:5]) # Hello
print(b[2:]) # llo, World!
print(b[-5:-2]) # orl
```

- Slice a string with step
  - `str[begin_index: last_index: step]`

```py

arr = "ABCDEFG"

print(arr[::])  # ABCDEFG, grap all characters
print(arr[::1])  # ABCDEFG, grap all characters
print(arr[::2])  # ACEG, grap characters from beginning to the end with step of 2
print(arr[::-1])  # GFEDCBA, with step of -1 means reverse all order
print(arr[::-2])  # GECA, reverse with step of 2
```

---

## String Function

```py
# String function

print("\n--------Upper Case--------\n")
a = "Hello, World!"
print(a.upper())    # HELLO, WORLD!


print("\n--------Lower Case--------\n")
a = "Hello, World!"
print(a.lower())    # hello, world!


print("\n--------Remove Whitespace--------\n")
a = "    Hello, World!    "
print(a.strip())    # "Hello, World!"


print("\n--------Replace String--------\n")
a = "Hello, World!"
print(a.replace("H", "J"))  # Jello, World!


print("\n--------Split String--------\n")
a = "Hello, World!"
print(a.split(",")) # ['Hello', ' World!']

```

---

## String Concatenation

```py
# String Concatenation

print("\n--------+--------\n")
a = "Hello"
b = "World"
c = a + b
print(c)    # HelloWorld

age = 36
txt = "My name is John, I am"
print(txt,age)  # My name is John, I am 36
```

---

## String Format

### str.format() Method

- combine strings and numbers by using the `format()` method!

  - The `format()` method takes the passed **arguments**, formats them, and places them in the string where the placeholders `{}`.
  - The `format()` method takes **unlimited number of arguments**, and are placed into the respective placeholders

- **Index Numbers**

  - use index numbers `{0}` to be sure the arguments are placed in the correct placeholders

- **Named Indexes**
  - use named indexes by entering a name inside the curly brackets `{carname}`, but then must use names when you pass the parameter values `txt.format(carname = "Ford")`.

```py
# String Format

age = 36
txt = "My name is John, and I am {}"
print(txt.format(age))  # My name is John, and I am 36


quantity = 3
itemno = 567
price = 49.95
myorder = "I want {} pieces of item {} for {} dollars."
print(myorder.format(quantity, itemno, price))  # I want 3 pieces of item 567 for 49.95 dollars.


quantity = 3
itemno = 567
price = 49.95
myorder = "I want to pay {2} dollars for {0} pieces of item {1}."
print(myorder.format(quantity, itemno, price))  # I want to pay 49.95 dollars for 3 pieces of item 567.

myorder = "I have a {carname}, it is a {model}."
print(myorder.format(carname = "Ford", model = "Mustang"))
# I have a Ford, it is a Mustang.
```

---

### F-string Method

- prefix the string with the letter `F`, the string becomes the `f-string` itself.

  - The `f-string` can be formatted in much **same as** the `str.format()` method.
  - The F-string offers a convenient way to embed Python expression inside string literals for formatting.

- Speed

  - The reason for adapting this formatting style is its speed. The f-string evaluates at runtime rather than constant values. It embeds expression inside string literals, using minimal syntax. It is fast because it evaluates at runtime, not a constant value.

- Python expressions

  - can put all valid Python expressions in them. 大括号中可以是变量, 表达式, 函数, 对象

- Dictionary

  - There is a different quotation to use dictionary keys and f-string. 注意: 在引用字典键时, 使用引号需要和字符串的引号不同.

- Braces
  - To make appear braces in the code, you should use the double quotes as follows. 需要显示大括号时,需要双括号.
  - If we use the triple braces, it will display single braces in our string.
  - can display the more braces if we use more than triple braces.

```py

print("\n--------f-string--------\n")

print("\n--------variable--------")
val = 'Geeks'
# GeeksforGeeks is a portal for Geeks.
print(f"{val}for{val} is a portal for {val}.")
name = 'Tushar'
age = 23
# Hello, My name is Tushar and I'm 23 years old.
print(f"Hello, My name is {name} and I'm {age} years old.")


print("\n--------expressions--------")
print(f"{2 * 30}")  # 60


print("\n--------fuction--------")


def upercase(input):
    return input.upper()


name = "Sachin Tendulkar"
print(f"{upercase(name)} is great.")    # SACHIN TENDULKAR is great.


print("\n--------fuction--------")


class Actor:
    def __init__(self, first_name, last_name, movie):
        self.first_name = first_name
        self.last_name = last_name
        self.movie = movie

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s superhit movie is {self.movie}."

    def __repr__(self):
        return f"{self.first_name} {self.last_name}  {self.movie}. Superhi!"


ac = Actor('Keenu', 'Reevs', 'Matrix')
print(f"{ac}")  # Keenu Reevs's superhit movie is Matrix.


print("\n--------Dictionary--------")

detail = {"name": "John", "age": 19}
# John is 19 years old.
print(f"{detail['name']} is {detail['age']} years old.")


print("\n--------Braces--------")

print(f"{70 + 40}")         # 110
print(f"{{70 + 40}}")       # {70 + 40}
print(f"{{{70 + 40}}}")     # {110}
print(f"{{{{70 + 4}}}}")    # {{70 + 4}}
```

---

## Escape Character

An escape character is a backslash `\` followed by the character you want to insert.

| Code   | Result          |
| ------ | --------------- |
| `\'`   | Single Quote    |
| `\\`   | Backslash       |
| `\n`   | New Line        |
| `\r`   | Carriage Return |
| `\t`   | Tab             |
| `\b`   | Backspace       |
| `\f`   | Form Feed       |
| `\ooo` | Octal value     |
| `\xhh` | Hex value       |

```py
txt = "We are the so-called \"Vikings\" from the north."
print(txt)  # We are the so-called "Vikings" from the north.
```

---

## Prefix: `b""`, `r""`

- `b` prefix: the given string is in bytes’ format.

  ```py
  print(("abcdefg"))          # b'abcdefg'
  print(type("abcdefg"))      # <class 'str'>

  bprint((b"abcdefg"))         # b'abcdefg'
  print(type(b"abcdefg"))     # <class 'bytes'>
  ```

- `r` prefix: the string is to be treated as a raw string, which means all escape codes will be ignored.

  ```py
  print(r'\s') # \s
  print(type(r'\s')) # <class 'str'>
  ```

---

## String Methods

- Return a new string.
  - The original string remains.

| Method         | Description                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------- |
| `capitalize()` | Converts the first character to upper case                                                    |
| `casefold()`   | Converts string into lower case                                                               |
| `center()`     | Returns a centered string                                                                     |
| `count()`      | Returns the number of times a specified value occurs in a string                              |
| `encode()`     | Returns an encoded version of the string                                                      |
| `format_map()` | Formats specified values in a string                                                          |
| `ljust()`      | Returns a left justified version of the string                                                |
| `lower()`      | Converts a string into lower case                                                             |
| `lstrip()`     | Returns a left trim version of the string                                                     |
| `maketrans()`  | Returns a translation table to be used in translations                                        |
| `partition()`  | Returns a tuple where the string is parted into three parts                                   |
| `replace()`    | Returns a string where a specified value is replaced with a specified value                   |
| `rfind()`      | Searches the string for a specified value and returns the last position of where it was found |
| `rindex()`     | Searches the string for a specified value and returns the last position of where it was found |
| `rjust()`      | Returns a right justified version of the string                                               |
| `rpartition()` | Returns a tuple where the string is parted into three parts                                   |
| `rsplit()`     | Splits the string at the specified separator, and returns a list                              |
| `rstrip()`     | Returns a right trim version of the string                                                    |
| `split()`      | Splits the string at the specified separator, and returns a list                              |
| `splitlines()` | Splits the string at line breaks and returns a list                                           |
| `startswith()` | Returns true if the string starts with the specified value                                    |
| `strip()`      | Returns a trimmed version of the string                                                       |
| `swapcase()`   | Swaps cases, lower case becomes upper case and vice versa                                     |
| `title()`      | Converts the first character of each word to upper case                                       |
| `translate()`  | Returns a translated string                                                                   |
| `upper()`      | Converts a string into upper case                                                             |
| `zfill()`      | Fills the string with a specified number of 0 values at the beginning                         |

---

[TOP](#python---string)
