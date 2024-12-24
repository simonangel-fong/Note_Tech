# !Linux - Storage: SMB

[Back](../../index.md)

- [!Linux - Storage: SMB](#linux---storage-smb)
  - [`Server Message Block (SMB)`](#server-message-block-smb)
  - [Package `Samba`](#package-samba)
  - [Server](#server)
    - [Package and Service](#package-and-service)
    - [Configuration File](#configuration-file)
    - [Access Control](#access-control)
    - [Commands](#commands)
  - [Lab: Create a Samba Server](#lab-create-a-samba-server)
    - [Install package](#install-package)
    - [Allow Samba through firewall](#allow-samba-through-firewall)
    - [Edit Configuration File and Start Service](#edit-configuration-file-and-start-service)
    - [Create resource](#create-resource)
    - [Access within Windows machine](#access-within-windows-machine)
  - [Lab: Configure a Client Linux machine](#lab-configure-a-client-linux-machine)
    - [Install Package](#install-package-1)
  - [Client](#client)
    - [Package and Service](#package-and-service-1)
    - [Mount Samba](#mount-samba)
    - [Access: Linux Clients](#access-linux-clients)
    - [Access: Windows Clients](#access-windows-clients)

---

## `Server Message Block (SMB)`

- `Server Message Block (SMB)`
  - a network protocol that allows systems on the same network to share resources like files, printers, and serial ports

---

## Package `Samba`

- `Samba`

  - an open-source implementation of the `Server Message Block (SMB)` and `CIFS` protocols.
  - It allows Linux/Unix systems to **share files** and **printers** with **Windows** systems and vice versa.
  - can also act as a **domain controller** or a **member server** in a `Windows Active Directory (AD)` environment.

- Features
  - **SMB Protocol**:
    - **uses the SMB protocol** to provide shared access to files, printers, and other resources over a network.
  - **Client-Server Model**:
    - `Samba` acts as a **server**, providing resources to **Windows** or **Linux/Unix** clients.

---

## Server

### Package and Service

- **Package**

```sh
sudo dnf install samba samba-client samba-common -y
rpm -qa | grep samba
```

- **Services**

```sh
sudo systemctl enable --now smb nmb
sudo systemctl status smb nmb
```

- Allowed through firewall

```sh
# Enable samba in firewall
firewall-cmd --permanent --zone=public --add-service=samba
# reload firewall
firewall-cmd --reload
```

---

### Configuration File

- Path: `/etc/samba/smb.conf`

- Sample:

```conf
[global]
    workgroup = WORKGROUP
    server string = Samba Server
    netbios name = samba_server
    security = user
    map to guest = Bad User
    dns proxy = no
    # Restrict Access
    hosts allow = 192.168.1.0/24
    # Enable logging
    log file = /var/log/samba/%m.log
    max log size = 50

[shared]
    path = /srv/samba/shared
    writable = yes
    guest ok = yes
    read only = no

# Encrypt Passwords
encrypt passwords = yes
```

---

### Access Control

- 1. Create a Shared Directory

```sh
sudo mkdir -p /srv/samba/shared
sudo chmod -R 0777 /srv/samba/shared
```

- 2. Add Samba Users

```sh
sudo smbpasswd -a username
sudo smbpasswd -e username
```

- 3. Restart Samba Services

```sh
# Apply the changes by restarting the Samba services
sudo systemctl restart smb nmb
```

---

### Commands

| CMD                                 | DESC                                             |
| ----------------------------------- | ------------------------------------------------ |
| `pdbedit -L`                        | List Samba Users                                 |
| `testparm`                          | Check the syntax of the /etc/samba/smb.conf file |
| `sudo smbcontrol all reload-config` | Apply changes without restarting the services    |

---

## Lab: Create a Samba Server

### Install package

```sh
# Install package
sudo dnf install samba samba-client samba-common -y
# confirm
rpm -qa | grep samba
# samba-ldb-ldap-modules-4.19.4-6.el8_10.x86_64
# samba-client-4.19.4-6.el8_10.x86_64
# samba-4.19.4-6.el8_10.x86_64
# samba-client-libs-4.19.4-6.el8_10.x86_64
# samba-libs-4.19.4-6.el8_10.x86_64
# samba-common-4.19.4-6.el8_10.noarch
# samba-common-libs-4.19.4-6.el8_10.x86_64
# samba-dcerpc-4.19.4-6.el8_10.x86_64
# samba-common-tools-4.19.4-6.el8_10.x86_64
```

---

### Allow Samba through firewall

```sh
systemctl status firewalld
# ● firewalld.service - firewalld - dynamic firewall daemon
#    Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; vendor preset: enabled)
#    Active: active (running) since Sat 2024-12-21 17:07:18 EST; 10min ago

# Enable samba in firewall
firewall-cmd --permanent --zone=public --add-service=samba
# reload firewall
firewall-cmd --reload

# Confirm
firewall-cmd --list-service
# cockpit dhcpv6-client samba ssh
```

---

### Edit Configuration File and Start Service

```sh

# stop the server
systemctl stop smb
systemctl status smb

# backup cf
cp /etc/samba/smb.conf /etc/samba/smb.conf.bak

# edit cf
vi /etc/samba/smb.conf

[global]
server string = Server Host
workgroup = MYWORKGROUP
security = user
map to guest = Bad User
name resolve order = bcast host
dns proxy = no
include = /etc/samba/shares.conf

# create 2 shares: public and Protected
vi /etc/samba/shares.conf

[Public Files]
path = /samba/public_files
force user = smbuser
force group = smbgroup
create mask = 0664
force create mode = 0664
directory mask = 0775
force directory mode = 0775
public = yes
writable = yes

[Protected Files]
path = /samba/private_files
force user = smbuser
force group = smbgroup
create mask = 0664
force create mode = 0664
directory mask = 0775
force directory mode = 0775
public = yes
writable = no

# test syntax of cf
testparm
# Load smb config files from /etc/samba/smb.conf
# Loaded services file OK.
# Weak crypto is allowed by GnuTLS (e.g. NTLM as a compatibility fallback)

# Server role: ROLE_STANDALONE

# Press enter to see a dump of your service definitions

# # Global parameters
# [global]
#         dns proxy = No
#         map to guest = Bad User
#         name resolve order = bcast host
#         security = USER
#         server string = Server Host
#         workgroup = MYWORKGROUP
#         idmap config * : backend = tdb
#         include = /etc/samba/shares.conf


# [Public Files]
#         create mask = 0664
#         directory mask = 0775
#         force create mode = 0664
#         force directory mode = 0775
#         force group = smbuser
#         force user = smbuser
#         guest ok = Yes
#         path = /samba/public_files
#         read only = No


# [Protected Files]
#         create mask = 0664
#         directory mask = 0775
#         force create mode = 0664
#         force directory mode = 0775
#         force group = smbuser
#         force user = smbuser
#         guest ok = Yes
#         path = /samba/private_files
```

### Create resource

- Create dir for share

```sh
# create dir
mkdir -p /samba/public_files
mkdir /samba/private_files

# create user and group
groupadd --system smbgroup
useradd --system --no-create-home --group smbgroup -s /bin/false smbuser
smbpasswd -a smbuser
# New SMB password:
# Retype new SMB password:
# Added user smbuser.

# confirm
cat /etc/group | grep smbgroup
# smbgroup:x:972:
cat /etc/passwd | grep smbuser
# smbuser:x:975:971::/home/smbuser:/bin/false



# change ownership
chown -R smbuser:smbgroup /samba
# set permission
chmod -R g+w /samba

# confirm
ll -d /samba
# drwxrwxr-x. 4 smbuser smbgroup 47 Dec 22 23:18 /samba
ll /samba
# drwxrwxr-x. 2 smbuser smbgroup 6 Dec 22 23:18 private_files
# drwxrwxr-x. 2 smbuser smbgroup 6 Dec 22 23:18 public_files
```

- Create resource

```sh
echo "This is a file in Samba server" > /samba/shared_data/testfile
cat /samba/shared_data/testfile
# This is a file in Samba server
```

---

- Start service

```sh
# enable service
sudo systemctl enable --now smb nmb
# confirm
sudo systemctl status smb nmb
# ● smb.service - Samba SMB Daemon
#    Loaded: loaded (/usr/lib/systemd/system/smb.service; enabled; vendor preset: disabled)
#    Active: active (running) since Sun 2024-12-22 23:27:49 EST; 10s ago
#      Docs: man:smbd(8)
#            man:samba(7)
#            man:smb.conf(5)
#  Main PID: 5893 (smbd)
#    Status: "smbd: ready to serve connections..."
#     Tasks: 3 (limit: 22890)
#    Memory: 8.3M
#    CGroup: /system.slice/smb.service
#            ├─5893 /usr/sbin/smbd --foreground --no-process-group
#            ├─5895 /usr/sbin/smbd --foreground --no-process-group
#            └─5896 /usr/sbin/smbd --foreground --no-process-group

# Dec 22 23:27:49 serverhost systemd[1]: Starting Samba SMB Daemon...
# Dec 22 23:27:49 serverhost smbd[5893]: [2024/12/22 23:27:49.070187,  0] ../../source3/smbd/server>
# Dec 22 23:27:49 serverhost smbd[5893]:   smbd version 4.19.4 started.
# Dec 22 23:27:49 serverhost smbd[5893]:   Copyright Andrew Tridgell and the Samba Team 1992-2023
# Dec 22 23:27:49 serverhost systemd[1]: Started Samba SMB Daemon.

# ● nmb.service - Samba NMB Daemon
#    Loaded: loaded (/usr/lib/systemd/system/nmb.service; enabled; vendor preset: disabled)
#    Active: active (running) since Sun 2024-12-22 22:58:29 EST; 29min ago
#      Docs: man:nmbd(8)
#            man:samba(7)
#            man:smb.conf(5)
#  Main PID: 5368 (nmbd)
#    Status: "nmbd: ready to serve connections..."
#     Tasks: 1 (limit: 22890)
#    Memory: 3.0M
#    CGroup: /system.slice/nmb.service
#            └─5368 /usr/sbin/nmbd --foreground --no-process-group

# Dec 22 22:58:29 serverhost systemd[1]: Starting Samba NMB Daemon...
# Dec 22 22:58:29 serverhost nmbd[5368]: [2024/12/22 22:58:29.949034,  0] ../../source3/nmbd/nmbd.c>
# Dec 22 22:58:29 serverhost nmbd[5368]:   nmbd version 4.19.4 started.
# Dec 22 22:58:29 serverhost nmbd[5368]:   Copyright Andrew Tridgell and the Samba Team 1992-2023
# Dec 22 22:58:29 serverhost systemd[1]: Started Samba NMB Daemon.
```

---

---

### Access within Windows machine

- Open File Explorer.
- Enter `\\samba_server_ip` in the address bar.

---

## Lab: Configure a Client Linux machine

### Install Package

```sh
sudo dnf install samba-client cifs-utils -y
```

---

## Client

### Package and Service

- Install the Samba client package

```sh
sudo dnf install samba-client cifs-utils
rpm -qa | egrep "samba|cifs"samba-client-libs-4.19.4-6.el8_10.x86_64
# samba-client-4.19.4-6.el8_10.x86_64
# samba-common-libs-4.19.4-6.el8_10.x86_64
# samba-common-4.19.4-6.el8_10.noarch
# cifs-utils-7.0-1.el8.x86_64
```

---

### Mount Samba

```sh
# create mount point
mkdir -p /mnt/samba
# mount samba share
mount -t cifs //192.168.1.130/Public /mnt/samba
# Password for root@//192.168.1.130/Anonymous:
# note: so far no user has been created. So just type ENTER

# Confirm
df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.7M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.5G   19G  29% /
# /dev/nvme0n1p1                 1014M  426M  589M  42% /boot
# tmpfs                           364M   36K  364M   1% /run/user/1000
# tmpfs                           364M  4.0K  364M   1% /run/user/1001
# //192.168.1.130/Anonymous        26G  7.5G   19G  29% /mnt/samba
```

- Manipulate resources in Samba shared

```sh
ll /mnt/samba
```

---

### Access: Linux Clients

| CMD                                                                                             | DESC                              |
| ----------------------------------------------------------------------------------------------- | --------------------------------- |
| `smbclient -L //samba_server_ip`                                                                | List available shares on a server |
| `smbclient //samba_server_ip/shared -U username`                                                | Access a Samba share              |
| `sudo mount -t cifs //samba_server_ip/shared /mnt/samba -o username=username,password=password` | Mount a Samba share:              |

---

### Access: Windows Clients

- Open File Explorer.
- Enter `\\samba_server_ip` in the address bar.
- Browse and access the shared resources.
