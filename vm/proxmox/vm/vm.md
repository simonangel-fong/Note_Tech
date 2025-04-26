# Proxmox - Virtual Machine

[Back](../proxmox.md)

- [Proxmox - Virtual Machine](#proxmox---virtual-machine)
  - [ISO Image](#iso-image)
  - [Create Virtual Machine - Ubuntu](#create-virtual-machine---ubuntu)
    - [Start VM: Linux](#start-vm-linux)
    - [Configure SSH Connection](#configure-ssh-connection)
  - [Create Virtual Machine: Windows](#create-virtual-machine-windows)
    - [Start Virtual Machine: Windows](#start-virtual-machine-windows)
    - [Configure Remote Desktop](#configure-remote-desktop)
  - [Remove VM](#remove-vm)
  - [Virtual Machine Template](#virtual-machine-template)
    - [Configure Template VM and Create Template](#configure-template-vm-and-create-template)
    - [Good Practices](#good-practices)
    - [Create VM by cloning Template](#create-vm-by-cloning-template)

---

## ISO Image

- Ubuntu ISO Download link:

  - https://releases.ubuntu.com/24.04.2/ubuntu-24.04.2-live-server-amd64.iso?_gl=1*ixii2c*_gcl_au*MTM5ODE4MjYwMy4xNzQ1NDM0MjE4

- Dowload Ubuntu ISO from URL

![pic](./pic/iso01.png)

![pic](./pic/iso02.png)

![pic](./pic/iso03.png)

![pic](./pic/iso04.png)

---

## Create Virtual Machine - Ubuntu

- General
  - Node: select the node
  - VM ID: unique
  - Name

![pic](./pic/create_vm01.png)

- OS
  - Select ISO

![pic](./pic/create_vm02.png)

![pic](./pic/create_vm03.png)

- Disk
  - specify the size

![pic](./pic/create_vm04.png)

- CPU
  - assign 1, then ajust the number of cores based on the cpu usage of the application

![pic](./pic/create_vm05.png)

- Memory
  - at least 1 Gib
  - memory size for each VM is limited by the total memory size

![pic](./pic/create_vm06.png)

- Network

![pic](./pic/create_vm07.png)

- Confirm

![pic](./pic/create_vm08.png)

---

### Start VM: Linux

![pic](./pic/vm_start01.png)

![pic](./pic/vm_start02.png)

- Configure network
  - Ip within the vLan

![pic](./pic/vm_start03.png)

![pic](./pic/vm_start04.png)

- Test network

```sh
ping 8.8.8.8
ping google.ca
sudo apt-get update
```

![pic](./pic/vm_start04.png)

---

### Configure SSH Connection

- On `Proxmox` Host create NAT port forwarding rules

```sh
# Inbound port forwarding for SSH traffic
# redirects incoming TCP traffic on port 2222 (via interface wlp7s0) to port 22 on IP 192.168.100.10 within the VLAN
iptables -t nat -A PREROUTING -i wlp7s0 -p tcp --dport 2222 -j DNAT --to-destination 192.168.100.10:22

# Outbound forwarding rule to allow SSH traffic to be routed
# permits forwarded TCP traffic destined for 192.168.100.10 on port 22 (SSH) to pass through the system
iptables -A FORWARD -p tcp -d 192.168.100.10 --dport 22 -j ACCEPT

# Delete the Inbound port forwarding rule for 192.168.100.10
# iptables -t nat -D PREROUTING -i wlp7s0 -p tcp --dport 2222 -j DNAT --to-destination 192.168.100.10:22

# Delete the outbound forwarding rule for 192.168.100.10
# iptables -D FORWARD -p tcp -d 192.168.100.10 --dport 22 -j ACCEPT

# Confirm the NAT rules are correctly applied
iptables -t nat -L -v -n
iptables -t nat -L -v -n | grep 192.168.100.10

# Save the iptables rules to make them persistent across reboots
netfilter-persistent save
```

- On the Admin Machine to test SSH connection

```sh
# Test the SSH connection to the forwarded device
ssh -p 2222 vm_container_user@192.168.1.80
```

---

## Create Virtual Machine: Windows

- Prerequisites
  - Download Windows ISO
  - Download Windows Dirver for Proxmox

![pic](./pic/create_vm_win01.png)

![pic](./pic/create_vm_win02.png)

![pic](./pic/create_vm_win03.png)

![pic](./pic/create_vm_win04.png)

![pic](./pic/create_vm_win05.png)

---

### Start Virtual Machine: Windows

![pic](./pic/vm_start_win01.png)

- When the driver is requied, select
  - Browse > Driver ISO > VIOSCSI > Win10 > X86

![pic](./pic/vm_start_win02.png)

![pic](./pic/vm_start_win03.png)

![pic](./pic/vm_start_win04.png)

![pic](./pic/vm_start_win05.png)

- Install driver
  - can select the entire driver ISO to install required driver

![pic](./pic/vm_start_win06.png)

- Configure Network
  - set the subnet based on the virtual network interface

![pic](./pic/vm_start_win07.png)

- Test

![pic](./pic/vm_start_win08.png)

- Install qemu

![pic](./pic/vm_start_win09.png)

- The Creation is finished.

---

### Configure Remote Desktop

- On VM, enable RDP

- On Proxmox host, Create NAT rule for port forwarding

```sh
# Add port forwarding rule
iptables -t nat -A PREROUTING -i wlp7s0 -p tcp --dport 3333 -j DNAT --to-destination 192.168.100.100:3389

# Add Outbound rule
iptables -A FORWARD -p tcp -d 192.168.100.100 --dport 3389 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
# Add Inbound rule
iptables -A FORWARD -p tcp -s 192.168.100.100 --sport 3389 -m state --state ESTABLISHED -j ACCEPT

# confirm
iptables -t nat -L -v -n | grep 192.168.100.100
# 2   104 DNAT       6    --  wlp7s0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:3333 to:192.168.100.100:3389

# persist
netfilter-persistent save
```

- Connect via RDP
  - Computer: 192.168.100.100:3333

![pic](./pic/vm_start_win10.png)

---

## Remove VM

![pic](./pic/remove_vm01.png)

---

## Virtual Machine Template

### Configure Template VM and Create Template

```sh
apt search cloud-init
sudo apt install cloud-init

#  remove ssh host key, since it is different for each host
sudo rm /etc/ssh/ssh_host_*
# truncate the file of machine id
sudo truncate -s 0 /etc/machine-id
# create symbolic link to machine id file if not exests
sudo ln -s /etc/machine-id /var/lib/dbus/machine-id

# confirm
cat /etc/machine-id
ls -l /var/lib/dbus/machine-id

# clears out the local repository
sudo apt clean
# cleans up leftover packages
sudo apt autoremove

# shutdown for tamplate creation
sudo poweroff
```

- Convert to template

![pic](./pic/vm_template01.png)

- Once done, symbol will change

![pic](./pic/vm_template02.png)

---

### Good Practices

- Optional: Good practices operation
- 1. Remove ISO

  - Hardware > Edit CD/DVD > use no media

- 2. Add CloudInit Drive

![pic](./pic/vm_template03.png)

- 3. Edit Cloud-Init
  - Add default user name
  - Add default pwd
  - Set DNS
  - set IP
  - Click Regenerate Image to apply

![pic](./pic/vm_template04.png)

---

### Create VM by cloning Template

![pic](./pic/vm_template05.png)

![pic](./pic/vm_template06.png)

- Start and login new vm

![pic](./pic/vm_template07.png)
