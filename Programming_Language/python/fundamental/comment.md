# Python Comment

[back](../index.md)

- [Python Comment](#python-comment)
  - [Comments](#comments)
  - [Creating a Comment](#creating-a-comment)
  - [Multiline Comments](#multiline-comments)
  - [Docstring](#docstring)

---

## Comments

- Comments can be used to **explain** Python code.

- Comments can be used to make the code more **readable**.

- Comments can be used to **prevent execution** when testing code.

---

## Creating a Comment

- Comments starts with a **hash mark** `#`, and Python will ignore them.

- Comments can be placed at the **end of a line**, and Python will ignore the rest of the line

```py
#This is a comment
print("Hello, World!")

print("Hello, World!") #This is a comment
```

---

## Multiline Comments

- insert a `#` for each line

- use a multiline string, since Python will ignore string literals that are not assigned to a variable
  - As long as the string is not assigned to a variable, Python will read the code, but then ignore it, and you have made a multiline comment.

```py
#This is a comment
#written in
#more than just one line
print("Hello, World!")

"""
This is a comment
written in
more than just one line
"""
print("Hello, World!")


```

---

## Docstring

- `Python docstring`:
  - The strings enclosed in triple quotes that come immediately after the defined function
  - It's designed to link documentation developed for Python modules, methods, classes, and functions together.
- It's placed just beneath the function, module, or class **to explain what they perform**.
- The docstring is then readily accessible in Python using the `__doc__` attribute.

```py
print("\n--------Docstring: function--------\n")


def add(x, y):
    """This function adds the values of x and y"""
    return x + y


# Displaying the docstring of the add function
print(add.__doc__)      # This function adds the values of x and y
print(help(add))
# Help on function add in module __main__:
# add(x, y)
#     This function adds the values of x and y
# None

print("\n--------Docstring: object--------\n")


class Dog:
    '''A class representing a dog'''

    def __init__(self, name, age):
        """Initialize a new dog"""
        self.name = name
        self.age = age

    def bark(self):
        """Let the dog bark"""
        print("wooof!!")


print(help(Dog))
# Help on class Dog in module __main__:

# class Dog(builtins.object)
#  |  Dog(name, age)
#  |
#  |  A class representing a dog
#  |
#  |  Methods defined here:
#  |
#  |  __init__(self, name, age)
#  |      Initialize a new dog
#  |
#  |  bark(self)
#  |      Let the dog bark
#  |
#  |  ----------------------------------------------------------------------
#  |  Data descriptors defined here:
#  |
#  |  __dict__
#  |      dictionary for instance variables (if defined)
#  |
#  |  __weakref__
#  |      list of weak references to the object (if defined)

# None

```

---

[TOP](#python-comment)
