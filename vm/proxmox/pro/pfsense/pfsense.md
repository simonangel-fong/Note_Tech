# Proxmox - pfSence

[Back](../proxmox.md)

- [Proxmox - pfSence](#proxmox---pfsence)
  - [Prerequisites](#prerequisites)
  - [Samba Service](#samba-service)
  - [PXE](#pxe)

---

## Prerequisites

- Download ISO:
  - https://www.pfsense.org/download/
- Upload ISO to Proxmox
- ref: https://docs.netgate.com/pfsense/en/latest/recipes/virtualize-proxmox-ve.html

---

```sh
iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o wlp7s0 -j MASQUERADE
# iptables -t nat -D POSTROUTING -s 192.168.200.0/24 -o wlp7s0 -j MASQUERADE
iptables -A FORWARD -s 192.168.200.0/24 -o wlp7s0 -j ACCEPT
# iptables -D FORWARD -s 192.168.200.0/24 -o wlp7s0 -j ACCEPT
iptables -A FORWARD -d 192.168.200.0/24 -m state --state ESTABLISHED,RELATED -i wlp7s0 -j ACCEPT
# iptables -D FORWARD -d 192.168.200.0/24 -m state --state ESTABLISHED,RELATED -i wlp7s0 -j ACCEPT

iptables -t nat -A PREROUTING -i wlp7s0 -p tcp --dport 9443 -j DNAT --to-destination 192.168.200.11:443
# iptables -t nat -D PREROUTING -i wlp7s0 -p tcp --dport 9443 -j DNAT --to-destination 192.168.200.11:443
iptables -A FORWARD -p tcp -d 192.168.200.11 --dport 443 -j ACCEPT
# iptables -D FORWARD -p tcp -d 192.168.200.11 --dport 80 -j ACCEPT

# confirm
iptables -t nat -L -v -n | grep 192.168.200.0
iptables -t nat -L PREROUTING -v -n | grep 192.168.200.11
iptables -L FORWARD -v -n --line-numbers | grep 192.168.200

netfilter-persistent save
```

```sh
iptables -t nat -F
iptables -F FORWARD

iptables -t nat -A POSTROUTING -s vmbr0.100 -o wlp7s0 -j MASQUERADE

iptables -A FORWARD -s vmbr0.100 -o wlp7s0 -j ACCEPT
iptables -A FORWARD -i wlp7s0 -o vmbr0.100@vmbr0 -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o wlp7s0 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o wlp7s0 -j SNAT --to-source 192.168.1.80
iptables -A FORWARD -d 192.168.100.0/24 -m state --state ESTABLISHED,RELATED -i wlp7s0 -j ACCEPT

iptables -t nat -L -v -n | grep 192.168.100
iptables -t nat -L PREROUTING -v -n | grep 192.168.100.1
iptables -L FORWARD -v -n --line-numbers | grep 192.168.200
```

https://192.168.1.80:9443

---

```sh
# on proxmox host


# Flush (clear) all NAT table rules
iptables -t nat -F

# Flush (clear) all FORWARD chain rules
iptables -F FORWARD

# NAT Rule 1: Masquerade packets from 192.168.100.0/24 going out via wifi interface (wlp7s0)
# This hides internal IP addresses by replacing the source IP with the outgoing interface IP.
iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o wlp7s0 -j MASQUERADE

# NAT Rule 2: SNAT packets from 192.168.100.0/24 to appear as coming specifically from 192.168.1.80 (Proxmox host IP)
# More control than MASQUERADE (static source IP).
iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o wlp7s0 -j SNAT --to-source 192.168.1.80

# Allow forwarding: Permit traffic from 192.168.100.0/24 to wlp7s0 (outbound)
iptables -A FORWARD -s 192.168.100.0/24 -o wlp7s0 -j ACCEPT

# Allow forwarding: Permit response traffic from wlp7s0 back to 192.168.100.0/24 (inbound)
iptables -A FORWARD -d 192.168.100.0/24 -i wlp7s0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Save iptables rules to persist after reboot
netfilter-persistent save
```

- On pfSense host

```sh
# install qemu
pkg install qemu-guest-agent

# enable
sysrc qemu_guest_agent_enable="YES"
# confirm
cat /etc/rc.conf
```

---

## Samba Service

```sh
sudo dnf install samba samba-client samba-common

sudo mkdir -p /srv/samba/shared
sudo chown nobody:nobody /srv/samba/shared
sudo chmod 0777 /srv/samba/shared

sudo cat > /etc/samba/smb.conf<<EOF
[Shared]
path = /srv/samba/shared
browsable = yes
writable = yes
guest ok = no
read only = no
valid users = sambauser
EOF

sudo useradd -s /sbin/nologin sambauser
sudo smbpasswd -a sambauser

sudo firewall-cmd --permanent --add-service=samba
sudo firewall-cmd --reload

sudo systemctl enable --now smb nmb

sudo semanage fcontext -a -t samba_share_t '/srv/samba/shared(/.*)?'
sudo restorecon -Rv /srv/samba/shared

smbclient //192.168.10.101/Shared -N
```

- Nat

```sh

sudo iptables -t nat -A PREROUTING -i <physical_nic> -d 192.168.1.80 -p tcp --dport 137:139 -j DNAT --to-destination 192.168.100.50
sudo iptables -t nat -A PREROUTING -i <physical_nic> -d 192.168.1.80 -p udp --dport 137:139 -j DNAT --to-destination 192.168.100.50
sudo iptables -t nat -A PREROUTING -i <physical_nic> -d 192.168.1.80 -p tcp --dport 445 -j DNAT --to-destination 192.168.100.50
sudo iptables -t nat -A POSTROUTING -o vmbr0.100 -j MASQUERADE
sudo iptables -A FORWARD -i <physical_nic> -o vmbr0.100 -j ACCEPT
sudo iptables -A FORWARD -i vmbr0.100 -o <physical_nic> -j ACCEPT
```

---

```sh
iptables -t nat -F
iptables -F FORWARD

# map interface
iptables -t nat -A POSTROUTING -s 192.168.10.0/24 -o wlp7s0 -j MASQUERADE
iptables -A FORWARD -i vmbr0 -o wlp7s0 -j ACCEPT
iptables -A FORWARD -i wlp7s0 -o vmbr0 -m state --state RELATED,ESTABLISHED -j ACCEPT


# Save iptables rules to persist after reboot
netfilter-persistent save
```

- SSH

```sh
# Port 1445 on Proxmox → Forward to 192.168.10.254:445 (SMB)
iptables -t nat -A PREROUTING -i wlp7s0 -p tcp --dport 1445 -j DNAT --to-destination 192.168.10.254:445
iptables -A FORWARD -i wlp7s0 -p tcp --dport 1445 -d 192.168.10.254 -j ACCEPT

# Port 1139 on Proxmox → Forward to 192.168.10.254:139 (NetBIOS Session Service)
iptables -t nat -A PREROUTING -i wlp7s0 -p tcp --dport 1139 -j DNAT --to-destination 192.168.10.254:139
iptables -A FORWARD -i wlp7s0 -p tcp --dport 1139 -d 192.168.10.254 -j ACCEPT

# DNAT: Forward 1445 to pfSense WAN
iptables -t nat -A PREROUTING -i wlp7s0 -p tcp --dport 445 -j DNAT --to-destination 192.168.10.254:445
iptables -A FORWARD -i wlp7s0 -o vmbr0 -p tcp --dport 445 -d 192.168.10.254 -j ACCEPT

# DNAT: Forward 1139 to pfSense WAN
iptables -t nat -A PREROUTING -i wlp7s0 -p tcp --dport 139 -j DNAT --to-destination 192.168.10.254:139
iptables -A FORWARD -i wlp7s0 -o vmbr0 -p tcp --dport 139 -d 192.168.10.254 -j ACCEPT

```

---

## PXE

```sh
dnf upgrade -y
dnf clean all

dnf install -y httpd

mkdir -vp /var/www/html/rhel9
mount -o ro /dev/sr0 /var/www/html/rhel9/

firewall-cmd --permanent --add-service=http
firewall-cmd --reload

http://192.168.100.50/rhel9


dnf install -y tftp-server


# ===== EFI Configuration
# copy boot image files
mkdir -pv /var/lib/tftpboot/rhel9/pxelinux
cp -rv /var/www/html/rhel9/EFI/ /var/lib/tftpboot/rhel9
cp -v /var/www/html/rhel9/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/rhel9/pxelinux

# Replace the PXE boot menu file for EFI
tee /var/lib/tftpboot/rhel9/EFI/BOOT/grub.cfg <<EOF
set default="1"

set timeout=120
menuentry 'Install Oracle Linux 8.10.0' {
  linux rhel9/pxelinux/vmlinuz ip=dhcp inst.repo=http://192.168.100.50/rhel9/
  # linuxefi rhel9/pxelinux/vmlinuz ip=dhcp inst.repo=http://192.168.100.50/rhel9/ quiet
  initrd rhel9/pxelinux/initrd.img
  # initrdefi rhel9/pxelinux/initrd.img
}
EOF

# ===== BIOS Configuration
# download and Copy PXELINUX bootloader files
dnf install -y syslinux
cp -v /usr/share/syslinux/* /var/lib/tftpboot/rhel9/pxelinux
# create cf
mkdir -v /var/lib/tftpboot/rhel9/pxelinux/pxelinux.cfg
cat > /var/lib/tftpboot/rhel9/pxelinux/pxelinux.cfg/default <<EOF
default vesamenu.c32
prompt 1
timeout 600

display boot.msg

label linux
  menu label ^Install system
  menu default
  kernel vmlinuz
  append initrd=initrd.img ip=dhcp inst.repo=http://192.168.100.50/rhel9/

label vesa
  menu label Install system with ^basic video driver
  kernel vmlinuz
  append initrd=initrd.img ip=dhcp inst.xdriver=vesa nomodeset inst.repo=http://192.168.100.50/rhel9/

label rescue
  menu label ^Rescue installed system
  kernel vmlinuz
  append initrd=initrd.img inst.rescue inst.repo=http://192.168.100.50/rhel9/

label local
  menu label Boot from ^local drive
  localboot 0xffff
EOF

chmod -R 755 /var/lib/tftpboot/rhel9/

# Start and enable the TFTP service:
systemctl enable --now tftp.socket

# Allow TFTP traffic through the firewall
firewall-cmd --permanent --add-service=tftp
firewall-cmd --reload

# confirm
firewall-cmd --list-services
```
