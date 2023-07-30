# Python - Regex Function

[Back](../index.md)

- [Python - Regex Function](#python---regex-function)
  - [Constructor](#constructor)
    - [`re.compile(pattern, flags=0)`](#recompilepattern-flags0)
  - [Search](#search)
    - [`re.match(pattern, string, flags=0)`](#rematchpattern-string-flags0)
    - [`re.fullmatch(pattern, string, flags=0)`](#refullmatchpattern-string-flags0)
    - [`re.search(pattern, string, flags=0)`: Return 1st](#researchpattern-string-flags0-return-1st)
  - [Replace](#replace)
    - [`re.sub(pattern, repl, string, count=0, flags=0)`](#resubpattern-repl-string-count0-flags0)
    - [`re.subn(pattern, repl, string, count=0, flags=0)`](#resubnpattern-repl-string-count0-flags0)
  - [Other](#other)
    - [`re.escape(pattern)`](#reescapepattern)
    - [`re.purge()`](#repurge)
  - [To List](#to-list)
    - [`re.findall(pattern, string, flags=0)`](#refindallpattern-string-flags0)
    - [`re.split(pattern, string, maxsplit=0, flags=0)`](#resplitpattern-string-maxsplit0-flags0)
    - [`re.finditer(pattern, string, flags=0)`](#refinditerpattern-string-flags0)

---

## Constructor

### `re.compile(pattern, flags=0)`

- create a regular expression object used to match patterns in a string.

```py
import re  # Importing re module
print("\n-------- re.compile(pattern, flags=0) --------\n")


# Defining regEx patterns
pattern = "amazing"
regex_object = re.compile(pattern)  # Createing a regEx object
text = "This tutorial is amazing!"   # String

# Searching for the pattern in the string
match_object = regex_object.search(text)
# Match Object: <re.Match object; span=(17, 24), match='amazing'>
print("Match Object:", match_object)
```

---

## Search

### `re.match(pattern, string, flags=0)`

- mateches the pattern **from the beginning** of the string.

- Parameters

  - `pattern`: the regular expression to be matched
  - `string`: the string compared to the pattern at the start of the string.
  - `flags`: Bitwise `OR` (`|`) can be used to express multiple flags

- Return
  - Returns a `match object` if any match is found with information like start, end, span, etc.
  - Returns a `None` value in the case no match is found

```py
import re  # Importing re module
print("\n-------- re.match(pattern, string, flags=0) --------\n")

print(re.match(r".?o", "dog"))  # <re.Match object; span=(0, 2), match='do'>
print(re.match("d", "dog"))     # <re.Match object; span=(0, 1), match='d'>
print(re.match("o", "dog"))     # None match='o'>

```

---

### `re.fullmatch(pattern, string, flags=0)`

- matches the whole string with the pattern.

- Parameters

  - `pattern`: the regular expression to be matched.
  - `string`: The string to be searched for the pattern wherever within it.
  - `flags`: Bitwise `OR` (`|`) can be used to express multiple flags.

- Returns
  - a corresponding match object.
  - `None` if no match is found.

```py
import re  # Importing re module
print("\n-------- re.fullmatch(pattern, string, flags=0) --------\n")

# Sample string
line = "Hello world"

# Using re.fullmatch()
print(re.fullmatch("Hello", line))      # None
print(re.fullmatch("Hello world", line))    # <re.Match object; span=(0, 11), match='Hello world'>
```

---

### `re.search(pattern, string, flags=0)`: Return 1st

- look for the **first occurrence** of a regular expression sequence and deliver it.
- It will verify all rows of the supplied string, unlike Python's re.match().

- Parameters

  - `pattern`: the regular expression to be matched.
  - `string`: The string to be searched for the pattern wherever within it.
  - `flags`: Bitwise `OR` (`|`) can be used to express multiple flags.

- Return:
  - If there is more than one match, only the **first occurrence** of the match will be returned.
  - If no matches are found, the value `None` is returned.

```py
import re  # Importing re module
print("\n-------- re.search(pattern, string, flags=0) --------\n")

print(re.search(r".?o", "dog"))  # <re.Match object; span=(0, 2), match='do'>
print(re.search("d", "dog"))     # <re.Match object; span=(0, 1), match='d'>
print(re.search("o", "dog"))     # <re.Match object; span=(1, 2), match='o'>
```

---

## Replace

### `re.sub(pattern, repl, string, count=0, flags=0)`

- substitutes the matching pattern with the new string

- Parameter:

  - `Pattern`: a regex pattern to be matched
  - `repl`: the "replacement" which replaces the pattern in string.
  - `Count`: control the number of substitutions

- Return:
  - the replaced string

```py
import re  # Importing re module
print("\n-------- re.sub(pattern, repl, string, count=0, flags=0) --------\n")

print(re.sub("\s", "9", "The rain in Spain"))
# The9rain9in9Spain

print(re.sub("\s", "9", "The rain in Spain", 2))
# The9rain9in Spain
```

---

### `re.subn(pattern, repl, string, count=0, flags=0)`

- Working of subn if same as sub-function
- It returns a tuple

```py
import re  # Importing re module
print("\n-------- re.subn(pattern, repl, string, count=0, flags=0) --------\n")

print(re.subn("\s", "9", "The rain in Spain"))
# ('The9rain9in9Spain', 3)

print(re.subn("\s", "9", "The rain in Spain", 2))
# ('The9rain9in Spain', 2)
```

---

## Other

### `re.escape(pattern)`

- escapes the special character in the pattern.
- The esacpe function become more important when the string contains regular expression metacharacters in it.

```py
import re  # Importing re module
print("\n-------- re.escape(pattern) --------\n")

print(re.escape('https://www.javatpoint.com/'))     # https://www\.javatpoint\.com/
```

---

### `re.purge()`

- clears the regular expression cache.

```py
import re  # Importing re module
print("\n-------- re.purge() --------\n")

# Define some regular expressions
pattern1 = r'\d+'
pattern2 = r'[a-z]+'

# Use the regular expressions
# <re.Match object; span=(0, 3), match='123'>
print(re.search(pattern1, '123abc'))
# <re.Match object; span=(3, 6), match='abc'>
print(re.search(pattern2, '123abc'))

# Clear the regular expression cache
re.purge()

# Use the regular expressions again
# <re.Match object; span=(0, 3), match='456'>
print(re.search(pattern1, '456def'))
# <re.Match object; span=(3, 6), match='def'>
print(re.search(pattern2, '456def'))
```

---

## To List

### `re.findall(pattern, string, flags=0)`

- Return all non-overlapping matches of pattern in string, as a list of strings or tuples.

```py

print(re.findall(r'',"which foot or hand fell fastest"))
# ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
print(re.findall(r'o',"which foot or hand fell fastest"))
# ['o', 'o', 'o']

print(re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest'))
# ['foot', 'fell', 'fastest']

print(re.findall(r'(\w+)=(\d+)', 'set width=20 and height=10'))
# [('width', '20'), ('height', '10')]
```

---

### `re.split(pattern, string, maxsplit=0, flags=0)`

- splits the pattern by the occurrences of patterns.
- If maxsplit is zero, then the maximum number of splits occurs.
- If maxsplit is one, then it splits the string by the first occurrence of the pattern and returns the remaining string as a final result.

```py
import re  # Importing re module
print("\n-------- re.split(pattern, string, maxsplit=0, flags=0) --------\n")

print(re.split("\s", "The rain in Spain"))
# ['The', 'rain', 'in', 'Spain']

print(re.split("\s", "The rain in Spain", maxsplit=1))
# ['The', 'rain in Spain']

print(re.split("\s", "The rain in Spain", maxsplit=2))
# ['The', 'rain', 'in Spain']

print(re.split("\s", "The rain in Spain", maxsplit=3))
# ['The', 'rain', 'in', 'Spain']

print(re.split("\s", "The rain in Spain", maxsplit=4))
# ['The', 'rain', 'in', 'Spain']
```

---

### `re.finditer(pattern, string, flags=0)`

- Returns an iterator that yields all **non-overlapping matches** of pattern in a string.
- String is scanned from left to right.

- Parameters

  - `pattern`: the regular expression to be matched.
  - `string`: The string to be searched for the pattern wherever within it.
  - `flags`: Bitwise `OR` (`|`) can be used to express multiple flags.

- Returns
  - a corresponding match object.
  - `None` if no match is found.

```py
import re  # Importing re module
print("\n-------- re.finditer(pattern, string, flags=0) --------\n")

# Using re.finditer()
iter_ = re.finditer(r'[aeiou]', "Hello world. I am Here!")

# Iterating the itre_
for i in iter_:
    print(i)

# <re.Match object; span=(1, 2), match='e'>
# <re.Match object; span=(4, 5), match='o'>
# <re.Match object; span=(7, 8), match='o'>
# <re.Match object; span=(15, 16), match='a'>
# <re.Match object; span=(19, 20), match='e'>
# <re.Match object; span=(21, 22), match='e'>
```

---

[TOP](#python---regex-function)
