# Linux - Networking

[Back](../../index.md)

- [Linux - Networking](#linux---networking)
  - [Get Host IP](#get-host-ip)
  - [Change Host name](#change-host-name)
  - [Change Local DNS Server](#change-local-dns-server)
  - [Ping \& `nping`](#ping--nping)
  - [`nmap`](#nmap)

---

## Get Host IP

- Get IP from interface.

```sh
ifconfig        # displays the status of the currently active interfaces.
ifconfig -a     # display all interfaces which are currently available, even if down
ifconfig -s     # display a short list

ifconfig | grep "inet" # return ip addresses of all interfaces.
```

- Get and set ip for host.

```sh
hostname        # show the system's host name
hostname -a     # Display the alias name
hostname -i     # Display  the  network  address(es) of the host name.
hostname -i     # Display  the  network  address(es) of the host name.
hostname -I     # Display all network addresses of the host.
```

---

## Change Host name

```sh
sudo vi /etc/hostname       # configures the name of the local Linux system that is set during boot
sudo vi /etc/hosts       # a plain text file used in matching a fully qualified domain name (FQDN) with the server IP hosting a specific domain.
```

---

## Change Local DNS Server

```sh
sudo nano /etc/resolv.conf      # configure DNS server
grep "nameserver" /etc/resolv.conf      # get DNS server

nslookup target_domain      # query Internet domain name servers
```

---

## Ping & `nping`

- `ping`

```sh
ping dest_url   # a network utility used to test a host's reachability on an Internet Protocol (IP) network.
ping -i 4 dest_url   # Wait interval 4 seconds between sending each packet. R
ping -c 5 dest_url   # Stop after sending 5 count ECHO_REQUEST packets.
```

- `nping`
  - allows users to generate network packets of a wide range of protocols, letting them tune virtually any field of the protocol headers.

```sh
nping --tcp-connect -p 80 --rate 10000 -c 50 dest_url
# --tcp-connect: TCP connect mode
# -p:   ports to connect to.
# -rate: the number of probes that Nping should send per second.
# -c: the number of times that Nping should loop over target hosts (and in some cases target ports).
```

---

## `nmap`

- Network exploration tool and security / port scanner

```sh
nmap –v1 –Pn –T4 --max-retries 1 192.168.50.80
# -v:     Increases the verbosity level, causing Nmap to print more information about the scan in progress.
# -Pn:    Treat all hosts as online
# -Ｔ：     timing templates， aggressive (4)
# ---max-retries 1:    number of retransmissions allowed

nmap --script http-slowloris --max-parallelism 10 192.168.50.80
# --script http-slowloris：   Loads script, Slowloris is a denial-of-service attack program
# --max-parallelism 10:        control the total number of probes
```

---

[TOP](#linux---networking)
