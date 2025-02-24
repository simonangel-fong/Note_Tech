# Hands-on: DHCP Server

[Back](../index.md)

- [Hands-on: DHCP Server](#hands-on-dhcp-server)
  - [Install and Configure the DHCP Server on ServerHost](#install-and-configure-the-dhcp-server-on-serverhost)
  - [Client Configuration](#client-configuration)

---

## Install and Configure the DHCP Server on ServerHost

interface name on ServerHost: ens160
available IP range: 192.168.128.100 - 192.168.128.200
gateway IP: 192.168.128.2

- The server's `ens160` interface is directly connected to the `192.168.128.0/24` network.
  - DHCP clients are in `192.168.128.0/24` network.
  - Subnet gateway: `192.168.128.2`
  - DNS: `192.168.128.2`, `8.8.8.8`
  - Broadcast address: `192.168.128.255`.
  - Address range for clients: `192.168.128.100` through `192.168.128.200`.
  - Maximum lease time for each client: `86,400` seconds (1 day).

```sh
# Install the DHCP Server Package
dnf install dhcp-server -y

# Edit the DHCP Configuration File
cat > /etc/dhcp/dhcpd.conf << EOF
subnet 192.168.128.0 netmask 255.255.255.0 {
    range 192.168.128.100 192.168.128.200;
    option routers 192.168.128.2;
    option domain-name-servers 192.168.128.2, 8.8.8.8, 8.8.4.4;
    option broadcast-address 192.168.128.255;
    default-lease-time 600;
    max-lease-time 86400;
}
EOF

# Set the Interface for DHCP Server
cp /usr/lib/systemd/system/dhcpd.service /etc/systemd/system/
# change with interface name ens160:
vi /etc/systemd/system/dhcpd.service
ExecStart=/usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid $DHCPDARGS ens160

# Start and Enable the DHCP Service
systemctl --system daemon-reload
systemctl enable --now dhcpd
systemctl status dhcpd

# Allow DHCP Traffic in the Firewall
firewall-cmd --permanent --add-service=dhcp
firewall-cmd --reload
firewall-cmd --list-services
# cockpit dhcp dhcpv6-client http ssh
```

---

## Client Configuration

```sh
nmcli c down ens160
nmcli c modify ens160 ipv4.method auto
nmcli c up ens160

ip a
# inet 192.168.128.100/24 brd 192.168.128.255 scope global dynamic noprefixroute ens160

nmcli device show ens160 | grep IP4
# IP4.ADDRESS[1]:                         192.168.128.100/24
# IP4.GATEWAY:                            192.168.128.2
# IP4.ROUTE[1]:                           dst = 192.168.128.0/24, nh = 0.0.0.0, mt = 100
# IP4.ROUTE[2]:                           dst = 0.0.0.0/0, nh = 192.168.128.2, mt = 100
# IP4.DNS[1]:                             192.168.128.2
# IP4.DOMAIN[1]:                          localdomain
```

- Verify DHCP Lease on Both Machines

```sh
# Check the DHCP lease assignments:
cat /var/lib/dhcpd/dhcpd.leases

# lease 192.168.128.100 {
#   starts 0 2025/02/23 20:41:21;
#   ends 0 2025/02/23 20:51:21;
#   cltt 0 2025/02/23 20:41:21;
#   binding state active;
#   next binding state free;
#   rewind binding state free;
#   hardware ethernet 00:0c:29:d5:35:27;
#   uid "\001\000\014)\3255'";
# }
```