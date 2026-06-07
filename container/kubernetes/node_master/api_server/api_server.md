# Kubernetes Cluster - API Server

[Back](../../index.md)

- [Kubernetes Cluster - API Server](#kubernetes-cluster---api-server)
  - [kube-apiserver Configuration](#kube-apiserver-configuration)
    - [Installation](#installation)
  - [API Server](#api-server)
  - [API Groups](#api-groups)
    - [`/api`: core group](#api-core-group)
    - [`/apis`: named group](#apis-named-group)
  - [Connection](#connection)

---

## kube-apiserver Configuration

- `kube-apiserver`
  - the front end of the Kubernetes control plane.
  - It receives API requests, authenticates users/components, authorizes actions, applies admission control, and reads/writes cluster state to etcd.

---

- 1. Network / Serving

| Option                   | Description                                                                       |
| ------------------------ | --------------------------------------------------------------------------------- |
| `--advertise-address`    | IP address advertised to other cluster members. Must be reachable by the cluster. |
| `--secure-port`          | HTTPS port used by the API server, commonly `6443`.                               |
| `--tls-cert-file`        | TLS certificate used by the API server for HTTPS.                                 |
| `--tls-private-key-file` | Private key for the API server TLS certificate.                                   |
| `--allow-privileged`     | Allows privileged containers. Default: `false`.                                   |

- 2. Authentication

| Option                          | Description                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| `--client-ca-file`              | CA certificate used to authenticate clients that present client certificates.             |
| `--enable-bootstrap-token-auth` | Enables bootstrap token authentication, commonly used when worker nodes join the cluster. |

- 3. Authorization

| Option                 | Description                                                          |
| ---------------------- | -------------------------------------------------------------------- |
| `--authorization-mode` | Defines authorization mechanisms. Common kubeadm value: `Node,RBAC`. |

- 4. Admission Control

| Option                       | Description                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `--enable-admission-plugins` | Enables admission plugins such as `NodeRestriction`. Admission runs after authentication and authorization. |

- 5. Etcd Connection

| Option            | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `--etcd-servers`  | List of etcd server URLs used by the API server.                   |
| `--etcd-cafile`   | CA certificate used to verify the etcd server certificate.         |
| `--etcd-certfile` | Client certificate used by the API server to authenticate to etcd. |
| `--etcd-keyfile`  | Client private key used with `--etcd-certfile`.                    |

- 6. Kubelet Connection

| Option                              | Description                                                                 |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `--kubelet-client-certificate`      | Client certificate used by the API server when connecting to kubelets.      |
| `--kubelet-client-key`              | Client private key used with `--kubelet-client-certificate`.                |
| `--kubelet-preferred-address-types` | Preferred node address types used when the API server connects to kubelets. |

- 7. API Aggregation / Front Proxy

| Option                                 | Description                                                                        |
| -------------------------------------- | ---------------------------------------------------------------------------------- |
| `--proxy-client-cert-file`             | Client certificate used by the API server when proxying to aggregated API servers. |
| `--proxy-client-key-file`              | Private key for `--proxy-client-cert-file`.                                        |
| `--requestheader-client-ca-file`       | CA bundle used to verify front-proxy client certificates.                          |
| `--requestheader-allowed-names`        | Allowed client certificate Common Names for request-header authentication.         |
| `--requestheader-extra-headers-prefix` | Header prefixes used for extra user information.                                   |
| `--requestheader-group-headers`        | Headers used to identify user groups.                                              |
| `--requestheader-username-headers`     | Headers used to identify the username.                                             |

- 8. Service Account Tokens

| Option                               | Description                                             |
| ------------------------------------ | ------------------------------------------------------- |
| `--service-account-issuer`           | Issuer identity placed in service account tokens.       |
| `--service-account-key-file`         | Key file used to verify service account tokens.         |
| `--service-account-signing-key-file` | Private key used to sign issued service account tokens. |

- 9. Service Networking

| Option                       | Description                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| `--service-cluster-ip-range` | CIDR range used to assign ClusterIP addresses to Services. Must not overlap with node or pod networks. |

---

### Installation

- Option A: use `kubeadm` to run as static pod
  - 1. configure `/etc/kubernetes/manifests/kube-apiserver.yaml`
  - 2. `kubelet` watches manifest
  - 3. `containerd` runs kube-apiserver container
  - 4. mirror Pod appears in `kube-system`
- Option B: use binary to run as systemd services
  - `/etc/systemd/system/kube-apiserver.service`
  - `systemd starts kube-apiserver`
  - `kube-apiserver` runs as Linux process

---

- example: kubeadm

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: kube-apiserver
      image: registry.k8s.io/kube-apiserver:v1.32.11
      command:
        - kube-apiserver
        - --advertise-address=192.168.10.150
        - --allow-privileged=true
        - --authorization-mode=Node,RBAC
        - --client-ca-file=/etc/kubernetes/pki/ca.crt
        - --enable-admission-plugins=NodeRestriction
        - --enable-bootstrap-token-auth=true
        - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
        - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
        - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
        - --etcd-servers=https://127.0.0.1:2379
        - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
        - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
        - --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
        - --requestheader-allowed-names=front-proxy-client
        - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
        - --requestheader-extra-headers-prefix=X-Remote-Extra-
        - --requestheader-group-headers=X-Remote-Group
        - --requestheader-username-headers=X-Remote-User
        - --secure-port=6443
        - --service-account-issuer=https://kubernetes.default.svc.cluster.local
        - --service-account-key-file=/etc/kubernetes/pki/sa.pub
        - --service-account-signing-key-file=/etc/kubernetes/pki/sa.key
        - --service-cluster-ip-range=10.96.0.0/12
        - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
        - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
      volumeMounts:
        - mountPath: /etc/ssl/certs
          name: ca-certs
          readOnly: true
        - mountPath: /etc/ca-certificates
          name: etc-ca-certificates
          readOnly: true
        - mountPath: /etc/kubernetes/pki
          name: k8s-certs
          readOnly: true
        - mountPath: /usr/local/share/ca-certificates
          name: usr-local-share-ca-certificates
          readOnly: true
        - mountPath: /usr/share/ca-certificates
          name: usr-share-ca-certificates
          readOnly: true
```

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
