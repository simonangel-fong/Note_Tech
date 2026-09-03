# CKS - Master node: Kubernetes Controller Manager

[Back](../../index.md)

- [CKS - Master node: Kubernetes Controller Manager](#cks---master-node-kubernetes-controller-manager)
  - [Kubernetes Controller Manager - Overview](#kubernetes-controller-manager---overview)
    - [Required files](#required-files)
  - [PKI](#pki)
  - [Configure `kube-controller-manager.conf`](#configure-kube-controller-managerconf)
  - [Install `kube-controller-manager`](#install-kube-controller-manager)

---

## Kubernetes Controller Manager - Overview

### Required files

Files required by the `kube-controller-manager` systemd unit:

| File                           | Type           | Purpose                                              |
| ------------------------------ | -------------- | ---------------------------------------------------- |
| `kube-controller-manager.conf` | Kubeconfig     | Connects the controller manager to the API server    |
| `ca.crt`                       | CA certificate | Signs cluster certificates and publishes the root CA |
| `ca.key`                       | CA private key | Signs cluster certificates                           |
| `front-proxy-ca.crt`           | CA certificate | Verifies aggregation-layer clients                   |
| `sa.key`                       | Private key    | Signs service-account tokens                         |

---

## PKI

```sh
cd ~/pki

# ##############################
# Create client cert: controller manager
# ##############################
# create client certificates: kube-controller-manager
gen_client kube-controller-manager "/CN=system:kube-controller-manager/O=system:kube-controller-manager"
# Certificate request self-signature ok
# subject=CN = system:kube-controller-manager, O = system:kube-controller-manager
# removed 'kube-controller-manager.csr'

ls -l kube-controller-manager.*
# -rw------- 1 ubuntuadmin ubuntuadmin 4252 Sep  3 15:29 kube-controller-manager.conf
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1277 Sep  3 16:42 kube-controller-manager.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1708 Sep  3 16:42 kube-controller-manager.key

# confirm
openssl x509 -in "kube-controller-manager.crt" -noout -subject
# subject=CN = system:kube-controller-manager, O = system:kube-controller-manager

# ##############################
# Install
# ##############################
sudo install -v -m 644 kube-controller-manager.crt /etc/kubernetes/pki/kube-controller-manager.crt
# 'kube-controller-manager.crt' -> '/etc/kubernetes/pki/kube-controller-manager.crt'

sudo install -v -m 600 kube-controller-manager.key /etc/kubernetes/pki/kube-controller-manager.key
# 'kube-controller-manager.key' -> '/etc/kubernetes/pki/kube-controller-manager.key'

ls -l /etc/kubernetes/pki/kube-controller-manager.crt /etc/kubernetes/pki/kube-controller-manager.key
# -rw-r--r-- 1 root root ... /etc/kubernetes/pki/kube-controller-manager.crt
# -rw------- 1 root root ... /etc/kubernetes/pki/kube-controller-manager.key
```

---

## Configure `kube-controller-manager.conf`

The `kube-controller-manager.conf` defines _where_ the API server is, _who_ the client is, and _which CA_ to trust.

```sh
cd ~/pki

# ##############################
# Configure kubeconfig: kube-controller-manager
# ##############################

# set cluster
kubectl config set-cluster kubernetes \
  --server=https://127.0.0.1:6443 \
  --certificate-authority=ca.crt \
  --embed-certs=true \
  --kubeconfig=kube-controller-manager.conf
# Cluster "kubernetes" set.

kubectl config set-credentials system:kube-controller-manager \
  --client-certificate=kube-controller-manager.crt \
  --client-key=kube-controller-manager.key \
  --embed-certs=true \
  --kubeconfig=kube-controller-manager.conf
# User "system:kube-controller-manager" set.

kubectl config set-context default \
  --cluster=kubernetes \
  --user=system:kube-controller-manager \
  --kubeconfig=kube-controller-manager.conf

# Context "default" modified.

kubectl config use-context default \
  --kubeconfig=kube-controller-manager.conf

# Switched to context "default".

# ##############################
# Install kubeconfig: kube-controller-manager
# ##############################
sudo install -v -m 600 kube-controller-manager.conf \
  /etc/kubernetes/kube-controller-manager.conf

# 'kube-controller-manager.conf' -> '/etc/kubernetes/kube-controller-manager.conf'
```

## Install `kube-controller-manager`

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
  --allocate-node-cidrs=true \
  --authentication-kubeconfig=/etc/kubernetes/kube-controller-manager.conf \
  --authorization-kubeconfig=/etc/kubernetes/kube-controller-manager.conf \
  --bind-address=127.0.0.1 \
  --cluster-name=kubernetes \
  --cluster-cidr=10.244.0.0/16 \
  --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt \
  --cluster-signing-key-file=/etc/kubernetes/pki/ca.key \
  --kubeconfig=/etc/kubernetes/kube-controller-manager.conf \
  --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt \
  --leader-elect=true \
  --root-ca-file=/etc/kubernetes/pki/ca.crt \
  --service-account-private-key-file=/etc/kubernetes/pki/sa.key \
  --service-cluster-ip-range=10.96.0.0/12 \
  --use-service-account-credentials=true \
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
sudo systemctl status kube-controller-manager --no-pager --full
# ● kube-controller-manager.service - Kubernetes Controller Manager
#      Loaded: loaded (/etc/systemd/system/kube-controller-manager.service; enabled; preset: enabled)
#      Active: active (running) since Thu 2026-09-03 15:18:21 EDT; 15min ago
#        Docs: https://kubernetes.io/docs/concepts/overview/components/
#    Main PID: 3542 (kube-controller)
#       Tasks: 6 (limit: 3179)
#      Memory: 17.7M (peak: 18.0M)
#         CPU: 3.654s
#      CGroup: /system.slice/kube-controller-manager.service
#              └─3542 /usr/local/bin/kube-controller-manager --allocate-node-cidrs=true --authentication-kubeconfig=…

# Sep 03 15:33:10 controlplane kube-controller-manager[3542]: E0903 15:33:10.767925    3542 reflector.go:204] "…gMap"
# Sep 03 15:33:11 controlplane kube-controller-manager[3542]: E0903 15:33:11.489420    3542 leaderelection.go:4…ager"
# Sep 03 15:33:14 controlplane kube-controller-manager[3542]: E0903 15:33:14.062028    3542 leaderelection.go:4…ager"
# Sep 03 15:33:16 controlplane kube-controller-manager[3542]: E0903 15:33:16.944537    3542 leaderelection.go:4…ager"
# Sep 03 15:33:20 controlplane kube-controller-manager[3542]: E0903 15:33:20.626492    3542 leaderelection.go:4…ager"
# Sep 03 15:33:24 controlplane kube-controller-manager[3542]: E0903 15:33:24.404425    3542 leaderelection.go:4…ager"
# Sep 03 15:33:28 controlplane kube-controller-manager[3542]: E0903 15:33:28.106557    3542 leaderelection.go:4…ager"
# Sep 03 15:33:32 controlplane kube-controller-manager[3542]: E0903 15:33:32.216710    3542 leaderelection.go:4…ager"
# Sep 03 15:33:36 controlplane kube-controller-manager[3542]: E0903 15:33:36.571366    3542 leaderelection.go:4…ager"
# Sep 03 15:33:39 controlplane kube-controller-manager[3542]: E0903 15:33:39.093775    3542 leaderelection.go:4…ager"
# Hint: Some lines were ellipsized, use -l to show in full.
```

---
