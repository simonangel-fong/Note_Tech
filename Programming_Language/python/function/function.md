# Python - Functions

[Back](../index.md)

- [Python - Functions](#python---functions)
  - [Function](#function)
  - [Parameter](#parameter)
    - [Parameters / Arguments](#parameters--arguments)
    - [Mutable and Inmutable Argument](#mutable-and-inmutable-argument)
    - [Arbitrary Arguments, `*args`](#arbitrary-arguments-args)
    - [Keyword Arguments](#keyword-arguments)
    - [Arbitrary Keyword Arguments, `**kwargs`](#arbitrary-keyword-arguments-kwargs)
  - [Return](#return)
  - [Recursion](#recursion)
  - [Lambda](#lambda)
  - [Nested Function](#nested-function)
  - [Closure](#closure)

---

## Function

- A function is a block of code which **only runs when it is called**.

  - can pass data, known as **parameters**, into a function.

  - A function can **return** data as a result.

- **Create a function**

  - using the `def` keyword

- **Calling a Function**

  - use the function name followed by **parenthesis**

---

## Parameter

### Parameters / Arguments

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

### Mutable and Inmutable Argument

- `immutable objects`: the value of immutable objects is not changed in the calling block if their value is changed inside the function or method block

  - `integer`, `float`, `string` and `tuple`

- `mutable object`: the value of mutable object is changed in the calling block if their value is changed inside the function or method block
  - `list`, `dict` and `set`

```py

print("\n--------Inmutable Argument--------\n")
print("\n--------Int--------")


def xInt(val):
    val = 2


value = 1
xInt(value)
print(value)    # 1

print("\n--------String--------")


def xStr(val):
    val = 'Change'


value = "unchanged"
xStr(value)
print(value)    # unchanged


print("\n--------float--------")


def xFloat(val):
    val = 0.1


value = 1.00
xFloat(value)
print(value)    # 1.0


print("\n--------tuple--------")


def xFloat(val):
    val = (3, 2, 1)


value = (0, 1, 2)
xFloat(value)
print(value)    # (0, 1, 2)


# Mutable and Inmutable Argument
print("\n--------Mutable Argument--------")

print("\n--------list--------")


def xFloat(val):
    val[0] = -1


value = [0, 1, 2]
xFloat(value)
print(value)    # [-1, 1, 2]


print("\n--------set--------")


def xFloat(val):
    val.add('cherry')


value = {'apple', 'banana'}
xFloat(value)
print(value)    # {'cherry', 'banana', 'apple'}


print("\n--------dict--------")


def xFloat(val):
    val["fname"] = 'Smith'


value = {"fname": 'John', 'lname': 'Wick'}
xFloat(value)
print(value)    # {'fname': 'Smith', 'lname': 'Wick'}
```

---

### Arbitrary Arguments, `*args`

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

### Keyword Arguments

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

### Arbitrary Keyword Arguments, `**kwargs`

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

## Return

- Return multiple value: return a tuple

```py
print("\n--------Return--------\n")

print("\n--------Return Multiple Values--------")


def xFunc(fname):
    lname = "Wick"
    return fname, lname, 88, [1, 2, 3]


print(xFunc('John'))      # ('John', 'Wick', 88, [1, 2, 3])

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

## Lambda

- A lambda function is a **small anonymous function**.

- A lambda function can take any number of arguments, but can **only have one expression**, which returns a value.

- **Syntax**

  - `lambda arguments : expression`

- **Adventage**:
  - Use lambda functions when an **anonymous function** is required for a short period of time.

```py
print("\n--------Lambda--------\n")

xlambda = lambda a: a + 10

ylambda = lambda a, b,c : a*b*c

print(xlambda(5))
print(ylambda(3,4,5))

print("\n--------Lambda: closure--------\n")


def xlambda(n):
    return lambda a: a * n
    # anomymous function inside a function
    # here actually is a closure, a lambda function nested inside a function


# 好处: 该处将n定义为2, 然后在随后的调用中定义a, 则ylambda变成2的倍数计算器
ylambda = xlambda(2)    # n 2
print(ylambda)          # <function xlambda.<locals>.<lambda> at 0x000001EA098E7280>
print(ylambda(1))       # 2
print(ylambda(2))       # 4
print(ylambda(3))       # 6

# # 灵活性:只需定义一个新变量并传递参数为4, 则调用时变成4的倍数计算器
zlambda = xlambda(4)    # n 4
print(zlambda)          # <function xlambda.<locals>.<lambda> at 0x0000021C80B27310>
print(zlambda(1))       # 4
print(zlambda(2))       # 8
print(zlambda(3))       # 12

```

---

## Nested Function

- `Nested function`: function within a function

  - inner function is visible only inside the outer function

- `nonlocal`: the keyword used to work with variables inside nested functions, where the variable should not belong to the inner function.

  - Use the keyword nonlocal to declare that the variable is not local.

- 只在嵌套函数中使用. 如果外层函数没有先行定义变量, 则会报错.
- 内层函数也可以使用 global 关键字,将直接引用调用环境中的变量, 而不是外层函数的变量.

```py

print("\n--------nonlocal--------\n")


def outerFunc():
    x = "John"

    def innerFunc():
        # x = "hello"     # without the nonlocal, x is a local variable
        nonlocal x      # declare x is not a local variable
        x = "hello"
    innerFunc()
    return x


print(outerFunc())        # hello


print("\n--------nonlocal+global--------\n")
fname = "John"


def outerFunc():
    global fname
    fname = 'Django'

    lname = "Wick"

    def innerFunc():
        nonlocal lname
        lname = "Unchained"

    innerFunc()
    print(lname)    # Unchained
    return fname, lname


print(outerFunc())      # ('Django', 'Unchained')
print(fname)      # Django

```

---

## Closure

- `closure`: a function object that remembers the values present in the enclosed scope.

  - With the help of closure, we can invoke functions that are outside the scope in Python.

- It is a record in which each variable of a function is mapped with the value or a reference to the name when the closure was created.
- It acts as an aid to fetch or access the variables with the help of closure copies.

- Usage:

  - A program must have a nested function.
  - The function should refer to a value in the enclosed function.
  - The enclosing function should return the nested function.

- Advantage:
  - Closures provide a kind of data hiding in our program and so we can avoid using global variables.将需要隐藏的数据方法在方法体中而不是全局变量.
  - It is an efficient option when we don't have too many functions in our program.高效: 避免引入太多函数.

```py
print("\n--------Cloaure: Counter--------\n")


def count():
    current_cont = 0    # a local variable starts from 0, rather than a global variable.

    def increment():
        nonlocal current_cont
        current_cont += 1
        return current_cont

    return increment


counter = count()
print(counter)      # <function count.<locals>.increment at 0x0000019E042D7280>
print(counter())    # 1
print(counter())    # 2
print(counter())    # 3


print("\n--------Cloaure: add_num--------\n")
def add_num(n):
    print("n", n)

    def addition(x):
        print("x", x)
        return x+n
    return addition


add_2 = add_num(2)      # n 2, 此时变量是方法的对象, 相当于设置n为2
print(add_2)            # <function add_num.<locals>.addition at 0x0000024EA6687430>
print(add_2(4))         # x 4; 6, 调用方法对象, 即运行方法并调用嵌套方法,并将4传递到嵌套方法.

add_8 = add_num(8)      # n 8
print(add_8(4))         # x 4; 12

print(add_8(add_2(7)))  # 17: 2+7+8=17
```

---

[TOP](#python---functions)
