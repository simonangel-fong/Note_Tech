# Python - `pip` Package

[Back](../index.md)

- [Python - `pip` Package](#python---pip-package)
  - [`pip`](#pip)
    - [Update](#update)
    - [Command](#command)
    - [Package Management](#package-management)
    - [Requirements Files](#requirements-files)

---

## `pip`

- `pip`
  - a package-management system
  - the package installer for Python.

---

### Update

```sh
$ py -m pip install --upgrade pip
```

---

### Command

- Syntax:

  - `py -m pip command option`
  - `pip command option`

- Common command:

| Command              | Descriptioni             |
| -------------------- | ------------------------ |
| `pip --version`      | Version of pip           |
| `pip list`           | Listing Packages         |
| `pip show package`   | Show packages details    |
| `pip search package` | Search PyPI for packages |

---

### Package Management

| Command                         | Descriptioni        |
| ------------------------------- | ------------------- |
| `pip install package`           | Install a package   |
| `pip install --upgrade package` | Upgrade a package   |
| `pip uninstall package`         | Uninstall a package |

---

### Requirements Files

- Requirements files
  - files containing a list of items to be installed using pip install

| Command                           | Descriptioni                                        |
| --------------------------------- | --------------------------------------------------- |
| `pip freeze > requirements.txt`   | Generate a requirements file                        |
| `pip install -r requirements.txt` | Install multiple packages using a requirements file |

---

[TOP](#python---pip-package)