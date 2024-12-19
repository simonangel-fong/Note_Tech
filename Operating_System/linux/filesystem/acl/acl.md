# Linux - File System: Access Control List

[Back](../../index.md)

- [Linux - File System: Access Control List](#linux---file-system-access-control-list)
  - [Access Control List (ACL)](#access-control-list-acl)
    - [Default ACLs](#default-acls)
    - [Effective ACLs and Mask](#effective-acls-and-mask)
    - [ACL Command](#acl-command)
  - [Standard Permissions vs ACLs](#standard-permissions-vs-acls)
  - [Lab: ACL](#lab-acl)
    - [Retrieve Stardard Permissions](#retrieve-stardard-permissions)
    - [Grant ACL to a specific user](#grant-acl-to-a-specific-user)
    - [Remove a ACL from a user](#remove-a-acl-from-a-user)
    - [Remove all ACLs(Reset to standard permissions)](#remove-all-aclsreset-to-standard-permissions)

---

## Access Control List (ACL)

- `Access Control List (ACL)`

  - a more **fine-grained and flexible** way to manage permissions compared to traditional file permissions.
  - allow you to assign **specific permissions to individual users or groups** for files and directories, beyond the typical owner, group, and others model.

- **Advantages**:
  - **Granular control**:
    - ACLs allow setting permissions for multiple users or groups on the same file or directory.
  - **No need to create new groups**:
    - You can assign permissions to individual users without changing group memberships.
  - **More flexibility**:
    - You can define read, write, and execute permissions for each user or group independently.

---

### Default ACLs

- `Default ACLs`:

  - the **predefined permissions** that are **automatically inherited** by new files and subdirectories created **within a directory**.
  - **Purpose**:
    - ensure **consistent permissions** for all **newly created files and subdirectories** under a parent directory.
  - Used for **directories**, not individual files
  - do not affect existing files

- Example:

```sh
# Set a Default ACL:
setfacl -m d:u:alice:rwx /parent_directory

# View Default ACLs:
getfacl /parent_directory
# # file: parent_directory
# # owner: root
# # group: root
# user::rwx
# group::r-x
# other::---
# default:user::rwx
# default:user:alice:rwX
# default:group::r-x
# default:mask::rwx
# default:other::---

# Inheritance
touch /parent_directory/new_file
getfacl /parent_directory/new_file
# # file: new_file
# # owner: root
# # group: root
# user::rw-
# user:alice:rw-
# group::r--
# mask::rw-
# other::r--

# Remove a Default ACL
setfacl -x d:u:alice /parent_directory
```

---

### Effective ACLs and Mask

- `Effective ACLs`:

  - the **permissions** that **actually take effect** when access is attempted.
  -
  - **Purpose**:
    - ensure permissions granted by ACLs are **filtered** through a restrictive layer (the `mask`), providing an additional level of control.
  - determined dynamically, by both the **ACL entries** and the **mask value**.
    - The `mask` limits the permissions of all ACL entries except the file owner.

---

- `Mask`
  - the **maximum** `effective permissions` for **users and groups** specified in ACL entries.
  - It acts as a **filter that limits the permissions** granted by ACLs, **except for the owner**.

```sh
getfacl file1
# file: file1
# owner: user
# group: group
user::rw-
group::r--
mask::r--
other::---
user:alice:rw-
```

> - The `mask::r--` restricts the **maximum permissions** to read-only for `group::r--` and `user:alice:rw-`.
> - `Effective permissions` for **Alice** are reduced to **read-only (r--)**, even though the ACL grants `rw-`.

---

### ACL Command

| CMD                                                  | DESC                                          |
| ---------------------------------------------------- | --------------------------------------------- |
| `getfacl filename`                                   | Display the ACL of a file or directory        |
| `setfacl -m u:username:permissions filename`         | Grant a user specific permissions             |
| `setfacl -rm u:username:permissions directory_name`  | Grant a user specific permissions recursively |
| `setfacl -m g:groupname:permissions filename`        | Grant a group specific permissions            |
| `setfacl -m d:u:username:permissions directory_name` | Set a **default ACL** for directories         |
| `setfacl -x u:username filename`                     | Remove specific ACLs                          |
| `setfacl -m m:permissions filename`                  | Modify the Mask                               |
| `setfacl -b filename`                                | Remove all ACLs                               |

- If the output of `ls -l` command contains a `+` at the end of the permissions (e.g., `rw-rw----+`), ACLs are in use.
- Setting `w` permission with ACL does not allow to remove the a file.

  - only the owner can remove the file.

- **ACLs rules**:
  - `u:uid:perms`:
    - Sets the access ACL for a user.
  - `g:gid:perms`
    - Sets the access ACL for a group.
  - `m:perms`
    - Sets the effective rights mask.
  - `o:perms`
    - Sets the access ACL for users other than the ones in the group for the file.
  - `d:rules`
    - Sets the default ACL for a directory.

---

## Standard Permissions vs ACLs

- `Standard permissions`

  - the traditional `read (r)`, `write (w)`, and `execute (x)` permissions assigned to three categories: **Owner**, **Group**, and **Others**.
  - visible using the `ls -l` command
  - `umask(user file-creation mask)` concept
    - applies only at the time of file or directory **creation** and **affects default permissions**.
    - `Default permissions` = `Base permissions` - `umask`

- `ACLs`

  - allow assigning **additional permissions** to **specific users or groups** beyond the owner, group, and others.
  - can **override** `umask` by adding or modifying permissions for specific users or groups **after creation**.
  - ACLs **coexist** with standard permissions
    - If ACLs are applied, a `+` symbol appears at the end of the permission string
  - `Mask`
    - defines the **maximum** `effective permissions` for **users and groups** specified in ACL entries.
    - It **acts as a filter that limits the permissions** granted by ACLs (**except for the owner**).

---

## Lab: ACL

- Create different users

```sh
useradd serveradmin
useradd devops
```

### Retrieve Stardard Permissions

- Create

```sh
su - serveradmin

# create a file
touch /tmp/acltest
# get the default permissions
ll /tmp/acltest
# -rw-rw-r--. 1 serveradmin serveradmin 0 Dec 18 20:23 /tmp/acltest

# get the acl of the file
getfacl /tmp/acltest
# getfacl: Removing leading '/' from absolute path names
# # file: tmp/acltest
# # owner: serveradmin
# # group: serveradmin
# user::rw-
# group::rw-
# other::r--
```

---

### Grant ACL to a specific user

- Try to write the target file without granting permission

```sh
su - devops

vi /tmp/acltest
# "/tmp/acltest" [readonly]
# E45: 'readonly' option is set
# "/tmp/acltest" E212: Can't open file for writing
```

- Grant write permission

```sh
su - serveradmin

# Grant write permission to devops user
setfacl -m u:devops:rw /tmp/acltest
# confirm
getfacl /tmp/acltest
# getfacl: Removing leading '/' from absolute path names
# # file: tmp/acltest
# # owner: serveradmin
# # group: serveradmin
# user::rw-
# user:devops:rw-
# group::rw-
# mask::rw-
# other::r--

ll /tmp/acltest
# -rw-rw-r--+ 1 serveradmin serveradmin 12 Dec 18 20:33 /tmp/acltest
```

> - Note:
>   - `user:devops:rw-` indicates that user `devops` has been granted `w` permission.
>   - `+` indicates that acl is applied to the file.

- Try to write the file as `devops`

```sh
su - devops

vi /tmp/acltest
```

---

### Remove a ACL from a user

- Get the acl of a file

```sh
su - serveradmin

getfacl /tmp/acltest
# getfacl: Removing leading '/' from absolute path names
# # file: tmp/acltest
# # owner: serveradmin
# # group: serveradmin
# user::rw-
# user:devops:rw-
# group::rw-
# mask::rw-
# other::r--
```

- Revoke acl from user

```sh
# remove from devops
setfacl -x u:devops /tmp/acltest
# confirm
getfacl /tmp/acltest
# getfacl: Removing leading '/' from absolute path names
# # file: tmp/acltest
# # owner: serveradmin
# # group: serveradmin
# user::rw-
# group::rw-
# mask::rw-
# other::r--

ll /tmp/acltest
# -rw-rw-r--+ 1 serveradmin serveradmin 12 Dec 18 20:33 /tmp/acltest
```

> Note: `+` indicates that acl still applied to the file, even though the acl has been revoked from the user.

---

### Remove all ACLs(Reset to standard permissions)

```sh
# Get file metadata
ll /tmp/acltest
# -rw-rw-r--+ 1 serveradmin serveradmin 12 Dec 18 20:33 /tmp/acltest

# Remove all ACL
setfacl -b /tmp/acltest
# confirm
getfacl /tmp/acltest
# getfacl: Removing leading '/' from absolute path names
# # file: tmp/acltest
# # owner: serveradmin
# # group: serveradmin
# user::rw-
# group::rw-
# other::r--

ll /tmp/acltest
# -rw-rw-r--. 1 serveradmin serveradmin 12 Dec 18 20:33 /tmp/acltest
```

```


---
```
