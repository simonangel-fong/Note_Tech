# Linux - Networking: Package `nmap`

[Back](../../index.md)

- [Linux - Networking: Package `nmap`](#linux---networking-package-nmap)
  - [`nmap` Package](#nmap-package)
  - [`nping` Utility](#nping-utility)
  - [`nmap` Utility](#nmap-utility)

---

## `nmap` Package

- Package

```sh
sudo yum install nmap
rpm -aq | grep nmap
```

---

## `nping` Utility

- `nping`
  - an advanced network packet generation and testing tool
  - allows users to generate network packets of a wide range of protocols, letting them tune virtually any field of the protocol headers.
  - Require root privilege.

| CMD                                  | DESC                               |
| ------------------------------------ | ---------------------------------- |
| `nping --icmp example.com`           | Test ICMP requests (default)       |
| `nping --tcp -p 80 example.com`      | Test http requests                 |
| `nping --tcp -p 443 google.com`      | Test https requests                |
| `nping --udp -p 53 example.com`      | Test DNS requests                  |
| `nping --arp 192.168.204.1`          | Send ARP requests (local network)  |
| `nping --icmp --count 5 example.com` | Number of packets to send          |
| `nping --ttl 64 example.com`         | Set Time-To-Live value for packets |
| `nping --rate 1000 example.com`      | Send num packets per second        |

- Example

```sh
nping --tcp-connect -p 80 --rate 10000 -c 50 dest_url
# --tcp-connect: TCP connect mode
# -p:   ports to connect to.
# -rate: the number of probes that Nping should send per second.
# -c: the number of times that Nping should loop over target hosts (and in some cases target ports).
```

---

## `nmap` Utility

- `nmap` command
  - a free and open-source network detection and security **scanning** utility.

| CMD                                 | DESC                                        |
| ----------------------------------- | ------------------------------------------- |
| `nmap 192.168.204.153 192.168.1.2`  | Scan Multiple Hosts                         |
| `nmap 192.168.204.1-100`            | Scan a Range of IPs                         |
| `nmap 192.168.1.0/24`               | Scan an entire subnet                       |
| `nmap -p 22,80,443 192.168.204.153` | Scan Specific Ports                         |
| `nmap -sV 192.168.204.153`          | Service Version Detection                   |
| `nmap -O 192.168.204.153`           | Operating System Detection                  |
| `nmap -A 192.168.204.153`           | Aggressive Scan                             |
| `nmap -sS 192.168.204.153`          | Scan Using TCP SYN (Stealth Scan)           |
| `nmap -sT 192.168.204.153`          | Scan Using TCP Connect (Full Scan)          |
| `nmap -sU 192.168.204.153`          | Stealth Scan (UDP Scan)                     |
| `nmap -T4 192.168.204.153`          | Scan with Timing Options                    |
| `nmap --traceroute 192.168.204.153` | Perform a traceroute                        |
| `nmap -sA 192.168.204.153`          | Detect firewall settings and packet filters |
| `nmap -R example.com`               | Attempt DNS resolution during the scan      |

---

[TOP](#linux---networking-package-nmap)
