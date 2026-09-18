# Cilium - Network Policy Layer 4 Policies

[Back](../index.md)

- [Cilium - Network Policy Layer 4 Policies](#cilium---network-policy-layer-4-policies)
  - [Layer 4 Policies](#layer-4-policies)
    - [Labels-dependent Layer 4 rule](#labels-dependent-layer-4-rule)
    - [CIDR-dependent Layer 4 Rule](#cidr-dependent-layer-4-rule)
  - [ICMP policy](#icmp-policy)

---

## Layer 4 Policies

- If **no** `layer 4 policy` is specified for an endpoint, the endpoint is allowed to send and receive on **all** layer 4 ports and protocols including `ICMP`.
- If **any** `layer 4 policy` is specified, then `ICMP` will be **blocked** unless it’s related to a connection that is otherwise allowed by the policy.

---

- sample

```yaml
---
# TCP on port 80
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "l4-rule"
spec:
  endpointSelector:
    matchLabels:
      app: myService
  egress:
    - toPorts:
        - ports:
            - port: "80"
              protocol: TCP
---
# TCP on ports 80-444
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "l4-port-range-rule"
spec:
  endpointSelector:
    matchLabels:
      app: myService
  egress:
    - toPorts:
        - ports:
            - port: "80"
              endPort: 444
              protocol: TCP
```

---

### Labels-dependent Layer 4 rule

- sample

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "l4-rule"
spec:
  endpointSelector:
    matchLabels:
      role: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            role: frontend
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
```

---

### CIDR-dependent Layer 4 Rule

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "cidr-l4-rule"
spec:
  endpointSelector:
    matchLabels:
      role: crawler
  egress:
    - toCIDR:
        - 192.0.2.0/24
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
```

---

## ICMP policy

- sample

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "icmp-rule"
spec:
  endpointSelector:
    matchLabels:
      app: myService
  egress:
    - icmps:
        - fields:
            - type: 8
              family: IPv4
            - type: EchoRequest
              family: IPv6
```
