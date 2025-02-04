# Linux - Storage: NFS

[Back](../../index.md)

- [Linux - Storage: NFS](#linux---storage-nfs)
  - [`NFS (Network File System)`](#nfs-network-file-system)
    - [Architecture](#architecture)
    - [Package and Service](#package-and-service)
  - [Server](#server)
  - [Client](#client)
  - [Lab: Create an NFS Server](#lab-create-an-nfs-server)
  - [Lab: Configure NFS Client](#lab-configure-nfs-client)
  - [Package: `AutoFS`](#package-autofs)
    - [Configuration File](#configuration-file)
    - [AutoFS Maps](#autofs-maps)
    - [Lab: Direct Map](#lab-direct-map)
    - [Lab: Indirect map](#lab-indirect-map)
    - [Lab: Auto mounting User Home](#lab-auto-mounting-user-home)

---

## `NFS (Network File System)`

- `NFS (Network File System)`

  - a **distributed file system protocol** that allows systems to **share directories and files over a network** as if they were locally mounted.
  - It was developed by **Sun Microsystems** and is widely used in Linux and Unix environments.

- **Features**
  - **File Sharing**:
    - Enables users to **access and share files across a network**.
  - **Transparency**:
    - Files appear to reside locally, even when they are on a remote server.
  - **Platform Independence**:
    - Allows different operating systems to share files.
  - **Authentication and Security**:
    - Supports features like Kerberos for secure authentication.
  - **Versatility**:
    - Used in small networks as well as large-scale enterprise environments.

---

### Architecture

- **Server:**
  - **Hosts** shared directories and **manages access** to them.
  - Runs the NFS server **daemon** to handle client requests.
- **Client:**
  - **Mounts** the shared directory from the NFS server.
  - **Accesses** files over the network as if they are on the local file system.

---

### Package and Service

- **Package**

```sh
sudo dnf install nfs-utils
rpm -qa | grep nfs-utils
```

- **Services**

```sh
sudo systemctl enable --now nfs-server rpcbind
sudo systemctl status nfs-server

# Test Exported Directories:
showmount -e server_ip
```

---

## Server

- **Configuration Files**: `/etc/exports`

  - contains a list of directories that can be exported to NFS clients.
  - The server automatically exports these directories each time it starts.

- **Format**

```conf
# share_dir client_ip (permissions)
/shared_directory 192.168.1.0/24(rw,sync,no_root_squash)
# share with everyone
/shared_directory *(rw,sync,no_root_squash)
```

- **Permission**

| Permission       | Desc                                |
| ---------------- | ----------------------------------- |
| `rw`             | Read-write access.                  |
| `sync`           | Write changes to disk immediately.  |
| `no_root_squash` | Allows root access from the client. |

- **Check Logs**
  - `/var/log/messages` or `/var/log/syslog`

---

- **Common Commands**

| CMD                | DESC                          |
| ------------------ | ----------------------------- |
| `exportfs -v`      | List all exported directories |
| `sudo exportfs -r` | Apply the changes             |

---

## Client

- **Configuration Files**: `/etc/fstab`
  - a file on client that specifies persistent mounts for NFS shares.
  - Make Mount Persistent

```conf
server_ip:/shared_dir /mount_point nfs defaults 0 0
```

- **Check Logs**
  - `/var/log/messages` or `/var/log/syslog`

---

- **Common Commands**

| CMD                                                    | DESC                |
| ------------------------------------------------------ | ------------------- |
| `sudo mount -t nfs server_ip:/shared_dir /mount_point` | Mount the NFS share |
| `sudo umount /mount_point`                             | Unmount a share     |

---

## Lab: Create an NFS Server

- install packages

```sh
yum install nfs-utils -y
rpm -qa | grep nfs
# nfs-utils-2.3.3-59.el8.x86_64
# libnfsidmap-2.3.3-59.el8.x86_64
# sssd-nfs-idmap-2.9.4-5.el8_10.1.x86_64
```

- Enable service

```sh
systemctl enable rpcbind
systemctl enable nfs-server
systemctl start rpcbind nfs-server rpc-statd nfs-idmapd
```

- Create share resource

```sh
# create dedicated dir for sharing
mkdir /shared_data
chmod 755 /shared_data
# create resource
touch /shared_data/resource
echo "this is resource on server" > /shared_data/resource
```

- Edit exports file

```sh
# backup exports
cp /etc/exports /etc/exports.bak
vi /etc/exports
# /shared_data 192.168.1.0/24(rw,sync,no_root_squash)
```

- Export fs

```sh
exportfs -rv
# exporting 192.168.1.0/24:/shared_data
```

- Disable firewall

```sh
firewall-cmd --permanent --add-service nfs
firewall-cmd --reload
firewall-cmd --list-all
```

---

## Lab: Configure NFS Client

- Install packages

```sh
dnf install nfs-utils rpcbind -y
rpm -qa | grep nfs
# sssd-nfs-idmap-2.9.4-5.el8_10.1.x86_64
# nfs-utils-2.3.3-59.el8.x86_64
# libnfsidmap-2.3.3-59.el8.x86_64
```

- Enable service

```sh
systemctl enable rpcbind
systemctl start rpcbind
systemctl status rpcbind
```

- Stop firewall or iptables

```sh
ps -ef | egrep "firewall|iptable"
# stop firewall
systemctl stop firewalld
systemctl status firewalld
```

- Show available mount from the NFS server

```sh
showmount -e 192.168.1.130
# Export list for 192.168.1.130:
# /shared_data 192.168.1.0/24
```

- mount

```sh
# create mount point
mkdir /mnt/app
mount 192.168.1.130:/shared_data /mnt/app

# verify
df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        1.8G     0  1.8G   0% /dev
# tmpfs                           1.8G     0  1.8G   0% /dev/shm
# tmpfs                           1.8G  9.7M  1.8G   1% /run
# tmpfs                           1.8G     0  1.8G   0% /sys/fs/cgroup
# /dev/mapper/rhel_rhelhost-root   26G  7.9G   19G  31% /
# /dev/nvme0n1p1                 1014M  424M  591M  42% /boot
# tmpfs                           364M   24K  364M   1% /run/user/1001
# 192.168.1.130:/shared_data       26G  7.5G   19G  29% /mnt/app
```

- Manipulate resource from client

```sh
# access to resource
ll /mnt/app
# total 4
# -rw-r--r--. 1 root root 27 Dec 21 00:57 resource

cat /mnt/app/resource
# this is resource on server

# create dir and file
mkdir /mnt/app/client
echo "this is data from client" > /mnt/app/client/test

# verify on server
cat /shared_data/client/test
# this is data from client
```

- unmount
  - kill the seesion working on the nfs before unmounting

```sh
umount /mnt/app
```

- Persist NFS share on client

```sh
echo "192.168.1.130:/shared_data /mnt/app nfs _netdev 0 0"
```

---

## Package: `AutoFS`

- `Auto File System (AutoFS)`

  - a service that mounts and unmounts a share on the clients during runtime as well as system reboots.
  - a client-side service

- With a proper **entry** placed in AutoFS configuration files, the `AutoFS` service **automatically mounts** a share upon detecting an activity in its mount point with a command such as `ls` or `cd`.
- To avoid inconsistencies, mounts managed with `AutoFS` should **not** be mounted or unmounted manually or via the `/etc/fstab` file.

- `maps`
  - NFS shares be defined in text configuration files
  - CF location: `/etc/auto.master.d`
- With AutoFS, a share is **unmounted automatically** if it is not accessed for **five minutes** by **default**.

- `automount`
  - the daemon of AutoFS service
  - invoked at system boot
  - It reads the AutoFS master **map** and creates initial **mount point** entries, but it does not mount any shares yet.
  - When the service **detects** a user activity under a mount point during runtime, it **mounts** the requested file system at that time.
  - If a share remains **idle** for a certain time period, **automount unmounts** it by itself.

---

### Configuration File

- `/etc/autofs.conf`

- Sample:

```conf
[ autofs ]
timeout = 300
browse_mode = no
mount_nfs_default_protocol = 4
[amd]
dismount_interval = 300
```

---

### AutoFS Maps

- 3 common AutoFS map types:
  - `master`
    - location: `/etc/auto.master`
  - `direct`
    - used to **mount shares automatically** on any number of unrelated mount points.
    - always visible to users
    - Local and direct mounted shares can coexist under one parent directory.
  - `indirect`
    - when need to mount all of the shares under one common parent directory.
    - visible only after they have been accessed.
    - Local and indirect mounted shares cannot coexist under the same parent directory.

---

### Lab: Direct Map

```sh
dnf install -y autofs

showmount -e 192.168.128.50
# Export list for 192.168.128.50:
# /home/guests/netuserX 192.168.128.0/24

# create mount point
mkdir /autodir

# add entry in master file
vi /etc/auto.master
/-  /etc/auto.master.d/auto.dir

# create file and map mount point
vi etc/auto.master.d/auto.dir
/autodir 192.168.128.50:/home/guests/netuserX

# confirm autofs running
systemctl status autofs.service -l --no-pager

# confirm
ll /autodir
# total 4
# -rw-r--r--. 1 xanadu xanadu 22 Jan 31 14:21 testfile
```

---

### Lab: Indirect map

```sh
# create mount point
mkdir /indirect

# edit misc file
vi /etc/auto.misc
autoindir 192.168.128.50:/home/guests/netuserX

# confirm
ll /misc/autoindir/
# total 4
# -rw-r--r--. 1 xanadu xanadu 22 Jan 31 14:21 testfile
```

---

### Lab: Auto mounting User Home

- Server:
  - Create user `netuserX` with UID 3000
  - Add home directory `/home/netuserX` to the list of NFS shares.

```sh
useradd -u 3000 netuserX
echo password | passwd --stdin netuserX

# add entry
echo "/home 192.168.128.0/24(rw)" >> /etc/exports

# export all share
exportfs -avr
# exporting 192.168.128.50:/home
# exporting 192.168.128.0/24:/home/guests/netuserX
```

- Client:
  - Create user `netuserX` with UID 3000 and no home dir.
  - Create mount poit `/nfshome`
  - Create indirect map to the remote user home.

```sh
# create user
# -M: no home dir
# -b: specify base dir
useradd netuserX -u 3000 -Mb /nfshome
echo password | passwd --stdin netuserX

# create mount point
mkdir /nfshome

# add entry to master
echo "/nfshome  /etc/auto.master.d/auto.home" >> /etc/auto.master

# create cf
echo "* -rw 192.168.128.50:/home/netuserX" > /etc/auto.master.d/auto.home

# confirm
su - netuserX
pwd
# /nfshome/netuserX
```