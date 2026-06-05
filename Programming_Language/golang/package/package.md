# Golang - Package

[Back](../index.md)

- [Golang - Package](#golang---package)
  - [Package](#package)
    - [Import packages](#import-packages)
    - [Common Commands](#common-commands)
  - [`main` package](#main-package)
    - [Vs python](#vs-python)
    - [Lab: Main package vs non-main package](#lab-main-package-vs-non-main-package)
  - [`import`](#import)

---

## Package

- `Package`
  - a group of Go **source files** that share the **same package name** and are **compiled together**.
  - source files in the same pacakge must has `package <name>` at the very first line.

- Types of packages
  - `main` package
    - the package to build an executable app.
  - Standard library packages
    - the packages already provided by Go.
      - `import "fmt"`: import
      - common: `os`, `math`, `strings`, `net/http`
  - custom packages
    - define: `package <pkg_name>`
    - call: `import <pkg_name>`
  - third-party packages
    - call: `import "github.com/gin-gonic/gin"`

-
- `pkg.go.dev`
  - official central hub for discovering, evaluating, and viewing documentation for Go (Golang) packages and modules

---

### Import packages

- `import` keyword: Importing package.

```go
// single package
import "fmt"
// multiple packages
import ( "fmt" "math" )
// alias
import m "math"
import (
	crand "crypto/rand"
	mrand "math/rand"
)

// use _ to import a package strictly for its initialization logic
import (
	_ "://github.com" // Registers the Postgres driver with the database/sql package
)

// call functions without the package prefix.
import . "fmt"

func main() {
	Println("Hello") // No 'fmt.' prefix needed
}
```

---

### Common Commands

| CMD                         | DESC                                              |
| --------------------------- | ------------------------------------------------- |
| `go mod init <module-name>` | Create a new Go module                            |
| `go get <package>`          | Add or update a dependency                        |
| `go mod tidy`               | Clean up unused dependencies and add missing ones |
| `go list`                   | List package information                          |
| `go doc <package>`          | Show documentation for a package                  |
| `go clean`                  | Remove build cache or generated build files       |
| `go install <package>`      | Build and install a Go command/tool               |

---

## `main` package

- `main package`
  - a special `Go package` used to declear an executable program.
  - Go compiler initializes the executable and invoking `func main()`.
- `func main()`
  - entry point of an executable program.
  - must defined in main package
  - no arguments and returns no value

- `fmt package`
  - a standard Go package for formatted input and output.

---

### Vs python

```py
def main():
    print("Hello")

if __name__ == "__main__":
    main()
```

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello")
}
```

---

### Lab: Main package vs non-main package

- non-main

```sh
tee non-main.go<<EOF
package apple

import "fmt"

func main(){
  fmt.Println("Hi there!")
}
EOF

ls
# non-main.go

go build non-main.go

# confirm. no executable
ls
# non-main.go
```

- main

```sh
tee main.go<<EOF
package main

import "fmt"

func main(){
  fmt.Println("Hi there!")
}
EOF

ls
# main.go  non-main.go

# build
go build main.go
ll
# total 2.3M
# -rwxr-xr-x 1 ubuntuadmin ubuntuadmin 2.3M Jun  4 20:16 main
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin   70 Jun  4 20:15 main.go
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin   71 Jun  4 20:14 non-main.go
```

---

## `import`
