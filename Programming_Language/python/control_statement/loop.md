# Python - Loops

[Back](../index.md)

- [Python - Loops](#python---loops)
  - [while Loop](#while-loop)
  - [for Loop](#for-loop)
  - [Nested Loops](#nested-loops)

---

## while Loop

- `while`: execute a set of statements as long as a condition is true.

  - Note: **remember to increment i**, or else the loop will continue forever.

- `break`: stop the loop.

- `continue`: stop the **current iteration**, and continue with the next iteration.

- `else`: run a block of code once when the condition no longer is true

```py

print("\n--------while loop--------\n")
i = 0
while i < 6:
    i += 1
    print(i)

# 1
# 2
# 3
# 4
# 5


print("\n--------break--------\n")
i = 0
while i < 6:
    i += 1
    if i == 3:
        break
    print(i)

# 1
# 2


print("\n--------continue--------\n")
i = 0
while i < 6:
    i += 1
    if i == 3:
        continue
    print(i)

# 1
# 2
# 4
# 5
# 6


print("\n--------else--------\n")
i = 0
while i < 6:
  i += 1
  print(i)
else:
  print("i is no longer less than 6")

# 1
# 2
# 3
# 4
# 5
# 6
# i is no longer less than 6
```

---

## for Loop

- A `for loop` is used for iterating over a **sequence** (that is either a `list`, a `tuple`, a `dictionary`, a `set`, or a `string`).

- `break`: stop the loop before it has looped through all the items.

- `continue`: stop the current iteration of the loop, and continue with the next.

- `range()`: returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and ends at a specified number.

  - To loop through a set of code a specified number of times.

- `else`: specifies a block of code to be executed **when the loop is finished**

  - The else block will **NOT be executed** if the loop is stopped by a `break` statement.

- `pass`: for loops cannot be empty, put in the `pass` statement to avoid getting an error.

```py
print("\n--------for loop--------\n")
# loop a list
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)

# apple
# banana
# cherry

# loop a string
for x in "banana":
  print(x)


# break
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)
# apple


# continue
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)
# apple
# cherry


# range()
for x in range(6):
  print(x)
# 0
# 1
# 2
# 3
# 4
# 5


# start with 2, end with 5
for x in range(2, 6):
  print(x)
# 2
# 3
# 4
# 5


# start with 2, end with 29, increment the sequence with 3
for x in range(2, 30, 3):
  print(x)
# 2
# 5
# 8
# 11
# 14
# 17
# 20
# 23
# 26
# 29


# else
for x in range(6):
  print(x)
else:
  print("Finally finished!")

# 0
# 1
# 2
# 3
# 4
# 5
# Finally finished!


# break + else
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")
# 0
# 1
# 2


# pass
for x in [0, 1, 2]:
  pass
```

---

## Nested Loops

- A `nested loop` is **a loop inside a loop**.
  - The "inner loop" will be executed one time for each iteration of the "outer loop":

```py
# Nested Loops
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)

# red apple
# red banana
# red cherry
# big apple
# big banana
# big cherry
# tasty apple
# tasty banana
# tasty cherry
```

---

[TOP](#python---loops)
