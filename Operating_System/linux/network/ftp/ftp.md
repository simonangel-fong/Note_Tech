# Linux - Network: FTP

[Back](../../index.md)

- [Linux - Network: FTP](#linux---network-ftp)
  - [FTP](#ftp)
  - [Server side: Package `vsftpd`](#server-side-package-vsftpd)
  - [Client Side: Package `ftp`](#client-side-package-ftp)
    - [Command](#command)
  - [Lab: Transfer a File](#lab-transfer-a-file)
    - [Install `vsftpd` on a Server](#install-vsftpd-on-a-server)
    - [Configure FTP settings](#configure-ftp-settings)
    - [Configure firewall for FTP](#configure-firewall-for-ftp)
    - [Create a User on Server(Optional)](#create-a-user-on-serveroptional)
    - [Install FTP client on Client](#install-ftp-client-on-client)
    - [Transfer File](#transfer-file)

---

## FTP

- `FTP (File Transfer Protocol)`
  - a standard network protocol used to transfer files between a client and a server.
- Ports:

  - `21`: Used for FTP **commands** and **control**.
  - `20`: Used for data transfer in **Active Mode**.

- Modes:
  - `Active Mode`: The **server actively connects to the client** for data transfer.
  - `Passive Mode`: The **client establishes the data connection** to the server (used to bypass firewalls).

---

## Server side: Package `vsftpd`

- Install

```sh
# install
sudo yum install -y vsftpd
# Check if install
rpm -qa | grep vsftpd
```

- Configuration File

  - `/etc/vsftpd/vsftpd.conf`

- Service

```sh
sudo systemctl list-unit-files | grep vsftpd
sudo systemctl status vsftpd
```

---

## Client Side: Package `ftp`

- Install

```sh
# install
sudo yum install -y ftp
# Check if install
rpm -qa | grep ftp
```

- Create connection

```sh
ftp remote_ip
# username + pwd
```

---

### Command

- Local Client

| CMD          | DESC                                                             |
| ------------ | ---------------------------------------------------------------- |
| `!`          | Toggles back the OS. Typing `exit` back to the FTP command line. |
| `lcd`        | Displays current directory                                       |
| `lcd /path/` | Change direcotry                                                 |

- Remote Server

| CMD                      | DESC                       |
| ------------------------ | -------------------------- |
| `pwd`                    | Display working directory. |
| `cd`                     | Changes directory.         |
| `ls` / `dir`             | Lists files                |
| `mkdir dirname`          | Make directory.            |
| `rmdir dirname`          | Removes a directory.       |
| `delete file`            | Deletes a file.            |
| `rename oldname newname` | Renames a file.            |

- Connection

| CMD       | DESC                              |
| --------- | --------------------------------- |
| `status`  | Display status of options         |
| `ascii`   | Switches to ASCII mode            |
| `binary`  | Switches to binary transfer mode. |
| `hash`    | Sets hash mark printing on or off |
| `passive` | Toggles passive mode.             |
| `trace`   | Toggles packet tracing.           |
| `verbose` | Sets verbose on or off.           |
| `open`    | Opens address.                    |
| `quit`    | Exits from FTP.                   |

- Transfer

| CMD                | DESC                 |
| ------------------ | -------------------- |
| `put file`         | Send one file.       |
| `send file`        | Send single file.    |
| `mput file1 file2` | Send multiple files. |

---

## Lab: Transfer a File

- Server: Redhat8
- Client/Sender: Redhat8

### Install `vsftpd` on a Server

```sh
# Login as root on the server
su -

# Confirm Internet connection
ping -c3 www.google.com

# update package
dnf upgrade -y
# install package
dnf install -y vsftpd
# verify
rpm -qa | grep vsftpd
# vsftpd-3.0.3-36.el8.x86_64
```

---

### Configure FTP settings

- Disable anonymous login
- Allow ascii upload and download
- Enable FTP banner
- Use local time

```sh
ll /etc/vsftpd/vsftpd.conf
# -rw-------. 1 root root 5039 Apr  6  2023 /etc/vsftpd/vsftpd.conf

# backup original cf
cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.bak

# configure
vi /etc/vsftpd/vsftpd.conf
# anonymous_enable=NO
# ascii_upload_enable=YES
# ascii_download_enable=YES
# ftpd_banner=Welcome to blah FTP service.
# use_localtime=YES

# start service
systemctl start vsftpd
# enable service
systemctl enable vsftpd
# Created symlink /etc/systemd/system/multi-user.target.wants/vsftpd.service → /usr/lib/systemd/system/vsftpd.service.
# confirm
systemctl status vsftpd
# ● vsftpd.service - Vsftpd ftp daemon
#    Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; enabled; vendor pres>
#    Active: active (running) since Sat 2024-12-07 01:05:17 EST; 1min 29s ago
#  Main PID: 6765 (vsftpd)
#     Tasks: 1 (limit: 22890)
#    Memory: 772.0K
#    CGroup: /system.slice/vsftpd.service
#            └─6765 /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf

# Dec 07 01:05:17 rhelhost.localdomain systemd[1]: Starting Vsftpd ftp daemon...
# Dec 07 01:05:17 rhelhost.localdomain systemd[1]: Started Vsftpd ftp daemon.
```

---

### Configure firewall for FTP

```sh
# Get firewall statud
firewall-cmd --state
# running

# list all rules
firewall-cmd --list-all
# ports:

# Add port 21 and 20
firewall-cmd --permanent --add-port=21/tcp --add-port=20/tcp
# success

# reload
firewall-cmd --reload
# success
# Confirm
firewall-cmd --list-all
# ports: 21/tcp 20/tcp
```

---

### Create a User on Server(Optional)

```sh
su -

useradd ftpuser
passwd ftpuser
```

---

### Install FTP client on Client

```sh
# act root
su -

# check Internet connetivity
ping -c3 google.com

# install package
dnf install -y ftp
# confirm
rpm -qa | grep ftp
# ftp-0.17-78.el8.x86_64
```

---

### Transfer File

- Prepare the target file to be transfered

```sh
# switch regular user
su rheladmin

# create a file to be transfered
cd ~
touch ~/tran_file
ll -tr > ~/tran_file
cat tran_file
# total 0
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Videos
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Templates
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Public
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Pictures
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Music
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Downloads
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Documents
# drwxr-xr-x. 2 rheladmin rheladmin 6 Nov 10 12:49 Desktop
# -rw-rw-r--. 1 rheladmin rheladmin 0 Dec  7 13:26 tran_file

ll -h ~/tran_file
# -rw-rw-r--. 1 rheladmin rheladmin 526 Dec  7 13:26 /home/rheladmin/tran_file
```

- Transfer the target file

```sh
ftp 192.168.204.153
# Connected to 192.168.204.153 (192.168.204.153).
# 220 Welcome to blah FTP service.
# Name (192.168.204.153:rheladmin): ftpuser
# 331 Please specify the password.
# Password:
# 230 Login successful.
# Remote system type is UNIX.
# Using binary mode to transfer files.
# ftp>

# use binary mode
bi
# 200 Switching to Binary mode.

# Enable the progression bar while transfer
hash
# Hash mark printing on (1024 bytes/hash mark).

# show working dir locally
lcd
# Local directory now /home/rheladmin

# Navigate remotely
pwd
# 257 "/home/ftpuser" is the current directory
ls
# 227 Entering Passive Mode (192,168,204,153,147,4).
# 150 Here comes the directory listing.
# 226 Directory send OK.
mkdir clientdir
# 257 "/home/ftpuser/clientdir" created
ls
# 227 Entering Passive Mode (192,168,204,153,238,53).
# 150 Here comes the directory listing.
# drwxr-xr-x    2 1001     1001            6 Dec 07 15:22 clientdir
# 226 Directory send OK.
cd clientdir
# 250 Directory successfully changed.
pwd
# 257 "/home/ftpuser/clientdir" is the current directory

# transfer file
put tran_file
# local: tran_file remote: tran_file
# 227 Entering Passive Mode (192,168,204,153,213,75).
# 150 Ok to send data.
# #
# 226 Transfer complete.
# 40 bytes sent in 0.000108 secs (370.37 Kbytes/sec)

# confirm
pwd
# 257 "/home/ftpuser/clientdir" is the current directory
ls
# 227 Entering Passive Mode (192,168,204,153,100,195).
# 150 Here comes the directory listing.
# -rw-r--r--    1 1001     1001           40 Dec 07 15:24 tran_file
# 226 Directory send OK.

# exit ftp session
quit
# 221 Goodbye.
```

---

[TOP](#linux---network-ftp)
