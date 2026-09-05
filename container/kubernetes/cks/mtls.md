## mTLS

- `Mutual TLS (mTLS)`
  - a security protocol where both the **client** and the **server** **verify each other**'s identities using digital certificates before data flows.

- `standard TLS`: only the client checks if the server is real
  - risk: `Man-in-the-Middle (MitM)` impersonation attack

- requirements
  - both has its own certificate
  - both certs are signed by CA trusted by both sender and receiver.

---

### Handshake process

1. The **client** connects to the server.
2. The **server** presents its **certificate** to the client.
3. The **client** verifies the server's certificate.
4. The **client** presents its **certificate** to the server.
5. The **server** verifies the client's certificate.
6. If both verifications pass, a secure, **encrypted connection** is established.

---

### COnfiration Workflow Steps

1. Certificate Authority.
2. Etcd certificate signed through the Certificate Authority.
3. Client certificate signed through the Certificate Authority.
4. Both etcd and client will trust the Certificate Authority

---

## Lab: mTLS with etcd and etcdctl

This lab runs a single etcd node on Linux AMD64 and uses mTLS to secure connections from `etcdctl`. You need `curl`, `tar`, and OpenSSL installed, with ports `2379` and `2380` available.

Run the download and certificate steps in the same terminal. Use a second terminal for client commands after starting etcd.

### Download etcd

```sh
cd /tmp
export ETCD_VERSION=v3.6.14
curl -fLO "https://github.com/etcd-io/etcd/releases/download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz"

tar -xzf "etcd-${ETCD_VERSION}-linux-amd64.tar.gz"
cd "/tmp/etcd-${ETCD_VERSION}-linux-amd64"

# Confirm that both binaries are available.
./etcd --version
# etcd Version: 3.6.14
# Git SHA: fc04cf7
# Go Version: go1.25.12
# Go OS/Arch: linux/amd64

./etcdctl version
# etcdctl version: 3.6.14
# API version: 3.6
```

### Create CA

```sh
cd "/tmp/etcd-${ETCD_VERSION}-linux-amd64"

# Store the lab certificates in the current directory.
mkdir -p certs

# Create the CA's private key.
openssl genrsa -out certs/ca.key 2048

# Create a self-signed CA certificate that can sign other certificates.
openssl req -new -x509 -sha256 -days 365 \
  -key certs/ca.key \
  -subj "/CN=etcd-lab-ca" \
  -out certs/ca.crt

# Inspect the CA certificate.
openssl x509 -in certs/ca.crt -text -noout | grep -E "Issuer:|Subject:"
        # Issuer: CN = etcd-lab-ca
        # Subject: CN = etcd-lab-ca

```

### Create etcd certificate

The server certificate includes subject alternative names (SANs) for `localhost` and `127.0.0.1`. The hostname or IP address used by the client must match a SAN in this certificate.

