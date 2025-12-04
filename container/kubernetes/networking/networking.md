
[Back](../index.md)

Fundamental

- `Switching`

  - the process of transferring data packets from one device to another within the **same network** by using a network switch
  - Connects devices within a **single network** (LAN)
  - OSI Layer: layer 2
  - Uses MAC addresses

- `Routing`

  - the process of selecting a path for data packets to travel across one or more networks from a source to a destination.
  - Connects devices within **different network** (LAN)
  - OSI Layer: layer 3
  - Uses IP addresses

- `gateway`

  - a hardware device or software program that **connects two different networks** with **different protocols**, acting as an **entry and exit point** for data.

- `forwarding`
  - **directing data packets** to their **destination**
  - can be:
    - at the network layer, like a router using a forwarding table
    - at the application layer, like "port forwarding," which redirects traffic through a gateway
  - get the value:
    - `cat /proc/sys/net/ipv4/ip_forward`
    - default 0
  - modify value:
    - `/etc/sysctl.conf`:`net.ipv4.ip_forward = 1`

| Command                            | Description                |
| ---------------------------------- | -------------------------- |
| `ip link`                          | manage interface           |
| `ip a`                             | manage ip                  |
| `ip a add ip_cidr dev if_name`     | Add ip                     |
| `ip r`                             | List route table           |
| `ip r add default via gw_cidr`     | Set a default gateway      |
| `ip r add subnet_cidr via gw_cidr` | Set a gateway for a subnet |

---

## DNS

- `Name Resolution`

  - the process of converting a **human-readable name** (like a website address) into the **numerical IP address** that computers use to communicate.
  - `/etc/hosts`
    - a plain-text file that maps `IP addresses` to `hostnames`

- `DNS server`

  - translates **human-readable domain names** (like "google.com") into **machine-readable IP addresses** (like "\(172.217.164.142\)")
  - acting as the "phone book of the internet".
  - `/etc/resolv.conf`: `nameserver ip_dns_server`

    - a configuration file that tells the system where to find **Domain Name System (DNS) servers**

  - Default order
    - `/etc/nsswitch.conf`: `file dns`
    - local hosts file > DNS server

- `Domain Names`

  - www.google.com
    - `.`: root
    - `.com`: top-level domain
    - `google`: domain
    - `www`: sub-domain

- Process of identify a domain name: `apps.googlecom`
  - query local hosts file
  - query organization DNS server
  - query root DNS server
  - query .com DNS server
  - query Google DNS
  - return the IP
  - cache the ip locally

---

- Search within the organization DNS server
  - `/etc/resolv.conf`
    - `search intermal_domain subdomain_domain`

| Record Type | Description                                                                                                                        |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `A`         | Maps a hostname to an IPv4 address.                                                                                                |
| `AAAA`      | Maps a hostname to an IPv6 address.                                                                                                |
| `CNAME`     | Creates an **alias**, pointing one domain name to another.                                                                         |
| `MX`        | Specifies the **mail servers** responsible for receiving email for a domain.                                                       |
| `NS`        | Points to the authoritative name servers for a domain.                                                                             |
| `PTR`       | Used for reverse **DNS lookups**, resolving an IP address back to a hostname.                                                      |
| `SOA`       | Stores **administrative information** about the `DNS zone`, such as the primary name server and email of the domain administrator. |
| `SRV`       | Specifies the **location** (hostname and port) of a **service**, like a VoIP or instant messaging server.                          |
| `TXT`       | used for verification or email security policies like SPF.                                                                         |

---

| Commoand             | Description                          |
| -------------------- | ------------------------------------ |
| `nslookup host_name` | Query for a hostname from DNS server |
| `dig host_name`      | Query details for a hostname         |

---

Lab:

- Configurate a server dedicated as the DNS server within in large environments with many hostnames and Ips
  - Solution: `CoreDNS`

