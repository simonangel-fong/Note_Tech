# Linux - User Management: Password

[Back](../../index.md)

- [Linux - User Management: Password](#linux---user-management-password)
  - [Password Mangement](#password-mangement)
    - [Configure Password for a user](#configure-password-for-a-user)
    - [Configure password for multiple users](#configure-password-for-multiple-users)

---

## Password Mangement

### Configure Password for a user

| CMD                   | DESC                                |
| --------------------- | ----------------------------------- |
| `usermod username -L` | Lock user's pwd                     |
| `usermod username -U` | Unlock user's pwd                   |
| `passwd`              | Modify pwd for the current user     |
| `passwd user`         | Modify pwd for a user               |
| `passwd user -l`      | Lock a user's pwd                   |
| `passwd user -u`      | Unlock a user's pwd                 |
| `passwd user -e`      | Expire a user's pwd                 |
| `passwd user -d`      | Delete a user's pwd                 |
| `passwd user -f`      | Force user to change pwd next login |

---

### Configure password for multiple users

- `chpasswd` syntax:

```sh
chpasswd [options]
[username]:[password]
```

| CMD           | DESC                                                                                                                     |
| ------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `chpasswd`    | update passwords in batch mode                                                                                           |
| `chpasswd -e` | **Encrypts** passwords before storing in the password file.                                                              |
| `chpasswd -c` | **Validates** the password before it is stored.                                                                          |
| `chpasswd -m` | Encrypts the password **using the MD5 algorithm**.                                                                       |
| `chpasswd -R` | Specifies the password file location.                                                                                    |
| `chpasswd -S` | Displays the encrypted password to standard output instead of modifying the password file.                               |
| `chpasswd -c` | Specifies the method to be used for encrypting the password.                                                             |
| `chpasswd -p` | Specifies the **prefix** for the crypt(3) algorithm, e.g.,`.                                                             |
| `chpasswd -s` | Uses the Blowfish encryption algorithm for the password with a minimum value of 1000 and a maximum value of 999,999,999. |

- `chpasswd -c`:

  - method for encryption:
    - `MD5`, `DES`, `SHA256`, `SHA512`, and `NONE`

- `chpasswd -p`:

  - prefix for crypt(3) algorithm
  - `$6$`for SHA512-CRYPT,`$5$`for SHA256-CRYPT, and`$2a$` for Blowfish

- Example: import a list of users and passwords

```sh

```
