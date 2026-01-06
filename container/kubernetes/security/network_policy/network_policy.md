# Kubernetes - Network Policy

[Back](../../index.md)

- [Kubernetes - Network Policy](#kubernetes---network-policy)
  - [Network Policy](#network-policy)
  - [Declarative](#declarative)
  - [Imperative Commands](#imperative-commands)

---

## Network Policy

- `Ingress`

  - the incoming traffic from the users

- `Egress`

  - the outgoing traffic from the app

- Default `all allow` rule:

  - Allow traffic from any pod to any other pod or services within the cluster.
  - enable pods can comuncate with each other.

- Network policy
  - used to regulate traffic within the cluster.
  - Not all network policies are supported
    - subject to the network solution
      - common supported solutions:
        - kube-router
        - Calico
        - Romana
      - not supported: Flannel
    - object can be created, but not enforced.

---

## Declarative

- 3 sections:
  - `podSelector`: the pod associate with the policy
  - `policyType`: Ingress/Egress
  - policy rule
    - from/to
      - 3 selectors:
        - `podSelector`
        - `namespaceSelector`
        - `ipBlock`
    - ports

```yaml
# limit mysql access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  # ingress rule
  ingress:
    # from/to
    - from:
        - podSelector:
            matchLabels:
              name: api-pod
      # port
      ports:
        - protocal: TCP
          port: 3306
```

---

- Example: protect mysql db

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  # associate with selected pods
  podSelector:
    matchLabels:
      role: db
    # define type of policy
    policyTypes:
      - Ingress
      - Egress
    # rules
    ingress:
      - from:
          # only allow request from api-pod
          - podSelector:
              matchLabel:
                name: api-pod
            # alllow request from a specific ns
            namespaceSelector:
              matchLabel:
                kubernetes.io/metadata.name: prod
            # allow pod with an ip
            - ipBlock:
                cidr: 192.168.5.10/32
        ports:
          - protocal: TCP
            port: 3306
    egress:
    - to:
        # allow request from db to a specific ip pod
        - ipBlock:
            cidr: 192.168.5.10/32
        ports:
        - protocal: TCP
          port: 80
```

> Note: ingress rule has 2 selectors in the above case:
>
> 1. api-pod within the prod ns
> 2. the pod with a given IP

---

## Imperative Commands

| Command                                                                                  | Description                                                                                  |
| ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `kubectl explain networkpolicy`                                                          | Display documentation for the NetworkPolicy API.                                             |
| `kubectl get networkpolicy`/`kubectl get netpol`                                         | List all NetworkPolicies in the current namespace.                                           |
| `kubectl get networkpolicy -A`                                                           | List all NetworkPolicies across all namespaces.                                              |
| `kubectl describe networkpolicy <name>`                                                  | Show details of a specific NetworkPolicy.                                                    |
| `kubectl create networkpolicy <name> --pod-selector=<k=v> --policy-types=Ingress,Egress` | Create a minimal NetworkPolicy allowing **no ingress/egress** except explicitly added rules. |
| `kubectl delete networkpolicy <name>`                                                    | Delete a specific NetworkPolicy.                                                             |
| `kubectl edit networkpolicy <name>`                                                      | Edit an existing NetworkPolicy in-place.                                                     |

---