```sh
# install
curl -LO https://github.com/coredns/coredns/releases/download/v1.12.4/coredns_1.12.4_linux_amd64.tgz
tar -zxf coredns_1.12.4_linux_amd64.tgz
```

```conf
.:53 {
    # Use /etc/hosts to resolve hostname
    hosts /etc/hosts {
        reload 1m
        fallthrough
    }

    # Forward unmatched queries to the host's resolver
    forward . /etc/resolv.conf {
       max_concurrent 1000
    }
    cache 30
    log
    errors
}
```

---

## Network Namespaces

- `namespace`

  - a feature of the Linux kernel that **isolates system resources** for a **group of processes**

- `process namespace`

  - a Linux kernel feature that **isolates a process's view** of system resources,
    - such as process IDs (PIDs), network stack, and mount points, from other processes.
  - Changes within a `process namespace` are only visible to other processes in the **same namespace**
    - processes in **different** `process namespaces` remain **unaware of** those changes.
  - host can view all the processes running in all namespace
    - `ps aux`

- `Network namespaces`

  - used to isolate a system's networking resources, such as network interfaces, IP addresses, routing tables, and firewall rules
  - a `container` within a namespace only can see the `network interfaces`, `routing table`, `ARP tables` within the **same namespace**.

- Interfaces

| Commond                                                       | Description                                |
| ------------------------------------------------------------- | ------------------------------------------ |
| `ip link`                                                     | List all interfaces on the host            |
| `ip -n net_ns_name link`/ `ip netns exec net_ns_name ip link` | List all interfaces of a network namespace |
| `ip netns`                                                    | List all network namespaces                |
| `ip netns add net_ns_name`                                    | Create a network namespace                 |

- arp table

| Commond                         | Description                               |
| ------------------------------- | ----------------------------------------- |
| `arp`                           | List arp table                            |
| `ip netns exec net_ns_name arp` | List arp table within a network namespace |

- Routing

| Commond                           | Description                                   |
| --------------------------------- | --------------------------------------------- |
| `route`                           | List all routing table                        |
| `ip netns exec net_ns_name route` | List routing table within a network namespace |

---

### Lab: Connection between Network Namespace

- Create a `pipe`(`virutal cable`) to connect 2 interfaces of 2 network-namespaces
  - namespace: red
    - virtual cable: veth-red
  - namespace: blue
    - virutal cable: veth-blue

```sh
# create virtual cables
ip link add veth-red type veth peer name veth-blue
# attach virtual cable to a ns
ip link set vetch-red netns red
ip link set vetch-blue netns blue
# assign ip to virtual cables
ip -n red a add 192.168.10.1 dev veth-red
ip -n blue a add 192.168.10.2 dev veth-blue
# bring up virutal cable
ip -n red link set veth-red up
ip -n blue link set veth-blue up
# confirm
ip netns exec red ping 192.168.10.2 # ping from red ns to blue cable
ip netns exec red arp # get arp in ns red
ip netns exec blue arp # get arp in blue red
# confirm from the host
arp # list nothing about the virual cable

# clear up
ip -n red link del veth-red
```

---

### Lab: Create virtual switch network in a host

- Solution: linux bridge / open vswitch
  - this lab: limux bridge
- purpose:
  - create a virtual switch that is attacthed to all network namespace, to enable communication between network namespace.

```sh
# create a new interface
ip link add v-net-0 type bridge
# bring up interface
ip link set dev v-net-0 up
# confirm
ip link

# create virtual cable
ip link add veth-red type tech peer name veth-red-br
ip link add veth-blue type tech peer name veth-blue-br

# attach virtual cable with ns
ip link set veth-red netns red
ip link set veth-blue netns blue

# attch virtual cable with interface(virtual switch)
ip link set veth-red master v-net-0
ip link set veth-blue master v-net-0

# assign ip to virtual cables
ip -n red a add 192.168.10.1 dev veth-red
ip -n blue a add 192.168.10.2 dev veth-blue

# bring up virtual cables
ip -n red link set veth-red up
ip -n blue link set veth-blue up
```

