# Advanced - Install cluster with binary

[back](../../index.md)

- [Advanced - Install cluster with binary](#advanced---install-cluster-with-binary)
    - [Configure PKI / Certificate Authority](#configure-pki--certificate-authority)
      - [Root CA](#root-ca)
      - [Identity table](#identity-table)
      - [Generate client certificates](#generate-client-certificates)
      - [Front-proxy certificates](#front-proxy-certificates)
      - [Kubelet certificate (control plane node)](#kubelet-certificate-control-plane-node)
      - [API server serving certificate](#api-server-serving-certificate)
      - [Create etcd certificates](#create-etcd-certificates)
      - [Install certificates](#install-certificates)
    - [Configure Kubeconfig](#configure-kubeconfig)
    - [Install `etcd`](#install-etcd)
    - [Prepare directories](#prepare-directories)
    - [Encryption at rest](#encryption-at-rest)
    - [Audit policy](#audit-policy)
    - [Install `kube-apiserver`](#install-kube-apiserver)
    - [Install `kube-controller-manager`](#install-kube-controller-manager)
    - [Install `kube-scheduler`](#install-kube-scheduler)
    - [Verify control plane](#verify-control-plane)
  - [Confirm encryption at rest](#confirm-encryption-at-rest)
    - [RBAC for apiserver -\> kubelet](#rbac-for-apiserver---kubelet)
  - [Install `kubelet` and `kube-proxy`](#install-kubelet-and-kube-proxy)
  - [Phase 7: CNI](#phase-7-cni)
  - [Phase 8: CoreDNS](#phase-8-coredns)
    - [If CoreDNS is in `CrashLoopBackOff`](#if-coredns-is-in-crashloopbackoff)
  - [Verification](#verification)
    - [Control plane completion checklist](#control-plane-completion-checklist)

---


### Configure PKI / Certificate Authority

#### Root CA

```sh
mkdir -pv ~/pki && cd ~/pki
# mkdir: created directory '/home/ubuntuadmin/pki'

# ##############################
# Configure Root CA
# ##############################
# generate CA private key
openssl genrsa -out ca.key 2048

# self-signed CA cert
openssl req -x509 -new -noenc -key ca.key -sha256 -days 3650 \
  -subj "/CN=kubernetes-ca/O=Kubernetes" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign" \
  -out ca.crt

# confirm
openssl x509 -in ca.crt -noout -subject -ext basicConstraints
# subject=CN = kubernetes-ca, O = Kubernetes
# X509v3 Basic Constraints: critical
#     CA:TRUE
```

#### Identity table

| Cert                       | CN (username)                    | O (group)                        | Purpose                     |
| -------------------------- | -------------------------------- | -------------------------------- | --------------------------- |
| `admin`                    | `admin`                          | `system:masters`                 | your `kubectl` identity     |
| `kube-controller-manager`  | `system:kube-controller-manager` | `system:kube-controller-manager` | controller loops            |
| `kube-scheduler`           | `system:kube-scheduler`          | `system:kube-scheduler`          | scheduling                  |
| `kube-proxy`               | `system:kube-proxy`              | `system:node-proxier`            | Service rules               |
| `kubelet` (per node)       | `system:node:<hostname>`         | `system:nodes`                   | Node authorizer             |
| `kube-apiserver`           | `kube-apiserver`                 | `Kubernetes`                     | serving cert (SANs matter)  |
| `apiserver-kubelet-client` | `kube-apiserver-kubelet-client`  | `system:masters`                 | apiserver -> kubelet        |
| `service-account`          | --                               | --                               | keypair, signs SA tokens    |
| `front-proxy-ca`           | `front-proxy-ca`                 | --                               | separate CA for aggregation |
| `front-proxy-client`       | `front-proxy-client`             | --                               | apiserver -> extension API  |

`system:masters` is hardwired to `cluster-admin`. The node certs' `system:nodes`
group is what the **Node authorizer** keys off -- this is a CKS topic.

#### Generate client certificates

Client certs carry **no SANs** -- identity is the subject alone. That makes
them a loop.

```sh
# ##############################
# Create client cert
# ##############################
cd ~/pki

# shared extension block for pure client certs
cat > client-ext.conf <<'EOF'
[ v3_ext ]
basicConstraints = CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = clientAuth
EOF

# function
gen_client() {
  local name="$1" subj="$2"
  # generate private key
  openssl genrsa -out "${name}.key" 2048
  # create Certificate Signing Requests (CSRs)
  openssl req -new -key "${name}.key" -out "${name}.csr" -subj "${subj}"
  # Signing Certificates
  openssl x509 -req -in "${name}.csr" \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -out "${name}.crt" -days 365 -sha256 \
    -extensions v3_ext -extfile client-ext.conf
  # remove csr
  rm -fv "${name}.csr"
}

# create client certificates: admin
gen_client admin                    "/CN=admin/O=system:masters"
# Certificate request self-signature ok
# subject=CN = admin, O = system:masters

# create client certificates: kube-controller-manager
gen_client kube-controller-manager  "/CN=system:kube-controller-manager/O=system:kube-controller-manager"
# Certificate request self-signature ok
# subject=CN = system:kube-controller-manager, O = system:kube-controller-manager
# removed 'kube-controller-manager.csr'

# create client certificates: kube-scheduler
gen_client kube-scheduler           "/CN=system:kube-scheduler/O=system:kube-scheduler"
# Certificate request self-signature ok
# subject=CN = system:kube-scheduler, O = system:kube-scheduler
# removed 'kube-scheduler.csr'

# create client certificates: kube-proxy
gen_client kube-proxy               "/CN=system:kube-proxy/O=system:node-proxier"
# Certificate request self-signature ok
# subject=CN = system:kube-proxy, O = system:node-proxier
# removed 'kube-proxy.csr'

# create client certificates: apiserver-kubelet-client
gen_client apiserver-kubelet-client "/CN=kube-apiserver-kubelet-client/O=system:masters"
# Certificate request self-signature ok
# subject=CN = kube-apiserver-kubelet-client, O = system:masters
# removed 'apiserver-kubelet-client.csr'

# create client certificates: apiserver-etcd-client
gen_client apiserver-etcd-client    "/CN=kube-apiserver-etcd-client/O=Kubernetes"
# Certificate request self-signature ok
# subject=CN = kube-apiserver-etcd-client, O = Kubernetes
# removed 'apiserver-etcd-client.csr'

# confirm subjects
for c in admin kube-controller-manager kube-scheduler kube-proxy \
         apiserver-kubelet-client apiserver-etcd-client; do
  echo "== $c"; openssl x509 -in "$c.crt" -noout -subject
done
# == admin
# subject=CN = admin, O = system:masters
# == kube-controller-manager
# subject=CN = system:kube-controller-manager, O = system:kube-controller-manager
# == kube-scheduler
# subject=CN = system:kube-scheduler, O = system:kube-scheduler
# == kube-proxy
# subject=CN = system:kube-proxy, O = system:node-proxier
# == apiserver-kubelet-client
# subject=CN = kube-apiserver-kubelet-client, O = system:masters
# == apiserver-etcd-client
# subject=CN = kube-apiserver-etcd-client, O = Kubernetes
```

```sh
# ##############################
# Create service-account. cert
# ##############################
openssl genrsa -out service-account.key 2048
openssl rsa -in service-account.key -pubout -out service-account.pub
# writing RSA ke
```

---

#### Front-proxy certificates

The API aggregation layer (metrics-server, any `APIService`) needs its **own
CA**, separate from the cluster CA. The apiserver proxies a request to an
extension server and asserts the caller's identity in HTTP headers; the
extension server trusts those headers **only** if the connection presents a
cert signed by this CA. Reusing the cluster CA here would let any cluster
client forge a `X-Remote-User: system:masters` header -- a privilege
escalation, and a CKS-relevant reason the two CAs stay separate.

```sh
cd ~/pki

# ##############################
# front-proxy CA
# ##############################
# create private key
openssl genrsa -out front-proxy-ca.key 2048

# create csr
openssl req -x509 -new -noenc -key front-proxy-ca.key -sha256 -days 3650 \
  -subj "/CN=front-proxy-ca" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign" \
  -out front-proxy-ca.crt

# ##############################
# front-proxy client cert
# ##############################
# create private key
openssl genrsa -out front-proxy-client.key 2048

# create csr
openssl req -new -key front-proxy-client.key -out front-proxy-client.csr \
  -subj "/CN=front-proxy-client"

# create csr
openssl x509 -req -in front-proxy-client.csr \
  -CA front-proxy-ca.crt -CAkey front-proxy-ca.key -CAcreateserial \
  -out front-proxy-client.crt -days 365 -sha256 \
  -extensions v3_ext -extfile client-ext.conf

# Certificate request self-signature ok
# subject=CN = front-proxy-client

# remove csr
rm -fv front-proxy-client.csr
# removed 'front-proxy-client.csr'

# confirm: issuer must be front-proxy-ca, not kubernetes-ca
openssl x509 -in front-proxy-client.crt -noout -subject -issuer
# subject=CN = front-proxy-client
# issuer=CN = front-proxy-ca
```

---

#### Kubelet certificate (control plane node)

```sh
# config file for generating a Certificate Signing Request (CSR).
cat > controlplane.conf <<'EOF'
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext

[ dn ]
CN = system:node:controlplane
O = system:nodes

[ req_ext ]
subjectAltName = @alt_names

[ v3_ext ]
basicConstraints = CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = clientAuth,serverAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = controlplane
IP.1  = 192.168.10.180
EOF

# create private key
openssl genrsa -out controlplane.key 2048
# create csr with conf
openssl req -new -key controlplane.key -out controlplane.csr -config controlplane.conf
# sign csr with conf
openssl x509 -req -in controlplane.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out controlplane.crt -days 365 -sha256 \
  -extensions v3_ext -extfile controlplane.conf

# Certificate request self-signature ok
# subject=CN = system:node:controlplane, O = system:nodes

# confirm CN, group and SANs
openssl x509 -in controlplane.crt -noout -subject -ext subjectAltName
# subject=CN = system:node:controlplane, O = system:nodes
# X509v3 Subject Alternative Name:
#     DNS:controlplane, IP Address:192.168.10.180
```

#### API server serving certificate

```sh
# conf file for csr
cat > kube-apiserver.conf <<'EOF'
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext

[ dn ]
CN = kube-apiserver
O = Kubernetes

[ req_ext ]
subjectAltName = @alt_names

[ v3_ext ]
basicConstraints = CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster
DNS.5 = kubernetes.default.svc.cluster.local
DNS.6 = controlplane
DNS.7 = localhost
IP.1  = 10.96.0.1
IP.2  = 192.168.10.180
IP.3  = 127.0.0.1
EOF

# create private key
openssl genrsa -out kube-apiserver.key 2048
# create csr with config file
openssl req -new -key kube-apiserver.key -out kube-apiserver.csr -config kube-apiserver.conf
# sign csr with config file
openssl x509 -req -in kube-apiserver.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out kube-apiserver.crt -days 365 -sha256 \
  -extensions v3_ext -extfile kube-apiserver.conf

# Certificate request self-signature ok
# subject=CN = kube-apiserver, O = Kubernetes

# confirm: every SAN is present
openssl x509 -in kube-apiserver.crt -noout -subject -ext subjectAltName
# subject=CN = kube-apiserver, O = Kubernetes
# X509v3 Subject Alternative Name:
#     DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, DNS:controlplane, DNS:localhost, IP Address:10.96.0.1, IP Address:192.168.10.180, IP Address:127.0.0.1
```

#### Create etcd certificates

```sh
# create conf file
cat > etcd-server.conf <<'EOF'
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext

[ dn ]
CN = etcd
O = Kubernetes

[ req_ext ]
subjectAltName = @alt_names

[ v3_ext ]
basicConstraints = CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth,clientAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = controlplane
DNS.2 = localhost
IP.1  = 192.168.10.180
IP.2  = 127.0.0.1
EOF

# create private key
openssl genrsa -out etcd-server.key 2048
# create csr
openssl req -new -key etcd-server.key -out etcd-server.csr -config etcd-server.conf
# sign csr
openssl x509 -req -in etcd-server.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out etcd-server.crt -days 365 -sha256 \
  -extensions v3_ext -extfile etcd-server.conf

# Certificate request self-signature ok
# subject=CN = etcd, O = Kubernetes

# confirm
openssl x509 -in etcd-server.crt -noout -subject -ext subjectAltName
# subject=CN = etcd, O = Kubernetes
# X509v3 Subject Alternative Name:
#     DNS:controlplane, DNS:localhost, IP Address:192.168.10.180, IP Address:127.0.0.1
```

#### Install certificates

```sh
sudo mkdir -pv /etc/kubernetes/pki
# mkdir: created directory '/etc/kubernetes'
# mkdir: created directory '/etc/kubernetes/pki'

cd ~/pki

# copy files and set permissions
# root ca
sudo install -v -m 644 ca.crt /etc/kubernetes/pki/ca.pem
# 'ca.crt' -> '/etc/kubernetes/pki/ca.pem'
sudo install -v -m 600 ca.key /etc/kubernetes/pki/ca-key.pem
# 'ca.key' -> '/etc/kubernetes/pki/ca-key.pem'

# api server
sudo install -v -m 644 kube-apiserver.crt /etc/kubernetes/pki/kube-apiserver.pem
# 'kube-apiserver.crt' -> '/etc/kubernetes/pki/kube-apiserver.pem'
sudo install -v -m 600 kube-apiserver.key /etc/kubernetes/pki/kube-apiserver-key.pem
# 'kube-apiserver.key' -> '/etc/kubernetes/pki/kube-apiserver-key.pem'

# kubelet client
sudo install -v -m 644 apiserver-kubelet-client.crt /etc/kubernetes/pki/apiserver-kubelet-client.pem
# 'apiserver-kubelet-client.crt' -> '/etc/kubernetes/pki/apiserver-kubelet-client.pem'
sudo install -v -m 600 apiserver-kubelet-client.key /etc/kubernetes/pki/apiserver-kubelet-client-key.pem
# 'apiserver-kubelet-client.key' -> '/etc/kubernetes/pki/apiserver-kubelet-client-key.pem'

# etcd client
sudo install -v -m 644 apiserver-etcd-client.crt /etc/kubernetes/pki/apiserver-etcd-client.pem
# 'apiserver-etcd-client.crt' -> '/etc/kubernetes/pki/apiserver-etcd-client.pem'
sudo install -v -m 600 apiserver-etcd-client.key /etc/kubernetes/pki/apiserver-etcd-client-key.pem
# 'apiserver-etcd-client.key' -> '/etc/kubernetes/pki/apiserver-etcd-client-key.pem'

# etcd server
sudo install -v -m 644 etcd-server.crt /etc/kubernetes/pki/etcd-server.pem
# 'etcd-server.crt' -> '/etc/kubernetes/pki/etcd-server.pem'
sudo install -v -m 600 etcd-server.key /etc/kubernetes/pki/etcd-server-key.pem
# 'etcd-server.key' -> '/etc/kubernetes/pki/etcd-server-key.pem'

# front proxy
sudo install -v -m 644 front-proxy-ca.crt /etc/kubernetes/pki/front-proxy-ca.pem
# 'front-proxy-ca.crt' -> '/etc/kubernetes/pki/front-proxy-ca.pem'
sudo install -v -m 600 front-proxy-ca.key /etc/kubernetes/pki/front-proxy-ca-key.pem
# 'front-proxy-ca.key' -> '/etc/kubernetes/pki/front-proxy-ca-key.pem'
sudo install -v -m 644 front-proxy-client.crt /etc/kubernetes/pki/front-proxy-client.pem
# 'front-proxy-client.crt' -> '/etc/kubernetes/pki/front-proxy-client.pem'
sudo install -v -m 600 front-proxy-client.key /etc/kubernetes/pki/front-proxy-client-key.pem
# 'front-proxy-client.key' -> '/etc/kubernetes/pki/front-proxy-client-key.pem'

# service account
sudo install -v -m 644 service-account.pub /etc/kubernetes/pki/service-account.pem
# 'service-account.pub' -> '/etc/kubernetes/pki/service-account.pem'
sudo install -v -m 600 service-account.key /etc/kubernetes/pki/service-account-key.pem
# 'service-account.key' -> '/etc/kubernetes/pki/service-account-key.pem'

# controlplane
sudo install -v -m 644 controlplane.crt /etc/kubernetes/pki/controlplane.pem
# 'controlplane.crt' -> '/etc/kubernetes/pki/controlplane.pem'
sudo install -v -m 600 controlplane.key /etc/kubernetes/pki/controlplane-key.pem
# 'controlplane.key' -> '/etc/kubernetes/pki/controlplane-key.pem'

# update ownership
sudo chown -Rv root:root /etc/kubernetes/pki
ls -l /etc/kubernetes/pki
# total 56
# -rw------- 1 root root 1704 Sep  2 16:02 apiserver-etcd-client-key.pem
# -rw-r--r-- 1 root root 1241 Sep  2 16:02 apiserver-etcd-client.pem
# -rw------- 1 root root 1704 Sep  2 16:01 apiserver-kubelet-client-key.pem
# -rw-r--r-- 1 root root 1249 Sep  2 16:01 apiserver-kubelet-client.pem
# -rw------- 1 root root 1704 Sep  2 16:00 ca-key.pem
# -rw-r--r-- 1 root root 1204 Sep  2 16:00 ca.pem
# -rw------- 1 root root 1704 Sep  2 16:05 controlplane-key.pem
# -rw-r--r-- 1 root root 1298 Sep  2 16:05 controlplane.pem
# -rw------- 1 root root 1704 Sep  2 16:03 etcd-server-key.pem
# -rw-r--r-- 1 root root 1294 Sep  2 16:03 etcd-server.pem
# -rw------- 1 root root 1704 Sep  2 16:01 kube-apiserver-key.pem
# -rw-r--r-- 1 root root 1476 Sep  2 16:00 kube-apiserver.pem
# -rw------- 1 root root 1704 Sep  2 16:04 service-account-key.pem
# -rw-r--r-- 1 root root  451 Sep  2 16:04 service-account.pem

# confirm cert chains
 for c in kube-apiserver apiserver-kubelet-client apiserver-etcd-client \
         etcd-server controlplane; do
  printf '%-26s ' "$c"
  sudo openssl verify -CAfile /etc/kubernetes/pki/ca.pem \
    "/etc/kubernetes/pki/${c}.pem"
done
# kube-apiserver             /etc/kubernetes/pki/kube-apiserver.pem: OK
# apiserver-kubelet-client   /etc/kubernetes/pki/apiserver-kubelet-client.pem: OK
# apiserver-etcd-client      /etc/kubernetes/pki/apiserver-etcd-client.pem: OK
# etcd-server                /etc/kubernetes/pki/etcd-server.pem: OK
# controlplane               /etc/kubernetes/pki/controlplane.pem: OK

# Inspect any cert to confirm identity
openssl x509 -in /etc/kubernetes/pki/kube-apiserver.pem -noout -subject -ext subjectAltName
# subject=CN = kube-apiserver, O = Kubernetes
# X509v3 Subject Alternative Name:
#     DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, DNS:controlplane, DNS:localhost, IP Address:10.96.0.1, IP Address:192.168.10.180, IP Address:127.0.0.1

# check expiry
openssl x509 -in /etc/kubernetes/pki/kube-apiserver.pem -noout -dates
# notBefore=Sep  2 19:50:25 2026 GMT
# notAfter=Sep  2 19:50:25 2027 GMT
```

---

### Configure Kubeconfig

A kubeconfig bundles _where_ the apiserver is, _who_ you are, and _what CA_ to
trust. One per component.

```sh
# ##############################
# Install kubectl
# ##############################
source /etc/profile.d/k8s-versions.sh

curl -L -o /tmp/kubectl "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kubectl"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 56.3M  100 56.3M    0     0  26.6M      0  0:00:02  0:00:02 --:--:-- 26.6M
sudo install -m 755 /tmp/kubectl /usr/local/bin/kubectl
kubectl version --client
# Client Version: v1.35.8
# Kustomize Version: v5.7.1

# ##############################
# Configure kubeconfig: controlplane
# ##############################
cd ~/pki
# set ip -- every kubeconfig below embeds this. If the variable is empty the
# kubeconfigs get "server: https://:6443" with no host, and the kubelet fails
# with "tls: either ServerName or InsecureSkipVerify must be specified".
export KUBERNETES_PUBLIC_ADDRESS=192.168.10.180

# set cluster: ip
kubectl config set-cluster kubernetes \
  --certificate-authority=ca.crt --embed-certs=true \
  --server=https://${KUBERNETES_PUBLIC_ADDRESS}:6443 \
  --kubeconfig=controlplane.kubeconfig

# Cluster "kubernetes" set.

# confirm
kubectl config get-clusters --kubeconfig=controlplane.kubeconfig
# NAME
# kubernetes

# set credential: controlplane
kubectl config set-credentials system:node:controlplane \
  --client-certificate=controlplane.crt --client-key=controlplane.key \
  --embed-certs=true --kubeconfig=controlplane.kubeconfig

# User "system:node:controlplane" set.

# confirm
kubectl config get-users --kubeconfig=controlplane.kubeconfig
# NAME
# system:node:controlplane

# set default context
kubectl config set-context default \
  --cluster=kubernetes --user=system:node:controlplane \
  --kubeconfig=controlplane.kubeconfig

# Context "default" created.

# confirm
# kubectl config get-contexts --kubeconfig=controlplane.kubeconfig
# CURRENT   NAME      CLUSTER      AUTHINFO                   NAMESPACE
#           default   kubernetes   system:node:controlplane

# use
kubectl config use-context default --kubeconfig=controlplane.kubeconfig
# Switched to context "default".


# ##############################
# Configure kubeconfig: proxy
# ##############################
# set cluster
kubectl config set-cluster kubernetes \
  --certificate-authority=ca.crt --embed-certs=true \
  --server=https://${KUBERNETES_PUBLIC_ADDRESS}:6443 \
  --kubeconfig=kube-proxy.kubeconfig

# Cluster "kubernetes" set.

# set user
kubectl config set-credentials system:kube-proxy \
  --client-certificate=kube-proxy.crt --client-key=kube-proxy.key \
  --embed-certs=true --kubeconfig=kube-proxy.kubeconfig

# User "system:kube-proxy" set.

# set context
kubectl config set-context default --cluster=kubernetes \
  --user=system:kube-proxy --kubeconfig=kube-proxy.kubeconfig

# Context "default" created.

kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig
# Switched to context "default".

# ##############################
# Configure kubeconfig: kube-controller-manager
# ##############################
# set cluster
kubectl config set-cluster kubernetes \
  --certificate-authority=ca.crt --embed-certs=true \
  --server=https://127.0.0.1:6443 \
  --kubeconfig=kube-controller-manager.kubeconfig

# Cluster "kubernetes" set.

# set user
kubectl config set-credentials system:kube-controller-manager \
  --client-certificate=kube-controller-manager.crt \
  --client-key=kube-controller-manager.key \
  --embed-certs=true --kubeconfig=kube-controller-manager.kubeconfig

# User "system:kube-controller-manager" set.

# set context
kubectl config set-context default --cluster=kubernetes \
  --user=system:kube-controller-manager --kubeconfig=kube-controller-manager.kubeconfig

# Context "default" created.

kubectl config use-context default --kubeconfig=kube-controller-manager.kubeconfig
# Switched to context "default".

# ##############################
# Configure kubeconfig: kube-scheduler
# ##############################
# set cluster
kubectl config set-cluster kubernetes \
  --certificate-authority=ca.crt --embed-certs=true \
  --server=https://127.0.0.1:6443 \
  --kubeconfig=kube-scheduler.kubeconfig

# Cluster "kubernetes" set.

# set user
kubectl config set-credentials system:kube-scheduler \
  --client-certificate=kube-scheduler.crt --client-key=kube-scheduler.key \
  --embed-certs=true --kubeconfig=kube-scheduler.kubeconfig

# User "system:kube-scheduler" set.

# set context
kubectl config set-context default --cluster=kubernetes \
  --user=system:kube-scheduler --kubeconfig=kube-scheduler.kubeconfig

# Context "default" created.

kubectl config use-context default --kubeconfig=kube-scheduler.kubeconfig
# Switched to context "default".

# ##############################
# Configure kubeconfig: admin
# ##############################
# set cluster
kubectl config set-cluster kubernetes \
  --certificate-authority=ca.crt --embed-certs=true \
  --server=https://127.0.0.1:6443 --kubeconfig=admin.kubeconfig

# Cluster "kubernetes" set.

# set user
kubectl config set-credentials admin \
  --client-certificate=admin.crt --client-key=admin.key \
  --embed-certs=true --kubeconfig=admin.kubeconfig

# User "admin" set.

# set context
kubectl config set-context default --cluster=kubernetes \
  --user=admin --kubeconfig=admin.kubeconfig

# Context "default" created.

kubectl config use-context default --kubeconfig=admin.kubeconfig
# Switched to context "default".


# ##############################
# Install kubeconfigs: controller-manager, scheduler
# ##############################
# copy kubeconfig to etc
sudo cp -v kube-controller-manager.kubeconfig kube-scheduler.kubeconfig /etc/kubernetes/
# 'kube-controller-manager.kubeconfig' -> '/etc/kubernetes/kube-controller-manager.kubeconfig'
# 'kube-scheduler.kubeconfig' -> '/etc/kubernetes/kube-scheduler.kubeconfig'

# set permission
sudo chmod -v 600 /etc/kubernetes/*.kubeconfig
# mode of '/etc/kubernetes/kube-controller-manager.kubeconfig' retained as 0600 (rw-------)
# mode of '/etc/kubernetes/kube-scheduler.kubeconfig' retained as 0600 (rw-------)

# ##############################
# Install kubeconfigs: kubelet
# ##############################
sudo mkdir -pv /var/lib/kubelet
# mkdir: created directory '/var/lib/kubelet'
sudo cp -v controlplane.kubeconfig /var/lib/kubelet/kubeconfig
# 'controlplane.kubeconfig' -> '/var/lib/kubelet/kubeconfig'

# set permissions
sudo chmod -v 600 /var/lib/kubelet/kubeconfig
# mode of '/var/lib/kubelet/kubeconfig' retained as 0600 (rw-------)

# ##############################
# Install kubeconfigs: proxy
# ##############################
sudo mkdir -pv /var/lib/kube-proxy
# mkdir: created directory '/var/lib/kube-proxy'
sudo cp -v kube-proxy.kubeconfig   /var/lib/kube-proxy/kubeconfig
# 'kube-proxy.kubeconfig' -> '/var/lib/kube-proxy/kubeconfig'

# set permission
sudo chmod -v 600 /var/lib/kube-proxy/kubeconfig
# mode of '/var/lib/kube-proxy/kubeconfig' retained as 0600 (rw-------)

# ##############################
# confirm every kubeconfig embedded a real host, not https://:6443
# ##############################
sudo grep -H 'server:' /var/lib/kubelet/kubeconfig /var/lib/kube-proxy/kubeconfig   /etc/kubernetes/*.kubeconfig ~/.kube/config
# each must show  server: https://192.168.10.180:6443  (or https://127.0.0.1:6443
# for the local control-plane clients) -- an empty host means
# KUBERNETES_PUBLIC_ADDRESS was unset when the kubeconfig was generated

# ##############################
# Install Kubernetes Root Certificate Authority (CA)
# ##############################
sudo mkdir -pv /var/lib/kubernetes
# mkdir: created directory '/var/lib/kubernetes'
sudo install -v -m 644 ca.crt /var/lib/kubernetes/ca.pem
# 'ca.crt' -> '/var/lib/kubernetes/ca.pem'

# ##############################
# Install kubeconfigs: admin
# ##############################
mkdir -pv ~/.kube
# mkdir: created directory '/home/ubuntuadmin/.kube'
cp -v admin.kubeconfig ~/.kube/config
# 'admin.kubeconfig' -> '/home/ubuntuadmin/.kube/config'

# set permissions
chmod -v 600 ~/.kube/config
# mode of '/home/ubuntuadmin/.kube/config' retained as 0600 (rw-------)


# ##############################
# Confirm kubeconfig
# ##############################
cd ~/pki
for f in controlplane kube-proxy kube-controller-manager kube-scheduler admin; do
  printf '%-26s ' "$f"
  kubectl config view --kubeconfig=$f.kubeconfig -o jsonpath='{.users[0].name} -> {.clusters[0].cluster.server}'
  echo
done
# controlplane               system:node:controlplane -> https://:6443
# kube-proxy                 system:kube-proxy -> https://:6443
# kube-controller-manager    system:kube-controller-manager -> https://127.0.0.1:6443
# kube-scheduler             system:kube-scheduler -> https://127.0.0.1:6443
# admin                      admin -> https://127.0.0.1:6443

```

---

### Install `etcd`

```sh
source /etc/profile.d/k8s-versions.sh

# ##############################
# Download etcd
# ##############################
cd /tmp
curl -LO "https://github.com/etcd-io/etcd/releases/download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
#   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
# 100 22.5M  100 22.5M    0     0  20.2M      0  0:00:01  0:00:01 --:--:-- 20.2M

tar xzf "etcd-${ETCD_VERSION}-linux-amd64.tar.gz"
sudo install -v -m 755 "etcd-${ETCD_VERSION}-linux-amd64/etcd" "etcd-${ETCD_VERSION}-linux-amd64/etcdctl" /usr/local/bin/
# 'etcd-v3.6.0-linux-amd64/etcd' -> '/usr/local/bin/etcd'
# 'etcd-v3.6.0-linux-amd64/etcdctl' -> '/usr/local/bin/etcdctl'

etcd --version
# etcd Version: 3.6.0
# Git SHA: f5d605a
# Go Version: go1.23.9
# Go OS/Arch: linux/amd64

etcdctl version
# etcdctl version: 3.6.0
# API version: 3.6

# ##############################
# Configure systemd unit: etcd
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/etcd.service
[Unit]
Description=etcd
Documentation=https://github.com/etcd-io/etcd
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/etcd \
  --name controlplane \
  --data-dir=/var/lib/etcd \
  --cert-file=/etc/kubernetes/pki/etcd-server.pem \
  --key-file=/etc/kubernetes/pki/etcd-server-key.pem \
  --peer-cert-file=/etc/kubernetes/pki/etcd-server.pem \
  --peer-key-file=/etc/kubernetes/pki/etcd-server-key.pem \
  --trusted-ca-file=/etc/kubernetes/pki/ca.pem \
  --peer-trusted-ca-file=/etc/kubernetes/pki/ca.pem \
  --client-cert-auth \
  --peer-client-cert-auth \
  --initial-advertise-peer-urls https://192.168.10.180:2380 \
  --listen-peer-urls https://192.168.10.180:2380 \
  --listen-client-urls https://192.168.10.180:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://192.168.10.180:2379 \
  --initial-cluster-token etcd-cluster-0 \
  --initial-cluster controlplane=https://192.168.10.180:2380 \
  --initial-cluster-state new
Restart=on-failure
RestartSec=5
LimitNOFILE=40000

[Install]
WantedBy=multi-user.target
EOF

# reload config
sudo systemctl daemon-reload
# start and enable
sudo systemctl enable --now etcd
# Created symlink /etc/systemd/system/multi-user.target.wants/etcd.service → /etc/systemd/system/etcd.service.

# confirm
sudo systemctl status etcd --no-pager
# ● etcd.service - etcd
#      Loaded: loaded (/etc/systemd/system/etcd.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 17:10:13 EDT; 5min ago
#        Docs: https://github.com/etcd-io/etcd
#    Main PID: 2318 (etcd)
#       Tasks: 10 (limit: 7689)
#      Memory: 10.7M (peak: 11.1M)
#         CPU: 2.271s
#      CGroup: /system.slice/etcd.service
#              └─2318 /usr/local/bin/etcd --name controlplane --data-dir=/var/lib/etcd --cert-file=/etc/kubernetes/pki/etcd-server.pem…

# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.163305-0400","caller":"embed/serve.go:13…equests"}
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.163446-0400","caller":"schema/migration.…:"3.6.0"}
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.165142-0400","caller":"v3rpc/health.go:6…SERVING"}
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.165293-0400","caller":"etcdmain/main.go:… daemon"}
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.165358-0400","caller":"etcdmain/main.go:… daemon"}
# Sep 02 17:10:13 controlplane systemd[1]: Started etcd.service - etcd.
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"warn","ts":"2026-09-02T17:10:13.167682-0400","caller":"v3rpc/grpc.go:52"…tempted"}
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.167839-0400","caller":"v3rpc/health.go:6…SERVING"}
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.169900-0400","caller":"embed/serve.go:28…80:2379"}
# Sep 02 17:10:13 controlplane etcd[2318]: {"level":"info","ts":"2026-09-02T17:10:13.171968-0400","caller":"embed/serve.go:28….1:2379"}
# Hint: Some lines were ellipsized, use -l to show in full.

# test connection
sudo etcdctl member list -w table \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/ca.pem \
  --cert=/etc/kubernetes/pki/etcd-server.pem \
  --key=/etc/kubernetes/pki/etcd-server-key.pem
# +------------------+---------+--------------+-----------------------------+-----------------------------+------------+
# |        ID        | STATUS  |     NAME     |         PEER ADDRS          |        CLIENT ADDRS         | IS LEARNER |
# +------------------+---------+--------------+-----------------------------+-----------------------------+------------+
# | 68b8303d1213ddbb | started | controlplane | https://192.168.10.180:2380 | https://192.168.10.180:2379 |      false |
# +------------------+---------+--------------+-----------------------------+-----------------------------+------------+

# health of the endpoint
sudo etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/ca.pem \
  --cert=/etc/kubernetes/pki/etcd-server.pem \
  --key=/etc/kubernetes/pki/etcd-server-key.pem
# https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 6.349056ms
```

---

### Prepare directories

Both directories below are referenced by the apiserver flags and by nothing
that creates them -- miss these and `kube-apiserver` exits immediately.

```sh
# holds encryption-config.yaml, audit-policy.yaml, kube-scheduler.yaml
sudo mkdir -pv /etc/kubernetes/config
# mkdir: created directory '/etc/kubernetes/config'

# --audit-log-path writes here
sudo mkdir -pv /var/log/kubernetes
# mkdir: created directory '/var/log/kubernetes'
```

---

### Encryption at rest

etcd stores Secrets base64-encoded, not encrypted. This config encrypts them
on write -- a named CKS objective.

```sh
ENCRYPTION_KEY=$(head -c 32 /dev/urandom | base64)

cat <<EOF | sudo tee /etc/kubernetes/config/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: ${ENCRYPTION_KEY}
      - identity: {}
EOF

sudo chmod 600 /etc/kubernetes/config/encryption-config.yaml
```

Provider order matters: `aescbc` first means new writes are encrypted;
`identity` last lets already-plaintext values still be read. Note the heredoc
delimiter here is **unquoted** (`<<EOF`) so `${ENCRYPTION_KEY}` expands -- a
quoted `<<'EOF'` writes the literal string and every Secret write then fails.

---

### Audit policy

```sh
cat <<'EOF' | sudo tee /etc/kubernetes/config/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - RequestReceived
rules:
  - level: RequestResponse
    resources:
      - group: ""
        resources: ["secrets", "configmaps"]
  - level: Metadata
EOF
```

---

### Install `kube-apiserver`

```sh
export K8S_VERSION=v1.35.8

# ##############################
# Download kube-apiserver
# ##############################
cd /tmp
curl -L -o kube-apiserver "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kube-apiserver"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 82.7M  100 82.7M    0     0  6020k      0  0:00:14  0:00:14 --:--:-- 12.1M

sudo install -v -m 755 kube-apiserver /usr/local/bin/
# 'kube-apiserver' -> '/usr/local/bin/kube-apiserver'

kube-apiserver --version
# Kubernetes v1.35.8

# ##############################
# Configure systemd unit: kube-apiserver
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kube-apiserver.service
[Unit]
Description=Kubernetes API Server
Documentation=https://kubernetes.io/docs/concepts/overview/components/
After=etcd.service
Requires=etcd.service

[Service]
ExecStart=/usr/local/bin/kube-apiserver \
  --advertise-address=192.168.10.180 \
  --allow-privileged=true \
  --authorization-mode=Node,RBAC \
  --anonymous-auth=false \
  --client-ca-file=/etc/kubernetes/pki/ca.pem \
  --enable-admission-plugins=NodeRestriction \
  --etcd-servers=https://127.0.0.1:2379 \
  --etcd-cafile=/etc/kubernetes/pki/ca.pem \
  --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.pem \
  --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client-key.pem \
  --encryption-provider-config=/etc/kubernetes/config/encryption-config.yaml \
  --audit-policy-file=/etc/kubernetes/config/audit-policy.yaml \
  --audit-log-path=/var/log/kubernetes/audit.log \
  --audit-log-maxage=30 \
  --audit-log-maxbackup=10 \
  --audit-log-maxsize=100 \
  --kubelet-certificate-authority=/etc/kubernetes/pki/ca.pem \
  --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.pem \
  --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client-key.pem \
  --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.pem \
  --requestheader-allowed-names=front-proxy-client \
  --requestheader-extra-headers-prefix=X-Remote-Extra- \
  --requestheader-group-headers=X-Remote-Group \
  --requestheader-username-headers=X-Remote-User \
  --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.pem \
  --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client-key.pem \
  --secure-port=6443 \
  --service-account-key-file=/etc/kubernetes/pki/service-account.pem \
  --service-account-signing-key-file=/etc/kubernetes/pki/service-account-key.pem \
  --service-account-issuer=https://192.168.10.180:6443 \
  --service-cluster-ip-range=10.96.0.0/12 \
  --tls-cert-file=/etc/kubernetes/pki/kube-apiserver.pem \
  --tls-private-key-file=/etc/kubernetes/pki/kube-apiserver-key.pem \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# reload config
sudo systemctl daemon-reload
# start and enable
sudo systemctl enable --now kube-apiserver
# Created symlink /etc/systemd/system/multi-user.target.wants/kube-apiserver.service → /etc/systemd/system/kube-apiserver.service.

# confirm
sudo systemctl status kube-apiserver --no-pager
# ● kube-apiserver.service - Kubernetes API Server
#      Loaded: loaded (/etc/systemd/system/kube-apiserver.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 17:47:32 EDT; 27s ago
#        Docs: https://kubernetes.io/docs/concepts/overview/components/
#    Main PID: 2915 (kube-apiserver)
#       Tasks: 10 (limit: 7689)
#      Memory: 166.3M (peak: 166.9M)
#         CPU: 2.795s
#      CGroup: /system.slice/kube-apiserver.service
#              └─2915 /usr/local/bin/kube-apiserver --advertise-address=192.168.10.180 --allow-privileged=true --authorization-mode=No…

# Sep 02 17:47:35 controlplane kube-apiserver[2915]: I0902 17:47:35.241719    2915 storage_rbac.go:321] created rolebinding.rb…e-system
# Sep 02 17:47:35 controlplane kube-apiserver[2915]: I0902 17:47:35.245675    2915 storage_rbac.go:321] created rolebinding.rb…e-system
# Sep 02 17:47:35 controlplane kube-apiserver[2915]: I0902 17:47:35.252040    2915 storage_rbac.go:321] created rolebinding.rb…e-system
# Sep 02 17:47:35 controlplane kube-apiserver[2915]: I0902 17:47:35.256057    2915 storage_rbac.go:321] created rolebinding.rb…e-public
# Sep 02 17:47:35 controlplane kube-apiserver[2915]: I0902 17:47:35.293647    2915 alloc.go:329] "allocated clusterIPs" servic…96.0.1"}
# Sep 02 17:47:35 controlplane kube-apiserver[2915]: W0902 17:47:35.299993    2915 lease.go:265] Resetting endpoints for maste….10.180]
# Sep 02 17:47:35 controlplane kube-apiserver[2915]: I0902 17:47:35.300947    2915 controller.go:667] quota admission added ev…ndpoints
# Sep 02 17:47:35 controlplane kube-apiserver[2915]: I0902 17:47:35.304218    2915 controller.go:667] quota admission added ev…y.k8s.io
# Sep 02 17:47:43 controlplane kube-apiserver[2915]: I0902 17:47:43.776787    2915 apf_controller.go:493] "Update CurrentCL" plName="e…
# Sep 02 17:47:53 controlplane kube-apiserver[2915]: I0902 17:47:53.777657    2915 apf_controller.go:493] "Update CurrentCL" plName="e…
# Hint: Some lines were ellipsized, use -l to show in full.

# query the raw endpoint
kubectl get --raw='/readyz?verbose'
# [+]ping ok
# [+]log ok
# [+]etcd ok
# [+]etcd-readiness ok
# [+]informer-sync ok
# [+]poststarthook/start-apiserver-admission-initializer ok
# [+]poststarthook/generic-apiserver-start-informers ok
# [+]poststarthook/priority-and-fairness-config-consumer ok
# [+]poststarthook/priority-and-fairness-filter ok
# [+]poststarthook/storage-object-count-tracker-hook ok
# [+]poststarthook/start-apiextensions-informers ok
# [+]poststarthook/start-apiextensions-controllers ok
# [+]poststarthook/crd-informer-synced ok
# [+]poststarthook/start-system-namespaces-controller ok
# [+]poststarthook/start-cluster-authentication-info-controller ok
# [+]poststarthook/start-kube-apiserver-identity-lease-controller ok
# [+]poststarthook/start-kube-apiserver-identity-lease-garbage-collector ok
# [+]poststarthook/start-legacy-token-tracking-controller ok
# [+]poststarthook/start-service-ip-repair-controllers ok
# [+]poststarthook/rbac/bootstrap-roles ok
# [+]poststarthook/scheduling/bootstrap-system-priority-classes ok
# [+]poststarthook/priority-and-fairness-config-producer ok
# [+]poststarthook/bootstrap-controller ok
# [+]poststarthook/start-kubernetes-service-cidr-controller ok
# [+]poststarthook/aggregator-reload-proxy-client-cert ok
# [+]poststarthook/start-kube-aggregator-informers ok
# [+]poststarthook/apiservice-status-local-available-controller ok
# [+]poststarthook/apiservice-status-remote-available-controller ok
# [+]poststarthook/apiservice-registration-controller ok
# [+]poststarthook/apiservice-discovery-controller ok
# [+]poststarthook/kube-apiserver-autoregistration ok
# [+]autoregister-completion ok
# [+]poststarthook/apiservice-openapi-controller ok
# [+]poststarthook/apiservice-openapiv3-controller ok
# [+]shutdown ok
# readyz check passed
```

---

### Install `kube-controller-manager`

```sh
export K8S_VERSION=v1.35.8

# ##############################
# Download kube-controller-manager
# ##############################
cd /tmp
curl -L -o kube-controller-manager "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kube-controller-manager"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 69.5M  100 69.5M    0     0  11.0M      0  0:00:06  0:00:06 --:--:-- 12.7M

sudo install -v -m 755 kube-controller-manager /usr/local/bin/
# 'kube-controller-manager' -> '/usr/local/bin/kube-controller-manager'

kube-controller-manager --version
# Kubernetes v1.35.8

# ##############################
# Configure systemd unit: kube-controller-manager
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kube-controller-manager.service
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://kubernetes.io/docs/concepts/overview/components/
After=kube-apiserver.service

[Service]
ExecStart=/usr/local/bin/kube-controller-manager \
  --bind-address=127.0.0.1 \
  --cluster-cidr=10.244.0.0/16 \
  --cluster-name=kubernetes \
  --cluster-signing-cert-file=/etc/kubernetes/pki/ca.pem \
  --cluster-signing-key-file=/etc/kubernetes/pki/ca-key.pem \
  --kubeconfig=/etc/kubernetes/kube-controller-manager.kubeconfig \
  --authentication-kubeconfig=/etc/kubernetes/kube-controller-manager.kubeconfig \
  --authorization-kubeconfig=/etc/kubernetes/kube-controller-manager.kubeconfig \
  --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.pem \
  --leader-elect=true \
  --root-ca-file=/etc/kubernetes/pki/ca.pem \
  --service-account-private-key-file=/etc/kubernetes/pki/service-account-key.pem \
  --service-cluster-ip-range=10.96.0.0/12 \
  --use-service-account-credentials=true \
  --allocate-node-cidrs=true \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# reload config
sudo systemctl daemon-reload
# start and enable
sudo systemctl enable --now kube-controller-manager
# Created symlink /etc/systemd/system/multi-user.target.wants/kube-controller-manager.service → /etc/systemd/system/kube-controller-manager.service.

# confirm
sudo systemctl status kube-controller-manager --no-pager
# ● kube-controller-manager.service - Kubernetes Controller Manager
#      Loaded: loaded (/etc/systemd/system/kube-controller-manager.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 17:51:08 EDT; 10s ago
#        Docs: https://kubernetes.io/docs/concepts/overview/components/
#    Main PID: 3370 (kube-controller)
#       Tasks: 7 (limit: 7689)
#      Memory: 36.9M (peak: 37.0M)
#         CPU: 464ms
#      CGroup: /system.slice/kube-controller-manager.service
#              └─3370 /usr/local/bin/kube-controller-manager --bind-address=127.0.0.1 --cluster-cidr=10.244.0.0/16 --cluster-name=kube…

# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.467738    3370 reflector.go:446] "Caches populated…go:161"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.467852    3370 reflector.go:446] "Caches populated…go:161"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.468026    3370 reflector.go:446] "Caches populated…go:138"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.468866    3370 reflector.go:446] "Caches populated…go:161"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.551672    3370 shared_informer.go:377] "Caches are synced"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.551774    3370 garbagecollector.go:166] "Garbage c…synced"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.551787    3370 garbagecollector.go:169] "Proceedin…arbage"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.565674    3370 shared_informer.go:377] "Caches are synced"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.565726    3370 garbagecollector.go:253] "synced ga…lector"
# Sep 02 17:51:13 controlplane kube-controller-manager[3370]: I0902 17:51:13.943447    3370 servicecidrs_controller.go:484] "Up…ason=""
# Hint: Some lines were ellipsized, use -l to show in full.
```

---

### Install `kube-scheduler`

```sh
export K8S_VERSION=v1.35.8

# ##############################
# Download kube-scheduler
# ##############################
cd /tmp
curl -L -o kube-scheduler "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kube-scheduler"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 46.1M  100 46.1M    0     0  11.4M      0  0:00:04  0:00:04 --:--:-- 11.4M

sudo install -v -m 755 kube-scheduler /usr/local/bin/
# 'kube-scheduler' -> '/usr/local/bin/kube-scheduler'

kube-scheduler --version
# Kubernetes v1.35.8

# ##############################
# Configure kube-scheduler
# ##############################
cat <<'EOF' | sudo tee /etc/kubernetes/config/kube-scheduler.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
clientConnection:
  kubeconfig: /etc/kubernetes/kube-scheduler.kubeconfig
leaderElection:
  leaderElect: true
EOF

# ##############################
# Configure systemd unit: kube-scheduler
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kube-scheduler.service
[Unit]
Description=Kubernetes Scheduler
Documentation=https://kubernetes.io/docs/concepts/overview/components/
After=kube-apiserver.service

[Service]
ExecStart=/usr/local/bin/kube-scheduler \
  --config=/etc/kubernetes/config/kube-scheduler.yaml \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# reload config
sudo systemctl daemon-reload
# start and enable
sudo systemctl enable --now kube-scheduler
# Created symlink /etc/systemd/system/multi-user.target.wants/kube-scheduler.service → /etc/systemd/system/kube-scheduler.service.

# confirm
sudo systemctl status kube-scheduler --no-pager
# ● kube-scheduler.service - Kubernetes Scheduler
#      Loaded: loaded (/etc/systemd/system/kube-scheduler.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 17:53:35 EDT; 11s ago
#        Docs: https://kubernetes.io/docs/concepts/overview/components/
#    Main PID: 3613 (kube-scheduler)
#       Tasks: 9 (limit: 7689)
#      Memory: 13.1M (peak: 13.3M)
#         CPU: 242ms
#      CGroup: /system.slice/kube-scheduler.service
#              └─3613 /usr/local/bin/kube-scheduler --config=/etc/kubernetes/config/kube-scheduler.yaml --v=2

# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570145    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570223    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570252    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570263    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570275    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570003    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.570439    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.569931    3613 reflector.go:446] "Caches populated" type="….go:161"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.661775    3613 leaderelection.go:258] "Attempting to acqui…heduler"
# Sep 02 17:53:35 controlplane kube-scheduler[3613]: I0902 17:53:35.668143    3613 leaderelection.go:272] "Successfully acquir…heduler"
# Hint: Some lines were ellipsized, use -l to show in full.
```

---

### Verify control plane

```sh
sudo systemctl status kube-apiserver kube-controller-manager kube-scheduler --no-pager

# component health
kubectl get --raw='/readyz?verbose'
# [+]ping ok
# [+]log ok
# [+]etcd ok
# [+]etcd-readiness ok
# [+]informer-sync ok
# [+]poststarthook/start-apiserver-admission-initializer ok
# [+]poststarthook/generic-apiserver-start-informers ok
# [+]poststarthook/priority-and-fairness-config-consumer ok
# [+]poststarthook/priority-and-fairness-filter ok
# [+]poststarthook/storage-object-count-tracker-hook ok
# [+]poststarthook/start-apiextensions-informers ok
# [+]poststarthook/start-apiextensions-controllers ok
# [+]poststarthook/crd-informer-synced ok
# [+]poststarthook/start-system-namespaces-controller ok
# [+]poststarthook/start-cluster-authentication-info-controller ok
# [+]poststarthook/start-kube-apiserver-identity-lease-controller ok
# [+]poststarthook/start-kube-apiserver-identity-lease-garbage-collector ok
# [+]poststarthook/start-legacy-token-tracking-controller ok
# [+]poststarthook/start-service-ip-repair-controllers ok
# [+]poststarthook/rbac/bootstrap-roles ok
# [+]poststarthook/scheduling/bootstrap-system-priority-classes ok
# [+]poststarthook/priority-and-fairness-config-producer ok
# [+]poststarthook/bootstrap-controller ok
# [+]poststarthook/start-kubernetes-service-cidr-controller ok
# [+]poststarthook/aggregator-reload-proxy-client-cert ok
# [+]poststarthook/start-kube-aggregator-informers ok
# [+]poststarthook/apiservice-status-local-available-controller ok
# [+]poststarthook/apiservice-status-remote-available-controller ok
# [+]poststarthook/apiservice-registration-controller ok
# [+]poststarthook/apiservice-discovery-controller ok
# [+]poststarthook/kube-apiserver-autoregistration ok
# [+]autoregister-completion ok
# [+]poststarthook/apiservice-openapi-controller ok
# [+]poststarthook/apiservice-openapiv3-controller ok
# [+]shutdown ok
# readyz check passed

kubectl cluster-info
# Kubernetes control plane is running at https://127.0.0.1:6443

# get lease
kubectl -n kube-system get lease
# NAME                                   HOLDER                                                                      AGE
# apiserver-ivtlveyukuyrha5ia44unn7io4   apiserver-ivtlveyukuyrha5ia44unn7io4_dd022c6a-3c0c-486c-9601-5ea07599f05f   7m56s
# kube-controller-manager                controlplane_8cd40c99-2c7d-437f-9252-28f342842551                           4m21s
# kube-scheduler                         controlplane_658947a0-c1b6-49c9-ad75-2d15b38166c2                           114s
```

---

## Confirm encryption at rest

```sh
# sample secret to test
kubectl create secret generic sample-test --from-literal=key=value
# secret/sample-test created

# get from etcd
sudo etcdctl get /registry/secrets/default/sample-test --hex \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/ca.pem \
  --cert=/etc/kubernetes/pki/etcd-server.pem \
  --key=/etc/kubernetes/pki/etcd-server-key.pem | head -5
# \x2f\x72\x65\x67\x69\x73\x74\x72\x79\x2f\x73\x65\x63\x72\x65\x74\x73\x2f\x64\x65\x66\x61\x75\x6c\x74\x2f\x73\x61\x6d\x70\x6c\x65\x2d\x74\x65\x73\x74
# \x6b\x38\x73\x3a\x65\x6e\x63\x3a\x61\x65\x73\x63\x62\x63\x3a\x76\x31\x3a\x6b\x65\x79\x31\x3a\x3f\xd9\x0f\xb0\x38\x25\x81\xca\x8d\xe6\x31\x73\x57\x0f\x23\x8c\x2a\x74\xa7\x2c\xef\xfd\x89\x09\x7e\xf3\x3f\x55\x52\x7b\xad\x39\xe5\xa5\x8d\x73\x7d\xb4\x2d\x59\x04\x66\x0b\xdd\x2a\x7c\x70\xac\x71\x9e\x38\x8b\xaf\x07\x5e\x46\xd7\x65\x8f\x87\xe1\xd0\x10\xdd\x75\x7d\x3c\x59\xda\xe0\x04\xa5\xa1\x35\x7e\xc4\xc3\x6a\xa6\x6b\x00\xfb\x41\x8c\x58\x61\xd3\x80\xbb\x44\xab\xcc\xc3\xa4\x69\x76\xca\x40\x2e\xfc\x91\xdc\x0b\x16\x0a\x2f\x5f\xf6\xbd\x55\xcc\xe9\x1e\x1b\xc5\x06\x2a\xf8\xb7\x85\xd7\xb6\xb3\x84\x27\x21\x07\x6b\xe5\x27\x6a\xcf\x5a\x8b\x5e\xdb\x30\xd9\x8b\x08\xdc\x7a\x33\xe4\x39\x38\x05\xc6\x95\x01\x84\x9b\xb7\x7d\xec\xab\x3a\x40\x8e\x96\x42\x04\xcc\x23\xd5\x52\x03\x2d\xae\x7b\x21\x49\x0c\x64\xf2\x9f\x1a\xad\x44\x5b\xa0\xe2\xcb\x81\x54\x88\xe8\x63\x45\x1c\xdb\x84\x16\xbe\xec\x9f\xa2\x6d\xed\x14\x8b\x71\x2e\x43\xe8\xb8\xd2\x60\x72\xf1\x76\xc9\xb3\x1a\x64\xc0\xba\xf5\x8e\x1e\x02\xa1\xcb\x20\x6f\x73\x26\x86\xc7\xeb\x13\xb2\x13\x39\x27\x62\x7e\x88\xb3\x71\xc5\x6a\x12\xda\xab\xf8\x94\x3c\x31\x1a\xb9\xed\x6f\xc1\xbb\xa0

kubectl delete secret sample-test
# secret "sample-test" deleted from default namespac
```

---

### RBAC for apiserver -> kubelet

The apiserver needs explicit permission to reach kubelet endpoints, or
`kubectl logs` and `kubectl exec` fail with 403.

```sh
cat <<'EOF' | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:kube-apiserver-to-kubelet
rules:
  - apiGroups: [""]
    resources:
      - nodes/proxy
      - nodes/stats
      - nodes/log
      - nodes/spec
      - nodes/metrics
    verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:kube-apiserver
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:kube-apiserver-to-kubelet
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: kube-apiserver-kubelet-client
EOF
# clusterrole.rbac.authorization.k8s.io/system:kube-apiserver-to-kubelet created
# clusterrolebinding.rbac.authorization.k8s.io/system:kube-apiserver created
```

The `name` here must match the `CN` of `apiserver-kubelet-client` exactly.

---

## Install `kubelet` and `kube-proxy`

```sh
export K8S_VERSION=v1.35.8

cd /tmp

# ##############################
# Install kubelet
# ##############################
curl -L -o "kubelet" "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kubelet"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 56.2M  100 56.2M    0     0  13.4M      0  0:00:04  0:00:04 --:--:-- 13.7M

sudo install -m 755 "kubelet" /usr/local/bin/
# 'kubelet' -> '/usr/local/bin/kubelet'

# ##############################
# Install kube-proxy
# ##############################
curl -L -o "kube-proxy" "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kube-proxy"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 41.8M  100 41.8M    0     0  10.0M      0  0:00:04  0:00:04 --:--:-- 10.5M

sudo install -m 755 "kube-proxy" /usr/local/bin/
# 'kube-proxy' -> '/usr/local/bin/kube-proxy'

# ##############################
# kubelet config
# ##############################
sudo install -v -m 644 ~/pki/controlplane.crt /var/lib/kubelet/controlplane.pem
# '/home/ubuntuadmin/pki/controlplane.crt' -> '/var/lib/kubelet/controlplane.pem'
sudo install -v -m 600 ~/pki/controlplane.key /var/lib/kubelet/controlplane-key.pem
# '/home/ubuntuadmin/pki/controlplane.key' -> '/var/lib/kubelet/controlplane-key.pem'
sudo install -v -m 644 ~/pki/ca.crt /var/lib/kubernetes/ca.pem
# '/home/ubuntuadmin/pki/ca.crt' -> '/var/lib/kubernetes/ca.pem'

# ##############################
# config file: kubelet
# ##############################
cat <<'EOF' | sudo tee /var/lib/kubelet/kubelet-config.yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
  x509:
    clientCAFile: /var/lib/kubernetes/ca.pem
authorization:
  mode: Webhook
clusterDomain: cluster.local
clusterDNS:
  - 10.96.0.10
cgroupDriver: systemd
runtimeRequestTimeout: "15m"
tlsCertFile: /var/lib/kubelet/controlplane.pem
tlsPrivateKeyFile: /var/lib/kubelet/controlplane-key.pem
readOnlyPort: 0
protectKernelDefaults: true
seccompDefault: true
EOF

# NOTE: protectKernelDefaults: true makes the kubelet REFUSE TO START unless
# the six sysctls in /etc/sysctl.d/90-kubelet.conf (Preparation) are already
# set -- it will not retune the host itself. Symptom if missing:
#   Failed to start ContainerManager: invalid kernel flag: vm/overcommit_memory
# readOnlyPort: 0 closes the unauthenticated :10255 metrics port, and
# authorization.mode: Webhook makes every kubelet API call go through the
# apiserver's RBAC -- both are named CKS hardening items.

# ##############################
# systemd unit: kubelet
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet
After=containerd.service
Requires=containerd.service

[Service]
ExecStart=/usr/local/bin/kubelet \
  --config=/var/lib/kubelet/kubelet-config.yaml \
  --kubeconfig=/var/lib/kubelet/kubeconfig \
  --container-runtime-endpoint=unix:///run/containerd/containerd.sock \
  --register-node=true \
  --node-ip=192.168.10.180 \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF


# ##############################
# config file: kube-proxy
# ##############################
cat <<'EOF' | sudo tee /var/lib/kube-proxy/kube-proxy-config.yaml
kind: KubeProxyConfiguration
apiVersion: kubeproxy.config.k8s.io/v1alpha1
clientConnection:
  kubeconfig: /var/lib/kube-proxy/kubeconfig
mode: iptables
clusterCIDR: 10.244.0.0/16
hostnameOverride: controlplane
EOF

# ##############################
# systemd unit: kube-proxy
# ##############################
cat <<'EOF' | sudo tee /etc/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube Proxy
After=kube-apiserver.service

[Service]
ExecStart=/usr/local/bin/kube-proxy \
  --config=/var/lib/kube-proxy/kube-proxy-config.yaml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# ##############################
# start service
# ##############################
sudo systemctl daemon-reload
sudo systemctl enable --now kubelet kube-proxy
# Created symlink /etc/systemd/system/multi-user.target.wants/kubelet.service → /etc/systemd/system/kubelet.service.
# Created symlink /etc/systemd/system/multi-user.target.wants/kube-proxy.service → /etc/systemd/system/kube-proxy.service.

sudo systemctl status kubelet --no-pager
# ● kubelet.service - Kubernetes Kubelet
#      Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 18:08:32 EDT; 22ms ago
#    Main PID: 4158 (kubelet)
#       Tasks: 6 (limit: 7689)
#      Memory: 5.0M (peak: 5.0M)
#         CPU: 15ms
#      CGroup: /system.slice/kubelet.service
#              └─4158 /usr/local/bin/kubelet --config=/var/lib/kubelet/kubelet-config.yaml --kubeconfig=/var/lib/kubelet/kubeconfig --…

# Sep 02 18:08:32 controlplane systemd[1]: Started kubelet.service - Kubernetes Kubelet.

# ##############################
# confirm registration
# ##############################
# the kubelet stays "active (running)" even when registration fails -- it
# retries silently -- so systemctl status alone proves nothing. Read the log.
sudo journalctl -u kubelet -n 20 --no-pager --output=cat
# "Successfully registered node" node="controlplane"

kubectl get nodes
# NAME           STATUS     ROLES    AGE   VERSION
# controlplane   NotReady   <none>   15s   v1.35.8

sudo systemctl status kube-proxy --no-pager
# ● kube-proxy.service - Kubernetes Kube Proxy
#      Loaded: loaded (/etc/systemd/system/kube-proxy.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2026-09-02 18:08:32 EDT; 17min ago
#    Main PID: 4157 (kube-proxy)
#       Tasks: 6 (limit: 7689)
#      Memory: 11.6M (peak: 14.3M)
#         CPU: 2.824s
#      CGroup: /system.slice/kube-proxy.service
#              └─4157 /usr/local/bin/kube-proxy --config=/var/lib/kube-proxy/kube-proxy-config.yaml

# Sep 02 18:19:05 controlplane kube-proxy[4157]: E0902 18:19:05.091011    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:19:53 controlplane kube-proxy[4157]: E0902 18:19:53.631932    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:20:47 controlplane kube-proxy[4157]: E0902 18:20:47.185752    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:21:26 controlplane kube-proxy[4157]: E0902 18:21:26.932890    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:22:06 controlplane kube-proxy[4157]: E0902 18:22:06.464710    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:22:57 controlplane kube-proxy[4157]: E0902 18:22:57.770523    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:23:46 controlplane kube-proxy[4157]: E0902 18:23:46.196506    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:24:18 controlplane kube-proxy[4157]: E0902 18:24:18.379399    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:25:12 controlplane kube-proxy[4157]: E0902 18:25:12.179101    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Sep 02 18:26:08 controlplane kube-proxy[4157]: E0902 18:26:08.089221    4157 reflector.go:204] "Failed to watch" err="failed to list…
# Hint: Some lines were ellipsized, use -l to show in full.
```

---

## Phase 7: CNI

See also: [Cilium](../../cilium.md).

```sh
# get stable version
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)

# download
curl -L --fail -o /tmp/cilium.tar.gz \
  "https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-amd64.tar.gz"

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
#   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
# 100 72.6M  100 72.6M    0     0  29.7M      0  0:00:02  0:00:02 --:--:-- 34.0M

sudo tar xzvfC /tmp/cilium.tar.gz /usr/local/bin
# cilium

cilium install \
  --set ipam.mode=kubernetes \
  --set k8sServiceHost=192.168.10.180 \
  --set k8sServicePort=6443

# ℹ️  Using Cilium version 1.20.1
# 🔮 Auto-detected cluster name: kubernetes

cilium status --wait
#     /¯¯\
#  /¯¯\__/¯¯\    Cilium:             OK
#  \__/¯¯\__/    Operator:           OK
#  /¯¯\__/¯¯\    Envoy DaemonSet:    OK
#  \__/¯¯\__/    Hubble Relay:       disabled
#     \__/       ClusterMesh:        disabled

# DaemonSet              cilium                   Desired: 1, Ready: 1/1, Available: 1/1
# DaemonSet              cilium-envoy             Desired: 1, Ready: 1/1, Available: 1/1
# Deployment             cilium-operator          Desired: 1, Ready: 1/1, Available: 1/1
# Containers:            cilium                   Running: 1
#                        cilium-envoy             Running: 1
#                        cilium-operator          Running: 1
#                        clustermesh-apiserver
#                        hubble-relay
# Cluster Pods:          2/2 managed by Cilium
# Helm chart version:    1.20.1
# Image versions         cilium             quay.io/cilium/cilium:v1.20.1@sha256:ae9ea21f7427fe24bc6ea7247eb552157a1b0a431744045d3f641545ca71d11b: 1
#                        cilium-envoy       quay.io/cilium/cilium-envoy:v1.37.5-1786810558-766ccfb37260a43e9d228837aa84ce3faf9f64e7@sha256:75b8094c7127736a2ffd2dce3945e0931cb6df21b0372ff661940eca26730b91: 1
#                        cilium-operator    quay.io/cilium/operator-generic:v1.20.1@sha256:6c3885fc7b629099fdbe2a5c87869c86feb825fa18fae299eac0f61918d16ecf: 1

# confirm by node
kubectl get nodes
# NAME           STATUS   ROLES    AGE     VERSION
# controlplane   Ready    <none>   4m48s   v1.35.8

# confirm dataplane
kubectl -n kube-system exec ds/cilium -- cilium-dbg status \
  | grep -iE 'kubeproxyreplacement|masquerad|routing'

# KubeProxyReplacement:    True   [ens33      192.168.10.180 10.0.0.167 2607:fea8:2adc:8500:82fc:e402:83ea:c9f6 2607:fea8:2adc:8500:20c:29ff:fecd:d439 fe80::20c:29ff:fecd:d439 (Direct Routing)]
# Routing:                 Network: Tunnel [vxlan]   Host: Legacy
# Masquerading:            IPTables [IPv4: Enabled, IPv6: Disabled]

# pod egress
kubectl run nettest --image=busybox:1.36 --rm -it --restart=Never -- \
  nslookup kubernetes.io 8.8.8.8
```

If `nslookup` times out, pod egress is broken -- fix it here, not in Phase 8.
Locate the drop with:

```sh
kubectl -n kube-system exec ds/cilium -- cilium-dbg monitor --type drop
```

---

## Phase 8: CoreDNS

The upstream base manifest ships with `__PILLAR__` placeholders, so render it
before applying:

```sh
# download -- pin to the release branch matching K8S_VERSION, not master
curl -sL -o /tmp/coredns.yaml \
  https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.35/cluster/addons/dns/coredns/coredns.yaml.base

sed -i \
  -e 's/__DNS__DOMAIN__/cluster.local/g' \
  -e 's/__DNS__SERVER__/10.96.0.10/g' \
  -e 's/__DNS__MEMORY__LIMIT__/170Mi/g' \
  -e 's/__PILLAR__DNS__DOMAIN__/cluster.local/g' \
  -e 's/__PILLAR__DNS__SERVER__/10.96.0.10/g' \
  -e 's/__PILLAR__DNS__MEMORY__LIMIT__/170Mi/g' \
  -e 's/__PILLAR__CLUSTER__DNS__/10.96.0.10/g' \
  /tmp/coredns.yaml

# REQUIRED on Ubuntu: the manifest ships "forward . /etc/resolv.conf", which
# on Ubuntu is the systemd-resolved stub (127.0.0.53) -- CoreDNS then forwards
# to itself and dies with "plugin/loop: Loop ... detected for zone ."
sed -i 's|forward . /etc/resolv.conf|forward . 8.8.8.8 1.1.1.1|' /tmp/coredns.yaml

grep -n 'forward' /tmp/coredns.yaml
#        forward . 8.8.8.8 1.1.1.1 {

kubectl apply -f /tmp/coredns.yaml
# serviceaccount/coredns created
# clusterrole.rbac.authorization.k8s.io/system:coredns created
# clusterrolebinding.rbac.authorization.k8s.io/system:coredns created
# configmap/coredns created
# deployment.apps/coredns created
# service/kube-dns created

kubectl -n kube-system get pods -l k8s-app=kube-dns
# NAME                       READY   STATUS    RESTARTS   AGE
# coredns-6f8d6ffb66-62kc2   1/1     Running   0          16s

# confirm the forwarder in the RUNNING ConfigMap, not just the local file
kubectl -n kube-system get cm coredns -o jsonpath='{.data.Corefile}' | grep forward
#        forward . 8.8.8.8 1.1.1.1 {
```

The control plane is tainted by default only under `kubeadm`; here it is not,
so CoreDNS schedules fine on a single node.

### If CoreDNS is in `CrashLoopBackOff`

```sh
kubectl -n kube-system logs -l k8s-app=kube-dns
# note: "kubectl logs pods -l ..." is invalid -- pass EITHER a pod name OR -l,
# and -w is not a flag for logs (use -f to follow)
```

| Log line                                              | Cause                                                                                    |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `[FATAL] plugin/loop: Loop ... detected for zone "."` | `forward . /etc/resolv.conf` resolving to the `127.0.0.53` stub -- apply the `sed` above |
| `SERVFAIL` on external names, pod otherwise `Running` | usually **not** CoreDNS -- check pod egress/masquerading in Phase 7 first                |
| `Listen: listen tcp :53: bind: permission denied`     | missing `NET_BIND_SERVICE` capability in the manifest                                    |
| pod `Pending`                                         | CNI not ready -- finish Phase 7 first                                                    |

Do **not** "fix" the loop by deleting the `loop` plugin from the Corefile, a
common suggestion online. The plugin is a guard, not the fault: removing it
turns an immediate crash into an unbounded query amplification loop between
CoreDNS and itself.

An alternative to hardcoding upstream IPs is `forward . /run/systemd/resolve/resolv.conf`
-- the _real_ resolver list rather than the stub, which is what `kubeadm` does.
It requires mounting that path into the pod, so the explicit addresses above
are simpler for a lab. Either way the addresses should match the `nameservers`
set in netplan during Preparation.

---

## Verification

```sh
# ##############################
# confirm
# ##############################
kubectl get nodes -o wide
# NAME           STATUS   ROLES    AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
# controlplane   Ready    <none>   10m   v1.35.8   192.168.10.180   <none>        Ubuntu 24.04.4 LTS   7.0.0-30-generic   containerd://2.2.1

kubectl get pods -A
# NAMESPACE     NAME                               READY   STATUS    RESTARTS   AGE
# kube-system   cilium-9jstq                       1/1     Running   0          7m13s
# kube-system   cilium-envoy-cmh7d                 1/1     Running   0          7m13s
# kube-system   cilium-operator-66df494884-htr2n   1/1     Running   0          7m13s
# kube-system   coredns-6f8d6ffb66-62kc2           1/1     Running   0          59s

kubectl get --raw='/readyz?verbose'

# ##############################
# DNS check
# ##############################
# run test pod
kubectl run dnsutils --image=registry.k8s.io/e2e-test-images/agnhost:2.39
# pod/dnsutils created

kubectl get pod dnsutils
# NAME       READY   STATUS    RESTARTS   AGE
# dnsutils   1/1     Running   0          10s

# test: service DNS
kubectl exec -it dnsutils -- nslookup kubernetes.default
# Server:         10.96.0.10
# Address:        10.96.0.10#53
#
# Name:   kubernetes.default.svc.cluster.local
# Address: 10.96.0.1

# test: fully qualified
kubectl exec -it dnsutils -- nslookup kubernetes.default.svc.cluster.local
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# Name:   kubernetes.default.svc.cluster.local
# Address: 10.96.0.1

# test: (external) resolution
kubectl exec -it dnsutils -- nslookup kubernetes.io
# Server:         10.96.0.10
# Address:        10.96.0.10#53
#
# Non-authoritative answer:
# Name:   kubernetes.io
# Address: 147.75.40.148

# FAILURE MODE -- if you get this instead:
#   ** server can't find kubernetes.io: SERVFAIL
#   command terminated with exit code 1
# there are TWO possible causes and they live in different phases. Check the
# CoreDNS config FIRST, because it is one command:
#
#   kubectl -n kube-system get cm coredns -o jsonpath='{.data.Corefile}' | grep forward
#
# a) shows "forward . /etc/resolv.conf"  -> Phase 8: CoreDNS is forwarding to
#    Ubuntu's 127.0.0.53 stub. Re-apply the rendered manifest.
# b) shows "forward . 8.8.8.8 1.1.1.1"   -> CoreDNS is FINE. The fault is pod
#    egress, i.e. Phase 7. Prove it by bypassing CoreDNS entirely:
#      kubectl run nettest --image=busybox:1.36 --rm -it --restart=Never -- #        nslookup kubernetes.io 8.8.8.8
#    A timeout there means masquerading is off -- see Phase 7. Note the node
#    itself resolving fine (dig +short @8.8.8.8 kubernetes.io) proves nothing;
#    the node is not masqueraded, pods are.

# confirm config file
kubectl exec -it dnsutils -- cat /etc/resolv.conf
# search default.svc.cluster.local svc.cluster.local cluster.local
# nameserver 10.96.0.10
# options ndots:5

kubectl delete pod dnsutils
# pod "dnsutils" deleted from default namespace

# ##############################
# Confirm Secret encryption at rest
# ##############################
kubectl create secret generic test-secret --from-literal=password=supersecret
# secret/test-secret created

sudo etcdctl get /registry/secrets/default/test-secret \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/ca.pem \
  --cert=/etc/kubernetes/pki/etcd-server.pem \
  --key=/etc/kubernetes/pki/etcd-server-key.pem | hexdump -C | head

# 00000000  2f 72 65 67 69 73 74 72  79 2f 73 65 63 72 65 74  |/registry/secret|
# 00000010  73 2f 64 65 66 61 75 6c  74 2f 74 65 73 74 2d 73  |s/default/test-s|
# 00000020  65 63 72 65 74 0a 6b 38  73 3a 65 6e 63 3a 61 65  |ecret.k8s:enc:ae|
# 00000030  73 63 62 63 3a 76 31 3a  6b 65 79 31 3a 00 49 42  |scbc:v1:key1:.IB|
# 00000040  d6 e4 9f 6e 1e 17 5f 38  e9 d7 ad f5 67 dc d3 f9  |...n.._8....g...|
# 00000050  c4 ab c4 1d fd c4 da 75  5d 9b dd 4c 2d 16 db 11  |.......u]..L-...|
# 00000060  83 92 3d 30 ea ba 19 a6  00 c1 f0 57 8a 30 c3 fb  |..=0.......W.0..|
# 00000070  9e e3 bf c4 79 c2 bb 06  b8 0c a0 8b 03 a6 3e 2d  |....y.........>-|
# 00000080  8a fa b4 7f ad 6c 4f 2c  66 08 a0 bb 1a 50 20 17  |.....lO,f....P .|
# 00000090  9a 82 7d bd a5 ce cf 77  7c 7f 2d 03 3a 9d 8d 2b  |..}....w|.-.:..+|


# ##############################
# Confirm the apiserver -> kubelet path (RBAC + kubelet authz)
# ##############################
# exercises the ClusterRoleBinding created earlier; 403 here means the binding
# is missing or its User name does not match the client cert CN
kubectl run pathtest --image=registry.k8s.io/e2e-test-images/agnhost:2.39
kubectl wait --for=condition=Ready pod/pathtest --timeout=60s

kubectl logs pathtest >/dev/null && echo "logs OK"
# logs OK
kubectl exec pathtest -- echo works
# works
kubectl delete pod pathtest

# ##############################
# Confirm the kubelet read-only port is closed
# ##############################
# readOnlyPort: 0 -- this port serves node and pod metadata with NO auth
curl -s --max-time 5 http://192.168.10.180:10255/pods; echo "exit=$?"
# exit=7   (connection refused -- correct)

# the authenticated port answers, but rejects anonymous callers
curl -sk --max-time 5 https://192.168.10.180:10250/pods | head -c 200
# Unauthorized

# ##############################
# Confirm audit logging is actually being written
# ##############################
sudo test -s /var/log/kubernetes/audit.log && echo "audit log has content"
# audit log has content

# Secrets are logged at RequestResponse level per the policy
sudo grep -c '"resource":"secrets"' /var/log/kubernetes/audit.log
# (non-zero -- the test-secret above produced entries)

# ##############################
# Confirm NodeRestriction admission is loaded
# ##############################
sudo journalctl -u kube-apiserver | grep -i "NodeRestriction" | head -2

# ##############################
# Confirm pod networking end to end (not just DNS)
# ##############################
kubectl create deployment nettest --image=nginx:alpine --replicas=2
kubectl wait --for=condition=Available deployment/nettest --timeout=120s
kubectl expose deployment nettest --port=80

# pod -> service ClusterIP
kubectl run curltest --image=curlimages/curl:8.10.1 --restart=Never -- \
  sh -c 'curl -s -o /dev/null -w "%{http_code}" http://nettest'
sleep 10
kubectl logs curltest
# 200

kubectl delete pod curltest
kubectl delete service nettest
kubectl delete deployment nettest

# ##############################
# Confirm anonymous access is closed:
# ##############################
curl -k https://192.168.10.180:6443/api/v1/nodes
# {
#   "kind": "Status",
#   "apiVersion": "v1",
#   "metadata": {},
#   "status": "Failure",
#   "message": "Unauthorized",
#   "reason": "Unauthorized",
#   "code": 401
# }
```

### Control plane completion checklist

The master node is done only when every row passes. A `Ready` node and running
pods are necessary but not sufficient -- several of the hardening settings fail
silently.

| #   | Check                                    | Pass condition                                       |
| --- | ---------------------------------------- | ---------------------------------------------------- |
| 1   | `kubectl get nodes`                      | `controlplane   Ready`                               |
| 2   | `kubectl get pods -A`                    | all cilium + coredns pods `1/1 Running`              |
| 3   | `kubectl get --raw='/readyz?verbose'`    | `readyz check passed`                                |
| 4   | `kubectl -n kube-system get lease`       | controller-manager and scheduler both held           |
| 5   | `nslookup kubernetes.default` in a pod   | resolves to `10.96.0.1`                              |
| 6   | `nslookup kubernetes.io` in a pod        | resolves -- **SERVFAIL means Phase 8 is unfinished** |
| 7   | pod -> Service ClusterIP over HTTP       | `200`                                                |
| 8   | Secret in etcd                           | starts `k8s:enc:aescbc:v1:key1`, no plaintext        |
| 9   | `curl -k https://<ip>:6443/api/v1/nodes` | `401 Unauthorized`                                   |
| 10  | `curl http://<ip>:10255/pods`            | connection refused                                   |
| 11  | `kubectl logs` / `kubectl exec` on a pod | succeed (not 403)                                    |
| 12  | `/var/log/kubernetes/audit.log`          | non-empty, contains `"resource":"secrets"`           |

Rows 1-4 prove the cluster runs. Rows 5-7 prove networking. Rows 8-12 prove the
CKS-relevant hardening is actually in effect rather than merely configured --
that distinction is the point of this build.

---
