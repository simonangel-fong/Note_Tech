# Kubernetes Cluster - API Server

[Back](../../index.md)

- [Kubernetes Cluster - API Server](#kubernetes-cluster---api-server)
  - [API Server](#api-server)
  - [API Groups](#api-groups)
    - [`/api`: core group](#api-core-group)
    - [`/apis`: named group](#apis-named-group)
  - [Connection](#connection)

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

---

## API Groups

- K8s API paths are grouped into serveral groups

  - `/api`: core group
  - `/apis`: named group, associate with resources

```sh
# list available paths
curl https://localhost:6443 -k

# get the sub-path
curl https://localhost:6443/apis -k | grep "name"


```

- Common API Endpoints

| **API Path**              | **Description**                                                             |
| ------------------------- | --------------------------------------------------------------------------- |
| `/healthz`                | Overall API server health check. Returns `200 OK` if healthy.               |
| `/healthz/<probe>`        | Per-component health (e.g., `/healthz/etcd`, `/healthz/poststarthook/...`). |
| `/readyz`                 | API server readiness check (often used by kubelet).                         |
| `/livez`                  | API server liveness check (container health).                               |
| `/metrics`                | Prometheus metrics for the API server (latency, request counts, etc.).      |
| `/version`                | Returns the Kubernetes version info (git version, build date, platform).    |
| `/swagger.json`           | The raw OpenAPI v2 spec (deprecated).                                       |
| `/openapi/v2`             | OpenAPI v2 API definitions.                                                 |
| `/openapi/v3`             | OpenAPI v3 schema split by groups.                                          |
| `/logs`                   | API server logs (if aggregation / logging is enabled).                      |
| `/debug/pprof/`           | Go pprof performance profiling endpoints (CPU, mem, traces).                |
| `/api`                    | Entry point for **core API group** → `/api/v1/…`                            |
| `/apis`                   | Entry point for **all named API groups**, e.g. `/apis/apps/v1/...`          |
| `/api/v1`                 | Core API group (pods, services, nodes, configmaps, etc.)                    |
| `/apis/<group>/<version>` | Named API group entry (apps, batch, networking…).                           |
| `/clusters/<name>`        | Multicluster access (largest distros; API aggregator).                      |

---

### `/api`: core group

| **API Path**                     | **Description**        |
| -------------------------------- | ---------------------- |
| `/api/v1/nodes`                  | Nodes                  |
| `/api/v1/pods`                   | Pod resources          |
| `/api/v1/services`               | Services               |
| `/api/v1/namespaces`             | Namespaces             |
| `/api/v1/endpoints`              | Endpoints              |
| `/api/v1/configmaps`             | ConfigMaps             |
| `/api/v1/secrets`                | Secrets                |
| `/api/v1/persistentvolumes`      | PersistentVolumes      |
| `/api/v1/persistentvolumeclaims` | PersistentVolumeClaims |
| `/api/v1/serviceaccounts`        | ServiceAccounts        |

---

### `/apis`: named group

- apps API
  - Workload controllers.

| **API Path**                        | **Description**                  |
| ----------------------------------- | -------------------------------- |
| `/apis/apps/v1/replicasets`         | ReplicaSets                      |
| `/apis/apps/v1/deployments`         | Deployments                      |
| `/apis/apps/v1/daemonsets`          | DaemonSets                       |
| `/apis/apps/v1/statefulsets`        | StatefulSets                     |
| `/apis/apps/v1/controllerrevisions` | Revision history for controllers |

- batch API
  - Jobs and CronJobs.

| **API Path**              | **Description** |
| ------------------------- | --------------- |
| `/apis/batch/v1/jobs`     | Jobs            |
| `/apis/batch/v1/cronjobs` | CronJobs        |

- networking.k8s.io API
  - Networking policies, Ingress, etc.

| **API Path**                                 | **Description**   |
| -------------------------------------------- | ----------------- |
| `/apis/networking.k8s.io/v1/networkpolicies` | Network policies  |
| `/apis/networking.k8s.io/v1/ingresses`       | Ingress resources |
| `/apis/networking.k8s.io/v1/ingressclasses`  | IngressClass      |

- policy API
  - Pod disruption budgets.

| **API Path**                           | **Description**               |
| -------------------------------------- | ----------------------------- |
| `/apis/policy/v1/poddisruptionbudgets` | Pod disruption budgets (PDBs) |

- rbac.authorization.k8s.io API
  - RBAC policies.

| **API Path**                                             | **Description**     |
| -------------------------------------------------------- | ------------------- |
| `/apis/rbac.authorization.k8s.io/v1/roles`               | Namespaced Roles    |
| `/apis/rbac.authorization.k8s.io/v1/clusterroles`        | Cluster roles       |
| `/apis/rbac.authorization.k8s.io/v1/rolebindings`        | RoleBindings        |
| `/apis/rbac.authorization.k8s.io/v1/clusterrolebindings` | ClusterRoleBindings |

- autoscaling API
  - HPA / VPA.

| **API Path**                                    | **Description**                     |
| ----------------------------------------------- | ----------------------------------- |
| `/apis/autoscaling/v1/horizontalpodautoscalers` | HPA (CPU-based)                     |
| `/apis/autoscaling/v2/horizontalpodautoscalers` | HPA (CPU + memory + custom metrics) |

- storage.k8s.io API
  - Storage classes, CSIs.

| **API Path**                                | **Description**                |
| ------------------------------------------- | ------------------------------ |
| `/apis/storage.k8s.io/v1/storageclasses`    | Storage classes                |
| `/apis/storage.k8s.io/v1/volumeattachments` | CSI volume attachments         |
| `/apis/storage.k8s.io/v1/csinodes`          | Nodes that support CSI drivers |

- admissionregistration.k8s.io API
  - Webhooks.

| **API Path**                                                            | **Description**     |
| ----------------------------------------------------------------------- | ------------------- |
| `/apis/admissionregistration.k8s.io/v1/mutatingwebhookconfigurations`   | Mutating webhooks   |
| `/apis/admissionregistration.k8s.io/v1/validatingwebhookconfigurations` | Validating webhooks |

- apiextensions.k8s.io API
  - CRDs.

| **API Path**                                              | **Description**                    |
| --------------------------------------------------------- | ---------------------------------- |
| `/apis/apiextensions.k8s.io/v1/customresourcedefinitions` | Custom Resource Definitions (CRDs) |

- metrics.k8s.io API

| **API Path**                         | **Description**       |
| ------------------------------------ | --------------------- |
| `/apis/metrics.k8s.io/v1beta1/nodes` | Node CPU/Memory usage |
| `/apis/metrics.k8s.io/v1beta1/pods`  | Pod CPU/Memory usage  |

- Coordination API
  - Used internally for leader election.

| **API Path**                          | **Description**        |
| ------------------------------------- | ---------------------- |
| `/apis/coordination.k8s.io/v1/leases` | Leader election leases |

---

## Connection

```sh
# method 1:
# access with endpint with credential
curl https://localhost:6443 -k --key admin.key --cert admin.crt --cacert ca.cert

# method 2:
# enable proxy
kubectl proxy
# starting to server on 127.0.0.1:8001

# access with proxy with kubeconfig automatically
curl https://localhost:8001 -k
```

---
