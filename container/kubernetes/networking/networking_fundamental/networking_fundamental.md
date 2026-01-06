# Kubernetes Networking: Fundamental

[Back](../../index.md)

- [Kubernetes Networking: Fundamental](#kubernetes-networking-fundamental)
  - [Networking Fundamental](#networking-fundamental)
    - [Terminology](#terminology)
    - [Common Commands](#common-commands)
  - [Domain Name System(DNS)](#domain-name-systemdns)
    - [DNS Type](#dns-type)
    - [Common Commands](#common-commands-1)
  - [Network Namespaces](#network-namespaces)
    - [Common Commands](#common-commands-2)
    - [Lab: Connection between Network Namespace](#lab-connection-between-network-namespace)
    - [Lab: Create virtual switch network in a host](#lab-create-virtual-switch-network-in-a-host)
    - [Lab: Enable access from a network namespace to a remote host](#lab-enable-access-from-a-network-namespace-to-a-remote-host)
  - [Docker Networking](#docker-networking)
    - [Bridge Network](#bridge-network)
    - [None Network](#none-network)
    - [Host Network](#host-network)
    - [Lab: obervation on how docker bridge network](#lab-obervation-on-how-docker-bridge-network)
  - [Kubernetes Networking](#kubernetes-networking)
    - [Cluster Node Networking](#cluster-node-networking)
    - [Container Networking Interface(CNI)](#container-networking-interfacecni)
    - [Pod Networking](#pod-networking)
    - [Solution: `WeaveWork`](#solution-weavework)
  - [Lab:](#lab)
  - [IP Address Mangement(IPAM)](#ip-address-mangementipam)
    - [Lab: Flannel](#lab-flannel)

---

## Networking Fundamental

### Terminology

- `Switching`

  - the process of **transferring** data packets from one **device** to another within the **same network** by using a `network switch`
  - Connects devices within a **single network** (LAN)
  - OSI Layer: `layer 2`
  - Uses `MAC addresses`

- `Routing`

  - the process of **selecting a path** for data packets to travel across **one or more networks** from a source to a destination.
  - Connects devices within **different network** (LAN)
  - OSI Layer: `layer 3`
  - Uses `IP addresses`

- `gateway`

  - a **hardware device** or **software program** that **connects two different networks** with **different protocols**, acting as an **entry and exit point** for data.

- `forwarding`
  - **directing data packets** to their **destination**
  - can be:
    - at the `network layer`, like a `router` using a **forwarding table**
    - at the `application layer`, like "port forwarding," which redirects traffic through a gateway
  - get the value:
    - `cat /proc/sys/net/ipv4/ip_forward`
    - default 0
  - modify value:
    - `/etc/sysctl.conf`:`net.ipv4.ip_forward = 1`

---

### Common Commands

| Command                            | Description                    |
| ---------------------------------- | ------------------------------ |
| `ip link`                          | manage **interface**           |
| `ip a`                             | manage **ip**                  |
| `ip a add ip_cidr dev if_name`     | Add ip                         |
| `ip r`                             | List route table               |
| `ip r add default via gw_cidr`     | Set a **default gateway**      |
| `ip r add subnet_cidr via gw_cidr` | Set a **gateway** for a subnet |

---

## Domain Name System(DNS)

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

- Process of identify a domain name: `apps.google.com`

| Step | Entity               | Action                                                                |
| ---- | -------------------- | --------------------------------------------------------------------- |
| 1    | Browser/OS           | **Checks local** `hosts` file and **local** `DNS cache`.              |
| 2    | Resolver             | `ISP server` receives the request and starts the lookup.              |
| 3    | `Root Server`        | Directs the Resolver to the `.com` `TLD(Top Level Domain) servers`.   |
| 4    | `TLD Server`         | Directs the Resolver to Google's specific `Name Servers`.             |
| 5    | Authoritative Server | Provides the specific `IP address` for apps.google.com.               |
| 6    | Client               | Receives IP, caches it, and initiates the connection (TCP Handshake). |

- Search **within the organization DNS server**
  - `/etc/resolv.conf`
    - `search intermal_domain subdomain_domain`

---

### DNS Type

| Record Type | Description                                                                                                                        |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `A`         | Maps a hostname to an **IPv4** address.                                                                                            |
| `AAAA`      | Maps a hostname to an **IPv6** address.                                                                                            |
| `CNAME`     | Creates an **alias**, pointing one domain name to another.                                                                         |
| `MX`        | Specifies the **mail servers** responsible for receiving email for a domain.                                                       |
| `NS`        | Points to the `authoritative name servers` for a domain.                                                                           |
| `PTR`       | Used for reverse **DNS lookups**, resolving an `IP address` back to a `hostname`.                                                  |
| `SOA`       | Stores **administrative information** about the `DNS zone`, such as the primary name server and email of the domain administrator. |
| `SRV`       | Specifies the **location** (hostname and port) of a **service**, like a VoIP or instant messaging server.                          |
| `TXT`       | used for verification or email security policies like SPF.                                                                         |

---

### Common Commands

| Commoand             | Description                          |
| -------------------- | ------------------------------------ |
| `nslookup host_name` | Query for a hostname from DNS server |
| `dig host_name`      | Query details for a hostname         |

---

- Example: install coredens

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

  - used to **isolate** a system's **networking resources**
    - e.g., `network interfaces`, `IP addresses`, `routing tables`, and `firewall rules`
  - a `container` within a `namespace` only can see the `network interfaces`, `routing table`, `ARP tables` within the **same namespace**.

---

### Common Commands

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

### Bridge Network

- **default** network type
- It creates a `virtual bridge (docker0)` on the host, connecting containers and allowing them to **communicate with each other and the host**.
- Containers get their own IP addresses **within** the `bridge network`
  - by default
    - ip range: `172.17.0.0/16`
    - **network namespace**
      - start with `b3165`
      - **isolate** the containers in the `bridge network` from the host
    - **interface** on host:
      - name: `docker0`
      - ip: `172.17.0.1`
      - type: bridge
      - use `virtual cable` to connect with the `host interface` to enable communication.
- External access to containers on a `bridge network` **requires explicit port mapping** (publishing ports).
- Use case:
  - Suitable for single-host container communication and small deployments.

---

- Common command

| Command                                                          | Description                            |
| ---------------------------------------------------------------- | -------------------------------------- |
| `docker network create -d bridge net_bridge`                     | Create a bridge network                |
| `docker run -d --name web --network=net_bridge -p 8080:80 nginx` | Run a container using a bridge network |

---

### None Network

- Provides **complete network isolation** for the container.
- have **no** network interfaces and **cannot communicate** with other containers or the host.
- Use case:
  - highly secure workloads
  - testing containers that do not require any network connectivity.

---

- Common command

| Command                                                         | Description                          |
| --------------------------------------------------------------- | ------------------------------------ |
| `docker run -d --name busybox --network=none busybox sleep 600` | Run a container using a none network |

---

### Host Network

- **share the host's network** stack directly,
  - **no** network isolation between the `container` and the `host`.
- The container uses the **same** `IP` address **as the host**
- any ports exposed by the `container` are bound directly to the **host**'s network.
  - if the existing contianer in the host network already took up a port, no addional contianer in the host network can take the same port.
- better **performance** due to the **lack** of a `virtual network layer`, but sacrifices isolation and security.
- use case:
  - specific cases where direct access to the host network is required.
- command:
  - `docker run -d --name busybox --network host busybox sleep 600`

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

## Kubernetes Networking

- Each `Node` has **IP address**
- Each `Pod` has its **internal IP address**

  - default range: `10.244.0.0/16`

- `Cluster Networking`:

  - **Pod-to-Pod Communication**:

    - `Pods` can communicate with each other **directly via IP addresses**.
    - Each `Pod` gets **its IP address**, and communication between `Pods` within the **same cluster** is efficient and fast.

  - **Service Abstraction**:
    - Kubernetes **abstracts `Pods` behind a `Service`**, which provides a **stable** **IP address** and **DNS name** for a set of `Pods`.
    - `Services` enable **load balancing** and **discovery** within the cluster.

---

- Example:

  - Node A:

    - IP: `192.168.1.2`
    - Internal Network: `10.244.0.0/16`
      - Pod: `10.244.0.2`

  - Node B:
    - IP: `192.168.1.3`
    - Internal Network: `10.244.0.0/16`
      - Pod: `10.244.0.2`

- Need networking routing to enable communication between node/pod **without NAT**.

---

### Cluster Node Networking

- Both `master` and `worker` nodes must

  - have **at least one** `interface` with **unique** `ip` and `mac addresses`
  - have **unique** `hostname`

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

---

### Container Networking Interface(CNI)

- `Container Networking Interface(CNI)`

  - a **standard** that specifies how to **configure network interfaces** for containers.
  - responsibility:
    - The `container runtime` must create **network namespace**
    - identify the **network** to which the container attach
    - invoke `Network Plugin(bridge)` when container is added/deleted
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

- `/opt/cni/bin`
  - **defalt path** for container runtime to find the CNI plugin
- `/etc/cni/net.d`
  - the path to determine which plugin to use
  - if multiple, choice by order

---

### Pod Networking

- **Pod Networking Model**

  - Each `Pod` should have an **IP address**
  - Each `Pod` should be able to **communicate** with other `Pod` **in the same node**
  - Each `Pod` can communicate with **other `Pod`** on **other nodes without NAT**.

- common solution:
  - flanel
  - cilium
  - nsx

---

- Step1: assign ip and enable communication in the same node

- Lan(192.168.1.0)
  - node01, 192.168.1.11
    - bridge network interface, `v-net-0`
    - subnet, 10.244.1.0/24
    - container run:
      - create and attach virtual swith
      - assign contianer ip
      - set container route
      - =>: each node has ip, and can communicate via virtual switch

---

- Step2: enable node01 talk to node02

  - Lan(192.168.1.0)

    - node01, 192.168.1.11
      - subnet, 10.244.1.0/24
      - v-switch: 10.244.1.1
      - pod01: 10.244.1.2
      - pod02: 10.244.1.3
    - node02, 192.168.1.12
      - v-switch: 10.244.2.1
      - pod01: 10.244.2.2

  - setup a default gateway for each node: 10.244.0.0/16 and manage a central routing table.

---

- All the above are manage by CNI automatically

---

### Solution: `WeaveWork`

- install agent on each node, responsible for:

  - create bridge interface
  - assign IP for each pod
  - manage routing for pods communication
  - manage NAT to forward traffice to another node

- Deploy weave
  - deploy as a daeamonSet
    - a pod act as an agen on each node, implementing CNI

---

## Lab:

- Get the runtime endpoint

```sh
# get conf file from kubelet process
ps -aux | grep -i kubelet | grep config
# bad data in /proc/uptime
# root        3572  0.0  0.1 2988188 83332 ?       Ssl  18:11   0:16 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --pod-infra-container-image=registry.k8s.io/pause:3.10.1

cat /var/lib/kubelet/config.yaml | grep -i containerRuntimeEndpoint
# containerRuntimeEndpoint: unix:///var/run/containerd/containerd.sock
```

- List all CNI binaries

```sh
# all CNI plugin path: /opt/CNI/bin
ls -hl /opt/cni/bin
# total 90M
# -rwxr-xr-x 1 root root 4.5M Dec 11  2024 bandwidth
# -rwxr-xr-x 1 root root 5.1M Dec 11  2024 bridge
# -rwxr-xr-x 1 root root  13M Dec 11  2024 dhcp
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 dummy
# -rwxr-xr-x 1 root root 5.1M Dec 11  2024 firewall
# -rwxr-xr-x 1 root root 2.4M Dec  3 18:11 flannel
# -rwxr-xr-x 1 root root 4.6M Dec 11  2024 host-device
# -rwxr-xr-x 1 root root 3.9M Dec 11  2024 host-local
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 ipvlan
# -rw-r--r-- 1 root root  12K Dec 11  2024 LICENSE
# -rwxr-xr-x 1 root root 4.0M Dec 11  2024 loopback
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 macvlan
# -rwxr-xr-x 1 root root 4.5M Dec 11  2024 portmap
# -rwxr-xr-x 1 root root 4.9M Dec 11  2024 ptp
# -rw-r--r-- 1 root root 2.3K Dec 11  2024 README.md
# -rwxr-xr-x 1 root root 4.2M Dec 11  2024 sbr
# -rwxr-xr-x 1 root root 3.5M Dec 11  2024 static
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 tap
# -rwxr-xr-x 1 root root 4.1M Dec 11  2024 tuning
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 vlan
# -rwxr-xr-x 1 root root 4.3M Dec 11  2024 vrf

# get the CNI in use
ls -hl /etc/cni/net.d
# total 4.0K
# -rw-r--r-- 1 root root 292 Dec  3 18:12 10-flannel.conflist

# get the binary to be run when a container is created
cat /etc/cni/net.d/10-flannel.conflist
# {
#   "name": "cbr0",
#   "cniVersion": "0.3.1",
#   "plugins": [
#     {
#       "type": "flannel",
#       "delegate": {
#         "hairpinMode": true,
#         "isDefaultGateway": true
#       }
#     },
#     {
#       "type": "portmap",
#       "capabilities": {
#         "portMappings": true
#       }
#     }
#   ]
# }

```

---

## IP Address Mangement(IPAM)

- `IP Address Mangement(IPAM)`

  - a method and software for planning, tracking, and managing a network's Internet Protocol (IP) addresses.

- CNI built-in plugin for IPAM
  - `DHCP`
  - `host-local`
- Can be configure within the conf file of the CNI
  - `ipam` field

### Lab: Flannel

```sh
# get the flannel daemonSet
kubectl get daemonset -A
# NAMESPACE      NAME              DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-flannel   kube-flannel-ds   1         1         1       1            1           <none>                   18m
# kube-system    kube-proxy        1         1         1       1            1           kubernetes.io/os=linux   18m

# delete flannel
kubectl delete daemonset -n kube-flannel kube-flannel-ds
# daemonset.apps "kube-flannel-ds" deleted from kube-flannel namespace

# get the flannel configMap
kubectl get configmap -n kube-flannel
# NAME               DATA   AGE
# kube-flannel-cfg   2      20m
# kube-root-ca.crt   1      20m

# delete flannel configmap
kubectl delete configmap -n kube-flannel kube-flannel-cfg
# configmap "kube-flannel-cfg" deleted from kube-flannel namespace

# list flannel conf file
ls /etc/cni/net.d/  # verify files
# 10-flannel.conflist
sudo rm -rf /etc/cni/net.d/*
```

- Install Calico CNI
  - ref: https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart

```sh
# Install Calico
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/tigera-operator.yaml
# namespace/tigera-operator created
# serviceaccount/tigera-operator created
# clusterrole.rbac.authorization.k8s.io/tigera-operator-secrets created
# clusterrole.rbac.authorization.k8s.io/tigera-operator created
# clusterrolebinding.rbac.authorization.k8s.io/tigera-operator created
# rolebinding.rbac.authorization.k8s.io/tigera-operator-secrets created
# deployment.apps/tigera-operator created
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "Installation" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "APIServer" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "Goldmane" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "Whisker" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml
# installation.operator.tigera.io/default created
# apiserver.operator.tigera.io/default created
# goldmane.operator.tigera.io/default created
# whisker.operator.tigera.io/default created

kubectl get tigerastatus
# NAME        AVAILABLE   PROGRESSING   DEGRADED   SINCE
# apiserver                             True
# calico                                True
# goldmane                              True
# ippools                               True
# whisker                               True
```
