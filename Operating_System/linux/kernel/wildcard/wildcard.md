# Linux - Wildcard

[Back](../../index.md)

---

- [Linux - Wildcard](#linux---wildcard)
  - [Wildcard](#wildcard)

---

## Wildcard

| Wildcard        | Desc                                                            |
| --------------- | --------------------------------------------------------------- |
| `*`             | Matches zero or more characters                                 |
| `?`             | Matches exactly one characters                                  |
| `[aeiou]`       | Character class, matches **exactly one** of included characters |
| `[!aeiou]`      | Exclude **exactly one** of characters                           |
| `[a-g]`,`[3-6]` | Range                                                           |
| `\?`,`\*`       | Escape character, match a wildcard character.                   |

- Named Character Classes

  - `[[:alpha:]]`: Matches alphabetic characters
  - `[[:lower:]]`: Matches lower-case letters
  - `[[:upper:]]`: Matches upper-case letters
  - `[[:digit:]]`: Matches any one digit 0-9
  - `[[:alnum:]]`: Matches all alphanumeric characters
  - `[[:space:]]`: Matches white space
  - `[[:blank:]]`: Matches blank characters, such as space and tab
  - `[[:cntrl:]]`: Matches control characters
  - `[[:graph:]]`: Matches graphical characters
  - `[[:print:]]`: Matches printable characters
  - `[[:punct:]]`: Matches punctuation characters

---

- Example

```sh
ll c[aeiou]t
ll [a-d]*
cp *[[:digit:]] /tmp

rm ??
```
