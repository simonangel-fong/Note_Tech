# !Linux - Storage: SMB

[Back](../../index.md)

- [!Linux - Storage: SMB](#linux---storage-smb)
  - [`Server Message Block (SMB)`](#server-message-block-smb)
  - [Package `Samba`](#package-samba)
  - [Configure Samba Server](#configure-samba-server)
  - [Access: Windows Clients](#access-windows-clients)
  - [Access: Linux Clients](#access-linux-clients)

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

## Configure Samba Server

```sh
# install package
dnf install samba samba-client samba-common -y

# backup original cf
mv /etc/samba/smb.conf /etc/samba/smb.conf.bk

# create global conf
cat > /etc/samba/smb.conf <<EOF
[global]
workgroup = WORKGROUP
server string = Samba Server
netbios name = samba_server
security = user
map to guest = Bad User
name resolve order = bcast host
dns proxy = no
# Restrict Access
hosts allow = 192.168.128.0/24
# Enable logging
log file = /var/log/samba/%m.log
max log size = 50
encrypt passwords = yes

include = /etc/samba/shares.conf
EOF

# create shared conf
cat > /etc/samba/shares.conf <<EOF
[Public Files]
path = /samba/public
force user = smbuser
force group = smbgroup
create mask = 0664
force create mode = 0664
directory mask = 0775
force directory mode = 0775
public = yes
writable = yes

[Protected Files]
path = /samba/protected
force user = smbuser
force group = smbgroup
create mask = 0664
force create mode = 0664
directory mask = 0775
force directory mode = 0775
public = yes
writable = no
EOF

# confirm
testparm

# create user and group
groupadd --system smbgroup
useradd --system --no-create-home --group smbgroup -s /bin/false smbuser

# add pwd to user
smbpasswd -a smbuser
smbpasswd -e smbuser

# Create dir for share
mkdir -vp /samba/public
mkdir -vp /samba/protected

# change ownership
chown -R smbuser:smbgroup /samba
# set permission
chmod -R g+w /samba

# selinux
semanage fcontext -a -t samba_share_t "/samba(/.*)?"
restorecon -Rv /samba

# enable service
systemctl enable --now smb nmb
# confirm
systemctl status smb nmb


# Enable samba in firewall
firewall-cmd --permanent --zone=public --add-service=samba
# reload firewall
firewall-cmd --reload
# Confirm
firewall-cmd --list-service
```

---

## Access: Windows Clients

- Open File Explorer.
- Enter `\\samba_server_ip` in the address bar.
- Browse and access the shared resources.

---

## Access: Linux Clients

| CMD                                                                                             | DESC                              |
| ----------------------------------------------------------------------------------------------- | --------------------------------- |
| `smbclient -L //samba_server_ip`                                                                | List available shares on a server |
| `smbclient //samba_server_ip/shared -U username`                                                | Access a Samba share              |
| `sudo mount -t cifs //samba_server_ip/shared /mnt/samba -o username=username,password=password` | Mount a Samba share:              |

---
