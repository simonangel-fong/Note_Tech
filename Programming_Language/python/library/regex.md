# Python - RegEx Library

[Back](../index.md)

- [Python - RegEx Library](#python---regex-library)
  - [`RegEx`](#regex)
  - [RegEx Functions](#regex-functions)
  - [Raw String Notation: `r"row_string"` Prefix](#raw-string-notation-rrow_string-prefix)
  - [Metacharacters](#metacharacters)
  - [Special Sequences](#special-sequences)
  - [Sets](#sets)
  - [Flags](#flags)
  - [Match Object](#match-object)

---

## `RegEx`

- `RegEx` / `Regular Expression`:

  - a set of characters with highly specialized syntax used to find or match other characters or groups of characters.

- `re` Module

  - Import
    - `import re`
  - Raise exception
    - `re.error`

- `metacharacters`

  - characters with a special meaning when utilized in a regular expression

- `Greedy repetitions`:
  - cause the matching algorithm to attempt to replicate the `RE` **as many times as** feasible. If later elements of the sequence fail to match, the matching algorithm will retry with lesser repetitions.

---

## RegEx Functions

| Function  | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| `findall` | Returns a list containing all matches                             |
| `search`  | Returns a Match object if there is a match anywhere in the string |
| `split`   | Returns a list where the string has been split at each match      |
| `sub`     | Replaces one or many matches with a string                        |

---

## Raw String Notation: `r"row_string"` Prefix

- How to match a literal backslash and special escape sequences in **Python string literals** is a problem

- The solution is to use Python’s **raw string notation** for regular expressions, in which backslashes are not handled in any special way in a string literal prefixed with `r`.

- Example:

  | Regular String  | Raw string     |
  | --------------- | -------------- |
  | `"ab\*"`        | `r"ab\*"`      |
  | `"\\\\section"` | `r"\\section"` |
  | `"\\w+\\s+\\1"` | `r"\w+\s+\1"`  |

- The `r` prefix, **making the literal a raw string literal**.

---

## Metacharacters

- `Metacharacters` are characters with a special meaning.

| Character | Description                                                                |                              |
| --------- | -------------------------------------------------------------------------- | ---------------------------- | ------- |
| `^`       | **Caret** - Starts with                                                    | `"^hello"`                   |
| `$`       | **Dolla** - Ends with                                                      | `"planet$"`                  |
| `.`       | **Dot** - Any character (except newline character)                         | `"he..o"`                    |
| `[]`      | **Bracket** - the set of characters                                        | `"[a-m]"`                    |
| `?`       | **Question mark** - Zero or one occurrences                                | `"he.?o"`                    |
| `+`       | **Plus** - One or more occurrences                                         | `"he.+o"`                    |
| `*`       | **Asterisk** - Zero or more occurrences                                    | `"he.*o"`                    |
| `{}`      | **Curly Braces** - Exactly the specified number of occurrences             | `"he.{2}o"`                  |
| `\`       | Signals a special sequence (can also be used to escape special characters) | `"\d"`                       |
| `         | `                                                                          | **Pipe** - Either or `"falls | stays"` |
| `()`      | Capture and group                                                          |

---

## Special Sequences

| Character | Matches                                                            |                          |
| --------- | ------------------------------------------------------------------ | ------------------------ |
| `\d`      | any digit character == `[0-9]`                                     | `"\d"`                   |
| `\D`      | non-digit character == `[^0-9]`                                    | `"\D"`                   |
| `\s`      | any white space character                                          | `"\s"`                   |
| `\S`      | any character except the white space character                     | `"\S"`                   |
| `\w`      | any alphanumeric character == `[a-zA-Z0-9]`                        | `"\w"`                   |
| `\W`      | any characters except the alphanumeric character == `[^a-zA-Z0-9]` | `"\W"`                   |
| `\A`      | the defined pattern at the start of the string                     | `"\AThe"`                |
| `\b`      | the pattern at the beginning or at the end of a word               | `r"\bain"` / `r"ain\b"`  |
| `\B`      | the opposite of \b.                                                | `r"\Bain"`<br>`r"ain\B"` |
| `\Z`      | the pattern is at the end of the string                            | `"Spain\Z"`              |

---

## Sets

- A `set` is a set of characters inside a pair of square brackets `[]` with a special meaning

| Set          | Match                                                                  |
| ------------ | ---------------------------------------------------------------------- |
| `[arn]`      | any of the specified characters (a, r, or n)                           |
| `[a-n]`      | alphabetically between a and n                                         |
| `[^arn]`     | any character EXCEPT a, r, and n                                       |
| `[0123]`     | any of the specified digits (0, 1, 2, or 3) are present                |
| `[0-9]`      | any digit between 0 and 9                                              |
| `[0-5][0-9]` | any two-digit numbers from 00 and 59                                   |
| `[a-zA-Z]`   | any character alphabetically between a and z, lower case OR upper case |
| `[+]`        | any `+` character in the string                                        |

---

## Flags

| Set                     | Match                     |
| ----------------------- | ------------------------- |
| `re.A`/ `re.ASCII`      | ASCII-only matching       |
| `re.I`/ `re.IGNORECASE` | case-insensitive matching |
| `re.M`/ `re.MULTILINE`  | each newline matching     |

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

[Top](#python---regex-library)
