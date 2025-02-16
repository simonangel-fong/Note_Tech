# Linux - Fundamental: Kernel

[Back](../../index.md)

- [Linux - Fundamental: Kernel](#linux---fundamental-kernel)
  - [I/O](#io)
    - [Input/Output Types](#inputoutput-types)
    - [Null Device](#null-device)
    - [Redirection](#redirection)
  - [`tee`: Redirect both display and a file](#tee-redirect-both-display-and-a-file)
    - [`|`: Pips](#-pips)
    - [Wildcard](#wildcard)
  - [Lab: I/O Redirection](#lab-io-redirection)
    - [Redirect the Error Output](#redirect-the-error-output)
    - [Redirect to Null Device](#redirect-to-null-device)

---

## I/O

### Input/Output Types

| I/O Name        | Abbreviation | File Descriptor |
| --------------- | ------------ | --------------- |
| Standard Input  | `stdin`      | `0`             |
| Standard Output | `stdout`     | `1`             |
| Standard Error  | `stderr`     | `2`             |

- Input(`stdin`) - `0`

  - when feeding file contents to a file.
  - `<` symbol
    - used to redirect input from a file

- Output(`stdout`) - `1`

  - by default, when running a command its output goes to the terminal
  - `>` symbol
    - used to redirect output to a file.
  - `>>` symbol
    - used to redirect output append to a file.

- Error(`stderr`) - `2`
  - when the command produced any error.
  - `2>` / `2>>` can be used to redirect output.

---

### Null Device

- `Null Device`

  - a special file that discards all the data written to it.

- `>/dev/null`: Redirect output to nowhere.

---

### Redirection

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
- `&>file`
  - redirect both output and error to alternative locations
- `2>file`
  - Redirect standard **error to a file**.

```sh
ls /usr /cdr &>output.out
cat output.out
# ls: cannot access '/cdr': No such file or directory
# /usr:
# bin
# games
# include
# lib
# lib64
# libexec
# local
# sbin
# share
# src
# tmp
```

---

## `tee`: Redirect both display and a file

| CMD                          | DESC                             |
| ---------------------------- | -------------------------------- |
| `ls /etc \| tee /tmp/output` | printed on the screen as well as |
| redirected to file           |

```sh
# As user1 on server1, run the ls command on /etc, /dvd, and
# /var. Have the output printed on the screen as well as
# redirected to file /tmp/ioutput, and the errors forwarded to
# file /tmp/ioerror. Check both files after the execution of the
# command and analyze the results. (Hint: Input, Output, and
# Error Redirections).

ls /dvd /var > /tmp/output 2> /tmp/error
```


---

### `|`: Pips

- `|`

  - pipe symbol
  - `command-output | command-input`
  - take standard **output** from the preceding command and passes it as standard **input** to the following command.
    - The error message of the preceding command will not be passed to the second command by default.
    - If error message is needed, using the I/O direction.

- Example:

```sh
# the file content from the cat command will be the content of grep command
cat file | grep pattern
```

---

### Wildcard

| Wildcard        | Desc                                                            |
| --------------- | --------------------------------------------------------------- |
| `*`             | Matches zero or more characters                                 |
| `?`             | Matches exactly one characters                                  |
| `[aeiou]`       | Character class, matches **exactly one** of included characters |
| `[!aeiou]`      | Exclude **exactly one** of characters                           |
| `[a-g]`,`[3-6]` | Range                                                           |
| `\?`,`\*`       | Escape character, match a wildcard character.                   |

- Named Character Classes

  - `[[:alpha:]]`: Matches alphabetic characters
  - `[[:lower:]]`: Matches lower-case letters
  - `[[:upper:]]`: Matches upper-case letters
  - `[[:digit:]]`: Matches any one digit 0-9
  - `[[:alnum:]]`: Matches all alphanumeric characters
  - `[[:space:]]`: Matches white space
  - `[[:blank:]]`: Matches blank characters, such as space and tab
  - `[[:cntrl:]]`: Matches control characters
  - `[[:graph:]]`: Matches graphical characters
  - `[[:print:]]`: Matches printable characters
  - `[[:punct:]]`: Matches punctuation characters

---

- Example

```sh
ll c[aeiou]t
ll [a-d]*
cp *[[:digit:]] /tmp

rm ??
```

---

## Lab: I/O Redirection

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

### Redirect the Error Output

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

### Redirect to Null Device

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
