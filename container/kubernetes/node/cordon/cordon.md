# Kubernetes - Node: Cordon & Drain

[Back](../../index.md)

- [Kubernetes - Node: Cordon \& Drain](#kubernetes---node-cordon--drain)
  - [Node Cordon](#node-cordon)
  - [Node Drain](#node-drain)
  - [Typical maintenance workflow](#typical-maintenance-workflow)
  - [Imperative](#imperative)
  - [Lab: Cordon a Node](#lab-cordon-a-node)

---

## Node Cordon

- `node cordon`

  - Mark `node` as **unschedulable**.
  - **NEW** `Pods` **cannot be scheduled** onto that `node`, but existing `Pods` keep running.
  - Effect
    - **Existing** `Pods` stay.
    - **No new** `Pods` will be scheduled.
    - The `node` remains fully **operational**.

- Use case:
  - preparing for **maintenance** but don't want to move existing Pods yet.
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
    - **Existing** Pods are **moved out**.
    - **No new** Pods scheduled.
    - Safe for maintenance.

- Use case:
  - need to do maintenance (patching, reboot, updates).
  - want Pods moved to other nodes automatically.

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

## Imperative

| **Command**                                           | **Description**                                                                           |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `kubectl cordon node_name`                            | Marks the node as **unschedulable**.                                                      |
| `kubectl uncordon node_name`                          | Marks the node as **schedulable** again.                                                  |
| `kubectl drain node_name --force`                     | Forces eviction of standalone Pods.                                                       |
| `kubectl drain node_name --delete-emptydir-data`      | Drain but also removes Pods with `emptyDir` volumes                                       |
| `kubectl drain node_name --ignore-daemonsets`         | Required because DaemonSet Pods **cannot be evicted**; tells Kubernetes to skip them.     |
| `kubectl drain node_name --ignore-daemonsets --force` | Safely **evicts all Pods** (except `DaemonSets`) and marks the node as **unschedulable**. |

- `DaemonSet Pods`

  - Drain will fail unless:
    - `kubectl drain node_name --ignore-daemonsets`

- Pods using **local storage (emptyDir)**

  - Drain can fail unless allow deleting them:
    - `kubectl drain node_name --delete-emptydir-data`

- Standalone Pods (no controller)

  - Drain refuses to delete them by default.
  - must force it: `kubectl drain node_name --force`

- Daily use:
  - `kubectl drain node_name --ignore-daemonsets --delete-emptydir-data --force`

---

## Lab: Cordon a Node

```sh
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   40d   v1.33.6
# node01         Ready    <none>          40d   v1.33.6
# node02         Ready    <none>          40d   v1.33.6

kubectl create deployment web --image=nginx --replicas=10
# deployment.apps/web created

kubectl get pod -o wide
# NAME                   READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# web-65d846d465-25dz5   1/1     Running   0          82s   10.244.1.62   node01   <none>           <none>
# web-65d846d465-5qqf4   1/1     Running   0          82s   10.244.1.64   node01   <none>           <none>
# web-65d846d465-6x7gw   1/1     Running   0          82s   10.244.2.37   node02   <none>           <none>
# web-65d846d465-9xrpg   1/1     Running   0          82s   10.244.2.40   node02   <none>           <none>
# web-65d846d465-ldc4k   1/1     Running   0          82s   10.244.1.63   node01   <none>           <none>
# web-65d846d465-lsfnl   1/1     Running   0          82s   10.244.2.36   node02   <none>           <none>
# web-65d846d465-ng8mc   1/1     Running   0          82s   10.244.2.39   node02   <none>           <none>
# web-65d846d465-qgknq   1/1     Running   0          82s   10.244.1.65   node01   <none>           <none>
# web-65d846d465-snvlr   1/1     Running   0          82s   10.244.1.66   node01   <none>           <none>
# web-65d846d465-xmdfv   1/1     Running   0          82s   10.244.2.38   node02   <none>           <none>
```

- Create Deploy

```sh
kubectl create deploy web --image=nginx --replicas=10
# deployment.apps/web created

kubectl get pod -o wide
# NAME                   READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# web-65d846d465-29wtp   1/1     Running   0          15m   10.244.2.41   node02   <none>           <none>
# web-65d846d465-5cj67   1/1     Running   0          15m   10.244.1.70   node01   <none>           <none>
# web-65d846d465-6cgbd   1/1     Running   0          15m   10.244.1.69   node01   <none>           <none>
# web-65d846d465-6ljsx   1/1     Running   0          15m   10.244.2.44   node02   <none>           <none>
# web-65d846d465-c6q28   1/1     Running   0          15m   10.244.1.67   node01   <none>           <none>
# web-65d846d465-nlskz   1/1     Running   0          15m   10.244.2.45   node02   <none>           <none>
# web-65d846d465-pcqx6   1/1     Running   0          15m   10.244.2.42   node02   <none>           <none>
# web-65d846d465-qzqbr   1/1     Running   0          15m   10.244.1.68   node01   <none>           <none>
# web-65d846d465-vzhsx   1/1     Running   0          15m   10.244.2.43   node02   <none>           <none>
# web-65d846d465-xlmcm   1/1     Running   0          15m   10.244.1.71   node01   <none>           <none>

kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName
# NAME                   NODE
# web-65d846d465-29wtp   node02
# web-65d846d465-5cj67   node01
# web-65d846d465-6cgbd   node01
# web-65d846d465-6ljsx   node02
# web-65d846d465-c6q28   node01
# web-65d846d465-nlskz   node02
# web-65d846d465-pcqx6   node02
# web-65d846d465-qzqbr   node01
# web-65d846d465-vzhsx   node02
# web-65d846d465-xlmcm   node01
```

- Add Cordon

```sh
kubectl cordon node02
# node/node02 cordoned

# confirm
kubectl describe node node02 | grep unschedulable:
# Taints:             node.kubernetes.io/unschedulable:NoSchedule

kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName
# NAME                   NODE
# web-65d846d465-29wtp   node02
# web-65d846d465-5cj67   node01
# web-65d846d465-6cgbd   node01
# web-65d846d465-6ljsx   node02
# web-65d846d465-c6q28   node01
# web-65d846d465-nlskz   node02
# web-65d846d465-pcqx6   node02
# web-65d846d465-qzqbr   node01
# web-65d846d465-vzhsx   node02
# web-65d846d465-xlmcm   node01
```

- Drain

```sh
kubectl drain node02 --ignore-daemonsets --force
# node/node02 already cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-xpvg6, kube-system/kube-proxy-bd2hf
# evicting pod default/web-65d846d465-6ljsx
# evicting pod default/web-65d846d465-29wtp
# evicting pod default/web-65d846d465-pcqx6
# evicting pod default/web-65d846d465-vzhsx
# evicting pod default/web-65d846d465-nlskz
# pod/web-65d846d465-nlskz evicted
# pod/web-65d846d465-pcqx6 evicted
# pod/web-65d846d465-vzhsx evicted
# pod/web-65d846d465-29wtp evicted
# pod/web-65d846d465-6ljsx evicted
# node/node02 drained

kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName
# NAME                   NODE
# web-65d846d465-2hm4v   node01
# web-65d846d465-4ntbx   node01
# web-65d846d465-5cj67   node01
# web-65d846d465-6cgbd   node01
# web-65d846d465-85772   node01
# web-65d846d465-c6q28   node01
# web-65d846d465-dstww   node01
# web-65d846d465-kxp6h   node01
# web-65d846d465-qzqbr   node01
# web-65d846d465-xlmcm   node01
```

- Uncordon

```sh
kubectl uncordon node02
# node/node02 uncordoned

# confirm current schedulability
kubectl describe node node02 | grep Unschedulable
# Unschedulable:      false

kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName
# NAME                   NODE
# web-65d846d465-2hm4v   node01
# web-65d846d465-4ntbx   node01
# web-65d846d465-5cj67   node01
# web-65d846d465-6cgbd   node01
# web-65d846d465-85772   node01
# web-65d846d465-c6q28   node01
# web-65d846d465-dstww   node01
# web-65d846d465-kxp6h   node01
# web-65d846d465-qzqbr   node01
# web-65d846d465-xlmcm   node01
```

- Restart

```sh
kubectl rollout restart deploy web
# deployment.apps/web restarted

# confirm: node01, node02
kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName
# NAME                   NODE
# web-869b5c46f4-4hj55   node01
# web-869b5c46f4-4kxb4   node02
# web-869b5c46f4-5zg7f   node02
# web-869b5c46f4-8f97t   node02
# web-869b5c46f4-dcpvt   node01
# web-869b5c46f4-jfjtq   node01
# web-869b5c46f4-lvmcb   node02
# web-869b5c46f4-mrw8w   node02
# web-869b5c46f4-v92xh   node02
# web-869b5c46f4-wl9ww   node01
```
