# Linux - I/O

[Back](../index.md)

---

- [Linux - I/O](#linux---io)
  - [Input/Output Types](#inputoutput-types)
  - [Null Device](#null-device)
  - [Redirection](#redirection)
    - [Example of redirection](#example-of-redirection)
    - [Example of error output](#example-of-error-output)
    - [Example of null device](#example-of-null-device)

---

## Input/Output Types

| I/O Name        | Abbreviation | File Descriptor |
| --------------- | ------------ | --------------- |
| Standard Input  | `stdin`      | `0`             |
| Standard Output | `stdout`     | `1`             |
| Standard Error  | `stderr`     | `2`             |

---

## Null Device

- `Null Device`

  - a special file that discards all the data written to it.

- `>/dev/null`: Redirect output to nowhere.

---

## Redirection

- `>`
  - Redirects standard **output to a file**.
  - **Overwrites** (truncating) existing contents.
- `>>`
  - Redirects standard **output to a file**.
  - **Appends** to any existing contents.
- `<`
  - Redirects input **from a file** to a **command**.
- `&`
  - Used with redirection to signal that a `file descriptor` is being **used**.
- `2>&1`
  - Combine stderr and standard output.
- `2>file`
  - Redirect standard **error to a file**.

---

### Example of redirection

```sh
# output to a file
ls -l > file.txt
ls -l 1> file.txt      # equivalent, no space between 1 and >

cat file.txt

# output and append to a file
ls >> file.txt

# redirect from a file to a command
sort < file.txt     # sort doesn't work on file.txt

sort < file.txt > sorted_files.txt  # redirect from file to sort and output to the new txt
```

---

### Example of error output

```sh
# try to ls one existing file and a not existing file, output error
ls file.txt not-here
# ls: cannot access 'not-here': No such file or directory
# file.txt

# output the std output to a file, but display error.
ls file.txt not-here > out
# ls: cannot access 'not-here': No such file or directory
cat out
# file.txt

# output the error to a file, but display std output
ls file.txt not-here 2> out.err
# file.txt
cat out.err
# ls: cannot access 'not-here': No such file or directory

# split std and err into two files
ls file.txt not-here 1>out 2> out.err
cat out
# file.txt
cat out.err
# ls: cannot access 'not-here': No such file or directory

# redirect both into a file
ls file.txt not-here > out.log 2>&1
cat out.log
# ls: cannot access 'not-here': No such file or directory
# file.txt
```

---

### Example of null device

```sh
# try to ls one existing file and a not existing file, output error
ls file.txt not-here
# ls: cannot access 'not-here': No such file or directory
# file.txt

# discard error
ls file.txt not-here 2>/dev/null
# file.txt

# display error only, discard std output
ls file.txt not-here 1>/dev/null
# ls: cannot access 'not-here': No such file or directory

# discard all message,including std output and error
ls file.txt not-here >/dev/null 2>&1
```

---

[TOP](#linux---io)
