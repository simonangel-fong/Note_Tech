# Hands-on: UEFI HTTP Source

[Back](../index.md)

- [Hands-on: UEFI HTTP Source](#hands-on-uefi-http-source)
  - [UEFI HTTP installation source](#uefi-http-installation-source)

---

## UEFI HTTP installation source

```sh
dnf install -y httpd

mkdir -p /var/www/html/redhat/


# Create a mount point for the ISO file:
mkdir -p /var/www/html/redhat/iso/
mount -o loop,ro -t iso9660 /dev/sr0 /var/www/html/redhat/iso

# Copy the boot loader, kernel, and initramfs from the mounted ISO file into your HTML directory:
cp -rv /var/www/html/redhat/iso/images /var/www/html/redhat/
cp -rv /var/www/html/redhat/iso/EFI /var/www/html/redhat/

chmod 644 /var/www/html/redhat/EFI/BOOT/grub.cfg

cat > /var/www/html/redhat/EFI/BOOT/grub.cfg<< EOF
set default="1"

function load_video {
  insmod efi_gop
  insmod efi_uga
  insmod video_bochs
  insmod video_cirrus
  insmod all_video
}

load_video
set gfxpayload=keep
insmod gzio
insmod part_gpt
insmod ext2

set timeout=60
# END /etc/grub.d/00_header #

search --no-floppy --set=root -l 'RHEL-9-3-0-BaseOS-x86_64'

# BEGIN /etc/grub.d/10_linux #
menuentry 'Install Red Hat Enterprise Linux 9.3' --class fedora --class gnu-linux --class gnu --class os {
    linuxefi ../../images/pxeboot/vmlinuz inst.repo=http://192.168.128.10/redhat/iso quiet
    initrdefi ../../images/pxeboot/initrd.img
}
menuentry 'Test this media & install Red Hat Enterprise Linux 9.3' --class fedora --class gnu-linux --class gnu --class os {
    linuxefi ../../images/pxeboot/vmlinuz inst.repo=http://192.168.128.10/redhat/iso quiet
    initrdefi ../../images/pxeboot/initrd.img
}
submenu 'Troubleshooting -->' {
    menuentry 'Install Red Hat Enterprise Linux 9.3 in text mode' --class fedora --class gnu-linux --class gnu --class os {
   	 linuxefi ../../images/pxeboot/vmlinuz inst.repo=http://192.168.128.10/redhat/iso inst.text quiet
   	 initrdefi ../../images/pxeboot/initrd.img
    }
    menuentry 'Rescue a Red Hat Enterprise Linux system' --class fedora --class gnu-linux --class gnu --class os {
   	 linuxefi ../../images/pxeboot/vmlinuz inst.repo=http://192.168.128.10/redhat/iso inst.rescue quiet
   	 initrdefi ../../images/pxeboot/initrd.img
    }
}
EOF

chmod 755 /var/www/html/redhat/EFI/BOOT/BOOTX64.EFI

# Open ports in the firewall to allow HTTP (80), DHCP (67, 68) and DHCPv6 (546, 547) traffic:
firewall-cmd --permanent --add-port={80/tcp,67/udp,68/udp,546/udp,547/udp}
firewall-cmd --reload

# Make the html directory and its content readable and executable
chmod -cR u=rwX,g=rX,o=rX /var/www/html
# Restore the SELinux context of the html directory
restorecon -FvvR /var/www/html

systemctl enable --now httpd
```