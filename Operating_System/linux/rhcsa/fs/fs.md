# RHCSA File System

[Back](../../index.md)

- [RHCSA File System](#rhcsa-file-system)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
Copy the file /etc/fstab to /var/tmp.

Configure the permissions of /var/tmp/fstab so that:
the file /var/tmp/fstab is owned by the root user
the file /var/tmp/fstab belong to the group root
the file /var/tmp/fstab should not be execubable by anyone
the user "natasha" is able to read and write /var/tmp/fstab
the user "harry" can neither write nor read /var/tmp/fstab
all other users (current or future) have the ability to read /var/tmp/fstab
```

---

### Solution

```sh
cp /etc/fstab /var/tmp
chown root:root /var/tmp/fstab
chmod a-x /var/tmp/fstab

# Grant read and write permissions to the user natasha
setfacl -m u:natasha:rw /var/tmp/fstab
# Deny all permissions to the user harry
setfacl -m u:harry:--- /var/tmp/fstab
# Allow all other users (current and future) to read the file
chmod o+r /var/tmp/fstab

# Verify the permissions
ls -l /var/tmp/fstab
# -rw-rw-r--+ 1 root root 666 Jan 15 21:50 /var/tmp/fstab
getfacl /var/tmp/fstab
# getfacl: Removing leading '/' from absolute path names
# # file: var/tmp/fstab
# # owner: root
# # group: root
# user::rw-
# user:harry:---
# user:natasha:rw-
# group::r--
# mask::rw-
# other::r--
```
