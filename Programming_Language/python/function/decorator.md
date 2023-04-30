# Python - Decorator

[Back](../index.md)

- [Python - Decorator](#python---decorator)
  - [Function as Object](#function-as-object)
  - [Decorator](#decorator)
  - [Reuse decorator](#reuse-decorator)
  - [Class Decorators](#class-decorators)
  - [Nesting Decorators](#nesting-decorators)
  - [更多在 functools 中](#更多在-functools-中)

---

## Function as Object

- `meta programming`: a part of the program attempts to change another part of program at compile time.

- In Python, everything is treated as an `object`. Even `classes` or any `variable` we define in Python is also assumed as an object.

  - `Functions` are **first-class objects** in the Python because they can **reference to**, **passed to a variable** and **returned from other functions** as well. 被引用, 传递到变量, 和返回.
  - The functions can be declared inside another function and passed as an argument to another function.嵌套函数

  ```py
  def func1(msg):
      print(msg)


  func1("Hii")    # Hii, call a function
  func2 = func1   # pass a function to a variable
  func2("Hii")    # Hii, call a function using a varaiable
  ```

- `higher order function`: A function that accepts other function as an argument.使用一个函数作为参数的函数

  ```py
  def add(x):
    return x+1

  def sub(x):
  return x-1

  def operator(func, x):
  '''high order function'''
  temp = func(x)
  return temp

  print(operator(sub, 10)) # 9
  print(operator(add, 20)) # 21

  ```

- A function can **return** another function.

  - 注意, 返回时没有括号.

  ```py
  def hello():
      def hi():
          print("Hello")
      return hi


  new = hello()
  new()
  # 以上
  # 1. 将hello()函数传递给变量(pass to a variable)new
  # 2. hi() 和hello()是嵌套函数
  # 3. hello函数返回的是hi函数
  # 4. 调用时,使用变量和括号.
  ```

---

## Decorator

```py
print("\n--------Example: without decorator--------\n")


# def divide(x, y):
#     print(x/y)


def outer_div(func):
    '''high order function'''
    def inner(x, y):
        if (x < y):
            x, y = y, x
        return func(x, y)
    return inner


# divide1 = outer_div(divide)
# divide1(2, 4)   # 2.0

print("\n--------Example: without decorator--------\n")


def outer_div(func):
    '''high order function'''
    def inner(x, y):
        if (x < y):
            x, y = y, x
        return func(x, y)
    return inner
# syntax of generator


@outer_div
def divide(x, y):
    '''
    Using decorator to define this function
    will be passed to outer_div function as
    an argument
    '''
    print(x/y)


divide(2, 4)    # 2.0, call function directly

```

---

## Reuse decorator

- `mod_decorator.py`

```py
def do_twice(func):
    def wrapper_function(*args, **kwargs):
      #using abritary parameter to accept unkown number of arguments
      func(*args, **kwargs)
      func(*args, **kwargs)
    return wrapper_function

```

- `main.py`

```py
from mod_decorator import do_twice
print("\n--------Reuse decorator--------\n")


@do_twice
def display(name):
    print(f"Hello {name}")


display("John")
# Hello John
# Hello John
```

---

## Class Decorators

- Python provides two ways to decorate a class.
  - `@classmethod` and `@staticmethod`:
    - used to modify methods inside class that is not connected to any other instance of a class
    - `@staticmethod`: used to define a static method in the class. It is called by using the class name as well as instance of the class.
  - `@property`:
    - used to modify the getters and setters of a class attributes.
    - use the class function as an attribute.

```py
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    @staticmethod
    def hello():
        print("Hello Peter")

    @property
    def display(self):
        return self.name + " got grade " + self.grade


stu = Student("John", "B")
print("Name:", stu.name)        # Name: John
print("Grade:", stu.grade)      # Grade: B

# @property
print(stu.display)              # John got grade B

# @staticmethod
stu.hello()                     # Hello Peter
Student.hello()                 # Hello Peter
```

---

## Nesting Decorators

```py
print("\n--------Nested Decorator--------\n")


def function1(func):
    def inner_func(*args, **kwargs):
        print("function1")
        func(*args, **kwargs)
        func(*args, **kwargs)
        print("------")
    return inner_func


def function2(func):
    def inner_func(*args, **kwargs):
        print("     function2")
        func(*args, **kwargs)
        func(*args, **kwargs)
        func(*args, **kwargs)
        print("     ------")
    return inner_func


@function1
@function2
def function(name):
    print(f"{name}")


function("John")
# function1
#      function2
# John
# John
# John
#      ------
#      function2
# John
# John
# John
#      ------
# ------
```

---

## 更多在 functools 中

---

[TOP](#python---decorator)
