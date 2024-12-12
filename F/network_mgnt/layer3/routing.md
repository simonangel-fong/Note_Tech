# Network - Lay3: Routing Protocol

[Back](../../index.md)

- [Network - Lay3: Routing Protocol](#network---lay3-routing-protocol)
  - [Routing Protocols](#routing-protocols)
    - [Routing](#routing)
      - [Routing Protocols](#routing-protocols-1)
        - [Interior Gateway Protocol](#interior-gateway-protocol)
        - [Routing Information Protocol (RIP)](#routing-information-protocol-rip)
      - [IGP - Open Shortest Path First (OSPF)](#igp---open-shortest-path-first-ospf)
      - [IGP - Enhanced / Interior Gateway Routing Protocol (IGRP/EIGRP)](#igp---enhanced--interior-gateway-routing-protocol-igrpeigrp)
  - [Border Gateway protocol](#border-gateway-protocol)
  - [Summary](#summary)

---

## Routing Protocols

### Routing

- `Routing` is the process of **finding a path to transfer** an IP `datagram` from the source to the destination
- Routing is done **by routers** which uses **routing tables** to route the traffic
- Routers always route according to the **destination IP address** located in the `IP datagram`

---

#### Routing Protocols

- `Routing protocols` learn about available routes, **build routing tables** and help taking routing decision
- Routing protocols are used to help to **dynamically update routing information** among multiple routers

- 2 main types of routing protocols

  - **Interior Gateway Protocols**
    - `Interior Gateway Routing Protocols (IGRP)`
    - `Routing Information Protocol (RIP & RIP2)`
    - `Open Shortest path First (OSPF)`
    - `Enhanced Interior Gateway Routing Protocols (EIGRP)`
  - **Exterior Gateway Protocols**
    - `Border Gateway Protocol (BGP)`
    - `Multiprotocol Extensions for BGP (MBGP)`

- `Autonomous Systems`
  - a collection of **networks** under a **common administration**
    - IGP: Intra-AS routing protocol
    - EGP: Inter-AS routing protocol

---

##### Interior Gateway Protocol

- There are multiple types of IGP
- **Distance-vector routing protocol**

  - Use of Bellman-Ford algorithm to calculate the shortest path
  - Each routers populates its **routing table** until the network **converge to stable values**
  - Example:
    - `Routing Information Protocol (RIP)`,
    - `Interior Gateway Routing Protocol(IGRP)`

- **Link-state routing protocol**

  - Each router posses information about the **entire** network topology
  - Each router **independently calculate the best** next hop
  - Information about the links are **shared** among the routers
  - Example:
    - `Open Shortest Path First (OSPF)`,
    - `Intermediate system to intermediate system (IS-IS)`

- **Hybrid routing protocol**
  - **Both** features of a distance-vector and link-state routing protocols
  - Examples:
    - `Enhanced Interior Gateway Routing Protocol (EIGRP)`

---

##### Routing Information Protocol (RIP)

- RIP uses **distance vectors (DV)** to identify the **best path** to a given destination address
- `Routing tables` gets **updated and shared** dynamically when the topology changes
  - `RIPv2` defined in RFC 2453 is used for IPv4 networks
  - `RIP-NG` defined in RFC 2080 is used for IPv6 networks

---

#### IGP - Open Shortest Path First (OSPF)

- `OSPF` is a **link-state** protocol - Link-state information is **shared** among the routers of a **same area**
- The SPF algorithm is used to calculate the shortest path to each node
- OSPF versions
  - `OSPF v2` defined in RFC 2328 is used for IPv4 networks
  - `OSPF v3` defined in RFC 5340 is used for IPv6 networks
- Routers are organized in **different Areas**

- Once router is **initialized**, it uses OSPF **Hello packet** to acquire neighbors- Neighbor routers send an **Hello packet back**; Hello packets also act as keep alive
- Following the **Hello process**, a **designated router** is elected
- SPF places each routers at a top of a tree and calculate the shortest path to each destination based on the link costs
- **Link State Advertisements (LSA)** are exchanged between routers to share topology updates

---

#### IGP - Enhanced / Interior Gateway Routing Protocol (IGRP/EIGRP)

- Until recently a Cisco proprietary protocol
- Fast at maintaining routing tables (when changes are made) but not as chatty as RIP. - It sends routing updates only **when network topology changes** instead of its entire routing table at regular intervals.
- Maintains multiple tables like OSPF
  - Neighbor Tables
  - Topology Tables
  - Routing Tables
- Has multiple parameters for finding the best route such as:
  - Speed
  - Reliability
  - Hop count
  - Metric
- It supports `classless interdomain routing (CIDR)` and `variable-length subnet masks (VLSM)`
- It is **less CPU** intensive.
- It supports IPX and AppleTalk. OSPF supports only IP.
- EIGRP supports unequal-cost load balancing.
- OSPF propagates network changes to all routers in an area. EIGRP has much better convergence time than OSPF/ISIS

---

## Border Gateway protocol

略 p30

---

## Summary

- `Routing`:
  - finding a path to transfer an IP `datagram`
  - by routers using routing tables
- `Routing protocol`

  - govern how routers communicate with each other to direct data packets through a network.

- 2 main types
  - **Interior Gateway Protocols**
    - `Interior Gateway Routing Protocols (IGRP)` - Distance
    - `Routing Information Protocol (RIP & RIP2)`- Distance
    - `Open Shortest path First (OSPF)` - Link
    - `Enhanced Interior Gateway Routing Protocols (EIGRP)` - Hybrid
  - **Exterior Gateway Protocols**
    - `Border Gateway Protocol (BGP)`
    - `Multiprotocol Extensions for BGP (MBGP)`
