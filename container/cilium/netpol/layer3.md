# Cilium - Network Policy Layer 3 Policies

[Back](../index.md)

- [Cilium - Network Policy Layer 3 Policies](#cilium---network-policy-layer-3-policies)
  - [Layer 3 Policies](#layer-3-policies)
  - [Endpoints based policies](#endpoints-based-policies)
    - [Egress Deny](#egress-deny)
    - [Egress Allow All Endpoints vs Egress Default Deny](#egress-allow-all-endpoints-vs-egress-default-deny)
  - [Services based policies](#services-based-policies)
  - [Entities-based L3 policies](#entities-based-l3-policies)
    - [entities](#entities)
  - [Node based L3 policies](#node-based-l3-policies)
  - [IP/CIDR based L3 policies](#ipcidr-based-l3-policies)
  - [DNS based L3 policies](#dns-based-l3-policies)

---

## Layer 3 Policies

- `layer 3 policy` establishes the **base connectivity** rules

- methods:
  - `Endpoints` based:
    - sed to establish rules between `endpoints` inside the cluster **managed by Cilium**.
    - advantage:
      - `IP` addresses are not encoded into the policies
      - the policy is completely decoupled from the addressing.
  - `Services` based:
    - use k8s `services`, even if the destination endpoint is not controlled by Cilium.
  - `Entities` based:
    - the **remote peers** which can be categorized **without knowing their IP addresses**.
    - e.g., connectivity to the local host serving the endpoints; all connectivity to outside of the cluster.
  - `Node` based:
    - extension of remote-node entity.
    - Optionally nodes can have unique identity that can be used to allow/block access only from specific ones.
  - `IP/CIDR` based:
    - the external services if the remote peer is not an endpoint.
    - requires to hardcode either **IP addresses** or **subnets** into the policies.
  - `DNS` based:
    - Selects remote, non-cluster, peers **using DNS names** converted to IPs via DNS lookups.

---

## Endpoints based policies

- `Endpoints-based L3 policy`
  - used to establish rules between `endpoints` inside the cluster **managed by Cilium**.
  - defined by using an `Endpoint Selector` inside a rule to select what kind of traffic can be received (on ingress), or sent (on egress).
    - An empty Endpoint Selector **allows all traffic**.

- sample:

```yaml
# allow
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "l3-rule"
spec:
  endpointSelector:
    matchLabels:
      role: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            role: frontend
---
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "l3-egress-rule"
spec:
  endpointSelector:
    matchLabels:
      role: frontend
  egress:
    - toEndpoints:
        - matchLabels:
            role: backend
```

```yaml
# allow all ingress traffic
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "allow-all-to-victim"
spec:
  endpointSelector:
    matchLabels:
      role: victim
  ingress:
    - fromEndpoints:
        - {}
```

---

### Egress Deny

- sample
  - allow all leaving traffic
  - block leaving traffic to backend

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "deny-egress-example"
spec:
  endpointSelector:
    matchLabels:
      role: frontend
  egress:
    - toEntities:
        - all
  egressDeny:
    - toEndpoints:
        - matchLabels:
            role: backend
```

---

### Egress Allow All Endpoints vs Egress Default Deny

- match all endpiont:
  - `toEndpoints: {}`

```yaml
# Egress Allow All Endpoints
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "allow-all-from-frontend"
spec:
  endpointSelector:
    matchLabels:
      role: frontend
  egress:
  - toEndpoints:
    - {}

# Egress Default Deny
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "deny-all-egress"
spec:
  endpointSelector:
    matchLabels:
      role: restricted
  egress:
  - {}
```

---

## Services based policies

- `Services-based L3 policy`
  - used to egress traffic to Kubernetes Services by name or label selector **without hardcoding IP addresses**.

- selector:
  - `k8sService`: by name
  - `k8sServiceSelector`: by label

- sample

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "service-rule"
spec:
  endpointSelector:
    matchLabels:
      id: app2
  egress:
    - toServices:
        # Services may be referenced by namespace + name
        - k8sService:
            serviceName: myservice
            namespace: default
        # Services may be referenced by namespace + label selector
        - k8sServiceSelector:
            selector:
              matchLabels:
                env: staging
            namespace: another-namespace
```

---

## Entities-based L3 policies

- `Entities-based L3 policies`
  - used to control network traffic to and from **broad, categorical groups** of peers (like the local host or the public internet) without needing to know or hardcode their changing IP addresses

---

### entities

| Entities         | Description                                                                           |
| ---------------- | ------------------------------------------------------------------------------------- |
| `host`           | the local host                                                                        |
| `remote-node`    | Any node in any of the connected clusters other than the local host.                  |
| `kube-apiserver` | the kube-apiserver in a Kubernetes cluster.                                           |
| `ingress`        | `Cilium Envoy` instance that handles ingress L7 traffic.                              |
| `cluster`        | the logical group of all network endpoints inside of the local cluster.               |
| `cluster-mesh`   | all endpoints in meshed clusters                                                      |
| `init`           | all endpoints in bootstrap phase                                                      |
| `health`         | the health endpoints, used to check cluster connectivity health.                      |
| `unmanaged`      | endpoints not managed by Cilium.                                                      |
| `world`          | all endpoints outside of the cluster.                                                 |
| `all`            | the combination of all known clusters as well world and whitelists all communication. |

- sample

```yaml
# kube-apiserver
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "dev-to-kube-apiserver"
spec:
  endpointSelector:
    matchLabels:
      env: dev
  egress:
    - toEntities:
        - kube-apiserver
```

```yaml
# access for all nodes
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "to-dev-from-nodes-in-cluster"
spec:
  endpointSelector:
    matchLabels:
      env: dev
  ingress:
    - fromEntities:
        - host
        - remote-node
```

```yaml
# Access to/from outside cluster
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "from-world-to-role-public"
spec:
  endpointSelector:
    matchLabels:
      role: public
  ingress:
    - fromEntities:
        - world
```

---

## Node based L3 policies

- `Node based L3 policies`
  - used to control traffic to or from specific **cluster nodes**.

- config:
  - helm: `nodeSelectorLabels: true`
  - cli flag: `--enable-node-selector-labels=true`

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "to-prod-from-control-plane-nodes"
spec:
  endpointSelector:
    matchLabels:
      env: prod
  ingress:
    - fromNodes:
        - matchLabels:
            node-role.kubernetes.io/control-plane: ""
```

---

## IP/CIDR based L3 policies

- `IP/CIDR based L3 policies`
  - used to define policies to and from endpoints which are not managed by Cilium and thus do not have labels associated with them.

- sample

```yaml
# Allow to external CIDR block
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "cidr-rule"
spec:
  endpointSelector:
    matchLabels:
      app: myService
  egress:
    - toCIDR:
        - 20.1.1.1/32
    - toCIDRSet:
        - cidr: 10.0.0.0/8
          except:
            - 10.96.0.0/12
```

---

## DNS based L3 policies

- `DNS based L3 policies`
  - used to define Layer 3 policies to endpoints that are not managed by Cilium, but have DNS queryable domain names.

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "to-fqdn"
spec:
  endpointSelector:
    matchLabels:
      app: test-app
  egress:
    - toEndpoints:
        - matchLabels:
            "k8s:io.kubernetes.pod.namespace": kube-system
            "k8s:k8s-app": kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: ANY
          rules:
            dns:
              - matchPattern: "*"
    - toFQDNs:
        - matchName: "my-remote-service.com"
```
