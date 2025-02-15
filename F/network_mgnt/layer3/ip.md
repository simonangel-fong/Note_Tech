# Network - Layer3: IP

[Back](../../index.md)

- [Network - Layer3: IP](#network---layer3-ip)
  - [Internet Protocol (IP)](#internet-protocol-ip)
    - [IPv4 Datagram](#ipv4-datagram)
    - [IPv6 Datagram](#ipv6-datagram)
    - [IP Services](#ip-services)
    - [Address](#address)
    - [IPv4 Address (4 billion addresses)](#ipv4-address-4-billion-addresses)
    - [IPv6 Address](#ipv6-address)
  - [IPv4 - Datagram](#ipv4---datagram)
    - [Version - 4 bit](#version---4-bit)
    - [Internet Head Length (IHL) - 4 bit](#internet-head-length-ihl---4-bit)
    - [Type Of Service (TOS)](#type-of-service-tos)
    - [Total Length (TL) - 16bit](#total-length-tl---16bit)
    - [Identification (ID) - 16 bit](#identification-id---16-bit)
    - [Flags - 3 bit](#flags---3-bit)
    - [Fragment Offset - 13 bit](#fragment-offset---13-bit)
    - [Time-to-Live (TTL) - 8 bit](#time-to-live-ttl---8-bit)
    - [Protocols - 8 bit](#protocols---8-bit)
    - [Header Checksum - 16bit](#header-checksum---16bit)
    - [Source Address - 32 bit](#source-address---32-bit)
    - [Destination Address](#destination-address)
    - [Options Field](#options-field)
  - [Encapsulation](#encapsulation)
    - [Fragmentation](#fragmentation)
    - [The Reassembly Process for IPv4](#the-reassembly-process-for-ipv4)
    - [Limitations of IPv4](#limitations-of-ipv4)
  - [IPv6](#ipv6)
    - [Datagram](#datagram)
      - [Version - 4bit](#version---4bit)
      - [Traffic Class - 8 bit](#traffic-class---8-bit)
      - [Flow Label](#flow-label)
      - [Payload Length](#payload-length)
      - [Next Header](#next-header)
      - [Hop Limit](#hop-limit)
      - [Source Address](#source-address)
      - [Destination Address](#destination-address-1)
    - [Addressing – Address Types](#addressing--address-types)
    - [Address Size](#address-size)
    - [Notation](#notation)
    - [Common](#common)
    - [Extension Headers](#extension-headers)
  - [Summary](#summary)

---

## Internet Protocol (IP)

- `IP`

  - a layer 3 protocol
  - IP contains **addressing information** and some control information that enables packets to be **routed**

- IP has 2 main **responsibilities**
  - Providing **connectionless**, best-effort delivery of `datagrams` through an internetwork **without acknowledgment**
  - Providing **fragmentation and reassembly** of `datagrams` to support data links with different maximum transmission unit (MTU) sizes

---

### IPv4 Datagram

![ip4_datagram](./pic/ip4_datagram.png)

- **Version**:
  - IP version used (0100)
- **Type of service:**
  - how an **upper layer protocol** would like the current datagram to be handle
- **Datagram length**:
  - total length of the datagram (**header + payload**)
- **16-bit Identifier**:
  - **Identify the current** datagram
- **Flags**:
  - used to **control fragmentation**
- **Fragmentation offset**:
  - indicates the position of a fragment related to the beginning of the data
- **Time-to-live**:
  - counter to **avoid looping**
- **Protocol**:
  - indicates which **upper layer** protocol is used
- **Options**:
  - allows IP to support options such as **security**
- **Source IP address**:
  - **32-bit** address
- **Destination IP address**:
  - **32-bit** address
- **Data**:
  - payload and data received from upper-layer protocol

---

### IPv6 Datagram

![ip4_datagram](./pic/ip6_datagram.png)

- **Version**:
  - IP version used (0110)
- **Fixed length**:
  - 40 bytes Minimized and simple approach
- **Traffic Class**:
  - used for QoS
- **Flow Label**:
  - identify a **group of datagram**
- **Payload Length**:
  - Only **size** of the payload
- **Next Header**:
  - Identify the type of following data (other IP header or L4 protocol)
- **Hop Limit**:
  - Same as the **Time to live** field in IPv4
- **Source IP address**:
  - **128-bit** address
- **Destination IP address**:
  - **128-bit** address
- **Data**:
  - **payload** and data received from upper-layer protoc

---

### IP Services

- IP Supports 3 Services
  - `Unicast`:one to one
  - `Multicast`: one to many & many to many
  - `Broadcast`: one to many (**IPv4** only)
  - `Anycast`: one to the closet one (**IPv6** only)

---

### Address

- Networks with in the class can be **broken down** in to `subnets`, or **built up** into `supernets`.
  - Two appropriate 24bit subnet can be put together to make a 23bit supernet, where as a 24bit network can be broken down to, up to 64, 30bit networks

### IPv4 Address (4 billion addresses)

![ip4_class](./pic/ip4_class.png)

- **Public** IPv4 Address
  - IP address that are routable on the **internet**
  - IP address you **get from the ISP**
    **Private** IPv4 Address
  - Addresses used in a `Local Area Network (LAN)`
  - **Not routable** on the internet
    - 10.0.0.0 - 10.255.255.255 (10/8 prefix) - Class A
    - 172.16.0.0 - 172.31.255.255 (172.16/12 prefix) - Class B
    - 192.168.0.0 - 192.168.255.255 (192.168/16 prefix) - Class C

---

### IPv6 Address

skip

---

## IPv4 - Datagram

- **Headers** fields are aligned on words of **32-bits**

- Length of header
  - Min 20 bytes (5 words)
  - Max 60 bytes (15 words)

### Version - 4 bit

- Identifies the **version of the IP protocol** used
  - “0100” for IPv4
  - Length of this field: 4 bit
- This field allows us to have multiple versions of the IP protocols (IPv4, IPv6)

### Internet Head Length (IHL) - 4 bit

- Identifies the **length** of the IP **datagram header** in 32-bit words
  - Ex: length of 20 bytes (5 words) = “0101”
  - Ex: length of 60 bytes (15 words) = “1111”
- Length of this field: 4 bits

### Type Of Service (TOS)

- Field carrying information to provide q**uality of service features**
- The original TOS (from RFC 791) has been widely redefined by the RFC 1812 (IP Precedence) and later by RFC 2474 (DiffServ) to better suit modern IP networks

### Total Length (TL) - 16bit

- Specifies the **total length of the IPv4 datagram** (size of **header** + size of **payload**)
  - Minimum size: 576 bytes
  - Maximum size: 65,535 bytes
- Size depends on the L2 protocol MTU (Ex: 1500bytes for Ethernet)
- Length of the field: 16 bits (2 bytes)

### Identification (ID) - 16 bit

- 16 bits number **randomly** generated by the source using an algorithm based on the system clock
- Used to **identify an IP datagram** if **fragmentation** occurs
  - The ID will be copied in every fragments
  - The destination can easily reassemble the fragments looking at the ID
- Length of the field
  - 16 bits (2 bytes)

### Flags - 3 bit

- 3 Bits
- Control flags
  - 2 of them are used for fragmentation
  - 1 is not used
- **Don’t Fragment (DF)**
  - When set to **1**, data should **not be fragmented**.
  - Not often practically used
  - Can be used to test the MTU of a link
- **More Fragment (MF)**
  - When set to 0, indicates the **last** fragment
  - When set to 1, indicates that **more** fragments are coming

### Fragment Offset - 13 bit

- In case of fragmentation, this field indicates the offset, or **position**, in the overall message where the data in this **fragment** goes
- It is specifies in units of 8 bytes (64 bits)
- Length of this field: 13 bits

---

### Time-to-Live (TTL) - 8 bit

- Specifies **how long** the datagram is **allowed to live** in the network
- Every time, the datagram is **routed**, this TTL is **decremented**
- If the TTL field drops to **0**, the datagram is **discarded**
- Length of the field
  - 1 byte (8 bits)
- Examples of default TTL values
  - On **Windows** 7/8/10: TTL = **128**
  - On **Mac** OS X: TTL = **64**

---

### Protocols - 8 bit

- This field indicates what type of **higher-layer** protocol is carried in the data field (payload)
- The values of this field were originally defined by RFC 1700
- They are now maintained by the IANA
- Length of the field: 1 byte (8 bits)

### Header Checksum - 16bit

- Checksum computed over the header
  - Calculating by forming the ones’ components of the ones’ components sum of the headers’ words
- Length of the checksum
  - 2 bytes (16 bits)
- **Recalculated** every time the header is **modified** (fragmentation or change of the TTL value)

---

### Source Address - 32 bit

- IP address of the **originator** of the datagram
- This field **does not change throughout the transmission** of the datagram from the sender to the receiver
- Length of this field
  - 4 bytes (32 bits)
- Usually represented by 4 decimal numbers separated by “.”
  - Ex: 192.168.10.2

### Destination Address

- IP address of the **recipient** of the datagram
- This field **does not change throughout the transmission** of the datagram from the sender to the receiver
- Length of this field
  - 4 bytes (32 bits)
- Usually represented by 4 decimal numbers separated by “.”
  - Ex: 192.168.10.2

### Options Field

- Some options are available in IPv4
- The **length** of this field is **variable** depending on the number of options
- Padding bit (“0”) can be added to align the option field to a multiple of 32 bits (1 word)
- This field adds a lot of complexity in how an IP datagram is handle and is, therefore, **not widely used**

---

## Encapsulation

- Each datagram must be small enough to **fit** into the **Layer 2 payload**
- The size of the layer 2 payload is defined by the `Maximum Transmission Unit (MTU)`
- The MTU is **1500** bytes by default on most devices

### Fragmentation

- **Fragments** the IP datagram so the total length **falls into the MTU specification**
- How does IP knows the MTU is?
  - It uses a mechanism called `Path MTU Discovery` (RFC 1191):

---

### The Reassembly Process for IPv4

- Fragment **recognition** & Fragmented **Message Identification**
  - The recipient knows if the message received is a fragment if the MF =1 or if Offset != 0
  - The recipient identifies the message
- Buffer Initialization
  - **Buffer** used to **store** the in coming fragments of the same message
- Timer Initialization
  - A **timer** is set for the reassembly of the message
  - It ensures that the recipient won’t wait too long for lost fragments
- Fragment **Receipt** & **Processing**
  - Whenever a fragment is **identified** from being part of the same message, it is **added** to the buffer for processing
- Reassembly is finished when the fragment with **MF=0** has been received

---

### Limitations of IPv4

- Number of Addresses
  - Public IPv4 addresses pool is get smaller by the day
- Fragmentation
  - Fragmentation can and will add a lot of **overhead** and complexity
- Security
  - IPsec provides security for IP but is not built-in and optional
- Quality of Service
  - TOS has limited functionality
  - Payload identification is not possible when encrypted

---

## IPv6

### Datagram

- Fixed Length of 40 bytes
  - Simple format
  - `Extension headers` can be **added** for more functionalities

#### Version - 4bit

- Identifies the version of the IP protocol used
  - “0110” for IPv6
- Length of this field
  - 4 bit
- This field is used the **same** way as in IPv4

#### Traffic Class - 8 bit

- Field used for `Quality Of Service (QoS)`
- Equivalent to the T`ype Of Service (TOS)` field in IPv4
- Used using the new Differential Services (DS) method (RFC 2474)
- Length of the field
  - 1 byte (8 bits)

---

#### Flow Label

- Provides additional support for **real-time datagram delivery** and quality of service features (QoS)
- The concept flow was defined in RFC 2460
- A **sequence of datagram** will be identified by the same flow label
- As they travel through an IP network, the routers will apply the same level of QoS to all the datagrams of the same flow
- Length of the field
  - 2,5 bytes (20 bits)

---

#### Payload Length

- Identifies the **length** of the datagram **payload**
- The length of **some optional extension** headers will be **included**
- Since the size of the **header** is fixed, it is **not included** in this field (Different from IPv4)
- Length of this field
  - 2 bytes (16 bits)

#### Next Header

- When **extension headers** are used, this field specifies the **identity** of the **first** extension header
- When extension headers are **not** used, this field is the same as the Protocol field in IPv4
- Note: New protocol numbers has been added in IPv6
- Length of this field
  - 1 byte (8 bits)

---

#### Hop Limit

- This field **replaces** the `TTL` field in IPv4
- The name better reflects how the field is used (It is **calculating hops and not time**)
- Specifies how long the datagram is allowed to live in the network
- Every time, the datagram is **routed**, Hop Limit is **decremented**
- If the field drops to **0**, the datagram is **discarded**
- Length of the field
  - 1 byte (8 bits)

#### Source Address

- The **128-bit** IPv6 address of the **originator** of the datagram
- As in IPv4, this field **does not change as the datagram is travelling** across the network
- Length of this field
  - 16 bytes (128 bits)

#### Destination Address

- The **128-bit** IPv6 address of the intended **recipient** of the datagram (unicast, anycast or multicast)
- As in IPv4, this field does **not change as the datagram is travelling** across the network
- Length of this field
  - 16 bytes (128 bits)

---

### Addressing – Address Types

- IPv6 supports 3 types of addresses
  - `Unicast` addresses (1:1)
    - Defines a **single destination**
  - `Anycast` addresses (1:anycast addresses)
    - Defines the **closest member** of a group
  - `Multicast` addresses (1:**multicast** addresses)
    - Any members of a group
- There is **no broadcast** addresses in IPv6, instead multicast is used in most cases.

---

### Address Size

- **128bit** long
- Usually grouped into **8 sets** of 4 x 4 bits (8 groups of 2 bytes using hex numbers)
- Address Space
  - 2128 = 3.4\*1035 addresses
  - 340,282,366,920,938,463,374,607,431,768,211,456 IP addresses!!
  - Equivalent to many millions of addresses per human on the planet
- Why were the IPv6 addresses made so large?
  - It provides flexibility
    - Allows us to divide the address space and assign various purpose to different bit ranges while still no having to worry about running out of space
- It allowed us to have a simpler protocol
  - We got **rid of the class-oriented addressing** used in IPv4 because we have enough addresses
  - `NAT` are **not** used as much in IPv6

---

### Notation

- The **dotted decimal** notation is **not** used for IPv6 addresses (It would be too long to write addresses and complicated to read)
  - example: 128.33.154.88.31.220.0.0.0.0.67.176.58.98.151.45
- **Hexadecimal notation** is used instead
  - example : FE80:0000:0000:0000:0202:B3FF:FE1E:8329
- **Leading zeros** can be **suppressed** in the notation
  - example : FE80:0:0:0:202:B3FF:FE1E:8329
- **Zero Compression**
  - A string of continuous “0”(zeros) can be replaced by “::”
  - This can only appear once in the address
  - **Brackets** shall be used if a **port** is specified after the address
- Examples
  - FF00:4501:0:0:0:0:0:32 → FF00:4501::32
  - 805B:2D9D:DC28:0:0:FC57:0:0 → 805B:2D9D:DC28::FC57:0:0
  - 0:0:0:0:0:0:0:1 → ::1 (this is the loopback address in IPv6)
  - Address with **port**: `[FF00:4501::32]:443`

---

### Common

- **Private** Addresses
  - They start with “1111 1100” (or **FC**::/7 in Hexa)
  - **Site-Local**
    - Have a **scope** of an entire organization. Begins with “1111 1110 1100” (or FEC::/10)
  - **Link-Local**
    - Have a **scope** of a **physical** network. Begins with “1111 1110 1000” (or FE80::/10)
- The **loopback** address is `::1`
- The unspecified address is `::0` and is used when a device does **not know its address**

---

### Extension Headers

- Several `extension headers` are **available** in IPv6:
  - Hop-by-Hop Options
  - Routing
  - Fragment
  - Encapsulating Security Payload (ESP)
  - Authentication Header (AH)
  - Destination Options
- **Multiple** Extension Headers **can be used** for 1 datagram
- Next Header (8 bits)
  - Protocol number or next header
- Fragment Offset (13 bits)
  - Position in the overall message
  - Specifies in unit of 8 bytes (64 bits)
- `More Fragment` or `MF` (1 bits)
  - Same as the MF field in IPv4
- Identification (32 bit)
  - 32-bit ID used to link this fragment to the overall message

---

## Summary

- `Ip`:
  - logical address
  - route
- `Datagrams`: larger data sequences

  - Structure
    - `Flags`:used to **control fragmentation**
      - Don’t Fragment (DF)
      - More Fragment
    - `Fragmentation offset`: **indicates the position**
    - **TTL/Hop Limit**: routed, this TTL is decremented
      - win: 128
      - mac: 64
    - `IP address`: 32-bit / 128-bit
    - `Data`: payload

- Ipv6

  - Notation:8:
  - loopback address is ::1
  - Extension Headers: Multiple, Fragment Offset,More Fragment or MF

- **Encapsulation**
  - Each datagram must be **small enough to fit into** the Layer 2 **payload**, defined by the `Maximum Transmission Unit (MTU)`
  - 1500 bytes by default
- **Fragmentation**
  - Fragments the IP datagram so the total length falls into the **MTU specification**
- Service:

  - `Unicast`:one to one
  - `Multicast`: one to many & many to many
  - `Broadcast`: one to many (**IPv4** only)
  - `Anycast`: one to the closet one (**IPv6** only)

- Address
  - `subnets`
  - lan class:
    - A: 10. /8
    - B 172.16-172.31 /16
    - C 192.168 - 192.168 /24
