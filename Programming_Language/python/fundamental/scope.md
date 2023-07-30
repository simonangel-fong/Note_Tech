# Python - Scope

[Back](../index.md)

- [Python - Scope](#python---scope)
  - [Scope](#scope)
    - [Local Scope](#local-scope)
    - [Enclosing Function Local](#enclosing-function-local)
    - [Global](#global)
      - [`global` Keyword](#global-keyword)
    - [Built-in](#built-in)

---

## Scope

- `scope`:

  - A variable is only **available from inside the region it is created**.

- A variable created inside a function belongs to the `local scope` of that function, and can only be used inside that function.

```py
print("\n--------Scope--------\n")


def xfunc():
    x = 300   # x available only inside the function
    print(x)


xfunc()
# print(x)        # NameError: name 'x' is not defined

```

- **Rule: `LEGB`**

  - Local
  - Enclosing Function local
  - Global
  - Built-in

---

### Local Scope

- `Local`: Names assigned in any way **within a function** (def or lambda), and not declared global in that function.

- When a variable is called whithin a function, Python will look for it inside the function first.

  - When the variable is found, it is a local variable.
  - Local variable is accessable only within the function.

  ```py
  print("\n--------Scope: Local Scope--------\n")

  # global variable
  x = 200


  def xfunc(x):
    # argument creates a local variable.
    # argument copies the value of referenced object.
    x = 300     # assign new value to local variable
    print(x)    # 300, call the local variable


  xfunc(x)    # call function and pass an argument.
  print(x)    # 200, here x is a global variable.
  ```

- When the function has any argument, the argument will create a local variable and copy the value of the referenced object.

  - When the argument a literal value, its value within a function is a literal value.
    - The value of global variable will not be affect.

  ```py
  print("\n--------Scope: Literal Value--------\n")

  x = 200


  def xFunc(x):
      x = 300
      print(x)    # 300


  xFunc(x)
  print(x)    # 200, the global value will be the same.
  ```

  - When the argument is an object, its value is the referenced address.
    - If the function modifies the argument, it will affect the object outside of the function.

  ```py
  print("\n--------Scope: Reference Type--------\n")

  x = [1, 2]


  def xFunc(x):
      x[0] = 0
      print(x)    # [0, 2]


  xFunc(x)
  print(x)    # [0, 2], the object outside the function will be affected.

  ```

---

### Enclosing Function Local

- `Enclosing Function local`:

  - Name in the local scope of any and all **enclosing functions** (def or lambda), **from inner to outer**.

- Variable in the outside function can be access within the inside function.

- When a variable is called whithin a function, Python will look for it inside the function first.

  - When the variable is not found within the current function and the current function is a function inside a function, Python will look for the same name within the outside function.

```py
print("\n--------Scope: function inside function--------\n")


def xfunc():
    x = 300     # local variable
    print(x)

    def yfunc():
        print(x)    # call variable outside of yfunc()

    yfunc()    # call the function inside function


xfunc()
```

---

### Global

- `Global`(module):

  - Names assigned at the top-level of a module file, or declared global in a def within the file.

- `global variable`

  - A variable created in the **main body of the Python code**.
  - belongs to the `global scope`.
  - are available from within **any scope, global and local**.

- When a variable is called whithin a function, Python will look for it inside the function first.

  - If the no variable is found within the current function, Python then looks for the same name in the global variable.

  ```py
  print("\n--------Scope: Global--------\n")

  x = 200


  def xfunc():
      # no x inside the function, Python will call the global variable
      print(x)    # 200


  xfunc()
  ```

---

#### `global` Keyword

- `global`:
  - to create a **global** variable in the **local** scope. The global keyword makes the variable global.
  - to change the value of a global variable inside a function.

```py
print("\n--------'global' Keyword--------\n")
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

### Built-in

- `Built-in`(Python):
  - Names preassigned in the built-in names module : open,range,SyntaxError,...

---

[TOP](#python-scope)
