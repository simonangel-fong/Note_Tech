# Kubernetes - Controller Manager

[Back](../../index.md)

- [Kubernetes - Controller Manager](#kubernetes---controller-manager)
  - [Controller Manager](#controller-manager)
  - [Common Controllers](#common-controllers)

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

## Common Controllers

- `node controller`
  - used to monitor the status of the nodes
  - default
    - check the status of the nodes every 5s
    - mark the node as `unreachable` if it cannot receive heartbeat for 40s.
    - give the `unreachable` node 5 min to come back
    - remove the `pods` running on `unreachable node`
      - provision the removed `pods` on a healthy ones.

---

- `replication controller`
  - used to monitor the status of the replica sets
  - Ensures the specified number of pod replicas are always running.
    - If a pod dies, it creates a replacement.
    - If too many pods are running, it deletes extras

---

- `deployment controller`
  - used to manages deployments (built on top of ReplicaSets).
  - Handles rolling updates and rollbacks.
  - Ensures the desired version of an application is running.

---

- `Endpoint Controller`
  - Populates Endpoints objects that map Services → Pod IPs.

---

- `Stateful-Set Controller`
  - Manages pods that need stable network identities and persistent storage.
  - Ensures ordered deployment, scaling, and deletion.

---

- `DaemonSet Controller`
  - Ensures one copy of a pod runs on every (or selected) node.
  - Commonly used for monitoring agents (Prometheus node exporter) or networking plugins (Calico, Flannel).

---

- `Job Controller`

  - runs Pods until a task completes successfully.

- `CronJob Controller`
  - schedules Jobs based on cron expressions (periodic tasks).

---

- `Service Account & Token Controllers`
  - Create default service accounts and attach API tokens to pods for authentication.
