# RHCSA Network

[Back](../../index.md)

- [RHCSA Network](#rhcsa-network)
  - [Qestion](#qestion)
  - [Solution A: nmtui](#solution-a-nmtui)
  - [Solution B: nmcli](#solution-b-nmcli)
  - [Confirm](#confirm)

---

## Qestion

Q1-ServerA-Network Configuration
Configure TCP/IP and "hostname" as following:

```conf
IP ADDRESS = 192.168.128.100
NETMASK = 255.255.255.0
GATEWAY = 192.168.128.2
DNS = 192.168.128.2
Hostname = serverA
```

---

## Solution A: nmtui

- Using nmtui

Solution 1:

Using nmtui
Terminal> nmtui
Select interface > edit >
Select IPv4 configuration: Manual
show >

- Addresses: 192.168.128.100/24
- Gateway: 192.168.128.2
- DNS servers: 192.168.128.2
  OK
  select activation connection
  Set Hostname: serverA
  quit

---

## Solution B: nmcli

- Network

```sh
# check the dev
nmcli d

# modify connection
nmcli c modify ens160 ipv4.addresses 192.168.128.100/24
nmcli c modify ens160 ipv4.gateway 192.168.128.2
nmcli c modify ens160 ipv4.dns 192.168.128.2
nmcli c modify ens160 ipv4.method manual
nmcli c modify ens160 connection.autoconnect yes

# confirm
nmcli c show ens160

# Apply the changes
nmcli c up ens160
```

- Hostname

```sh
hostnamectl set-hostname serverA

# Verify the hostname
hostnamectl status

# Ensure the hostname resolves locally
vi /etc/hosts
# 192.168.128.100 serverA
```

---

## Confirm

```sh
# verify ip addresses
ip a

# hostname
hostname
cat /etc/hostname

# gateway
route -n
ip r

# DNS
cat /etc/resolv.conf

# connectivity
ping -c 4 192.168.128.2
nslookup google.com
```