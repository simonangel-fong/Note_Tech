# homelab - Samba

[Back](../../index.md)

- [homelab - Samba](#homelab---samba)
  - [Install and configure Samba](#install-and-configure-samba)
  - [Create resource](#create-resource)
  - [Start service](#start-service)
  - [Security Configuration](#security-configuration)
  - [Access within Windows machine](#access-within-windows-machine)

---

## Install and configure Samba

- Install

```sh
# upgrade
dnf upgrade -y
dnf install samba samba-client samba-common -y
```

- CF

```sh
# backup cf
cp /etc/samba/smb.conf /etc/samba/smb.conf.bak

# edit cf
cat > /etc/samba/smb.conf<<EOF
[global]
server string = Server Host
workgroup = MYWORKGROUP
security = user
map to guest = Bad User
name resolve order = bcast host
dns proxy = no
include = /etc/samba/shares.conf
EOF

# create 2 shares: public and Protected
cat > /etc/samba/shares.conf<<EOF
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
browseable = yes

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
browseable = yes
EOF

# test syntax of cf
testparm
```

---

## Create resource

```sh
# create user and group
groupadd --system smbgroup
useradd --system --no-create-home --group smbgroup -s /bin/false smbuser

# Added user smbuser.
smbpasswd -a smbuser

# create dir
mkdir -p /samba/public_files
mkdir /samba/private_files

# change ownership
chown -R smbuser:smbgroup /samba
# set permission
chmod -R g+w /samba

# Create test file
echo "This is a file in Samba server" > /samba/public_files/testfile
cat /samba/public_files/testfile
```

---

## Start service

```sh
# Start service
systemctl enable --now smb nmb
systemctl status smb nmb
```

---

## Security Configuration

```sh
# Configure SELinux
semanage fcontext -a -t samba_share_t "/samba/public_files(/.*)?"
restorecon -Rv /samba/public_files

semanage fcontext -a -t samba_share_t "/samba/private_files(/.*)?"
restorecon -Rv /samba/private_files

firewall-cmd --permanent --add-service=samba
firewall-cmd --reload
firewall-cmd --list-all
```

---

## Access within Windows machine

Open File Explorer.
Enter \\samba_server_ip in the address bar.
