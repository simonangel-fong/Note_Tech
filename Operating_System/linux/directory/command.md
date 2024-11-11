# Linux - Directory: Command

[Back](../index.md)

---

- [Linux - Directory: Command](#linux---directory-command)
  - [Navigation](#navigation)
  - [Directory Management](#directory-management)

---

## Navigation

| Command       | Desc                                                      |
| ------------- | --------------------------------------------------------- |
| `pwd`         | Print work directory                                      |
| `pwd -P`      | Print work directory, avoid all symlinks 显示出确实的路径 |
| `cd`          | return to home directory                                  |
| `cd dir_path` | Change directory                                          |
| `ls`          | List files and direcotry                                  |
| `ls -alht`    | List files and direcotry                                  |

---

## Directory Management

| Command                      | Desc                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `mkdir dir_name`             | Make directory                                               |
| `mkdir -p dir_name/dir_name` | Make parent directories as needed                            |
| `mkdir -m 711 dir_name`      | Make directory and **set file mode**                         |
| `rmdir dir_name`             | Remove an empty directory                                    |
| `rmdir -p dir_name/dir_name` | Remove DIRECTORY and its ancestors                           |
| `rm dir_name`                | Remove file of dir                                           |
| `rm -rf dir_name`            | Force to remove directories and their contents recursively   |
| `rm -i dir_name`             | prompt before every removal                                  |
| `cp source destination`      | Copy directory                                               |
| `cp -f source destination`   | Force copy directory                                         |
| `cp -i source destination`   | Copy directory, prompt before overwrite                      |
| `cp -n source destination`   | do not overwrite an existing file                            |
| `cp -r source destination`   | copy directories recursively                                 |
| `mv source destination`      | Move/Rename file or dir                                      |
| `mv -f source destination`   | Force to overwrite                                           |
| `mv -u source destination`   | Move only when the SOURCE file is newer than the destination |

- There is no undo for the above operations.
