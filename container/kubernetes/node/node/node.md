# Kubernetes - Node

[Back](../../index.md)

- [Kubernetes - Node](#kubernetes---node)
  - [Node](#node)
  - [Imperative Command](#imperative-command)
  - [Lab: Node info](#lab-node-info)
  - [Label a node and Node Selector](#label-a-node-and-node-selector)

---

## Node

## Imperative Command

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

## Lab: Node info

```sh
kubectl get nodes
# NAME             STATUS   ROLES           AGE    VERSION
# docker-desktop   Ready    control-plane   5d9h   v1.32.2

kubectl describe node docker-desktop
# Name:               docker-desktop
# Roles:              control-plane
# Labels:             beta.kubernetes.io/arch=amd64
#                     beta.kubernetes.io/os=linux
#                     kubernetes.io/arch=amd64
#                     kubernetes.io/hostname=docker-desktop
#                     kubernetes.io/os=linux
#                     node-role.kubernetes.io/control-plane=
#                     node.kubernetes.io/exclude-from-external-load-balancers=
# Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/cri-dockerd.sock
#                     node.alpha.kubernetes.io/ttl: 0
#                     volumes.kubernetes.io/controller-managed-attach-detach: true
# CreationTimestamp:  Wed, 24 Sep 2025 22:21:51 -0400
# Taints:             <none>
# Unschedulable:      false
# Lease:
#   HolderIdentity:  docker-desktop
#   AcquireTime:     <unset>
#   RenewTime:       Tue, 30 Sep 2025 07:40:14 -0400
# Conditions:
#   Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
#   ----             ------  -----------------                 ------------------                ------                       -------
#   MemoryPressure   False   Tue, 30 Sep 2025 07:40:10 -0400   Wed, 24 Sep 2025 22:21:50 -0400   KubeletHasSufficientMemory   kubelet has sufficient memory available
#   DiskPressure     False   Tue, 30 Sep 2025 07:40:10 -0400   Wed, 24 Sep 2025 22:21:50 -0400   KubeletHasNoDiskPressure     kubelet has no disk pressure
#   PIDPressure      False   Tue, 30 Sep 2025 07:40:10 -0400   Wed, 24 Sep 2025 22:21:50 -0400   KubeletHasSufficientPID      kubelet has sufficient PID available
#   Ready            True    Tue, 30 Sep 2025 07:40:10 -0400   Wed, 24 Sep 2025 22:21:52 -0400   KubeletReady                 kubelet is posting ready status
# Addresses:
#   InternalIP:  192.168.65.3
#   Hostname:    docker-desktop
# Capacity:
#   cpu:                12
#   ephemeral-storage:  1055762868Ki
#   hugepages-1Gi:      0
#   hugepages-2Mi:      0
#   memory:             7976124Ki
#   pods:               110
# Allocatable:
#   cpu:                12
#   ephemeral-storage:  972991057538
#   hugepages-1Gi:      0
#   hugepages-2Mi:      0
#   memory:             7873724Ki
#   pods:               110
# System Info:
#   Machine ID:                 a7ccffad-180a-4916-82c8-a5b4ff65df07
#   System UUID:                a7ccffad-180a-4916-82c8-a5b4ff65df07
#   Boot ID:                    089869ee-b212-4b40-84cb-156d3f4777d1
#   Kernel Version:             5.15.153.1-microsoft-standard-WSL2
#   OS Image:                   Docker Desktop
#   Operating System:           linux
#   Architecture:               amd64
#   Container Runtime Version:  docker://28.3.0
#   Kubelet Version:            v1.32.2
#   Kube-Proxy Version:         v1.32.2
# Non-terminated Pods:          (10 in total)
#   Namespace                   Name                                      CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
#   ---------                   ----                                      ------------  ----------  ---------------  -------------  ---
#   default                     nginx                                     0 (0%)        0 (0%)      0 (0%)           0 (0%)         12h
#   kube-system                 coredns-668d6bf9bc-2ztgc                  100m (0%)     0 (0%)      70Mi (0%)        170Mi (2%)     5d9h
#   kube-system                 coredns-668d6bf9bc-sb6nr                  100m (0%)     0 (0%)      70Mi (0%)        170Mi (2%)     5d9h
#   kube-system                 etcd-docker-desktop                       100m (0%)     0 (0%)      100Mi (1%)       0 (0%)         5d9h
#   kube-system                 kube-apiserver-docker-desktop             250m (2%)     0 (0%)      0 (0%)           0 (0%)         5d9h
#   kube-system                 kube-controller-manager-docker-desktop    200m (1%)     0 (0%)      0 (0%)           0 (0%)         5d9h
#   kube-system                 kube-proxy-l9pz4                          0 (0%)        0 (0%)      0 (0%)           0 (0%)         5d9h
#   kube-system                 kube-scheduler-docker-desktop             100m (0%)     0 (0%)      0 (0%)           0 (0%)         5d9h
#   kube-system                 storage-provisioner                       0 (0%)        0 (0%)      0 (0%)           0 (0%)         5d9h
#   kube-system                 vpnkit-controller                         0 (0%)        0 (0%)      0 (0%)           0 (0%)         5d9h
# Allocated resources:
#   (Total limits may be over 100 percent, i.e., overcommitted.)
#   Resource           Requests    Limits
#   --------           --------    ------
#   cpu                850m (7%)   0 (0%)
#   memory             240Mi (3%)  340Mi (4%)
#   ephemeral-storage  0 (0%)      0 (0%)
#   hugepages-1Gi      0 (0%)      0 (0%)
#   hugepages-2Mi      0 (0%)      0 (0%)
# Events:              <none>
```

---

## Label a node and Node Selector

- Label a node

| CMD                                       | DESC                            |
| ----------------------------------------- | ------------------------------- |
| `kubectl label node node_name size=large` | Add or update a label on a node |
| `kubectl label node node_name size-`      | Remove a label from a node      |

- Use Node selector for a pod

```yaml
spec:
  nodeSelector:
    size: large
```
