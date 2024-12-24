# Linux - Networking: Firewall

[Back](../../index.md)

- [Linux - Networking: Firewall](#linux---networking-firewall)
  - [Firewall](#firewall)
    - [Types of Firewalls](#types-of-firewalls)
    - [Common Components](#common-components)
  - [Package `firewalld`](#package-firewalld)
    - [Firewalld Zones](#firewalld-zones)
    - [Package and Service](#package-and-service)
    - [Common Commands](#common-commands)
  - [Best Practices](#best-practices)
  - [Lab: Add a new service](#lab-add-a-new-service)
  - [Lab: Add a reject rule](#lab-add-a-reject-rule)
  - [Lab: Block ICMP ping](#lab-block-icmp-ping)
  - [Lab: Block engress traffic to Facebook](#lab-block-engress-traffic-to-facebook)

---

## Firewall

- `firewall`
  - a network security system that **monitors** and **controls** incoming and outgoing **network traffic** based on predefined security rules.
  - It acts as a **barrier** between a **trusted internal network** and **untrusted external networks**, such as the internet.

---

### Types of Firewalls

- **Packet-Filtering Firewalls:**

  - Operates at the `network layer (Layer 3)`.
  - Filters traffic based on **source/destination IP addresses**, **ports**, and **protocols**.
    - Example: IP tables in Linux.

- **Stateful Firewalls:**

  - **Tracks the state** of active connections.
  - Only **allows** packets that match a **known connection state**.

- **Application Layer Firewalls:**

  - Filters traffic based on **application-level protocols** like HTTP, FTP, and DNS.

- **Next-Generation Firewalls (NGFW):**
  - Combines stateful inspection with `deep packet inspection (DPI)`.
  - Can detect and block advanced threats.

---

### Common Components

- **Rules** and **Policies**:

  - Define what traffic is **allowed** or **blocked** based on conditions.
  - Conditions include IP addresses, ports, protocols, and more.

- **Zones:**
  - **Logical groupings** of network **interfaces**, e.g., internal, external, dmz.
- **Logging and Monitoring:**

  - **Records** information about allowed/blocked traffic for analysis.

- Terms:
  - `Ingress Traffic`: **Incoming** traffic to a system or network.
  - `Egress Traffic`: **Outgoing** traffic from a system or network.
  - `Port`: A logical **endpoint** for communication (e.g., 80 for HTTP, 22 for SSH).
  - `Protocol`: A set of **rules** for data communication (e.g., TCP, UDP, ICMP).

---

## Package `firewalld`

- `firewalld`
  - the default firewall management tool
  - replacing traditional `iptables`.
  - It uses zones and rules for managing network traffic.

### Firewalld Zones

| Zone       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `drop`     | Drops all incoming traffic without response.            |
| `block`    | Blocks incoming traffic but sends a reject response.    |
| `public`   | For use in public networks, allowing limited services.  |
| `home`     | For trusted home networks, allows more services.        |
| `work`     | Similar to home but for work environments.              |
| `internal` | Trusted internal networks, allowing even more services. |
| `trusted`  | All traffic is accepted                                 |

---

### Package and Service

- Pacakge

```sh
dnf install firewalld -y
rpm -qa | grep firewalld
# firewalld-filesystem-0.9.11-9.el8_10.noarch
# firewalld-0.9.11-9.el8_10.noarch
```

- Service

```sh
sudo systemctl enable firewalld
sudo systemctl start firewalld
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

---

### Common Commands

- Required `sudo` privilege

- Admin

| CMD                     | DESC                                 |
| ----------------------- | ------------------------------------ |
| `firewall-cmd --state`  | Check Firewall Status                |
| `firewall-cmd --reload` | Reloads the permanent firewall rules |

- Zone

| CMD                               | DESC                 |
| --------------------------------- | -------------------- |
| `firewall-cmd --get-zones`        | List supported zones |
| `firewall-cmd --get-active-zones` | View Active Zones    |

- Rule

| CMD                                                                                          | DESC                              |
| -------------------------------------------------------------------------------------------- | --------------------------------- |
| `firewall-cmd --list-all`                                                                    | List all rules in the active zone |
| `firewall-cmd --zone=public --list-all`                                                      | List all rules in a specific zone |
| `firewall-cmd --add-icmp-block-inversion`                                                    | Block ICMP ping                   |
| `firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.140" reject'`    | Add a reject rule                 |
| `firewall-cmd --remove-rich-rule='rule family="ipv4" source address="192.168.1.140" reject'` | Remove an ingress reject rule     |
| `firewall-cmd --remove-rich-rule='rule family="ipv4" source address="192.168.1.140" reject'` | Remove an ingress reject rule     |
| `firewall-cmd --direct --add-rule ipv4 filter OUTPUT 0 -d 192.168.1.140 -j DROP`             | Block an Egress traffic           |

- Services
  - cf: `/usr/lib/firewalld/services/*.xml`
  - Adding a 3rd party service
    - add an xml file in the cf path.
    - add the service with `--add-service`

| CMD                                                           | DESC                         |
| ------------------------------------------------------------- | ---------------------------- |
| `firewall-cmd --get-services`                                 | List supported services      |
| `firewall-cmd --zone=public --add-service=ssh`                | Allow a Service temporarily  |
| `firewall-cmd --permanent --zone=public --add-service=ssh`    | Allow a Service permanently  |
| `firewall-cmd --permanent --zone=public --remove-service=ssh` | Remove a Service permanently |

- Port

| CMD                                                           | DESC          |
| ------------------------------------------------------------- | ------------- |
| `firewall-cmd --permanent --zone=public --add-port=80/tcp`    | Open a Port   |
| `firewall-cmd --permanent --zone=public --remove-port=80/tcp` | Remove a Port |

---

## Best Practices

- **Default Deny Policy**:

  - **Block all incoming** traffic by default
  - **explicitly allow required** traffic.

- **Limit Open Ports**:
  - Only open necessary ports to **reduce attack surface**.
- Enable **Logging**:
  - Monitor and analyze firewall logs for suspicious activities.
- Use **Zones** Appropriately:
  - Assign network **interfaces** to zones based on trust levels.
- **Regularly Review** Rules:
  - **Periodically** audit and update firewall rules as needed.

---

## Lab: Add a new service

- Add new xml

```sh
# Confirm new sap service is not included
firewall-cmd --get-services | grep sap

# add new xml
vi /usr/lib/firewalld/services/sap.xml
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<service>
  <short>SAP</short>
  <description>A test of a 3rd party application services</description>
  <port protocol="tcp" port="22"/>
</service>
```

- Confirm

```sh
# reload cf
firewall-cmd --reload
# success

# confirm
firewall-cmd --get-services | grep sap
# RH-Satellite-6 RH-Satellite-6-capsule amanda-client amanda-k5-client amqp amqps apcupsd audit bacula bacula-client bb bgp bitcoin bitcoin-rpc bitcoin-testnet bitcoin-testnet-rpc bittorrent-lsd ceph ceph-mon cfengine cockpit collectd condor-collector ctdb dhcp dhcpv6 dhcpv6-client distcc dns dns-over-tls docker-registry docker-swarm dropbox-lansync elasticsearch etcd-client etcd-server finger foreman foreman-proxy freeipa-4 freeipa-ldap freeipa-ldaps freeipa-replication freeipa-trust ftp galera ganglia-client ganglia-master git grafana gre high-availability http https imap imaps ipp ipp-client ipsec irc ircs iscsi-target isns jenkins kadmin kdeconnect kerberos kibana klogin kpasswd kprop kshell kube-apiserver ldap ldaps libvirt libvirt-tls lightning-network llmnr managesieve matrix mdns memcache minidlna mongodb mosh mountd mqtt mqtt-tls ms-wbt mssql murmur mysql nbd nfs nfs3 nmea-0183 nrpe ntp nut openvpn ovirt-imageio ovirt-storageconsole ovirt-vmconsole plex pmcd pmproxy pmwebapi pmwebapis pop3 pop3s postgresql privoxy prometheus proxy-dhcp ptp pulseaudio puppetmaster quassel radius rdp redis redis-sentinel rpc-bind rquotad rsh rsyncd rtsp salt-master samba samba-client samba-dc sane sap sip sips slp smtp smtp-submission smtps snmp snmptrap spideroak-lansync spotify-sync squid ssdp ssh steam-streaming svdrp svn syncthing syncthing-gui synergy syslog syslog-tls telnet tentacle tftp tftp-client tile38 tinc tor-socks transmission-client upnp-client vdsm vnc-server wbem-http wbem-https wsman wsmans xdmcp xmpp-bosh xmpp-client xmpp-local xmpp-server zabbix-agent zabbix-server
```

- Add new service

```sh
# add
firewall-cmd --add-service=sap
# Warning: ALREADY_ENABLED: 'sap' already in 'public'
# success

# confirm
firewall-cmd --list-all
# public (active)
#   target: default
#   icmp-block-inversion: no
#   interfaces: ens160 ens224
#   sources:
#   services: cockpit dhcpv6-client samba sap ssh
#   ports: 80/tcp 443/tcp
#   protocols:
#   forward: no
#   masquerade: no
#   forward-ports:
#   source-ports:
#   icmp-blocks:
#   rich rules:
```

- Remove a service

```sh
firewall-cmd --remove-service=sap
# success

# confirm
firewall-cmd --list-all
# public (active)
# ...
#   services: cockpit dhcpv6-client samba sap ssh
```

---

## Lab: Add a reject rule

- Before

```sh
# ping from a client to the server
ping -c3 192.168.1.130
# PING 192.168.1.130 (192.168.1.130) 56(84) bytes of data.
# 64 bytes from 192.168.1.130: icmp_seq=1 ttl=64 time=1.14 ms
# 64 bytes from 192.168.1.130: icmp_seq=2 ttl=64 time=0.552 ms
# 64 bytes from 192.168.1.130: icmp_seq=3 ttl=64 time=0.588 ms

# --- 192.168.1.130 ping statistics ---
# 3 packets transmitted, 3 received, 0% packet loss, time 2055ms
# rtt min/avg/max/mdev = 0.552/0.760/1.141/0.270 ms
```

- Add a rule in server firewall

```sh
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.140" reject'
# success
firewall-cmd --list-all
#   rich rules:
#         rule family="ipv4" source address="192.168.1.140" reject
```

- Confirm

```sh
# ping from a client
ping -c3 192.168.1.130
# PING 192.168.1.130 (192.168.1.130) 56(84) bytes of data.
# From 192.168.1.130 icmp_seq=1 Destination Port Unreachable
# From 192.168.1.130 icmp_seq=2 Destination Port Unreachable
# From 192.168.1.130 icmp_seq=3 Destination Port Unreachable

# --- 192.168.1.130 ping statistics ---
# 3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2059ms
```

- Remove a rule

```sh
# remove on server
firewall-cmd --remove-rich-rule='rule family="ipv4" source address="192.168.1.140" reject'
# success

firewall-cmd --list-all
#   rich rules:
```

- Confirm from a client

```sh
ping -c3 192.168.1.130
# PING 192.168.1.130 (192.168.1.130) 56(84) bytes of data.
# 64 bytes from 192.168.1.130: icmp_seq=1 ttl=64 time=0.868 ms
# 64 bytes from 192.168.1.130: icmp_seq=2 ttl=64 time=1.29 ms
# 64 bytes from 192.168.1.130: icmp_seq=3 ttl=64 time=0.892 ms

# --- 192.168.1.130 ping statistics ---
# 3 packets transmitted, 3 received, 0% packet loss, time 2004ms
# rtt min/avg/max/mdev = 0.868/1.016/1.289/0.194 ms
```

---

## Lab: Block ICMP ping

- On server side

```sh
# block icmp on server side
firewall-cmd --add-icmp-block-inversion
# success
firewall-cmd --list-all
#   icmp-block-inversion: yes
```

- on Client side

```sh
ping -c3 192.168.1.130
# PING 192.168.1.130 (192.168.1.130) 56(84) bytes of data.
# From 192.168.1.130 icmp_seq=1 Packet filtered
# From 192.168.1.130 icmp_seq=2 Packet filtered
# From 192.168.1.130 icmp_seq=3 Packet filtered

# --- 192.168.1.130 ping statistics ---
# 3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2003ms
```

- Turn on ICMP

```sh
# on server side
firewall-cmd --remove-icmp-block-inversion
# success
firewall-cmd --list-all
#   icmp-block-inversion: no
```

- Confirm from client

```sh
ping -c3 192.168.1.130
# PING 192.168.1.130 (192.168.1.130) 56(84) bytes of data.
# 64 bytes from 192.168.1.130: icmp_seq=1 ttl=64 time=2.34 ms
# 64 bytes from 192.168.1.130: icmp_seq=2 ttl=64 time=0.724 ms
# 64 bytes from 192.168.1.130: icmp_seq=3 ttl=64 time=1.58 ms

# --- 192.168.1.130 ping statistics ---
# 3 packets transmitted, 3 received, 0% packet loss, time 2003ms
# rtt min/avg/max/mdev = 0.724/1.547/2.338/0.659 ms
```

---

## Lab: Block engress traffic to Facebook

```sh
# Find facebook ip
nslookup facebook.com
# Server:         8.8.8.8
# Address:        8.8.8.8#53

# Non-authoritative answer:
# Name:   facebook.com
# Address: 31.13.80.36
# Name:   facebook.com
# Address: 2a03:2880:f10e:83:face:b00c:0:25de

# ping before blocking
ping -c3 facebook.com
# PING facebook.com (31.13.80.36) 56(84) bytes of data.
# 64 bytes from edge-star-mini-shv-01-yyz1.facebook.com (31.13.80.36): icmp_seq=1 ttl=128 time=25.5 ms
# 64 bytes from edge-star-mini-shv-01-yyz1.facebook.com (31.13.80.36): icmp_seq=2 ttl=128 time=26.8 ms
# 64 bytes from edge-star-mini-shv-01-yyz1.facebook.com (31.13.80.36): icmp_seq=3 ttl=128 time=28.3 ms

# --- facebook.com ping statistics ---
# 3 packets transmitted, 3 received, 0% packet loss, time 2003ms
# rtt min/avg/max/mdev = 25.546/26.899/28.324/1.135 ms

# add block rule
firewall-cmd --direct --add-rule ipv4 filter OUTPUT 0 -d 31.13.80.36 -j DROP
# success

# confirm
ping -c3 facebook.com
# PING facebook.com (31.13.80.36) 56(84) bytes of data.
# ping: sendmsg: Operation not permitted
# ping: sendmsg: Operation not permitted
# ping: sendmsg: Operation not permitted

# --- facebook.com ping statistics ---
# 3 packets transmitted, 0 received, 100% packet loss, time 2059ms
```

---

[TOP](#linux---networking-firewall)
