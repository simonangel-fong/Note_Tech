# Linux - Environment Variables

[Back](../../index.md)

---

- [Linux - Environment Variables](#linux---environment-variables)
  - [Environment Variables](#environment-variables)
    - [Common Env Var](#common-env-var)
    - [Env Var Management](#env-var-management)
      - [Persisting Environment Variables](#persisting-environment-variables)

---

## Environment Variables

- `Environment Variable`

  - a **storage location** that has a name and a value.
    - They often effect the way programs behave.
    - used to enhance and to standardize your shell environment on Linux systems.
  - Name/Value pairs
    - `NAME=value`
  - Default: upper case

- Value:

  - do not use space sign

- vs **program/process**
  - When a `process` is **started** it **inherits** the **exported** `environment variables` of the process that **spawned** it.
  - A variable that is set or changed **only effects** the **current running process** unless it is exported.
  - The variables that are **not exported** are called `local variables`.
  - The `export` command allows variables to be used by **subsequently** executed commands

---

### Common Env Var

| Environment Variables | Variable Description                                          |
| --------------------- | ------------------------------------------------------------- |
| `EDITOR`              | The program to run to perform edits.                          |
| `HOME`                | The Home directory of the user.                               |
| `LOGNAME`             | The login name of the user.                                   |
| `MAIL`                | The location of the user's local inbox.                       |
| `OLDPWD`              | The previous working directory.                               |
| `PATH`                | A colon separated list of directories to search for commands. |
| `PAGER`               | This program may be called to view a file.                    |
| `PS1`                 | The primary prompt string.                                    |
| `PWD`                 | The present working directory.                                |
| `USER`                | The username of the user.                                     |

---

### Env Var Management

| Command                      | Desc                                 |
| ---------------------------- | ------------------------------------ |
| `env`                        | list all env var                     |
| `printenv`                   | print all environment                |
| `printenv \| less`           | print all environment                |
| `printenv ENV_VAR1 ENV_VAR2` | print environment var, without `$`   |
| `echo $ENV_VAR1 $ENV_VAR2`   | print environment var                |
| `export ENV_VAR="value"`     | **Create/Update** an environment var |
| `unset ENV_VAR`              | Removing an env var                  |

---

#### Persisting Environment Variables

```sh
echo 'export TZ="US/Pacific"' >> ~/.bash_profile
```
