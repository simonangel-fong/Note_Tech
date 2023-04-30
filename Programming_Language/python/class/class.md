# Python - Classes/Objects

[back](../index.md)

- [Python - Classes/Objects](#python---classesobjects)
  - [Classes/Objects](#classesobjects)
  - [Object Methods](#object-methods)
  - [Operators Overloading](#operators-overloading)

---

## Classes/Objects

- Almost everything in Python is an object, with its properties and methods.

- A Class is like an object constructor, or a "blueprint" for creating objects.

- `class`: To create a class

- `self`

  - a reference to the **current instance of the class**, and is used to access variables that belongs to the class.
  - it has to be the **first parameter** of any **function** in the class.

- `pass`

  - class definitions **cannot be empty**
  - put in the `pass` statement to avoid getting an error.

- `del`

  - `del object_name`
  - `del property_name`

```py
print("\n--------Create class--------\n")


# pass statement
class Person:
    pass


class Person:

    def __init__(self):
        self.fname = "John"
        self.age = 3

    def printName(self):
        print("print", self.fname, self.age)


print("\n--------Create objects--------\n")
# create an object
p1 = Person()
p2 = Person()
p3 = p2

print("p1:\t", p1)      # p1:      <__main__.Person object at 0x000001920671DE20>

print("p2:\t", p2)      # p2:      <__main__.Person object at 0x000001920671DDC0>
print("p3:\t", p3)      # p3:      <__main__.Person object at 0x000001920671DDC0>


print("\n--------Delete Object--------\n")
del p2
# print("p2:\t", p2)                      # NameError: name 'p2' is not defined
print("p3:\t", p3)                      # p3:      <__main__.Person object at 0x000001DBBD9FDDC0>
# 即以上创建了两个object, p1指向reference一个, p2, p3指向另外一个;
# 删除p2变量, 但另一个对象还被p3指向. 所以调用p2异常, 调用p3正常


print("\n--------Access Properties--------\n")
print("p1.fname:\t", p1.fname)           # John
print("p1.age:\t\t", p1.age)             # 3
# print("p1.lname: ", p1.lname)           # AttributeError: 'Person' object has no attribute 'lname'
# 未创建对象属性时, 不能调用


print("\n--------Change Properties value--------\n")
p1.fname = "Mark"
p1.age = 6

print("p1.fname:\t", p1.fname)           # Mark
print("p1.age:\t\t", p1.age)             # 6

print("p3.fname:\t", p3.fname)           # John
print("p3.age:\t\t", p3.age)             # 3


print("\n--------Create Propertires for an object--------\n")
p1.lname = "Wick"
print("p1.lname: ", p1.lname)           # Wick

print("\n--------Delete Propertires--------\n")
# delete a property from an object
del p1.lname
# print(p1.lname)                           # AttributeError: 'Person' object has no attribute 'lname'

del p1.age
# print(p1.age)                           # AttributeError: 'Person' object has no attribute 'age'

```

---

## Object Methods

- Objects can also contain methods.
- Methods in objects are functions that belong to the object.
- `self`: The first parameter in object's funtion

- `__init__()`

  - `__init__()`: always executed when the class is being initiated.
  - it is called **automatically** every time the class is being used to create a new object.
  - `__init__`并不是构造函数，它只是初始化方法。
  - 类的构造函数是`__new__()`

- `__str__()`
  - returns the object representation in a **string format**. This method is supposed to return a human-readable format which is used to display some information about the object

---

## Operators Overloading

- `operator overloading`

  - define the function to use the operator by instances of user-defined data type class.

- When the user uses the operator on the user-defined data types of class, then a **magic function that is associated with the operator** will be invoked automatically. The process of changing the behaviour of the operator is as simple as the behaviour of the function or method defined.

```py
print("\n--------Example: Operator overloading--------\n")


class example01:
    def __init__(self, X):
        self.X = X

    # adding two objects
    def __add__(self, U):
        return self.X + U.X


object_1 = example01(int(input("Please enter the value: ")))
object_2 = example01(int(input("Please enter the value: ")))
print(": ", object_1 + object_2)

object_3 = example01(str(input("Please enter the value: ")))
object_4 = example01(str(input("Please enter the value: ")))
print(": ", object_3 + object_4)

# Please enter the value: 23
# Please enter the value: 23
# :  46
# Please enter the value: dfsd
# Please enter the value: fesfe
# :  dfsdfesfe


class example02:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    # Now, we will add the two objects
    def __add__(self, U):
        return self.X + U.X, self.Y + U.Y


Object_1 = example02(23, 12)
Object_2 = example02(21, 22)
Object_3 = Object_1 + Object_2
print(Object_3)         # (44, 34)


class example03:
    def __init__(self, X: int):
        self.X = X

    def __gt__(self, U) -> bool:
        if (self.X > U.X):
            return True
        else:
            return False


object_1 = example03(int(input(("Please enter the value: "))))
object_2 = example03(int(input(("Please enter the value: "))))
if (object_1 > object_2):
    print("The object_1 is greater than object_2")
else:
    print("The object_2 is greater than object_1")
# Please enter the value: 11
# Please enter the value: 22
# The object_2 is greater than object_1


class example04:
    def __init__(self, X):
        self.X = X

    def __lt__(self, U):
        if (self.X < U.X):
            return "object_1 is less than object_2"
        else:
            return "object_2 is less than object_1"

    def __eq__(self, U):
        if (self.X == U.X):
            return "Both the objects are equal"
        else:
            return "Objects are not equal"


object_1 = example04(int(input("Please enter the value: ")))
object_2 = example04(int(input("Please enter the value: ")))
print(": ", object_1 < object_2)
# Please enter the value: 11
# Please enter the value: 23
# :  object_1 is less than object_2


object_3 = example04(int(input("Please enter the value: ")))
object_4 = example04(int(input("Please enter the value: ")))
print(": ", object_3 == object_4)
# Please enter the value: 1
# Please enter the value: 1
# :  Both the objects are equal

```

- Binary Operators

| Operator | Magic Function            |
| -------- | ------------------------- | ------------------- |
|          |                           |
| `-`      | **add**(self, other)      |
| `*`      | **sub**(self, other)      |
| `-`      | **mul**(self, other)      |
| `/`      | **truediv**(self, other)  |
| `//`     | **floordiv**(self, other) |
| `%`      | **mod**(self, other)      |
| `**`     | **pow**(self, other)      |
| `>>`     | **rshift**(self, other)   |
| `<<`     | **lshift**(self, other)   |
| `&`      | **and**(self, other)      |
| `        | `                         | **or**(self, other) |
| `^`      | **xor**(self, other)      |

- Comparison Operators

| Operator | Magic Function      |
| -------- | ------------------- |
| `<`      | **LT**(SELF, OTHER) |
| `>`      | **GT**(SELF, OTHER) |
| `<=`     | **LE**(SELF, OTHER) |
| `=`      | **GE**(SELF, OTHER) |
| `==`     | **EQ**(SELF, OTHER) |
| `!=`     | **NE**(SELF, OTHER) |

- Assignment Operators

| Operator | Magic Function             |
| -------- | -------------------------- | -------------------- |
| `-=`     | **ISUB**(SELF, OTHER)      |
| `+=`     | **IADD**(SELF, OTHER)      |
| `*=`     | **IMUL**(SELF, OTHER)      |
| `/=`     | **IDIV**(SELF, OTHER)      |
| `//=`    | **IFLOORDIV**(SELF, OTHER) |
| `%=`     | **IMOD**(SELF, OTHER)      |
| `**=`    | **IPOW**(SELF, OTHER)      |
| `=`      | **IRSHIFT**(SELF, OTHER)   |
| `<<=`    | **ILSHIFT**(SELF, OTHER)   |
| `&=`     | **IAND**(SELF, OTHER)      |
| `        | =`                         | **IOR**(SELF, OTHER) |
| `^=`     | **IXOR**(SELF, OTHER)      |

- Unary Operator:

| Operator | Magic Function          |
| -------- | ----------------------- |
| `*`      | **NEG**(SELF, OTHER)    |
| `-`      | **POS**(SELF, OTHER)    |
| `~`      | **INVERT**(SELF, OTHER) |

---

[TOP](#python---classesobjects)
