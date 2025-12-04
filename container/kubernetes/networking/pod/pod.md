# k8s - Pod networking

[Back](../../index.md)

---

## Pod Networking

- Pod Networking Model

  - every pod should have an **IP address**
  - every pod should be able to **communicate** with other pod **in the same node**
  - each pod can communicate with other pod on **other nodes without NAT**.

- common solution:
  - flanel
  - cilium
  - nsx

---

- Step1: assign ip and enable communication in the same node

- Lan(192.168.1.0)
  - node01, 192.168.1.11
    - bridge network interface, `v-net-0`
    - subnet, 10.244.1.0/24
    - container run:
      - create and attach virtual swith
      - assign contianer ip
      - set container route
      - =>: each node has ip, and can communicate via virtual switch

---

- Step2: enable node01 talk to node02

  - Lan(192.168.1.0)

    - node01, 192.168.1.11
      - subnet, 10.244.1.0/24
      - v-switch: 10.244.1.1
      - pod01: 10.244.1.2
      - pod02: 10.244.1.3
    - node02, 192.168.1.12
      - v-switch: 10.244.2.1
      - pod01: 10.244.2.2

  - setup a default gateway for each node: 10.244.0.0/16 and manage a central routing table.

---

- All the above are manage by CNI automatically

---

## CNI in K8s

- defalt path for container runtime to find the CNI plugin: `/opt/cni/bin`
- the path to determine which plugin to use: `/etc/cni/net.d`

  - if multiple, choice by order

---

### Solution: `WeaveWork`

- install agent on each node, responsible for:

  - create bridge interface
  - assign IP for each pod
  - manage routing for pods communication
  - manage NAT to forward traffice to another node

- Deploy weave
  - deploy as a daeamonSet
    - a pod act as an agen on each node, implementing CNI

---

## Lab:

- Get the runtime endpoint

```sh
# get conf file from kubelet process
ps -aux | grep -i kubelet | grep config
# bad data in /proc/uptime
# root        3572  0.0  0.1 2988188 83332 ?       Ssl  18:11   0:16 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --pod-infra-container-image=registry.k8s.io/pause:3.10.1

cat /var/lib/kubelet/config.yaml | grep -i containerRuntimeEndpoint
# containerRuntimeEndpoint: unix:///var/run/containerd/containerd.sock
```

- List all CNI binaries

```sh
# all CNI plugin path: /opt/CNI/bin
ls -hl /opt/cni/bin
# total 90M
# -rwxr-xr-x 1 root root 4.5M Dec 11  2024 bandwidth
# -rwxr-xr-x 1 root root 5.1M Dec 11  2024 bridge
# -rwxr-xr-x 1 root root  13M Dec 11  2024 dhcp
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 dummy
# -rwxr-xr-x 1 root root 5.1M Dec 11  2024 firewall
# -rwxr-xr-x 1 root root 2.4M Dec  3 18:11 flannel
# -rwxr-xr-x 1 root root 4.6M Dec 11  2024 host-device
# -rwxr-xr-x 1 root root 3.9M Dec 11  2024 host-local
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 ipvlan
# -rw-r--r-- 1 root root  12K Dec 11  2024 LICENSE
# -rwxr-xr-x 1 root root 4.0M Dec 11  2024 loopback
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 macvlan
# -rwxr-xr-x 1 root root 4.5M Dec 11  2024 portmap
# -rwxr-xr-x 1 root root 4.9M Dec 11  2024 ptp
# -rw-r--r-- 1 root root 2.3K Dec 11  2024 README.md
# -rwxr-xr-x 1 root root 4.2M Dec 11  2024 sbr
# -rwxr-xr-x 1 root root 3.5M Dec 11  2024 static
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 tap
# -rwxr-xr-x 1 root root 4.1M Dec 11  2024 tuning
# -rwxr-xr-x 1 root root 4.7M Dec 11  2024 vlan
# -rwxr-xr-x 1 root root 4.3M Dec 11  2024 vrf

# get the CNI in use
ls -hl /etc/cni/net.d
# total 4.0K
# -rw-r--r-- 1 root root 292 Dec  3 18:12 10-flannel.conflist

# get the binary to be run when a container is created
cat /etc/cni/net.d/10-flannel.conflist
# {
#   "name": "cbr0",
#   "cniVersion": "0.3.1",
#   "plugins": [
#     {
#       "type": "flannel",
#       "delegate": {
#         "hairpinMode": true,
#         "isDefaultGateway": true
#       }
#     },
#     {
#       "type": "portmap",
#       "capabilities": {
#         "portMappings": true
#       }
#     }
#   ]
# }

```

---

## IP Address Mangement(IPAM)

- `IP Address Mangement(IPAM)`

  - a method and software for planning, tracking, and managing a network's Internet Protocol (IP) addresses.

- CNI built-in plugin for IPAM
  - `DHCP`
  - `host-local`
- Can be configure within the conf file of the CNI
  - `ipam` field

### Lab: Flannel

```sh
# get the flannel daemonSet
kubectl get daemonset -A
# NAMESPACE      NAME              DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-flannel   kube-flannel-ds   1         1         1       1            1           <none>                   18m
# kube-system    kube-proxy        1         1         1       1            1           kubernetes.io/os=linux   18m

# delete flannel
kubectl delete daemonset -n kube-flannel kube-flannel-ds
# daemonset.apps "kube-flannel-ds" deleted from kube-flannel namespace

# get the flannel configMap
kubectl get configmap -n kube-flannel
# NAME               DATA   AGE
# kube-flannel-cfg   2      20m
# kube-root-ca.crt   1      20m

# delete flannel configmap
kubectl delete configmap -n kube-flannel kube-flannel-cfg
# configmap "kube-flannel-cfg" deleted from kube-flannel namespace

# list flannel conf file
ls /etc/cni/net.d/  # verify files
# 10-flannel.conflist
sudo rm -rf /etc/cni/net.d/*
```
- Install Calico CNI
  - ref: https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart

```sh
# Install Calico
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/tigera-operator.yaml
# namespace/tigera-operator created
# serviceaccount/tigera-operator created
# clusterrole.rbac.authorization.k8s.io/tigera-operator-secrets created
# clusterrole.rbac.authorization.k8s.io/tigera-operator created
# clusterrolebinding.rbac.authorization.k8s.io/tigera-operator created
# rolebinding.rbac.authorization.k8s.io/tigera-operator-secrets created
# deployment.apps/tigera-operator created
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "Installation" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "APIServer" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "Goldmane" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
# resource mapping not found for name: "default" namespace: "" from "https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml": no matches for kind "Whisker" in version "operator.tigera.io/v1"
# ensure CRDs are installed first
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.2/manifests/custom-resources.yaml
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
```

