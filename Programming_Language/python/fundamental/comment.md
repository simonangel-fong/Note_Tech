# Python Comment

[back](../index.md)

- [Python Comment](#python-comment)
  - [Comments](#comments)
  - [Creating a Comment](#creating-a-comment)
  - [Multiline Comments](#multiline-comments)

---

## Comments

- Comments can be used to **explain** Python code.

- Comments can be used to make the code more **readable**.

- Comments can be used to **prevent execution** when testing code.

---

## Creating a Comment

- Comments starts with a **hash mark** `#`, and Python will ignore them.

- Comments can be placed at the **end of a line**, and Python will ignore the rest of the line

```py
#This is a comment
print("Hello, World!")

print("Hello, World!") #This is a comment
```

---

## Multiline Comments

- insert a `#` for each line

- use a multiline string, since Python will ignore string literals that are not assigned to a variable
  - As long as the string is not assigned to a variable, Python will read the code, but then ignore it, and you have made a multiline comment.

```py
#This is a comment
#written in
#more than just one line
print("Hello, World!")

"""
This is a comment
written in
more than just one line
"""
print("Hello, World!")


```

---

[TOP](#python-comment)
