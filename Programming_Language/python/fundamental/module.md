# Python - Modules & Package

[Back](../index.md)

- [Python - Modules \& Package](#python---modules--package)
  - [Module](#module)
    - [Example](#example)
    - [Built-in Modules](#built-in-modules)
    - [Module Attributes](#module-attributes)
    - [`dir()` Function](#dir-function)
    - [Python Built-in Module](#python-built-in-module)
    - [Run a `.py` File](#run-a-py-file)
    - [`if __name__ == __main__:`](#if-__name__--__main__)
  - [Package](#package)
    - [Pip](#pip)

---

- Cheapsheet: Hierarchy
  - Framework > Library(packages) > Package(directory) > Module(file)

---

## Module

- `module`: A **document** with definitions of functions and various statements written in Python

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

### Built-in Modules

```py
import platform

x = platform.system()
print(x)  # Windows
```

---

### Module Attributes

- `Module Attributes`:
  - the attributes to describe module

```py
[print(idf, ":",  eval(idf)) for idf in dir()]
# __annotations__ : {}
# __builtins__ : <module 'builtins' (built-in)>
# __cached__ : None
# __doc__ : None
# __file__ : c:\Users\simon\Documents\IIS\Tech_Notes\Programming_Language\python\trial.py
# __loader__ : <_frozen_importlib_external.SourceFileLoader object at 0x0000028A498E6CD0>
# __name__ : __main__
# __package__ : None
# __spec__ : None
```

---

### `dir()` Function

- `dir()`: list all the function names (or variable names) in a module.
  - parameter: the name of imported module

```py
import platform

x = dir(platform)
print(x)
```

---

### Python Built-in Module

| Module       | Description                   |
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

### Run a `.py` File

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

### `if __name__ == __main__:`

- Unlike other languages, Python has no `main()` function that gets run automatically. The `main()` function is **implicitly** all the code **at the top level**.

- the top-level code is an if block. To identify whether a `.py` file is original or a imported file:

```py
if __name__ == "__main__":
```

- `__name__` is a built-in variable which evaluate to **the name of the current module**.
  - If a module is being run directly, then `__name__` instead is set to the string `"__main__"`.
  - If a modules function is being used as an import, the `__name__` is name of the imported module, not `"__main__"`.

---

## Package

A module is basically You may choose to define functions, classes, or variables in a module.

- `module`: a simple <u>Python script</u> with a `.py` extension file that defines functions, classes, or variables .

- `package`: a **directory** of a collection of `modules`.

  - Packages allow the hierarchical structure of the module namespace.
  - directory also contains an `__init__.py` file by which the interpreter interprets it as a package.
    - `__init__.py` Python File works as a Constructor for the Python Package.

- `library`: a **reusable** chunk of code.

  - it is often assumed that while a `package` is a collection of `modules`, a `library` is a collection of `packages`.

- `Python frameworks`: a collection of `modules` and `packages` that help programmers to fast track the development process.
  - However, frameworks are usually more complex than libraries.

---

### Pip

- `pip`: The standard package manager for Python

- Download pip: https://pypi.org/project/pip/

- Find pacakge: https://pypi.org/

- import a Package: `import <package>`

- Pip Commands

| Command                           | Description                                        |
| --------------------------------- | -------------------------------------------------- |
| `pip --version`                   | check the pip version                              |
| `pip list`                        | List installed packages                            |
| `pip show <package>`              | Show information about a package                   |
| `pip install <package>`           | downloaded and installed package                   |
| `pip install <package>==1.0.4`    | installed specific version                         |
| `pip install --upgrade <package>` | Upgrade package                                    |
| `pip uninstall <package>`         | Uninstall a package.                               |
| `pip install -r requirements.txt` | Install a list of requirements specified in a file |
| `pip freeze`                      | Generate output suitable for a requirements file   |
| `pip freeze > requirements.txt`   | Generate a txt requirements file                   |

---

[TOP](#python---modules)
