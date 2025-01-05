# Server - Database: Oracle 19c on `Redhat9`

[Back](../../index.md)

- [Server - Database: Oracle 19c on `Redhat9`](#server---database-oracle-19c-on-redhat9)
  - [Oracle 19c](#oracle-19c)

---

## Oracle 19c

- Intall "preinstall-19c" package

```sh
curl -o oracle-database-preinstall-19c-1.0-1.el9.x86_64.rpm https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackage/oracle-database-preinstall-19c-1.0-1.el9.x86_64.rpm

dnf -y localinstall oracle-database-preinstall-19c-1.0-1.el9.x86_64.rpm
```
