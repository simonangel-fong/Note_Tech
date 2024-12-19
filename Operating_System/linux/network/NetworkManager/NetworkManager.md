# Linux - Networking: Package `NetworkManager`

[Back](../../index.md)

- [Linux - Networking: Package `NetworkManager`](#linux---networking-package-networkmanager)
  - [`NetworkManager` Package](#networkmanager-package)
    - [Configuration File](#configuration-file)
    - [`NetworkManager` Utility](#networkmanager-utility)
  - [Lab: Enable/Disable Network Connectivity](#lab-enabledisable-network-connectivity)
  - [Lab: Managing Devices](#lab-managing-devices)
  - [Lab: Manging Connection](#lab-manging-connection)
  - [Lab: Creating a Permanent Static IP Connection](#lab-creating-a-permanent-static-ip-connection)
  - [Lab: Add/Delete a Secondary Static IP to a Connection](#lab-adddelete-a-secondary-static-ip-to-a-connection)
  - [Lab: Configure Multiple Interfaces](#lab-configure-multiple-interfaces)
    - [List Adapters](#list-adapters)
    - [Configure Interfaces](#configure-interfaces)
    - [Configure Gateway and Priority](#configure-gateway-and-priority)
    - [Configure Default DNS](#configure-default-dns)

---

## `NetworkManager` Package

- `NetworkManager`

  - a daemon that provides the default networking service in Linux.

- Package info:
  - `dnf info NetworkManager`
- File location:
  - `/usr/sbin/NetworkManager`
- Service
  - `systemctl status NetworkManager`
- Process
  - `ps -ef | grep NetworkManager`
- Tools to configure network manager
  - `nmcli`: Network manager command line interface
  - `nmtui`: Network manager text user interface
  - `nm-connection-editor`: Network manager GUI tool
  - `GNOME Settings`: GNOME desktop app.

---

### Configuration File

- Configuration File Directory:
  - `/etc/NetworkManager`

---

### `NetworkManager` Utility

- Retrieves network information: Does not required privilege.
- Configure networking: requires privileges.
- Ref:

  - https://people.freedesktop.org/~lkundrak/nm-docs/nmcli.html#property_aliases

---

- **Networking**

| CMD                    | DESC                       |
| ---------------------- | -------------------------- |
| `nmcli general status` | Display the overall status |
| `nmcli networking`     | Display networking status  |
| `nmcli networking on`  | Enable networking          |
| `nmcli networking off` | Disable networking         |

- **Device**

| CMD                                   | DESC                                                                     |
| ------------------------------------- | ------------------------------------------------------------------------ |
| `nmcli device status`                 | Display status of devices (Default)                                      |
| `nmcli device show`                   | Display detailed information about all devices.                          |
| `nmcli device show device_name`       | Display a device detail infromation                                      |
| `nmcli device connect device_name`    | Connect the device with a suitable connection                            |
| `nmcli device disconnect device_name` | Disconnect a device and prevent the device from automatically activating |
| `nmcli device delete device_name`     | Removes the interface (only works for software devices)                  |

- **Wi-Fi Networks**

| CMD                                                    | DESC                                   |
| ------------------------------------------------------ | -------------------------------------- |
| `nmcli device wifi list`                               | Scan and display nearby Wi-Fi networks |
| `nmcli device wifi connect "SSID" password "password"` | Connect to a Wi-Fi network             |
| `nmcli device disconnect device_name`                  | Disconnect a Network                   |

- **Connection management**

- `NetworkManager Connections`

  - a collection of data (Layer2 details, IP addressing, etc.) that describe how to create or connect to a network.
  - all network configurations

- `Active Connection`
  - a connection status when a device uses that connection's configuration to create or connect to a network.
  - There may be **multiple** connections that **apply** to a device, but **only one** of them can be **active** on that device **at any given time**.
    - The additional connections can be used to allow quick **switching** between different networks and configurations.

| CMD                                                                                                  | DESC                                       |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `nmcli connection show`/`nmcli c`                                                                    | Display the status of all connections      |
| `nmcli connection show "id_name"`                                                                    | Display details for specified connections  |
| `nmcli connection up "id_name"`                                                                      | Activate a connection                      |
| `nmcli connection down "id_name"`                                                                    | Deactivate a connection                    |
| `nmcli connection add con-name "id_name" ifname "if_name" type ethernet ip4 "ip/mask" gw4 "gw_ip"`   | Create a new connection                    |
| `nmcli connection modify "id_name" ipv4.addresses "ip/mask" ipv4.gateway "gw_ip" ipv4.method manual` | Modify ip address.                         |
| `nmcli connection modify "id_name" ipv4.dns "dns_ip"`                                                | Modify DNS settings                        |
| `nmcli connection delete "id_name"`                                                                  | Delete a Connection                        |
| `nmcli connection reload "id_name"`                                                                  | Reload all connection files from disk.     |
| `nmcli connection reload filename`                                                                   | Load/reload connection files from disk.    |
| `nmcli connection export id_name`                                                                    | Export a connection.                       |
| `nmcli connection import filename`                                                                   | Import an external/foreign configuration . |

---

## Lab: Enable/Disable Network Connectivity

```sh
# Get overall networking status
nmcli general status
# STATE      CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
# connected  full          missing  enabled  missing  enabled

# Disable networking
nmcli networking off
# STATE   CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
# asleep  none          missing  enabled  missing  enabled

# Confirm networking status
nmcli networking
# disabled
nmcli networking connectivity
# none
nmcli general status
# STATE   CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
# asleep  none          missing  enabled  missing  enabled

# Enable networking
nmcli networking on

# Verify
nmcli networking
# enabled
nmcli general status
# STATE      CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
# connected  full          missing  enabled  missing  enabled
nmcli networking connectivity
# full
```

---

## Lab: Managing Devices

```sh
# get the status of all devices
nmcli device status
# DEVICE  TYPE      STATE                   CONNECTION
# ens160  ethernet  connected               ens161
# virbr0  bridge    connected (externally)  virbr0
# lo      loopback  unmanaged               --

# Add a new network adapter

# get new status
nmcli device status
# DEVICE  TYPE      STATE                   CONNECTION
# ens160  ethernet  connected               ens161
# virbr0  bridge    connected (externally)  virbr0
# ens224  ethernet  disconnected            --
# lo      loopback  unmanaged               --


# Get the detail info of a device
nmcli device show ens224
# GENERAL.DEVICE:                         ens224
# GENERAL.TYPE:                           ethernet
# GENERAL.HWADDR:                         00:0C:29:5B:CE:82
# GENERAL.MTU:                            1500
# GENERAL.STATE:                          30 (disconnected)
# GENERAL.CONNECTION:                     --
# GENERAL.CON-PATH:                       --
# WIRED-PROPERTIES.CARRIER:               on
# IP4.GATEWAY:                            --
# IP6.GATEWAY:                            --

# Connect a device
nmcli device connect ens224
# Device 'ens224' successfully activated with '6e3f82e8-2608-3d23-b02d-4cbd390003bb'.

# verify status
nmcli device status
# DEVICE  TYPE      STATE                   CONNECTION
# ens160  ethernet  connected               ens161
# ens224  ethernet  connected               Wired connection 1
# virbr0  bridge    connected (externally)  virbr0
# lo      loopback  unmanaged               --

# verify detail info
nmcli device show ens224
# GENERAL.DEVICE:                         ens224
# GENERAL.TYPE:                           ethernet
# GENERAL.HWADDR:                         00:0C:29:5B:CE:82
# GENERAL.MTU:                            1500
# GENERAL.STATE:                          100 (connected)
# GENERAL.CONNECTION:                     Wired connection 1
# GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveC>
# WIRED-PROPERTIES.CARRIER:               on
# IP4.ADDRESS[1]:                         192.168.204.159/24
# IP4.GATEWAY:                            192.168.204.2
# IP4.ROUTE[1]:                           dst = 192.168.204.0/24, nh = 0.0.0.0, m>
# IP4.ROUTE[2]:                           dst = 0.0.0.0/0, nh = 192.168.204.2, mt>
# IP4.DNS[1]:                             192.168.204.2
# IP4.DOMAIN[1]:                          localdomain
# IP6.ADDRESS[1]:                         fe80::c796:2422:9cde:9b61/64
# IP6.GATEWAY:                            --
# IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 1024

# verify ip address
hostname -I
# 192.168.204.153 192.168.122.1 192.168.204.159
# the 3rd one the ip of the new device

# disconnect
nmcli device disconnect ens224
# Device 'ens224' successfully disconnected.

# verify
nmcli device status
# DEVICE  TYPE      STATE                   CONNECTION
# ens160  ethernet  connected               ens161
# virbr0  bridge    connected (externally)  virbr0
# ens224  ethernet  disconnected            --
# lo      loopback  unmanaged               --
```

---

## Lab: Manging Connection

```sh
# Get all connections status
nmcli connection show
# NAME                UUID                                  TYPE      DEVICE
# ens161              bea1745d-c7f0-430a-a575-9c06f5d420a7  ethernet  ens160
# virbr0              157372ca-2156-4a35-b0e5-b7f4c3efb605  bridge    virbr0
# Wired connection 1  6e3f82e8-2608-3d23-b02d-4cbd390003bb  ethernet  --

# Get details for a specified connection
nmcli connection show "Wired connection 1"
# connection.id:                          Wired connection 1
# connection.uuid:                        6e3f82e8-2608-3d23-b02d-4cbd390003bb
# connection.stable-id:                   --
# connection.type:                        802-3-ethernet
# connection.interface-name:              ens224
# connection.autoconnect:                 yes
# connection.autoconnect-priority:        -999
# ...

# Delete a connection
nmcli connection delete "Wired connection 1"
# Connection 'Wired connection 1' (6e3f82e8-2608-3d23-b02d-4cbd390003bb) successfully deleted.

# verify
nmcli connection show
# NAME    UUID                                  TYPE      DEVICE
# ens161  bea1745d-c7f0-430a-a575-9c06f5d420a7  ethernet  ens160
# virbr0  157372ca-2156-4a35-b0e5-b7f4c3efb605  bridge    virbr0
```

---

## Lab: Creating a Permanent Static IP Connection

```sh
# Create a new connection
nmcli connection add con-name "static_con" type ethernet
# Connection 'static_con' (8bb06276-9ca1-4a9f-adc5-e2d02ac361ec) successfully added.

# confirm
nmcli connection show
# NAME        UUID                                  TYPE      DEVICE
# ens160      bea1745d-c7f0-430a-a575-9c06f5d420a7  ethernet  ens160
# virbr0      22dfb61f-7c71-44a3-87b2-4b95ebec61e2  bridge    virbr0
# static_con  8bb06276-9ca1-4a9f-adc5-e2d02ac361ec  ethernet  --

# Modify
# Specify an IP
nmcli connection modify "static_con" ipv4.addresses "192.168.204.170/24"
# Assign gateway IP
nmcli connection modify "static_con" ipv4.gateway "192.168.204.2"
# Set method as manual
nmcli connection modify "static_con" ipv4.method manual
# Set the dns ip
nmcli connection modify "static_con" ipv4.dns 8.8.8.8,8.8.4.4
# Set device
nmcli connection modify "static_con" ifname "ens224"

# Confirm configuration
nmcli connection show static_con
# ipv4.method:                            manual
# ipv4.dns:                               8.8.8.8,8.8.4.4
# ipv4.dns-search:                        --
# ipv4.dns-options:                       --
# ipv4.dns-priority:                      0
# ipv4.addresses:                         192.168.204.170/24
# ipv4.gateway:                           192.168.204.2
# ipv4.routes:                            --
# ipv4.route-metric:                      -1
# ipv4.route-table:                       0 (unspec)
# ipv4.routing-rules:                     --
# ipv4.ignore-auto-routes:                no
# ipv4.ignore-auto-dns:                   no
# ipv4.dhcp-client-id:                    --
# ipv4.dhcp-iaid:                         --
# ipv4.dhcp-timeout:                      0 (default)
# ipv4.dhcp-send-hostname:                yes
# ipv4.dhcp-hostname:                     --
# ipv4.dhcp-fqdn:                         --
# ipv4.dhcp-hostname-flags:               0x0 (none)
# ipv4.never-default:                     no
# ipv4.may-fail:                          yes
# ipv4.required-timeout:                  -1 (default)
# ipv4.dad-timeout:                       -1 (default)
# ipv4.dhcp-vendor-class-identifier:      --
# ipv4.link-local:                        0 (default)

# Activate a connecton
nmcli connection up static_con
# Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/6)

# Verify the connection is active
nmcli conn show
# NAME        UUID                                  TYPE      DEVICE
# ens160      bea1745d-c7f0-430a-a575-9c06f5d420a7  ethernet  ens160
# static_con  8bb06276-9ca1-4a9f-adc5-e2d02ac361ec  ethernet  ens224
# virbr0      22dfb61f-7c71-44a3-87b2-4b95ebec61e2  bridge    virbr0


# varify the IP of the device
ip addr show ens224
# 4: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
#     link/ether 00:0c:29:5b:ce:82 brd ff:ff:ff:ff:ff:ff
#     altname enp19s0
#     inet 192.168.204.170/24 brd 192.168.204.255 scope global noprefixroute ens224
#        valid_lft forever preferred_lft forever
#     inet6 fe80::70eb:5c8e:a06e:f8e2/64 scope link noprefixroute
#        valid_lft forever preferred_lft forever
```

---

## Lab: Add/Delete a Secondary Static IP to a Connection

- Adding a Secondary static IP to a Connection

```sh
# show the active connection
nmcli connection show --active
# NAME        UUID                                  TYPE      DEVICE
# ens160      bea1745d-c7f0-430a-a575-9c06f5d420a7  ethernet  ens160
# static_con  8bb06276-9ca1-4a9f-adc5-e2d02ac361ec  ethernet  ens224
# virbr0      22dfb61f-7c71-44a3-87b2-4b95ebec61e2  bridge    virbr0

# show the current ip
ip address show ens224 | grep "inet "
# inet 192.168.204.170/24 brd 192.168.204.255 scope global noprefixroute ens224

# modify a connection by adding a new ip
nmcli connection modify static_con +ipv4.addresses 192.168.204.171/24

# Confirm configuration
nmcli connection show static_con
# ipv4.method:                            manual
# ipv4.dns:                               8.8.8.8
# ipv4.dns-search:                        --
# ipv4.dns-options:                       --
# ipv4.dns-priority:                      0
# ipv4.addresses:                         192.168.204.170/24, 192.168.204.171/24
# ipv4.gateway:                           192.168.204.2
# ipv4.routes:                            --
# ipv4.route-metric:                      -1
# ipv4.route-table:                       0 (unspec)
# ipv4.routing-rules:                     --
# ipv4.ignore-auto-routes:                no
# ipv4.ignore-auto-dns:                   no
# ipv4.dhcp-client-id:                    --
# ipv4.dhcp-iaid:                         --
# ipv4.dhcp-timeout:                      0 (default)
# ipv4.dhcp-send-hostname:                yes
# ipv4.dhcp-hostname:                     --
# ipv4.dhcp-fqdn:                         --
# ipv4.dhcp-hostname-flags:               0x0 (none)

# reload the connection
nmcli connection reload
# same as down and up

# reboot
systemctl reboot

# verify
ip address show ens224 | grep "inet "
# inet 192.168.204.170/24 brd 192.168.204.255 scope global noprefixroute ens224
# inet 192.168.204.171/24 brd 192.168.204.255 scope global secondary noprefixroute ens224
```

- Removing a Secondary static IP to a Connection

```sh
# modify a connection by removing a new ip
nmcli connection modify static_con -ipv4.addresses 192.168.204.170/24

# Confirm configuration
nmcli connection show static_con
# ipv4.method:                            manual
# ipv4.dns:                               8.8.8.8
# ipv4.dns-search:                        --
# ipv4.dns-options:                       --
# ipv4.dns-priority:                      0
# ipv4.addresses:                         192.168.204.171/24
# ipv4.gateway:                           192.168.204.2
# ipv4.routes:                            --
# ipv4.route-metric:                      -1
# ipv4.route-table:                       0 (unspec)
# ipv4.routing-rules:                     --
# ipv4.ignore-auto-routes:                no
# ipv4.ignore-auto-dns:                   no
# ipv4.dhcp-client-id:                    --
# ipv4.dhcp-iaid:                         --
# ipv4.dhcp-timeout:                      0 (default)
# ipv4.dhcp-send-hostname:                yes
# ipv4.dhcp-hostname:                     --
# ipv4.dhcp-fqdn:                         --

# reload the connection
nmcli connection reload

# reboot
systemctl reboot

# verify
ip address show ens224 | grep "inet "
# inet 192.168.204.171/24 brd 192.168.204.255 scope global noprefixroute ens224
```

---

## Lab: Configure Multiple Interfaces

### List Adapters

```sh
# list all interface
ip link show
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
#     link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
# 2: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default qlen 1000
#     link/ether 52:54:00:c5:c9:4d brd ff:ff:ff:ff:ff:ff
# 3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
#     link/ether 00:0c:29:27:6b:f3 brd ff:ff:ff:ff:ff:ff
#     altname enp19s0
# 4: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
#     link/ether 00:0c:29:27:6b:fd brd ff:ff:ff:ff:ff:ff
#     altname enp3s0

nmcli d
# DEVICE  TYPE      STATE         CONNECTION
# ens160  ethernet  disconnected  --
# ens224  ethernet  disconnected  --
# virbr0  bridge    unmanaged     --
# lo      loopback  unmanaged     --
```

---

### Configure Interfaces

```sh
su -

# add ens160 connection
nmcli connection add con-name "ens160" type ethernet
nmcli connection modify ens160 ipv4.addresses 192.168.1.130/24
nmcli connection modify ens160 ipv4.method manual
nmcli connection modify ens160 ifname ens160
nmcli connection show ens160

# add ens224 connection
nmcli connection add con-name "ens224" type ethernet
nmcli connection modify ens224 ipv4.addresses 192.168.1.135/24
nmcli connection modify ens224 ipv4.method manual
nmcli connection modify ens224 ifname ens224

# enable connections
nmcli connection down ens160
nmcli connection up ens160
# Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/4)
nmcli connection down ens224
nmcli connection up ens224
# Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/5)

# confirm
nmcli c
# NAME    UUID                                  TYPE      DEVICE
# ens160  c6bae8b9-3866-47a6-8771-abc591b09bf7  ethernet  ens160
# ens224  5780461f-424b-49b2-9df5-a82106ac7c77  ethernet  ens224
nmcli d
# DEVICE  TYPE      STATE      CONNECTION
# ens160  ethernet  connected  ens160
# ens224  ethernet  connected  ens224
# virbr0  bridge    unmanaged  --
# lo      loopback  unmanaged  --
```

---

### Configure Gateway and Priority

```sh
nmcli c modify ens160 ipv4.gateway 192.168.1.2 ipv4.route-metric 100
nmcli c down ens160; nmcli c up ens160
# Connection 'ens160' successfully deactivated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/1)
# Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/3)

nmcli connection modify ens224 ipv4.gateway 192.168.1.2 ipv4.route-metric 200
nmcli c down ens224; nmcli c up ens224
# Connection 'ens224' successfully deactivated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/2)
# Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/4)

# confirm
ip route
# default via 192.168.1.2 dev ens160 proto static metric 100
# default via 192.168.1.2 dev ens224 proto static metric 200
# 192.168.1.0/24 dev ens160 proto kernel scope link src 192.168.1.130 metric 100
# 192.168.1.0/24 dev ens224 proto kernel scope link src 192.168.1.135 metric 200

# verify the default interface
ip route get 8.8.8.8
# 8.8.8.8 via 192.168.1.2 dev ens160 src 192.168.1.130 uid 0
    # cache
```

---

### Configure Default DNS

```sh
hostname
# serverhost

vi /etc/resolv.conf
# Generated by NetworkManager
# search serverhost
# nameserver 8.8.8.8

# restart nm
systemctl restart NetworkManager

# test
ping -c4 google.ca
```

---

[TOP](#linux---networking-package-networkmanager)
