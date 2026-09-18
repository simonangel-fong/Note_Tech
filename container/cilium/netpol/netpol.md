# Cilium - Network Policy

[Back](../index.md)

- [Cilium - Network Policy](#cilium---network-policy)
  - [Network Policy](#network-policy)
    - [Policy Enforcement Modes](#policy-enforcement-modes)
    - [Endpoint default policy](#endpoint-default-policy)
  - [Rule Basics](#rule-basics)
  - [CiliumClusterwideNetworkPolicy vs ClusterNetworkPolicy](#ciliumclusterwidenetworkpolicy-vs-clusternetworkpolicy)

---

## Network Policy

### Policy Enforcement Modes

- 3 policy enforcement modes of agent:
  - `default`:
    - `endpoints` have **unrestricted network access** until selected by policy.
    - Upon being selected by a policy, the `endpoint` **permits only allowed traffic**.
  - `always`
    - policy enforcement is **enabled** on **all** `endpoints` even if no rules select specific endpoints.
  - `never`
    - policy enforcement is **disabled** on **all** `endpoints`, even if rules do select specific endpoints.

- configuration:
  - helm method: `policyEnforcementMode`
  - cli flag: `enable-policy`

---

### Endpoint default policy

- **By default**, all `egress` and `ingress` traffic is **allowed** for all `endpoints`.
- When an `endpoint` is selected by a `network policy`, it transitions to a `default-deny state`, where **only explicitly allowed traffic** is permitted.
  - If any rule selects an `Endpoint` and the rule has an `ingress` section, the `endpoint` goes into **default deny-mode** for `ingress`.
  - If any rule selects an `Endpoint` and the rule has an `egress` section, the `endpoint` goes into **default-deny mode** for egress.

---

- configure default `deny-mode`
  - rule: `EnableDefaultDeny`

- sample:
  - intercept dns traffic
  - do not block any traffic

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: intercept-all-dns
spec:
  endpointSelector:
    matchExpressions:
      - key: "io.kubernetes.pod.namespace"
        operator: "NotIn"
        values:
          - "kube-system"
      - key: "k8s-app"
        operator: "NotIn"
        values:
          - kube-dns
  # disable default deny
  enableDefaultDeny:
    egress: false
    ingress: false
  egress:
    - toEndpoints:
        - matchLabels:
            io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: TCP
            - port: "53"
              protocol: UDP
          rules:
            dns:
              - matchPattern: "*"
```

---

## Rule Basics

- based upon a `whitelist model`:
  - seach rule in the policy **allows traffic** that **matches** the rule.
    - If **two** rules exist, and one would match a broader set of traffic, then all traffic matching the **broader rule will be allowed**.
    - If there is an **intersection** between two or more rules, then traffic **matching the union** of those rules will be allowed.
    - If traffic does **not match** any of the rules, it will be **dropped** pursuant to the `Policy Enforcement Modes`.

- `endpointSelector / nodeSelector`
  - Selects the `endpoints` or `nodes` which the policy rules apply to.
- `ingress`
  - List of rules which must apply at `ingress` of the endpoint, i.e. to all network packets which are **entering** the endpoint.
- `egress`
  - List of rules which must apply at `egress` of the endpoint, i.e. to all network packets which are **leaving** the endpoint.
- `labels`
  - Labels are used to **identify** the rule.
  - Rules can be listed and deleted by labels.
- `description`
  - Description is a string which is not interpreted by Cilium.

---

## CiliumClusterwideNetworkPolicy vs ClusterNetworkPolicy

- `CiliumNetworkPolicy`:
  - Namespace-scoped.
  - applies only to workloads **inside the specific namespace** where the resource is created.
  - Typically managed by **application or namespace teams** for their specific services.

- `CiliumClusterwideNetworkPolicy`:
  - Cluster-scoped.
  - applies globally across **all namespaces** in the entire cluster.
  - Requires cluster **admin** permissions and is managed by **platform** or security teams for global guardrails.

- sample:

```yaml
# deny ingress from “world” on all namespaces on all Pods managed by Cilium
apiVersion: "cilium.io/v2"
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: "external-lockdown"
spec:
  endpointSelector: {}
  ingress:
    - fromEntities:
        - "all"
  ingressDeny:
    - fromEntities:
        - "world"
```
