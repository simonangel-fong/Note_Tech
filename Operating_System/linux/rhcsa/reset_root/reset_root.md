# RHCSA Reset root password

[Back](../../index.md)

- [RHCSA Reset root password](#rhcsa-reset-root-password)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
Perform task on Serverb machine
Set "root" password to "ablerate"
```

---

### Solution

- Need to do in console
- Restart
- Interrupt Grub2
  - `e`
  - Ctrl + E
    - `init=/bin/bash`
  - next
- Bash prompt

```sh
# mount fs
mount -o remount,rw /
# reset pass
passwd root
# set auto relabel for SELinux
touch /.autorelabel

exit
exit
```