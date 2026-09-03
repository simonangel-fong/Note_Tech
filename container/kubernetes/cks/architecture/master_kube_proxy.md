# CKS - Master node: `kube-proxy`

[Back](../../index.md)

- [CKS - Master node: `kube-proxy`](#cks---master-node-kube-proxy)
  - [kube-proxy - Overview](#kube-proxy---overview)
  - [Install `kube-proxy`](#install-kube-proxy)
  - [PKI - kube-proxy certificate](#pki---kube-proxy-certificate)
  - [Configure kubeconfig](#configure-kubeconfig)
  - [Configure `kube-proxy`](#configure-kube-proxy)
  - [Install CNI - `Calico`](#install-cni---calico)
  - [Test controlplane](#test-controlplane)
  - [CoreDNS](#coredns)

---

## kube-proxy - Overview

## Install `kube-proxy`

```sh
cd /tmp

export K8S_VERSION=v1.35.8

# ##############################
# Install kube-proxy
# ##############################
curl -L -o "kube-proxy" "https://dl.k8s.io/${K8S_VERSION}/bin/linux/amd64/kube-proxy"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100 41.8M  100 41.8M    0     0  10.0M      0  0:00:04  0:00:04 --:--:-- 10.5M

sudo install -m 755 "kube-proxy" /usr/local/bin/
# 'kube-proxy' -> '/usr/local/bin/kube-proxy'

kube-proxy --version
# Kubernetes v1.35.8

```

## PKI - kube-proxy certificate

```sh
cd ~/pki

# create client certificates: kube-proxy
gen_client kube-proxy               "/CN=system:kube-proxy/O=system:node-proxier"
# Certificate request self-signature ok
# subject=CN = system:kube-proxy, O = system:node-proxier
# removed 'kube-proxy.csr'

# confirm
ls -l kube-proxy.*
# -rw-rw-r-- 1 ubuntuadmin ubuntuadmin 1241 Sep  3 17:42 kube-proxy.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Sep  3 17:42 kube-proxy.key

# confirm subject
openssl x509 -in "kube-proxy.crt" -noout -subject
# subject=CN = system:kube-proxy, O = system:node-proxier
```

---

## Configure kubeconfig

```sh
cd ~/pki

export KUBERNETES_PUBLIC_ADDRESS=192.168.10.180

# ##############################
# Configure kubeconfig: proxy
# ##############################
# set cluster
kubectl config set-cluster kubernetes   \
    --server=https://${KUBERNETES_PUBLIC_ADDRESS}:6443  \
    --certificate-authority=ca.crt  \
    --embed-certs=true  \
    --kubeconfig=kube-proxy.config

# Cluster "kubernetes" set.

# set user
kubectl config set-credentials system:kube-proxy    \
    --client-key=kube-proxy.key     \
    --client-certificate=kube-proxy.crt     \
    --embed-certs=true  \
    --kubeconfig=kube-proxy.config

# User "system:kube-proxy" set.

# set context
kubectl config set-context default  \
    --cluster=kubernetes    \
    --user=system:kube-proxy    \
    --kubeconfig=kube-proxy.config

# Context "default" created.

kubectl config use-context default --kubeconfig=kube-proxy.config
# Switched to context "default".

# ##############################
# Install kubeconfigs: proxy
# ##############################
sudo mkdir -pv /var/lib/kube-proxy
# mkdir: created directory '/var/lib/kube-proxy'
sudo install -v -o root -g root -m 600 ~/pki/kube-proxy.config   /var/lib/kube-proxy/kube-proxy.config
# '/home/ubuntuadmin/pki/kube-proxy.config' -> '/var/lib/kube-proxy/kube-proxy.config'
```

---

## Configure `kube-proxy`

```sh
# ##############################
# config file: kube-proxy
# ##############################
cat <<'EOF' | sudo tee /var/lib/kube-proxy/kube-proxy-config.yaml
kind: KubeProxyConfiguration
apiVersion: kubeproxy.config.k8s.io/v1alpha1
clientConnection:
  kubeconfig: /var/lib/kube-proxy/kube-proxy.config
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
# Created symlink /etc/systemd/system/multi-user.target.wants/kube-proxy.service → /etc/systemd/system/kube-proxy.service.

sudo systemctl status kube-proxy --no-pager --full
# ● kube-proxy.service - Kubernetes Kube Proxy
#      Loaded: loaded (/etc/systemd/system/kube-proxy.service; enabled; preset: enabled)
#      Active: active (running) since Thu 2026-09-03 17:49:05 EDT; 22s ago
#    Main PID: 8303 (kube-proxy)
#       Tasks: 6 (limit: 3179)
#      Memory: 12.7M (peak: 14.7M)
#         CPU: 247ms
#      CGroup: /system.slice/kube-proxy.service
#              └─8303 /usr/local/bin/kube-proxy --config=/var/lib/kube-proxy/kube-proxy-config.yaml

# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.503019    8303 config.go:106] "Starting endpoint slice config controller"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.503022    8303 shared_informer.go:349] "Waiting for caches to sync" controller="endpoint slice config"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.503038    8303 config.go:403] "Starting serviceCIDR config controller"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.503041    8303 shared_informer.go:349] "Waiting for caches to sync" controller="serviceCIDR config"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.508267    8303 config.go:309] "Starting node config controller"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.508281    8303 shared_informer.go:349] "Waiting for caches to sync" controller="node config"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.508285    8303 shared_informer.go:356] "Caches are synced" controller="node config"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.603808    8303 shared_informer.go:356] "Caches are synced" controller="serviceCIDR config"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.603878    8303 shared_informer.go:356] "Caches are synced" controller="endpoint slice config"
# Sep 03 17:49:05 controlplane kube-proxy[8303]: I0903 17:49:05.603855    8303 shared_informer.go:356] "Caches are synced" controller="service config"
```

---

## Install CNI - `Calico`

```sh
# install crd
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.32.2/manifests/v1_crd_projectcalico_org.yaml

# install operator
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.32.2/manifests/tigera-operator.yaml

# get cluster ip cidr
kubectl cluster-info dump | grep -m 1 cluster-cidr
# "--cluster-cidr=10.244.0.0/16"

# Download the custom resources necessary to configure Calico.
curl -L -o /tmp/custom-resources.yaml https://raw.githubusercontent.com/projectcalico/calico/v3.32.2/manifests/custom-resources.yaml
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100  1046  100  1046    0     0   7860      0 --:--:-- --:--:-- --:--:--  7924

# update the manifest with the cluster cidr
vi /tmp/custom-resources.yaml
# find:
# spec:
#   calicoNetwork:
#     ipPools:
#       - name: default-ipv4-ippool
#         cidr: 192.168.0.0/16
# replace:
# spec:
#   calicoNetwork:
#     ipPools:
#       - name: default-ipv4-ippool
#         cidr: 10.244.0.0/16

# create resources
kubectl create -f /tmp/custom-resources.yaml
# installation.operator.tigera.io/default created
# apiserver.operator.tigera.io/default created
# goldmane.operator.tigera.io/default created
# whisker.operator.tigera.io/default created

# wait until all available
watch kubectl get tigerastatus

# confirm: node status ready
kubectl get node
# NAME           STATUS   ROLES    AGE   VERSION
# controlplane   Ready    <none>   36m   v1.35.8
```

---

## Test controlplane

```sh
kubectl get po -A
# NAMESPACE         NAME                                       READY   STATUS    RESTARTS   AGE
# calico-system     calico-apiserver-d6897b8df-dlc62           1/1     Running   0          4m1s
# calico-system     calico-apiserver-d6897b8df-p6rxz           1/1     Running   0          4m1s
# calico-system     calico-kube-controllers-86884dfdcf-8cxd2   1/1     Running   0          4m
# calico-system     calico-node-fz5wr                          1/1     Running   0          4m
# calico-system     calico-typha-86d46f7cdd-w9lth              1/1     Running   0          4m
# calico-system     csi-node-driver-fd725                      2/2     Running   0          4m
# calico-system     goldmane-5d7c56cd95-hll92                  1/1     Running   0          4m1s
# calico-system     whisker-5cc8cd46d5-x29pd                   2/2     Running   0          3m25s
# tigera-operator   tigera-operator-676bbdd645-7npnz           1/1     Running   0          9m29s
```

---

## CoreDNS

```sh
# download
curl -sL -o /tmp/coredns.yaml https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.35/cluster/addons/dns/coredns/coredns.yaml.base

sed -i \
  -e 's/__DNS__DOMAIN__/cluster.local/g' \
  -e 's/__DNS__SERVER__/10.96.0.10/g' \
  -e 's/__DNS__MEMORY__LIMIT__/170Mi/g' \
  -e 's/__PILLAR__DNS__DOMAIN__/cluster.local/g' \
  -e 's/__PILLAR__DNS__SERVER__/10.96.0.10/g' \
  -e 's/__PILLAR__DNS__MEMORY__LIMIT__/170Mi/g' \
  -e 's/__PILLAR__CLUSTER__DNS__/10.96.0.10/g' \
  /tmp/coredns.yaml

sed -i 's|forward . /etc/resolv.conf|forward . 8.8.8.8 1.1.1.1|' /tmp/coredns.yaml

grep -n 'forward' /tmp/coredns.yaml
# 77:        forward . 8.8.8.8 1.1.1.1 {

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

# Name:   kubernetes.default.svc.cluster.local
# Address: 10.96.0.1

# test: fully qualified
kubectl exec -it dnsutils -- nslookup kubernetes.default.svc.cluster.local
# Server:         10.96.0.10
# Address:        10.96.0.10#53

# Name:   kubernetes.default.svc.cluster.local
# Address: 10.96.0.1

kubectl delete pod dnsutils
# pod "dnsutils" deleted from default namespace
```
