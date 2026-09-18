# Cilium

[Back](../../README.md)

---

- [Installation](./install/install.md)

---

- [Network Policy](./netpol/netpol.md)
  - [Layer 3 Policies](./netpol/layer3.md)
  - [Layer 4 Policies](./netpol/layer4.md)
  - [Layer 7 Policies](./netpol/layer7.md)

---

- `Cilium` cli

| Command                    | Description            |
| -------------------------- | ---------------------- |
| `cilium status`            | Check cluster status   |
| `cilium connectivity test` | Run connectivity tests |
| `cilium config view`       | View configuration     |

- `cilium-dbg` (Agent CLI)

| Command                          | Description                                           |
| -------------------------------- | ----------------------------------------------------- |
| `cilium-dbg endpoint list`       | List all endpoints managed by a specific node's agent |
| `cilium-dbg identity list`       | List all known identities in the cluster              |
| `cilium-dbg policy get`          | View active policy rules                              |
| `cilium-dbg monitor --type drop` | Monitor network drops                                 |

```sh
kubectl exec -n kube-system <cilium-pod-name> -c cilium-agent -- cilium-dbg monitor --type drop
```

```sh
kubectl exec -n kube-system cilium-g4pdl -c cilium-agent -- cilium-dbg endpoint list
kubectl exec -n kube-system cilium-g4pdl -c cilium-agent -- cilium-dbg identity list
kubectl exec -n kube-system cilium-g4pdl -c cilium-agent -- cilium-dbg policy get
```
