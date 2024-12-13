# F

[Back](../index.md)

- Web Security

  - [Wk01](./web_security/wk01.md)
  - [Wk02 - Mark Up Languages](./web_security/wk02.md)
  - [Wk03 - JavaScript & Web Browsers](./web_security/wk03.md)
  - [Wk04 - Classification & Prioritization](./web_security/wk04.md)
  - [Wk05 - Web App Enumeration & HTTP](./web_security/wk05.md)
  - [Wk06 - Server-Side Languages](./web_security/wk06.md)
  - [Wk07 - SQL Injection & Prevention](./web_security/wk07.md)
  - [Wk08 - Sessions, Cookies & Authentication](./web_security/wk08.md)
  - [Wk09 - Web Application Firewalls](./web_security/wk09.md)
  - [Wk10 - Automation](./web_security/wk10.md)
  - [Wk11 - Social Media & The Dark Web](./web_security/wk11.md)

- Securing Servers

  - [WK01](./securing_servers/wk01.md)
  - [WK02](./securing_servers/wk02.md)
  - [WK03](./securing_servers/wk03.md)
  - [WK04](./securing_servers/wk04.md)
  - [WK05 - Access Management, BItlocker](./securing_servers/wk05.md)
  - [WK06 - AD, FIM](./securing_servers/wk06.md)
  - [WK07 - Key Distribution，Kerberos](./securing_servers/wk07.md)
  - [WK08 - NPS](./securing_servers/wk08.md)

- Securing Edge

  - [Wk01](./securing_edge/wk01.md)
  - [Wk02](./securing_edge/wk02.md)
  - [Wk03](./securing_edge/wk03.md)
  - [Wk04](./securing_edge/wk04.md)
  - [CP01](./securing_edge/wk05.md)
  - [CP02](./securing_edge/wk06.md)
  - [CP03](./securing_edge/wk07.md)
  - [CP04](./securing_edge/wk08.md)
  - [pf01](./securing_edge/pf01.md)
  - [pf02](./securing_edge/pf02.md)
  - [pf03](./securing_edge/pf03.md)

- Securing Network

  - [Wk01](./securing_network/wk01.md)
  - [Wk02](./securing_network/wk02.md)
  - [Wk03](./securing_network/wk03.md)
  - [Wk04](./securing_network/wk04.md)
  - [Wk05-Public Key Cryptography and RSA](./securing_network/wk05.md)
  - [Wk06-Cryptographic Hash Functions](./securing_network/wk06.md)
  - [Wk07-key distribution](./securing_network/wk07.md)
  - [Wk08-User Authentication](./securing_network/wk08.md)
  - [Wk09-Web security](./securing_network/wk09.md)
  - [Wk10-Electronic Mail Security](./securing_network/wk10.md)
  - [Wk11-IP Security lecture](./securing_network/wk11.md)

- **Network Mgnt**
  - [Fundamental](./network_mgnt/fun.md)
  - [OSI](./network_mgnt/osi.md)
  - Layer 2(Data Link)
    - [Ethernet & Wifi](./network_mgnt/layer2/ethernet&wifi.md)
    - [ARP](./network_mgnt/layer2/arp.md)
  - Layer 3(Network)
    - [IP](./network_mgnt/layer3/ip.md)
    - [Routing Protocols](./network_mgnt/layer3/routing.md)
    - [ICMP](./network_mgnt/layer3/icmp.md)
  - Layer4(Transport)
    - [TCP](./network_mgnt/layer4/tcp.md)
    - [UDP](./network_mgnt/layer4/udp.md)
  - App Layer
    - [DHCP](./network_mgnt/app_layer/dhcp.md)
    - [DNS](./network_mgnt/app_layer/dns.md)
    - [Telnet](./network_mgnt/app_layer/telnet.md)
    - [SSh](./network_mgnt/app_layer/ssh.md)
    - [HTTP/HTTPS](./network_mgnt/app_layer/http&https.md)
    - [FTP](./network_mgnt/app_layer/ftp.md)
    - [SFTP](./network_mgnt/app_layer/SFTP.md)
    - [TFTP](./network_mgnt/app_layer/TFTP.md)
    - [SYSLOG](./network_mgnt/app_layer/syslog.md)
    - [snmp](./network_mgnt/app_layer/snmp.md)

---

| Protocol                                | Port #                                                  |
| --------------------------------------- | ------------------------------------------------------- |
| **Dynamic Host Configuration Protocol** | 67/UDP(to server) 68/UDP (to client)                    |
| **Domain Name Server**                  | 53/UDP, 53/TCP(longer)                                  |
| Telnet                                  | 23/tcp                                                  |
| SSH                                     | 22/tcp                                                  |
| http/https                              | 80/tcp, 443/tcp                                         |
| File Transfer Protocol                  | 21/tcp(control), 20/tcp(data)                           |
| SFTP: SSH FTP                           | 22/tcp                                                  |
| SFTP: Simple File Transfer Protocol     | 115/tcp                                                 |
| **Trivial File Transfer Protocol**      | 69/udp                                                  |
| **Syslog**                              | 514/udp(default),514/TCP, 6514/TLS TCP                  |
| **Simple Network Management Protocol**  | 161/UDP (default),161/UDP(SNMP poll),162/UDP (SNMPTRAP) |

---

## TCP vs. UDP

|                          | TCP                                       | UDP                                      |
| ------------------------ | ----------------------------------------- | ---------------------------------------- |
| Connection               | connection-oriented protocol              | connectionless protocol                  |
| Acknowledgement          | Acknowledgement segments                  | No Acknowledgement                       |
| Handshake                | SYN, SYN-ACK, ACK                         | No handshake                             |
| Checksum                 | used for integrity                        | used to detect errors                    |
| Error Checking           | error checking                            | error checking, but no recovery          |
| Reliability              | absolute guarantee intact and order       | no guarantee would reach                 |
| Header size              | 20 bytes                                  | 8 bytes                                  |
| Ordering of data packets | keep inherent order                       | no inherent order                        |
| Speed                    | slower than UDP                           | faster-no errorchecking for packets      |
| Usage                    | applications that requirehigh reliability | applications that need fast transmission |
| protocols                | HTTP, HTTPs, FTP, SMTP, Telnet            | DNS, DHCP, TFTP, SNMP, RIP, VOIP         |
| Function                 | connection based                          | not connection based                     |
| Stream of data           | read as a byte stream                     | Packets are sent individually            |
| Weight                   | heavy-weight, requires three packets      | lightweight                              |
| Data Flow Control        | Flow Control, congestion control          | not                                      |
