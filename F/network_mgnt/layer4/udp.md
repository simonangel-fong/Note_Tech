# Network - Layer4: UDP

[Back](../../index.md)

- [Network - Layer4: UDP](#network---layer4-udp)
  - [UDP – General Presentation](#udp--general-presentation)
  - [Basic UDP Mechanisms](#basic-udp-mechanisms)
  - [Datagram](#datagram)
    - [Datagram Headers](#datagram-headers)
    - [Pseudo Header](#pseudo-header)
    - [When do we use UDP](#when-do-we-use-udp)
  - [Summary](#summary)

---

## UDP – General Presentation

- `User Datagram Protocol`
  - **Layer 4** protocol → **transport** protocol
  - **Connectionless** transport protocol
- Main features of UDP
  - Low **overhead** generated (a.k.a. simple)
  - Low **latency** (a.k.a. fast)
  - **65535** bytes payload **minus headers**

---

## Basic UDP Mechanisms

- `UDP` is designed to do as little as possible
- What UDP does
  - Take data from **upper** layer and forward **down** to the `IP (layer 3)` for **transmission**
  - That’s it !
- The basic steps for transmission using UDP are
  - Higher-layer **data transfer**
    - An application sends a message to the **UDP software**
- UDP message **encapsulation**
  - The higher-layer message is **encapsulated** into the `Data field` of a UDP message.
  - The headers of the UDP messages are **filled** including the **Source Port** of the application and the **destination Port** of the intended recipient
  - The **checksum** value **may** also be calculated
- **Transfer** message to IP
  - The UDP message is **passed to IP for transmission**

---

- What UDP does NOT do:
  - UDP does **not establish connections** before sending data. It just packages it and… off it goes
  - UDP does **not provide acknowledgments** to show that data was received (Connection-less protocol)
  - UDP does **not provide any guarantees** that its messages will **arrive**
  - UDP does **not detect lost** messages and **retransmit** them
  - UDP does **not ensure** that data is received in the **same order** that they were sent
  - UDP does **not** provide any mechanism to **manage the flow** of data between devices, or handle **congestion**

---

## Datagram

### Datagram Headers

- **Source Port**
  - **Optional** field (If not used a value of 0 is used)
  - Indicates the port of the sending process
  - Length: 16 bits
- **Destination Port**
  - **Port number** of the process that is the ultimate intended recipient of the message on the destination device
  - This will usually be a **well-known/registered port number**
  - Length: 16 bits
- **Length**
  - The length of the entire UDP datagram **including** the header and the payload (Data Field)
  - Length of this field: 16 bits
- **Checksum**
  - This field is **optional**
  - Computed of the entire UDP datagram **plus** a special pseudo header
  - Length of this field: 16 bits

---

### Pseudo Header

- The `pseudo header` conceptually **prefixed** to the UDP header contains
  - The **source** address,
  - The **destination** address,
  - The **protocol**
  - The UDP **length**.
- This information gives **protection against misrouted datagrams**.
- This checksum procedure is the same as is used in TCP

---

### When do we use UDP

- Data where **performance is more important** than completeness
  - **Multimedia** applications (Video/Audio streaming…)
- Data **exchanges** that are **Short and Sweet**
  - **Management** protocols (syslog, SNMP, NTP…)
- If **multicast** is need

  - UDP would be the de facto Layer 4 protocol used for **multicast** applications

---

## Summary

- User Datagram Protocol
  - Connectionless， fast， large payload 65535
  - checksum value may also be calculated
  - No connection, ack
- Datagram

  - Src port( optional)
  - dst Port
  - Checksum(optional)

- Pseudo Header

  - against misrouted

- Use case:
  - Multimedia app
  - Multicase \ performance
