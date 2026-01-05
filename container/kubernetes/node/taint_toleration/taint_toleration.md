# Kubernetes - Node: Taints and Tolerations

[Back](../../index.md)

- [Kubernetes - Node: Taints and Tolerations](#kubernetes---node-taints-and-tolerations)
  - [Taints \& Tolerations](#taints--tolerations)
    - [Effects options](#effects-options)
  - [Tolerations](#tolerations)
    - [Use Cases](#use-cases)
    - [Imperative Commands](#imperative-commands)
  - [Lab: Control Plane Default Taint](#lab-control-plane-default-taint)
  - [Lab: Taint NoSchedule Effect](#lab-taint-noschedule-effect)
  - [Lab: Taint NoExecute Effect](#lab-taint-noexecute-effect)

---

## Taints & Tolerations

- `taint`

  - a **restriction** applied to a `node` that prevent `pods` from being **scheduled** onto the `Node` unless allowed.
    - **set on** the `node`
  - format: `key=value:effect`
    - key/value pair to identify the toleration that is allowed.

- By default the `control-plane` / `master Node` is **tainted** so that regular `Pods` are not scheduled onto it.

- **NOTE**:
  - `taint` works with `scheduler`; However, `Scheduler` **skips** the `Pod` with `pod.spec.nodeSelector`, can schedule directly on the specific `node`.

---

### Effects options

- `NoSchedule`
  - **New** Pods without matching `toleration` are **not scheduled**.
- `PreferNoSchedule`:
  - Scheduler tries to avoid placing Pods, but not strictly enforced.
- `NoExecute`
  - Prevents **scheduling** and **evicts** **existing** non-tolerating Pods.

---

## Tolerations

- `Tolerations`

  - a **exceptions** applied to a `pod` that **allow pods to be scheduled** even if a `taint` **exists** on a node.
  - set on the `Pod`, allowing a pod to be scheduled
  - key/value pair identifys toleration that is allowed
    - e.g.,
      - taint: `app=web:NoSchedule`
      - toleration `app=web`

- With `taint`

  - `Taints` on `Nodes` **repel** `Pods`.
  - `Tolerations` on `Pods` allow **exceptions**.
  - But `toleration` alone does **not guarantee** `scheduling` on a `tainted` Node
    - it just makes it **possible**.
    - Kubernetes still considers other scheduling rules (like resource requests, affinities, etc.).

- e.g.:

```yaml
kind: Pod
spec:
  tolerations:
    - key: "key"
      operator: "Equal"
      value: "value"
      effect: "NoSchedule"
```

---

### Use Cases

- **Dedicated nodes**
  - Ensure that **only specific workloads** run on **certain nodes**.
  - e.g., databases, monitoring agents
- **Node maintenance / cordon**
  - Temporarily taint nodes so no new Pods are scheduled.
- **Special hardware** (e.g., GPU nodes)
  - Taint GPU nodes; only GPU workloads with tolerations can land there.
- **Critical system Pods**
  - Nodes can be tainted `NoExecute` so only Pods with tolerations (like `kube-dns`) survive.

---

### Imperative Commands

| **CMD**                                                    | **DESC**                                                                    |
| ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| `kubectl describe node node_name \| grep Taint`            | Get taint info from a node                                                  |
| `kubectl taint nodes node_name key=value:NoSchedule`       | Taint to a Node; **prevents** scheduling Pods without matching toleration.  |
| `kubectl taint nodes node_name key=value:PreferNoSchedule` | Taint to a Node; scheduler **avoids** placing Pods there, but not strictly. |
| `kubectl taint nodes node_name key=value:NoExecute`        | Taint; **blocks** new Pods without toleration and evicts existing ones.     |
| `kubectl taint nodes node_name key=value:NoSchedule-`      | Remove a specific taint from a Node (note the trailing `-`).                |
| `kubectl describe node node_name`                          | Show details of a Node, including its taints.                               |

---

## Lab: Control Plane Default Taint

```sh
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   37d   v1.33.6
# node01         Ready    <none>          37d   v1.33.6
# node02         Ready    <none>          37d   v1.33.6

kubectl describe node controlplane
# Taints:             node-role.kubernetes.io/control-plane:NoSchedule
```

---

## Lab: Taint NoSchedule Effect

```sh
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   37d   v1.33.6
# node01         Ready    <none>          37d   v1.33.6
# node02         Ready    <none>          37d   v1.33.6

kubectl describe node node01 | grep Taints
# Taints:             <none>

kubectl describe node node02 | grep Taints
# Taints:             <none>

# add taint
kubectl taint node node02 app=database:NoSchedule
# node/node02 tainted

# confirm
kubectl describe node node02 | grep Taints
# Taints:             app=database:NoSchedule
```

---

- Create pod without toleration

```sh
kubectl run mongo01 --image=mongo
# pod/mongo01 created
kubectl run mongo02 --image=mongo
# pod/mongo02 created

# confirm: all schedule on node
kubectl get pod -o wide
# NAME      READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# mongo01   1/1     Running   0          11s   10.244.1.31   node01   <none>           <none>
# mongo02   1/1     Running   0          6s    10.244.1.32   node01   <none>           <none>
```

---

- Create pod with toleration

```yaml
# demo-taint-noschedule-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-taint-noschedule-pod
spec:
  tolerations:
    - key: "app"
      operator: "Equal"
      value: "database"
      effect: "NoSchedule"
  containers:
    - name: mongo
      image: mongo
```

```sh
kubectl apply -f demo-taint-noschedule-pod.yaml
# pod/demo-taint-noschedule-pod created

# pod can be scheduled on node02
kubectl get pod -o wide
# NAME                        READY   STATUS    RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
# demo-taint-noschedule-pod   1/1     Running   0          7s      10.244.2.34   node02   <none>           <none>
# mongo01                     1/1     Running   0          7m18s   10.244.1.36   node01   <none>           <none>
# mongo02                     1/1     Running   0          7m7s    10.244.1.37   node01   <none>           <none>
```

- Delete taint

```sh
kubectl taint node node02 app=database:NoSchedule-
# node/node02 untainted

kubectl describe node node02 | grep Taints
# Taints:             <none>

kubectl run mongo03 --image=mongo
# pod/mongo03 created

# Confirm
kubectl get pod mongo03 -o wide
# NAME      READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# mongo03   1/1     Running   0          29s   10.244.2.35   node02   <none>           <none>
```

---

## Lab: Taint NoExecute Effect

- Change Env, leave only one node

```sh
kubectl get node
# NAME           STATUS     ROLES           AGE   VERSION
# controlplane   Ready      control-plane   40d   v1.33.6
# node01         Ready      <none>          40d   v1.33.6
# node02         NotReady   <none>          40d   v1.33.6
```

```yaml
# demo-taint-noexecute-existing-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-old-mongo-notoleration
spec:
  containers:
    - name: mongo
      image: mongo

---
apiVersion: v1
kind: Pod
metadata:
  name: demo-old-mongo-toleration
spec:
  tolerations:
    - key: "app"
      operator: "Equal"
      value: "database"
      effect: "NoExecute"
  containers:
    - name: mongo
      image: mongo
```

```sh
kubectl apply -f demo-taint-noexecute-existing-pod.yaml
# pod/demo-old-mongo-notoleration created
# pod/demo-old-mongo-toleration created

kubectl get pod -o wide
# NAME                          READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# demo-old-mongo-notoleration   1/1     Running   0          77s   10.244.1.42   node01   <none>           <none>
# demo-old-mongo-toleration     1/1     Running   0          77s   10.244.1.41   node01   <none>           <none>
```

- Add taints

```sh
kubectl taint node node01 app=database:NoExecute
# node/node01 tainted

# confirm
kubectl describe node node01 | grep Taints
# Taints:             app=database:NoExecute

# confirm: only the toleration pod
kubectl get pod -o wide
# NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# demo-old-mongo-toleration   1/1     Running   0          27s   10.244.1.48   node01   <none>           <none>
```

---

```yaml
# demo-taint-noexecute-new-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-new-mongo-notoleration
spec:
  containers:
    - name: mongo
      image: mongo

---
apiVersion: v1
kind: Pod
metadata:
  name: demo-new-mongo-toleration
spec:
  tolerations:
    - key: "app"
      operator: "Equal"
      value: "database"
      effect: "NoExecute"
  containers:
    - name: mongo
      image: mongo
```

```sh
kubectl apply -f demo-taint-noexecute-new-pod.yaml
# pod/demo-new-mongo-notoleration created
# pod/demo-new-mongo-toleration created

# confirm: 1 pending; 1 running
kubectl get pod
# NAME                          READY   STATUS    RESTARTS   AGE
# demo-new-mongo-notoleration   0/1     Pending   0          40s
# demo-new-mongo-toleration     1/1     Running   0          40s
# demo-old-mongo-toleration     1/1     Running   0          3m22s
```

- Delete taints

```sh
kubectl taint node node01 app=database:NoExecute-
# node/node01 untainted

# confirm
kubectl describe node node01 | grep Taints
# Taints:             <none>

# confirm: all running
kubectl get pod
# NAME                          READY   STATUS    RESTARTS   AGE
# demo-new-mongo-notoleration   1/1     Running   0          2m15s
# demo-new-mongo-toleration     1/1     Running   0          2m15s
# demo-old-mongo-toleration     1/1     Running   0          4m57s
```