- enable the host to access the virtual network

```sh
# add v-interface to the host namespace
ip a add 192.168.10.5/24 dev v-net-o

# confirm: ping from the host to a network namespace
ping ip_virtual_cable
```

---

### Lab: Enable access from a network namespace to a remote host

- local host: eth0(192.168.1.2), server as the gateway of the network namespace
  - blue network namespace(192.168.10.2)
  - virtual switch: v-net-0(192.168.10.5), has been added to the host namespace
- remote host(192.168.1.3)

```sh
# add gateway to the network namespace
ip netns exec blue ip route add 192.168.1.0/24 via 192.168.10.5 # can access the target subnet via the v-net-0

# enable NAT on the host interface eth0
iptables -t nat -A POSTROUTING -s 192.168.10.0/24 -j MASQUERADE # enable forwarding for the source from the network namespace

# confirm
ip netns exec blue ping 192.168.1.3
```

- enable access the Internet:

```sh
# add the default gw to the namespace
ip netns exec blue ip route add default via 192.168.10.5
# confirm
ip netns exec blue ping 8.8.8.8
```

- Enable external access to the namespace

```sh
# add NAT rule
iptables -t nat -A PREROUTING --dport 80 -to-destination 192.168.10.2:80 -j DNAT
```

---

## Docker Networking

- Environment Setting
  - host
    - eth0(192.168.1.10)

---

### Docker network type

- **Bridge Network:**

  - default network type
  - It creates a `virtual bridge (docker0)` on the host, connecting containers and allowing them to **communicate with each other and the host**.
  - Containers get their own IP addresses **within** the `bridge network`
    - by default
      - ip range: `172.17.0.0/16`
      - network namespace
        - start with `b3165`
        - isolate the containers in the bridge network from the host
      - interface on host:
        - name: `docker0`
        - ip: `172.17.0.1`
        - type: bridge
        - use virtual cable to connect with the host interface to enable communication.
  - External access to containers on a bridge network **requires explicit port mapping** (publishing ports).
  - Use case:
    - Suitable for single-host container communication and small deployments.
  - command:
    - `docker run nginx`

- **None Network:**

  - Provides **complete network isolation** for the container.
  - have **no** network interfaces and **cannot communicate** with other containers or the host.
  - Use case:
    - highly secure workloads
    - testing containers that do not require any network connectivity.
  - command:
    - `docker run --network none nginx`

- **Host Network:**
  - **share the host's network** stack directly,
    - **no** network isolation between the `container` and the `host`.
  - The container uses the **same** `IP` address **as the host**
  - any ports exposed by the `container` are bound directly to the **host**'s network.
    - if the existing contianer in the host network already took up a port, no addional contianer in the host network can take the same port.
  - better **performance** due to the **lack** of a `virtual network layer`, but sacrifices isolation and security.
  - use case:
    - specific cases where direct access to the host network is required.
  - command:
    - `docker run --network host nginx`

---

### Lab: obervation on how docker bridge network

