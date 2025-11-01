# Kubernetes - PriorityClass

[Back](../../index.md)

- [Kubernetes - PriorityClass](#kubernetes---priorityclass)
  - [PriorityClass](#priorityclass)
  - [Imperative Command](#imperative-command)
  - [Declarative File](#declarative-file)
  - [Lab: priorityclass](#lab-priorityclass)

---

## PriorityClass

- `PriorityClass`

  - a **cluster-scoped object** that **assigns an integer priority** to pods.
  - No-namespaced objects
    - no created within a specific namespace

- Priority:

  - Higher numbers = higher priority.
  - Control plane components range
    - system-cluster-critical: 2,000,000,000
    - system-node-critical: 2,000,001,000
  - application and workloads range:
    - -2,147,483,648 - 1,000,000,000

- Behaviaor:

  - When the cluster is **short on resources**, the scheduler may **preempt (evict) lower-priority pods** to make room for higher-priority ones.

- Default priority value

  - By default: `0`
  - Custom default priority
    - by creating a pc with `globalDefault: true`
    - can only be define in one pc

- Preemption Policy:

  - `PreemptLowerPriority`:
    - default
    - preempt (evict) the existing lower-priority pods
  - `never`:
    - no action,
    - wait for the resources to free up

- Purpose:

  - **Ensure critical workloads** (e.g., ingress, DNS, controllers) get scheduled first.
  - Let batch/BestEffort jobs **yield to user-facing services** during pressure.
  - Provide a sensible default priority for “everything else.”

- Feature:

---

## Imperative Command

| CMD                         | DESC                 |
| --------------------------- | -------------------- |
| `kubectl get pc`            | List priorityclass   |
| `kubectl delete pc pc_name` | Delete priorityclass |

---

## Declarative File

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

## Lab: priorityclass

```sh
kubectl get pc
# NAME                      VALUE        GLOBAL-DEFAULT   AGE   PREEMPTIONPOLICY
# system-cluster-critical   2000000000   false            36d   PreemptLowerPriority
# system-node-critical      2000001000   false            36d   PreemptLowerPriority
```

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 100000
preemptionPolicy: PreemptLowerPriority

apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 1000
preemptionPolicy: PreemptLowerPriority
```

- Create pod

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: low-prio-pod
spec:
    containers:
    - image: nginx
      name: nginx
    priorityClassName: low-priority
```

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: high-prio-pod
spec:
    containers:
    - image: nginx
      name: nginx
    priorityClassName: high-priority
```

```sh
kubectl get pods -o custom-columns="NAME:.metadata.name,PRIORITY:.spec.priorityClassName"
# NAME            PRIORITY
# high-prio-pod   high-priority
# low-prio-pod    low-priority
```
