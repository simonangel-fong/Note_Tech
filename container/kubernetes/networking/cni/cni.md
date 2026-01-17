# Kubernetes Networking: Container Networking Interface(CNI)

[Back](../../index.md)

- [Kubernetes Networking: Container Networking Interface(CNI)](#kubernetes-networking-container-networking-interfacecni)
  - [Container Networking Interface(CNI)](#container-networking-interfacecni)
  - [Calico](#calico)
  - [Lab: Install Calico](#lab-install-calico)

---

## Container Networking Interface(CNI)

- `Container Networking Interface(CNI)`
  - a **standard** that specifies how to **configure network interfaces** for containers.
  - responsibility:
    - The `container runtime` must create **network namespace**
    - identify the **network** to which the container attach
    - invoke `Network Plugin(bridge)` when container is added/deleted
    - assign ip address to the container
    - output netowork configuration
  - common supported runtime:
    - `rkt`
    - `mesos`
    - `k8s`

- Docker does not support `CNI`
  - use Container Network Model(CNM)
  - can work around with manaul work with CNI
    - `docker run --network=none nginx`
    - `bridge add con_id /var/run/netns/con_id`

- `/opt/cni/bin`
  - **defalt path** for container runtime to find the CNI plugin
- `/etc/cni/net.d`
  - the path to determine which plugin to use
  - if multiple, choice by order

---

## Calico

- `Calico`
  - a `Container Network Interface (CNI)` plugin for Kubernetes clusters, **enabling container communication** with high performance and network policy enforcement.

---

## Lab: Install Calico

- ref: https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart

```sh
kubectl get node
# NAME           STATUS     ROLES           AGE     VERSION
# controlplane   NotReady   control-plane   16m     v1.32.11
# node01         NotReady   <none>          5m53s   v1.32.11
# node02         NotReady   <none>          5m25s   v1.32.11

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/operator-crds.yaml
# customresourcedefinition.apiextensions.k8s.io/apiservers.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/gatewayapis.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/goldmanes.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/imagesets.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/installations.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/managementclusterconnections.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/tigerastatuses.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/whiskers.operator.tigera.io created
# customresourcedefinition.apiextensions.k8s.io/bgpconfigurations.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/bgpfilters.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/bgppeers.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/blockaffinities.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/caliconodestatuses.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/clusterinformations.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/felixconfigurations.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/globalnetworkpolicies.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/globalnetworksets.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/hostendpoints.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/ipamblocks.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/ipamconfigs.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/ipamhandles.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/ippools.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/ipreservations.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/kubecontrollersconfigurations.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/networkpolicies.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/networksets.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/stagedglobalnetworkpolicies.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/stagedkubernetesnetworkpolicies.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/stagednetworkpolicies.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/tiers.crd.projectcalico.org created
# customresourcedefinition.apiextensions.k8s.io/adminnetworkpolicies.policy.networking.k8s.io created
# customresourcedefinition.apiextensions.k8s.io/baselineadminnetworkpolicies.policy.networking.k8s.io created

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/tigera-operator.yaml
# namespace/tigera-operator created
# serviceaccount/tigera-operator created
# clusterrole.rbac.authorization.k8s.io/tigera-operator-secrets created
# clusterrole.rbac.authorization.k8s.io/tigera-operator created
# clusterrolebinding.rbac.authorization.k8s.io/tigera-operator created
# rolebinding.rbac.authorization.k8s.io/tigera-operator-secrets created
# deployment.apps/tigera-operator created

# get cluster ip cidr
kubectl cluster-info dump | grep -m 1 cluster-cidr
# "--cluster-cidr=10.244.0.0/16"

# Download the custom resources necessary to configure Calico.
curl -O https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/custom-resources.yaml
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100  1046  100  1046    0     0   3587      0 --:--:-- --:--:-- --:--:--  3594

# update the manifest with the cluster cidr
vi custom-resources.yaml
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
kubectl create -f custom-resources.yaml
# installation.operator.tigera.io/default created
# apiserver.operator.tigera.io/default created
# goldmane.operator.tigera.io/default created
# whisker.operator.tigera.io/default created

# wait until all available
watch kubectl get tigerastatus
# Every 2.0s: kubectl get tigerastatus                        controlplane: Sat Jan 17 00:23:23 2026

# NAME        AVAILABLE   PROGRESSING   DEGRADED   SINCE
# apiserver   True        False         False      59s
# calico      True        False         False      9s
# goldmane    True        False         False      39s
# ippools     True        False         False      2m19s
# whisker     True        False         False      54s

# confirm: node status ready
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   23m   v1.32.11
# node01         Ready    <none>          21m   v1.32.11
# node02         Ready    <none>          20m   v1.32.11
```
