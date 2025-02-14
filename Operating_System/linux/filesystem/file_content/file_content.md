# Linux - File System: File Content

[Back](../../index.md)

- [Linux - File System: File Content](#linux---file-system-file-content)
  - [Displaying File Content](#displaying-file-content)
  - [Searching Content in Files](#searching-content-in-files)
    - [Search a user name in `/etc/passwd`](#search-a-user-name-in-etcpasswd)
  - [Filtering Text File Data](#filtering-text-file-data)
  - [Sorting Text File Data](#sorting-text-file-data)
  - [Text File Statistics](#text-file-statistics)
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

| CMD                                          | DESC                                                    |
| -------------------------------------------- | ------------------------------------------------------- |
| `grep "pattern" filename`                    | Search for a Simple Word                                |
| `grep "^pattern" filename`                   | Matches lines beginning with                            |
| `grep "pattern$" filename`                   | Matches lines ending with                               |
| `grep "[0-9]" filename`                      | Match Lines with Digits                                 |
| `grep -E "error\|warning" filename`          | Match Multiple Patterns                                 |
| `grep "pattern" file1 file2`                 | Search in Multiple Files                                |
| `grep -r "pattern" /path/to/directory`       | Recursive Search in Directories                         |
| `grep -l "pattern" -r /direcotry`            | List only filenames with matches.                       |
| `grep -v "pattern" filename`                 | Invert match: show lines that do not match the pattern. |
| `grep -i "pattern" filename`                 | Case-Insensitive Search                                 |
| `grep -n "pattern" filename`                 | Show Line Numbers                                       |
| `grep -w "pattern" filename`                 | Match whole words only.                                 |
| `grep -c "pattern" filename`                 | Count the number of matching lines.                     |
| `grep -o "pattern" filename`                 | Print only the matched part of the line.                |
| `grep -A NUM "pattern" filename`             | Show NUM lines after a match.                           |
| `grep -B NUM "pattern" filename`             | Show NUM lines before a match.                          |
| `grep -C NUM "pattern" filename`             | Show NUM lines of context (before and after).           |
| `egrep "pattern" file1.txt file2.txt`        | Match Patterns in Multiple Files                        |
| `egrep "error\| warning\|critical" file.txt` | Searches for lines containing any of the words.         |
| `egrep -i "pattern" file.txt`                | Ignore Case                                             |
| `egrep -v "pattern" file.txt`                | Show lines that do not match the pattern.               |
| `egrep -n	"pattern" file.txt`                 | Display line numbers with the matching lines.           |
| `egrep -c "pattern" file.txt`                | Count the Number of Matches                             |
| `egrep "a{3}" file.txt`                      | Match a Specific Number of Repetitions                  |
| `egrep "colou?r" file.txt`                   | the u? makes the "u" optional.                          |
| `egrep "file-+" file.txt`                    | Match "file-" followed by one or more hyphens           |
| `egrep -A NUM "pattern" filename`            | Show NUM lines after a match.                           |
| `egrep -B NUM "pattern" filename`            | Show NUM lines before a match.                          |
| `egrep -C NUM "pattern" filename`            | Show NUM lines of context (before and after).           |

- `grep`:

  - `global regular expression print`
  - by default uses `basic regular expressions (BREs)`
  - filtering and displaying lines in a file or input that match a given pattern.

- `egrep`:
  - `extended grep`
  - using `extended regular expressions (EREs)`.
  - provides enhanced functionality and eliminates the need to escape certain special characters like +, ?, {}, and |.
  - equivalent to `grep -E`

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

## Text File Statistics

| Command           | Desc                                                  |
| ----------------- | ----------------------------------------------------- |
| `wc text_file`    | Display newline, word, and byte counts for each file. |
| `wc -c text_file` | Display byte counts for each file.                    |
| `wc -m text_file` | Display character counts for each file.               |
| `wc -w text_file` | Display word counts for each file.                    |
| `wc -l text_file` | Display newline counts for each file.                 |

```sh
wc /etc/profile
# 78  247 1899 /etc/profile

# Display newline counts
wc -l /etc/profile
# 78 /etc/profile

# Display word counts
wc -w /etc/profile
# 247 /etc/profile

# Display character counts
wc -m /etc/profile
# 1899 /etc/profile

# Display byte counts
wc -c /etc/profile
# 1899 /etc/profile
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
