# CKA - Cluster

[Back](../index.md)

- [CKA - Cluster](#cka---cluster)
  - [kubeadm](#kubeadm)
    - [Task: join a node](#task-join-a-node)
    - [Task: Install CNI](#task-install-cni)
    - [Task: Install runtime](#task-install-runtime)
    - [Task: install runtime](#task-install-runtime-1)
  - [Cluster](#cluster)
    - [Task: Upgrade controlplane](#task-upgrade-controlplane)
    - [Task: Snapshot etcd](#task-snapshot-etcd)
    - [Task: Troubleshooting](#task-troubleshooting)
    - [Task: upgrade cluster](#task-upgrade-cluster)
    - [Task: backup and restore etcd](#task-backup-and-restore-etcd)
    - [Task: Troubleshooting worker node](#task-troubleshooting-worker-node)
    - [Task: fix cluster connection](#task-fix-cluster-connection)
    - [Task: Troubleshooting API server](#task-troubleshooting-api-server)
  - [Scheduling](#scheduling)
    - [Task: Node selector](#task-node-selector)
    - [Task: node selector](#task-node-selector-1)
    - [Task: Taints and Tolerations](#task-taints-and-tolerations)
    - [Task: Taints](#task-taints)
    - [Task: available node](#task-available-node)
    - [Task: Cordon](#task-cordon)

---

## kubeadm

### Task: join a node

CKA EXAM OBJECTIVE: Create and manage Kubernetes clusters using kubeadm
TASK:

1. Join node02 to your existing kubeadm cluster. It has already been pre-provisioned with all necessary inst
   allations.

---

- Solution

- ref:
  - https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/
    - Token-based discovery with CA pinning

```sh
# ssh to controlplane
k get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   47d   v1.33.6

# output command with tokens
kubeadm token create --print-join-command
# kubeadm join 192.168.10.150:6443 --token 50jiwr.l7--discovery-token-ca-cert-hash sha256:f56b2

# ssh to node02

# join with command
sudo kubeadm join 192.168.10.150:6443 --token 50jiwr.l7--discovery-token-ca-cert-hash sha256:f56b2
# This node has joined the cluster:
# * Certificate signing request was sent to apiserver and a response was received.
# * The Kubelet was informed of the new secure connection details.

# confirm
# ssh controlplane
k get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   62m   v1.32.11
# node01         Ready    <none>          15m   v1.32.11
# node02         Ready    <none>          14m   v1.32.11
```

> if error, reset the kubelet: `kubeadm reset`

---

### Task: Install CNI

Install and configure a Container Network Interface (CNI) of your choice that meets the specified requirements. Choose one of the following CNI options:

- Flannel using the manifest:
  - https://github.com/flannel-io/flannel/releases/download/v0.26.1/kube-flannel.yml
- Calico using the manifest:
  - crds: https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/operator-crds.yaml
  - Tigera Operator:https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/tigera-operator.yaml

Ensure the selected CNI is properly installed and configured in the Kubernetes cluster.

- The CNI you choose must:
  - Let Pods communicate with each other
  - Support Network Policy enforcement
  - Install from manifest files (do not use Helm)

---

- Solution

```sh
# install operator
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/operator-crds.yaml
# namespace/tigera-operator created
# serviceaccount/tigera-operator created
# clusterrole.rbac.authorization.k8s.io/tigera-operator-secrets created
# clusterrole.rbac.authorization.k8s.io/tigera-operator created
# clusterrolebinding.rbac.authorization.k8s.io/tigera-operator created
# rolebinding.rbac.authorization.k8s.io/tigera-operator-secrets created
# deployment.apps/tigera-operator created

# confirm
kubectl get pod -n tigera-operator
# NAME                              READY   STATUS    RESTARTS   AGE
# tigera-operator-7d4578d8d-hb6sg   1/1     Running   0          2m50s

# install customer resources
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/custom-resources.yaml
# installation.operator.tigera.io/default created
# apiserver.operator.tigera.io/default created
# goldmane.operator.tigera.io/default created
# whisker.operator.tigera.io/default created

kubectl get tigerastatus
# NAME        AVAILABLE   PROGRESSING   DEGRADED   SINCE
# apiserver                             True
# calico                                True
# goldmane                              True
# ippools                               True
# whisker                               True

# test
kubectl run web2test --image=nginx
kubectl expose pod web2test --port=80 --name=web2test-svc

kubectl get pod,svc
# NAME           READY   STATUS    RESTARTS   AGE
# pod/web2test   1/1     Running   0          22m

# NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes     ClusterIP   10.96.0.1        <none>        443/TCP   3d22h
# service/web2test-svc   ClusterIP   10.107.175.223   <none>        80/TCP    2m31s

kubectl run --rm -it tester --image=busybox --restart=Never -- wget -qO- http://web2test-svc
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
# html { color-scheme: light dark; }
# body { width: 35em; margin: 0 auto;
# font-family: Tahoma, Verdana, Arial, sans-serif; }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>
# pod "tester" deleted

# test network policy
tee netpol.yaml<<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

kubectl apply -f netpol.yaml
# networkpolicy.networking.k8s.io/deny-all created

kubectl describe netpol deny-all
# Name:         deny-all
# Namespace:    default
# Created on:   2026-01-16 18:01:26 -0500 EST
# Labels:       <none>
# Annotations:  <none>
# Spec:
#   PodSelector:     <none> (Allowing the specific traffic to all pods in this namespace)
#   Allowing ingress traffic:
#     <none> (Selected pods are isolated for ingress connectivity)
#   Allowing egress traffic:
#     <none> (Selected pods are isolated for egress connectivity)
#   Policy Types: Ingress, Egress

# test networkpolicy
kubectl run --rm -it tester --image=busybox --restart=Never -- wget -qO- http://web2test-svc
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
# html { color-scheme: light dark; }
# body { width: 35em; margin: 0 auto;
# font-family: Tahoma, Verdana, Arial, sans-serif; }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>
# pod "tester" deleted
```

---

### Task: Install runtime

This question needs to be solved on node node01. To access the node using SSH, use the credentials below:

username: bob
password: caleston123

As an administrator, you need to prepare node01 to install kubernetes. One of the steps is installing a container runtime. Install the cri-dockerd_0.3.22.3-0.ubuntu-jammy_amd64.deb package located in /root and ensure that the cri-docker service is running and enabled to start on boot.

---

- Solution

```sh
sudo -i
dpkg -i /root/cri-dockerd_0.3.22.3-0.ubuntu-jammy_amd64.deb

apt-get update
apt-get install -f -y

systemctl daemon-reload
systemctl enable --now cri-docker

systemctl status cri-docker
# Warning: The unit file, source configuration file or drop-ins of cri-docker.service changed on di>
# ● cri-docker.service - CRI Interface for Docker Application Container Engine
#      Loaded: loaded (/usr/lib/systemd/system/cri-docker.service; enabled; preset: enabled)
#      Active: active (running) since Sat 2026-01-17 20:43:32 EST; 1min 42s ago
# TriggeredBy: ● cri-docker.socket
#        Docs: https://docs.mirantis.com
#    Main PID: 2403 (cri-dockerd)
#       Tasks: 10
#      Memory: 9.8M (peak: 10.2M)
#         CPU: 77ms
#      CGroup: /system.slice/cri-docker.service
#              └─2403 /usr/bin/cri-dockerd --container-runtime-endpoint fd://
```

---

### Task: install runtime

Prepare a Linux system for Kubernetes. Docker is already installed, but you
need to configure it for kubeadm.
Task

Complete these tasks to prepare the system for Kubernetes :

- Set up cri-dockerd:
  - Install the Debian package `~/cri-dockerd_0.3.9.3-0.ubuntu-jammy_amd64.deb`
  - Debian packages are installed using dpkg.

Enable and start the cri-docker service

- Configure these system parameters:
  - Set net.bridge.bridge-nf-call-iptables to 1
  - Set net.ipv6.conf.all.forwarding to 1
  - Set net.ipv4.ip_forward to 1
  - Set net.netfilter.nf_conntrack max to 131072

- Setup Env

```sh
wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.3.22/cri-dockerd_0.3.22.3-0.ubuntu-jammy_amd64.deb
ls ~/cri-dockerd_0.3.22.3-0.ubuntu-jammy_amd64.deb


```

---

- Solution

```sh
sudo dpkg -i ~/cri-dockerd_0.3.9.3-0.ubuntu-jammy_amd64.deb
sudo apt-get -f install -y
cri-dockerd --version

sudo systemctl daemon-reload
sudo systemctl enable cri-docker
sudo systemctl start cri-docker

sudo tee /etc/sysctl.d/99-kubernetes-cri.conf <<EOF
net.bridge.bridge-nf-call-iptables = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.ip_forward = 1
net.netfilter.nf_conntrack_max = 131072
EOF

sudo sysctl --system
```

---

## Cluster

### Task: Upgrade controlplane

CKA EXAM OBJECTIVE: Manage the lifecycle of Kubernetes clusters
TASK:

1. Use kubeadm to upgrade the controller node from version v1.31.4 to v1.32.1.
2. You will also upgrade kubelet and kubectl to match this version.

---

- Solution

- ref:
  - https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/
- Common mistake:
  - log in the wrong node
  - use incorrect versions

```sh
# confirm the node to be upgraded
# confirm the version
k get node

# update version in config
vi /etc/apt/sources.list.d/kubernetes.list
#  https://pkgs.k8s.io/core:/stable:/v1.33/deb/

# update repo
sudo apt update

# find the version to update
sudo apt-cache madison kubeadm
#  kubeadm | 1.33.7-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
#  kubeadm | 1.33.6-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
#  kubeadm | 1.33.5-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
#  kubeadm | 1.33.4-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
#  kubeadm | 1.33.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
#  kubeadm | 1.33.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
#  kubeadm | 1.33.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
#  kubeadm | 1.33.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages

# unhold
sudo apt-mark unhold kubeadm
# update packages
sudo apt-get update
# install the correct version
sudo apt-get install -y kubeadm='1.33.7-1.1'

# hold
sudo apt-mark hold kubeadm

# confirm adm version
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"33", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.33.7", GitCommit:"a7245cdf3f69e11356c7e8f92b3e78ca4ee4e757", GitTreeState:"clean", BuildDate:"2025-12-09T14:41:01Z", GoVersion:"go1.24.11", Compiler:"gc", Platform:"linux/amd64"}

# Verify the upgrade plan
sudo kubeadm upgrade plan

# upgrade with correct version
sudo kubeadm upgrade apply v1.33.7

# ########### upgrade kubelet

# drain
kubectl drain <node-to-drain> --ignore-daemonsets

# find the version
apt-cache madison kubelet
# kubelet | 1.33.7-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubelet | 1.33.6-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubelet | 1.33.5-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubelet | 1.33.4-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubelet | 1.33.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubelet | 1.33.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubelet | 1.33.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubelet | 1.33.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages

apt-cache madison kubectl
# kubectl | 1.33.7-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubectl | 1.33.6-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubectl | 1.33.5-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubectl | 1.33.4-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubectl | 1.33.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubectl | 1.33.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubectl | 1.33.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages
# kubectl | 1.33.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.33/deb  Packages

sudo apt-mark unhold kubelet kubectl
sudo apt-get update
sudo apt-get install -y kubelet='1.33.7-1.1' kubectl='1.33.7-1.1'
sudo apt-mark hold kubelet kubectl

# Restart the kubelet:
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# Uncordon the node
kubectl uncordon controlplane

# confirm node and version
kubectl get nodes
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   82m   v1.33.7
# node01         Ready    <none>          34m   v1.32.11
# node02         Ready    <none>          34m   v1.32.11
```

---

### Task: Snapshot etcd

CKA EXAM OBJECTIVE: Manage the lifecycle of Kubernetes clusters
TASK :

1. Take a snapshot of the etcd cluster and save it as /opt/clusterstate.backup
2. Restore the cluster state from /opt/clusterstate.backup.

- Save path: /var/lib/backup/etcd-snapshot.db
- cacert: /etc/kubernetes/pki/etcd/ca.crt
- cert: /etc/kubernetes/pki/etcd/server.crt
- key: /etc/kubernetes/pki/etcd/server.key

---

- Solution

- ref:
  - https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster

- Dangous Step
  - better do it first.
- !!!: This will hang
  - `sudo ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db`
- !!!: always use command with options

```sh
# get crt and key
sudo cat /etc/kubernetes/manifests/etcd.yaml
#   - --cert-file=/etc/kubernetes/pki/etcd/server.crt
#   - --listen-client-urls=https://127.0.0.1:2379,https://192.168.10.150:2379
#   - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
#   - --key-file=/etc/kubernetes/pki/etcd/server.key
# - hostPath:
#     path: /var/lib/etcd
#     type: DirectoryOrCreate
#   name: etcd-data

export ETCDCTL_API=3
etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /var/lib/backup/etcd-snapshot.db
# {"level":"info","ts":1768269549.202995,"caller":"snapshot/v3_snapshot.go:119","msg":"created temporary db file","path":"/var/lib/backup/etcd-snapshot.db.part"}
# {"level":"info","ts":"2026-01-12T20:59:09.208264-0500","caller":"clientv3/maintenance.go:212","msg":"opened snapshot stream; downloading"}
# {"level":"info","ts":1768269549.2083018,"caller":"snapshot/v3_snapshot.go:127","msg":"fetching snapshot","endpoint":"https://127.0.0.1:2379"}
# {"level":"info","ts":"2026-01-12T20:59:09.25052-0500","caller":"clientv3/maintenance.go:220","msg":"completed snapshot read; closing"}
# {"level":"info","ts":1768269549.2593517,"caller":"snapshot/v3_snapshot.go:142","msg":"fetched snapshot","endpoint":"https://127.0.0.1:2379","size":"4.2 MB","took":0.056287114}
# {"level":"info","ts":1768269549.259501,"caller":"snapshot/v3_snapshot.go:152","msg":"saved","path":"/var/lib/backup/etcd-snapshot.db"}
# Snapshot saved at /var/lib/backup/etcd-snapshot.db

# Verify the snapshot
sudo etcdctl --write-out=table snapshot status /var/lib/backup/etcd-snapshot.db
# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | 943ae218 |     7340 |       1516 |     4.2 MB |
# +----------+----------+------------+------------+
```

---

- Restore
  - ref: https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#restoring-an-etcd-cluster
- Command int he doc without option
  - it will hang
  - need to **add option**

```sh
# get default data dir
sudo cat /etc/kubernetes/manifests/etcd.yaml
# - hostPath:
#     path: /var/lib/etcd
#     type: DirectoryOrCreate
#   name: etcd-data

# set data-dir a new path
export ETCDCTL_API=3
sudo etcdctl --data-dir /var/lib/etcd/data snapshot restore /var/lib/backup/etcd-snapshot.db
# {"level":"info","ts":1768270244.5142756,"caller":"snapshot/v3_snapshot.go:306","msg":"restoring snapshot","path":"/var/lib/backup/etcd-snapshot.db","wal-dir":"/var/lib/etcd/data/member/wal","data-dir":"/var/lib/etcd/data","snap-dir":"/var/lib/etcd/data/member/snap"}
# {"level":"info","ts":1768270244.6023808,"caller":"mvcc/kvstore.go:388","msg":"restored last compact revision","meta-bucket-name":"meta","meta-bucket-name-key":"finishedCompactRev","restored-compact-revision":6631}
# {"level":"info","ts":1768270244.6671963,"caller":"membership/cluster.go:392","msg":"added member","cluster-id":"cdf818194e3a8c32","local-member-id":"0","added-peer-id":"8e9e05c52164694d","added-peer-peer-urls":["http://localhost:2380"]}
# {"level":"info","ts":1768270244.7137876,"caller":"snapshot/v3_snapshot.go:326","msg":"restored snapshot","path":"/var/lib/backup/etcd-snapshot.db","wal-dir":"/var/lib/etcd/data/member/wal","data-dir":"/var/lib/etcd/data","snap-dir":"/var/lib/etcd/data/member/snap"}

# confirm
sudo ls /var/lib/etcd/data

# update etcd config for the new data-dir
# /etc/kubernetes/manifests/etcd.yaml's volumes.hostPath.path
vi /etc/kubernetes/manifests/etcd.yaml
  # - hostPath:
  #     path: /var/lib/etcd/data
  #     type: DirectoryOrCreate
  #   name: etcd-data

# wait for kubectl
 kubectl get node
```

> data-dir-location: must diff from backup-file-location
> default path: /var/lib/etcd
> It will take munites for restore etcd, at the same time kubectl will fail.

---

### Task: Troubleshooting

CKA EXAM OBJECTIVE: Troubleshoot clusters and nodes
TASK:

1. Fix whatever problem is causing a node to be in the NotReady state.

---

- Solution

```sh
# identify the failure node
kubectl get nodes

kubectl describe node NODE_NAME
# commonly show nothing useful

# ssh node
# check kubelet service
sudo systemctl status kubelet

sudo systemctl restart kubelet

sudo systemctl status kubelet

# ssh controlplane
# confirm
kubectl get node
```

---

### Task: upgrade cluster

设置配置环境：
[candidate@node-1] $ kubectl config use-context mk8s

Task
现有的 Kubernetes 集群正在运行版本 1.24.2。仅将 master 节点上的所有 Kubernetes 控制平面和节点组件升级到版本 1.24.3。

确保在升级之前 drain master 节点，并在升级后 uncordon master 节点。

可以使用以下命令，通过 ssh 连接到 master 节点：
ssh master01
可以使用以下命令，在该 master 节点上获取更高权限：
sudo -i

另外，在主节点上升级 kubelet 和 kubectl。
请不要升级工作节点，etcd，container 管理器，CNI 插件， DNS 服务或任何其他插件。Copy

---

- Preparation

```sh
# get current version
kubectl version
# Client Version: v1.33.6
# Kustomize Version: v5.6.0
# Server Version: v1.33.6

# kubeadm version
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"33", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.33.6", GitCommit:"1e09fec02ac194c1044224e45e60d249e98cd092", GitTreeState:"clean", BuildDate:"2025-11-11T19:13:44Z", GoVersion:"go1.24.9", Compiler:"gc", Platform:"linux/amd64"}

# get nodes
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   44d   v1.33.6
# node01         Ready    <none>          43d   v1.33.6
# node02         Ready    <none>          43d   v1.33.6

# drain master
kubectl drain controlplane --ignore-daemonsets --delete-emptydir-data
# node/controlplane already cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-vjfmq, kube-system/kube-proxy-8rr2r
# evicting pod kube-system/coredns-674b8bbfcf-4chqx
# evicting pod kube-system/coredns-674b8bbfcf-tx5xf
# pod/coredns-674b8bbfcf-tx5xf evicted
# pod/coredns-674b8bbfcf-4chqx evicted
# node/controlplane drained

kubectl describe node controlplane | grep Unschedulable
# Unschedulable:      true
```

- Upgrading control plane nodes

```sh
# Find the latest patch release
sudo apt update
apt-cache madison kubeadm
#  kubeadm | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubeadm | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubeadm | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubeadm | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

# Upgrade kubeadm: replace version
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.34.3-1.1' && \
sudo apt-mark hold kubeadm

# confirm
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"34", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.34.3", GitCommit:"df11db1c0f08fab3c0baee1e5ce6efbf816af7f1", GitTreeState:"clean", BuildDate:"2025-12-09T15:05:15Z", GoVersion:"go1.24.11", Compiler:"gc", Platform:"linux/amd64"}


# Verify the upgrade plan
sudo kubeadm upgrade plan
# [preflight] Running pre-flight checks.
# [upgrade/config] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [upgrade/config] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
# [upgrade] Running cluster health checks
# [upgrade] Fetching available versions to upgrade to
# [upgrade/versions] Cluster version: 1.33.6
# [upgrade/versions] kubeadm version: v1.34.3
# I0108 20:37:17.267120  133354 version.go:260] remote version is much newer: v1.35.0; falling back to: stable-1.34
# [upgrade/versions] Target version: v1.34.3
# [upgrade/versions] Latest version in the v1.33 series: v1.33.7

# Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
# COMPONENT   NODE           CURRENT   TARGET
# kubelet     controlplane   v1.33.6   v1.33.7
# kubelet     node01         v1.33.6   v1.33.7
# kubelet     node02         v1.33.6   v1.33.7

# Upgrade to the latest version in the v1.33 series:

# COMPONENT                 NODE           CURRENT    TARGET
# kube-apiserver            controlplane   v1.33.6    v1.33.7
# kube-controller-manager   controlplane   v1.33.6    v1.33.7
# kube-scheduler            controlplane   v1.33.6    v1.33.7
# kube-proxy                               1.33.6     v1.33.7
# CoreDNS                                  v1.12.0    v1.12.1
# etcd                      controlplane   3.5.24-0   3.5.24-0

# You can now apply the upgrade by executing the following command:

#         kubeadm upgrade apply v1.33.7

# _____________________________________________________________________

# Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
# COMPONENT   NODE           CURRENT   TARGET
# kubelet     controlplane   v1.33.6   v1.34.3
# kubelet     node01         v1.33.6   v1.34.3
# kubelet     node02         v1.33.6   v1.34.3

# Upgrade to the latest stable version:

# COMPONENT                 NODE           CURRENT    TARGET
# kube-apiserver            controlplane   v1.33.6    v1.34.3
# kube-controller-manager   controlplane   v1.33.6    v1.34.3
# kube-scheduler            controlplane   v1.33.6    v1.34.3
# kube-proxy                               1.33.6     v1.34.3
# CoreDNS                                  v1.12.0    v1.12.1
# etcd                      controlplane   3.5.24-0   3.6.5-0

# You can now apply the upgrade by executing the following command:

#         kubeadm upgrade apply v1.34.3

# _____________________________________________________________________


# The table below shows the current state of component configs as understood by this version of kubeadm.
# Configs that have a "yes" mark in the "MANUAL UPGRADE REQUIRED" column require manual config upgrade or
# resetting to kubeadm defaults before a successful upgrade can be performed. The version to manually
# upgrade to is denoted in the "PREFERRED VERSION" column.

# API GROUP                 CURRENT VERSION   PREFERRED VERSION   MANUAL UPGRADE REQUIRED
# kubeproxy.config.k8s.io   v1alpha1          v1alpha1            no
# kubelet.config.k8s.io     v1beta1           v1beta1             no
# _____________________________________________________________________


# upgrade
sudo kubeadm upgrade apply v1.34.3
# [upgrade] SUCCESS! A control plane node of your cluster was upgraded to "v1.34.3".
# [upgrade] Now please proceed with upgrading the rest of the nodes by following the right order.

# confirm: server version
kubectl version
# Client Version: v1.33.6
# Kustomize Version: v5.6.0
# Server Version: v1.34.3

```

- upgrade kubelet 和 kubectl

```sh
kubectl drain controlplane --ignore-daemonsets
# node/controlplane cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-vjfmq, kube-system/kube-proxy-mlgw2
# node/controlplane drained

# confirm
kubectl describe node controlplane | grep Unschedulable
# Unschedulable:      true

sudo apt-cache madison kubelet
# kubelet | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubelet | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubelet | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubelet | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

apt-cache madison kubectl
# kubectl | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubectl | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubectl | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubectl | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages


# Upgrade the kubelet and kubectl
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='1.34.3-1.1' kubectl='1.34.3-1.1' && \
sudo apt-mark hold kubelet kubectl

# Restart the kubelet:
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# Uncordon the node
kubectl uncordon controlplane
# node/controlplane uncordoned

# confirm
kubectl describe node controlplane | grep Unschedulable
# Unschedulable:      false

# confirm
kubectl version
# Client Version: v1.34.3
# Kustomize Version: v5.7.1
# Server Version: v1.34.3

kubectl get nodes
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   44d   v1.34.3
# node01         Ready    <none>          44d   v1.33.6
# node02         Ready    <none>          43d   v1.33.6
```

---

### Task: backup and restore etcd

设置配置环境
此项目无需更改配置环境。但是，在执行此项目之前，请确保您已返回初始节点。
[candidate@master01] $ exit #注意，这个之前是在 master01 上，所以要 exit 退到 node01，如果已经是 node01 了，就不要再 exit 了。

Task
首先，为运行在 https://11.0.1.111:2379 上的现有 etcd 实例创建快照并将快照保存到 /var/lib/backup/etcd-snapshot.db
（注意，真实考试中，这里写的是 https://127.0.0.1:2379）
为给定实例创建快照预计能在几秒钟内完成。 如果该操作似乎挂起，则命令可能有问题。用 CTRL + C 来取消操作，然后重试。

然后还原位于/data/backup/etcd-snapshot-previous.db 的现有先前快照。
提供了以下 TLS 证书和密钥，以通过 etcdctl 连接到服务器。

CA 证书: /opt/KUIN00601/ca.crt
客户端证书: /opt/KUIN00601/etcd-client.crt
客户端密钥: /opt/KUIN00601/etcd-client.key

---

- ref:

- Backup

```sh
sudo mkdir -pv /var/lib/backup/

export ETCDCTL_API=3
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot save /var/lib/backup/etcd-snapshot.db

# Verify the snapshot:
sudo -i ETCDCTL_API=3 etcdctl --write-out=table snapshot status /var/lib/backup/etcd-snapshot.db
# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | 765f9b29 |   454115 |       1907 |     8.7 MB |
# +----------+----------+------------+------------+
```

- Restore

```sh
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot restore /var/lib/backup/etcd-snapshot.db

sudo vi /etc/kubernetes/manifests/etcd.yaml
# find:
# - name: etcd-data
#   hostPath:
#     path: /var/lib/etcd
# update:
# - name: etcd-data
#   hostPath:
#     path: /var/lib/backup
```

---

### Task: Troubleshooting worker node

设置配置环境：
[candidate@node-1] $ kubectl config use-context wk8s

Task
名为 node02 的 Kubernetes worker node 处于 NotReady 状态。
调查发生这种情况的原因，并采取相应的措施将 node 恢复为 Ready 状态，确保所做的任何更改永久生效。

可以使用以下命令，通过 ssh 连接到 node02 节点：
ssh node02
可以使用以下命令，在该节点上获取更高权限：
sudo -i

---

- Prepare Exam Environment

```sh
ssh node02
sudo systemctl stop kubelet
sudo systemctl status kubelet
# ○ kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: inactive (dead) since Thu 2026-01-08 22:07:20 EST; 14s ago
#    Duration: 2w 1d 5h 28min 15.575s
#        Docs: https://kubernetes.io/docs/
#     Process: 1294 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBEL>
#    Main PID: 1294 (code=exited, status=0/SUCCESS)
#         CPU: 4h 2min 16.574s
```

- Solution

```sh
ssh node01

kubectl get node
# NAME           STATUS     ROLES           AGE   VERSION
# controlplane   Ready      control-plane   44d   v1.34.3
# node01         Ready      <none>          44d   v1.33.6
# node02         NotReady   <none>          44d   v1.33.6

kubectl describe node node02
# Conditions:
#   Type                 Status    LastHeartbeatTime                 LastTransitionTime                Reason              Message
#   ----                 ------    -----------------                 ------------------                ------              -------
#   NetworkUnavailable   False     Mon, 05 Jan 2026 01:16:38 -0500   Mon, 05 Jan 2026 01:16:38 -0500   FlannelIsUp         Flannel is running on this node
#   MemoryPressure       Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
#   DiskPressure         Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
#   PIDPressure          Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
#   Ready                Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
# Events:
#   Type     Reason                   Age                  From             Message
#   ----     ------                   ----                 ----             -------
#   Normal   Starting                 9m5s                 kubelet          Starting kubelet.
#   Warning  InvalidDiskCapacity      9m5s                 kubelet          invalid capacity 0 on image filesystem
#   Normal   NodeAllocatableEnforced  9m4s                 kubelet          Updated Node Allocatable limit across pods
#   Normal   NodeHasSufficientMemory  9m4s (x2 over 9m4s)  kubelet          Node node02 status is now: NodeHasSufficientMemory
#   Normal   NodeHasNoDiskPressure    9m4s (x2 over 9m4s)  kubelet          Node node02 status is now: NodeHasNoDiskPressure
#   Normal   NodeHasSufficientPID     9m4s (x2 over 9m4s)  kubelet          Node node02 status is now: NodeHasSufficientPID
#   Normal   NodeReady                9m4s                 kubelet          Node node02 status is now: NodeReady
#   Normal   NodeNotReady             94s (x2 over 11m)    node-controller  Node node02 status is now: NodeNotReady
```

- Diagnose

```sh
ssh node02

sudo -i

# check log
journalctl -u kubelet -xe --no-pager | tail -n 60
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.971510 1346259 memory_manager.go:186] "Starting memorymanager" policy="None"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.971570 1346259 state_mem.go:35] "Initializing new in-memory state store"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.973184 1346259 state_mem.go:75] "Updated machine memory state"
# Jan 08 22:10:18 node02 kubelet[1346259]: E0108 22:10:18.991945 1346259 manager.go:517] "Failed to read data from checkpoint" err="checkpoint is not found" checkpoint="kubelet_internal_checkpoint"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.993449 1346259 eviction_manager.go:189] "Eviction manager: starting control loop"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.993493 1346259 container_log_manager.go:189] "Initializing container log rotate workers" workers=1 monitorPeriod="10s"
# Jan 08 22:10:18 node02 kubelet[1346259]: E0108 22:10:18.997433 1346259 eviction_manager.go:267] "eviction manager: failed to check if we have separate container filesystem. Ignoring." err="no imagefs label for configured runtime"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:18.998332 1346259 plugin_manager.go:118] "Starting Kubelet Plugin Manager"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.003216 1346259 kuberuntime_manager.go:1746] "Updating runtime config through cri with podcidr" CIDR="10.244.2.0/24"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.048343 1346259 kubelet_network.go:61] "Updating Pod CIDR" originalPodCIDR="" newPodCIDR="10.244.2.0/24"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.052192 1346259 kubelet_node_status.go:501] "Fast updating node status as it just became ready"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.151261 1346259 apiserver.go:52] "Watching apiserver"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.205231 1346259 kubelet_node_status.go:75] "Attempting to register node" node="node02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.257612 1346259 desired_state_of_world_populator.go:158] "Finished populating initial desired state of world"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.276066 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"registration-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-registration-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.276302 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"dev-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-dev-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.276485 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"run\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-run\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.287285 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"xtables-lock\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-xtables-lock\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.287577 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"socket-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-socket-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.288596 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"xtables-lock\" (UniqueName: \"kubernetes.io/host-path/f2c5d99e-11bd-40d1-adc1-1addb0f95798-xtables-lock\") pod \"kube-proxy-sx5wr\" (UID: \"f2c5d99e-11bd-40d1-adc1-1addb0f95798\") " pod="kube-system/kube-proxy-sx5wr"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.296105 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"lib-modules\" (UniqueName: \"kubernetes.io/host-path/f2c5d99e-11bd-40d1-adc1-1addb0f95798-lib-modules\") pod \"kube-proxy-sx5wr\" (UID: \"f2c5d99e-11bd-40d1-adc1-1addb0f95798\") " pod="kube-system/kube-proxy-sx5wr"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.296480 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"cni-plugin\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-cni-plugin\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.306376 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"plugins-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-plugins-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.310969 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"csi-data-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-csi-data-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.313071 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"cni\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-cni\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.317281 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"var-lib-calico\" (UniqueName: \"kubernetes.io/host-path/462c6931-5abd-4b32-a1fb-2018c5ae055f-var-lib-calico\") pod \"tigera-operator-7d4578d8d-8vf9w\" (UID: \"462c6931-5abd-4b32-a1fb-2018c5ae055f\") " pod="tigera-operator/tigera-operator-7d4578d8d-8vf9w"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.317415 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"mountpoint-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-mountpoint-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.363982 1346259 kubelet_node_status.go:124] "Node was previously registered" node="node02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.364443 1346259 kubelet_node_status.go:78] "Successfully registered node" node="node02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.691938 1346259 csi_plugin.go:106] kubernetes.io/csi: Trying to validate a new CSI Driver with name: hostpath.csi.k8s.io endpoint: /var/lib/kubelet/plugins/csi-hostpath/csi.sock versions: 1.0.0
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.697336 1346259 csi_plugin.go:119] kubernetes.io/csi: Register new plugin with name: hostpath.csi.k8s.io at endpoint: /var/lib/kubelet/plugins/csi-hostpath/csi.sock
# Jan 08 22:16:57 node02 systemd[1]: Stopping kubelet.service - kubelet: The Kubernetes Node Agent...
# ░░ Subject: A stop job for unit kubelet.service has begun execution
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ A stop job for unit kubelet.service has begun execution.
# ░░
# ░░ The job identifier is 67933.
# Jan 08 22:16:57 node02 kubelet[1346259]: I0108 22:16:57.312242 1346259 dynamic_cafile_content.go:175] "Shutting down controller" name="client-ca-bundle::/etc/kubernetes/pki/ca.crt"
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Deactivated successfully.
# ░░ Subject: Unit succeeded
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ The unit kubelet.service has successfully entered the 'dead' state.
# Jan 08 22:16:57 node02 systemd[1]: Stopped kubelet.service - kubelet: The Kubernetes Node Agent.
# ░░ Subject: A stop job for unit kubelet.service has finished
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ A stop job for unit kubelet.service has finished.
# ░░
# ░░ The job identifier is 67933 and the job result is done.
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Consumed 26.274s CPU time, 89.4M memory peak, 0B memory swap peak.
# ░░ Subject: Resources consumed by unit runtime
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ The unit kubelet.service completed and consumed the indicated resources.

# check kubelet
systemctl status kubelet --no-pager
# ○ kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: inactive (dead) since Thu 2026-01-08 22:16:57 EST; 5min ago
#    Duration: 6min 40.143s
#        Docs: https://kubernetes.io/docs/
#     Process: 1346259 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS (code=exited, status=0/SUCCESS)
#    Main PID: 1346259 (code=exited, status=0/SUCCESS)
#         CPU: 26.274s

# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.317415 1346259 reconciler_common.go:251] …
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.363982 1346259 kubelet_node_status.…ode02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.364443 1346259 kubelet_node_status.…ode02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.691938 1346259 csi_plugin.go:106] k… 1.0.0
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.697336 1346259 csi_plugin.go:119] k…i.sock
# Jan 08 22:16:57 node02 systemd[1]: Stopping kubelet.service - kubelet: The Kubernetes Node …ent...
# Jan 08 22:16:57 node02 kubelet[1346259]: I0108 22:16:57.312242 1346259 dynamic_cafile_conte…a.crt"
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Deactivated successfully.
# Jan 08 22:16:57 node02 systemd[1]: Stopped kubelet.service - kubelet: The Kubernetes Node Agent.
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Consumed 26.274s CPU time, 89.4M memory… peak.
# Hint: Some lines were ellipsized, use -l to show in full.


# check container runtime
systemctl status containerd --no-pager
# ● containerd.service - containerd container runtime
#      Loaded: loaded (/usr/lib/systemd/system/containerd.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2025-12-24 16:39:07 EST; 2 weeks 1 day ago
#        Docs: https://containerd.io
#    Main PID: 1279 (containerd)
#       Tasks: 123
#      Memory: 119.0M (peak: 353.0M)
#         CPU: 1h 41min 10.049s
#      CGroup: /system.slice/containerd.service
#              ├─   1279 /usr/bin/containerd
#              ├─ 998698 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 074b829e17d42c30e1d…
#              ├─1106965 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 886323e8aff112d8ecf…
#              ├─1111471 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 2650b7b8f91b24f236c…
#              ├─1136983 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 5c4eb6a2c3e8029c9b7…
#              ├─1174159 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 62aa1841e5f52ebc830…
#              ├─1323970 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 64f4f2986757ee970ff…
#              ├─1323972 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 6248e8312b504aa68af…
#              └─1324433 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id c353def57aea55f5a2b…

# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.882044101-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.883482261-05:00" level=i…6ec\""
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.919718776-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.919773879-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.921404147-05:00" level=i…6ec\""
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.921463749-05:00" level=i…6ec\""
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.961157008-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.968244305-05:00" level=w…atus."
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.968527616-05:00" level=i…fully"
# Jan 08 22:10:19 node02 containerd[1279]: time="2026-01-08T22:10:19.033113557-05:00" level=i…nfig."
# Hint: Some lines were ellipsized, use -l to show in full.
```

- Solution

```sh
# check kubelet
sudo systemctl enable kubelet --now

# confirm
sudo systemctl status kubelet
# ● kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: active (running) since Thu 2026-01-08 22:10:17 EST; 8s ago
#        Docs: https://kubernetes.io/docs/
#    Main PID: 1346259 (kubelet)
#       Tasks: 14 (limit: 2205)
#      Memory: 88.5M (peak: 89.4M)
#         CPU: 3.515s
#      CGroup: /system.slice/kubelet.service
#              └─1346259 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.>
```

- Confirm

```sh
ssh node01

# confirm
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   44d   v1.34.3
# node01         Ready    <none>          44d   v1.33.6
# node02         Ready    <none>          44d   v1.33.6
```

---

### Task: fix cluster connection

the command `kubectl get po` return "The connection to the server 192.168.10.150:6443 was refused - did you specify the right host or port?"

---

- Solution
  - detail errer `journalctl -u kubelet --no-pager`

1. Confirm the `kubelet` is running

```sh
sudo systemctl status kubelet

# if not, start kubelet
sudo systemctl daemon-reload
sudo systemctl restart kubelet

```

2. Checkt the manifests to ensure the configurations are correct.

```sh
# check all manifests
ls /etc/kubernetes/manifests/
# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml

# check api server manifest
sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml
# spec:
#   containers:
#   - command:
#     - kube-apiserver
#     - --etcd-servers=https://127.0.0.1:2379

# restart the kubelet whenever manifests updates
sudo systemctl restart kubelet
```

---

### Task: Troubleshooting API server

A kubeadm provisioned cluster was migrated to a new machine. Requires configuration changes to run successfully.

Task:

We need fix a single-node cluster that got broken during machine migration.
Identify the broken cluster components and investigate what caused to break those components.
The decommissioned cluster used an external etcd server.
Next, fix the configuration of all broken cluster components.
Ensure to restart all necessary services and components for changes to take effect.
Finally, ensure the cluster, single node and all pods are Ready.

- setup env

```sh
vi /etc/kubernetes/manifests/kube-apiserver.yaml
#    - --etcd-servers=https://128.0.0.1:2379
```

---

- Solution
  - analyze: "Used an external etcd server." is a hint
  - issue could be caused by etcd server configuration

```sh
# confirm issue
k get node
# The connection to the server 192.168.10.150:6443 was refused - did you specify the right host or port?

# debug
journalctl -u kubelet --no-pager | tail -n 60
# Jan 15 14:11:13 controlplane kubelet[1233]: E0115 14:11:13.207487    1233 event.go:368] "Unable to write event (may retry after sleeping)" err="Patch \"https://192.168.10.150:6443/api/v1/namespaces/kube-system/events/kube-scheduler-controlplane.188af5f3415b8a3d\": dial tcp 192.168.10.150:6443: connect: connection refused" event="&Event{ObjectMeta:{kube-scheduler-controlplane.188af5f3415b8a3d  kube-system   2157 0 0001-01-01 00:00:00 +0000 UTC <nil> <nil> map[] map[] [] [] []},InvolvedObject:ObjectReference{Kind:Pod,Namespace:kube-system,Name:kube-scheduler-controlplane,UID:03251309c465d6762648423f73e80586,APIVersion:v1,ResourceVersion:,FieldPath:spec.containers{kube-scheduler},},Reason:Unhealthy,Message:Readiness probe failed: Get \"https://127.0.0.1:10259/readyz\": dial tcp 127.0.0.1:10259: connect: connection refused,Source:EventSource{Component:kubelet,Host:controlplane,},FirstTimestamp:2026-01-15 11:57:08 -0500 EST,LastTimestamp:2026-01-15 14:06:44.094794979 -0500 EST m=+7337.020981358,Count:25,Type:Warning,EventTime:0001-01-01 00:00:00 +0000 UTC,Series:nil,Action:,Related:nil,ReportingController:kubelet,ReportingInstance:controlplane,}"
# Jan 15 14:11:18 controlplane kubelet[1233]: E0115 14:11:18.155764    1233 kubelet_node_status.go:548] "Error updating node status, will retry" err="failed to patch status \"{\\\"status\\\":{\\\"$setElementOrder/conditions\\\":[{\\\"type\\\":\\\"NetworkUnavailable\\\"},{\\\"type\\\":\\\"MemoryPressure\\\"},{\\\"type\\\":\\\"DiskPressure\\\"},{\\\"type\\\":\\\"PIDPressure\\\"},{\\\"type\\\":\\\"Ready\\\"}],\\\"conditions\\\":[{\\\"lastHeartbeatTime\\\":\\\"2026-01-15T19:11:18Z\\\",\\\"type\\\":\\\"MemoryPressure\\\"},{\\\"lastHeartbeatTime\\\":\\\"2026-01-15T19:11:18Z\\\",\\\"type\\\":\\\"DiskPressure\\\"},{\\\"lastHeartbeatTime\\\":\\\"2026-01-15T19:11:18Z\\\",\\\"type\\\":\\\"PIDPressure\\\"},{\\\"lastHeartbeatTime\\\":\\\"2026-01-15T19:11:18Z\\\",\\\"type\\\":\\\"Ready\\\"}]}}\" for node \"controlplane\": Patch \"https://192.168.10.150:6443/api/v1/nodes/controlplane/status?timeout=10s\": dial tcp 192.168.10.150:6443: connect: connection refused"
# Jan 15 14:11:18 controlplane kubelet[1233]: E0115 14:11:18.156328    1233 kubelet_node_status.go:548] "Error updating node status, will retry" err="error getting node \"controlplane\": Get \"https://192.168.10.150:6443/api/v1/nodes/controlplane?timeout=10s\": dial tcp 192.168.10.150:6443: connect: connection refused"
# Jan 15 14:11:18 controlplane kubelet[1233]: E0115 14:11:18.157119    1233 kubelet_node_status.go:548] "Error updating node status, will retry" err="error getting node \"controlplane\": Get \"https://192.168.10.150:6443/api/v1/nodes/controlplane?timeout=10s\": dial tcp 192.168.10.150:6443: connect: connection refused"
# Jan 15 14:11:18 controlplane kubelet[1233]: E0115 14:11:18.157450    1233 kubelet_node_status.go:548] "Error updating node status, will retry" err="error getting node \"controlplane\": Get \"https://192.168.10.150:6443/api/v1/nodes/controlplane?timeout=10s\": dial tcp 192.168.10.150:6443: connect: connection refused"
# Jan 15 14:11:18 controlplane kubelet[1233]: E0115 14:11:18.157743    1233 kubelet_node_status.go:548] "Error updating node status, will retry" err="error getting node \"controlplane\": Get \"https://192.168.10.150:6443/api/v1/nodes/controlplane?timeout=10s\": dial tcp 192.168.10.150:6443: connect: connection refused"
# Jan 15 14:11:18 controlplane kubelet[1233]: E0115 14:11:18.157760    1233 kubelet_node_status.go:535] "Unable to update node status" err="update node status exceeds retry count"

# check the api server cf
vi /etc/kubernetes/manifest/kube-apiserver.yaml
# check:
#    - --etcd-servers=https://128.0.0.1:2379
# correct:
#    - --etcd-servers=https://127.0.0.1:2379

# confirm
kubectl get node
# NAME           STATUS   ROLES           AGE     VERSION
# controlplane   Ready    control-plane   2d19h   v1.32.11
# node01         Ready    <none>          12h     v1.32.11
# node02         Ready    <none>          12h     v1.32.11
```

> Common Issue:
>
> - etcd connection error:
>   - If the api uses internal etcd, check the api server manifest.
>   - If the api uses external etcd, `kubectl get pod api-server -o yaml` to get the etcd ip and confirm it is correct.
>     - curl -k https://ip:2379/readyz
> - pod status keep `Pending`:
>   - `/etc/kubernetes/manifests/kube-scheduler.yaml`: check ip
> - deployment/sts can created but pod cannot create:
>   - scheduler manager error: check the bind-address

---

## Scheduling

### Task: Node selector

1. create a pod named noded that uses the nginx image
2. ensure the pod is scheduled to the a node labeled disk=nvme

- setup env

```sh
k label node node02 disk=nvme --overwrite
```

---

- Solution

```yaml
# task-nodeselector.yaml
apiVersion: v1
kind: Pod
metadata:
  name: noded
spec:
  containers:
    - name: nginx
      image: nginx
      imagePullPolicy: IfNotPresent
  nodeSelector:
    disk: nvme
```

```sh
k get node -L disk
# NAME           STATUS   ROLES           AGE   VERSION   DISK
# controlplane   Ready    control-plane   46d   v1.34.3
# node01         Ready    <none>          46d   v1.33.6
# node02         Ready    <none>          46d   v1.33.6   nvme

k apply -f task-nodeselector.yaml
# pod/nginx created

 kubectl get pod nginx -o wide
# NAME    READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
# nginx   1/1     Running   0          30s   10.244.2.183   node02   <none>           <none>
```

---

### Task: node selector

Task
按如下要求调度一个 pod：
名称：nginx-kusc00401
Image：nginx
Node selector：disktype=ssd

---

- Solution

```sh
# ##############################
# Collect Info
# ##############################
kubectl get node --show-labels
# NAME           STATUS   ROLES           AGE   VERSION   LABELS
# controlplane   Ready    control-plane   42d   v1.33.6   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=controlplane,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=,node.kubernetes.io/exclude-from-external-load-balancers=
# node01         Ready    <none>          42d   v1.33.6   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux
# node02         Ready    <none>          42d   v1.33.6   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,disk=ssd,kubernetes.io/arch=amd64,kubernetes.io/hostname=node02,kubernetes.io/os=linux,node-role=front-end,ssd=

# add node label
kubectl label node node02 disktype=ssd
# node/node02 labeled

# confirm
kubectl get node -l disktype=ssd
# NAME     STATUS   ROLES    AGE   VERSION
# node02   Ready    <none>   42d   v1.33.6

kubectl run nginx-kusc00401 --image=nginx --dry-run=client -o yaml > nodeSelector-pod.yaml

vi nodeSelector-pod.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   name: nginx-kusc00401
# spec:
#   nodeSelector:
#     disktype: ssd
#   containers:
#   - name: nginx
#     image: nginx

# create pod
kubectl apply -f nodeSelector-pod.yaml
# pod/nginx-kusc00401 created

# confirm
kubectl get pod nginx-kusc00401 -o wide
# NAME              READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# nginx-kusc00401   1/1     Running   0          81s   10.244.2.85   node02   <none>           <none>
```

---

### Task: Taints and Tolerations

On node node-1, add a taint so that no normal pods can schedule there.
Then schedule a Pod on that node by adding the appropriate toleration to the Pod spec (and ensure it actually lands on node-2).

---

- Solution

- Taints

```sh
kubectl describe node node01 | grep Taints
# Taints:             <none>

kubectl taint nodes node01 process=gpu:NoSchedule
# node/node01 tainted

kubectl describe node node01 | grep Taints
# Taints:             process=gpu:NoSchedule

kubectl run web --image=nginx --dry-run=client -o yaml > toleration-pod.yaml

vi toleration-pod.yaml
# apiVersion: v1
# kind: Pod
# matadata:
#   name: web
# spec:
#   tolerations:
#   - key: "process"
#     operator: "Equal"
#     value: "gpu"
#     effect: "NoSchedule"
#   containers:
#   - image: nginx
#     name: web

kubectl apply -f toleration-pod.yaml
# pod/web created

kubectl get pod web -o wide
# NAME   READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
# web    1/1     Running   0          3m53s   10.244.2.132   node02   <none>           <none>
```

---

### Task: Taints

CKA EXAM OBJECTIVE: Troubleshoot clusters and nodes
TASK:

1. Inspect the nodes controlplane and node01 for any taints they have. Write the results to their respective files:
2. controller /opt/cka/answers/controller.taint
3. node01 /opt/cka/answers/node-1.taint

---

- Solution

```sh
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   46d   v1.34.3
# node01         Ready    <none>          46d   v1.33.6
# node02         Ready    <none>          46d   v1.33.6

kubectl describe node controlplane | grep -i Taints
# Taints:             node-role.kubernetes.io/control-plane:NoSchedule

kubectl describe node node01 | grep -i Taints
# Taints:             process=gpu:NoSchedule
```

---

### Task: available node

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
检查有多少 nodes 已准备就绪（不包括被打上 Taint：NoSchedule 的节点），
并将数量写入 /opt/KUSC00402/kusc00402.txtCopy

---

- Configure Environment

```sh
kubectl taint node node01 app=db:NoSchedule
# node/node01 tainted

# confirm
kubectl describe node node01 | grep Taints
# Taints:             app=db:NoSchedule
```

- Solution

```sh
kubectl describe node | grep Taints
# Taints:             node-role.kubernetes.io/control-plane:NoSchedule
# Taints:             app=db:NoSchedule
# Taints:             <none>

kubectl describe node | grep Taints | grep -vc NoSchedule > /opt/KUSC00402/kusc00402.txt
# 1

# confirm
cat /opt/KUSC00402/kusc00402.txt
```

---

### Task: Cordon

设置配置环境：
[candidate@node-1] $ kubectl config use-context ek8s

Task
将名为 node02 的 node 设置为不可用，并重新调度该 node 上所有运行的 pods。Copy

---

- Setup Exam environment

```sh
kubectl create deploy web --image=nginx --replicas=6
```

---

- Answer

```sh
# info: node
kubectl get node -o wide
# NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
# controlplane   Ready    control-plane   44d   v1.34.3   192.168.10.150   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node01         Ready    <none>          44d   v1.33.6   192.168.10.151   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node02         Ready    <none>          44d   v1.33.6   192.168.10.152   <none>        Ubuntu 24.04.3 LTS   6.14.0-36-generic   containerd://1.7.28

# info: pods
kubectl get pod -o wide
# NAME                   READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
# csi-hostpathplugin-0   8/8     Running   0          9m23s   10.244.2.117   node02   <none>           <none>
# web-64c966cf88-5h65m   1/1     Running   0          27s     10.244.1.102   node01   <none>           <none>
# web-64c966cf88-9vb5l   1/1     Running   0          27s     10.244.2.130   node02   <none>           <none>
# web-64c966cf88-gbvbp   1/1     Running   0          27s     10.244.2.128   node02   <none>           <none>
# web-64c966cf88-k5xwd   1/1     Running   0          27s     10.244.1.103   node01   <none>           <none>
# web-64c966cf88-mhrsr   1/1     Running   0          27s     10.244.1.104   node01   <none>           <none>
# web-64c966cf88-sfhmv   1/1     Running   0          27s     10.244.2.129   node02   <none>           <none>

# cordon a node
kubectl cordon node02
# node/node02 cordoned

# drain workload
kubectl drain node02 --ignore-daemonsets --delete-emptydir-data --force
# node/node02 already cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-xpvg6, kube-system/kube-proxy-sx5wr
# evicting pod tigera-operator/tigera-operator-7d4578d8d-8vf9w
# evicting pod ing-internal/hello-5f8f7fff68-82dwv
# evicting pod default/web-64c966cf88-sfhmv
# evicting pod default/web-64c966cf88-9vb5l
# evicting pod db/mongo-689485f9f7-ld59l
# evicting pod default/csi-hostpathplugin-0
# evicting pod default/web-64c966cf88-gbvbp
# I0108 22:38:00.684453  171955 request.go:752] "Waited before sending request" delay="1.002110385s" reason="client-side throttling, not priority and fairness" verb="GET" URL="https://192.168.10.150:6443/api/v1/namespaces/tigera-operator/pods/tigera-operator-7d4578d8d-8vf9w"
# pod/tigera-operator-7d4578d8d-8vf9w evicted
# pod/web-64c966cf88-gbvbp evicted
# pod/web-64c966cf88-sfhmv evicted
# pod/web-64c966cf88-9vb5l evicted
# pod/mongo-689485f9f7-ld59l evicted
# pod/hello-5f8f7fff68-82dwv evicted
# pod/csi-hostpathplugin-0 evicted
# node/node02 drained

# verify
kubectl get node
# NAME           STATUS                     ROLES           AGE   VERSION
# controlplane   Ready                      control-plane   44d   v1.34.3
# node01         Ready                      <none>          44d   v1.33.6
# node02         Ready,SchedulingDisabled   <none>          44d   v1.33.6

kubectl get pod | grep node02
# NAME                   READY   STATUS              RESTARTS   AGE    IP             NODE     NOMINATED NODE   READINESS GATES
# csi-hostpathplugin-0   0/8     ContainerCreating   0          48s    <none>         node01   <none>           <none>
# web-64c966cf88-5h65m   1/1     Running             0          103s   10.244.1.102   node01   <none>           <none>
# web-64c966cf88-8jh54   1/1     Running             0          55s    10.244.1.108   node01   <none>           <none>
# web-64c966cf88-9nsj9   1/1     Running             0          56s    10.244.1.106   node01   <none>           <none>
# web-64c966cf88-jw42h   1/1     Running             0          55s    10.244.1.107   node01   <none>           <none>
# web-64c966cf88-k5xwd   1/1     Running             0          103s   10.244.1.103   node01   <none>           <none>
# web-64c966cf88-mhrsr   1/1     Running             0          103s   10.244.1.104   node01   <none>           <none>
```

---
