# CKS - Secure `etcd`

[Back](../../index.md)

- [CKS - Secure `etcd`](#cks---secure-etcd)
  - [Secure `etcd`](#secure-etcd)
    - [Secure data storage at rest](#secure-data-storage-at-rest)
    - [Secure communication](#secure-communication)
    - [Authentication](#authentication)
  - [Lab: etcd in plain text](#lab-etcd-in-plain-text)
  - [Lab: Secure etcd with certificate](#lab-secure-etcd-with-certificate)
    - [Create etcd certificate](#create-etcd-certificate)
    - [Configure etcd using https](#configure-etcd-using-https)
    - [Access etcd with https](#access-etcd-with-https)
  - [Authentication](#authentication-1)

---

## Secure `etcd`

3 areas

- secure data at rest
- sercure communication
- authentication
- tls encryption
- certificate based authentication

---

### Secure data storage at rest

- By defautl, etcd stores data **in plain text.**
  - sensitive data, e.g., secrets, can be read directly from the disk.

---

### Secure communication

- by default, etcd communication are in plain text
  - can be detecept with tcpdump
- Secure communication by certificate

---

### Authentication

- by default, authentication is not required.
  - everyone can request etcd database
- secure by certificate based authentication

---

## Lab: etcd in plain text

- install etcd

```sh
cd /tmp
export ETCD_VERSION=v3.6.14
curl -fLO "https://github.com/etcd-io/etcd/releases/download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz"

tar -xzf "etcd-${ETCD_VERSION}-linux-amd64.tar.gz"
cd "/tmp/etcd-${ETCD_VERSION}-linux-amd64"

ls -l
# total 60664
# drwxr-xr-x 6 ubuntuadmin ubuntuadmin     4096 Jul 23 15:21 Documentation
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin    44075 Jul 23 15:21 README-etcdctl.md
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin     8275 Jul 23 15:21 README-etcdutl.md
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin     9839 Jul 23 15:21 README.md
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin     7896 Jul 23 15:21 READMEv2-etcdctl.md
# -rwxr-xr-x 1 ubuntuadmin ubuntuadmin 26734776 Jul 23 15:21 etcd
# -rwxr-xr-x 1 ubuntuadmin ubuntuadmin 17567928 Jul 23 15:21 etcdctl
# -rwxr-xr-x 1 ubuntuadmin ubuntuadmin 17723576 Jul 23 15:21 etcdutl

# raw start
./etcd

# confirm ports
sudo ss -ntlp | grep -E "2379|2380"
# LISTEN 0      4096        127.0.0.1:2380      0.0.0.0:*    users:(("etcd",pid=2602,fd=4))
# LISTEN 0      4096        127.0.0.1:2379      0.0.0.0:*    users:(("etcd",pid=2602,fd=7))

# confirm connection without tls
./etcdctl --endpoints=http://127.0.0.1:2379 endpoint health
# http://127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.530133ms
```

- insert a kv pair
  - without auth
  - communicate in plain text, http, not https
  - store data in plain text

```sh
# insert a kv pair
cd "/tmp/etcd-${ETCD_VERSION}-linux-amd64"

./etcdctl --endpoints=http://127.0.0.1:2379 put message "test,test,test"
# OK

# query data
./etcdctl --endpoints=http://127.0.0.1:2379 get message
# message
# test,test,test

# confirm plain text
grep -R "test,test,test" .
# grep: ./default.etcd/member/snap/db: binary file matches
# grep: ./default.etcd/member/wal/0000000000000000-0000000000000000.wal: binary file matches

```

- capture plain text traffic with tcpdump, skip

---

## Lab: Secure etcd with certificate

### Create etcd certificate

```sh
mkdir -pv ~/cert/etcd/
# mkdir: created directory '/home/ubuntuadmin/cert/etcd/'
cd ~/cert/etcd

# ##############################
# create etcd key and csr
# ##############################
# create private key
openssl genrsa -out etcd.key 2048

# create csr config file
cat > etcd.cnf <<EOF
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
IP.1 = 192.168.10.180
IP.2 = 127.0.0.1
EOF


ls etcd.cnf
# etcd.cnf

# create csr
openssl req -new -key etcd.key -subj "/CN=etcd" -out etcd.csr -config etcd.cnf

# ##############################
# sign csr
# ##############################
openssl x509 -req -in etcd.csr -CA ~/cert/ca/ca.crt -CAkey ~/cert/ca/ca.key -CAcreateserial -out etcd.crt -extensions v3_req -extfile etcd.cnf -days 2000
# Certificate request self-signature ok
# subject=CN = etcd

# confirm
ll ~/cert/etcd
# rwxr-xr-x 2 ubuntuadmin ubuntuadmin 4096 Sep  4 21:59 ./
# drwxr-xr-x 5 ubuntuadmin ubuntuadmin 4096 Sep  4 21:51 ../
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin  278 Sep  4 21:58 etcd.cnf
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 1196 Sep  4 22:01 etcd.crt
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin  972 Sep  4 22:00 etcd.csr
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Sep  4 21:52 etcd.key

openssl x509 -in etcd.crt -text -noout | grep -E "Issuer:|Subject:"
        # Issuer: CN = KUBERNETES-CA
        # Subject: CN = etcd

openssl verify -CAfile ~/cert/ca/ca.crt etcd.crt
# etcd.crt: OK
```

---

### Configure etcd using https

- important flags
  - `--cert-file`: path to TLS certificate file
  - `--key-file`: path to private key with TLS certificate file
  - `--advertise-client-urls`: the URLs for client communicateion, e.g. https://ip:2379
  - `--listen=client-urls`:the URLs etcd listens for client requests, e.g., https://0.0.0.0:2379

```sh
export ETCD_VERSION=v3.6.14
cd "/tmp/etcd-${ETCD_VERSION}-linux-amd64"

# apply cert and key, specify https endpoint
./etcd --cert-file=/home/ubuntuadmin/cert/etcd/etcd.crt   \
  --key-file=/home/ubuntuadmin/cert/etcd/etcd.key  \
  --advertise-client-urls=https://127.0.0.1:2379  \
  --listen-client-urls=https://127.0.0.1:2379

# confirm
# without crt
./etcdctl put course "cks"
# {"level":"warn","ts":"2026-09-04T22:10:46.029225-0400","logger":"etcd-client","caller":"v3@v3.6.14/retry_interceptor.go:68","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc0002f0b40/127.0.0.1:2379","peer":"Peer{Addr: <nil>, LocalAddr: <nil>, AuthInfo: <nil>}","method":"/etcdserverpb.KV/Put","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = latest balancer error: connection error: desc = \"error reading server preface: EOF\""}
# Error: context deadline exceeded

# disable secure
./etcdctl --endpoints=https://127.0.0.1:2379 --insecure-skip-tls-verify --insecure-transport=false put course "cks"
# OK

./etcdctl --endpoints=https://127.0.0.1:2379 --insecure-skip-tls-verify --insecure-transport=false get course
# course
# cks


```

### Access etcd with https

---

## Authentication

authentication workflow

request with credential
authenticate
fetch data

types of authentication

- username/pwd
- certificate
