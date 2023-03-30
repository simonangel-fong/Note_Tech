# Python Modules

[Back](../index.md)

- [Python Modules](#python-modules)
  - [Module](#module)
    - [Example](#example)
  - [Built-in Modules](#built-in-modules)
  - [`dir()` Function](#dir-function)

---

## Module

- `module`: a file containing Python **definitions and statements**

  - A module can define `functions`, `classes`, and `variables`.
  - A module can also include **runnable code**.

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

[TOP](#python-modules)
