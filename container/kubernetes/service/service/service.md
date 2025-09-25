# Kubernetes - Service

[Back](../../index.md)

- [Kubernetes - Service](#kubernetes---service)
  - [Service](#service)
    - [Common Commands](#common-commands)

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

### Common Commands

| Command                             | Description                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------ |
| `kubectl create -f yaml_file`       | Create a Service from a YAML file.                                                   |
| `kubectl apply -f yaml_file`        | Apply changes to a Service configuration from a YAML file.                           |
| `kubectl get svc`                   | List all Services in the current namespace.                                          |
| `kubectl describe svc service_name` | Show detailed information about a specific Service.                                  |
| `kubectl delete svc service_name`   | Delete a Service by name.                                                            |
| `kubectl expose`                    | Expose a Service using a specific type such as NodePort, LoadBalancer, or ClusterIP. |

---

