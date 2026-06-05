# Golang - Install

[Back](../index.md)

---

## Installation

- ref: https://go.dev/doc/install

- Ubuntu

```sh
wget https://go.dev/dl/go1.26.4.linux-amd64.tar.gz
# --2026-06-04 19:57:48--  https://go.dev/dl/go1.26.4.linux-amd64.tar.gz
# Resolving go.dev (go.dev)... 216.239.34.21, 216.239.38.21, 216.239.36.21, ...
# Connecting to go.dev (go.dev)|216.239.34.21|:443... connected.
# HTTP request sent, awaiting response... 302 Found
# Location: https://dl.google.com/go/go1.26.4.linux-amd64.tar.gz [following]
# --2026-06-04 19:57:49--  https://dl.google.com/go/go1.26.4.linux-amd64.tar.gz
# Resolving dl.google.com (dl.google.com)... 142.250.139.91, 142.250.139.93, 142.250.139.136, ...
# Connecting to dl.google.com (dl.google.com)|142.250.139.91|:443... connected.
# HTTP request sent, awaiting response... 200 OK
# Length: 66861266 (64M) [application/x-gzip]
# Saving to: ‘go1.26.4.linux-amd64.tar.gz’

# go1.26.4.linux-amd64.tar 100%[================================>]  63.76M  25.9MB/s    in 2.5s

# 2026-06-04 19:57:52 (25.9 MB/s) - ‘go1.26.4.linux-amd64.tar.gz’ saved [66861266/66861266]

sudo mkdir /usr/local/go
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.26.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

go version
# go version go1.26.4 linux/amd64
```

---
