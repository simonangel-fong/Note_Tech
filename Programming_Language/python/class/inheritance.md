# Python - Inheritance

[Back](../index.md)

- [Python - Inheritance](#python---inheritance)
  - [Inheritance](#inheritance)
  - [Method](#method)
  - [Example: Inheritance](#example-inheritance)

---

## Inheritance

- `Inheritance` allows us to define a class that inherits all **the methods and properties** from another class.

  - `Parent class`: the class being inherited from, also called `base class`.

  - `Child class`: the class that inherits from another class, also called `derived class`.

---

## Method

- `__init__()`

  - the child class will no longer inherit the parent's `__init__()` function
  - The child's `__init__()` function **overrides** the inheritance of the parent's `__init__()` function.

- `super()`
  - reference the parent class to access the parent class’s methods and properties.
  - `super()` function returns an object that represents the parent class.

---

## Example: Inheritance

```py
print("\n--------Class: Inheritance--------\n")


class Person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def __str__(self):
        return f'{self.fname} {self.lname}'

    def printName(self):
        print(f"Name: {self.fname} {self.lname}")


# inherit Person Class


class Student(Person):
    def __init__(self, fname, lname, id):
        super().__init__(fname, lname)
        self.id = id

    def __str__(self):
        return f"{super().__str__()} - {self.id}"

    def printID(self):
        print(f'ID: {self.id}')


std = Student("John", "Wick", "001")

print(std)                  # John Wick - 001
std.printName()             # Name: John Wick
std.printID()               # ID: 001

```

---

[TOP](#python---inheritance)
