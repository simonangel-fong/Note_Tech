# Network - App layer: TFTP

[Back](../../index.md)

- [Network - App layer: TFTP](#network---app-layer-tftp)
  - [`TFTP`](#tftp)
    - [Operation](#operation)
  - [Summary](#summary)

---


## `TFTP`

- `TFTP`

  - `Trivial FTP`
  - a simple protocol for transferring files
  - on top of the `UDP`
  - port number `69`
  - designed to be **small and easy to implement**
    - lacks most of the advanced features offered by more robust `file transfer protocols (FTP/SFTP)`

- TFTP **only reads and writes files** from or to a remote server.
  - It **cannot** list, delete, or rename files or directories
  - it has no provisions for user **authentication**
- Today TFTP is generally **only used** on `local area networks (LAN)`
  - TFTP supports other services like `Bootstrap Protocol (BOOTP)`, `(Peer exchange)PEX`, & `Boot Service Discovery Protocol (BSDP)`

---

### Operation

- The `TFTP client` then **sends** a `read request (RRQ)` or **sends** a `write request (WRQ)`
  - TFTP **splits** a file, to be transferred,** into blocks** of size **512 bytes (default)**
  - Each `TFTP DATA block` is **numbered** and carried inside separate `UDP messages`
  - The **last block** of a file is always sent with a size **lesser than** `512`.
- When the peer receives a block with size **less than 512 bytes**, it treats that block as the **last block**

- **Reliability**:

  - Each **block** is **numbered** and sent inside a separate UDP message. Since TFTP uses UDP, reliable **delivery of each block is not guaranteed** by the underlying network protocols.
    - So, `TFTP` itself takes care of reliability by **requiring the peer** to **acknowledge each successfully received block**.

- **Flow Control**:

  - `TFTP` sends data block by **block**. After sending a block, the sending end **starts a block timer**.
    - If an **acknowledgment** is received for the block from the peer **before the timer expires**, then the **next block** of the file is **sent**.
    - Otherwise, the current block is **resent** as soon as the block timer expires and the whole process **repeats** itself **till the block is successfully acknowledged**.
  - Hence, `TFTP` is basically a **stop and wait protocol** and `flow control` is achieved **by the sender sending at most one outstanding block** at any instant of time. 受控于发送方在某一时刻能发送多少未完成的块。

---

## Summary

- TFTP: 69/udp
  
- TFTP **splits** a file, to be transferred,into **blocks of size 512 bytes (default)**
- **last** block of a file is always sent with a size **lesser** than 512.

- Reliability:
  - by requiring the peer to **acknowledge** each successfully received block.
- Flow control
  TFTP is basically a **stop and wait** protocol and flow control is achieved **by the sender** sending at most one outstanding block at any instant of time. 受控于发送方在某一时刻能发送多少未完成的块。

