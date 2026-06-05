# Golang - Hello world

[Back](../index.md)

- [Golang - Hello world](#golang---hello-world)
  - [Hello world](#hello-world)

---

## Hello world

```sh
# create project dir
mkdir hello-go
cd hello-go

# Create a Go module
go mod init hello-go
# go: creating new go.mod: module hello-go

ls go.mod

cat go.mod
# module hello-go

# go 1.26.4

# create source file
tee main.go <<EOF
package main

import "fmt"

func main() {
    fmt.Println("Hello World")
}
EOF

# run program
go run .
# Hello World
```

```sh
# build
go build .
# ls -hl
# total 2.3M
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin   27 Jun  4 20:04 go.mod
# -rwxr-xr-x 1 ubuntuadmin ubuntuadmin 2.3M Jun  4 20:06 hello-go
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin   75 Jun  4 20:06 main.go

# run
./hello-go
# Hello World
```
