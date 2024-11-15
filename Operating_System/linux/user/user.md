# Linux - User

[Back](../index.md)

---

- [Linux - User](#linux---user)
  - [Groups](#groups)

---

## Groups

- Every `user` is in **at least one** `group`.
- `Users` can belong to **many** `groups`.
- `Groups` are used to **organize** `users`.
- The `groups` command displays a user’s groups.
- You can also use `id -Gn`.

| Command            | Desc                                   |
| ------------------ | -------------------------------------- |
| `groups`           | show the groups the current user is in |
| `id -Gn`           | show the groups the current user is in |
| `groups user_name` | show the groups a specific user is in  |
| `id user_name -Gn` | show the groups a specific user is in  |
