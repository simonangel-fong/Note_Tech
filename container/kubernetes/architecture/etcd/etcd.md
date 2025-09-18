# Kubernetes - etcd

[Back](../../index.md)

- [Kubernetes - etcd](#kubernetes---etcd)
  - [`etcd`](#etcd)
    - [How it Works - `kubectl apply`](#how-it-works---kubectl-apply)
    - [How it Works - `kubectl get`](#how-it-works---kubectl-get)
  - [Common commands](#common-commands)

---

## `etcd`

- `etcd`

  - a **distributed**, consistent **key-value store**
  - acts as the **single source of truth** for the cluster.

- **Everything** is created or changed in Kubernetes is **stored** in `etcd`

  - **Cluster state**: what nodes exist, their health, etc.
  - **Workloads**: Deployments, Pods, ReplicaSets, DaemonSets.
  - **Configuration**: ConfigMaps, Secrets.
  - **Networking**: Services, Endpoints, network policies.
  - **Access control**: Roles and RoleBindings.

- Port:
  - `2379`
    - client communication
    - Used by the Kubernetes `API Server` (and any other client) to **read/write data**.
    - https://etcd_server:2379
  - `2380`
    - peer communication
    - Used for etcd members to talk to each other in an `etcd` cluster.
    - https://etcd_server:2380

---

- Important roles:
  - **Consistency**: `etcd` ensures that all `API servers` see the **same state**, even in multi-master setups.(implementing **locks** within the cluster)
  - **Fault Tolerance**: `etcd clusters` **replicate data** across multiple members to survive node failures.
  - **Performance**: optimized for fast reads/writes of **small JSON objects**, which is ideal for Kubernetes metadata.

---

### How it Works - `kubectl apply`

- issue **apply** YAML (`kubectl apply -f yaml_file`) send request goes to `API Server`.
- `API Server` **validates** and **writes** the **desired state** into `etcd`.
- `Controllers`, `schedulers`, and other `control plane` components take actions to make the actual cluster **match** the **desired state**.

---

### How it Works - `kubectl get`

- When launching the command `kubectl get pods`, the request is sent to the `API Server` via a REST API call.

  - kubectl is just a `thin client` — it **doesn’t** talk to `etcd` or nodes **directly**.

- The `API Server` **checks** authentication and authorization, RBAC.

  - If you don’t have permission to get pods, it denies the request.

- The `API Server` looks up the current cluster state from `etcd`
  - the API Server also uses its **local cache** that is always consistent with the latest state.
- The `API Server` **returns** the requested objects

---

## Common commands

```sh
kubectl get pods -n kube-system
# NAME                                     READY   STATUS    RESTARTS        AGE
# ...
etcd-docker-desktop                      1/1     Running   124 (41s ago)   147d
# ...

```

- version 2

| CMD                      | DESC |
| ------------------------ | ---- |
| `etcdctl backup`         |      |
| `etcdctl cluster-health` |      |
| `etcdctl mk`             |      |
| `etcdctl mkdir`          |      |
| `etcdctl set`            |      |

- version 3

| CMD                       | DESC |
| ------------------------- | ---- |
| `etcdctl snapshot save`   |      |
| `etcdctl endpoint health` |      |
| `etcdctl get`             |      |
| `etcdctl put`             |      |

- Command to get the version os API
  - `export ETCDCTL_API=3`
