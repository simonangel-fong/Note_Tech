# Kubernetes Networking: Topology-Aware Routing (TAR)

[Back](../../index.md)

- [Kubernetes Networking: Topology-Aware Routing (TAR)](#kubernetes-networking-topology-aware-routing-tar)
  - [Configuring Services to route traffic to nearby endpoints](#configuring-services-to-route-traffic-to-nearby-endpoints)
  - [Topology-Aware Routing (TAR)](#topology-aware-routing-tar)

---

## Configuring Services to route traffic to nearby endpoints

- When you deploy `pods`, they are **distributed across** the `nodes` in the cluster.

  - If cluster `nodes` **span different** `availability zones` or `regions` and the `pods` deployed on those nodes exchange traffic with each other, **network performance and traffic costs** can become an issue.
  - In this case, it makes sense for services to **forward traffic** to pods that aren’t far from the pod where the traffic originates.

- `svc.spec.internalTrafficPolicy` field
  - `local`:
    - traffic from `pods` on a given `node` is **forwarded only to** `pods` on the **same node**.
    - If there are **no** node-local service endpoints, the **connection fails**.

---

## Topology-Aware Routing (TAR)

- `Topology-Aware Routing (TAR)`

  - intelligently directs network traffic to stay **within the same physical zone** (like an AWS Availability Zone) where it started, reducing latency, cutting cloud provider costs for cross-zone data transfer, and improving performance by keeping communication local

- all cluster `nodes` must contain the `kubernetes.io/zone` label to **indicate which zone** each node is located in.
- `service.kubernetes.io/topology-aware-hints`=`auto`

  - adds the hints to each endpoint in the `EndpointSlice` object(s)

- Example:

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: example-hints
  labels:
    kubernetes.io/service-name: example-svc
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 80
endpoints:
  - addresses:
      - "10.1.2.3"
    conditions:
      ready: true
    hostname: pod-1
    zone: zone-a
    hints: # hint
      forZones:
        - name: "zone-a"
```

---
