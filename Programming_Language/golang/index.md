# Golang

[back](../../index.md)

---

- [Fundamental](./fundamental/fundamental.md)
- [Package](./package/package.md)
- [Variable](./variable/variable.md)
- [Array](./array/array.md)
- [Function](./func/func.md)

---

- [project: card](./proj/card.md)
- [Install](./install/install.md)
  - [hello world](./hello_world/hello_world.md)

---

## Cheapsheet

| CMD                         | DESC                                              |
| --------------------------- | ------------------------------------------------- |
| `go version`                | Show installed Go version                         |
| `go env`                    | Show Go environment settings                      |
| `go mod init <module-name>` | Create a new Go module                            |
| `go run .`                  | Compile and run the current Go program            |
| `go run main.go`            | Run one Go file                                   |
| `go build`                  | Compile the program                               |
| `go build -o app`           | Compile and create an executable named `app`      |
| `go test`                   | Run tests                                         |
| `go test ./...`             | Run all tests in the project                      |
| `go fmt ./...`              | Format all Go code                                |
| `go vet ./...`              | Check for common code problems                    |
| `go get <package>`          | Add or update a dependency                        |
| `go mod tidy`               | Clean up unused dependencies and add missing ones |
| `go list`                   | List package information                          |
| `go doc <package>`          | Show documentation for a package                  |
| `go clean`                  | Remove build cache or generated build files       |
| `go install <package>`      | Build and install a Go command/tool               |
