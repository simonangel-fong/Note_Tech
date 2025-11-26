# Kubernetes - Node Cordon

[Back](../../index.md)

- [Kubernetes - Node Cordon](#kubernetes---node-cordon)
  - [Node Cordon](#node-cordon)
  - [Node Drain](#node-drain)
  - [Imperative](#imperative)
  - [Typical maintenance workflow](#typical-maintenance-workflow)
  - [Lab:](#lab)

---

## Node Cordon

- `node cordon`

  - Mark node as unschedulable.
  - no **NEW** Pods can be scheduled onto that node, but existing Pods keep running.
  - Effect
    - **Existing** `Pods` stay.
    - **No new** `Pods` will be scheduled.
    - The `node` remains fully **operational**.

- Use case:
  - preparing for maintenance but don't want to move existing Pods yet.
  - stop Kubernetes from placing new workloads on the node.

---

- `node uncordon`

  - Uncordoning re-enables scheduling on a previously cordoned/drained node.
  - Effects
    - `Node` becomes **schedulable** again.
    - **New** Pods can be **placed** on it.
    - It returns to **normal operation**.

---

## Node Drain

- `Node Drain`

  - **evicts** (safely removes) all Pods and **marks** the node **unschedulable**.
  - Effects
    - Existing Pods are moved out.
    - No new Pods scheduled.
    - Safe for maintenance.

- Use case:
  - need to do maintenance (patching, reboot, updates).
  - want Pods moved to other nodes automatically.

---

## Imperative

| **Command**                                           | **Description**                                                                           |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `kubectl cordon node_name`                            | Marks the node as **unschedulable**.                                                      |
| `kubectl uncordon node_name`                          | Marks the node as **schedulable** again.                                                  |
| `kubectl drain node_name --force`                     | Forces eviction of standalone Pods.                                                       |
| `kubectl drain node_name --delete-emptydir-data`      | Drain but also removes Pods with `emptyDir` volumes                                       |
| `kubectl drain node_name --ignore-daemonsets`         | Required because DaemonSet Pods **cannot be evicted**; tells Kubernetes to skip them.     |
| `kubectl drain node_name --ignore-daemonsets --force` | Safely **evicts all Pods** (except `DaemonSets`) and marks the node as **unschedulable**. |

- DaemonSet Pods

  - Drain will fail unless:
    - `kubectl drain node_name --ignore-daemonsets`

- Pods using local storage (emptyDir)

  - Drain can fail unless allow deleting them:
    - `kubectl drain node_name --delete-emptydir-data`

- Standalone Pods (no controller)

  - Drain refuses to delete them by default.
  - must force it: `kubectl drain node_name --force`

- Daily use:
  - `kubectl drain node_name --ignore-daemonsets --delete-emptydir-data --force`

---

## Typical maintenance workflow

```sh
#  move workloads away:
kubectl drain node_name --ignore-daemonsets --force --delete-emptydir-data

# Do maintenance (reboot, patch OS, upgrade kubelet, etc.)

# Bring node back:
kubectl uncordon node_name
```

---

## Lab:

```sh
# confirm current schedulability
kubectl describe node node01 | grep unschedulable:
# Unschedulable:      false

# try to empty the node
kubectl drain node01
# error: unable to drain node "node01" due to error: cannot delete DaemonSet-managed Pods (use --ignore-daemonsets to ignore): kube-flannel/kube-flannel-ds-rk729, kube-system/kube-proxy-nw7vt, continuing command...
# There are pending nodes to be drained:
#  node01
# cannot delete DaemonSet-managed Pods (use --ignore-daemonsets to ignore): kube-flannel/kube-flannel-ds-rk729, kube-system/kube-proxy-nw7vt

# empty the node except the daemonset
kubectl drain node01 --ignore-daemonsets
# node/node01 already cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-rk729, kube-system/kube-proxy-nw7vt
# evicting pod default/blue-759779556-tsbt9
# evicting pod default/blue-759779556-c9qzt
# pod/blue-759779556-tsbt9 evicted
# pod/blue-759779556-c9qzt evicted
# node/node01 drained

# confirm cordon
kubectl describe node node01 | grep schedulable
# Taints:             node.kubernetes.io/unschedulable:NoSchedule
# Unschedulable:      true
```

- Uncordon

```sh
# confirm cordon
kubectl describe node node01 | grep schedulable
# Taints:             node.kubernetes.io/unschedulable:NoSchedule
# Unschedulable:      true

kubectl uncordon node01
# node/node01 uncordoned

kubectl describe node node01 | grep schedulable
# Unschedulable:      false
```
