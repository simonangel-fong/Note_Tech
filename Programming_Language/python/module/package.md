# Python Package

[Back](../index.md)

- [Python Package](#python-package)
  - [Package](#package)
  - [Pip](#pip)

---

## Package

A module is basically You may choose to define functions, classes, or variables in a module.

- `module`: a simple <u>Python script</u> with a `.py` extension file that defines functions, classes, or variables .

- `package`: a directory of a collection of `modules`.

  - Packages allow the hierarchical structure of the module namespace.
  - directory also contains an `__init__.py` file by which the interpreter interprets it as a package.
    - `__init__.py` Python File works as a Constructor for the Python Package.

- `library`: a **reusable** chunk of code.

  - it is often assumed that while a `package` is a collection of `modules`, a `library` is a collection of `packages`.

- `Python frameworks`: a collection of `modules` and `packages` that help programmers to fast track the development process.
  - However, frameworks are usually more complex than libraries.

---

## Pip

- `pip`: The standard package manager for Python

- Download pip: https://pypi.org/project/pip/

- Find pacakge: https://pypi.org/

- import a Package: `import <package>`

- Pip Commands

| Command                           | Description                                        |
| --------------------------------- | -------------------------------------------------- |
| `pip --version`                   | check the pip version                              |
| `pip list`                        | List installed packages                            |
| `pip show <package>`              | Show information about a package                   |
| `pip install <package>`           | downloaded and installed package                   |
| `pip install <package>==1.0.4`    | installed specific version                         |
| `pip install --upgrade <package>` | Upgrade package                                    |
| `pip uninstall <package>`         | Uninstall a package.                               |
| `pip install -r requirements.txt` | Install a list of requirements specified in a file |
| `pip freeze`                      | Generate output suitable for a requirements file   |
| `pip freeze > requirements.txt`   | Generate a txt requirements file                   |

---

[TOP](#python-package)
