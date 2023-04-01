# Python RegEx

[Back](../index.md)

- [Python RegEx](#python-regex)
  - [RegEx Module](#regex-module)
  - [RegEx Functions](#regex-functions)
  - [Metacharacters](#metacharacters)
  - [Special Sequences](#special-sequences)
  - [Sets](#sets)
  - [The `findall()` Function](#the-findall-function)
  - [The search() Function](#the-search-function)
  - [The split() Function](#the-split-function)
  - [The sub() Function](#the-sub-function)
  - [Match Object](#match-object)

---

## RegEx Module

- A `RegEx`, or `Regular Expression`, is a sequence of characters that forms a search pattern.

  - `RegEx` can be used to check if a string contains the specified search pattern.

- `import re`

---

## RegEx Functions

| Function  | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| `findall` | Returns a list containing all matches                             |
| `search`  | Returns a Match object if there is a match anywhere in the string |
| `split`   | Returns a list where the string has been split at each match      |
| `sub`     | Replaces one or many matches with a string                        |

---

## Metacharacters

- `Metacharacters` are characters with a special meaning.

| Character | Description                                                                |                   |
| --------- | -------------------------------------------------------------------------- | ----------------- | ------- |
| `[]`      | A set of characters                                                        | `"[a-m]"`         |
| `\`       | Signals a special sequence (can also be used to escape special characters) | `"\d"`            |
| `.`       | Any character (except newline character)                                   | `"he..o"`         |
| `^`       | Starts with                                                                | `"^hello"`        |
| `$`       | Ends with                                                                  | `"planet$"`       |
| `*`       | Zero or more occurrences                                                   | `"he.*o"`         |
| `+`       | One or more occurrences                                                    | `"he.+o"`         |
| `?`       | Zero or one occurrences                                                    | `"he.?o"`         |
| `{}`      | Exactly the specified number of occurrences                                | `"he.{2}o"`       |
| `         | `                                                                          | Either or `"falls | stays"` |
| `()`      | Capture and group                                                          |

---

## Special Sequences

| Character | Description                                                                                                                              |                          |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `\A`      | Returns a match if the specified characters are at the beginning of the string                                                           | `"\AThe"`                |
| `\b`      | Returns a match where the specified characters are at the beginning or at the end of a word<br>                                          | `r"\bain"`<br>`r"ain\b"` |
|           | (the "r" in the beginning is making sure that the string is being treated as a "raw string")                                             |                          |
| `\B`      | Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word<br>                       | `r"\Bain"`<br>`r"ain\B"` |
|           | (the "r" in the beginning is making sure that the string is being treated as a "raw string")                                             |
| `\d`      | Returns a match where the string contains digits (numbers from 0-9)                                                                      | `"\d"`                   |
| `\D`      | Returns a match where the string DOES NOT contain digits                                                                                 | `"\D"`                   |
| `\s`      | Returns a match where the string contains a white space character                                                                        | `"\s"`                   |
| `\S`      | Returns a match where the string DOES NOT contain a white space character                                                                | `"\S"`                   |
| `\w`      | Returns a match where the string contains any word characters (characters from a to Z, digits from 0-9, and the underscore \_ character) | `"\w"`                   |
| `\W`      | Returns a match where the string DOES NOT contain any word characters                                                                    | `"\W"`                   |
| `\Z`      | Returns a match if the specified characters are at the end of the string                                                                 | `"Spain\Z"`              |

---

## Sets

- A `set` is a set of characters inside a pair of square brackets `[]` with a special meaning

| Set          | Description                                                                                                             |
| ------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `[arn]`      | Returns a match where one of the specified characters (a, r, or n) is present                                           |
| `[a-n]`      | Returns a match for any lower case character, alphabetically between a and n                                            |
| `[^arn]`     | Returns a match for any character EXCEPT a, r, and n                                                                    |
| `[0123]`     | Returns a match where any of the specified digits (0, 1, 2, or 3) are present                                           |
| `[0-9]`      | Returns a match for any digit between 0 and 9                                                                           |
| `[0-5][0-9]` | Returns a match for any two-digit numbers from 00 and 59                                                                |
| `[a-zA-Z]`   | Returns a match for any character alphabetically between a and z, lower case OR upper case                              |
| `[+]`        | In sets, +, \*, ., \| , (), $,{} has no special meaning, so [+] means: return a match for any + character in the string |

---

## The `findall()` Function

- The list contains the matches **in the order** they are found.

- If no matches are found, an **empty list** is returned

```py
print("\n--------findall()--------\n")

import re

txt = "The rain in Spain"
xregex = re.findall("ai", txt)
print(xregex)       # ['ai', 'ai']


yregex = re.findall("Portugal", txt)
print(yregex)       # []

```

---

## The search() Function

- The `search()` function searches the string for a match, and **returns a Match object** if there is a match.
  - If there is more than one match, only the **first occurrence** of the match will be returned.
  - If no matches are found, the value `None` is returned.

```py
import re
print("\n--------search()--------\n")

txt = "The rain in Spain"

xMatch = re.search("\s", txt)
print("start:\t", xMatch.start())       # 3
print("end:\t", xMatch.end())           # 4

yMatch = re.search("PP", txt)
# print(yMatch.start())       # AttributeError: 'NoneType' object has no attribute 'start'
print("No match:\t", yMatch)            # None

zMatch = re.search("ai", txt)
if zMatch != None:
    print("Matched:\t", zMatch.start())
else:
    print("Not matched:\t", zMatch)
```

---

## The split() Function

- `split()`: returns a list where the string has been split at each match.
- parameter
  - `maxsplit`: control the number of occurrences

```py
import re
print("\n--------split()--------\n")

txt = "The rain in Spain"
xspilt = re.split("\s", txt)
print(xspilt)           # ['The', 'rain', 'in', 'Spain']

yspilt = re.split("\s", txt, 1)
print(yspilt)           # ['The', 'rain in Spain']

```

---

## The sub() Function

- `sub()`: replaces the matches with the given text

- parameter
  - `count`: control the number of replacements

```py
import re
print("\n--------sub()--------\n")

txt = "The rain in Spain"
xSub = re.sub("\s", "--", txt)
print(xSub)         # The--rain--in--Spain

txt = "The rain in Spain"
ySub = re.sub("\s", "--", txt, 2)
print(ySub)         # The--rain--in Spain

txt = "The rain in Spain"
zSub = re.sub("-", "--", txt, 2)
print(zSub)         # The rain in Spain
```

---

## Match Object

- A `Match Object` is an object containing information about the search and the result.

  - Note: If there is no match, the value `None` will be returned, instead of the Match Object.

- The `Match object` has properties and methods used to retrieve information about the search, and the result.
  - `.span()`: returns a tuple containing the **start-**, and **end** positions of the match.
  - `.string`: returns the string passed into the function,返回 search 方法的文本参数
  - `.group()`: returns the part of the string where there was a match.返回匹配字符

```py

import re
print("\n--------Match Object.span()--------\n")


txt = "The rain in Spain"
xMatch = re.search(r"\bS\w+", txt)
print("span():\t\t", xMatch.span())         # span():          (12, 17)
print("start():\t", xMatch.start())         # start():         12
print("end():\t\t", xMatch.end())           # end():           17
print("group():\t", xMatch.group())         # group():         Spain

print("re:\t\t", xMatch.re)                 # re:              re.compile('\\bS\\w+')
print("string:\t\t", xMatch.string)         # string:          The rain in Spain

```

---

[Top](#python-regex)
