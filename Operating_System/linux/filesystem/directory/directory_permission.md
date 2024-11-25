# Filesystem Security - Directory Permission

[Back](../../index.md)

- [Filesystem Security - Directory Permission](#filesystem-security---directory-permission)
  - [Directory Permissions Overview](#directory-permissions-overview)
  - [`x` Permission on a Directory](#x-permission-on-a-directory)
    - [Lab: Understanding `x` Permission](#lab-understanding-x-permission)
    - [Results](#results)
  - [`r` Permission on a Directory](#r-permission-on-a-directory)
    - [Lab: Understanding `r` Permission](#lab-understanding-r-permission)
    - [Result](#result)
  - [Comparison: `x` vs `r` Permissions on a Directory](#comparison-x-vs-r-permissions-on-a-directory)
  - [Key Foundations](#key-foundations)
    - [Understanding the Role of Permissions in the `ls` Command](#understanding-the-role-of-permissions-in-the-ls-command)
    - [Default File and Directory Permissions](#default-file-and-directory-permissions)

---

Published blog:[linux filesystem security: understanding directory permissions](https://medium.com/@simonangelfong/linux-filesystem-security-understanding-directory-permissions-b0fb423c3db6)

---

## Directory Permissions Overview

In Linux, every entity is treated as a file, and there are three main types of permissions for each file or directory: `r`, `w`, and `x`. While the impact of these permissions is straightforward for files, they behave differently for directories. In this blog, we’ll dive deeper into the effects of x and r permissions on directories.

---

## `x` Permission on a Directory

For files, the `x` permission allows execution. But what does it mean for a directory? The `x` permission on a directory governs the ability to traverse it, i.e., access files or subdirectories within it by their names.

---

### Lab: Understanding `x` Permission

Environment

- OS: `Red Hat Enterprise Linux 8.10`
  Steps:
- 1. Create Users
     Create a user dirowner to own the directory and another user otheruser to test permissions.

```sh
su - root

# create user dirowner
sudo useradd dirowner
echo "dirowner:Linux101" | sudo chpasswd

# create user otheruser
sudo useradd otheruser
echo "otheruser:Linux101" | sudo chpasswd
```

---

- 2. Setup Directory and Files
     Switch to dirowner and create a directory `/tmp/dir` with two files: `file` (regular file) and `script.sh` (shell script). Adjust permissions to test the effects of `x` permission on the directory.

```sh
# switch to dirowner
su - dirowner
whoami
# dirowner

# create target dir
mkdir -p /tmp/dir
# create file within the dir
touch /tmp/dir/file

# create script file and change mode
cat <<EOF > /tmp/dir/script.sh
#!/bin/bash
echo "Hello world"
EOF
cat /tmp/dir/script.sh
# #!/bin/bash
# echo "Hello world"

# Grant x on the script file
chmod o+x /tmp/dir/script.sh

# change mode of the target dir
chmod o-x /tmp/dir

# verify the mode
ls -ld /tmp/dir
# drwxrwxr--. 2 dirowner dirowner 35 Nov 24 16:56 /tmp/dir
ls -l /tmp/dir/file
# -rw-rw-r--. 1 dirowner dirowner 0 Nov 24 16:56 /tmp/dir/file
ls -l /tmp/dir/script.sh
# -rw-rw-r-x. 1 dirowner dirowner 31 Nov 24 16:56 /tmp/dir/script.sh

exit
```

---

- 3. Test Permissions as otheruser
     Switch to otheruser and attempt various operations.

```sh
# Test as otheruser
su - otheruser
whoami
# otheruser

# Test ls commands
ls -dl /tmp/dir
# drwxrwxr--. 2 dirowner dirowner 35 Nov 24 16:56 /tmp/dir

ls /tmp/dir
# ls: cannot access '/tmp/dir/file': Permission denied
# ls: cannot access '/tmp/dir/script.sh': Permission denied
# file  script.sh

ls -l /tmp/dir
# ls: cannot access '/tmp/dir/file': Permission denied
# ls: cannot access '/tmp/dir/script.sh': Permission denied
# total 0
# -????????? ? ? ? ?            ? file
# -????????? ? ? ? ?            ? script.sh

ls /tmp/dir/file
# ls: cannot access '/tmp/dir/file': Permission denied
ls -l /tmp/dir/file
# ls: cannot access '/tmp/dir/file': Permission denied
ls -l /tmp/dir/script.sh
# ls: cannot access '/tmp/dir/script.sh': Permission denied

bash /tmp/dir/script.sh
# bash: /tmp/dir/script.sh: Permission denied

exit
```

---

- 4.Restore `x` Permission
  Restore `x` permission for others and repeat the tests.

```sh
# Correct the directory permission
# switch to dirowner
su - dirowner
whoami
# dirowner
chmod o+x /tmp/dir

# verify mode
ls -dl /tmp/dir
# drwxrwxr-x. 2 dirowner dirowner 35 Nov 24 16:56 /tmp/dir
ls -l /tmp/dir
# total 4
# -rw-rw-r--. 1 dirowner dirowner  0 Nov 24 16:56 file
# -rw-rw-r-x. 1 dirowner dirowner 31 Nov 24 16:56 script.sh

exit
```

---

- 6. Test Permissions as `otheruser`
     Switch to `otheruser` and attempt various operations.

```sh
# Test after correction
# switch to otheruser
su - otheruser
whoami
# otheruser

ls -l /tmp/dir
# -rw-rw-r--. 1 dirowner dirowner  0 Nov 24 16:56 file
# -rw-rw-r-x. 1 dirowner dirowner 31 Nov 24 16:56 script.sh

bash /tmp/dir/script.sh
# Hello world

exit
```

---

### Results

Without `x` Permission on the Directory

| Command                   | Execution         | File name |
| ------------------------- | ----------------- | --------- |
| `ls -dl dir`              | Success           | -         |
| `ls dir`                  | Permission Denied | List      |
| `ls -l dir`               | Permission Denied | List      |
| `ls dir/file`             | Permission Denied | -         |
| `ls -l dir/file`          | Permission Denied | -         |
| `bash /tmp/dir/script.sh` | Permission Denied | -         |

With `x` Permission Restored

| Command                   | Execution |
| ------------------------- | --------- |
| `ls -l dir`               | Success   |
| `bash /tmp/dir/script.sh` | Success   |

---

## `r` Permission on a Directory

For files, the `r` permission allows reading their content. On a directory, `r` permission enables listing the names of files and subdirectories within it.

---

### Lab: Understanding `r` Permission

Continue the lab on top of the above codes.

- Steps
- 1. Revoke `r` Permission
     Modify the permissions of /tmp/dir to revoke r for others.

```sh
su - dirowner
whoami
# dirowner

# list the permission of target dir
ls -dl /tmp/dir
# drwxrwxr-x. 2 dirowner dirowner 35 Nov 24 16:56 /tmp/dir

# Revoking the r permission
chmod o-r /tmp/dir
# verify the mode
ls -dl /tmp/dir
# drwxrwx--x. 2 dirowner dirowner 35 Nov 24 16:56 /tmp/dir

exit
```

---

- 2. Test as `otheruser`
     Repeat the same commands as above.

```sh
# switch user
su - otheruser
whoami
# otheruser

# test command
ls -ld /tmp/dir
# drwxrwx--x. 2 dirowner dirowner 35 Nov 24 16:56 /tmp/dir

ls /tmp/dir
# ls: cannot open directory '/tmp/dir': Permission denied
ls -l /tmp/dir
# ls: cannot open directory '/tmp/dir': Permission denied

ls /tmp/dir/file
# /tmp/dir/file
ls -l /tmp/dir/file
# -rw-rw-r--. 1 dirowner dirowner 0 Nov 24 16:56 /tmp/dir/file
ls -l /tmp/dir/script.sh
# -rw-rw-r-x. 1 dirowner dirowner 31 Nov 24 16:56 /tmp/dir/script.sh

bash /tmp/dir/script.sh
# Hello world
```

---

### Result

Without `r` Permission on the Directory

| Command                   | Execution         | File name |
| ------------------------- | ----------------- | --------- |
| `ls -dl dir`              | Success           | -         |
| `ls dir`                  | Permission Denied | No List   |
| `ls -l dir`               | Permission Denied | No List   |
| `ls dir/file`             | Success           | -         |
| `ls -l dir/file`          | Success           | -         |
| `bash /tmp/dir/script.sh` | Success           | -         |

---

## Comparison: `x` vs `r` Permissions on a Directory

- List only the directory itself

| Command      | Result without `x` | Filename without `x` | Result without `r` | Filename without `r` |
| ------------ | ------------------ | -------------------- | ------------------ | -------------------- |
| `ls -dl dir` | Success            | -                    | Success            | -                    |

---

- List all files within the directory

| Command     | Result without `x` | Filename without `x` | Result without `r` | Filename without `r` |
| ----------- | ------------------ | -------------------- | ------------------ | -------------------- |
| `ls dir`    | Permission Denied  | List                 | Permission Denied  | No List              |
| `ls -l dir` | Permission Denied  | List                 | Permission Denied  | No List              |

---

- List a specific file within the directory

| Command          | Result without `x` | Filename without `x` | Result without `r` | Filename without `r` |
| ---------------- | ------------------ | -------------------- | ------------------ | -------------------- |
| `ls dir/file`    | Permission Denied  | -                    | Success            | -                    |
| `ls -l dir/file` | Permission Denied  | -                    | Success            | -                    |

---

- Execute a specific shell file within the directory

| Command                   | Result without `x` | Filename without `x` | Result without `r` | Filename without `r` |
| ------------------------- | ------------------ | -------------------- | ------------------ | -------------------- |
| `bash /tmp/dir/script.sh` | Permission Denied  | -                    | Success            | -                    |

---

## Key Foundations

To better understand the behavior of the `ls` command and the default permission settings, it's essential to first establish some fundamental concepts about the file system and permissions:

- **Root Directory (`/`) Permissions**:
  - Default permissions: `0555(dr-xr-xr-x)`
  - This ensures the `root` directory is accessible (readable and traversable) by all users, but not writable.
- **Default Permissions in `RHEL`**:
  - **Directories**: Initially assigned `0777` permissions (`drwxrwxrwx`) before applying the `umask`.
  - **Files**: Initially assigned `0666` permissions (`-rw-rw-rw-`) before applying the `umask`.
- **File Creation Mask in RHEL**:
  - The `umask` value: `0022`
  - This subtractive mask **modifies the initial permissions**, ensuring a safer default setup for newly created files and directories.
- **Default Permissions After Applying `umask`**:
  - **Directories**: `0755 (drwxr-xr-x)`
    - Read, write, and execute for the owner; read and execute for others.
  - **Files**: `0644 (-rw-r--r--)`
    - Read and write for the owner; read-only for others.

---

### Understanding the Role of Permissions in the `ls` Command

- The `ls` Command Behavior
  - By default, `ls` retrieves the metadata of its target (file or directory), which requires `x` permission on the parent directory.
  - When the target is a directory, it also gathers the list of filenames, requiring `r` permission on the directory itself.
  - The output of `ls` varies depending on the options used, such as `-l` for detailed metadata or `-t` for sorting by modification time.
- Listing Files Within a Directory (`ls dir` / `ls -l dir`)
  - **Metadata Access**: Controlled by the directory's `x` permission.
  - **Filename Access**: Controlled by the directory's `r` permission.
  - If either `x` or `r` permission is missing, the command will result in a `Permission denied` error.
- Listing a Specific File (`ls /path/to/file` / `ls -l /path/to/file`)
  - The command relies on the `x` permission of the file's parent directory to access its metadata.
- Executing a Script File (`bash /path/to/script`)
  - Both the `x` permission on the script's **parent directory** and the **script file** itself are required to execute the file.

---

### Default File and Directory Permissions

- **Why the default permission of a directory is `5` for others?**
  - It guarantees access to both its **file metadata** and **filename** without further permission configuration, which requires both `1` and `4`.
- **Why the default permission of a file is `4` for others?**
  - Execution of a file need is a privileged operation, which depends on **both** the `x` permission of its **parent directory** and the **file itself**.
  - By default, the parent directory includes `1` to traverse and, therefore, the file must not include `1` bit.
  - Otherwise, file's `1` bit makes it executable by default, which is a risk to the system.

---

[TOP](#filesystem-security---directory-permission)
