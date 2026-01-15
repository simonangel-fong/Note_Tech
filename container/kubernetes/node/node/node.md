# Kubernetes: Node

[Back](../../index.md)

- [Kubernetes: Node](#kubernetes-node)
  - [Node](#node)
    - [Imperative Command](#imperative-command)
  - [Lab: Join a Node into a Cluster](#lab-join-a-node-into-a-cluster)
  - [Lab: Node Info](#lab-node-info)
    - [Master Node Info](#master-node-info)
    - [Worker Node Info](#worker-node-info)

---

## Node

### Imperative Command

| Command                                                              | Description                                            |
| -------------------------------------------------------------------- | ------------------------------------------------------ |
| `kubectl get nodes`                                                  | List all nodes in the cluster                          |
| `kubectl describe node node_name`                                    | Show detailed information about a node                 |
| `kubectl top node node_name`                                         | Display resource usage (CPU, memory) of a node         |
| `kubectl cordon node_name`                                           | Mark a node as **unschedulable**                       |
| `kubectl uncordon node_name`                                         | Mark a node as schedulable again                       |
| `kubectl drain node_name --ignore-daemonsets --delete-emptydir-data` | Safely **evict Pods** from a node                      |
| `kubectl label node node_name key=value`                             | Add or update a label on a node                        |
| `kubectl taint nodes node_name key=value:NoSchedule`                 | Apply a taint to **prevent Pods** from being scheduled |
| `kubectl taint nodes node_name key:NoSchedule-`                      | Remove a taint from a node                             |
| `kubectl delete node node_name`                                      | Remove a node object from the cluster                  |

---

## Lab: Join a Node into a Cluster

- Controlplane

```sh
kubectl get node
# NAME           STATUS   ROLES           AGE    VERSION
# controlplane   Ready    control-plane   2d5h   v1.32.11

kubeadm token create --print-join-command
# kubeadm join 192.168.10.150:6443 --token tgy7dp.da167gnv**** --discovery-token-ca-cert-hash sha256:6338358a5a35659fdbf0d2d91cf04889***
```

- SSH node01

```sh
sudo kubeadm join 192.168.10.150:6443 --token tgy7dp.da167gnv**** --discovery-token-ca-cert-hash sha256:6338358a5a35659fdbf0d2d91cf04889***
# [preflight] Running pre-flight checks
# [preflight] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [preflight] Use 'kubeadm init phase upload-config --config your-config.yaml' to re-upload it.
# [kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
# [kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
# [kubelet-start] Starting the kubelet
# [kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
# [kubelet-check] The kubelet is healthy after 1.025918679s
# [kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap

# This node has joined the cluster:
# * Certificate signing request was sent to apiserver and a response was received.
# * The Kubelet was informed of the new secure connection details.

# Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

- Controlplane

```sh
kubectl get node
# NAME           STATUS   ROLES           AGE    VERSION
# controlplane   Ready    control-plane   2d5h   v1.32.11
# node01         Ready    <none>          105s   v1.32.11
```

---

## Lab: Node Info

### Master Node Info

```sh
kubectl get nodes
# NAME           STATUS   ROLES           AGE    VERSION
# controlplane   Ready    control-plane   2d5h   v1.32.11
# node01         Ready    <none>          3m9s   v1.32.11

kubectl describe node controlplane
# Name:               controlplane
# Roles:              control-plane
# Labels:             beta.kubernetes.io/arch=amd64
#                     beta.kubernetes.io/os=linux
#                     kubernetes.io/arch=amd64
#                     kubernetes.io/hostname=controlplane
#                     kubernetes.io/os=linux
#                     node-role.kubernetes.io/control-plane=
#                     node.kubernetes.io/exclude-from-external-load-balancers=
# Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"b2:0e:14:f4:05:6d"}
#                     flannel.alpha.coreos.com/backend-type: vxlan
#                     flannel.alpha.coreos.com/kube-subnet-manager: true
#                     flannel.alpha.coreos.com/public-ip: 192.168.10.150
#                     kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
#                     node.alpha.kubernetes.io/ttl: 0
#                     volumes.kubernetes.io/controller-managed-attach-detach: true
# CreationTimestamp:  Mon, 12 Jan 2026 19:08:57 -0500
# Taints:             node-role.kubernetes.io/control-plane:NoSchedule
# Unschedulable:      false
# Lease:
#   HolderIdentity:  controlplane
#   AcquireTime:     <unset>
#   RenewTime:       Thu, 15 Jan 2026 00:58:38 -0500
# Conditions:
#   Type                 Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
#   ----                 ------  -----------------                 ------------------                ------                       -------
#   NetworkUnavailable   False   Wed, 14 Jan 2026 23:59:41 -0500   Wed, 14 Jan 2026 23:59:41 -0500   FlannelIsUp                  Flannel is running on this node
#   MemoryPressure       False   Thu, 15 Jan 2026 00:55:44 -0500   Mon, 12 Jan 2026 19:08:57 -0500   KubeletHasSufficientMemory   kubelet has sufficient memory available
#   DiskPressure         False   Thu, 15 Jan 2026 00:55:44 -0500   Mon, 12 Jan 2026 19:08:57 -0500   KubeletHasNoDiskPressure     kubelet has no disk pressure
#   PIDPressure          False   Thu, 15 Jan 2026 00:55:44 -0500   Mon, 12 Jan 2026 19:08:57 -0500   KubeletHasSufficientPID      kubelet has sufficient PID available
#   Ready                True    Thu, 15 Jan 2026 00:55:44 -0500   Mon, 12 Jan 2026 19:09:57 -0500   KubeletReady                 kubelet is posting ready status
# Addresses:
#   InternalIP:  192.168.10.150
#   Hostname:    controlplane
# Capacity:
#   cpu:                4
#   ephemeral-storage:  30784420Ki
#   hugepages-1Gi:      0
#   hugepages-2Mi:      0
#   memory:             3960428Ki
#   pods:               110
# Allocatable:
#   cpu:                4
#   ephemeral-storage:  28370921426
#   hugepages-1Gi:      0
#   hugepages-2Mi:      0
#   memory:             3858028Ki
#   pods:               110
# System Info:
#   Machine ID:                 b972f5c0ff56412b8ac4ea330e0dc501
#   System UUID:                b44c4d56-68c1-34e9-b050-95dd2881e109
#   Boot ID:                    7d8acd8f-9d11-4de2-bced-9512fa2bb391
#   Kernel Version:             6.14.0-37-generic
#   OS Image:                   Ubuntu 24.04.3 LTS
#   Operating System:           linux
#   Architecture:               amd64
#   Container Runtime Version:  containerd://1.7.28
#   Kubelet Version:            v1.32.11
#   Kube-Proxy Version:         v1.32.11
# PodCIDR:                      10.244.0.0/24
# PodCIDRs:                     10.244.0.0/24
# Non-terminated Pods:          (8 in total)
#   Namespace                   Name                                    CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
#   ---------                   ----                                    ------------  ----------  ---------------  -------------  ---
#   kube-flannel                kube-flannel-ds-jwtcj                   100m (2%)     0 (0%)      50Mi (1%)        0 (0%)         2d5h
#   kube-system                 coredns-668d6bf9bc-4sxd6                100m (2%)     0 (0%)      70Mi (1%)        170Mi (4%)     2d5h
#   kube-system                 coredns-668d6bf9bc-lw8gs                100m (2%)     0 (0%)      70Mi (1%)        170Mi (4%)     2d5h
#   kube-system                 etcd-controlplane                       100m (2%)     0 (0%)      100Mi (2%)       0 (0%)         2d5h
#   kube-system                 kube-apiserver-controlplane             250m (6%)     0 (0%)      0 (0%)           0 (0%)         2d5h
#   kube-system                 kube-controller-manager-controlplane    200m (5%)     0 (0%)      0 (0%)           0 (0%)         2d5h
#   kube-system                 kube-proxy-pcd6g                        0 (0%)        0 (0%)      0 (0%)           0 (0%)         2d5h
#   kube-system                 kube-scheduler-controlplane             100m (2%)     0 (0%)      0 (0%)           0 (0%)         2d5h
# Allocated resources:
#   (Total limits may be over 100 percent, i.e., overcommitted.)
#   Resource           Requests    Limits
#   --------           --------    ------
#   cpu                950m (23%)  0 (0%)
#   memory             290Mi (7%)  340Mi (9%)
#   ephemeral-storage  0 (0%)      0 (0%)
#   hugepages-1Gi      0 (0%)      0 (0%)
#   hugepages-2Mi      0 (0%)      0 (0%)
# Events:
#   Type     Reason                   Age                  From             Message
#   ----     ------                   ----                 ----             -------
#   Normal   Starting                 2d5h                 kube-proxy
#   Normal   Starting                 59m                  kube-proxy
#   Normal   Starting                 34h                  kube-proxy
#   Normal   NodeAllocatableEnforced  2d5h                 kubelet          Updated Node Allocatable limit across pods
#   Normal   Starting                 2d5h                 kubelet          Starting kubelet.
#   Normal   NodeHasSufficientMemory  2d5h (x8 over 2d5h)  kubelet          Node controlplane status is now: NodeHasSufficientMemory
#   Normal   NodeHasNoDiskPressure    2d5h (x8 over 2d5h)  kubelet          Node controlplane status is now: NodeHasNoDiskPressure
#   Normal   NodeHasSufficientPID     2d5h (x7 over 2d5h)  kubelet          Node controlplane status is now: NodeHasSufficientPID
#   Warning  InvalidDiskCapacity      2d5h                 kubelet          invalid capacity 0 on image filesystem
#   Warning  InvalidDiskCapacity      2d5h                 kubelet          invalid capacity 0 on image filesystem
#   Normal   Starting                 2d5h                 kubelet          Starting kubelet.
#   Normal   NodeAllocatableEnforced  2d5h                 kubelet          Updated Node Allocatable limit across pods
#   Normal   NodeHasSufficientMemory  2d5h                 kubelet          Node controlplane status is now: NodeHasSufficientMemory
#   Normal   NodeHasNoDiskPressure    2d5h                 kubelet          Node controlplane status is now: NodeHasNoDiskPressure
#   Normal   NodeHasSufficientPID     2d5h                 kubelet          Node controlplane status is now: NodeHasSufficientPID
#   Normal   RegisteredNode           2d5h                 node-controller  Node controlplane event: Registered Node controlplane in Controller
#   Normal   NodeReady                2d5h                 kubelet          Node controlplane status is now: NodeReady
#   Normal   Starting                 34h                  kubelet          Starting kubelet.
#   Normal   NodeHasSufficientMemory  34h (x8 over 34h)    kubelet          Node controlplane status is now: NodeHasSufficientMemory
#   Warning  InvalidDiskCapacity      34h                  kubelet          invalid capacity 0 on image filesystem
#   Normal   NodeHasNoDiskPressure    34h (x8 over 34h)    kubelet          Node controlplane status is now: NodeHasNoDiskPressure
#   Normal   NodeHasSufficientPID     34h (x7 over 34h)    kubelet          Node controlplane status is now: NodeHasSufficientPID
#   Normal   NodeAllocatableEnforced  34h                  kubelet          Updated Node Allocatable limit across pods
#   Warning  Rebooted                 34h                  kubelet          Node controlplane has been rebooted, boot id: 3834e1eb-cf51-44a8-8689-fc82acc8dff5
#   Normal   RegisteredNode           34h                  node-controller  Node controlplane event: Registered Node controlplane in Controller
#   Normal   Starting                 59m                  kubelet          Starting kubelet.
#   Warning  InvalidDiskCapacity      59m                  kubelet          invalid capacity 0 on image filesystem
#   Normal   NodeHasSufficientMemory  59m (x8 over 59m)    kubelet          Node controlplane status is now: NodeHasSufficientMemory
#   Normal   NodeHasNoDiskPressure    59m (x8 over 59m)    kubelet          Node controlplane status is now: NodeHasNoDiskPressure
#   Normal   NodeHasSufficientPID     59m (x7 over 59m)    kubelet          Node controlplane status is now: NodeHasSufficientPID
#   Normal   NodeAllocatableEnforced  59m                  kubelet          Updated Node Allocatable limit across pods
#   Warning  Rebooted                 59m                  kubelet          Node controlplane has been rebooted, boot id: 7d8acd8f-9d11-4de2-bced-9512fa2bb391
#   Normal   RegisteredNode           58m                  node-controller  Node controlplane event: Registered Node controlplane in Controller
```

### Worker Node Info

```sh
kubectl describe node node01
# Name:               node01
# Roles:              <none>
# Labels:             beta.kubernetes.io/arch=amd64
#                     beta.kubernetes.io/os=linux
#                     kubernetes.io/arch=amd64
#                     kubernetes.io/hostname=node01
#                     kubernetes.io/os=linux
# Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"82:9f:d2:57:43:88"}
#                     flannel.alpha.coreos.com/backend-type: vxlan
#                     flannel.alpha.coreos.com/kube-subnet-manager: true
#                     flannel.alpha.coreos.com/public-ip: 192.168.10.151
#                     kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
#                     node.alpha.kubernetes.io/ttl: 0
#                     volumes.kubernetes.io/controller-managed-attach-detach: true
# CreationTimestamp:  Thu, 15 Jan 2026 00:55:20 -0500
# Taints:             <none>
# Unschedulable:      false
# Lease:
#   HolderIdentity:  node01
#   AcquireTime:     <unset>
#   RenewTime:       Thu, 15 Jan 2026 01:00:56 -0500
# Conditions:
#   Type                 Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
#   ----                 ------  -----------------                 ------------------                ------                       -------
#   NetworkUnavailable   False   Thu, 15 Jan 2026 00:55:43 -0500   Thu, 15 Jan 2026 00:55:43 -0500   FlannelIsUp                  Flannel is running on this node
#   MemoryPressure       False   Thu, 15 Jan 2026 00:56:21 -0500   Thu, 15 Jan 2026 00:55:19 -0500   KubeletHasSufficientMemory   kubelet has sufficient memory available
#   DiskPressure         False   Thu, 15 Jan 2026 00:56:21 -0500   Thu, 15 Jan 2026 00:55:19 -0500   KubeletHasNoDiskPressure     kubelet has no disk pressure
#   PIDPressure          False   Thu, 15 Jan 2026 00:56:21 -0500   Thu, 15 Jan 2026 00:55:19 -0500   KubeletHasSufficientPID      kubelet has sufficient PID available
#   Ready                True    Thu, 15 Jan 2026 00:56:21 -0500   Thu, 15 Jan 2026 00:55:41 -0500   KubeletReady                 kubelet is posting ready status
# Addresses:
#   InternalIP:  192.168.10.151
#   Hostname:    node01
# Capacity:
#   cpu:                1
#   ephemeral-storage:  30784420Ki
#   hugepages-1Gi:      0
#   hugepages-2Mi:      0
#   memory:             1965460Ki
#   pods:               110
# Allocatable:
#   cpu:                1
#   ephemeral-storage:  28370921426
#   hugepages-1Gi:      0
#   hugepages-2Mi:      0
#   memory:             1863060Ki
#   pods:               110
# System Info:
#   Machine ID:                 b972f5c0ff56412b8ac4ea330e0dc501
#   System UUID:                bc764d56-792c-709d-e23f-e1ef6ef5b90c
#   Boot ID:                    e11d7962-e552-4fce-a01f-a65e58f823c3
#   Kernel Version:             6.14.0-37-generic
#   OS Image:                   Ubuntu 24.04.3 LTS
#   Operating System:           linux
#   Architecture:               amd64
#   Container Runtime Version:  containerd://1.7.28
#   Kubelet Version:            v1.32.11
#   Kube-Proxy Version:         v1.32.11
# PodCIDR:                      10.244.1.0/24
# PodCIDRs:                     10.244.1.0/24
# Non-terminated Pods:          (3 in total)
#   Namespace                   Name                                       CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
#   ---------                   ----                                       ------------  ----------  ---------------  -------------  ---
#   kube-flannel                kube-flannel-ds-kvkxw                      100m (10%)    0 (0%)      50Mi (2%)        0 (0%)         5m45s
#   kube-system                 kube-proxy-4jhbr                           0 (0%)        0 (0%)      0 (0%)           0 (0%)         5m45s
#   local-path-storage          local-path-provisioner-689dd6b546-2cn67    0 (0%)        0 (0%)      0 (0%)           0 (0%)         34h
# Allocated resources:
#   (Total limits may be over 100 percent, i.e., overcommitted.)
#   Resource           Requests    Limits
#   --------           --------    ------
#   cpu                100m (10%)  0 (0%)
#   memory             50Mi (2%)   0 (0%)
#   ephemeral-storage  0 (0%)      0 (0%)
#   hugepages-1Gi      0 (0%)      0 (0%)
#   hugepages-2Mi      0 (0%)      0 (0%)
# Events:
#   Type     Reason                   Age                    From             Message
#   ----     ------                   ----                   ----             -------
#   Normal   Starting                 5m31s                  kube-proxy
#   Normal   Starting                 5m47s                  kubelet          Starting kubelet.
#   Warning  InvalidDiskCapacity      5m46s                  kubelet          invalid capacity 0 on image filesystem
#   Normal   NodeAllocatableEnforced  5m46s                  kubelet          Updated Node Allocatable limit across pods
#   Normal   NodeHasSufficientMemory  5m45s (x8 over 5m46s)  kubelet          Node node01 status is now: NodeHasSufficientMemory
#   Normal   NodeHasNoDiskPressure    5m45s (x8 over 5m46s)  kubelet          Node node01 status is now: NodeHasNoDiskPressure
#   Normal   NodeHasSufficientPID     5m45s (x7 over 5m46s)  kubelet          Node node01 status is now: NodeHasSufficientPID
#   Normal   RegisteredNode           5m42s                  node-controller  Node node01 event: Registered Node node01 in Controller
```

---
