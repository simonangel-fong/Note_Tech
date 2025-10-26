# Kubernetes - Node Affinity

[Back](../../index.md)

- [Kubernetes - Node Affinity](#kubernetes---node-affinity)
  - [Node Affinity](#node-affinity)
    - [Types of Node Affinity](#types-of-node-affinity)
    - [Operators for `matchExpressions`](#operators-for-matchexpressions)
    - [vs Taints \& Tolerations](#vs-taints--tolerations)
  - [Specify Pods dedicated to a node](#specify-pods-dedicated-to-a-node)

---

## Node Affinity

- `Node Affinity`

  - a set of **rules** that **constrain** which `Nodes` a `Pod` can be **scheduled** on, based on `Node labels`.
    - not repelling Pods
    - attracting Pods to Nodes with matching labels.

- Used on Pod

---

### Types of Node Affinity

| During Scheduling | During Execution | Affinity Type                                     |
| ----------------- | ---------------- | ------------------------------------------------- |
| Required          | Ignored          | `requiredDuringSchedulingIgnoredDuringExecution`  |
| Preferred         | Ignored          | `preferredDuringSchedulingIgnoredDuringExecution` |

---

- `requiredDuringSchedulingIgnoredDuringExecution`

  - available affinity type
  - mandatory
  - Hard rule
    - If no matching Nodes are found, the `Pod` will **not be scheduled**.
  - use case:
    - a Pod must run on GPU-enabled Nodes.

- e.g.,

```yaml
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

---

- `preferredDuringSchedulingIgnoredDuringExecution`

  - available affinity type
  - preference
  - Soft rule
  - The scheduler will try to place the `Pod` on matching Nodes,
    - will **fall back to others if needed**.
  - use case:
    - prefer running on SSD Nodes, but allow other Nodes if none are available.

- e.g.,

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

- `requiredDuringSchedulingRequiredDuringExecution`
  - planed affinity type

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

## Specify Pods dedicated to a node

- Add node taint, to repel unwanted pod
- Add pod toleration, to prefer wanted pod
- Add pod affinity, to attract desired pod