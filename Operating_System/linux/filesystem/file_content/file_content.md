# Linux - File System: File Content

[Back](../../index.md)

- [Linux - File System: File Content](#linux---file-system-file-content)
  - [Displaying File Content](#displaying-file-content)
  - [Searching Content in Files](#searching-content-in-files)
    - [Search a user name in `/etc/passwd`](#search-a-user-name-in-etcpasswd)
  - [Filtering Text File Data](#filtering-text-file-data)
  - [Sorting Text File Data](#sorting-text-file-data)
  - [Comparing Files](#comparing-files)

---

## Displaying File Content

| Command            | Desc                                                    |
| ------------------ | ------------------------------------------------------- |
| `cat file_name`    | Display all contents                                    |
| `cat -n file_name` | Display all contents with line numbers                  |
| `more file_name`   | Browse through a text file.                             |
| `less file`        | More features than more.                                |
| `head file`        | Output the first 10 line from the beginning of the file |
| `head -50 file`    | Output the first 50 line from the beginning of the file |
| `tail file`        | Output the last 10 line from the ending of the file     |
| `tail -50 file`    | Output the last 50 line from the ending of the file     |
| `tail -f file`     | Display data as it is being written to the file         |
| `strings`          | Display binary into human readable strings.             |

- `cat`: used for static file contents
- `tail -f`: view file in real time
  - e.g., view log file

---

## Searching Content in Files

| Command                  | Desc                                               |
| ------------------------ | -------------------------------------------------- |
| `grep pattern file`      | Display lines matching a pattern                   |
| `grep -i pattern file`   | Perform a search, **ignoring** case.               |
| `grep -c pattern file`   | **Count** the number of **occurrences** in a file. |
| `grep -n pattern file`   | Precede output with **line numbers**.              |
| `grep -v pattern file`   | Invert Match. Print lines that **don’t match**.    |
| `cut -d'delimiter' file` | Use delimiter as the field separator.              |
| `cut -fN file`           | Display the Nth field.                             |

```sh
cut -d" " -f1 file1
# facebook
# Instagram
# Twitter
# LinkedIn
# TikTok
# Snapchat
# Reddit
# Pinterest
# YouTube
# WhatsApp

cat file1 | grep -i music | cut -d' ' -f1
# TikTok
```

---

### Search a user name in `/etc/passwd`

- Find all users named "rheladmin" in /etc/passwd.
- Print account name and real name.
- Print in alphabetical order by account name.
- Print in a tabular format.

```sh
grep -i rheladmin /etc/passwd | cut -d: -f1,5 | sort | tr ":" " " | column -t
```

---

## Filtering Text File Data

| CMD                       | DESC                         |
| ------------------------- | ---------------------------- |
| `grep pattern /path/file` | Print lines matching pattern |

---

## Sorting Text File Data

- `sort`:
  - alphabetically sort lines of text files
  - only sort text

| Command                | Desc                                |
| ---------------------- | ----------------------------------- |
| `sort file`            | sort from a file and display        |
| `sort file -o newfile` | sort and write result to FILE       |
| `sort -kF file`        | sort via a key. F: the field number |
| `sort -r file`         | sort in reverse order               |
| `sort -u file`         | sort unique                         |
| `sort -n file`         | sort by string numerical value      |

- Example

```sh
cat > txtfile <<EOF
tags: credentials
site: facebook.com
user: bob
pass: Abee!
tags: credentials
EOF
cat txtfile

sort txtfile
# pass: Abee!
# site: facebook.com
# tags: credentials
# tags: credentials
# user: bob

sort -u txtfile
# pass: Abee!
# site: facebook.com
# tags: credentials
# user: bob

sort -ru txtfile
# user: bob
# tags: credentials
# site: facebook.com
# pass: Abee!

sort -u -k2 txtfile
# pass: Abee!
# user: bob
# tags: credentials
# site: facebook.com
```

---

## Comparing Files

| Command               | Desc                                |
| --------------------- | ----------------------------------- |
| `diff file1 file2`    | Compare two files line by line.     |
| `sdiff file1 file2`   | Side-by-side comparison. using `\|` |
| `vimdiff file1 file2` | Highlight differences in vim.       |

- `diff`
  - differences:
    - LineNumFile1-Action-LineNumFile2
    - Action: `(A)dd`, `(C)hange`, `(D)elete`
  - detailed:
    - `<`: Line from file1
    - `---`: separator
    - `>`: Line from file2

```sh
diff file1 file2
# 1,2c1
# < facebook
# < Instagram
# ---
# > Facebook
# 5c4
# < TikTok
# ---
# > 1TikTok
# 8d6
# < Pinterest
```

> Note:
>
> - 1,2c1: line 1,2 of file1 get changed from line 1 of file2
> - 8d6: file1's line 8 have been deleted from file2's line6

---

- `vimdiff`: display in 2 vim windows
  - `Ctrl-w`, `w`: Go to next window
  - `:q`: Quit (close current window)
  - `:qa`: Quit all (close both files)
  - `:qa!`: Force quit all

---

[TOP](#linux---file-system-file-content)
