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
      - [Commands](#commands)
    - [Lab: Find](#lab-find)
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
| `updatedb`       | updated manually                                |

```sh
locate passwd
# /etc/passwd
# /etc/passwd-
# /etc/pam.d/passwd
# /etc/security/opasswd
# /usr/bin/gpasswd
# /usr/bin/grub2-mkpasswd-pbkdf2
# /usr/bin/passwd
# /usr/lib/firewalld/services/kpasswd.xml
# /usr/lib64/samba/pdb/smbpasswd.so
# /usr/lib64/security/pam_unix_passwd.so
# /usr/sbin/chgpasswd
# /usr/sbin/chpasswd
# /usr/sbin/lpasswd
# ...

# limit return
locate -n 3 passwd
# /etc/passwd
# /etc/passwd-
# /etc/pam.d/passwd

locate .sh -n2
# /etc/X11/xinit/xinitrc.d/50-systemd-user.sh
# /etc/X11/xinit/xinitrc.d/localuser.sh

locate -S
# Database /var/lib/mlocate/mlocate.db:
#         10,323 directories
#         134,075 files
#         6,859,661 bytes in file names
#         3,264,303 bytes used to store database
```

---

### `find`: advanced search

- `find`:

  - search for files in a directory hierarchy
  - find files match the expression
  - default: find all files in the current directory

- Syntax:

  - `find` + `path` + `search option` + `action`

- **search option**

  - by name: `-name` / `-iname`
  - by UID//GID: `-user` / `-group`
  - by permissions: `-perm`
  - by inode: `-inum`
  - by access time: `-atime` / `-amin`
  - by modification time: `-mtime` / `-amin`
  - by size / type: `-size` / `-type`

- **Action**
  - `-exec cmd {} \`
  - `-ok cmd {} \`
  - `-delete`

---

#### Commands

- Find by file attributes

| Command                                      | Desc                                                 |
| -------------------------------------------- | ---------------------------------------------------- |
| `find`                                       | Find everything under the current directory          |
| `find /etc -name "*Text"`                    | Find the file that ends with "Text"                  |
| `find /etc -iname "Text"`                    | ignore case                                          |
| `find /etc -iname "Text" -ls`                | Performs ls on each of the found items               |
| `find /usr -size +1M`                        | Finds file that are larger than 1M                   |
| `find /usr -size -1M`                        | Finds file that are smaller than 1M                  |
| `find /var -user rheladmin`                  | Finds file owned by a user                           |
| `find /var -group rheladmin`                 | Finds file owned by a group                          |
| `find /etc -user root -not -group root`      | Finds file owned by a user by not by a group         |
| `find /root -maxdepth 2 -type d`             | Finds directory with max 2 depth                     |
| `find /root -mindepth 2 -maxdepth 3 -type d` | Finds directory with min 2 depth and max 3 depth     |
| `find /dev -perm 660`                        | Finds file with permission                           |
| `find /dev -perm -222`                       | Finds file with at least (-222) writable permissions |
| `find /usr -type l -perm -ug=rw`             | Finds link with read and write for user and group    |

- Find by time

| Command                                | Desc                                                            |
| -------------------------------------- | --------------------------------------------------------------- |
| `find /etc -mtime 0`                   | Finds fine modified today                                       |
| `find /etc -mtime 1`                   | Finds fine modified yesterday                                   |
| `find /etc -mtime +3000`               | Finds fine modified more than 3000 days                         |
| `find /var/log -mmin -30`              | Finds file modified less than 30 min                            |
| `find /usr -mtime +10 -mtime -90`      | Finds files that are more 10 days old but less than 90 days old |
| `find -newer /root/sdir/`              | Finds file that are newer than file.                            |
| `find /etc -type d -newer /etc/passwd` | Find all directories that are newer than the passwd file        |

- Exec/ok
  - `-ok`: need confirm
  - `{}`: replace the found items
  - `\;`: escape `;` which terminate the command

| Command                                                        | Desc                                                           |
| -------------------------------------------------------------- | -------------------------------------------------------------- |
| `find / -name core -type d -exec ls -ld {} \;`                 | List all found directory                                       |
| `find . -exec file {} \;`                                      | Execute file command on each items under the current directory |
| `find /etc/sysconfig -name *.conf -ok cp {} /tmp \;`           | Copies each file or directory recursively to the path          |
| `find /home -user rheladmin -exec cp -r --parents  {} /tmp \;` | Copies each file or directory recursively to the path          |

---

### Lab: Find

```sh
# case sensitive
find /etc -name "*Text"
# /etc/brltty/Text

# case insensitive
find /etc -iname "*Text"
# /etc/selinux/targeted/contexts/initrc_context
# /etc/selinux/targeted/contexts/removable_context
# /etc/selinux/targeted/contexts/userhelper_context
# /etc/selinux/targeted/contexts/virtual_domain_context
# /etc/selinux/targeted/contexts/virtual_image_context
# /etc/selinux/targeted/contexts/failsafe_context
# /etc/brltty/Text

# list
find /etc -name "*Text" -ls
#  880503      8 drwxr-xr-x   2 root     root         4096 Jan 27 02:26 /etc/brltty/Text
find /etc -iname "*Text" -ls
#  938234      4 -rw-r--r--   1 root     root           30 Jan 11  2024 /etc/selinux/targeted/contexts/initrc_context
#  938237      4 -rw-r--r--   1 root     root           33 Jan 11  2024 /etc/selinux/targeted/contexts/removable_context
#  938306      4 -rw-r--r--   1 root     root           33 Jan 11  2024 /etc/selinux/targeted/contexts/userhelper_context
#  938307      4 -rw-r--r--   1 root     root           62 Jan 11  2024 /etc/selinux/targeted/contexts/virtual_domain_context
#  938308      4 -rw-r--r--   1 root     root           71 Jan 11  2024 /etc/selinux/targeted/contexts/virtual_image_context
# 2172386      4 -rw-r--r--   1 root     root           29 Feb 15 13:43 /etc/selinux/targeted/contexts/failsafe_context
#  880503      8 drwxr-xr-x   2 root     root         4096 Jan 27 02:26 /etc/brltty/Text

# find by size
find /usr -size +100M
# /usr/lib/locale/locale-archive
# /usr/lib/locale/locale-archive.real
# /usr/lib64/libLLVM-16.so
# /usr/lib64/firefox/libxul.so

find /usr -size -1k


# find by ownership
find /etc -user root -not -group root
# /etc/polkit-1/localauthority
# /etc/cups
# /etc/cups/classes.conf
# /etc/cups/client.conf
# /etc/cups/cups-files.conf
# /etc/cups/cups-files.conf.default
# /etc/cups/cupsd.conf
# /etc/cups/cupsd.conf.default
# /etc/cups/lpoptions
# /etc/cups/ppd
# /etc/cups/printers.conf
# /etc/cups/snmp.conf
# /etc/cups/snmp.conf.default
# /etc/cups/ssl
# /etc/cups/subscriptions.conf.O
# /etc/cups/subscriptions.conf
# /etc/ssh/ssh_host_ed25519_key
# /etc/ssh/ssh_host_ecdsa_key
# /etc/ssh/ssh_host_rsa_key
# /etc/brlapi.key
# /etc/chrony.keys
# /etc/dnsmasq.conf
# /etc/dnsmasq.d
ll /etc/dnsmasq.d
# drwxr-xr-x. 2 root dnsmasq 6 Feb 28  2024 /etc/dnsmasq.d

# find by type and depth
find /usr/ -maxdepth 2 -type d -name src
# /usr/local/src
# /usr/src

# find  modified (-mtime) more than (the + sign) 2000 days ago
find /etc -mtime +2000

find /etc -mtime +3000
# /etc/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
# /etc/avahi/hosts
# /etc/xdg/user-dirs.conf
# /etc/xdg/user-dirs.defaults
# /etc/speech-dispatcher/clients/emacs.conf

find /var/log -mmin -30
# /var/log/wtmp
# /var/log/audit/audit.log
# /var/log/rhsm/rhsmcertd.log
# /var/log/rhsm/rhsm.log
# /var/log/cron
# /var/log/messages
# /var/log/secure

find /dev -type b -perm 660
# /dev/dm-1
# /dev/dm-0
# /dev/nvme0n1p3
# /dev/nvme0n1p2
# /dev/nvme0n1p1
# /dev/nvme0n1
find . -perm -222 -ls
#  2039722      0 lrwxrwxrwx   1 root     root           28 Feb 12 21:00 ./lndir/softdirln -> /root/lndir/softlink/softdir
#  2039723      0 lrwxrwxrwx   1 root     root           29 Feb 12 21:00 ./lndir/softfileln -> /root/lndir/softlink/softfile
# 20538447      0 -rwxrwxrwx   1 root     root            0 Feb 14 23:26 ./permdir/permfile

find /dev -perm -222 -type c
# /dev/vsock
# /dev/vhost-vsock
# /dev/vhost-net
# /dev/vfio/vfio
# /dev/net/tun
# /dev/dri/renderD128
# /dev/fuse
# /dev/ptmx
# /dev/tty
# /dev/urandom
# /dev/random
# /dev/full
# /dev/zero
# /dev/null

find /etc/sysconfig -name *.conf -ok cp {} /tmp \;
# < cp ... /etc/sysconfig/nftables.conf > ? y
ll /tmp/nftables.conf
# -rw-------. 1 root root 364 Feb 15 14:40 /tmp/nftables.conf

find . -exec file {} \;
# .: directory
# ./.ssh: directory
# ./.bash_logout: ASCII text
# ./.bash_profile: ASCII text
# ./.bashrc: ASCII text
# ./.cshrc: ASCII text
# ./.tcshrc: ASCII text
# ./anaconda-ks.cfg: ASCII text
# ./.cache: directory
# ./.viminfo: ASCII text
# ./.bash_history: ASCII text


ll /home/rheladmin/
# total 0
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Desktop
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Documents
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Downloads
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Music
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Pictures
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Public
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Templates
# drwxr-xr-x. 2 rheladmin rheladmin 6 Jan 27 02:33 Videos

# find and copy
find /home -user rheladmin -exec cp -r --parents  {} /tmp \;

# confirm
ll /tmp/home/rheladmin/
# total 0
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Desktop
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Documents
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Downloads
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Music
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Pictures
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Public
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Templates
# drwxr-xr-x. 2 root root 6 Feb 15 14:49 Videos
```

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
