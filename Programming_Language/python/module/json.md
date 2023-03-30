# Python JSON

[Back](../index.md)

- [Python JSON](#python-json)
  - [JSON](#json)
  - [`json.loads()`: String -\> Dict](#jsonloads-string---dict)
  - [`json.dumps()`: Dict -\> String](#jsondumps-dict---string)

---

## JSON

- `JSON` is a syntax for storing and exchanging data.

- `JSON` is text, written with JavaScript object notation.

- `json`: a built-in package to work with JSON data.

---

## `json.loads()`: String -> Dict

- `json.loads()`: Convert from JSON String to Python Dictionary
-

```py
print("\n----------json.loads()-------\n")
import json

json_str = '{ "name":"John", "age":30, "city":"New York"}'
json_dict = json.loads(json_str)

print(json_dict)                # {'name': 'John', 'age': 30, 'city': 'New York'}
print(json_dict["age"])         # 30
```

---

## `json.dumps()`: Dict -> String

- `json.dumps()`: convert a Python object into a JSON string

- parameter:

  - `indent`: number, define the numbers of indents.
  - `separators`: tuple, change the default separator. default separator is (", ", ": ").
  - `sort_keys`: boolean, specify if the order of the keys should be sorted or not.

```py

import json
print("\n----------json.dumps(): indent-------\n")

print(json.dumps({"name": "John", "age": 30}))
# {"name": "John", "age": 30}

print(json.dumps({"name": "John", "age": 30}, indent=2))
# {
#   "name": "John",
#   "age": 30
# }


print("\n----------json.dumps(): separators-------\n")

print(json.dumps({"name": "John", "age": 30}))
# {"name": "John", "age": 30}

print(json.dumps({"name": "John", "age": 30}, separators=(". ", " = ")))
# {"name" = "John". "age" = 30}


print("\n----------json.dumps(): sort_keys-------\n")

print(json.dumps({"name": "John", "age": 30}))
# {"name": "John", "age": 30}

print(json.dumps({"name": "John", "age": 30}, sort_keys=True))
# {"age": 30, "name": "John"}
```

- Different type of Python object convert to JSON.
  - Set cannot convert to JSON (not JSON serializable).

```py
print("\n----------json.dumps()-------\n")
import json

xDict = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(xDict))


print("dict:\t\t", json.dumps({"name": "John", "age": 30}))     # dict:            {"name": "John", "age": 30}
print("list:\t\t", json.dumps(["apple", "bananas"]))            # list:            ["apple", "bananas"]
print("tuple:\t\t", json.dumps(("apple", "bananas")))           # tuple:           ["apple", "bananas"]
print("string:\t\t", json.dumps("hello"))                       # string:          "hello"
print("int:\t\t", json.dumps(42))                               # int:             42
print("float:\t\t", json.dumps(31.76))                          # float:           31.76
print("boolean:\t", json.dumps(True))                           # boolean:         true
print("boolean:\t", json.dumps(False))                          # boolean:         false
print("None:\t\t", json.dumps(None))                            # None:            null

# print(json.dumps({1,2,3}))      # TypeError: Object of type set is not JSON serializable
```

---

[TOP](#python-json)
