# RHCSA Tar

[Back](../../index.md)

- [RHCSA Tar](#rhcsa-tar)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
Create a tar archive of "/etc/" Directory with .bzip2 extension.
Tar archive named "myetcbackup.tar" should be place in "/root/" Directory.
```

---

### Solution

```sh
tar -cvjf /root/myetcbackup.tar /etc/
# note, cannot use option: -cvfj, doesnot work.

# confirm
ll -h /root/myetcbackup.tar
# list the contents of the archive
tar -tvjf /root/myetcbackup.tar.bz2
```
