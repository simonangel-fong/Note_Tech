# Linux - Networking: Package `iproute`

[Back](../../index.md)

- [Linux - Networking: Package `iproute`](#linux---networking-package-iproute)
  - [`iproute` Package](#iproute-package)
  - [`ip` Utility](#ip-utility)
    - [`ip addr`: Get Interface and IP Info](#ip-addr-get-interface-and-ip-info)
    - [Lab: View Interface Information](#lab-view-interface-information)
    - [Lab: Assign a Static Runtime IP](#lab-assign-a-static-runtime-ip)
  - [`ss` Utility](#ss-utility)
    - [Lab: Filter and Kill Connection](#lab-filter-and-kill-connection)

---

## `iproute` Package

- Package
  - `sudo yum install iproute`
  - `rpm -aq | grep iproute`

---

## `ip` Utility

- `ip` command

  - a utility for network configuration and management.
  - replaces the deprecated `ifconfig` and `route` command.

- **Network Device**

| CMD                                          | DESC                                              |
| -------------------------------------------- | ------------------------------------------------- |
| `ip link show`                               | Displays information about all network interfaces |
| `ip link show dev_id`                        | Displays information about a network interface    |
| `ip link show up`                            | Displays only running interfaces                  |
| `ip link set dev_id up`                      | Enable an interface                               |
| `ip link set dev_id down`                    | Disable an interface                              |
| `ip link set dev old_id name new_id`         | Rename a device                                   |
| `ip link set dev dev_id address MAC_address` | Change the MAC Address                            |
| `ip link set dev dev_id mtu size`            | Set the MTU                                       |

- **IP address**
  - Ref: https://man7.org/linux/man-pages/man8/ip-address.8.html

| CMD                                          | DESC                                        |
| -------------------------------------------- | ------------------------------------------- |
| `ip addr show`                               | Displays ip for all interfaces              |
| `ip addr show up`                            | Displays ip for all active interface        |
| `ip addr show device_name`                   | Displays ip for an interface                |
| `ip addr add ip/mask dev device_name`        | Assign a runtime IP Address to an Interface |
| `ip addr del ip/mask dev device_name`        | Remove an IP Address                        |
| `ip addr flush dev device_name scope global` | Removes all global IPv4 and IPv6 addresses  |

- **Routing Table Entry**

| CMD                                                      | DESC                  |
| -------------------------------------------------------- | --------------------- |
| `ip route show`                                          | Display routing table |
| `ip route add dest_ip/mask via gw_ip dev interface_name` | Add a route           |
| `ip route del dest_ip/mask`                              | Delete a route        |
| `ip route add default via gw_ip dev interface_name`      | Set a Default Gateway |

---

### `ip addr`: Get Interface and IP Info

```sh
ip addr
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
#     link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
#     inet 127.0.0.1/8 scope host lo
#        valid_lft forever preferred_lft forever
#     inet6 ::1/128 scope host
#        valid_lft forever preferred_lft forever
# 2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
#     link/ether 00:0c:29:5b:ce:78 brd ff:ff:ff:ff:ff:ff
#     altname enp3s0
#     inet 192.168.204.153/24 brd 192.168.204.255 scope global dynamic noprefixroute ens160
#        valid_lft 1287sec preferred_lft 1287sec
#     inet6 fe80::20c:29ff:fe5b:ce78/64 scope link noprefixroute
#        valid_lft forever preferred_lft forever
# 3: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
#     link/ether 52:54:00:c5:c9:4d brd ff:ff:ff:ff:ff:ff
#     inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
#        valid_lft forever preferred_lft forever
```

---

- **Loopback Interface**
  - logical interface for local communication within the system
  - name: `lo`
- **Flags**:
  - `<LOOPBACK>`: Marks this as the **loopback interface**.
  - `<UP>`: The interface is **enabled**.
  - `<LOWER_UP>`: The interface is **operational at the hardware level**.
- `MTU (Maximum Transmission Unit)`:
  - 65536:the maximum packet size (very large since it does not involve physical transmission).
- **Queue Discipline (qdisc)**:
  - `qdisc noqueue`: the interface does **not use a queuing mechanism** since there’s no traffic contention on the loopback interface.
- `State UNKNOWN`: the interface is operational but **doesn’t have a conventional carrier link** like physical interfaces.
- `Group default`: this interface belongs to the **default interface group**.
- `qlen 1000`: Transmit Queue Length, the maximum number of packets queued for transmission.

- `link/loopback 00:00:00:00:00:00`:
  - `loopback`: refers to the loopback interface, a loopback interface doesn’t interact with external networks.
  - The MAC address for loopback is always `00:00:00:00:00:00`, which is a reserved address indicating it does not have a physical hardware counterpart.
- `brd 00:00:00:00:00:00`:
  - `brd`: broadcast address, which is typically used in physical networks for broadcasting packets to all devices on a subnet.
  - For the loopback interface, the broadcast address is also `00:00:00:00:00:00`, as broadcasting is irrelevant for this purely internal interface.
- **IPv4 Address**:
  - `inet 127.0.0.1/8`: The loopback IPv4 address with a subnet mask of /8.
  - `scope host`: The address is **limited to the local host**.
  - `valid_lft forever, preferred_lft forever`: These addresses are **valid** and **preferred** indefinitely.
- **IPv6 Address**:

  - `inet6 ::1/128`: The loopback IPv6 address with a subnet mask of /128.
  - `scope host`: Same as IPv4, **limited to the local host**.

---

- `ens160` The name of a physical or virtual network interface.
- **Flags**:
  - `<BROADCAST>`: Supports broadcasting.
  - `<MULTICAST>`: Supports multicast traffic.
  - `<UP>`: The interface is enabled.
  - `<LOWER_UP>`: The physical link is active.
- `mtu 1500`: the standard Ethernet packet size.
- `qdisc mq`:
  - `qdisc`: Queue Discipline
  - `mq (multi-queue)`: the interface supports multiple transmit queues, often for better performance on multi-core systems.
- `state UP`: the interface is active and functioning.
- `group default`: the interface belongs to the default group.
- `qlen 1000`: Transmit Queue Length (qlen)is 1000 packets.
- **Hardware (Link Layer)**:
  - `link/ether: 00:0c:29:5b:ce:78`: the MAC address.
  - `brd: ff:ff:ff:ff:ff:ff`: the broadcast address.
- `altname enp3s0`:
  - Alternate Name, an alternate naming convention for the interface.
- **IPv4 Address**:
  - `inet 192.168.204.153/24`: The IP address with a subnet mask of /24.
  - `brd 192.168.204.255`: The broadcast address.
  - `scope global`: the address is globally routable.
  - `dynamic`: The address is assigned **dynamically** (likely via DHCP).
  - `noprefixroute`: No automatic creation of routes for this address.
  - `valid_lft 1287sec`: The **remaining time** (in seconds) the address is valid.
  - `preferred_lft 1287sec`: The remaining time (in seconds) the address is **preferred for outgoing connections**.
- **IPv6 Address**:
  - `inet6 fe80::20c:29ff:fe5b:ce78/64`: The link-local IPv6 address with a /64 subnet mask.
  - `scope link`: The address is only valid within the same link.
  - `noprefixroute`: No automatic route creation.
  - `valid_lft forever, preferred_lft forever`: The address is valid and preferred indefinitely.

---

- `virbr0`: A v**irtual bridge interface**, often used for virtual machines or containers.
- **Flags**:
  - `<NO-CARRIER>`: The interface is **not connected to a physical carrier**.
  - `<BROADCAST>`: Supports broadcasting.
  - `<MULTICAST>`: Supports multicast.
  - `<UP>`: The interface is enabled.
- `MTU 1500`: the standard packet size.
- `qdisc noqueue`:
  - qdisc: Queue Discipline
  - noqueue: no queuing mechanism since it’s a virtual interface.
- `state DOWN`:
  - interface is enabled but not operational.
- `group default`:
  - default Group
- `qlen 1000`
  - Transmit Queue Length (qlen)
- **Hardware (Link Layer)**:
  - `link/ether: 52:54:00:c5:c9:4d` the MAC address.
  - `brd: ff:ff:ff:ff:ff:ff`: the broadcast address.
- **IPv4 Address**:
  - `inet 192.168.122.1/24`: The IP address assigned to the bridge interface with a /24 subnet mask.
  - `brd 192.168.122.255`: The broadcast address.
  - `scope global`: The address is globally routable.
  - `valid_lft forever, preferred_lft forever`: The address is valid and preferred indefinitely.

---

### Lab: View Interface Information

```sh
# List all devices
ip link show
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
#     link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
# 2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
#     link/ether 00:0c:29:5b:ce:78 brd ff:ff:ff:ff:ff:ff
#     altname enp3s0
# 3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
#     link/ether 00:0c:29:5b:ce:82 brd ff:ff:ff:ff:ff:ff
#     altname enp19s0
# 4: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default qlen 1000
#     link/ether 52:54:00:c5:c9:4d brd ff:ff:ff:ff:ff:ff

ip link show ens224
# 3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
#     link/ether 00:0c:29:5b:ce:82 brd ff:ff:ff:ff:ff:ff
#     altname enp19s0
```

---

### Lab: Assign a Static Runtime IP

```sh
# list all ip of all interfaces
ip addr show

# Get ip of a interface
ip addr show ens224
# 3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
#     link/ether 00:0c:29:5b:ce:82 brd ff:ff:ff:ff:ff:ff
#     altname enp19s0
#     inet 192.168.204.171/24 brd 192.168.204.255 scope global noprefixroute ens224
#        valid_lft forever preferred_lft forever
#     inet6 fe80::70eb:5c8e:a06e:f8e2/64 scope link noprefixroute
#        valid_lft forever preferred_lft forever

# Add an ip
ip addr add 192.168.204.170/24 dev ens224
ip addr show ens224 | grep "inet "
# inet 192.168.204.171/24 brd 192.168.204.255 scope global noprefixroute ens224
# inet 192.168.204.170/24 scope global secondary ens224

# Delete ip
ip addr del 192.168.204.173/24 dev ens224
ip addr show ens224 | grep "inet "
# inet 192.168.204.170/24 scope global ens224

# Removes all global IPv4 and IPv6 addresses
ip address flush dev ens224 scope global
ip addr show ens224
# 3: ens224: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
#     link/ether 00:0c:29:5b:ce:82 brd ff:ff:ff:ff:ff:ff
#     altname enp19s0
#     inet6 fe80::70eb:5c8e:a06e:f8e2/64 scope link noprefixroute
#        valid_lft forever preferred_lft forever
```

---

## `ss` Utility

- `ss` command
  - short for `Socket Statistics`
  - used to display information about **network sockets** in Linux.
  - a modern replacement for the deprecated `netstat` command

| CMD                                     | DESC                                                            |
| --------------------------------------- | --------------------------------------------------------------- |
| `ss -s`                                 | Statistics for a Specific Protocol                              |
| `ss -a`                                 | Displaya both listening and non-listening sockets.              |
| `ss -t`                                 | Displays TCP connections.                                       |
| `ss -u`                                 | Displays UDP connections.                                       |
| `ss -x`                                 | Displays UNIX domain sockets.                                   |
| `ss -l`                                 | Displays only sockets in the listening state.                   |
| `ss -p`                                 | Displays Connections with Process Information                   |
| `ss -tp src :22`                        | Displays pid and established TCP sockets with local port 22     |
| `ss -tp dst :ssh`                       | Displays pid and established TCP sockets with remote ssh port   |
| `ss -ltp src :22`                       | Displays pid and listening TCP sockets with local port 22       |
| `ss -ltp dst :ssh`                      | Displays pid and listening TCP sockets with remote ssh port     |
| `ss -4tp src 192.168/16`                | Displays pid and TCP IPv4 sockets on a local subnet             |
| `ss -K dst 192.168.204.1 dport = 54739` | Kill Socket Connection with destination IP and destination port |

---

### Lab: Filter and Kill Connection

- Create 2 SSH connection

```sh
# Confirm listen to ssh port
ss -ltp src :22
# State   Recv-Q  Send-Q   Local Address:Port    Peer Address:Port  Process
# LISTEN  0       128            0.0.0.0:ssh          0.0.0.0:*      users:(("sshd",pid=1188,fd=3))
# LISTEN  0       128               [::]:ssh             [::]:*      users:(("sshd",pid=1188,fd=4))

# Displays pid and SSH connection
ss -tp src :22
# State      Recv-Q      Send-Q              Local Address:Port              Peer Address:Port       Process
# ESTAB      0           0                 192.168.204.153:ssh              192.168.204.1:55073       users:(("sshd",pid=70913,fd=4),("sshd",pid=70909,fd=4))
# ESTAB      0           64                192.168.204.153:ssh              192.168.204.1:52810       users:(("sshd",pid=3727,fd=4),("sshd",pid=2978,fd=4))

# Kill a ssh connection
ss -K dst 192.168.204.1 dport = 55073
# Netid   State    Recv-Q    Send-Q         Local Address:Port        Peer Address:Port    Process
# tcp     ESTAB    0         0            192.168.204.153:ssh        192.168.204.1:55073

# Verify
ss -tp src :22
# State     Recv-Q     Send-Q           Local Address:Port          Peer Address:Port     Process
# ESTAB     0          0              192.168.204.153:ssh          192.168.204.1:52810     users:(("sshd",pid=3727,fd=4),("sshd",pid=2978,fd=4))
```

---

[TOP](#linux---networking-package-iproute)
