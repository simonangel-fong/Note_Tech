# Python Syntax

[Back](../index.md)

- [Python Syntax](#python-syntax)
  - [Syntax](#syntax)
  - [Indentation 缩进](#indentation-缩进)

---

## Syntax

- Python syntax can be **executed** by writing directly in the Command Line or in a python file

- `Expression`: the code that returns a value.

  - Example: `1+1`

- `Statement`: the operation on a value.
  - Example: `a=1`
  - a program is formed by a series of statements
  - can put statements in one line using semicolon
    - Example: `a=1;print(a)`

## Indentation 缩进

- `Indentation`: <u>the spaces</u> **at the beginning** of a code line.

- Python uses `indentation` to **indicate a block of code**.

  - Python will give you an **error** if you **skip** the indentation.

  ```py
  if 5 > 2:
  print("Five is greater than two!") #error
  ```

  - The number of spaces is up to you as a programmer, the most common use is **four**, but it has to be at least one.

  ```py
  if 5 > 2:
   print("Five is greater than two!") # one space
  if 5 > 2:
          print("Five is greater than two!") # eight spaces
  ```

- You have to use the **same number** of spaces in the **same block of code**, otherwise Python will give you an error.

```py
if 5 > 2:
 print("Five is greater than two!")
        print("Five is greater than two!")  #error, should use same number of spaces in the same block
```

---

[TOP](#python-syntax)
