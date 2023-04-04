# Python Try Except

[Back](../index.md)

- [Python Try Except](#python-try-except)
  - [Try Except](#try-except)
  - [Exception Handling](#exception-handling)
  - [Raise an exception](#raise-an-exception)

---

## Try Except

- The `try` block: test a block of code for errors.
- The `except` block: handle the error.
- The `else` block: execute code when there is no error.
- The `finally` block: execute code, regardless of the result of the `try` and `except` blocks.

---

## Exception Handling

- When an `error` (or called as `exception`) occurs, Python will normally **stop** and **generate an error message**.

- Since the `try` block **raises** an error, the except block will be executed.

  - Without the `try` block, the program will **crash and raise an error**.

- define exception blocks

  - if to execute a special block of code for a special kind of error, can define as many exception blocks.

  ```py
  try:
    print(x)    # x is not defined
  except NameError:
      print("Variable x is not defined")  # execute
  except:
      print("An exception occurred")
  ```

- **Else**

  - define a block of code to be executed if no errors were raised

    ```py
    print("\n--------else--------\n")
    try:
      print("Hello")
    except:
      print("Something went wrong")
    else:
      print("Nothing went wrong")         # executed
    ```

- **Finally**

  - `finally` block, if specified, will be executed regardless if the try block raises an error or not.
  - to close objects and clean up resources: The program can continue, without leaving the file object open.

  ```py
  print("\n--------finally--------\n")

  try:
      print(x)
  except:
      print("Something went wrong")
  finally:
      print("The 'try except' is finished")       # executed


  print("\n--------finally: close file--------\n")
  try:
      f = open("./demofile.txt")
      try:
          f.write("Lorum Ipsum")
      except:
          print("Something went wrong when writing to the file")
      finally:
          f.close()
  except:
      print("Something went wrong when opening the file")
  ```

---

## Raise an exception

- `raise` to throw (or raise) an exception

```py
print("\n--------raise--------\n")

x = -1
try:
    if x < 0:
        raise Exception("Sorry, no numbers below zero")
except Exception as ex:
    print(ex)           # Sorry, no numbers below zero

x = "hello"
try:
    if not type(x) is int:
        raise TypeError("Only integers are allowed")
except TypeError as ex:
    print("TypeError: {ex}".format(ex=ex))      # TypeError: Only integers are allowed
except Exception as ex:
    print("Exception: {ex}".format(ex=ex))
```

---

[TOP](#python-try-except)
