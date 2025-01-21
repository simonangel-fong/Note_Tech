# Linux - File System: File Operation

[Back](../../index.md)

---

- [Linux - File System: File Operation](#linux---file-system-file-operation)
  - [Create new file](#create-new-file)
  - [List files](#list-files)
    - [`ls`: List Files](#ls-list-files)
    - [`tree`: list in tree](#tree-list-in-tree)
  - [Search files and directories](#search-files-and-directories)
    - [`locate`: find files using index](#locate-find-files-using-index)
    - [`find`: advanced search](#find-advanced-search)
  - [Move, Copy, Delete](#move-copy-delete)
  - [Archive/Compress Files](#archivecompress-files)
  - [File's Disk Usage](#files-disk-usage)

---

## Create new file

| Cmd                  | desc                            |
| -------------------- | ------------------------------- |
| `touch file`         | create new file                 |
| `cp file destinatio` | copy and create new file        |
| `vi file`            | Create new file using vi editor |

- `vi`:
  - file would be created unless saving the file.

---

## List files

### `ls`: List Files

| Command      | Desc                                                           |
| ------------ | -------------------------------------------------------------- |
| `ls`         | List files and direcotry                                       |
| `ls -alht`   | List files and direcotry                                       |
| `ls -F`      | lists the contents and appends symbols to indicate file types. |
| `ls -t`      | lists files sored by time, most recent file placed at the top  |
| `ls -r`      | lists file wit reverse order.                                  |
| `ls -R`      | lists file recursively                                         |
| `ls -d`      | lists directory name, not contents                             |
| `ls --color` | Colorize the output                                            |

- `ls -F`

  - indicator appended:
    - `/`: Directory
    - `@`: Link
    - `*`: Executable

- `ls -p | grep -v /`:

  - List files only

- `ls -lt`

  - list files base on time
    - newest: at the top
    - oldest: at the bottom

- `ls -ltr`
  - list files base on time reversely
    - newest: at the bottom
    - oldest: at the top

---

### `tree`: list in tree

- `tree`:
  - list contents of directories **in a tree-like format**

| Commande  | Desc                  |
| --------- | --------------------- |
| `tree -d` | List directories only |
| `tree -C` | Colosize output       |

---

## Search files and directories

### `locate`: find files using index

- `locate pattern`:
  - find files by name
  - pattern is requried
  - `locate` if faster than `find`
    - queries an index
    - result are not in real time,非实时，与 index 的失效有关。
      - 新建的文件可能未被 index， 所以无法被 locate
    - 如需要实时，则使用 find

| Command          | Desc                                            |
| ---------------- | ----------------------------------------------- |
| `locate pattern` | Find files and directories matching the pattern |
| `locate uptime`  | matching the pattern                            |
| `locate upti`    | matching the pattern                            |

---

### `find`: advanced search

- `find`:
  - search for files in a directory hierarchy
  - find files match the expression
  - default: find all files in the current directory

| Command                                            | Desc                                                           |
| -------------------------------------------------- | -------------------------------------------------------------- |
| `find`                                             | Find everything under the current directory                    |
| `find path -name file_name`                        | Find files and directories matching pattern under the path     |
| `find /usr/sbin/ -name "*config"`                  | Find the file that ends with "config"                          |
| `find path -iname file_name`                       | ignore case                                                    |
| `find path -ls -name file_name`                    | Performs ls on each of the found items                         |
| `find /usr -name "s*" -ls`                         | comprehensive search                                           |
| `find path -mtime days`                            | find files that are days old                                   |
| `find /usr -mtime +10 -mtime -90`                  | find files that are more 10 days old but less than 90 days old |
| `find path -size num`                              | Finds file that are of size num                                |
| `find /usr -size +1M`                              | Finds file that are larger than 1M                             |
| `find -newer file_name`                            | Finds file that are newer than file.                           |
| `find /etc -type d -newer /etc/passwd`             | Find all directories that are newer than the passwd file       |
| `find -exec command {} \;`                         | Run command against all the files that are found               |
| `find . -exec file {} \;`                          | Execute file command on each items under the current directory |
| `find / -user username -exec cp -rf  {} /path/ \;` | Copies each file or directory recursively to the path          |

---

## Move, Copy, Delete

| Command                          | Desc                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| `mv source destination`          | Move/Rename file                                             |
| `mv -f source destination`       | Force to overwrite                                           |
| `mv -i source destination`       | Move/Rename file, prompt before overwrite                    |
| `mv -u source destination`       | Move only when the SOURCE file is newer than the destination |
| `cp source destination`          | Copy file                                                    |
| `cp source1 source2 destination` | Copy multiple files to a destination                         |
| `cp -f source destination`       | Force copy file                                              |
| `cp -i source destination`       | Copy file, prompt before overwrite                           |
| `cp -n source destination`       | do not overwrite an existing file                            |
| `rm file`                        | Remove file                                                  |
| `rm -f file`                     | Force to remove a file                                       |
| `rm -i file`                     | prompt before every removal                                  |

---

## Archive/Compress Files

| Command                    | Desc                                                                               |
| -------------------------- | ---------------------------------------------------------------------------------- |
| `tar cf tar_file target`   | **Create** a tar archive from a target.                                            |
| `tar cfzv tar_file target` | **Create** a tar archive from a target, using compression.                         |
| `tar tf tar_file`          | **Display** the table of contents (list).                                          |
| `tar xf tar_file`          | **Extract** files from the archive.                                                |
| `tar vxf tar_file`         | **Extract** files from the archive displaying a file list                          |
| `tar vxfj tar_file`        | **Extract** files from the archive displaying a file list using .bzip2 Compression |
| `gzip filename`            | Compress the files into `.gz` file                                                 |
| `gzip -v filename`         | Verbose output                                                                     |
| `gzip -k filename`         | Keep the original file                                                             |
| `gzip -r directory`        | Compress all files in a directory                                                  |
| `gzip -9 filename`         | Change the compression level, from 1 to 9. Default 6                               |
| `gunzip gz_file`           | Uncompress files.                                                                  |
| `gunzip -vk gz_file`       | Uncompress files and Verbose output, keep the gz file                              |
| `zcat gz_file`             | displaying the contents of a gzip compressed file                                  |

- example

```sh
mkdir tardir
cd tardir
touch sheet.csv word.doc
cd ..
ll tardir

# create an archive file from tardir directory
tar cf tps.tar tardir

# list a tar file's content
tar tf tps.tar
# tardir/
# tardir/sheet.csv
# tardir/word.doc

# Extract files to /tmp
cd /tmp
tar xf /home/rheladmin/rhel/tps.tar
ll -d tardir
# drwxrwxr-x. 2 rheladmin rheladmin 39 Nov 13 21:50 tardir

# list files as extracting files
tar vxf /home/rheladmin/rhel/tps.tar
# tardir/
# tardir/sheet.csv
# tardir/word.doc

# create an archive file from tardir directory
tar cf tps.tar tardir

# archive without compress
tar cf arch.tar tardir/
tar czf archc.tar tardir/
ll -h
# -rw-rw-r--. 1 rheladmin rheladmin  70K Nov 13 22:12 archc.tar
# -rw-rw-r--. 1 rheladmin rheladmin 180K Nov 13 22:12 arch.tar
```

---

## File's Disk Usage

| Command          | Desc                                    |
| ---------------- | --------------------------------------- |
| `du`             | Estimates file usage in current path    |
| `du dir/file`    | Estimates file usage of a dir/file      |
| `du -k dir/file` | Display sizes in Kilobytes.             |
| `du -h dir/file` | Display sizes in human readable format. |

---

[TOP](#linux---file-system-file-operation)
