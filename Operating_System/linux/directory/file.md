# Linux - File

[Back](../index.md)

---

- [Linux - File](#linux---file)
  - [File Property](#file-property)
    - [Hidden files](#hidden-files)
    - [Symbolic Links](#symbolic-links)

---

## File Property

| Command    | Desc                     |
| ---------- | ------------------------ |
| `ls`       | List files and direcotry |
| `ls -alht` | List files and direcotry |

```sh
$ ls -l
# -rw-rw-r-- 1 jason users 10400 Sep 27 08:52 sales.data
```

- Permissions: `-rw-rw-r--`
- Number of links: `1`
- Owner name: `jason`
- Group name: `users`
- Number of bytes in the file: `10400`
- Last modification time: `Sep 27 08:52`
- File name: `sales.data`

---

### Hidden files

- Hidden files begin with a period.
  - `.file_name`
- can use `ls -a` to list all hidden files.

---

### Symbolic Links

- A link points to the actual file or directory.
- Use the link as if it were the file.
- A link can be used to create a shortcut.
- Use for long file or directory names.
- Use to indicate the current version of software.
