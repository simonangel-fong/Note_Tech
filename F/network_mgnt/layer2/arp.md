# Network - Layer2: ARP

[Back](../../index.md)

- [Network - Layer2: ARP](#network---layer2-arp)
  - [Address Resolution Protocol (ARP)](#address-resolution-protocol-arp)

---

## Address Resolution Protocol (ARP)

- `Address Resolution Protocol (ARP)`:
  - a network protocol that connects a device's **IP address** to its **MAC address**

---

- ARP was made a general protocol capable of **resolving addresses from IP to different link layer technologies**

  - Proxy ARP
  - Improved Caching

- Purpose

  - What we have
    - The layer 3 address (**IP address**) + IP datagram
  - What do we want
    - The layer 2 address (**MAC** address most of the time) to build the layer 2 header
  - ARP will help us in **getting the layer 2 (MAC)** address so we can build our layer 2 segment and send it onto the physical network.

- For IPv4 and IPv6
  - ARP for `IPv4` is done through a **broadcast** of all “F”s (**Flooding ARP**) for the unknown destination the system with the correct IP address responds back with it’s ARP address and cashed entries are updated.
- Arp for `IPv6` is performed by the new process named `Neighbor Discovery (ND)`
  - Neighbors refers to the devices on the **local network**
  - The process is very similar to the one used by ARP and IPv4
