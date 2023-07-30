# Python - `pathlib`

[Back](../index.md)

- [Python - `pathlib`](#python---pathlib)
  - [`pathlib`: Object-oriented filesystem paths](#pathlib-object-oriented-filesystem-paths)
  - [Concrete Paths](#concrete-paths)
    - [`class pathlib.Path(*pathsegments)`](#class-pathlibpathpathsegments)

---

## `pathlib`: Object-oriented filesystem paths

- `pathlib` module

  - offers classes representing filesystem paths with semantics appropriate **for different operating systems**.

- Path classes are divided between **pure paths**, which provide purely computational operations without I/O, and **concrete paths**, which inherit from pure paths but also provide I/O operations.

---

## Concrete Paths

### `class pathlib.Path(*pathsegments)`

- represents concrete paths of the system’s path flavour(instantiating it creates either a PosixPath or a WindowsPath)

- **Attributes**

| Attribute  | Description                                            |
| ---------- | ------------------------------------------------------ |
| `root`     | A string representing the (local or global) root       |
| `anchor`   | the concatenation of the drive and root                |
| `parents`  | the logical ancestors of the path                      |
| `parent`   | The logical parent of the pat                          |
| `name`     | the final path component, excluding the drive and root |
| `suffix`   | The file extension of the final component              |
| `suffixes` | A list of the path’s file extensions:                  |
| `stem`     | The final path component, without its suffix           |

- Methods

| Method             | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `as_posix()`       | Return path string with forward slashes                   |
| `joinpath(*other)` | Combine the path with each of the other arguments in turn |

- Example:

```py
print("\n------- pathlib.Path(*pathsegments)--------\n")

from pathlib import Path

f_path = Path(__file__)

print(f_path)       # c:\Users\simon\Desktop\demo.py

# Attributes
print(f_path.root)          # \
print(f_path.anchor)        # c:\
print(f_path.parents)       # <WindowsPath.parents>

[print(p) for p in f_path.parents]
# c:\Users\simon\Desktop
# c:\Users\simon
# c:\Users
# c:\

print(f_path.parent)        # c:\Users\simon\Desktop
print(f_path.name)          # demo.py
print(f_path.suffix)        # .py
print(f_path.suffixes)      # ['.py']
print(f_path.stem)          # demo

# Methods
print(f_path.as_posix())    # c:/Users/simon/Desktop/demo.py
print(f_path.joinpath("dir1", "dir2"))    # c:\Users\simon\Desktop\demo.py\dir1\dir2
print(Path().joinpath("dir1","dir2"))       #dir1\dir2
```

---

[TOP](#python---pathlib-object-oriented-filesystem-paths)
