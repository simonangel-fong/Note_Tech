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
yum install nfs-utils libnfsidmap -y
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
systemctl stop firewalld
systemctl status firewalld
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
