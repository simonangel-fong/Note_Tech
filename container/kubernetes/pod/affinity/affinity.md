# Kubernetes - Pod: Node Affinity

[Back](../../index.md)

- [Kubernetes - Pod: Node Affinity](#kubernetes---pod-node-affinity)
  - [Affinity](#affinity)
  - [Node Affinity](#node-affinity)
    - [Scheduling Types](#scheduling-types)
    - [Operators for `matchExpressions`](#operators-for-matchexpressions)
    - [vs Taints \& Tolerations](#vs-taints--tolerations)
    - [Declarative Manifest](#declarative-manifest)
    - [Lab: Node Affinity - Required](#lab-node-affinity---required)
    - [Lab: Node Affinity - Preferred](#lab-node-affinity---preferred)
  - [Inter-pod Affinity and Anti-Affinity](#inter-pod-affinity-and-anti-affinity)
    - [Scheduling Types](#scheduling-types-1)
    - [Vs nodeAffinity](#vs-nodeaffinity)
    - [Lab: Pod Affinity - Required](#lab-pod-affinity---required)
    - [Lab: Pod Anti Affinity - Required](#lab-pod-anti-affinity---required)
  - [Good Pratices: Schedule Pods to a Node](#good-pratices-schedule-pods-to-a-node)

---

## Affinity

- `Affinity`

  - a scheduling rule that **attract or repel** `pods` from specific `nodes` or other `pods`.

- 2 primary types of affinity:

  - `Node Affinity`
  - `Inter-pod Affinity`.

- `pod.spec.affinity` field:

  - specify the pod's **scheduling constraints**

---

## Node Affinity

- `Node Affinity`

  - A `Pod`'s attribute.
  - used to **constrain** which `nodes` the `pod` can be **scheduled** on based on `node labels`.
    - not repelling Pods
    - **attracting** `Pods` to `Nodes` with **matching labels**.

- Example Use Case

  - ensure that a **machine-learning workload** only runs on nodes with specific `GPU` hardware.

---

### Scheduling Types

| Type      | Parameter                                         | Description                                                                      |
| --------- | ------------------------------------------------- | -------------------------------------------------------------------------------- |
| Required  | `requiredDuringSchedulingIgnoredDuringExecution`  | Schedules only on matching nodes; otherwise, stays `Pending`.                    |
| Preferred | `preferredDuringSchedulingIgnoredDuringExecution` | Tries to schedule on matching nodes; otherwise, schedules on any available node. |

- `IgnoredDuringExecution`:
  - If the node labels change while the pod is already running, Kubernetes will not evict or move the pod, regardless of whether it was Required or Preferred.

---

### Operators for `matchExpressions`

- `In`: key’s value must match one of the listed values.
- `NotIn`: key’s value must not match any of the listed values.
- `Exists`: the key must exist (value doesn’t matter).
- `DoesNotExist`: the key must not exist.
- `Gt` / `Lt`: numeric comparison.

---

### vs Taints & Tolerations

- `Node Affinity`:
  - `Pod` **attraction** to `Nodes` with labels.
- `Taints/Tolerations`:

  - `Node` **repelling** `Pods` unless tolerated.

- Often used together:
  - `Node Labels` + `Pod Affinity`: **desired** placement
  - `Node Taints` + `Pod Tolerations`: workload **isolation**.

---

### Declarative Manifest

- Example: a Pod must run on GPU-enabled Nodes.

```yaml
kind: Pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: "hardware"
                operator: In
                values:
                  - gpu
  containers:
    - name: myapp
      image: nginx
```

- Example: prefer running on SSD Nodes, but allow other Nodes if none are available.

```yaml
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 1
          preference:
            matchExpressions:
              - key: "disk"
                operator: In
                values:
                  - ssd
  containers:
    - name: myapp
      image: nginx
```

---

### Lab: Node Affinity - Required

```yaml
# demo-nodeaffinity-preferred.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-nodeaffinity-required
spec:
  replicas: 10
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: "disk"
                    operator: In
                    values:
                      - ssd
```

```sh
kubectl label node node02 disk=ssd
# node/node02 labeled

# confirm
kubectl get node -l disk=ssd
# NAME     STATUS   ROLES    AGE   VERSION
# node02   Ready    <none>   41d   v1.33.6

kubectl apply -f demo-nodeaffinity-required.yaml
# deployment.apps/demo-nodeaffinity-required created

# confirm scheduled on node02
kubectl get pod -l app=nginx -o wide
# NAME                                          READY   STATUS    RESTARTS   AGE    IP            NODE     NOMINATED NODE   READINESS GATES
# demo-nodeaffinity-required-55cbcd7b4c-47g46   1/1     Running   0          110s   10.244.2.53   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-5fkl2   1/1     Running   0          110s   10.244.2.56   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-6vjcw   1/1     Running   0          110s   10.244.2.52   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-86k48   1/1     Running   0          110s   10.244.2.59   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-kh8ct   1/1     Running   0          110s   10.244.2.60   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-pp9qd   1/1     Running   0          110s   10.244.2.57   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-qxbzh   1/1     Running   0          110s   10.244.2.61   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-spfqn   1/1     Running   0          110s   10.244.2.55   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-wcq62   1/1     Running   0          110s   10.244.2.54   node02   <none>           <none>
# demo-nodeaffinity-required-55cbcd7b4c-xc52r   1/1     Running   0          110s   10.244.2.58   node02   <none>           <none>
```

---

### Lab: Node Affinity - Preferred

```yaml
# demo-nodeaffinity-preferred.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-nodeaffinity-preferred
spec:
  replicas: 10
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: kubernetes.io/os
                    operator: In
                    values:
                      - linux
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 1
              preference:
                matchExpressions:
                  - key: label-1
                    operator: In
                    values:
                      - key-1
            - weight: 50
              preference:
                matchExpressions:
                  - key: label-2
                    operator: In
                    values:
                      - key-2
```

```sh
# no node label match

kubectl apply -f demo-nodeaffinity-preferred.yaml
# deployment.apps/demo-nodeaffinity-preferred created

# confirm scheduled on any nodes
kubectl get pod -l app=nginx -o wide
# NAME                                           READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# demo-nodeaffinity-preferred-6b489c7564-6t94l   1/1     Running   0          58s   10.244.1.81   node01   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-8gzmj   1/1     Running   0          59s   10.244.2.64   node02   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-dkpwr   1/1     Running   0          59s   10.244.2.63   node02   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-ftlzj   1/1     Running   0          58s   10.244.2.66   node02   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-gpc6q   1/1     Running   0          59s   10.244.1.82   node01   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-hsxsv   1/1     Running   0          59s   10.244.2.65   node02   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-nvnm4   1/1     Running   0          59s   10.244.1.83   node01   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-psd6h   1/1     Running   0          58s   10.244.1.85   node01   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-q9qcd   1/1     Running   0          59s   10.244.2.62   node02   <none>           <none>
# demo-nodeaffinity-preferred-6b489c7564-xvh5j   1/1     Running   0          59s   10.244.1.84   node01   <none>           <none>
```

---

## Inter-pod Affinity and Anti-Affinity

- allows to **constrain** `pod scheduling` based on the **labels** of `pods` that are **already running** on the `nodes`.

- `Pod Affinity`

  - Use this when needs to keep "buddy" services together.
  - e.g,: You have a web server and a cache (like Redis). Since they communicate frequently, you want them on the **same node** or in the same availability zone to reduce latency.

---

- `Pod Anti-Affinity`

  - Use this when need to keep `pods` **apart**.
  - e.g.: You have three replicas of a database. You want to ensure that **no two replicas** sit **on the same node**. This way, if one node fails, your entire service doesn't go down.

- `Topology Key`
  - What is the "boundary" for being considered "together"?
    - `kubernetes.io/hostname`: the same node.
    - `topology.kubernetes.io/zone`: the same availability zone.

---

### Scheduling Types

| Type      | Parameter                                         | Description                                                                           |
| --------- | ------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Required  | `requiredDuringSchedulingIgnoredDuringExecution`  | Schedules only if a matching pod is found in that topology; otherwise, stays Pending. |
| Preferred | `preferredDuringSchedulingIgnoredDuringExecution` | Tries to co-locate with matching pods; otherwise, schedules on any available node.    |

---

### Vs nodeAffinity

| feature      | Node Affinity                           | Pod Affinity                         |
| ------------ | --------------------------------------- | ------------------------------------ |
| Logic        | "Run on a node with label X"            | "Run near pods that have label Y"    |
| Operators    | In, NotIn, Exists, DoesNotExist, Gt, Lt | In, NotIn, Exists, DoesNotExist      |
| Topology Key | N/A                                     | Defines the scope (Node, Rack, Zone) |

---

### Lab: Pod Affinity - Required

```yaml
# demo-podaffinity-required.yaml
apiVersion: v1
kind: Pod
metadata:
  name: web
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchExpressions:
              - key: app
                operator: In
                values:
                  - web
          topologyKey: "kubernetes.io/hostname"
  containers:
    - name: nginx
      image: nginx
```

```sh
kubectl apply -f demo-podaffinity-required.yaml
# pod/web created

kubectl get pod web
# NAME   READY   STATUS    RESTARTS   AGE
# web    0/1     Pending   0          20s

# create web pod

kubectl run nginx --image=nginx -l app=web
# pod/nginx created

# confirm: web running after nginx created
kubectl get pod web
# NAME   READY   STATUS    RESTARTS   AGE
# web    1/1     Running   0          5m
```

---

### Lab: Pod Anti Affinity - Required

```yaml
# demo-podantiaffinity-required.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-podantiaffinity-required
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchExpressions:
              - key: app
                operator: In
                values:
                  - web
          topologyKey: "kubernetes.io/hostname"
  containers:
    - name: nginx
      image: nginx
```

```sh
kubectl run web --image=nginx -l app=web
# pod/web created

kubectl get pod -o wide
# NAME   READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# web    1/1     Running   0          16s   10.244.2.69   node02   <none>           <none>

kubectl apply -f demo-podantiaffinity-required.yaml
# pod/demo-podantiaffinity-required created

# confirm: deploy on node01
kubectl get pod
# NAME                            READY   STATUS    RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
# demo-podantiaffinity-required   1/1     Running   0          13s     10.244.1.87   node01   <none>           <none>
# web                             1/1     Running   0          3m18s   10.244.2.69   node02   <none>           <none>
```

---

## Good Pratices: Schedule Pods to a Node

- Add `Node taint`, to **repel unwanted** `Pod`
- Add `Pod toleration`, to **prefer wanted** `Pod`
- Add `Pod affinity`, to **attract desired** `Pod`
