# Python Scope

[Back](../index.md)

- [Python Scope](#python-scope)
  - [Scope](#scope)
  - [Function Inside Function](#function-inside-function)
  - [Global Scope](#global-scope)
  - [Global Keyword](#global-keyword)

---

## Scope

- `scope`: A variable is only **available from inside the region it is created**.

- A variable created inside a function belongs to the `local scope` of that function, and can only be used inside that function.

```py
print("\n--------Scope--------\n")


def xfunc():
    x = 300
    print(x)


xfunc()
# print(x)        # NameError: name 'x' is not defined

```

---

## Function Inside Function

- Variable in the outside function can be access within the inside function.

```py
print("\n--------Scope: function inside function--------\n")


def xfunc():
    x = 300
    print(x)


    def yfunc():
        print(x)

    yfunc()


xfunc()
# 300
# 300

```

---

## Global Scope

- A variable created in the main body of the Python code is a `global variable` and belongs to the `global scope`.

- `Global variables` are available from within **any scope, global and local**.

  ```py
  print("\n--------Global Scope--------\n")
  x = 300  # global scope


  def xfunc():
      print(x)


  xfunc()         # 300
  print(x)        # 300

  ```

- **Naming Variables**

  If you operate with the same variable name inside and outside of a function, Python will treat them as two separate variables, one available in the global scope (outside the function) and one available in the local scope (inside the function).

  ```py
  x = 300


  def xfunc():
      x = 200
      print(x)        # 200 local variable


  xfunc()

  print(x)            # 300 global variable
  ```

---

## Global Keyword

- `global`:
  - to create a **global** variable in the **local** scope. The global keyword makes the variable global.
  - to change the value of a global variable inside a function.

```py
print("\n--------Global Keyword--------\n")
x = 300


def xfunc():
    x = 200


def yfunc():
    global x        # declare that x in local scope is a global variable
    x = 200


xfunc()
print(x)            # 300 global variable does not change
yfunc()
print(x)            # 200 global variable does not change
```

---

[TOP](#python-scope)
