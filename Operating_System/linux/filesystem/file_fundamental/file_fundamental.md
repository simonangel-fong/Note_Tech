# Linux - File System: Fundamental

[Back](../../index.md)

---

- [Linux - File System: Fundamental](#linux---file-system-fundamental)
  - [File System](#file-system)
  - [File Metadata](#file-metadata)
    - [File name](#file-name)
  - [File type](#file-type)
    - [Hidden files](#hidden-files)
    - [Link](#link)
      - [Hard Link](#hard-link)
      - [Symbolic Links](#symbolic-links)
      - [Hard vs soft](#hard-vs-soft)
      - [Command](#command)
    - [`file`: Display the file type](#file-display-the-file-type)

---

## File System

- `File System`
  - a system used by an operating system to manage files.
  - The system controls how data is saved or retrived.
- OS stores files and directory in an organized and structred way

---

## File Metadata

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

![sample](./pic/ls_sample.jpg)

---

### File name

- No spaces!
  - For some reason, some file names include spaces:
    - encapsulate the entire file name in quotes
      - e.g., `ls "my file"`, `ls 'my file'`
    - escape spaces using backslash(`\`)
      - e.g., `ls my\ file`
- Can include
  - `-`: Hyphens
  - `_`: Underscores
- CamelCase: capitalize the first letter of each word.

---

## File type

- `-`: Regular file
- `d`: Directory
- `l`: Symbolic link
- `c`:
  - `Character special file` / `Character device files`
  - provide access to devices that transfer data character by character
  - Character devices example:
    - audio or graphics cards,
    - input devices like keyboard and mouse.
- `b`:
  - `Block special file`
    - a special type of file that provides an interface to block devices, such as **hard drives**, **SSDs**, **USB drives**, and optical drives.
    - `Block devices` handle data in **fixed-size chunks** or "**blocks**" (usually `512` bytes or more), making them suitable for storage operations.
- `n`: **Network file**
  - refers to a file or resource **located on a remote system** but **accessed over a network** as though it were local.
  - commonly **accessed via protocols** like `NFS` (`Network File System`), `SMB` (`Server Message Block`), or similar technologies that enable file sharing over a network.
- `p`: FIFO
- `s`: Socket

---

### Hidden files

- Hidden files begin with a period.
  - `.file_name`
- can use `ls -a` to list all hidden files.

---

### Link

- 2 Type of link:

  - Hard Link, default
  - Symbolic Link

- `inode`
  - `index node`
  - pointer or number of a file on the hard disk.

---

#### Hard Link

- `Hard Links`

  - connections made via `inode numbers` in the Linux file system.
  - Every `file` in a Linux filesystem is associated with an `index node (inode)`, which is a data structure **containing metadata** about the file.

- In a `hard link`, **multiple** filenames can **point** to the **same inode number**.

  - Example: If file A is a hard link to file B, both A and B share the same inode number and are equal in the file system.

- Feature:
  - **Equality**:
    - A and B are **treated equally** by the file system.
  - **Independence on Deletion**:
    - Deleting one does **not affect the other**.
    - The file's data and inode **persist until all** associated hard links are **deleted**.
  - **Multiple Path Names**:
    - A single file can have **multiple valid path names** via hard links.
- Advantages:

  - Protects **against accidental deletion**:
    - As long as one hard link remains, the file’s data is preserved.
  - When Files Are Deleted:
    - The file's data blocks and inode are **released only after the last** hard link is **removed**.

- Permission:
  - same as regular file `-rw-rw-r--`

---

#### Symbolic Links

- `Soft Links`/`Symbolic Links`

  - special files that **act as shortcuts** to another file.
  - They **store the path** to the target file rather than pointing to the same inode.
  - Example: If file A is a soft link to file B, their **inode numbers are different**, and A points to a different data block containing the path to B.

- Features:
  - **Shortcut-Like Behavior**
    - Similar to shortcuts in Windows, they **simply redirect** to the target file.
- **Separate Inodes**:
  - The inode numbers of the link and the target file are **different**.
- **Dependency**:
  - If the target file (B) is **deleted**, the soft link (A) remains but **points to an invalid location**.
- Advantages:
  - Can link to directories or files on different filesystems.
  - Useful for creating flexible paths without duplicating data.
- Limitations:

  - If the target is deleted or renamed, the soft link becomes **broken (invalid)**.

- Permission:
  - `lrwxrwxrwx`

---

#### Hard vs soft

| Feature    | Hard Links                                                 | Soft Links                                         |
| ---------- | ---------------------------------------------------------- | -------------------------------------------------- |
| Inode      | Share the **same** `inode` with the target file.           | Have a **different** `inode` from the target file. |
| Filesystem | Must be on the **same filesystem** as the target.          | Can **span across different** filesystems.         |
| Deletion   | Effect Target file deletion **doesn’t** affect hard links. | Becomes **invalid** if the target file is deleted. |
| Directory  | Support **Cannot link to directories**.                    | **Can** link to directories.                       |

- Use Cases
  - `Hard Links`:
    - Best for maintaining **multiple valid references** to critical files within the **same** filesystem.
  - `Soft Links`:
    - Ideal for creating shortcuts or referencing files **across different** filesystems.

---

#### Command

| CMD                 | DESC                                         |
| ------------------- | -------------------------------------------- |
| `ln file hlink`     | Create a hard link with different file name  |
| `ln target_file`    | Create a hard link with the same file name   |
| `ln -s file slink`  | Create a soft link with different file name  |
| `ln -s target_file` | Create a soft link with the same file name   |
| `ls -i`             | list inode numbers and identify linked files |

- Example

```sh
mkdir link_dir
cd link_dir

touch file
ln file hln
ln -s file sln
ls -li
total 0
# 20044951 -rw-rw-r--. 2 rheladmin rheladmin 0 Nov 19 21:28 file
# 20044951 -rw-rw-r--. 2 rheladmin rheladmin 0 Nov 19 21:28 hln
# 20044952 lrwxrwxrwx. 1 rheladmin rheladmin 4 Nov 19 21:28 sln -> file

echo "I am the file" >>file
cat file
# I am the file
cat hln
# I am the file
cat sln
# I am the file

rm -f file
cat hln
# I am the file
cat sln
# cat: sln: No such file or directory


ln link_dir/
# ln: link_dir/: hard link not allowed for directory

ln -s link_dir/ l_dir
cd l_dir
pwd
# /home/rheladmin/l_dir
```

---

### `file`: Display the file type

| Command         | Desc                                          |
| --------------- | --------------------------------------------- |
| `file filename` | Display type of a file                        |
| `file *`        | Display each file's type in current directory |

---

[TOP](#linux---file-system-fundamental)
