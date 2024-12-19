# Linux - Networking: Package `net-tools` (deprecated)

[Back](../../index.md)

- [Linux - Networking: Package `net-tools` (deprecated)](#linux---networking-package-net-tools-deprecated)
  - [Package `net-tools`](#package-net-tools)
  - [`ifconfig` Utility](#ifconfig-utility)
    - [`ifconfig`: Interface Info](#ifconfig-interface-info)
    - [Lab: Activate/Deactivate an Interface](#lab-activatedeactivate-an-interface)
    - [Lab: Assign a Static Runtime IP](#lab-assign-a-static-runtime-ip)
  - [`route` Utility](#route-utility)
    - [Lab: Displays IP Routing Table](#lab-displays-ip-routing-table)
  - [`netstat` Utility](#netstat-utility)
    - [Lab: Displays IP Routing Table](#lab-displays-ip-routing-table-1)

---

## Package `net-tools`

- Package

```sh
sudo yum install net-tools
rpm -aq | grep net-tools
```

---

## `ifconfig` Utility

- `ifconfig`

  - Stands for (`interface configuration`)
  - used to configure, control, and display information about network interfaces.
  - replaced by the `ip` command from the `iproute` suite.

- Device

| CMD                      | DESC                                        |
| ------------------------ | ------------------------------------------- |
| `ifconfig`               | Display includes active network interfaces. |
| `ifconfig -a`            | Display only active interfaces.             |
| `ifconfig devce_id`      | Display a specific network interface.       |
| `ifconfig devce_id up`   | Activates a specific network interface.     |
| `ifconfig devce_id down` | Deactivates a specific network interface.   |

- **Runtime Configure**

| CMD                                                 | DESC                                             |
| --------------------------------------------------- | ------------------------------------------------ |
| `ifconfig eth0 192.168.1.100 netmask 255.255.255.0` | Assigns an IP address for a specific interface.  |
| `ifconfig eth0 broadcast 192.168.1.255`             | Assigns a broadcast address to an interface.     |
| `ifconfig devce_id hw ether new_MAC_address`        | Change a new MAC address to a network interface. |

---

### `ifconfig`: Interface Info

```sh
ifconfig
# ens160: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
#         inet 192.168.204.153  netmask 255.255.255.0  broadcast 192.168.204.255
#         inet6 fe80::20c:29ff:fe5b:ce78  prefixlen 64  scopeid 0x20<link>
#         ether 00:0c:29:5b:ce:78  txqueuelen 1000  (Ethernet)
#         RX packets 166189  bytes 241795084 (230.5 MiB)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 13913  bytes 2465843 (2.3 MiB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
#         inet 127.0.0.1  netmask 255.0.0.0
#         inet6 ::1  prefixlen 128  scopeid 0x10<host>
#         loop  txqueuelen 1000  (Local Loopback)
#         RX packets 0  bytes 0 (0.0 B)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 0  bytes 0 (0.0 B)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# virbr0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
#         inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
#         ether 52:54:00:c5:c9:4d  txqueuelen 1000  (Ethernet)
#         RX packets 0  bytes 0 (0.0 B)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 0  bytes 0 (0.0 B)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

---

- **Interface Name**:
  - the name of a physical or virtual network interface.
  - `ens160`
- `Flags: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>`
  - **UP**: The interface is **enabled**.
  - **BROADCAST**: The interface **supports broadcasting**.
  - **RUNNING**: The interface is **operational**.
  - **MULTICAST**: The interface **supports multicast**.
- `MTU (Maximum Transmission Unit)`:
  - `mtu 1500`: the maximum size of packets (in bytes) that can be transmitted **without fragmentation**.
- **IPv4 Address Details**:
  - `inet: 192.168.204.153`: the IPv4 address assigned to the interface.
  - `netmask: 255.255.255.0`: the subnet mask.
  - `broadcast: 192.168.204.255`: the broadcast address.
- **IPv6 Address Details**:
  - `inet6: fe80::20c:29ff:fe5b:ce78`: the link-local IPv6 address.
  - `prefixlen 64`: Specifies the subnet mask for IPv6.
  - `scopeid`: Indicates the scope of the address (`<link>` means it's local to the link).
- **MAC Address**:
  - `ether 00:0c:29:5b:ce:78`: the Media Access Control (MAC) address of the interface.
- **Transmit Queue Length**
  - `txqueuelen 1000  (Ethernet)`: 1000 packets can be queued in the kernel for transmission before they are sent to the network hardware.
  - interface type is `Ethernet`
- **Statistics**:
  - `RX packets 166189`: The number of packets **received**.
  - `RX bytes 241795084 (230.5 MiB)`: Total data **received**.
  - `RX errors, dropped, overruns, frame`: All error counts for **received** packets are 0.
  - `TX packets 13913`: The number of packets **transmitted**.
  - `TX bytes 2465843 (2.3 MiB)`: Total data **transmitted**.
  - `TX errors, dropped, overruns, carrier, collisions`: All error counts for **transmitted** packets are 0.

---

- **Loopback Interface**
  - loopback interface used for **communication within** the local machine.
  - name: `lo`
- `Flags: flags=73<UP,LOOPBACK,RUNNING>`
  - `UP`: The interface is **enabled**.
  - `LOOPBACK`: Indicates it is a loopback interface.
  - `RUNNING`: The interface is operational.
- `MTU (Maximum Transmission Unit)`:
  - `mtu 65536` allows larger packet sizes since it does **not involve physical hardware**.

---

- **Bridge Interface**
  - Interface Name: `virbr0`
  - a **virtual bridge interface** used for virtual machines or containers.
- `Flags: flags=4099<UP,BROADCAST,MULTICAST>`
  - `UP`: The interface is enabled.
  - `BROADCAST`: Supports broadcasting.
  - `MULTICAST`: Supports multicast.
- `MTU (Maximum Transmission Unit)`:
  - `mtu 1500`: specifies the maximum packet size.

---

### Lab: Activate/Deactivate an Interface

```sh
# List all interfaces
ifconfig

# Get interface info
ifconfig ens224
# ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
#         inet 192.168.204.170  netmask 255.255.255.0  broadcast 0.0.0.0
#         inet6 fe80::70eb:5c8e:a06e:f8e2  prefixlen 64  scopeid 0x20<link>
#         ether 00:0c:29:5b:ce:82  txqueuelen 1000  (Ethernet)
#         RX packets 2829  bytes 316014 (308.6 KiB)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 521  bytes 71586 (69.9 KiB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# Deactivate an interface
ifconfig ens224 down
# verify
ifconfig ens224
# ens224: flags=4098<BROADCAST,MULTICAST>  mtu 1500
#         ether 00:0c:29:5b:ce:82  txqueuelen 1000  (Ethernet)
#         RX packets 2927  bytes 325316 (317.6 KiB)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 544  bytes 74548 (72.8 KiB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# Activate an interface
ifconfig ens224 up
# verify
ifconfig ens224
# ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
#         inet 192.168.204.171  netmask 255.255.255.0  broadcast 192.168.204.255
#         inet6 fe80::70eb:5c8e:a06e:f8e2  prefixlen 64  scopeid 0x20<link>
#         ether 00:0c:29:5b:ce:82  txqueuelen 1000  (Ethernet)
#         RX packets 0  bytes 0 (0.0 B)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 10  bytes 1454 (1.4 KiB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

---

### Lab: Assign a Static Runtime IP

```sh
# rename an inerface
ifconfig ens224 | grep "inet "
# inet 192.168.204.171  netmask 255.255.255.0  broadcast 192.168.204.255

# shutdown an interface device
ifconfig ens224 down

# assign a static IP
ifconfig ens224 192.168.204.100
ifconfig ens224 netmask 255.255.255.0

# Activate the interface device
ifconfig ens224 up

# verify
ifconfig ens224 | grep "inet "
# inet 192.168.204.100  netmask 255.255.255.0  broadcast 192.168.204.255
```

- Reboot system and check ip

```sh
systemctl reboot

ifconfig ens224 | grep "inet "
# inet 192.168.204.171  netmask 255.255.255.0  broadcast 192.168.204.255
```

---

## `route` Utility

- `route` command

  - used to view and manipulate the kernel's **IP routing table**
  - deprecated and has been replaced by the `ip route` command

- **Route Table**

| CMD                                                                  | DESC                                     |
| -------------------------------------------------------------------- | ---------------------------------------- |
| `route`                                                              | Display IP routing table                 |
| `route -n`                                                           | Display numerical addresses              |
| `route add default gw 192.168.0.1`                                   | Add a Default Route                      |
| `route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.0.1`    | Add a static route to a specific network |
| `route change -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.0.2` | Change a Route                           |
| `route del -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.0.1`    | Delete a Route                           |

---

### Lab: Displays IP Routing Table

```sh
route -n
# Kernel IP routing table
# Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
# 0.0.0.0         192.168.204.2   0.0.0.0         UG    100    0        0 ens160
# 0.0.0.0         192.168.204.2   0.0.0.0         UG    101    0        0 ens224
# 192.168.204.0   0.0.0.0         255.255.255.0   U     100    0        0 ens160
# 192.168.204.0   0.0.0.0         255.255.255.0   U     101    0        0 ens224
```

- **Columns**:
  - `Destination`:
    - Specifies the destination network or host.
    - `0.0.0.0`:
      - Indicates the default route for all traffic not matching any specific destination.
    - `192.168.204.0`: The
      - local subnet.
  - `Gateway`:
    - The next-hop gateway for the route.
    - `192.168.204.2`: Indicates that traffic destined for the listed Destination will be sent via this gateway.
    - `0.0.0.0`: Indicates that the destination is directly reachable (no gateway is required).
  - `Genmask`:
    - The subnet mask for the destination.
    - `0.0.0.0`: Applies to **all IP addresses** (used for the default route).
    - `255.255.255.0`: Applies to the subnet range 192.168.204.1–192.168.204.254.
  - `Flags`:
    - Indicates the route's properties.
    - `U`: The route is up (usable).
    - `G`: The route uses a gateway.
  - `Metric`:
    - The cost of using this route.
    - Lower values are preferred when multiple routes exist.
    - `100` and `101` are metrics for the respective routes.
  - `Ref`:
    - Unused in modern Linux systems (legacy field).
  - `Use`:
    - Shows the count of lookups for this route (generally 0 for a new table).
  - `Iface`:
    - The network interface associated with the route.
    - `ens160` and `ens224` are the interfaces for these routes.

---

## `netstat` Utility

- `netstat` command

  - a network utility used to display active network connections, listening ports, routing tables, interface statistics, and other network-related information.

- largely replaced by the `ss` command in newer Linux distributions

---

| CMD              | DESC                                          |
| ---------------- | --------------------------------------------- |
| `netstat`        | Display Active Network Connections            |
| `netstat -t`     | Display TCP Connections                       |
| `netstat -u`     | Display UDP Connections                       |
| `netstat -l`     | Display Listening Ports                       |
| `netstat -p`     | Display Connections with Process Information  |
| `netstat -tunlp` | Display Listening and Established Connections |
| `netstat -i`     | Display Network Statistics                    |
| `netstat -r`     | Display Routing Table                         |
| `netstat -rnv`   | Display IP routing table                      |

---

### Lab: Displays IP Routing Table

```sh
netstat -rnv
# Kernel IP routing table
# Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
# 0.0.0.0         192.168.204.2   0.0.0.0         UG        0 0          0 ens160
# 0.0.0.0         192.168.204.2   0.0.0.0         UG        0 0          0 ens224
# 192.168.204.0   0.0.0.0         255.255.255.0   U         0 0          0 ens160
# 192.168.204.0   0.0.0.0         255.255.255.0   U         0 0          0 ens224
```

---

- **Kernel IP Routing Table**

  - shows how the system **routes IP packets**.
  - Each row corresponds to a route in the routing table.

- **Columns**:
  - `Destination`:
    - The destination network or host to which packets are routed.
  - `Gateway`:
    - The **gateway (next-hop router)** to reach the destination.
    - `0.0.0.0`:
      - no gateway is needed;
      - the destination is **directly reachable**.
  - `Genmask`:
    - The **subnet mask** applied to the destination to define the network's size.
  - `Flags`:
    - Indicates the route's type.
    - Common flags:
      - `U`: The route is **up (usable)**.
      - `G`: The route **uses a gateway**.
  - `MSS`:
    - `Maximum Segment Size` for TCP connections over this route (`0` means **default**).
  - `Window`:
    - TCP **window size** (unused here).
  - `irtt`:
    - `Initial round-trip time` (unused here, often 0).
  - `Iface`:
    - The **network interface** used for the route.

---

- **Default Route**:

  - `Destination`:
    - `0.0.0.0`
    - default route, meaning all traffic not matching any other route goes here.
  - `Gateway`:
    - `192.168.204.2`
    - next-hop router for traffic to non-local networks.
  - `Genmask`:
    - `0.0.0.0`
    - applies to all addresses.
  - `Flags`: `UG`
    - Up and uses a Gateway.
  - `Iface`:
    - `ens160` and `ens224`
    - two interfaces are configured with the same default gateway.

- **Local Subnet**:
  - `Destination`:
    - `192.168.204.0`
    - local subnet for this interface.
  - `Gateway`:
    - `0.0.0.0`
    - no gateway is needed, directly connected.
  - `Genmask`:
    - `255.255.255.0`
    - covers IPs from 192.168.204.1 to 192.168.204.254.
  - `Flags`: `U`
    - Up, directly reachable.
  - `Iface`:
    - `ens160` and `ens224`
    - both interfaces are on the same subnet.

---

[TOP](#linux---networking-package-net-tools-deprecated)
