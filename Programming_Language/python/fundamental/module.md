# Python - Modules

[Back](../index.md)

- [Python - Modules](#python---modules)
  - [Module](#module)
    - [Example](#example)
  - [Built-in Modules](#built-in-modules)
  - [`dir()` Function](#dir-function)
  - [Python Built-in Library](#python-built-in-library)
  - [Run a .py File](#run-a-py-file)

---

## Module

- `module`: A document with definitions of functions and various statements written in Python

  - Every python file is a module.
  - A module can define `functions`, `classes`, and `variables`.
  - A module can also include **runnable code**.
  - A module can be imported from another python file.

- **Create a Module**

  - Create a module(file) with the file extension `.py`.

- Syntax

  - Import Module

    - `import module_name`

  - Re-name Module

    - `import module_name as alias`

  - Import Function & Variable

    - `from module_name import function_name`
    - `from module_name import variable_name`

---

### Example

- module_person.py

  ```py
  def greeting(name):
      print("Hello, " + name)
      print(person1)


  person1 = {
      "name": "John",
      "age": 36,
      "country": "Norway"
  }

  ```

- module_demo.py

  - 1. Import Module

  ```py
  print("\n--------Import a Module--------\n")
  import module_person

  # call the members of the imported module
  module_person.greeting("John")  # function
  person = module_person.person1  # Variables
  print(person)
  # Hello, John
  # {'name': 'John', 'age': 36, 'country': 'Norway'}
  # {'name': 'John', 'age': 36, 'country': 'Norway'}
  ```

  - 2. Re-name Module

  ```py
  print("\n--------Re-naming a Module--------\n")
  import module_person as p   # rename imported module

  p.greeting("John")
  person = p.person1
  print(person)
  # Hello, John
  # {'name': 'John', 'age': 36, 'country': 'Norway'}
  # {'name': 'John', 'age': 36, 'country': 'Norway'}
  ```

  - 3. Import Function & Variable

  ```py
  print("\n--------Import a Function--------\n")
  from module_person import greeting

  greeting("John")
  # Hello, John
  # {'name': 'John', 'age': 36, 'country': 'Norway'}


  print("\n--------Import a Variable--------\n")
  from module_person import person1

  person = person1
  print(person)

  ```

---

## Built-in Modules

```py
import platform

x = platform.system()
print(x)  # Windows
```

---

## `dir()` Function

- `dir()`: list all the function names (or variable names) in a module.
  - parameter: the name of imported module

```py
import platform

x = dir(platform)
print(x)
```

---

## Python Built-in Library

| Library name | Description                   |
| ------------ | ----------------------------- |
| `math`       | math utilities                |
| `re`         | regular expressions           |
| `json`       | JSON                          |
| `datetime`   | date and time                 |
| `sqlite3`    | use SQLite                    |
| `os`         | os utilities                  |
| `random`     | random number generation      |
| `statistics` | statistics generation         |
| `requests`   | perform HTTP network requests |
| `http`       | to create HTTP servers        |
| `urllib`     | to manage urlsservers         |

---

## Run a .py File

- Command Line:

```shell
# target file: main.py
python main.py
```

- Pass arguments from command line

  - py file:
    - imort sys
    - using `sys.argv` to accept arguments
  - CLI: `python file_name.py [arguement]`

```shell
py Programming_Language\python\lab.py john 16
```

```py
import sys

print(sys.argv[1:])   # ['john', '16']
```

---

[TOP](#python---modules)
