# Python - Number

[Back](../index.md)

- [Python - Number](#python---number)
  - [Int](#int)
  - [Float](#float)
  - [Complex](#complex)
  - [Type Conversion](#type-conversion)
  - [Random Number](#random-number)

---

- There are three numeric types in Python:
  - `int`
  - `float`
  - `complex`

## Int

- `Int`, or integer, is a whole number, positive or negative, **without decimals**, of unlimited length.

```py
x = 1
y = 35656222554887711
z = -3255522

print(type(x))
print(type(y))
print(type(z))

```

---

## Float

- `Float`, or "floating point number" is a number, positive or negative, **containing one or more decimals**.

- `Float` can also be scientific numbers with an "e" to indicate the power of 10.

```py
x = 1.10
y = 1.0
z = -35.59

x = 35e3
y = 12E4
z = -87.7e100

print(x)  #35000.0
print(y)  #120000.0
print(z)  #-8.77e+101

```

---

## Complex

Complex numbers are written with a "j" as the imaginary part.

```py
x = 3+5j
y = 5j
z = -5j

print(x)    #(3+5j)
print(y)    #5j
print(z)    #(-0-5j)
print(x+y)    #(3+10j)
print(x+z)    #(3+0j)
print(y+z)    #0j
print(x*y)    #(-25+15j)
print(x*z)    #(25-15j)
print(y*z)    #(25-0j)

```

---

## Type Conversion

- convert from one type to another with the `int()`, `float()`, and `complex()` methods

- Note: You cannot convert `complex` numbers into another number type.

```py
x = 1    # int
y = 2.8  # float

#convert from int to float:
a = float(x)
print(a)    #1.0
print(type(a))  #<class 'float'>

#convert from float to int:
b = int(y)
print(b)    #2
print(type(b))  #<class 'int'>

#convert from int to complex:
c = complex(y)
print(c)    #(2.8+0j)
print(type(c))  #<class 'complex'>

```

---

## Random Number

Python **does not have a random() function** to make a random number, but Python has a **built-in module** called random that can be used to make random numbers.

```py
import random

for i in range(3):
    x= random.randrange(1, 10)
    print("x:",x)
'''
x: 6
x: 1
x: 3
'''

```

---

[TOP](#python---number)
