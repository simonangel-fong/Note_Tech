# Kubernetes - Node Selector

[Back](../../index.md)

- [Kubernetes - Node Selector](#kubernetes---node-selector)
  - [Node Selector](#node-selector)

---

## Node Selector

- Used on pod to select node where it is scheduled.
  - Only support the complete label match
  - Affinity provide more flexible match
- Label a node

| CMD                                       | DESC                            |
| ----------------------------------------- | ------------------------------- |
| `kubectl label node node_name size=large` | Add or update a label on a node |
| `kubectl label node node_name size-`      | Remove a label from a node      |

- Label a node

```sh
kubectl label node node_name size=Large
```

- Use Node selector for a pod

```yaml
spec:
  nodeSelector:
    size: Large # refer to the node label
```
