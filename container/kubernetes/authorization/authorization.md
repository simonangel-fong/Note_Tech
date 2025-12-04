# Kubernetes - Authorization

[Back](../index.md)

- [Kubernetes - Authorization](#kubernetes---authorization)
  - [API Groups](#api-groups)
    - [`/api`: core group](#api-core-group)
    - [`/apis`: named group](#apis-named-group)
  - [COnnection](#connection)
  - [Authorization](#authorization)
  - [`Role-based access control`(`RBAC`)](#role-based-access-controlrbac)
  - [Lab: Authorization](#lab-authorization)
- [get the api server authorization mode](#get-the-api-server-authorization-mode)
- [--authorization-mode=Node,RBAC](#--authorization-modenoderbac)
- [get the authorization mode by process](#get-the-authorization-mode-by-process)
- [list role](#list-role)
- [get a role](#get-a-role)
- [NAME         CREATED AT](#name---------created-at)
- [kube-proxy   2025-11-28T02:05:01Z](#kube-proxy---2025-11-28t020501z)
- [get detail](#get-detail)
- [Name:         kube-proxy](#name---------kube-proxy)
- [Labels:       ](#labels-------)
- [Annotations:  ](#annotations--)
- [PolicyRule:](#policyrule)
- [Resources   Non-Resource URLs  Resource Names  Verbs](#resources---non-resource-urls--resource-names--verbs)
- [---------   -----------------  --------------  -----](#----------------------------------------------------)
- [configmaps  \[\]                 \[kube-proxy\]    \[get\]](#configmaps-------------------kube-proxy----get)
- [get the related rolebinding](#get-the-related-rolebinding)
- [NAMESPACE     NAME                                                ROLE                                                  AGE](#namespace-----name------------------------------------------------role--------------------------------------------------age)
- [proxy         kube-proxy                                          Role/kube-proxy                                       27m](#proxy---------kube-proxy------------------------------------------rolekube-proxy---------------------------------------27m)
- [get the related group](#get-the-related-group)
- [stem](#stem)
- [Name:         kube-proxy](#name---------kube-proxy-1)
- [Labels:       ](#labels--------1)
- [Annotations:  ](#annotations---1)
- [Role:](#role)
- [Kind:  Role](#kind--role)
- [Name:  kube-proxy](#name--kube-proxy)
- [Subjects:](#subjects)
- [Kind   Name                                             Namespace](#kind---name---------------------------------------------namespace)
- [----   ----                                             ---------](#-----------------------------------------------------------------)
- [Group  system:bootstrappers:kubeadm:default-node-token](#group--systembootstrapperskubeadmdefault-node-token)
- [check a user's access](#check-a-users-access)
- [create a role in default ns for dev-user to list pod](#create-a-role-in-default-ns-for-dev-user-to-list-pod)
- [apiVersion: rbac.authorization.k8s.io/v1](#apiversion-rbacauthorizationk8siov1)
- [kind: Role](#kind-role)
- [metadata:](#metadata)
- [name: developer](#name-developer)
- [rules:](#rules)
- [- apiGroups:](#--apigroups)
- [- ""](#--)
- [resources:](#resources)
- [- pods](#--pods)
- [verbs:](#verbs)
- [- list](#--list)
- [- create](#--create)
- [- delete](#--delete)
- [create role](#create-role)
- [role.rbac.authorization.k8s.io/developer created](#rolerbacauthorizationk8siodeveloper-created)
- [create role binding](#create-role-binding)
- [apiVersion: rbac.authorization.k8s.io/v1](#apiversion-rbacauthorizationk8siov1-1)
- [kind: RoleBinding](#kind-rolebinding)
- [metadata:](#metadata-1)
- [name: dev-user-binding](#name-dev-user-binding)
- [roleRef:](#roleref)
- [apiGroup: rbac.authorization.k8s.io](#apigroup-rbacauthorizationk8sio)
- [kind: Role](#kind-role-1)
- [name: developer](#name-developer-1)
- [subjects:](#subjects-1)
- [- apiGroup: rbac.authorization.k8s.io](#--apigroup-rbacauthorizationk8sio)
- [kind: User](#kind-user)
- [name: dev-user](#name-dev-user)
- [create rolebinding](#create-rolebinding)
- [rolebinding.rbac.authorization.k8s.io/dev-user-binding created](#rolebindingrbacauthorizationk8siodev-user-binding-created)
- [confirm](#confirm)

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

## COnnection

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

## Authorization

- `Authorization`

  - evaluates all of the request attributes against all policies, potentially also consulting external services, and then allows or denies the request.
  - within the API server
  - takes place following authentication.
  - denied by default.

- authorization mode

  - Node(Node authorizer)
  - ABAC(Attribute-based access control)
  - RBAC(Role-based access control)
  - Webhook(Webhook authorization)
  - AlwaysAllow (always allows requests;)
  - AlwaysDeny (always denies requests)

---

- `Node authorizer`
  - kubelet access to api server
  - request name: `system:node`
  - group: `system:nodes`

---

- `Attribute-based access control`(`ABAC`)
  - External access to the API
  - controled by a JSON policy file
    - `{"kind": "Policy", "spec": {"user": "dev-user", "namespace": "*", "resource":"pods","apiGroup":"*"}}`
  - hard to use:
    - require to edit policy manually and restart API server

---

- `Role-based access control`(`RBAC`)
  - controll the access to the API server by defining a role

---

- `Webhook authorization`(`Webhook`)
  - manage authorization externally
  - e.g., `Open Policy Agent`, a 3-rd party tools helps with admission control and authorization.

---

- API service

```conf
ExecStart=/usr/local/bin/kube-apiserver \\
--advertise-address=${INTERNAL_IP} \\
--allow-privileged=true \\
--apiserver-count=3 \\
--authorization-mode=AlwaysAllow \\   # default mode; can be multiple modes with order: --authorization-mode=Node,RBAC,Webhook
--bind-address=0.0.0.0 \\
--enable-swagger-ui=true \\
--etcd-cafile=/var/lib/kubernetes/ca.pem \\
--etcd-certfile=/var/lib/kubernetes/apiserver-etcd-client.crt \\
--etcd-keyfile=/var/lib/kubernetes/apiserver-etcd-client.key \\
--etcd-servers=https://127.0.0.1:2379 \\
--event-ttl=1h \\
--kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\
--kubelet-client-certificate=/var/lib/kubernetes/apiserver-etcd-client.crt \\
--kubelet-client-key=/var/lib/kubernetes/apiserver-etcd-client.key \\
--service-node-port-range=30000-32767 \\
--client-ca-file=/var/lib/kubernetes/ca.pem \\
--tls-cert-file=/var/lib/kubernetes/apiserver.crt \\
--tls-private-key-file=/var/lib/kubernetes/apiserver.key \\
--v=2

```

- for `--authorization-mode=Node,RBAC,Webhook`,
  - the access tries to be handled by the node mode first, then RBAC, and Webhook
  - it the previous one denied, check the next mode
  - check stops when the access is approved.

---

## `Role-based access control`(`RBAC`)

- A `role` is created by defining a **role oject**.
- each role has 3 sections:

  - API Group
  - Resource
  - Verbs

- Example: Create a role

```yaml
# developer-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: developer
rules:
  - apiGroups: [""] # "" indicates the core API group
    resources: ["pods"]
    verbs: ["list", "get", "create", "update", "dalete"]
    resourceNames: ["blue", "orange"] # optional; can specific a typical resource with the name
  - apiGroups: [""]
    resource: ["ConfigMap"]
    verb: ["create"]
```

```sh
kubectl create -f developer-role.yaml
```

- Link the created role with a user

  - using `RoleBinding` Object

- Example

```yaml
# devuser-developer-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
  namespace: default
# user details
subjects:
  - kind: User
    name: dev-user
    apiGroup: rbac.authorization.k8s.io
# role details
roleRef:
  kind: Role #this must be Role or ClusterRole
  name: developer # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
```

- Create

```sh
kubectl create -f devuser-developer-binding.yaml
```

- View the RBAC

```sh
kubectl get roles
kubectl get rolebindings
kubectl describe role developer
kubectl describe rolebindings devuser-developer-binding

# check whether the current user has the access to a specific resources.
kubectl auth can-i create deployment
# test a specific user's access
kubectl auth can-i create deployment --as dev-user
kubectl auth can-i create deployment --as dev-user -n test
```

---

## Lab: Authorization

```sh
# get the api server authorization mode
cat kube-apiserver.yaml | grep authorization
# --authorization-mode=Node,RBAC

# get the authorization mode by process
ps -aux | grep kube-apiserver

# list role
kubectl get role

# get a role
kubectl get role kube-proxy -n kube-system
# NAME         CREATED AT
# kube-proxy   2025-11-28T02:05:01Z

# get detail
kubectl describe role kube-proxy -n kube-system
# Name:         kube-proxy
# Labels:       <none>
# Annotations:  <none>
# PolicyRule:
  # Resources   Non-Resource URLs  Resource Names  Verbs
  # ---------   -----------------  --------------  -----
  # configmaps  []                 [kube-proxy]    [get]

# get the related rolebinding
kubectl get rolebinding -n kube-system| grep kube-proxy
# NAMESPACE     NAME                                                ROLE                                                  AGE
# proxy         kube-proxy                                          Role/kube-proxy                                       27m

# get the related group
kubectl describe rolebinding kube-proxy -n kube-system 
# stem 
# Name:         kube-proxy
# Labels:       <none>
# Annotations:  <none>
# Role:
  # Kind:  Role
  # Name:  kube-proxy
# Subjects:
  # Kind   Name                                             Namespace
  # ----   ----                                             ---------
  # Group  system:bootstrappers:kubeadm:default-node-token  

# check a user's access
kubectl auth can-i list pod --as dev-user
kubectl list pod --as dev-user

# create a role in default ns for dev-user to list pod
kubectl create role developer --verb=list --verb=create --verb=delete --resource=pod --dry-run=client -o yaml > role.yaml

cat role.yaml
# apiVersion: rbac.authorization.k8s.io/v1
# kind: Role
# metadata:
#   name: developer
# rules:
# - apiGroups:
#   - ""
#   resources:
#   - pods
#   verbs:
#   - list
#   - create
#   - delete

# create role
kubectl apply -f role.yaml
# role.rbac.authorization.k8s.io/developer created

# create role binding
kubectl create rolebinding dev-user-binding --role=developer --user=dev-user --dry-run=client -o yaml > rbd.yaml

cat rbd.yaml
# apiVersion: rbac.authorization.k8s.io/v1
# kind: RoleBinding
# metadata:
#   name: dev-user-binding
# roleRef:
#   apiGroup: rbac.authorization.k8s.io
#   kind: Role
#   name: developer
# subjects:
# - apiGroup: rbac.authorization.k8s.io
#   kind: User
#   name: dev-user

# create rolebinding
kubectl apply -f rbd.yaml
# rolebinding.rbac.authorization.k8s.io/dev-user-binding created

kubectl edit role developer -n blue

# confirm
kubectl auth can-i list pod --as dev-user