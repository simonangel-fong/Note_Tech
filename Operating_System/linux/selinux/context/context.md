# Linux - SELinux: Context

[Back](../../index.md)

- [Linux - SELinux: Context](#linux---selinux-context)
  - [SELinux Contexts](#selinux-contexts)
  - [SELinux user](#selinux-user)
    - [Confined users and Unconfined users](#confined-users-and-unconfined-users)
    - [role](#role)
    - [type](#type)
    - [level](#level)
  - [Common Commands](#common-commands)
  - [Lab:](#lab)
    - [View Proces Content](#view-proces-content)
    - [View User's Context](#view-users-context)

---

## SELinux Contexts

- `SELinux contexts`

  - used on **processes**, Linux **users**, and **files**, on Linux operating systems that run SELinux.
  - used to make access control decisions.

| CMD     | DESC                                              |
| ------- | ------------------------------------------------- |
| `ls -Z` | View the SELinux context of files and directories |

- The `security context` for a Linux user consists of the `SELinux user`, the `SELinux role`, and the `SELinux type`.

  - e.g., `user_u:user_r:user_t`
    - `user_u`: Is the SELinux user.
    - `user_r`: Is the SELinux role.
    - `user_t`: Is the SELinux type.

- After a Linux user logs in, its `SELinux user` **cannot** change.

  - However, its `type` and `role` can change, for example, during transitions.

- To see the SELinux user mapping on your system, use the semanage login -l command as root:

```sh
semanage login -l

# Login Name           SELinux User         MLS/MCS Range        Service
# __default__          unconfined_u         s0-s0:c0.c1023       *
# root                 unconfined_u         s0-s0:c0.c1023       *
```

> Columns
>
> - **Login Name**: Linux users
> - **SELinux User**: The SELinux user to whom the Linux user is mapped.
>   For processes, the SELinux user limits which roles and levels are accessible.
> - **MLS/MCS Range**: level used by `Multi-Level Security (MLS)` and `Multi-Category Security (MCS)`.

---

## SELinux user

- `SELinux user`

  - an identity **known to the authorized policy**
  - Each `Linux user` is **mapped** to an `SELinux user` via SELinux **policy**.

- a `Linux user` has the **restrictions** of the `SELinux user` to which it is assigned.

  - When a `Linux user` that is assigned to an `SELinux user` **launches a process**, this process **inherits** the `SELinux user`’s **restrictions**, unless other rules specify a different role or type.

- By default, **all** `Linux users` in Red Hat Enterprise Linux, including users with administrative privileges, are **mapped** to the **unconfined SELinux user** `unconfined_u`.
  - You can improve the security of the system by assigning users to SELinux confined users.
  - `Linux users` are mapped to the SELinux `__default__` login **by default**, which is mapped to the SELinux `unconfined_u` user.

| CMD                 | DESC                                                              |
| ------------------- | ----------------------------------------------------------------- |
| `semanage login -l` | View the SELinux user mapping                                     |
| `seinfo -u`         | list the available SELinux users(needs `setools-console` package) |

---

### Confined users and Unconfined users

- `Confined users`
  - **restricted** by SELinux rules **explicitly** defined in the current `SELinux policy`.
- `Unconfined users`

  - subject to only **minimal restrictions** by SELinux.

- If an **unconfined** Linux user **executes an application** that SELinux policy defines as one that can transition from the `unconfined_t` domain to its own **confined domain**, the unconfined Linux user is **still subject** to the restrictions of that **confined domain**.

  - The security benefit of this is that, even though a Linux **user** is running **unconfined**, the **application** remains **confined**.
  - Therefore, the exploitation of a flaw in the application can be limited by the policy.

- Each **confined** user is **restricted** by a **confined user domain**.
- The SELinux policy can also define a transition from a confined user domain to its own **target confined domain**.
  - In such a case, confined users are **subject** to the **restrictions** of that **target confined domain**.
  - The main point is that special privileges are associated with the confined users according to their `role`.

---

### role

- `Role-Based Access Control (RBAC)` security model
  - Part of SELinux
- `role`
  - an attribute of `RBAC`.
- `SELinux users` are **authorized** for `roles`, and `roles` are **authorized** for `domains`.
  - The `role` serves as an **intermediary** between `domains` and SELinux `users`.
  - The `role` can be used to determine which `domains` can be **entered** and which **object** types can be accessed.
    - This helps reduce vulnerability to **privilege escalation attacks**.







```sh
semanage user -l
#                 Labeling   MLS/       MLS/
# SELinux User    Prefix     MCS Level  MCS Range                      SELinux Roles

# guest_u         user       s0         s0                             guest_r
# root            user       s0         s0-s0:c0.c1023                 staff_r sysadm_r system_r unconfined_r
# staff_u         user       s0         s0-s0:c0.c1023                 staff_r sysadm_r system_r unconfined_r
# sysadm_u        user       s0         s0-s0:c0.c1023                 sysadm_r
# system_u        user       s0         s0-s0:c0.c1023                 system_r unconfined_r
# unconfined_u    user       s0         s0-s0:c0.c1023                 system_r unconfined_r
# user_u          user       s0         s0                             user_r
# xguest_u        user       s0         s0                             xguest_r
```


```sh
seinfo -r

# Roles: 15
#    auditadm_r
#    container_user_r
#    dbadm_r
#    guest_r
#    logadm_r
#    nx_server_r
#    object_r
#    secadm_r
#    staff_r
#    sysadm_r
#    system_r
#    unconfined_r
#    user_r
#    webadm_r
#    xguest_r
```




---

### type

- `type`
  - an attribute of `Type Enforcement`.
  - defines a `domain` for **processes**, and a `type` for **files**.
- `SELinux policy rules` define how `types` can **access** each other,
  - whether it be a `domain` accessing a `type`,
  - or a `domain` accessing another `domain`.
- **Access is only allowed** if a specific SELinux **policy rule** exists that **allows** it.

---

### level

- `level`
  - an attribute of `MLS` and `MCS`.
- `MLS range`

  - a pair of levels
  - written as
    - `lowlevel-highlevel` if the levels **differ**
    - `lowlevel` if the levels are **identical** (s0-s0 is the same as s0).

- Each `level` is a **sensitivity-category pair**, with categories being optional.

  - If there are **categories**, the level is written as `sensitivity:category-set`.
  - If there are **no categories**, it is written as `sensitivity`.
  - If the category set is a contiguous series, it can be abbreviated.
    - For example, `c0.c3` is the same as `c0,c1,c2,c3`.

- `/etc/selinux/targeted/setrans.conf` file

  - maps levels (`s0:c0`) to human-readable form (that is CompanyConfidential).
  - Do not edit setrans.conf with a text editor
  - use the `semanage` command to make changes.

- Sample of CF

```sh
cat /etc/selinux/targeted/setrans.conf
# s0=SystemLow
# s0-s0:c0.c1023=SystemLow-SystemHigh
# s0:c0.c1023=SystemHigh
```

> - CF: contains human-readable table
> - `s0`: the only one sensitivity When targeted policy enforces MCS
> - `s0-s0:c0.c1023`: sensitivity `s0` and authorized for all categories

---

## Common Commands

| CMD                     | DESC                                         |
| ----------------------- | -------------------------------------------- |
| `ps -eZ \| grep passwd` | Get context of a process                     |
| `id -Z`                 | Get context associated with the current user |

---

## Lab:

### View Proces Content

```sh
ps -eZ | grep passwd
# unconfined_u:unconfined_r:passwd_t:s0-s0:c0.c1023 5768 pts/1 00:00:00 passwd
```

> - `passwd_exec_t`: Context Type
>   the user's shell process transitions to the passwd_t domain

---

### View User's Context

```sh
# view context of root user
id -Z
# unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

> - Current user is mapped to the SELinux `unconfined_u` user
> - running as the `unconfined_r` role
> - running in the `unconfined_t` domain
> - MLS range: `s0-s0`, = `s0`
> - categories the user has access to is defined by c0.c1023, which is all categories (c0 through to c1023).
