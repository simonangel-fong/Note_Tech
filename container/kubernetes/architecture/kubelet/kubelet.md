# Kubernetes - `kubelet`

[Back](../../index.md)

- [Kubernetes - `kubelet`](#kubernetes---kubelet)
  - [Kubelet](#kubelet)

---

## Kubelet

- `kubelet`

  - the **agent** that **runs on every node** in a Kubernetes cluster and ensures that containers are running in Pods as expected on its node.

- Primary Roles

  - **Node Registration & Management**
    - **Registers the node** with the cluster’s `API Server`.
    - Ensures node labels, capacity, and conditions are kept up to date.
  - **Static Pod Management**
    - Runs Pods defined locally on the node (in `/etc/kubernetes/manifests/`).
    - Commonly used to run `control plane` components on `master nodes`.
  - **Pod Lifecycle Management**
    - **Watches** the `API Server` for Pods assigned to its node.
    - **Creates, starts, stops, and deletes** containers to match the `PodSpec`.
    - Continuously checks and **reconciles**: “Are the right Pods running on this node?”
  - **Interface to Container Runtime**
    - Talks to the `container runtime` (Docker, containerd, CRI-O) via the `Container Runtime Interface (CRI)`.
    - Actually launches containers as requested in `PodSpecs`.
  - **Health Monitoring & Reporting**
    - Runs liveness, readiness, and startup **probes** for containers.
    - Reports Pod and Node status (e.g., CPU/memory pressure, health) back to the `API Server`.

---
