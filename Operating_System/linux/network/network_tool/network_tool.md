# Linux - Network: Common Tools

[Back](../../index.md)

- [Linux - Network: Common Tools](#linux---network-common-tools)
  - [Test Connection](#test-connection)
  - [Query Route Path](#query-route-path)
  - [Query DNS](#query-dns)
  - [Analyze Network Traffic](#analyze-network-traffic)

---

## Test Connection

| CMD                     | DESC                                               |
| ----------------------- | -------------------------------------------------- |
| `ping -c5 target_url`   | Send a specific number of packets                  |
| `ping -i0.5 target_url` | Set interval between sending packets (default: 1a) |
| `ping -t64 target_url`  | Set the Time-To-Live (TTL) value for packets       |
| `ping -s64 target_url`  | Specify packet size in bytes                       |
| `ping -4 target_url`    | Force using IPv4                                   |
| `ping -6 target_url`    | Force using IPv6                                   |

---

## Query Route Path

- `traceroute`
  - sends packets with progressively increasing TTL (Time To Live) values.
  - It provides **information about each hop** (router or intermediary device) along the route and measures the time it takes for packets to travel to each hop.

| CMD                               | DESC                                                            |
| --------------------------------- | --------------------------------------------------------------- |
| `traceroute google.com`           | Route packets trace to target host                              |
| `traceroute -m 15 google.com`     | Set the maximum number of hops (default is 30)                  |
| `traceroute -I google.com`        | Use ICMP ECHO for probes                                        |
| `traceroute -T google.com`        | Use TCP SYN packets (Trace to web servers or through firewalls) |
| `traceroute -i ens160 google.com` | Specifies the interface                                         |
| `traceroute -n google.com`        | Skipping hostname resolution for faster output.                 |
| `traceroute -d google.com`        | Display IP of routers.                                          |

---

## Query DNS

- `nslookup`:

  - a network utility used to query `DNS (Domain Name System)` servers to obtain information about a domain name or IP address.
  - It helps **troubleshoot DNS-related issues** by retrieving details such as the IP address associated with a domain name or the domain name associated with an IP address.

- `dig (Domain Information Groper)`:
  - a powerful **DNS lookup utility** that allows users to query Domain Name System (DNS) servers for information about domain names, IP addresses, and other DNS records.
  - It is commonly **used for troubleshooting** and verifying DNS configurations.

| CMD                            | DESC                                        |
| ------------------------------ | ------------------------------------------- |
| `nslookup google.com`          | Find the IP Address of a Domain             |
| `nslookup 8.8.8.8`             | Find the Domain Name of an IP Address       |
| `nslookup youtube.com 8.8.8.8` | Specify the DNS server to use for the query |
| `dig www.youtube.com`          | Resolve a Domain Name to an IP Address      |
| `dig 142.251.32.78`            | Resolve an IP Address                       |
| `dig www.youtube.com +short`   | Provide a terse answer                      |
| `dig @8.8.8.8 www.youtube.com` | Reverse via a specific DNS server           |
| `dig www.youtube.com -t A`     | Reverse for IPv4 IP address                 |
| `dig www.youtube.com -t AAAA`  | Reverse for IPv6 IP address                 |
| `dig www.youtube.com -t CNAME` | Reverse for Canonical name record           |
| `dig www.youtube.com -t MX`    | Reverse for Email server host names         |
| `dig www.youtube.com -t NS`    | Reverse for Name (DNS) server names         |
| `dig www.youtube.com -t TXT`   | Reverse for Text record                     |

---

## Analyze Network Traffic

- `tcpdump`
  - a powerful command-line network packet analyzer used to capture, filter, and **analyze network traffic**.
  - It is widely used for network troubleshooting, monitoring, and security analysis.

| CMD                          | DESC                                       |
| ---------------------------- | ------------------------------------------ |
| `tcpdump`                    | Capture All Traffic                        |
| `tcpdump -i if_name`         | Capture Traffic on a Specific Interface    |
| `tcpdump -c NUM`             | Exit after receiving count packets.        |
| `tcpdump tcp`                | Capture packets for TCP                    |
| `tcpdump udp`                | Capture packets for UDP                    |
| `tcpdump icmp`               | Capture packets for ICMP                   |
| `tcpdump port 80`            | Capture Traffic on a Specific Port         |
| `tcpdump host 192.168.1.170` | Capture Traffic to or from a Specific Host |

---

[TOP](#linux---network-common-tools)
