[Back](../index.md)

- The `oraenv` and `coraenv` scripts:

  - **created** during installation.
  - set environment variables based on the contents of the `oratab` file and provide:
    - A central means of **updating all user accounts** with database changes
    - A mechanism for **switching between databases** specified in the `oratab` file

- DBA can use the `oraenv` or `coraenv` script to ensure that **user accounts are updated** and to **switch between databases**.

- file location: `/usr/local/bin/oraenv`

```sh
. oraenv

# or
. /usr/local/bin/oraenv
```

- The `oratab` file resides in different locations based on the host operating system

| Host operating system | File location          |
| --------------------- | ---------------------- |
| Linux                 | /etc/oratab            |
| Solaris               | /var/opt/oracle/oratab |
| IBM AIX               | /etc/oratab            |

![oratab01](./pic/oratab01.png)