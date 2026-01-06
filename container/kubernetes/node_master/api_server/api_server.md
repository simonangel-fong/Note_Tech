# Kubernetes Cluster - API Server

[Back](../../index.md)

- [Kubernetes Cluster - API Server](#kubernetes-cluster---api-server)
  - [API Server](#api-server)

---

## API Server

- `API Server`

  - A `control plane` component that is the **front-end** to the `cluster`, **exposing** the `Kubernetes API`
    - `kubectl` (CLI) and Kubernetes **dashboard**
    - Other `control plane` **components** (scheduler, controllers)
    - Applications or automation tools (via API calls)
  - the **only component** that **talks directly** to `etcd`, storing and retrieving the cluster state.

---

- Key Roles:
  - **Entry point**: **All requests** to the `cluster` (create pod, scale deployment, query status) go through the `API Server`.
  - **Authentication & Authorization**: **Validates** user/clients via configured auth methods (certs, tokens, RBAC).
  - **Validation & Admission Control**: Ensures objects are **valid** before writing them to `etcd` (e.g., pod spec schema, quotas, policies).
  - **Cluster state storage**: **Persists desired state** into `etcd`.
  - **Watch/Notify**: Lets **controllers** and `kubelets` watch API resources to react when something changes.

---

- Installed with `kubeadm`
  - API Server runs as a `Pod` (usually a `static Pod`) on the `control plane (master)`
  - view api server using command `kubectl get pods -n kube-system`
- Custom Installations
  - can also be run as a systemd service (binary) directly on the host.