The etcd certificate needs both `serverAuth` and `clientAuth` because etcd also uses it for internal client connections to its own endpoint. Using only `serverAuth` can cause `x509: certificate specifies an incompatible key usage`. See the [etcd project discussion](https://github.com/etcd-io/etcd/discussions/17279).

```sh
# Create the server's private key.
openssl genrsa -out certs/etcd.key 2048

# Create the server's certificate signing request (CSR).
openssl req -new -key certs/etcd.key -subj "/CN=etcd-server" -out certs/etcd.csr

# Define the certificate's purpose and permitted server addresses.
cat > certs/etcd.ext <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectAltName=DNS:localhost,IP:127.0.0.1
EOF

# Sign the server certificate with the CA.
openssl x509 -req -sha256 -days 365 \
  -in certs/etcd.csr \
  -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
  -extfile certs/etcd.ext -out certs/etcd.crt

# Certificate request self-signature ok
# subject=CN = etcd-server

# Verify the certificate's trust, purpose, and IP address.
openssl verify -CAfile certs/ca.crt -purpose sslserver -verify_ip 127.0.0.1 certs/etcd.crt
openssl verify -CAfile certs/ca.crt -purpose sslclient certs/etcd.crt
# certs/etcd.crt: OK

openssl x509 -in certs/etcd.crt -text -noout | grep -E "Issuer:|Subject:"
        # Issuer: CN = etcd-lab-ca
        # Subject: CN = etcd-server
```

---

### Create etcdctl certificate

```sh
# Create the client's private key.
openssl genrsa -out certs/etcdctl.key 2048

# Create the client's CSR.
openssl req -new -key certs/etcdctl.key -subj "/CN=etcdctl-client" -out certs/etcdctl.csr

# Define the certificate's client authentication purpose.
cat > certs/etcdctl.ext <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature
extendedKeyUsage=clientAuth
EOF

# Sign the client certificate using the same CA.
openssl x509 -req -sha256 -days 365 \
  -in certs/etcdctl.csr \
  -CA certs/ca.crt -CAkey certs/ca.key -CAserial certs/ca.srl \
  -extfile certs/etcdctl.ext -out certs/etcdctl.crt

# Certificate request self-signature ok
# subject=CN = etcdctl-client

# Verify the certificate's trust and client authentication purpose.
openssl verify -CAfile certs/ca.crt -purpose sslclient certs/etcdctl.crt
# certs/etcdctl.crt: OK

openssl x509 -in certs/etcdctl.crt -text -noout | grep -E "Issuer:|Subject:"
        # Issuer: CN = etcd-lab-ca
        # Subject: CN = etcdctl-client
```

---

### Apply certificates

In the first terminal, start etcd in the foreground. The data directory is unique to this run.

```sh

./etcd \
  --name=mtls-lab \
  --advertise-client-urls=https://127.0.0.1:2379 \
  --listen-client-urls=https://127.0.0.1:2379 \
  --client-cert-auth=true \
  --trusted-ca-file=certs/ca.crt \
  --cert-file=certs/etcd.crt \
  --key-file=certs/etcd.key
```

- `--cert-file` and `--key-file` configure the server's identity.
- `--trusted-ca-file` identifies the CA that etcd trusts for client certificates.
- `--client-cert-auth=true` requires clients to present a valid certificate signed by the trusted CA.

In a second terminal, configure `etcdctl` and test the connection:

```sh
export ETCD_VERSION=v3.6.14
cd "/tmp/etcd-${ETCD_VERSION}-linux-amd64"

# Confirm that the endpoint is healthy.
./etcdctl --endpoints=https://127.0.0.1:2379 --cacert=certs/ca.crt --cert=certs/etcdctl.crt --key=certs/etcdctl.key endpoint health
# 127.0.0.1:2379 is healthy: successfully committed proposal: took = 9.633138ms

# mTLS fails without ca, cert, key
./etcdctl put /lab/mtls "hello-mtls"
# {"level":"warn","ts":"2026-09-04T23:28:54.905772-0400","logger":"etcd-client","caller":"v3@v3.6.14/retry_interceptor.go:68","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00030a960/127.0.0.1:2379","peer":"Peer{Addr: <nil>, LocalAddr: <nil>, AuthInfo: <nil>}","method":"/etcdserverpb.KV/Put","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = latest balancer error: connection error: desc = \"error reading server preface: connection reset by peer\""}
# Error: context deadline exceeded

# success with ca, cert, key
./etcdctl --endpoints=https://127.0.0.1:2379 --cacert=certs/ca.crt --cert=certs/etcdctl.crt --key=certs/etcdctl.key put /lab/mtls "hello-mtls"
# OK

./etcdctl --endpoints=https://127.0.0.1:2379 --cacert=certs/ca.crt --cert=certs/etcdctl.crt --key=certs/etcdctl.key get /lab/mtls
# /lab/mtls
# hello-mtls
```
