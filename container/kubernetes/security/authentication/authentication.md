# Kubernetes Security: Authentication

[Back](../../index.md)

- [Kubernetes Security: Authentication](#kubernetes-security-authentication)
  - [Authentication](#authentication)
  - [State Token File](#state-token-file)
  - [TLS in k8s](#tls-in-k8s)
    - [Certificates in K8s](#certificates-in-k8s)
    - [Certificate Creation](#certificate-creation)
  - [Lab: Generate Cert and Key with Openssl](#lab-generate-cert-and-key-with-openssl)
    - [Cerfiticate Authority(CA) Certificate](#cerfiticate-authorityca-certificate)
    - [Client Certificates](#client-certificates)
    - [Server Certificate](#server-certificate)
    - [Kubelet](#kubelet)
    - [View the certificate](#view-the-certificate)
  - [Troubleshooting `kubeadm` TLS cert](#troubleshooting-kubeadm-tls-cert)
  - [Certificate Management](#certificate-management)
    - [Lab: CertificateSigninRequest](#lab-certificatesigninrequest)

---

## Authentication

- Who are the candidate to access the cluster:

| candidate     | Description                 |
| ------------- | --------------------------- |
| Admin         | User of the cluster         |
| Developer     | User of the cluster         |
| User          | Handled by the application  |
| Bot/3rd party | Handled as service accounts |

- K8s cannot manage the user of the cluster, like create/list
- K8s can manage the serviceaccount, like `kubectl create serviceaccount` / `kubectl get serviceaccount`

- All user of the cluser are managed by the `API Server`.

- Methods of auth mechanisms
  - state token file
  - certificates
  - 3rd-party identity services, e.g., LDAP, Kerberos

---

## State Token File

- Not a recommended method in production env

  - only for learning purpose
  - deprecated in v1.19

- csv file

```csv
# /tmp/users/user-details.csv
password123,user10,u0010,group1
password123,user11,u0011,group1
```

- Edit the API server static pod
  - mount volume that contains csv file

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
      <content-hidden>
    image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
    name: kube-apiserver
    volumeMounts:
    - mountPath: /tmp/users
      name: usr-details
      readOnly: true
  volumes:
  - hostPath:
      path: /tmp/users
      type: DirectoryOrCreate
    name: usr-details



--token-auth-file=user-token-details.csv
```

- Modify the kube-apiserver **startup options** to include the basic-auth file

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
    - command:
        - kube-apiserver
        - --authorization-mode=Node,RBAC
          <content-hidden>
        - --basic-auth-file=/tmp/users/user-details.csv
```

- Create the necessary roles and role bindings for these users:

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""] # "" indicates the core API group
    resources: ["pods"]
    verbs: ["get", "watch", "list"]

---
# This role binding allows "jane" to read pods in the "default" namespace.
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods
  namespace: default
subjects:
  - kind: User
    name: user1 # Name is case sensitive
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role #this must be Role or ClusterRole
  name: pod-reader # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
```

- authenticate into the kube-api server using the users credentials

```sh
curl -v -k https://localhost:6443/api/v1/pods -u "user1:password123"
```

---


## TLS in k8s

- `Server certificate` for all servers
- `client certificate` for all clients

---

### Certificates in K8s

- Server Cerfiticate

  - `API server`
    - server certificate: `apiserver.crt`
    - private key: `apiserver.key`
  - `etcd server`
    - `API server` connect with `etcd server` as a **client** with the same crt and key/a new crt and key
    - server certificate: `etcdserver.crt`
    - private key: `etcdserver.key`
  - `kubelet server`
    - `API server` connect with `kubelet server` as a **client** with the same crt and key/a new crt and key
    - server certificate: `kubelet.crt`
    - private key: `kubelet.key`

- Client certificate

  - `Admin`:
    - connect with `API server` via `kubectl` REST API
    - Client certificate: `admin.crt`
    - private key: `admin.key`
  - `Scheduler`:
    - Connec with `API server` as a **client**
    - Client certificate: `scheduler.crt`
    - private key: `scheduler.key`
  - `Controller Manager`:
    - Connec with `API server` as a **client**
    - Client certificate: `controller-manager.crt`
    - private key: `controller-manager.key`
  - `Kube-proxy`:
    - Connec with `API server` as a **client**
    - Client certificate: `kube-proxy.crt`
    - private key: `kube-proxy.key`

- CA
  - K8s requires at least one CA within the k8s
  - has its own cert and key
  - CA certificate: `ca.crt`
  - CA key: `ca.key`

---

### Certificate Creation

- tools:
  - openssl
  - easyrsa
  - cfssl

---

## Lab: Generate Cert and Key with Openssl

### Cerfiticate Authority(CA) Certificate

```sh
# generate keys
openssl genrsa -out ca.key 2048
# ca.key

# generate CSR
openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" -out ca.crs
# ca.csr

# sign certificate
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
# ca.crt
```

---

### Client Certificates

- Admin user

```sh
# generate keys
openssl genrsa -out admin.key 2048
# admin.key

# generate CSR; OU=system:masters: specify the group
openssl req -new -key admin.key -subj "/CN=kube-admin/OU=system:masters" -out admin.crs
# admin.csr

# sign client certificate with the created ca
openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt
# admin.crt
```

- Kube Scheduler

```sh
# generate keys
openssl genrsa -out scheduler.key 2048
# scheduler.key

# generate CSR; OU=system:kube-scheduler: specify the group
openssl req -new -key scheduler.key -subj "/CN=kube-scheduler/OU=system:kube-scheduler" -out scheduler.crs
# scheduler.csr

# sign client certificate with the created ca
openssl x509 -req -in scheduler.csr -CA ca.crt -CAkey ca.key -out scheduler.crt
# scheduler.crt
```

- Kube Control Manager

```sh
# generate keys
openssl genrsa -out controller-manager.key 2048
# controller-manager.key

# generate CSR; OU=system:kube-controller-manager: specify the group
openssl req -new -key controller-manager.key -subj "/CN=kube-controller-manager/OU=system:kube-controller-manager" -out controller-manager.crs
# controller-manager.csr

# sign client certificate with the created ca
openssl x509 -req -in controller-manager.csr -CA ca.crt -CAkey ca.key -out controller-manager.crt
# controller-manager.crt
```

- Kube proxy

```sh
# generate keys
openssl genrsa -out kube-proxy.key 2048
# kube-proxy.key

# generate CSR; OU=system:kube-proxy: specify the group
openssl req -new -key kube-proxy.key -subj "/CN=kube-proxy/OU=system:kube-proxy" -out kube-proxy.crs
# kube-proxy.csr

# sign client certificate with the created ca
openssl x509 -req -in kube-proxy.csr -CA ca.crt -CAkey ca.key -out kube-proxy.crt
# kube-proxy.crt
```

---

- Apply the certificate

```sh
# admin request for API server
curl https://kube-apiserver:6443/api/v1/pods \
    --key admin.key     \
    --cert admin.crt    \
    --cacert ca.crt
```

- Use with kube config

```yaml
apiVersion: v1
kind: Config
clusters:
  - cluster:
      certificate-authority: ca.crt
      server: https://kube-apis
users:
  - name: kubernetes-admin
    user:
      client-certificate: admin.crt
      client-key: admin.key
```

---

### Server Certificate

- etcd server

```sh
# generate keys
openssl genrsa -out etcdserver.key 2048
# etcdserver.key

etcd
  --advertise-client-urls=https://127.0.0.1:2379
  --key-file=/path-to-certs/etcdserver.key      # key
  --cert-file=/path-to-certs/etcdserver.crt     # cert
  --client-cert-auth=true
  --data-dir=/var/lib/etcd
  --initial-advertise-peer-urls=https://127.0.0.1:2380
  --initial-cluster=master=https://127.0.0.1:2380
  --listen-client-urls=https://127.0.0.1:2379
  --listen-peer-urls=https://127.0.0.1:2380
  --name=master
  --peer-cert-file=/path-to-certs/etcdpeer1.crt     # peer cert if multiple etcd
  --peer-client-cert-auth=true                      # peer client cert if multiple etcd
  --peer-key-file=/etc/kubernetes/pki/etcd/peer.key     # peer key if multiple etcd
  --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt    # peer ca key if multiple etcd
  --snapshot-count=10000
  --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt         # ca cert

```

---

- Kube API Server
  - can have alias
    - all alias must be represented in the cert

```sh
# generate keys
openssl genrsa -out apiserver.key 2048
# apiserver.key

# generate CSR;
openssl req -new -key apiserver.key -subj "/CN=kube-apiserver" -out apiserver.crs
# apiserver.csr
```

- To specify all the alias
  - openssl.cnf

```cnf
[req]
req_extensions = v3_req
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,
subjectAltName = @alt_names
[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
IP.1 = 10.96.0.1
IP.2 = 172.17.0.87
```

- Create server cert

```sh
openssl x509 -req -in apiserver.csr -CA ca.crt -CAkey ca.key -out apiserver.crt
```

- Specify the api server key
  - service configuration file

```conf
ExecStart=/usr/local/bin/kube-apiserver \\
--advertise-address=${INTERNAL_IP} \\
--allow-privileged=true \\
--apiserver-count=3 \\
--authorization-mode=Node,RBAC \\
--bind-address=0.0.0.0 \\
--enable-swagger-ui=true \\
--etcd-cafile=/var/lib/kubernetes/ca.pem \\         # ca public key for etcd
--etcd-certfile=/var/lib/kubernetes/apiserver-etcd-client.crt \\        # client cert for etcd
--etcd-keyfile=/var/lib/kubernetes/apiserver-etcd-client.key \\         # client keky for etcd
--etcd-servers=https://127.0.0.1:2379 \\
--event-ttl=1h \\
--kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\           # ca public key for kubelet
--kubelet-client-certificate=/var/lib/kubernetes/apiserver-etcd-client.crt \\   # client cert for kubelet
--kubelet-client-key=/var/lib/kubernetes/apiserver-etcd-client.key \\           # client key for kubelet
--kubelet-https=true \\
--runtime-config=api/all \\
--service-account-key-file=/var/lib/kubernetes/service-account.pem \\
--service-cluster-ip-range=10.32.0.0/24 \\
--service-node-port-range=30000-32767 \\
--client-ca-file=/var/lib/kubernetes/ca.pem \\      # ca public key for api server
--tls-cert-file=/var/lib/kubernetes/apiserver.crt \\        # client cert for api server
--tls-private-key-file=/var/lib/kubernetes/apiserver.key \\ # client key for api server
--v=2
```

---

### Kubelet

- Server Certificates
  - kubectl send request from api server
  - name after the node name

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  x509:
    clientCAFile: "/var/lib/kubernetes/ca.pem" # ca public key
authorization:
  mode: Webhook
clusterDomain: "cluster.local"
clusterDNS:
  - "10.32.0.10"
podCIDR: "${POD_CIDR}"
resolvConf: "/run/systemd/resolve/resolv.conf"
runtimeRequestTimeout: "15m"
tlsCertFile: "/var/lib/kubelet/kubelet-node01.crt" # server cert for kubelet on a node
tlsPrivateKeyFile: "/var/lib/kubelet/kubeletnode01.key" # server key for kubelet on a node
```

- Client Certificates
  - kubelet send request to api server

---

### View the certificate

- Based on how the cluster is set up:

- Cluster created manually

```sh
cat /etc/systemd/system/kube-apiserver.service

<!-- [Service]
ExecStart=/usr/local/bin/kube-apiserver \\
--advertise-address=172.17.0.32 \\
--allow-privileged=true \\
--apiserver-count=3 \\
--authorization-mode=Node,RBAC \\
--bind-address=0.0.0.0 \\
--client-ca-file=/var/lib/kubernetes/ca.pem \\
--enable-swagger-ui=true \\
--etcd-cafile=/var/lib/kubernetes/ca.pem \\
--etcd-certfile=/var/lib/kubernetes/kubernetes.pem \\
--etcd-keyfile=/var/lib/kubernetes/kubernetes-key.pem \\
--event-ttl=1h \\
--kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\
--kubelet-client-key=/var/lib/kubernetes/kubernetes-key.pem \\
--kubelet-https=true \\
--service-node-port-range=30000-32767 \\
--tls-cert-file=/var/lib/kubernetes/kubernetes.pem \\
--tls-private-key-file=/var/lib/kubernetes/kubernetes-key.pem
--v=2 -->
```

- Cluster created by kubeadm

```sh
cat /etc/kubernetes/manifests/kube-apiserver.yaml
# spec:
#   containers:
#   - command:
#     - kube-apiserver
#     - --authorization-mode=Node,RBAC
#     - --advertise-address=172.17.0.32
#     - --allow-privileged=true
#     - --client-ca-file=/etc/kubernetes/pki/ca.crt
#     - --disable-admission-plugins=PersistentVolumeLabel
#     - --enable-admission-plugins=NodeRestriction
#     - --enable-bootstrap-token-auth=true
#     - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
#     - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.cr- --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key- --etcd-servers=https://127.0.0.1:2379
#     - --insecure-port=0
#     - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-k- --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-c- --kubelet-preferred-address-types=InternalIP,ExternalIP,Host- --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-cli- --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-clie- --requestheader-allowed-names=front-proxy-client

```

---

## Troubleshooting `kubeadm` TLS cert

- View API server TLS cert

```sh
cat /etc/kubernetes/manifests/kube-apiserver.yaml
# spec:
#   containers:
#   - command:
#     - kube-apiserver
#     - --authorization-mode=Node,RBAC
#     - --advertise-address=172.17.0.32
#     - --allow-privileged=true
#     - --client-ca-file=/etc/kubernetes/pki/ca.crt               # ca cert
#     - --disable-admission-plugins=PersistentVolumeLabel
#     - --enable-admission-plugins=NodeRestriction
#     - --enable-bootstrap-token-auth=true
#     - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt                         # etcd ca cert
#     - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt         # etcd client cert
#     - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key          # etcd client key
#     - --etcd-servers=https://127.0.0.1:2379
#     - --insecure-port=0
#     - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt     # kubelet client cert
#     - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key             # kubelet client key
#     - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
#     - --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
#     - --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
#     - --secure-port=6443
#     - --service-account-key-file=/etc/kubernetes/pki/sa.pub
#     - --service-cluster-ip-range=10.96.0.0/12
#     - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt                                 # api server cert
#     - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key                          # api esrver key

```

- Decode the API certificate
  - Verify
    - the subject name: `CN=kube-apiserver`
    - Alternative Name: the alias of the api server
    - the cert is not expired: `Validity.Not After`
    - Issuer: `Issuer: CN=kubernetes`

```sh
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
# Certificate:
#   Data:
#     Version: 3 (0x2)
#     Serial Number: 3147495682089747350 (0x2bae26a58f090396)
#   Signature Algorithm: sha256WithRSAEncryption
#     Issuer: CN=kubernetes
#     Validity
#       Not Before: Feb 11 05:39:19 2019 GMT
#       Not After : Feb 11 05:39:20 2020 GMT
#     Subject: CN=kube-apiserver
#     Subject Public Key Info:
#       Public Key Algorithm: rsaEncryption
#         Public-Key: (2048 bit)
#         Modulus:
#           00:d9:69:38:80:68:3b:b7:2e:9e:25:00:e8:fd:01:

#         Exponent: 65537 (0x10001)
#     X509v3 extensions:
#       X509v3 Key Usage: critical
#         Digital Signature, Key Encipherment
#       X509v3 Extended Key Usage:
#         TLS Web Server Authentication
#       X509v3 Subject Alternative Name:
#         DNS:master, DNS:kubernetes, DNS:kubernetes.default,
# DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster.local, IP
# Address:10.96.0.1, IP Address:172.17.0.27
```

- Example:
  - Used the same procedure to identify all the information
  - issues:
    - self sign cert
    - ca.crt expired

| Certificate Path                                  | CN name                      | Alias | Organization   | Issuer     | Expiration                      |
| ------------------------------------------------- | ---------------------------- | ----- | -------------- | ---------- | ------------------------------- |
| `/etc/kubernetes/pki/apiserver.crt`               | kube-apiserver               |       |                | kubernetes | kubernetes Feb 11 05:39:20 2020 |
| `/etc/kubernetes/pki/apiserver.key`               |                              |       |                |            |                                 |
| `/etc/kubernetes/pki/ca.crt`                      | kubernetes                   |       |                | kubernetes | kubernetes Feb 8 05:39:19 2029  |
| `/etc/kubernetes/pki/apiserver-kubeletclient.crt` | kube-apiserver-kubeletclient |       | system:masters | kubernetes | Feb 11 05:39:20 2020            |
| `/etc/kubernetes/pki/apiserver-etcd-client.crt`   | kube-apiserver-etcd-client   |       | system:masters | **self**   | Feb 11 05:39:22 2020            |
| `/etc/kubernetes/pki/etcd/ca.crt `                | kubernetes                   |       |                | kubernetes | **Feb 8 05:39:21 2017**         |

---

- Troubleshotting by inspecting services logs

```sh
# manual setup
journalctl -u etcd.service -l

# kubeadm setup
kubectl logs etcd-master

# if the api server / etcd is down
# identify etcd container_id
crictl ps -a
# view etcd log
crictl logs container_id

```

- Common Issues caused by the cert is the in correct path of the certificate.

  - update the correct cert path
  - wait until the pod of api server / etcd recreated.

- Common path:
  - api server ca cert:
  - etcd ca cert:

---

## Certificate Management

- CA server

  - server to store the certificate key file and sign certificate.

- Certificate API

  - an API to automate the process of rotating certificates.
  - The admin creates CertificateSigningRequest Object
    - when a user sends the CSR to the API
    - this object helps
      - **review** the CSR
      - **approve** the CSR
      - **extract and share** the certificate

- All the certificate operations are handled by the controller manager.
- The controller in Controller Manager

  - `CSR-APPROVING`
  - `CSR-SIGNING`

- The Root certificate(ca cert) must present before the CSR

```sh
cat /etc/kubernetes/manifests/kube-controller-manager.yaml
# spec:
# containers:
# - command:
# - kube-controller-manager
# - --address=127.0.0.1
# - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt  # ca cert
# - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key   # ca key
# - --controllers=*,bootstrapsigner,tokencleaner
# - --kubeconfig=/etc/kubernetes/controller-manager.conf
# - --leader-elect=true
# - --root-ca-file=/etc/kubernetes/pki/ca.crt
# - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
# - --use-service-account-credentials=true
```

---

- A new admin user create cert

```sh
# create key
openssl genrsa -out admin01.key 2048
# admin01.key

# send csr
openssl req -new -key admin01.key -subj "/CN=admin01" -out admin01.csr
# admin01.csr
```

- The admin recieve the csr and encode

```sh
cat admin01.csr | base64
# the encode csr
```

- The admin creates the object

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigninRequest
metadata:
  name: admin01
spec:
  expirationSeconds: 600 # seconds
  usages:
    - digital signature
    - key encipherment
    - server auth
  request:
  # the encode csr
```

- Now all the CSR can be seen by the admin via `kubectl`

```sh
# list csr
kubectl get csr

# approve
kubectl certificate approve admin01
# admin01 approved

# view the approve cert; certificate is encoded with base64, which can be decoded.
kubectl get csr admin01 -o yaml

# decode:
echo "encoded_cert" | base64 --decode
```

---

### Lab: CertificateSigninRequest

- new admin akshay send the cert and key to admin

```sh
cat akshay.csr
# -----BEGIN CERTIFICATE REQUEST-----
# MIICVjCCAT4CAQAwETEPMA0GA1UEAwwGYWtzaGF5MIIBIjANBgkqhkiG9w0BAQEF
# AAOCAQ8AMIIBCgKCAQEAj83f+eLE2+qzaBUobPtpSRkoJpTIjgXzF6k4KsD23EFB
# i/NmTQnQ8lvt1pw0vx2FnMGNTuoVDDAhI54sJ4YlBJEECEDepwlxPhnJqa0/uWvB
# o3p+MWdY2LemI5OK4rzOWSDeq+PLo0yP4yC/rgjwsuIPvpz+Y9/BNK07DEs+0atc
# 9FKF4bd61iA3SWAhbYlyaQ54orqSJUDjmOVzp3R9Uuh/tOM5dAEOfqkhRK8JT5sL
# q7vTkxzH4lnnNSxLQk1yAA6T0qupz0CqmRwLO1gnzyd7DUAjuam+BdFAK0cNhpJ0
# Nko8bKWhMsyljbTfUFOSSFy7OyRfG7gmn8/71QBC3QIDAQABoAAwDQYJKoZIhvcN
# AQELBQADggEBADObh3ZjxLupSpqS0vDAn3pTfqSENPjgw2AqcgYlnSq1xef5VoM7
# /3dQ/kocXQDOTMMajojK/hW9DGOUxu5Hd1tjpFfZZIotWFolj5RkqNOZjz2iFhJC
# kS8aln/+rUN48gZGY/8w9DkSd7U+CRQD0LhqpFCNmS1L48YMBecfn0PT8u5wH/39
# rJQr6T715NnpFOqRM/84CP48OK9PBrUGzZl6WbRim3T08k1hw0Ynkm57KoSTxTOG
# 2/v/kKxWQnUcHr3oZ2l/7QPjw6RycaFaiB7spgACp/HvHwAK8QnGUqFORRU0wSMd
# 2ELyQyUHNYQsX/ifGNTum6Md79/SllhR6qc=
# -----END CERTIFICATE REQUEST-----

cat akshay.key
# -----BEGIN PRIVATE KEY-----
# MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCPzd/54sTb6rNo
# FShs+2lJGSgmlMiOBfMXqTgqwPbcQUGL82ZNCdDyW+3WnDS/HYWcwY1O6hUMMCEj
# niwnhiUEkQQIQN6nCXE+GcmprT+5a8Gjen4xZ1jYt6Yjk4rivM5ZIN6r48ujTI/j
# IL+uCPCy4g++nP5j38E0rTsMSz7Rq1z0UoXht3rWIDdJYCFtiXJpDniiupIlQOOY
# 5XOndH1S6H+04zl0AQ5+qSFErwlPmwuru9OTHMfiWec1LEtCTXIADpPSq6nPQKqZ
# HAs7WCfPJ3sNQCO5qb4F0UArRw2GknQ2SjxspaEyzKWNtN9QU5JIXLs7JF8buCaf
# z/vVAELdAgMBAAECggEAD6pyaXMSVhDZ7Y9MgZ7b5+o1LQrNVGeChYPaShIOco0r
# WlcwQFk+6YApR1VqC53oNd0CC2RF2beOjKZJEh8zfi1cHpgOiWzmaMj/ZpwokocS
# J8CK6c/j5mwPTdXfbfb6lcwWZexhfU80Z55kM03nBt3IsE/DCNdR4W6zvZGe7NFP
# 6FBxxvmzu9Fn9jAxhYC8fZq0zEY/QaUAZl6YeS9FvekDtLTlJ3CSosgI5VyDEtTk
# q2Mvuozi8t68O3YawKOr1Aqmg2hIIFV7HTPcSaxotAXAGMC/yDTonjJ0OxQidhfv
# vTpbPUtkSxpC+wmrsTJaWDlb1pj0NZnz30QE4HLYMwKBgQDKZoURnbHO8jzfh1fY
# ghk88EMsyndEd/NW0X9qgfteB2gvgnYTEAt9I/FP2brAfmvkqF4V0NopyVy7YCiP
# LN8j6PxfPCSUe/oE2CipwakCQP9aPtjwFCa5oYGWa8BI0XvFIi3E37dGC88oIyUM
# 2qScRSj72Bp+tvayXIO8LqfTUwKBgQC14uVr0wUgR+NHa/hpIUk7kr9XbV88HGoA
# MFV1Ix2eQesSqJ/20HjNGNxeJEifQXQD8/iH9w4otgR25DAZklvgMvyHKgzUAgU/
# FsZmEFRlvdSBdVKC1oVxm6dV7nxeU/ApZfgONzFQyjVn2wV6ZmgkaJSBTWN0MYvZ
# XxKoTJZ7DwKBgFOEmFZbjvqJJKtMKuiRTp7BucZqyWo8YPIrQnuNpU74mXo5SEW3
# cjYyNaowewphYF4bR6+S3eMuTxCWrkXeSzmDM1iM9b87pUCIfccGvZnLflMb6eKv
# PgeNaG7MiazCnGMNJnu9oN/LkbDLR8eVFSXSuAWr98rf7s5MtKNbUS83AoGAI3zw
# zHfw0RqVotLTNhfzhPcd9D33ze+xUvYbRm6ikcVEy3AxPePxHftSy9+Cd+g6bacF
# f+nZTmItPtFI/URMPtNT6D9xH1CBm4yjCzj2bp96PgQZJEQc50y6eo68n177ReiK
# XKOyMJQzlV7rk7U1bp0lFJF37SzZn4DoUAQZfEsCgYEAxWLN52NPKlZQv6DWX2nL
# h8ajK84dyzQys8BZ9sz3vIpH1RaiSR+o8i9TFeLnk9SDWiKnsCDqX7tUXZgKz/cV
# ZkzCTx8GzcMCGaLweNBTAyZYQ0A2GFX/pRCr+qV366vspe7gzF+XCpAXW5ts4tz9
# fMFTlmRP3EmMkI7B69pxzvs=
# -----END PRIVATE KEY-----
```

- The admin creates the CSR object

```sh
# decode with one line
cat akshay.csr | base64 -w 0
# LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQWo4M2YrZUxFMitxemFCVW9iUHRwU1Jrb0pwVElqZ1h6RjZrNEtzRDIzRUZCCmkvTm1UUW5ROGx2dDFwdzB2eDJGbk1HTlR1b1ZEREFoSTU0c0o0WWxCSkVFQ0VEZXB3bHhQaG5KcWEwL3VXdkIKbzNwK01XZFkyTGVtSTVPSzRyek9XU0RlcStQTG8weVA0eUMvcmdqd3N1SVB2cHorWTkvQk5LMDdERXMrMGF0Ywo5RktGNGJkNjFpQTNTV0FoYllseWFRNTRvcnFTSlVEam1PVnpwM1I5VXVoL3RPTTVkQUVPZnFraFJLOEpUNXNMCnE3dlRreHpINGxubk5TeExRazF5QUE2VDBxdXB6MENxbVJ3TE8xZ256eWQ3RFVBanVhbStCZEZBSzBjTmhwSjAKTmtvOGJLV2hNc3lsamJUZlVGT1NTRnk3T3lSZkc3Z21uOC83MVFCQzNRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBRE9iaDNaanhMdXBTcHFTMHZEQW4zcFRmcVNFTlBqZ3cyQXFjZ1lsblNxMXhlZjVWb003Ci8zZFEva29jWFFET1RNTWFqb2pLL2hXOURHT1V4dTVIZDF0anBGZlpaSW90V0ZvbGo1UmtxTk9aanoyaUZoSkMKa1M4YWxuLytyVU40OGdaR1kvOHc5RGtTZDdVK0NSUUQwTGhxcEZDTm1TMUw0OFlNQmVjZm4wUFQ4dTV3SC8zOQpySlFyNlQ3MTVObnBGT3FSTS84NENQNDhPSzlQQnJVR3pabDZXYlJpbTNUMDhrMWh3MFlua201N0tvU1R4VE9HCjIvdi9rS3hXUW5VY0hyM29aMmwvN1FQanc2UnljYUZhaUI3c3BnQUNwL0h2SHdBSzhRbkdVcUZPUlJVMHdTTWQKMkVMeVF5VUhOWVFzWC9pZkdOVHVtNk1kNzkvU2xsaFI2cWM9Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=

tee csr-akshay.yaml <<EOF
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: akshay
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQWo4M2YrZUxFMitxemFCVW9iUHRwU1Jrb0pwVElqZ1h6RjZrNEtzRDIzRUZCCmkvTm1UUW5ROGx2dDFwdzB2eDJGbk1HTlR1b1ZEREFoSTU0c0o0WWxCSkVFQ0VEZXB3bHhQaG5KcWEwL3VXdkIKbzNwK01XZFkyTGVtSTVPSzRyek9XU0RlcStQTG8weVA0eUMvcmdqd3N1SVB2cHorWTkvQk5LMDdERXMrMGF0Ywo5RktGNGJkNjFpQTNTV0FoYllseWFRNTRvcnFTSlVEam1PVnpwM1I5VXVoL3RPTTVkQUVPZnFraFJLOEpUNXNMCnE3dlRreHpINGxubk5TeExRazF5QUE2VDBxdXB6MENxbVJ3TE8xZ256eWQ3RFVBanVhbStCZEZBSzBjTmhwSjAKTmtvOGJLV2hNc3lsamJUZlVGT1NTRnk3T3lSZkc3Z21uOC83MVFCQzNRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBRE9iaDNaanhMdXBTcHFTMHZEQW4zcFRmcVNFTlBqZ3cyQXFjZ1lsblNxMXhlZjVWb003Ci8zZFEva29jWFFET1RNTWFqb2pLL2hXOURHT1V4dTVIZDF0anBGZlpaSW90V0ZvbGo1UmtxTk9aanoyaUZoSkMKa1M4YWxuLytyVU40OGdaR1kvOHc5RGtTZDdVK0NSUUQwTGhxcEZDTm1TMUw0OFlNQmVjZm4wUFQ4dTV3SC8zOQpySlFyNlQ3MTVObnBGT3FSTS84NENQNDhPSzlQQnJVR3pabDZXYlJpbTNUMDhrMWh3MFlua201N0tvU1R4VE9HCjIvdi9rS3hXUW5VY0hyM29aMmwvN1FQanc2UnljYUZhaUI3c3BnQUNwL0h2SHdBSzhRbkdVcUZPUlJVMHdTTWQKMkVMeVF5VUhOWVFzWC9pZkdOVHVtNk1kNzkvU2xsaFI2cWM9Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # one day
  usages:
  - client auth
EOF

kubectl create -f csr-akshay.yaml
# certificatesigningrequest.certificates.k8s.io/akshay created

# list all csr
kubectl get csr
# NAME        AGE   SIGNERNAME                                    REQUESTOR                  REQUESTEDDURATION   CONDITION
# akshay      58s   kubernetes.io/kube-apiserver-client           kubernetes-admin           24h                 Pending
# csr-ldcqk   29m   kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   <none>              Approved,Issued

# approve the CSR
kubectl certificate approve akshay
# certificatesigningrequest.certificates.k8s.io/akshay approved

# confirm
kubectl get csr
# NAME        AGE     SIGNERNAME                                    REQUESTOR                  REQUESTEDDURATION   CONDITION
# akshay      2m32s   kubernetes.io/kube-apiserver-client           kubernetes-admin           24h                 Approved,Issued
# csr-ldcqk   31m     kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   <none>              Approved,Issued
```

- unknown CSR comes
  - check the groups of this CSR

```sh
kubectl get csr
# NAME          AGE    SIGNERNAME                                    REQUESTOR                  REQUESTEDDURATION   CONDITION
# agent-smith   15s    kubernetes.io/kube-apiserver-client           agent-x                    <none>              Pending
# akshay        3m2s   kubernetes.io/kube-apiserver-client           kubernetes-admin           24h                 Approved,Issued
# csr-ldcqk     32m    kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   <none>              Approved,Issued

# output the csr as yaml
kubectl get csr agent-smith -o yaml
# apiVersion: certificates.k8s.io/v1
# kind: CertificateSigningRequest
# metadata:
#   creationTimestamp: "2025-11-27T20:10:40Z"
#   name: agent-smith
#   resourceVersion: "2906"
#   uid: cceeb551-6c01-465c-b670-3bc55f6d3d1f
# spec:
#   extra:
#     authentication.kubernetes.io/credential-id:
#     - X509SHA256=e41a3feea298ef281987f4ea2c3d65d9ffd5ab6aa6c23ffa9ac696c11115b037
#   groups:
#   - system:masters
#   - system:authenticated
#   request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1dEQ0NBVUFDQVFBd0V6RVJNQThHQTFVRUF3d0libVYzTFhWelpYSXdnZ0VpTUEwR0NTcUdTSWIzRFFFQgpBUVVBQTRJQkR3QXdnZ0VLQW9JQkFRRE8wV0pXK0RYc0FKU0lyanBObzV2UklCcGxuemcrNnhjOStVVndrS2kwCkxmQzI3dCsxZUVuT041TXVxOTlOZXZtTUVPbnJEVU8vdGh5VnFQMncyWE5JRFJYall5RjQwRmJtRCs1eld5Q0sKeTNCaWhoQjkzTUo3T3FsM1VUdlo4VEVMcXlhRGtuUmwvanYvU3hnWGtvazBBQlVUcFdNeDRCcFNpS2IwVSt0RQpJRjVueEF0dE1Wa0RQUTdOYmVaUkc0M2IrUVdsVkdSL3o2RFdPZkpuYmZlek90YUF5ZEdMVFpGQy93VHB6NTJrCkVjQ1hBd3FDaGpCTGt6MkJIUFI0Sjg5RDZYYjhrMzlwdTZqcHluZ1Y2dVAwdEliT3pwcU52MFkwcWRFWnB3bXcKajJxRUwraFpFV2trRno4MGxOTnR5VDVMeE1xRU5EQ25JZ3dDNEdaaVJHYnJBZ01CQUFHZ0FEQU5CZ2txaGtpRwo5dzBCQVFzRkFBT0NBUUVBUzlpUzZDMXV4VHVmNUJCWVNVN1FGUUhVemFsTnhBZFlzYU9SUlFOd0had0hxR2k0CmhPSzRhMnp5TnlpNDRPT2lqeWFENnRVVzhEU3hrcjhCTEs4S2czc3JSRXRKcWw1ckxaeTlMUlZyc0pnaEQ0Z1kKUDlOTCthRFJTeFJPVlNxQmFCMm5XZVlwTTVjSjVURjUzbGVzTlNOTUxRMisrUk1uakRRSjdqdVBFaWM4L2RoawpXcjJFVU02VWF3enlrcmRISW13VHYybWxNWTBSK0ROdFYxWWllKzBIOS9ZRWx0K0ZTR2poNUw1WVV2STFEcWl5CjRsM0UveTNxTDcxV2ZBY3VIM09zVnBVVW5RSVNNZFFzMHFXQ3NiRTU2Q0M1RGhQR1pJcFVibktVcEF3a2ErOEUKdndRMDdqRytocGtueG11RkFlWHhnVXdvZEFMYUo3anUvVERJY3c9PQotLS0tLUVORCBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0K
#   signerName: kubernetes.io/kube-apiserver-client
#   usages:
#   - digital signature
#   - key encipherment
#   - server auth
#   username: agent-x
# status: {}

# reject the CSR
kubectl certificate deny agent-smith
# certificatesigningrequest.certificates.k8s.io/agent-smith denied

# confirm
kubectl get csr
# NAME          AGE     SIGNERNAME                                    REQUESTOR                  REQUESTEDDURATION   CONDITION
# agent-smith   8m47s   kubernetes.io/kube-apiserver-client           agent-x                    <none>              Denied
# akshay        11m     kubernetes.io/kube-apiserver-client           kubernetes-admin           24h                 Approved,Issued
# csr-ldcqk     40m     kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   <none>              Approved,Issued

# delete CSR object
kubectl delete csr agent-smith
# certificatesigningrequest.certificates.k8s.io "agent-smith" deleted

# confirm
kubectl get csr
# NAME        AGE   SIGNERNAME                                    REQUESTOR                  REQUESTEDDURATION   CONDITION
# akshay      12m   kubernetes.io/kube-apiserver-client           kubernetes-admin           24h                 Approved,Issued
# csr-ldcqk   41m   kubernetes.io/kube-apiserver-client-kubelet   system:node:controlplane   <none>              Approved,Issued
```
