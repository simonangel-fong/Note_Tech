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
    - [Archive commands](#archive-commands)
    - [Lab: Archive](#lab-archive)
      - [Create archive file without Compression](#create-archive-file-without-compression)
      - [Extract archived files](#extract-archived-files)
      - [Create archive file with Compression](#create-archive-file-with-compression)
      - [Archive multiple files](#archive-multiple-files)
      - [Append file to existing tarfile](#append-file-to-existing-tarfile)
      - [Restore a specific file from tarfile](#restore-a-specific-file-from-tarfile)
    - [Compress Commands](#compress-commands)
    - [Lab: Compress File with `gzip`](#lab-compress-file-with-gzip)
    - [Lab: Compress File with `bzip2`](#lab-compress-file-with-bzip2)
  - [File's Disk Usage](#files-disk-usage)

---

## Create new file

| Cmd                        | desc                            |
| -------------------------- | ------------------------------- |
| `touch file`               | create new file                 |
| `touch -d 2019-09-20 file` | Set the date on file1           |
| `touch -m file`            | change the modification time    |
| `cp file destinatio`       | copy and create new file        |
| `vi file`                  | Create new file using vi editor |

- `vi`:
  - file would be created unless saving the file.

```sh
touch newfile
ll
# total 0
# -rw-r--r--. 1 root root 0 Feb 12 13:41 newfile

# Change date on a file
touch -d 2019-02-09 newfile
# confirm
ll
# total 0
# -rw-r--r--. 1 root root 0 Feb  9  2019 newfile

# Change modfication time
touch -m newfile
ll
# total 0
# -rw-r--r--. 1 root root 0 Feb 12 13:42 newfile

```

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

| Command                        | Desc                                                              |
| ------------------------------ | ----------------------------------------------------------------- |
| `mv source destination`        | Move/Rename file                                                  |
| `mv -f source destination`     | Force to overwrite                                                |
| `mv -i source destination`     | Move/Rename file, prompt before overwrite                         |
| `mv -u source destination`     | Move only when the SOURCE file is newer than the destination      |
| `cp sourcefile newfile`        | Copy file within the same direcotry                               |
| `cp sourcefile dest_dir/`      | Copy file file to a destination directory                         |
| `cp file1 file2 dest_dir`      | Copy multiple files to a destination directory                    |
| `cp -r source_dir/ dest_dir/ ` | Copy all files within a source direcotry to destination directory |
| `cp -p sourcefile dest_dir/`   | Copy and preserve the attributes                                  |
| `cp -f source destination`     | Force copy file                                                   |
| `cp -i source destination`     | Copy file, prompt before overwrite                                |
| `cp -n source destination`     | do not overwrite an existing file                                 |
| `rm file`                      | Remove file                                                       |
| `rm -f file`                   | Force to remove a file                                            |
| `rm -i file`                   | prompt before every removal                                       |

---

## Archive/Compress Files

### Archive commands

- create a single compressed archive of hundreds of files and directories.打包
- `tar` or `star`
  - **preserve** general file **attributes** such as ownership, owning group, and timestamp as well as extended attributes such as ACLs and SELinux contexts.

| Command                     | Desc                                                                               |
| --------------------------- | ---------------------------------------------------------------------------------- |
| `tar -cf tar_file target`   | **Create** a tar archive from a target.                                            |
| `tar -cpf tar_file target`  | **Create** a tar archive from a target, Preserve file permissions                  |
| `tar -cvfz tar_file target` | **Create** a tar archive from a target, using gzip compression.                    |
| `tar -cvjz tar_file target` | **Create** a tar archive from a target, using bzip2 compression.                   |
| `tar -tf tar_file`          | **Display** the table of contents (list).                                          |
| `tar -xf tar_file`          | **Extract** files from the archive.                                                |
| `tar -xvf tar_file`         | **Extract** files from the archive displaying a file list                          |
| `tar -xvfj tar_file`        | **Extract** files from the archive displaying a file list using .bzip2 Compression |

---

### Lab: Archive

#### Create archive file without Compression

```sh
mkdir /root/tardir
touch /root/tardir/sheet.csv /root/tardir/word.doc
ll /root/tardir
# total 0
# -rw-r--r--. 1 root root 0 Feb 11 19:57 sheet.csv
# -rw-r--r--. 1 root root 0 Feb 11 19:57 word.doc

# create an archive file from tardir directory
tar -cvf /root/archive.tar /root/tardir
# /root/tardir/
# /root/tardir/sheet.csv
# /root/tardir/word.doc
# confirm
ll -h /root/archive.tar
# -rw-r--r--. 1 root root 10K Feb 11 20:15 /root/archive.tar

# list a tar file's content
tar -tvf /root/archive.tar
# drwxr-xr-x root/root         0 2025-02-11 19:57 root/tardir/
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/sheet.csv
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/word.doc
```

---

#### Extract archived files

```sh
# Extract files to /root/exdir
mkdir /root/exdir
tar -vxf /root/archive.tar -C /root/exdir
# root/tardir/
# root/tardir/sheet.csv
# root/tardir/word.doc

# confirm
ll -R /root/exdir
# /root/exdir:
# total 0
# drwxr-xr-x. 3 root root 20 Feb 11 20:05 root

# /root/exdir/root:
# total 0
# drwxr-xr-x. 2 root root 39 Feb 11 19:57 tardir

# /root/exdir/root/tardir:
# total 0
# -rw-r--r--. 1 root root 0 Feb 11 19:57 sheet.csv
# -rw-r--r--. 1 root root 0 Feb 11 19:57 word.doc
```

---

#### Create archive file with Compression

```sh
# auto compress
tar -caf /root/archive_auto.tar /root/tardir

# use bzip2
tar -cjf /root/archive_bzip2.tar /root/tardir

# use gzip
tar -czf /root/archive_gzip.tar /root/tardir

# confirm and compare
ll -hS /root/archive.tar /root/archive_auto.tar /root/archive_bzip2.tar /root/archive_gzip.tar
# -rw-r--r--. 1 root root 10K Feb 11 20:22 /root/archive_auto.tar
# -rw-r--r--. 1 root root 10K Feb 11 20:15 /root/archive.tar
# -rw-r--r--. 1 root root 168 Feb 11 20:22 /root/archive_bzip2.tar
# -rw-r--r--. 1 root root 167 Feb 11 20:23 /root/archive_gzip.tar
```

---

#### Archive multiple files

```sh
tar -cvf /root/archive_multi.tar /root/tardir/sheet.csv /root/tardir/word.doc
# tar: Removing leading `/' from member names
# /root/tardir/sheet.csv
# tar: Removing leading `/' from hard link targets
# /root/tardir/word.doc

# confirm
ll -h /root/archive_multi.tar
# -rw-r--r--. 1 root root 10K Feb 11 20:58 /root/archive_multi.tar
tar -tvf /root/archive_multi.tar
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/sheet.csv
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/word.doc
```

#### Append file to existing tarfile

```sh
# append
tar -rvf /root/archive_multi.tar /etc/fstab
# tar: Removing leading `/' from member names
# /etc/fstab
# tar: Removing leading `/' from hard link targets

# confirm
ll -h /root/archive_multi.tar
# -rw-r--r--. 1 root root 10K Feb 11 21:01 /root/archive_multi.tar
tar -tvf /root/archive_multi.tar
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/sheet.csv
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/word.doc
# -rw-r--r-- root/root       666 2025-01-27 02:21 etc/fstab
```

#### Restore a specific file from tarfile

```sh
tar -tvf /root/archive_multi.tar
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/sheet.csv
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/word.doc
# -rw-r--r-- root/root       666 2025-01-27 02:21 etc/fstab

# extract
tar -xvf /root/archive_multi.tar etc/fstab -C /root
# etc/fstab

# confirm
ll -h /root/etc/fstab
# -rw-r--r--. 1 root root 666 Jan 27 02:21 /root/etc/fstab/

tar -tvf /root/archive_multi.tar
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/sheet.csv
# -rw-r--r-- root/root         0 2025-02-11 19:57 root/tardir/word.doc
# -rw-r--r-- root/root       666 2025-01-27 02:21 etc/fstab


```

---

### Compress Commands

- compression tools
  - `gzip`/`gunzip`
    - create a compressed file of each of the specified files
    - adds the `.gz` extension to each file
  - `bzip2` /`bunzip2`
    - creates a compressed file of each of the specified files
    - adds the `.bz2` extension to each file

| Command                  | Desc                                                  |
| ------------------------ | ----------------------------------------------------- |
| `gzip filename`          | Compress the files into `.gz` file                    |
| `gzip -c file1 > foo.gz` | Compress to a destination                             |
| `gzip -v filename`       | Verbose output                                        |
| `gzip -k filename`       | Keep the original file                                |
| `gzip -r directory`      | Compress all files in a directory                     |
| `gzip -9 filename`       | Change the compression level, from 1 to 9. Default 6  |
| `gunzip gz_file`         | Uncompress files.                                     |
| `gunzip -vk gz_file`     | Uncompress files and Verbose output, keep the gz file |
| `bzip2 file_name`        | Compress the files into `.bz2` file                   |
| `bunzip2 bz2_file`       | Uncompress the files                                  |

---

### Lab: Compress File with `gzip`

```sh
mkdir /root/gzipdir
touch /root/gzipdir/sheet.csv /root/gzipdir/word.doc


gzip /root/gzipdir/sheet.csv /root/gzipdir/word.doc

# confirm
ll -h /root/gzipdir/
# total 8.0K
# -rw-r--r--. 1 root root 30 Feb 11 20:39 sheet.csv.gz
# -rw-r--r--. 1 root root 29 Feb 11 20:39 word.doc.gz

# list files
gzip -l /root/gzipdir/sheet.csv.gz
#  compressed        uncompressed  ratio uncompressed_name
#          30                   0   0.0% /root/gzipdir/sheet.csv

# extract
gunzip /root/gzipdir/sheet.csv.gz /root/gzipdir/word.doc.gz
# confirm
ll -h /root/gzipdir/
# total 0
# -rw-r--r--. 1 root root 0 Feb 11 20:39 sheet.csv
# -rw-r--r--. 1 root root 0 Feb 11 20:39 word.doc
```

---

### Lab: Compress File with `bzip2`

```sh
mkdir /root/bzip2
touch /root/bzip2/sheet.csv /root/bzip2/word.doc

ll -h /root/bzip2/
# total 0
# -rw-r--r--. 1 root root 0 Feb 11 20:45 sheet.csv
# -rw-r--r--. 1 root root 0 Feb 11 20:45 word.doc

# compress with bzip2
bzip2 /root/bzip2/sheet.csv /root/bzip2/word.doc
# confirm
ll -h /root/bzip2/
# total 8.0K
# -rw-r--r--. 1 root root 14 Feb 11 20:45 sheet.csv.bz2
# -rw-r--r--. 1 root root 14 Feb 11 20:45 word.doc.bz2

# extract
bunzip2  /root/bzip2/sheet.csv.bz2 /root/bzip2/word.doc.bz2
ll -h /root/bzip2/
# total 0
# -rw-r--r--. 1 root root 0 Feb 11 20:45 sheet.csv
# -rw-r--r--. 1 root root 0 Feb 11 20:45 word.doc
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
