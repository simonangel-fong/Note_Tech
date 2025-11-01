# Kubernetes - Networking

[Back](../index.md)

- [Kubernetes - Networking](#kubernetes---networking)
  - [Networking](#networking)

---

## Networking

- each node has IP address
- each pod has its internal IP address

  - default range: 10.244.0.0/16

- Internal networking

- `Cluster Networking`:

  - **Pod-to-Pod Communication**:

    - Pods can communicate with each other directly via IP addresses.
    - Each Pod gets **its IP address**, and communication between Pods within the **same cluster** is efficient and fast.

  - **Service Abstraction**:
    - Kubernetes **abstracts Pods behind a `Service`**, which provides a stable **IP address** and **DNS name** for a set of Pods.
    - Services enable **load balancing** and discovery within the cluster.

---

- Example:

  - Node A:

    - IP: 192.168.1.2
    - Internal Network: 10.244.0.0/16
      - Pod: 10.244.0.2

  - Node B:
    - IP: 192.168.1.3
    - Internal Network: 10.244.0.0/16
      - Pod: 10.244.0.2

- Need networking routing to enable communication between node/pod without NAT.
