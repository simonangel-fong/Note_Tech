# Hands-on: PXE Installation Server - OEL 8

[Back](../index.md)

- [Hands-on: PXE Installation Server - OEL 8](#hands-on-pxe-installation-server---oel-8)
  - [Configure Server Network](#configure-server-network)
  - [Configure NFS](#configure-nfs)
  - [Configure dnsmasq](#configure-dnsmasq)
  - [Configure for BIOS-based PXE Clients](#configure-for-bios-based-pxe-clients)
  - [Configure for UEFI-based PXE Clients](#configure-for-uefi-based-pxe-clients)
- [Set up a DHCPv4 server](#set-up-a-dhcpv4-server)
- [Handle PXE Clients](#handle-pxe-clients)
- [Defines a DHCP class named "pxeclients" to match devices that send the DHCP vendor-class-identifier as "PXEClient".](#defines-a-dhcp-class-named-pxeclients-to-match-devices-that-send-the-dhcp-vendor-class-identifier-as-pxeclient)
    - [Configuring a TFTP server for BIOS-based clients](#configuring-a-tftp-server-for-bios-based-clients)
  - [Configuring the DHCPv4 server for network boot](#configuring-the-dhcpv4-server-for-network-boot)
    - [Configuring a TFTP server for UEFI-based clients](#configuring-a-tftp-server-for-uefi-based-clients)
    - [Configuring a TFTP server for BIOS-based clients](#configuring-a-tftp-server-for-bios-based-clients-1)

---

- PXE server IP: `192.168.128.30`
- Subnet IP: `192.168.128.0/24`
- Broadcast IP: `192.168.128.255`
- RHEL9 DVD path: `/dev/sr0`
- Mount path: `/mnt`

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
```

---

## Configure NFS

```sh
dnf install nfs-utils -y
firewall-cmd --add-service nfs --permanent
firewall-cmd --reload
firewall-cmd --list-services

mkdir -pv /var/nfs-exports/ISOs/ol8

echo "/var/nfs-exports/ISOs   192.168.128.0/24(ro)" >> /etc/exports
exportfs -rav
# exporting 192.168.128.0/24:/var/nfs-exports/ISOs

systemctl enable --now nfs-server

# copy dvd to disk
# mount -o ro /dev/sr0 /mnt
# cp -av /mnt /var/nfs-exports/ISOs/ol8

mount -o ro /dev/sr0 /var/nfs-exports/ISOs/ol8
```

---

## Configure dnsmasq

```sh
dnf install dnsmasq -y

cat >> /etc/dnsmasq.conf <<EOF
interface=ens160
dhcp-range=192.168.128.100,192.168.128.200,6h

# BIOS Clients Boot File
dhcp-boot=tag:!efi-x86_64,pxelinux/pxelinux.0

# UEFI Clients Boot File
dhcp-match=set:efi-x86_64,option:client-arch,8
dhcp-boot=tag:efi-x86_64,efi/shim.efi

# Define the TFTP Server Address
dhcp-option=66,192.168.128.30

# Network Settings
dhcp-option=3,192.168.128.2   # Gateway
dhcp-option=6,8.8.8.8,8.8.4.4 # DNS

# Enable TFTP
enable-tftp
tftp-root=/var/lib/tftpboot
EOF

firewall-cmd --permanent --add-service=dhcp
firewall-cmd --permanent --add-service=tftp
# firewall-cmd --permanent --add-port=69/udp
# firewall-cmd --permanent --add-port=67/udp
firewall-cmd --permanent --add-port=4011/udp  # PXE boot requests
firewall-cmd --reload
```

---

## Configure for BIOS-based PXE Clients

```sh
dnf install syslinux -y

#
mkdir -p /var/lib/tftpboot/pxelinux/pxelinux.cfg
# Copy the boot loader file to the pxelinux subdirectory
cp /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot/pxelinux

# copy the installation kernel (vmlinuz), and the ram-disk image file (initrd.img) to the pxelinux subdirectory.
cp -v /var/nfs-exports/ISOs/ol8/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/pxelinux/

# Copy the modules for displaying the boot loader as a menu to the boot loader directory
cp /usr/share/syslinux/*.c32 /var/lib/tftpboot/pxelinux

cat > /var/lib/tftpboot/pxelinux/pxelinux.cfg/default<<EOF
DEFAULT menu.c32
TIMEOUT 400
ONTIMEOUT BootLocal
PROMPT 0
NOESCAPE 1

LABEL BootLocal
    localboot 0
    TEXT HELP
    Boot to local hard disk
    ENDTEXT

LABEL OL8
    MENU LABEL OL8
    kernel vmlinuz
    append initrd=initrd.img inst.repo=/var/nfs-exports/ISOs/ol8/ inst.ks.sendmac inst.ks=/var/nfs-exports/ISOs/ksfiles/kstart-file
    TEXT HELP
    Install Oracle Linux 8
    ENDTEXT
EOF
```

---

## Configure for UEFI-based PXE Clients

```sh
# Download the grub2-efi and shim packages
mkdir /tmp/boot_rpms
dnf download shim grub2-efi --downloaddir=/tmp/boot_rpms

# extract their contents
cd /tmp/boot_rpms
rpm2cpio grub2*.rpm | cpio -idmv
rpm2cpio shim*.rpm | cpio -idmv

# Copy the boot loader and other related files to the efi subdirectory
# Create a subdirectory
mkdir -p /var/lib/tftpboot/efi

cp -v /tmp/boot_rpms/boot/efi/EFI/redhat/grubx64.efi /var/lib/tftpboot/efi
cp -v /tmp/boot_rpms/boot/efi/EFI/redhat/MokManager.efi /var/lib/tftpboot/efi
cp -v /tmp/boot_rpms/boot/efi/EFI/redhat/shim*.efi /var/lib/tftpboot/efi
# As a passthrough boot loader, you would then specify shim.efi when setting dhcp-boot for UEFI-based clients in the /etc/dnsmasq.conf file

# From the NFS share directory, copy the installation kernel (vmlinuz) and the ram-disk image file (initrd.img) to the efi subdirectory.
cp -v /var/nfs-exports/ISOs/ol8/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/efi/

# In the efi subdirectory, create and then add entries to the grub.cfg boot loader configuration file.
cat > /var/lib/tftpboot/efi/grub.cfg<<EOF
set default 0
set timeout=10

menuentry 'ol8 localboot' {
echo "Booting from local disk"
set root=(hd0,gpt1)
chainloader efi/shim.efi
boot
}

menuentry 'ol8' {
  echo "Loading vmlinuz"
  linuxefi vmlinuz inst.repo=/var/nfs-exports/ISOs/ol8/ inst.ks.sendmac \
  inst.ks=/var/nfs-exports/ISOs/ksfiles/kstart-file
  echo "Loading /initrd.img"
  initrdefi initrd.img
  echo "Booting installation kernel"
}
EOF

sudo chmod -R 755 /var/lib/tftpboot
sudo chown -R dnsmasq:dnsmasq /var/lib/tftpboot
```

---

dnf install -y dhcp-server

# Set up a DHCPv4 server

cat > /etc/dhcp/dhcpd.conf <<EOF
option architecture-type code 93 = unsigned integer 16;

subnet 192.168.128.0 netmask 255.255.255.0 {
range 192.168.128.100 192.168.128.200;
option routers 192.168.128.2;
option domain-name-servers 192.168.128.2, 8.8.8.8, 8.8.4.4;
option broadcast-address 192.168.128.255;
default-lease-time 600;
max-lease-time 86400;

# Handle PXE Clients

# Defines a DHCP class named "pxeclients" to match devices that send the DHCP vendor-class-identifier as "PXEClient".

class "pxeclients" {
match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
next-server 192.168.128.10; # If the architecture type (option 93) is 00:07, which indicates a UEFI x86_64 system
if option architecture-type = 00:07 {
filename "redhat/EFI/BOOT/BOOTX64.EFI";
} # Otherwise (for legacy BIOS clients)
else {
filename "pxelinux/pxelinux.0";
}
}

    # Handle HTTP Boot Clients
    # Defines a class "httpclients" for clients that request PXE boot over HTTP (HTTPBoot).
    class "httpclients" {
        match if substring (option vendor-class-identifier, 0, 10) = "HTTPClient";
        option vendor-class-identifier "HTTPClient";
        filename "http://192.168.128.10/redhat/iso/EFI/BOOT/BOOTX64.EFI";
    }

}
EOF

systemctl enable --now dhcpd

firewall-cmd --add-service=dhcp --permanent
firewall-cmd --reload
firewall-cmd --list-services

````

---

### Configuring a TFTP server for UEFI-based clients

```sh
dnf install -y tftp-server
firewall-cmd --add-service=tftp --permanent
firewall-cmd --reload
firewall-cmd --list-services

mount -o ro -t iso9660 /dev/sr0 /mnt

mkdir -v /var/lib/tftpboot/redhat
# mkdir: created directory '/var/lib/tftpboot/redhat'
cp -rv /mnt/EFI /var/lib/tftpboot/redhat/

chmod -R 755 /var/lib/tftpboot/redhat/

# Replace the content of /var/lib/tftpboot/redhat/EFI/BOOT/grub.cfg
cat > /var/lib/tftpboot/redhat/EFI/BOOT/grub.cfg <<EOF
set timeout=60
menuentry 'RHEL 9' {
  linux images/RHEL-9/vmlinuz ip=dhcp inst.repo=http://192.168.128.10/redhat/iso/
  initrd images/RHEL-9/initrd.img
}
EOF

# Create a subdirectory to store the boot image files
mkdir -pv /var/lib/tftpboot/images/RHEL-9/
cp -v /mnt/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/images/RHEL-9/

# Start and enable the tftp.socket service:
systemctl enable --now tftp.socket
````

- The PXE boot server is now ready to serve PXE clients.
  - You can start the client, which is the system to which you are installing Red Hat Enterprise Linux, select PXE Boot when prompted to specify a boot source, and start the network installation.

---

### Configuring a TFTP server for BIOS-based clients

```sh
# copy
cp -pr /mnt/AppStream/Packages/syslinux-tftpboot-6.04-0.20.el9.noarch.rpm /root

# Extract the package
rpm2cpio syslinux-tftpboot-6.04-0.20.el9.noarch.rpm | cpio -dimv

# Create a pxelinux/ directory in tftpboot/ and copy all the files from the directory into the pxelinux/ directory:
mkdir /var/lib/tftpboot/pxelinux
cp /root/tftpboot/* /var/lib/tftpboot/pxelinux

# Create the directory pxelinux.cfg/
mkdir /var/lib/tftpboot/pxelinux/pxelinux.cfg
cat > /var/lib/tftpboot/pxelinux/pxelinux.cfg/default <<EOF
default vesamenu.c32
prompt 1
timeout 600

display boot.msg

label linux
  menu label ^Install system
  menu default
  kernel images/RHEL-9/vmlinuz
  append initrd=images/RHEL-9/initrd.img ip=dhcp inst.repo=http://192.168.128.10/redhat/iso

label vesa
  menu label Install system with ^basic video driver
  kernel images/RHEL-9/vmlinuz
  append initrd=images/RHEL-9/initrd.img ip=dhcp inst.xdriver=vesa nomodeset inst.repo=http://192.168.128.10/redhat/iso

label rescue
  menu label ^Rescue installed system
  kernel images/RHEL-9/vmlinuz
  append initrd=images/RHEL-9/initrd.img inst.rescue
  inst.repo=http://192.168.128.10/redhat/iso

label local
  menu label Boot from ^local drive
  localboot 0xffff
EOF

# Create a subdirectory to store the boot image files in the /var/lib/tftpboot/ directory, and copy the boot image files to the directory. In this example, the directory is /var/lib/tftpboot/pxelinux/images/RHEL-9/
mkdir -pv /var/lib/tftpboot/pxelinux/images/RHEL-9/
cp -v /mnt/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/pxelinux/images/RHEL-9/

```

---

## Configuring the DHCPv4 server for network boot

```sh
dnf install -y dhcp-server

# Set up a DHCPv4 server

cat > /etc/dhcp/dhcpd.conf <<EOF
option architecture-type code 93 = unsigned integer 16;

subnet 192.168.128.0 netmask 255.255.255.0 {
  range 192.168.128.100 192.168.128.200;
  option routers 192.168.128.2;
  option domain-name-servers 192.168.128.2, 8.8.8.8, 8.8.4.4;
  option broadcast-address 192.168.128.255;
  default-lease-time 600;
  max-lease-time 86400;

  # Handle PXE Clients
  # Defines a DHCP class named "pxeclients" to match devices that send the DHCP vendor-class-identifier as "PXEClient".
  class "pxeclients" {
    match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
    next-server 192.168.128.10;
        # If the architecture type (option 93) is 00:07, which indicates a UEFI x86_64 system
        if option architecture-type = 00:07 {
            filename "redhat/EFI/BOOT/BOOTX64.EFI";
        }
        # Otherwise (for legacy BIOS clients)
        else {
            filename "pxelinux/pxelinux.0";
        }
  }

    # Handle HTTP Boot Clients
    # Defines a class "httpclients" for clients that request PXE boot over HTTP (HTTPBoot).
    class "httpclients" {
        match if substring (option vendor-class-identifier, 0, 10) = "HTTPClient";
        option vendor-class-identifier "HTTPClient";
        filename "http://192.168.128.10/redhat/iso/EFI/BOOT/BOOTX64.EFI";
    }
}
EOF

systemctl enable --now dhcpd

firewall-cmd --add-service=dhcp --permanent
firewall-cmd --reload
firewall-cmd --list-services
```

---

### Configuring a TFTP server for UEFI-based clients

```sh
dnf install -y tftp-server
firewall-cmd --add-service=tftp --permanent
firewall-cmd --reload
firewall-cmd --list-services

mount -o ro -t iso9660 /dev/sr0 /mnt

mkdir -v /var/lib/tftpboot/redhat
# mkdir: created directory '/var/lib/tftpboot/redhat'
cp -rv /mnt/EFI /var/lib/tftpboot/redhat/

chmod -R 755 /var/lib/tftpboot/redhat/

# Replace the content of /var/lib/tftpboot/redhat/EFI/BOOT/grub.cfg
cat > /var/lib/tftpboot/redhat/EFI/BOOT/grub.cfg <<EOF
set timeout=60
menuentry 'RHEL 9' {
  linux images/RHEL-9/vmlinuz ip=dhcp inst.repo=http://192.168.128.10/redhat/iso/
  initrd images/RHEL-9/initrd.img
}
EOF

# Create a subdirectory to store the boot image files
mkdir -pv /var/lib/tftpboot/images/RHEL-9/
cp -v /mnt/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/images/RHEL-9/

# Start and enable the tftp.socket service:
systemctl enable --now tftp.socket
```

- The PXE boot server is now ready to serve PXE clients.
  - You can start the client, which is the system to which you are installing Red Hat Enterprise Linux, select PXE Boot when prompted to specify a boot source, and start the network installation.

---

### Configuring a TFTP server for BIOS-based clients

```sh
# copy
cp -pr /mnt/AppStream/Packages/syslinux-tftpboot-6.04-0.20.el9.noarch.rpm /root

# Extract the package
rpm2cpio syslinux-tftpboot-6.04-0.20.el9.noarch.rpm | cpio -dimv

# Create a pxelinux/ directory in tftpboot/ and copy all the files from the directory into the pxelinux/ directory:
mkdir /var/lib/tftpboot/pxelinux
cp /root/tftpboot/* /var/lib/tftpboot/pxelinux

# Create the directory pxelinux.cfg/
mkdir /var/lib/tftpboot/pxelinux/pxelinux.cfg
cat > /var/lib/tftpboot/pxelinux/pxelinux.cfg/default <<EOF
default vesamenu.c32
prompt 1
timeout 600

display boot.msg

label linux
  menu label ^Install system
  menu default
  kernel images/RHEL-9/vmlinuz
  append initrd=images/RHEL-9/initrd.img ip=dhcp inst.repo=http://192.168.128.10/redhat/iso

label vesa
  menu label Install system with ^basic video driver
  kernel images/RHEL-9/vmlinuz
  append initrd=images/RHEL-9/initrd.img ip=dhcp inst.xdriver=vesa nomodeset inst.repo=http://192.168.128.10/redhat/iso

label rescue
  menu label ^Rescue installed system
  kernel images/RHEL-9/vmlinuz
  append initrd=images/RHEL-9/initrd.img inst.rescue
  inst.repo=http://192.168.128.10/redhat/iso

label local
  menu label Boot from ^local drive
  localboot 0xffff
EOF

# Create a subdirectory to store the boot image files in the /var/lib/tftpboot/ directory, and copy the boot image files to the directory. In this example, the directory is /var/lib/tftpboot/pxelinux/images/RHEL-9/
mkdir -pv /var/lib/tftpboot/pxelinux/images/RHEL-9/
cp -v /mnt/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/pxelinux/images/RHEL-9/

```

---
