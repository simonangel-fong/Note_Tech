# RHCSA NFS

[Back](../../index.md)

- [RHCSA NFS](#rhcsa-nfs)
  - [Question](#question)
    - [Solution](#solution)
  - [Setup NFS](#setup-nfs)

---

## Question

```conf
Configure autofs to automount the home directories of netuserX user. Note the following:
netuserX home directory is exported via NFS, which is available on classroom.example.com (172.25.254.254)
your NFS-exports directory is /netdir for netuser,
netuserX's home directory is classroom.example.com:/home/guests/netuserX,
netuserX's home directory should be automounted autofs service.
home directories must be writable by their users.
password for netuser is ablerate.
```

---

### Solution

```sh
# install package
yum install -y nfs-utils autofs

showmount -e 192.168.128.50
# Export list for 192.168.128.50:
# /home/guests/netuserX 192.168.128.0/24

# Edit auto fs cf
vi /etc/auto.master
# add entry: mount_point  Map_file
/netdir /etc/auto.misc

# Edit cf misc Map_file
vi /etc/auto.misc
# add entry: mount-point  options  location
netuserX   -fstype=nfs,rw,sync 192.168.128.50:/home/guests/netuserX
# netuserX   -rw,soft,intr 192.168.128.50:/home/guests/netuserX

# reload autofs
systemctl reload autofs
```

---

## Setup NFS

```sh
# install
yum install nfs-utils -y
rpm -qa | grep nfs
# nfs-utils-2.3.3-59.el8.x86_64
# libnfsidmap-2.3.3-59.el8.x86_64
# sssd-nfs-idmap-2.9.4-5.el8_10.1.x86_64

# enable service
systemctl enable --now nfs-server
systemctl status rpcbind
systemctl status nfs-server

# create nfsuser
useradd netuserX
echo "password" | passwd --stdin netuserX

# create shared dir
sudo mkdir -p /home/guests/netuserX
sudo chmod 755 /home/guests
sudo chmod 700 /home/guests/netuserX
sudo chown netuserX:netuserX /home/guests/netuserX
ll -d /home/guests/netuserX/
# drwx------. 2 netuserX netuserX 6 Jan 14 15:27 /home/guests/netuserX/

# Edit the NFS exports file
vi /etc/exports
# /home/guests/netuserX 192.168.128.0/24(rw,sync,no_root_squash)

# Apply the changes
exportfs -r
# Confirm
exportfs -v
# /home/guests/netuserX 192.168.128.0/24(sync,wdelay,hide,no_subtree_check,sec=sys,rw,secure,no_root_squash,no_all_squash)

# Configure firewall
firewall-cmd --permanent --add-service=nfs
firewall-cmd --permanent --add-service=rpc-bind
firewall-cmd --permanent --add-service=mountd
firewall-cmd --reload
# confirm
firewall-cmd --list-all
# services: cockpit dhcpv6-client mountd nfs rpc-bind ssh
```

- Test on Client

```sh
showmount -e 192.168.128.50
# Export list for 192.168.128.50:
# /home/guests/netuserX 192.168.128.0/24
```
