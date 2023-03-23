# Python Conditions

[Back](../index.md)

- [Python Conditions](#python-conditions)
  - [IF Statement](#if-statement)
  - [Conditional expressions](#conditional-expressions)
  - [Equivalent Expression](#equivalent-expression)

---

## IF Statement

- **Indentation**

  - Python relies on `indentation` (whitespace at the beginning of a line) to **define scope in the code**.
  - Other programming languages often use curly-brackets for this purpose.

- **Logical Condition**

  - mathematics
    - Equals: `a == b`
    - Not Equals: `a != b`
    - Less than: `a < b`
    - Less than or equal to: `a <= b`
    - Greater than: `a > b`
    - Greater than or equal to: `a >= b`

- `elif` is Python's way of saying "if the previous conditions were not true, then try this condition".

- `else`: catches anything which isn't caught by the preceding conditions.

- `pass`: avoid getting an error due to if statement with no content

```py

print("\n--------If Statement--------\n")
a = 33
b = 200
if b > a:
    # print("b is greater than a") # IndentationError: expected an indented block
    print("b is greater than a")


print("\n--------Elif Statement--------\n")
a = 33
b = 33
if b > a:
    print("b is greater than a")
elif a == b:
    print("a and b are equal")


print("\n--------Else Statement--------\n")
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")


a = 200
b = 33
if b > a:
    print("b is greater than a")
elif a == b:
    print("a and b are equal")
else:
    print("a is greater than b")


print("\n--------Pass Statement--------\n")
a = 33
b = 200

if b > a:
  pass
```

---

## Conditional expressions

- `Conditional expressions` (sometimes called a `ternary operator`)

  - allows testing a condition in a single line.

- Syntax:

  - `[on_true] if [expression] else [on_false] `

```py
print("\n--------Conditional expressions--------\n")
a, b = 10, 20
min = a if a < b else b
max = a if a > b else b
print('min: ', min)
print('max: ', max)


# 等价
a, b = 10, 20
if a < b:
    print(b, "is greater")
elif a > b:
    print(b, "is greater")
else:
    print("Equal")

a, b = 20, 20
print(b, "is greater") if a < b else print(
    a, "is greater") if a > b else print("Euqal")


# Define the data to be evaluated
data = [3, 5, 2, 8, 4]
# Use a for loop to evaluate each element in the data
for num in data:
    # Use the ternary operator to determine if the number is even or odd
    result = 'even' if num % 2 == 0 else 'odd'
    # Optionally, print the result of the ternary operator for each element
    print(f'The number {num} is {result}.')

# The number 3 is odd.
# The number 5 is odd.
# The number 2 is even.
# The number 8 is even.
# The number 4 is even.ss
```

---

## Equivalent Expression

```py

# Ternary operator
a, b = 10, 20
min = a if a < b else b
print(min)


# Use tuple for selecting an item
# (if_test_false,if_test_true)[test]
# if [a<b] is true it return 1, so element with 1 index will print
# else if [a<b] is false it return 0, so element with 0 index will
a, b = 10, 20
min = (b, a)[a < b]
print(min)


# Use Dictionary for selecting an item
# if [a < b] is true then value of True key will print
# else if [a<b] is false then value of False key will print
a, b = 10, 20
min = {True: a, False: b}[a < b]
print(min)


# lambda is more efficient than above two methods
# because in lambda  we are assure that
# only one expression will be evaluated unlike in
# tuple and Dictionary
a, b = 10, 20
print((lambda: b, lambda: a)[a < b]())

```

---

[TOP](#python-conditions)
