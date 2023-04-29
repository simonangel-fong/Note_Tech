# Python - Classes/Objects

[back](../index.md)

- [Python - Classes/Objects](#python---classesobjects)
  - [Classes/Objects](#classesobjects)
  - [Object Methods](#object-methods)

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

```py


```

---

[TOP](#python---classesobjects)
