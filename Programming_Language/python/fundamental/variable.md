# Python Variable

[Back](../index.md)

- [Python Variable](#python-variable)
  - [Variable](#variable)
  - [Creating Variables](#creating-variables)
    - [Declare multiple variables in one line](#declare-multiple-variables-in-one-line)
    - [Unpack a Collection](#unpack-a-collection)
  - [Variable Names](#variable-names)
  - [Scope](#scope)
    - [Output Variables](#output-variables)
    - [Global Variables](#global-variables)

---

## Variable

- `Variables`: **containers** for storing data values.

---

## Creating Variables

- Python has **no command for declaring** a variable.

- A variable is **created** the moment you **first assign** a value to it.

- Variables do **not need** to be declared with any particular **type**, and can even **change type** after they have been set.

```py
x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)
```

### Declare multiple variables in one line

- Python allows you to assign values to **multiple variables** <u>in one line</u>.
  - Note: Make sure the number of variables matches the number of values, or else you will get an error.

```py
x, y, z = "Orange", "Banana", "Cherry"
print(x)    # Orange
print(y)    # Banana
print(z)    # Cherry

```

- And you can assign the same value to **multiple variables** <u>in one line</u>.

```py
x = y = z = "Orange"
print(x)    # Orange
print(y)    # Orange
print(z)    # Orange

```

### Unpack a Collection

- `unpacking`: to extract the values in a collection, such as list, tuple etc, into variables.

```py
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)    # apple
print(y)    # banana
print(z)    # cherry

```

---

## Variable Names

- A variable can have a **short name** (like x and y) or a more **descriptive name** (age, carname, total\*volume).

- Rules for Python variables:

  - A variable name must **start with** a <u>letter</u> or the <u>underscore character</u>
  - A variable name **cannot start with a number**
  - A variable name can only contain **alpha-numeric characters** and **underscores** (A-z, 0-9, and \_ )
  - Variable names are **case-sensitive** (age, Age and AGE are three different variables)
  - A variable name cannot be any of the Python **keywords**.

- `Camel Case`: Each word, except the first, starts with a capital letter.

- `Pascal Case`: Each word starts with a capital letter.

- `Snake Case`: Each word is separated by an underscore character.

```py
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

# illegal variable name
# 2myvar = "John"
# my-var = "John"
# my var = "John"

# Camel Case
myVariableName = "John"
# Pascal Case
MyVariableName = "John"
# Snake Case
my_variable_name = "John"
```

---

## Scope

### Output Variables

- The Python `print()` function is often used to output variables.

  - output multiple variables, separated by a comma.
  - use the `+` operator to output multiple variables

- The best way to output multiple variables in the print() function is to separate them with **commas**, which even **support different data types**.

```py
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)  # Python is awesome
print(x + y + z)    # Pythonisawesome

x = 5
y = 10
print(x + y)    # 15

x = 5
y = "John"
print(x + y)    #error: combine a string and a number with the + operator, Python will give you an error.
print(x, y)     #5 John
```

---

### Global Variables

- `global variables`: Variables that are created **outside of a function**.

- `local variables`: variables only used **within a function**.

- The global variable with the same name will remain as it was, global and with the original value.

```py
x = "awesome"   # global variable

def myfunc():
  x = "fantastic"   # local variable
  print("Python is " + x)   # Python is fantastic

myfunc()

print("Python is " + x)     # Python is awesome

```

- `global` Keyword

  - To **create** a `global` variable inside a function
  - to **change** a `global` variable inside a function.

```py

# create a global variable
def myfunc():
  global x  # declare x inside myfunc() as a global variable
  x = "fantastic"

myfunc()

print("Python is " + x) # Python is fantastic

# change a global variable
x = "awesome"

def myfunc():
  global x  # declare x inside myfunc() as a global variable
  x = "fantastic"

myfunc()

print("Python is " + x)  # Python is fantastic


```

---

[TOP](#python-variable)
