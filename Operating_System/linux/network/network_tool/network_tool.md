# Linux - Network: Common Tools

[Back](../../index.md)

- [Linux - Network: Common Tools](#linux---network-common-tools)
  - [Connection Test](#connection-test)
  - [Ping \& `nping`](#ping--nping)
  - [`nmap`](#nmap)

---

## Connection Test

| CMD                            | DESC                                               |
| ------------------------------ | -------------------------------------------------- |
| `ping -c5 target_url`          | Send a specific number of packets                  |
| `ping -i0.5 target_url`        | Set interval between sending packets (default: 1a) |
| `ping -t64 target_url`         | Set the Time-To-Live (TTL) value for packets       |
| `ping -s64 target_url`         | Specify packet size in bytes                       |
| `ping -4 target_url`           | Force using IPv4                                   |
| `ping -6 target_url`           | Force using IPv6                                   |


## Ping & `nping`

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

| CMD                    | DESC                      |
| ---------------------- | ------------------------- |
| `tcpdump`              | dump traffic on a network |
| `tcpdump -i interface` | listen on the interface   |

---

- Command

| CMD          | Desc |
| ------------ | ---- |
| `ping`       |      |
| `ip`         |      |
| `traceroute` |      |
| `tcpdump`    |      |
| `nslookup`   |      |
| `dig`        |      |
| `ethtool`    |      |
