# Kubernetes: Pod - PriorityClass

[Back](../../index.md)

- [Kubernetes: Pod - PriorityClass](#kubernetes-pod---priorityclass)
  - [PriorityClass](#priorityclass)
    - [Imperative Command](#imperative-command)
    - [Declarative Manifest](#declarative-manifest)
  - [Lab: Priority Class](#lab-priority-class)
    - [Default Priority Class](#default-priority-class)
    - [Create Priority Class](#create-priority-class)

---

## PriorityClass

- `PriorityClass`

  - a **cluster-scoped object** that **assigns an integer priority** to pods.
  - **No-namespaced** objects
    - no created within a specific namespace

- **Priority**:

  - **Higher** numbers = **higher** priority.
  - `Control plane` components range
    - **system-node-critical**: `2,000,001,000`
    - **system-cluster-critical**: `2,000,000,000`
  - `User-Defined` Range:
    - `-2,147,483,648` - `1,000,000,000`

- **Priority Value**

  - By default: `0`
  - Custom default priority
    - by creating a `PriorityClass` with `globalDefault: true`
    - can only be define in one `PriorityClass`

- **Behaviaor**:

  - When the cluster is **short on resources**, the scheduler may **preempt (evict) lower-priority pods** to make room for higher-priority ones.

- **Preemption Policy**:

  - `PreemptLowerPriority`:
    - default
      - preempt (evict) the existing lower-priority pods
  - `never`:
    - no action,
    - wait for the resources to free up

- **Purpose**:

  - **Ensure critical workloads** (e.g., ingress, DNS, controllers) get scheduled first.
  - Let batch/BestEffort jobs **yield to user-facing services** during pressure.
  - Provide a sensible default priority for “everything else.”

---

### Imperative Command

| CMD                                          | DESC                 |
| -------------------------------------------- | -------------------- |
| `kubectl get priorityclass`/`kubectl get pc` | List priorityclass   |
| `kubectl delete pc NAME`                     | Delete priorityclass |

---

### Declarative Manifest

- Create a pc

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Critical platform services."
preemptionPolicy: PreemptLowerPriority
globalDefault: false
```

- Associate with pod

```yaml
# pod
spec:
  priorityClassName: high-priority
```

---

## Lab: Priority Class

### Default Priority Class

```sh
kubectl get pc
# NAME                      VALUE        GLOBAL-DEFAULT   AGE   PREEMPTIONPOLICY
# system-cluster-critical   2000000000   false            36d   PreemptLowerPriority
# system-node-critical      2000001000   false            36d   PreemptLowerPriority
```

---

### Create Priority Class

```yaml
# demo-priorityclass.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 100000
preemptionPolicy: PreemptLowerPriority

---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 1000
preemptionPolicy: PreemptLowerPriority
```

- Create pod

```yaml
# demo-priorityclass-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: low-priority-pod
spec:
  priorityClassName: low-priority # specify priority
  containers:
    - image: nginx
      name: nginx

---
apiVersion: v1
kind: Pod
metadata:
  name: high-prio-pod
spec:
  priorityClassName: high-priority # specify priority
  containers:
    - image: nginx
      name: nginx
```

```sh
kubectl apply -f demo-priorityclass.yaml
# priorityclass.scheduling.k8s.io/high-priority created
# priorityclass.scheduling.k8s.io/low-priority created

kubectl apply -f demo-priorityclass-pod.yaml
# pod/low-priority-pod created
# pod/high-prio-pod created


kubectl get pods -o custom-columns="NAME:.metadata.name,PRIORITY:.spec.priorityClassName"
# NAME            PRIORITY
# high-prio-pod   high-priority
# low-prio-pod    low-priority
```
