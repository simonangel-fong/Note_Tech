# Hands-on: OEL8 PXE Installation Server running RHEL9

[Back](../index.md)

- [Hands-on: OEL8 PXE Installation Server running RHEL9](#hands-on-oel8-pxe-installation-server-running-rhel9)
  - [Diagram](#diagram)
  - [Configure Server Network](#configure-server-network)
  - [Configure HTTP (Enabling Installation Repository)](#configure-http-enabling-installation-repository)
  - [Configure TFTP (PXE Bootloader)](#configure-tftp-pxe-bootloader)
  - [Configure DHCP](#configure-dhcp)
    - [Using `dhcp-server`](#using-dhcp-server)
    - [Using `dnsmasq`](#using-dnsmasq)
  - [Client](#client)
    - [BIOS Method](#bios-method)

---

- PXE server IP: `192.168.128.30`
- Subnet IP: `192.168.128.0/24`
- Broadcast IP: `192.168.128.255`
- RHEL9 DVD path: `/dev/sr0`

## Diagram

![pic](./pic/pxe_diagram.gif)


## Configure Server Network

```sh
nmcli c down ens160
nmcli c modify ens160 ipv4.addresses 192.168.128.10/24
nmcli c modify ens160 ipv4.dns 192.168.128.2
nmcli c modify ens160 ipv4.gateway 192.168.128.2
nmcli c modify ens160 ipv4.method manual
nmcli c modify ens160 connection.autoconnect yes
nmcli c up ens160

hostnamectl set-hostname pxe-server
echo "192.168.128.10 pxe-server" >> /etc/hosts

dnf upgrade -y
dnf clean all
```

---

## Configure HTTP (Enabling Installation Repository)

```sh
# Install the HTTP server
dnf install -y httpd

# mount dvd
mkdir -pv /var/www/html/ol8
mount -o ro /dev/sr0 /var/www/html/ol8/

# Start and enable the HTTP service
systemctl enable --now httpd

# Allow HTTP traffic through the firewall
firewall-cmd --permanent --add-service=http
firewall-cmd --reload

# confirm
firewall-cmd --list-services

# access by
http://192.168.128.10/ol8
```

---

## Configure TFTP (PXE Bootloader)

- The TFTP server is responsible for delivering the PXE bootloader to the client.

```sh
# Install the TFTP server:
dnf install -y tftp-server


# ===== EFI Configuration
# copy boot image files
mkdir -pv /var/lib/tftpboot/ol8/pxelinux
cp -rv /var/www/html/ol8/EFI/ /var/lib/tftpboot/ol8
cp -v /var/www/html/ol8/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/ol8/pxelinux

# Replace the PXE boot menu file for EFI
tee /var/lib/tftpboot/ol8/EFI/BOOT/grub.cfg <<EOF
set default="1"

set timeout=120
menuentry 'Install Oracle Linux 8.10.0' {
  # linux ol8/pxelinux/vmlinuz ip=dhcp inst.repo=http://192.168.128.10/ol8/
  linuxefi ol8/pxelinux/vmlinuz ip=dhcp inst.repo=http://192.168.128.10/ol8/ quiet
  # initrd ol8/pxelinux/initrd.img
  initrdefi ol8/pxelinux/initrd.img
}
EOF

# ===== BIOS Configuration
# download and Copy PXELINUX bootloader files
dnf install -y syslinux
cp -v /usr/share/syslinux/* /var/lib/tftpboot/ol8/pxelinux
# create cf
mkdir -v /var/lib/tftpboot/ol8/pxelinux/pxelinux.cfg
cat > /var/lib/tftpboot/ol8/pxelinux/pxelinux.cfg/default <<EOF
default vesamenu.c32
prompt 1
timeout 600

display boot.msg

label linux
  menu label ^Install system
  menu default
  kernel vmlinuz
  append initrd=initrd.img ip=dhcp inst.repo=http://192.168.128.10/ol8/

label vesa
  menu label Install system with ^basic video driver
  kernel vmlinuz
  append initrd=initrd.img ip=dhcp inst.xdriver=vesa nomodeset inst.repo=http://192.168.128.10/ol8/

label rescue
  menu label ^Rescue installed system
  kernel vmlinuz
  append initrd=initrd.img inst.rescue inst.repo=http://192.168.128.10/ol8/

label local
  menu label Boot from ^local drive
  localboot 0xffff
EOF

# Start and enable the TFTP service:
systemctl enable --now tftp.socket

# Allow TFTP traffic through the firewall
firewall-cmd --permanent --add-service=tftp
firewall-cmd --reload

# confirm
firewall-cmd --list-services
```

---

## Configure DHCP

### Using `dhcp-server`

```sh
# Install the DHCP server
dnf install -y dhcp-server

# Configure DHCP by editing /etc/dhcp/dhcpd.conf:
tee /etc/dhcp/dhcpd.conf <<EOF
option architecture-type code 93 = unsigned integer 16;

subnet 192.168.128.0 netmask 255.255.255.0 {
  range 192.168.128.100 192.168.128.200;
  option routers 192.168.128.2;
  option domain-name-servers 192.168.128.2, 8.8.8.8, 8.8.4.4;
  option broadcast-address 192.168.128.255;
  default-lease-time 600;
  max-lease-time 86400;

  class "pxeclients" {
    match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
    next-server 192.168.128.10;
        if option architecture-type = 00:07 {
            filename "ol8/EFI/BOOT/BOOTX64.EFI";
        }
        # Otherwise (for legacy BIOS clients)
        else {
            filename "ol8/pxelinux/pxelinux.0";
        }

  }

  class "httpclients" {
    match if substring (option vendor-class-identifier, 0, 10) = "HTTPClient";
    option vendor-class-identifier "HTTPClient";
    filename "http://192.168.128.10/ol8/EFI/BOOT/BOOTX64.EFI";
    }
}
EOF

# Start and enable the DHCP service:
systemctl enable --now dhcpd
systemctl restart dhcpd
systemctl status dhcpd

# Allow DHCP traffic through the firewall:
sudo firewall-cmd --permanent --add-service=dhcp
sudo firewall-cmd --reload
# confirm
firewall-cmd --list-services
systemctl status dhcpd
```

---

### Using `dnsmasq`

```sh
# Installing dnsmasq
dnf install -y dnsmasq

# Create soft link of grubx64.efi, which is read during EFI installation, to the tftpboot boot dir
# grub.cfg-C0A880 is for 24 bits of the IP address
# determine the name using journalctl -u dnsmasq -f
ln -s /var/lib/tftpboot/ol8/EFI/BOOT/grubx64.efi /var/lib/tftpboot/grub.cfg-C0A880

# Backup cf

cat > /etc/dnsmasq.conf<<EOF
# Don't function as a DNS server:
port=0

# Log lots of extra information about DHCP transactions.
log-dhcp

# Specify the interface listened on
interface=ens160
# IP address range: start ip,end ip,mask,lease time
dhcp-range=192.168.128.100,192.168.128.200,255.255.255.0,12h

# Enable TFTP
enable-tftp
# specify tftp root
tftp-root=/var/lib/tftpboot/

# BIOS PXE Boot
dhcp-match=set:x86pc,option:client-arch,0
dhcp-boot=tag:x86pc,ol8/pxelinux/pxelinux.0

# UEFI boot settings
dhcp-match=set:efi-x86_64,option:client-arch,7
dhcp-boot=tag:efi-x86_64,ol8/EFI/BOOT/BOOTX64.EFI

EOF

dnsmasq --test

systemctl enable --now dnsmasq

firewall-cmd --permanent --zone=public --add-service=dhcp
firewall-cmd --reload
```

---

## Client

- Power up and select OS to install.

### BIOS Method

