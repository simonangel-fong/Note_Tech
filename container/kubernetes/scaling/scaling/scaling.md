# Kubernetes - Workload: Scaling

[Back](../../index.md)

- [Kubernetes - Workload: Scaling](#kubernetes---workload-scaling)
  - [Scaling](#scaling)
    - [Scaling in k8s](#scaling-in-k8s)
    - [VPA vs HPA](#vpa-vs-hpa)

---

## Scaling

- `scaling`

  - **dynamically adjusting** the number of **resources** allocated to an application **to meet changing demand**.

- 2 types of scaling
  - `vertical scaling`
    - Increases the size of CPU or memory for the server
    - lead to app downtime
  - `horizontal scaling`
    - Increases the number of servers and shares the workload
    - avoid downtime

---

### Scaling in k8s

- 2 types of scaling

  - `scaling workload`
    - scale the worklad by adding or removing pods
  - `scaling cluster infrastructure`
    - scale the underline infrastructure by adding or removing servers or infrastructure

- 2 methods to implement scaling
  - manual
  - automated

| way of scaling             | scaling cluster infra                                   | scaling workload                                         |
| -------------------------- | ------------------------------------------------------- | -------------------------------------------------------- |
| Horizontal scaling(manual) | Add more nodes (`kubeadmin join`)                       | Add more pods (`kubectl scale`)                          |
| Horizontal scaling(auto)   | `Cluster Autoscaler`                                    | `Horizontal Pod Autoscaler(HPA)`                         |
| Vertical scaling (manual)  | Add more resource to the existing nodes (downtime risk) | Allocate more resource to existing pods (`kubectl edit`) |
| Vertical scaling (auto)    | N/A                                                     | `Vertical Pod Autoscaler(VPA)`                           |

---

### VPA vs HPA

| Feature               | VPA                                              | HPA                                         |
| --------------------- | ------------------------------------------------ | ------------------------------------------- |
| Scaling method        | Increase CPU and memory of **existing** pod      | **Add/Remove** pod based on load            |
| Pod behavior          | **Restarts** pod to apply new resource values    | **Keep** existing pod running               |
| Handle traffic spikes | No, scaling needs a pod restart                  | Yes, instantly adds more pods               |
| Optimizes Costs       | Prevents over-provisioning of CPU/memory         | Avoids unnecessary idle pods                |
| Best for              | Stateful workloads,CPU/memory-heavy apps(DB, ML) | Web apps, microservices, stateless services |
| use cases             | DB, JVM-based apps, AI/ML                        | Web servers, message queues, microservices  |
