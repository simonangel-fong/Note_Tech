# Python Functions

[Back](../index.md)

- [Python Functions](#python-functions)
- [Function](#function)
  - [Parameters / Arguments](#parameters--arguments)
  - [Arbitrary Arguments, `*args`](#arbitrary-arguments-args)
  - [Keyword Arguments](#keyword-arguments)
  - [Arbitrary Keyword Arguments, `**kwargs`](#arbitrary-keyword-arguments-kwargs)
  - [Recursion](#recursion)

---

# Function

- A function is a block of code which **only runs when it is called**.

  - can pass data, known as **parameters**, into a function.

  - A function can **return** data as a result.

- **Create a function**

  - using the `def` keyword

- **Calling a Function**

  - use the function name followed by **parenthesis**

---

## Parameters / Arguments

- A `parameter` is the variable listed inside the parentheses **in the function definition**.

- An `argument` is the value that is sent to the function **when it is called**.

- `Arguments` are often shortened to `args` in Python documentations.

- **Number of Arguments**

  | # Passing Arguments      | Outcome                                                                                    |
  | ------------------------ | ------------------------------------------------------------------------------------------ |
  | `<` # Defined Parameters | TypeError: `function_name()` missing `num` required positional argument: `parameter_names` |
  | `>` # Defined Parameters | TypeError: `function_name()` takes `num` positional argument but `over_num` were give      |

- Python 中本**没有重载函数**，如果我们在同一命名空间中定义的多个函数是同名的，**最后一个**将覆盖前面的各函数，也就是函数的名称只能是唯一的。

  ```py
  # overloading
  def printName():
      print("good")


  def printName(name):
      print(name)


  printName()    # TypeError: printName() missing 1 required positional argument: 'name'

  ```

- **Default Parameter Value**

  ```py
  print("\n--------Default Value--------\n")


  def printName(name="John"):
      print(name)


  printName()  # John
  printName("Carl")  # Carl

  ```

- **Return Values**

  - To let a function return a value, use the `return` statement.

  ```py
  print("\n--------Return--------\n")


  def square(num):
      return num * num


  print(square(3))  # 9
  print(square(5))  # 25
  print(square(9))  # 81
  ```

- `pass`:

  - function definitions cannot be empty.
  - put in the `pass` statement to avoid getting an error when a function has no content.

  ```py
  def myfunction():
    pass
  ```

---

## Arbitrary Arguments, `*args`

- add a `*` before the parameter name in the function definition, when the number of arguments is unknown.

- the function will receive a **tuple** of arguments, and can access the items accordingly.

- `Arbitrary Arguments` are often shortened to `*args` in Python documentations.

- `Arbitrary Arguments` cannot have default values.

```py
def printOS(*names):
    print("\n2nd OS: " + names[1])


printOS("iOS", "Windows", "Linux")      # 2nd OS: Window
printOS("iOS", "Windows")               # 2nd OS: Window
# printOS("iOS")                         # IndexError: tuple index out of range
```

---

## Keyword Arguments

- `Keyword Arguments`: send arguments with the `key = value` syntax.

  - the order of the arguments does not matter.

- The phrase `Keyword Arguments` are often shortened to `kwargs` in Python documentations.

- Positional argument **cannot appear** after keyword arguments
  - Note: All the positional parameters should **precede** the named parameters

```py
def printName(fname, lname, nickname):
    print(fname, lname, nickname)


# John Doe steely-eyed missile man
printName("John", "Doe", "steely-eyed missile man")
# positional: steely-eyed missile man Doe John
printName("steely-eyed missile man", "Doe", "John")
# Keyword Arguments: John Doe steely-eyed missile man
printName(nickname="steely-eyed missile man", lname="Doe", fname="John")
# Combination: John Doe steely-eyed missile man
printName("John", nickname="steely-eyed missile man", lname="Doe")

```

---

## Arbitrary Keyword Arguments, `**kwargs`

- add two asterisk: `**` before the parameter name in the function definition, when the number of keyword arguments is unknown.

- The function will receive a **dictionary** of arguments, and can access the items accordingly.

- `Arbitrary Kword Arguments` are often shortened to `**kwargs` in Python documentations.

```py
print("\n--------Key Argument--------\n")


def printName(**person):
    print(person["fname"], person["lname"], person["nickname"])


# John Doe Iron Man
printName(fname="John", lname="Doe", nickname="Iron Man")

# Key Argument cannot replace with a dict: TypeError: printName() takes 0 positional arguments but 1 was given
# 因为使用**定义,所以表明没有positional参数,所以使用字典作为参数时, 与函数定义的不同.
printName({"fname": "John", "lname": "Doe", "nickname": "Iron Man"})

print("\n--------Parameter + Key Argument--------\n")


def printName(fname, **person):
    print(fname, person["lname"], person["nickname"])


# John Doe Iron Man
printName(fname="John", lname="Doe", nickname="Iron Man")

print("\n--------Default + Key Argument--------\n")


def printName(fname="john", **person):
    print(fname, person["lname"], person["nickname"])


# john Doe Iron Man
printName(lname="Doe", nickname="Iron Man")

```

---

## Recursion

- Python also accepts function recursion, which means a defined **function can call itself**.

- `Recursion` is a common mathematical and programming concept. It means that a **function calls itself**. This has the benefit of meaning that you can loop through data to reach a result.
  - The developer should be very careful with recursion as it can be quite easy to slip into writing a <u>function which never terminates</u>, or one that <u>uses excess amounts of memory or processor power</u>.
  - However, when written correctly recursion can be a very efficient and mathematically-elegant approach to programming.

```py
def sumInteger(num):
    if num > 0:
        result = num + sumInteger(num-1)
        print(result)
    else:
        result = 0
    return result


num = 4
print(f"Sum of 1-{num}: ", sumInteger(num))
# 1
# 3
# 6
# 10
# Sum of 1-4:  10

```

---

[TOP](#python-functions)
