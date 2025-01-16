# RHCSA File Permission

[Back](../../index.md)

- [RHCSA File Permission](#rhcsa-file-permission)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
create a collaborative directory /shared/sysadm with the following characteristics:

Group ownership of /shared/sysadm is sysadm.
The directory should be readable, writable, and accessible to member of sysadm, but not to any other user.
(It is understood that root has access to all files and directories on the system.)
Files created in /shared/sysadm automatically have group ownership set to the sysadm group.
```

---

### Solution

```sh
mkdir -p /shared/sysadm
# chgrp sysadm /shared/sysadm
chown :sysadm /shared/sysadm
chmod 2770 /shared/sysadm
# chmod g+s /shared/sysadm
```

- Confirm

```sh
ls -ld /shared/sysadm
# drwxrws--- 2 root sysadm 4096 Jan 13 12:00 /shared/sysadm

# switch to a user in sysadm group
touch touch /shared/sysadm/testfile
ll touch /shared/sysadm/testfile
# -rw-r--r--. 1 harry sysadm 0 Jan 13 12:49 /shared/sysadm/file
```