```sh
# list interface on the host
ip link
# 3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    # link/ether 0a:5c:ff:41:6a:a8 brd ff:ff:ff:ff:ff:ff

# list ip
ip a show docker0
# 3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
#     link/ether 0a:5c:ff:41:6a:a8 brd ff:ff:ff:ff:ff:ff
#     inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
#        valid_lft forever preferred_lft forever

# list route
ip r
# default via 172.27.224.1 dev eth0 proto kernel
# 172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
# 172.27.224.0/20 dev eth0 proto kernel scope link src 172.27.224.217

# list namespace
sudo lsns -t net
        # NS TYPE NPROCS PID USER    NETNSID NSFS COMMAND
# 4026531840 net      37   1 root unassigned      /sbin/init

docker run -d --name nginx nginx

docker inspect nginx | grep IPAddress
# "IPAddress": "172.17.0.2",

ping 172.17.0.2
# PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data

curl http://172.17.0.2:80
# curl: (7) Failed to connect to 172.17.0.2 port 80 after 3112 ms: Couldn't connect to server

curl http://localhost:80
# curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server

# port mapping to enable external access
docker rm -f nginx
docker run -d --name nginx -p 8080:80 nginx

curl http://localhost:8080
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
# html { color-scheme: light dark; }
# body { width: 35em; margin: 0 auto;
# font-family: Tahoma, Verdana, Arial, sans-serif; }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>


# NAT to forwarding traffic to docker container
sudo iptables -nvL -t nat
# Chain PREROUTING (policy ACCEPT 5512 packets, 1310K bytes)
#  pkts bytes target     prot opt in     out     source               destination
#     3  3734 DOCKER     0    --  *      *       0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

# Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
#  pkts bytes target     prot opt in     out     source               destination

# Chain OUTPUT (policy ACCEPT 4139 packets, 312K bytes)
#  pkts bytes target     prot opt in     out     source               destination
#    42  2883 DOCKER     0    --  *      *       0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

# Chain POSTROUTING (policy ACCEPT 4139 packets, 312K bytes)
#  pkts bytes target     prot opt in     out     source               destination
#     0     0 MASQUERADE  0    --  *      !docker0  172.17.0.0/16        0.0.0.0/0

# Chain DOCKER (2 references)
#  pkts bytes target     prot opt in     out     source               destination
#     0     0 RETURN     0    --  docker0 *       0.0.0.0/0            0.0.0.0/0
```

---

## Container Networking Interface(CNI)

- CNI

  - a **standard** that specifies how to **configure network interfaces** for containers.
  - responsibility:
    - The container runtime must create **network namespace**
    - identify the **network** to which the container attach
    - invoke Network Plugin(bridge) when container is added/deleted
    - assign ip address to the container
    - output netowork configuration
  - common supported runtime:
    - rkt
    - mesos
    - k8s

- Docker does not support CNI
  - use Container Network Model(CNM)
  - can work around with manaul work with CNI
    - `docker run --network=none nginx`
    - `bridge add con_id /var/run/netns/con_id`

---

## Cluster Node Networking

- Both master and worker nodes must

  - have at least one interface with unique ip and mac addresses
  - have unique hostname

- Port:
  - Master node:
    - `6443` for API server
    - `2379` for etcd
    - `10250` for kubelet if applied
    - `10257`: for controller
    - `10259`: for scheduler
    - `23780`: for etcd client if multiple master nodes applied
  - Worker node:
    - `10250` for kubelet
    - `30,000`~`32,767` for external access


```sh
# command to show the bridge interface which is default interface used by a container runtime
ip a show type bridge
# 6: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1360 qdisc noqueue state UP group default qlen 1000
#     link/ether 62:f0:a2:97:23:27 brd ff:ff:ff:ff:ff:ff
#     inet 172.17.0.1/24 brd 172.17.0.255 scope global cni0
#        valid_lft forever preferred_lft forever
#     inet6 fe80::60f0:a2ff:fe97:2327/64 scope link 
#        valid_lft forever preferred_lft forever

# identify what port is listen on
# schduler
netstat -npl | grep -i scheduler
# tcp        0      0 127.0.0.1:10259         0.0.0.0:*               LISTEN      2878/kube-scheduler

ss -tulp | grep -i scheduler
# tcp   LISTEN 0      4096         127.0.0.1:10259         0.0.0.0:*    users:(("kube-scheduler",pid=2878,fd=3)) 

# count all etcd connection with a specific port
netstat -npa | grep -i etcd | grep -i 2379 | wc -l
# 64
netstat -npa | grep -i etcd | grep -i 2380 | wc -l
# 1
```