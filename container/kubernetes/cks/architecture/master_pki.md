# CKS - Master node: Certificate & PKI

[Back](../../index.md)

- [CKS - Master node: Certificate \& PKI](#cks---master-node-certificate--pki)
  - [Configure PKI / Certificate Authority](#configure-pki--certificate-authority)
    - [Root CA](#root-ca)
    - [Identity table](#identity-table)
      - [Generate client certificates](#generate-client-certificates)
      - [Front-proxy certificates](#front-proxy-certificates)
      - [Kubelet certificate (control plane node)](#kubelet-certificate-control-plane-node)
      - [API server serving certificate](#api-server-serving-certificate)
      - [Install certificates](#install-certificates)
    - [Configure Kubeconfig](#configure-kubeconfig)

---

## Configure PKI / Certificate Authority

### Root CA

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

ls ca.*
# ca.crt  ca.key
```

### Identity table

| Cert                       | CN (username)                    | O (group)                        | Purpose                     |
| -------------------------- | -------------------------------- | -------------------------------- | --------------------------- |
| `admin`                    | `admin`                          | `system:masters`                 | `kubectl` identity          |
| `kube-controller-manager`  | `system:kube-controller-manager` | `system:kube-controller-manager` | controller loops            |
| `kube-scheduler`           | `system:kube-scheduler`          | `system:kube-scheduler`          | scheduling                  |
| `kube-proxy`               | `system:kube-proxy`              | `system:node-proxier`            | Service rules               |
| `kubelet` (per node)       | `system:node:<hostname>`         | `system:nodes`                   | Node authorizer             |
| `kube-apiserver`           | `kube-apiserver`                 | `Kubernetes`                     | serving cert (SANs matter)  |
| `apiserver-kubelet-client` | `kube-apiserver-kubelet-client`  | `system:masters`                 | apiserver -> kubelet        |
| `service-account`          | --                               | --                               | keypair, signs SA tokens    |
| `front-proxy-ca`           | `front-proxy-ca`                 | --                               | separate CA for aggregation |
| `front-proxy-client`       | `front-proxy-client`             | --                               | apiserver -> extension API  |

- Group:
  - `system:masters`: a built-in, hard-coded Kubernetes group that grants full, unrestricted **super-user access** to the API server,
  - `system:nodes`: a built-in system group automatically assigned to **all** `Kubelets` (the node agents) for authentication and RBAC authorization.

#### Generate client certificates

- Client certs carry **no SANs**
  - identity is the subject alone.
  - `Subject Alternative Name (SAN)`:
    - extension in an SSL/TLS certificate that allows a single certificate to secure multiple identities,
    - use the SAN field as the authoritative check to verify a website's identity.

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

ls -l
# total 56
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1216 Sep  3 08:01 admin.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1708 Sep  3 08:01 admin.key
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1241 Sep  3 08:02 apiserver-etcd-client.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Sep  3 08:02 apiserver-etcd-client.key
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1249 Sep  3 08:02 apiserver-kubelet-client.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Sep  3 08:02 apiserver-kubelet-client.key
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1204 Sep  3 07:43 ca.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Sep  3 07:43 ca.key
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin   41 Sep  3 08:02 ca.srl
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin  122 Sep  3 08:01 client-ext.conf
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1273 Sep  3 08:02 kube-controller-manager.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1700 Sep  3 08:02 kube-controller-manager.key
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1241 Sep  3 08:02 kube-proxy.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Sep  3 08:02 kube-proxy.key

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

s
