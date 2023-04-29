# Python - Input & Print

[Back](../index.md)

- [Python - Input \& Print](#python---input--print)
  - [User Input](#user-input)
  - [Print](#print)

---

## User Input

- Python allows for user input.

```py
print("\n--------input--------\n")
username = input("Enter username:\n>>")
print("Username is: " + username)
```

- Python stops executing when it comes to the `input()` function, and continues when the user has given some input.

---

## Print

```py

print("\n--------print--------\n")


print("\n--------OR--------")
# OR
# return or valuate the fisrt expression when the first expression is true.
# Otherwise, return the second value
print(0 or 1)               # 1
print(1 or 0)               # 1
print(False or 'hey')       # hey
print('hey' or False)       # hey
print('hi!' or 'hey')       # hi!
print('hey' or 'hi!')       # hey
print([] or False)          # False
print(False or [])          # []
print(False or True)        # True
print(True or True)         # True
print(True or 1)            # True
print(1 or True)            # 1

print("\n--------AND--------")
# AND
# return or valuate the second expression when the first expression is true.
# Otherwise, return the first value
print(0 and 1)               # 0
print(1 and 0)               # 0
print(False and 'hey')       # False
print('hey' and False)       # False
print('hi!' and 'hey')       # hey
print('hey' and 'hi!')       # hi!
print([] and False)          # []
print(False and [])          # False
print(False and True)        # False
print(True and True)         # True
print(True and 1)            # 1
print(1 and True)            # True

```

---

[TOP](#python---input--print)
