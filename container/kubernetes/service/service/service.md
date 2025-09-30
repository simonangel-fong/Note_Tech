# Kubernetes - Service

[Back](../../index.md)

- [Kubernetes - Service](#kubernetes---service)
  - [Service](#service)
    - [Imperative Commands](#imperative-commands)
    - [Declarative Commands](#declarative-commands)

---

## Service

- `Service`

  - an **object** to **map network traffic** to the `Pods` in the `cluster`.
    - Since `Pods` are **ephemeral** (they can die, restart, change IPs), `Services` provide a **stable network identity** and a **consistent** way to reach them.
      - provides a **fixed** `DNS name` + `virtual IP`.
      - **Load balances traffic** across **healthy** `Pods`.
    - `Services` use **labels** and **selectors** to find the right `Pods`.

- Types of Services

  - `ClusterIP`
    - default
    - Exposes Pods on a `virtual internal IP`.
    - Accessible **only within** the `cluster`.
      - e.g. backend services for microservices.
  - `NodePort`
    - **Exposes the Service** on a **static port** (30000–32767) on **each** `Node`’s IP.
    - Accessible from **outside** the `cluster` using `NodeIP:NodePort`.
    - Good for **testing**, not ideal for production.
  - `LoadBalancer`
    - **Integrates** with cloud provider `load balancers` (`AWS ELB`, `GCP LB`, `Azure LB`).
    - **Exposes** the Service to the `internet`.
    - `Cloud provider` assigns a `public IP`.
  - `ExternalName`
    - **Maps** the `Service` to an **external** `DNS` name (like api.example.com).
    - No selector, just returns a `CNAME`.

- `Service Discovery`
  - **Inside** the `cluster`, `Services` are **automatically registered** with `DNS`.
  - e.g., `nginx-service.default.svc.cluster.local`
  - Other Pods can talk to it **using this name** instead of IP.

### Imperative Commands

| Command                                             | Description                                         |
| --------------------------------------------------- | --------------------------------------------------- |
| `kubectl get svc`                                   | List all Services in the current namespace.         |
| `kubectl describe svc service_name`                 | Show detailed information about a specific Service. |
| `kubectl create svc clusterip svc_name --tcp=80`    | Create a ClusterIP service                          |
| `kubectl create svc nodeport svc_name --tcp=80`     | Create a NodePort service                           |
| `kubectl create svc loadbalancer svc_name --tcp=80` | Create a LoadBalancer service                       |
| `kubectl delete svc svc_name`                       | Delete a Service by name.                           |

### Declarative Commands

| Command                       | Description                                                |
| ----------------------------- | ---------------------------------------------------------- |
| `kubectl create -f yaml_file` | Create a Service from a YAML file.                         |
| `kubectl apply -f yaml_file`  | Apply changes to a Service configuration from a YAML file. |

---
