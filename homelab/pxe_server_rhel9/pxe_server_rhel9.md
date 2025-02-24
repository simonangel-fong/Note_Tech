# Configure PXE Server on RHEL9

[Back](../index.md)

- [Configure PXE Server on RHEL9](#configure-pxe-server-on-rhel9)
  - [PXE Server](#pxe-server)
  - [Configuration](#configuration)
    - [Prerequisites: Network](#prerequisites-network)
    - [Configuring the DHCPv4 Server](#configuring-the-dhcpv4-server)
    - [Configuring a TFTP server for UEFI-based clients](#configuring-a-tftp-server-for-uefi-based-clients)

---

## PXE Server

---

## Configuration

- Ref:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/interactively_installing_rhel_over_the_network/preparing-to-install-from-the-network-using-http_rhel-installer#preparing-to-install-from-the-network-using-http_rhel-installer

### Prerequisites: Network

- **IPv4 address**
  - `192.168.128.10/24`
- **IPv4 gateway**
  - `192.168.128.2`
- **IPv4 dns**
  - `192.168.128.2`

```sh
# create networkmanager profile
nmcli d
# DEVICE  TYPE      STATE                   CONNECTION
# ens160  ethernet  connected               ens160

nmcli c down ens160
nmcli c modify ens160 connection.id lan_con
nmcli c modify lan_con ipv4.addresses 192.168.128.10/24
nmcli c modify lan_con ipv4.dns 192.168.128.2
nmcli c modify lan_con ipv4.gateway 192.168.128.2
nmcli c modify lan_con ipv4.method manual

nmcli c up lan_con

hostnamectl set-hostname pxe-server.com

echo "192.168.128.10 pxe-server.com pxe-server" >> /etc/hosts

yum install -y vsftpd httpd syslinux

mv -v /etc/dnsmasq.conf /etc/dnsmasq.conf.bak

cat > /etc/dnsmasq.conf<<EOF
interface=ens160
bind-interfaces
domain=pxe-server.com
dhcp-range=ens160,192.168.128.100,192.168.128.200,255.0.0.0,8h
dhcp-option=option:router,192.168.128.2
dhcp-option=option:dns-server,192.168.128.2
dhcp-option=option:dns-server,8.8.8.8
enable-tftp
tftp-root=/netboot/tftp
dhcp-boot=pxelinux.0,linuxhint-s80,192.168.128.2
pxe-promt="Press F8 For PXE Network boot.",10
pxe-service=x86PC,"Install RHEL-9 OS via PXE Server",pxelinux
EOF

mkdir -pv /netboot/tftp/pxelinux.cfg

cp -v /usr/share/syslinux/{pxelinux.0,menu.c32,ldlinux.c32,libutil.c32} /netboot/tftp/

ln -s /var/www/html/ /netboot/www

systemctl enable --now httpd

mkdir -v /netboot/tftp/rhel9
mkdir -v /netboot/www/rhel9

cp -rvf /rhel9_iso/* /netboot/www/rhel9

cp -v /netboot/www/rhel9/images/pxeboot/{initrd.img,vmlinuz} /netboot/tftp/rhel9

cat > /netboot/tftp/pxelinux.cfg/default<<EOF
default menu.c32
label install_rhel-9
menu label ^Install RHEL 9
menu default
kernel rhel9/vmlinux
append initrd=rhel9/initrd.img ip=dhcp inst.repo=http://192.168.128.10/rhel9
EOF

systemctl restart httpd
systemctl restart dnsmasq


```

- Update pacakges

```sh
dnf upgrade -y
```

---

### Configuring the DHCPv4 Server

- Enable the DHCP version 4 (DHCPv4) service on your server, so that it can provide network boot functionality.

```sh
dnf install dhcp-server -y

# Edit the DHCP configuration file:
cat > /etc/dhcp/dhcpd.conf << EOF
option architecture-type code 93 = unsigned integer 16;

subnet 192.168.128.0 netmask 255.255.255.0 {
  option routers 192.168.128.2;
  option domain-name-servers 192.168.128.2;
  range 192.168.128.100 192.168.128.200;
  class "pxeclients" {
    match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
    next-server 192.168.128.30;
          if option architecture-type = 00:07 {
            filename "redhat/EFI/BOOT/BOOTX64.EFI";
          }
          else {
            filename "pxelinux/pxelinux.0";
          }
  }
  class "httpclients" {
    match if substring (option vendor-class-identifier, 0, 10) = "HTTPClient";
    option vendor-class-identifier "HTTPClient";
    filename "http://192.168.128.3/redhat/EFI/BOOT/BOOTX64.EFI";
  }
}
EOF

# Enable and Start the DHCP Service
systemctl enable --now dhcpd
systemctl status dhcpd

# Allow DHCP Traffic in the Firewall
firewall-cmd --permanent --add-service=dhcp
firewall-cmd --reload
firewall-cmd --list-services
# cockpit dhcp dhcpv6-client ssh
```

---


### Configuring a TFTP server for UEFI-based clients

- The TFTP (Trivial File Transfer Protocol) server is required to serve the PXE bootloader files to the client.

```sh
dnf install -y tftp-server

# Allow incoming connections to the tftp service in the firewall:
firewall-cmd --permanent --add-service=tftp
firewall-cmd --reload
firewall-cmd --list-service
# cockpit dhcp dhcpv6-client ssh tftp

# create mount poit
mkdir /rhel9

# Access the EFI boot image files from the DVD ISO image:
mount -o loop,ro -t iso9660 /dev/sr0 /rhel9
df -Th /rhel9
# Filesystem     Type     Size  Used Avail Use% Mounted on
# /dev/loop0     iso9660  9.9G  9.9G     0 100% /rhel9

# Copy the EFI boot images from the DVD ISO image:
mkdir /var/lib/tftpboot/redhat
cp -r /rhel9/EFI /var/lib/tftpboot/redhat/
chmod -R 755 /var/lib/tftpboot/redhat

umount /rhel9

# Replace the content of /var/lib/tftpboot/redhat/efi/boot/grub.cfg
cat > /var/lib/tftpboot/redhat/EFI/BOOT/grub.cfg <<EOF
set timeout=60
menuentry 'RHEL 9' {
  linux images/RHEL-9/vmlinuz ip=dhcp inst.repo=http://192.168.128.10/redhat/iso
  initrd images/RHEL-9/initrd.img
}
EOF


# Create a subdirectory to store the boot image files in the /var/lib/tftpboot/ directory, and copy the boot image files to the directory. In this example, the directory is /var/lib/tftpboot/images/RHEL-9/:
mkdir -p /var/lib/tftpboot/images/RHEL-9/
cp /rhel9/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/images/RHEL-9/

# Start and enable the tftp.socket service:
systemctl enable --now tftp.socket
```

---

- Configure NFS

```sh
dnf upgrade -y
dnf install nfs-utils -y

firewall-cmd --add-service nfs --permanent

# Create a directory to store the ISO image
mkdir -p /var/nfs-exports/ISOs
echo "/var/nfs-exports/ISOs   192.168.128.0/24(ro)" >> /etc/exports

exportfs -rv
# exporting 192.168.128.0/24:/var/nfs-exports/ISOs

systemctl enable --now nfs-server


# Extract the downloaded ISO image to a subdirectory of the NFS share directory
mkdir /ol8_iso
mount -o ro /dev/sr0 /ol8_iso

mkdir -v /var/nfs-exports/ISOs/ol8
cp -a /ol8_iso/* /var/nfs-exports/ISOs/ol8
```

- Configure dnsmasq

```sh

cat > /etc/dnsmasq.conf<<EOF
interface=ens160
dhcp-range=192.168.128.101,192.168.128.200,8h
# dhcp-host=80:00:27:c6:a1:16,192.168.128.253,svr1,infinite
# BIOS-based clients
dhcp-boot=pxelinux/pxelinux.0
# UEFI-based clients
dhcp-boot=tag:efi-x86_64,shim.efi
dhcp-match=set:efi-x86_64,option:client-arch,8

enable-tftp
tftp-root=/var/lib/tftpboot
EOF

vi /etc/resolv.conf
nameserver 127.0.0.1
nameserver 192.168.128.2

sudo firewall-cmd --add-service=dns --permanent


systemctl enable --now dnsmasq
```

- Configure for BIOS-based PXE Clients

```sh
dnf install syslinux -y
mkdir -pv /var/lib/tftpboot/pxelinux/pxelinux.cfg

cp /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot/pxelinux
cp /var/nfs-exports/ISOs/ol8/vmlinuz /var/lib/tftpboot/pxelinux/vmlinuz
cp /var/nfs-exports/ISOs/ol8/initrd.img /var/lib/tftpboot/pxelinux/initrd.img
```
