# Python String

[Back](./index.md)

- [Python String](#python-string)
  - [Strings](#strings)
  - [Strings are Arrays](#strings-are-arrays)
  - [String Length: `len()`](#string-length-len)
  - [String Check: `in`](#string-check-in)
  - [String Slicing](#string-slicing)
  - [String Function](#string-function)
  - [String Concatenation](#string-concatenation)
  - [String Format](#string-format)
  - [Escape Character](#escape-character)
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

- combine strings and numbers by using the `format()` method!

  - The `format()` method takes the passed **arguments**, formats them, and places them in the string where the placeholders `{}`.
  - The `format()` method takes **unlimited number of arguments**, and are placed into the respective placeholders
  - use index numbers `{0}` to be sure the arguments are placed in the correct placeholders

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

## String Methods

| Method           | Description                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------- |
| `encode()`       | Returns an encoded version of the string                                                      |
| `format_map()`   | Formats specified values in a string                                                          |
| `istitle()`      | Returns True if the string follows the rules of a title                                       |
| `isupper()`      | Returns True if all characters in the string are upper case                                   |
| `join()`         | Joins the elements of an iterable to the end of the string                                    |
| `ljust()`        | Returns a left justified version of the string                                                |
| `lower()`        | Converts a string into lower case                                                             |
| `lstrip()`       | Returns a left trim version of the string                                                     |
| `maketrans()`    | Returns a translation table to be used in translations                                        |
| `partition()`    | Returns a tuple where the string is parted into three parts                                   |
| `replace()`      | Returns a string where a specified value is replaced with a specified value                   |
| `rfind()`        | Searches the string for a specified value and returns the last position of where it was found |
| `rindex()`       | Searches the string for a specified value and returns the last position of where it was found |
| `rjust()`        | Returns a right justified version of the string                                               |
| `rpartition()`   | Returns a tuple where the string is parted into three parts                                   |
| `rsplit()`       | Splits the string at the specified separator, and returns a list                              |
| `rstrip()`       | Returns a right trim version of the string                                                    |
| `split()`        | Splits the string at the specified separator, and returns a list                              |
| `splitlines()`   | Splits the string at line breaks and returns a list                                           |
| `startswith()`   | Returns true if the string starts with the specified value                                    |
| `strip()`        | Returns a trimmed version of the string                                                       |
| `swapcase()`     | Swaps cases, lower case becomes upper case and vice versa                                     |
| `title()`        | Converts the first character of each word to upper case                                       |
| `translate()`    | Returns a translated string                                                                   |
| `upper()`        | Converts a string into upper case                                                             |
| `zfill()`        | Fills the string with a specified number of 0 values at the beginning                         |

---

[TOP](#python-string)
