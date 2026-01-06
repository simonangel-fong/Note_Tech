# Kubernetes Cluster - Controller Manager

[Back](../../index.md)

- [Kubernetes Cluster - Controller Manager](#kubernetes-cluster---controller-manager)
  - [Controller Manager](#controller-manager)
  - [Controllers](#controllers)
  - [Common Controllers](#common-controllers)
    - [Workload controllers](#workload-controllers)
    - [Node \& service discovery](#node--service-discovery)
    - [Config \& security](#config--security)
    - [Storage](#storage)
    - [Autoscaling \& disruption](#autoscaling--disruption)

---

## Controller Manager

- `Controller Manager`

  - A `control plane` component that runs `controller processes`, which continuously monitor the cluster through the `API Server` and reconcile the **actual** cluster state to match the **desired** state.
  - act as the **automation brain**
    - **constantly watching** the `API Server` and **taking action** to drive the system **toward the declared configuration**.

- a `control plane` **service** that runs on `master node(s)`, hosting **multiple** controllers in **one process** to ensure the **cluster state** matches the **desired state**.

- Roles of controllers

  - **Watching resource objects** via the API Server.
  - **Detecting differences** between **desired** state (from etcd) and **actual** state
  - Reconciling: taking corrective action to move toward the desired state.

- `Kubernetes Controller Manager (kube-controller-manager)`

  - a single process to manage all controllers
  - `ps -aux | grep kube-controller-manager`

---

```sh
kubectl get pods -n kube-system
# kube-controller-manager-docker-desktop   1/1     Running   126 (4h2m ago)   148d
```

---

## Controllers

- `controllers`
  - a **control loops** that **watch the state** of cluster, then make or request changes where needed.

---

## Common Controllers

### Workload controllers

| Controller               | Description                                                                |
| ------------------------ | -------------------------------------------------------------------------- |
| `ReplicaSet Controller`  | Keeps an exact number of identical Pods running.                           |
| `Deployment Controller`  | Manages stateless apps via ReplicaSets; handles rolling updates/rollbacks. |
| `StatefulSet Controller` | Stable Pod IDs and storage; ordered rollout/scale for stateful apps.       |
| `DaemonSet Controller`   | Ensures one Pod per (matching) node (agents, CNIs, CSI nodes).             |
| `Job Controller`         | Runs Pods to completion with retries/backoff.                              |
| `CronJob Controller`     | Schedules Jobs on a cron timetable.                                        |

---

### Node & service discovery

| Controller                             | Description                                                       |
| -------------------------------------- | ----------------------------------------------------------------- |
| `Node controller Controller`           | Tracks node health; taints/evicts from NotReady nodes.            |
| `Endpoints / EndpointSlice Controller` | Maintains Service → Pod endpoint lists for traffic routing.       |
| `Service controller` (cloud)           | Creates/updates external load balancers for `type: LoadBalancer`. |

---

### Config & security

| Controller                                   | Description                                                  |
| -------------------------------------------- | ------------------------------------------------------------ |
| `ServiceAccount Controller`                  | Creates default ServiceAccounts in namespaces.               |
| `Token Controller`                           | Manages projected service account tokens for Pods.           |
| `ResourceQuota Controller`                   | Enforces per-namespace quotas (CPU/mem/PVCs, etc.).          |
| `LimitRange Controller`                      | Sets default/max/min resource requests/limits per namespace. |
| `Namespace Controller`                       | Finalizes resources during namespace deletion.               |
| `Garbage Collector Controller`               | Cleans up dependents via ownerReferences/finalizers.         |
| `TTLAfterFinished Controller`                | Deletes completed Jobs/Pods after a set TTL.                 |
| `CertificateSigningRequest (CSR) Controller` | Approves/signs node/user certs per policy (if enabled).      |

---

### Storage

| Controller                                | Description                                        |
| ----------------------------------------- | -------------------------------------------------- |
| `PersistentVolume (PV) binder Controller` | Binds PVCs to PVs per StorageClass & access modes. |
| `Attach/Detach Controller`                | Safely attaches/detaches volumes to nodes.         |
| `Volume expansion Controller`             | Handles PVC resize (online if driver supports it). |

---

### Autoscaling & disruption

| Controller                                 | Description                                                  |
| ------------------------------------------ | ------------------------------------------------------------ |
| `HorizontalPodAutoscaler (HPA) Controller` | Scales replicas based on metrics (CPU/memory/custom).        |
| `PodDisruptionBudget (PDB) Controller`     | Limits voluntary disruptions to keep minimum Pods available. |
