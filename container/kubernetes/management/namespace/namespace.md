# Kubernetes Namespace

[Back](../../index.md)

- [Kubernetes Namespace](#kubernetes-namespace)
  - [Namespace](#namespace)
    - [In DNS](#in-dns)
    - [Built-in Namespaces](#built-in-namespaces)
    - [Declarative Method](#declarative-method)
    - [Imperative Commands](#imperative-commands)
  - [Lab: Built-in Namespace](#lab-built-in-namespace)
    - [`default` Namespace](#default-namespace)
    - [`kube-system` Namespace](#kube-system-namespace)
    - [`kube-public` Namespace](#kube-public-namespace)
    - [`kube-node-lease` Namespace](#kube-node-lease-namespace)
  - [Lab: Create Namespace(Imperative Method)](#lab-create-namespaceimperative-method)
  - [Lab: Create namespace(Declarative Method)](#lab-create-namespacedeclarative-method)
  - [Lab: Set default for a context](#lab-set-default-for-a-context)

---

## Namespace

- `Namespace`

  - a **mechanism** used to **partition** a single `physical cluster` into multiple **isolated** `virtual clusters`.
  - a **logical partition** of the cluster that **groups resources** (like `Pods`, `Services`, `Deployments`)
  - helps divide cluster resources between multiple users, teams, or applications.

- **Role** of a Namespace

  - **Organize resources**
    - **Group** related Pods, Services, Deployments, etc.
      - e.g., separate dev, test, prod environments in one cluster.
  - **Avoid naming conflicts**
    - can have two `Services` both called web, as long as they are in **different** `namespaces`.
  - **Enable fine-grained access control (RBAC)**
    - **Permissions** can be **granted** per `namespace`.
      - e.g., Team A can only access dev namespace; Team B only prod.
  - **Support multi-tenancy**
    - Different teams/users can safely **share** the same cluster.
  - **Apply resource quotas and limits**
    - Prevent one team from consuming all cluster resources.
      - e.g., prod namespace gets more CPU/memory quota than dev.

- **Features of Namespaces**
  - **Segregation**:
    - **Logical separation** without physical isolation (still one cluster).
  - **Scoping**:
    - Resource **names** only need to be **unique** within the `namespace`, not the whole cluster.
  - **Default Assignment**:
    - If no namespace is specified, resources go into the `default namespace`.
  - **Access Control**:
    - Works with `RBAC` to **restrict access** to certain namespaces.
  - **Resource Management**:
    - **Quotas** (ResourceQuota), limits (LimitRange) can be applied per namespace.
  - **DNS Naming**: Services get names using namespace

---

### In DNS

- `resource_name.namespace.resource_type.domain`
  - e.g., `db-service.dev.svc.cluster.local`
    - resource_name: `db-service`
    - namespace: `dev`
    - resource_type: `svc`
    - domain: `cluster.local`

---

### Built-in Namespaces

- `default`
  - the default namespace
  - the “workspace” namespace used when you don’t explicitly specify one.
  - Use case:
    - Quick **testing**, running workloads **without explicit** `namespace` separation.

```sh
kubectl run nginx --image=nginx
kubectl describe pod nginx | grep "Namespace"
# Namespace:        default
```

---

- `kube-system`

  - reserved for Kubernetes system components.
  - Contains Pods and services like:
    - kube-dns (CoreDNS)
    - kube-proxy
    - Control plane add-ons (metrics-server, etc.)
  - should not modify resources here unless you know what you’re doing.

- `kube-public`

  - A special namespace that is **readable** by **all users**, including those **not authenticated**.
  - Used for **cluster-wide public info**.
    - e.g., it often holds a `ConfigMap` named cluster-info that helps bootstrap new clients.

- `kube-node-lease`
  - contains `Lease` object for each node
  - These leases are **updated periodically** by `kubelet`, and the `control plane` uses them to:
    - Determine **node heartbeat/liveness**.
    - Improve cluster scalability by reducing load on `etcd`.

---

### Declarative Method

- Create a ns

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

- CMD

```sh
kubectl create -f ns-dev.yaml
```

- Specify namespace to resource

```yaml
apiVersion: v1
kind: Pod
metadata:
  namespace: dev
```

---

### Imperative Commands

- Manage namespace

| Command                       | Description                                           |
| ----------------------------- | ----------------------------------------------------- |
| `kubectl get ns`              | List all namespaces                                   |
| `kubectl describe ns ns_name` | Show detailed information about a namespace.          |
| `kubectl create ns ns_name`   | Create a new namespace.                               |
| `kubectl delete ns ns_name`   | Delete a namespace (removes all resources inside it). |

- Manage resources in a namespace

| Command                                                    | Description                                               |
| ---------------------------------------------------------- | --------------------------------------------------------- |
| `kubectl get all -n ns_name`                               | List all resources (pods, services, etc.) in a namespace. |
| `kubectl get pods -n ns_name`                              | List all pods in a specific namespace.                    |
| `kubectl get pods --all-namespaces`                        | List all pods in all namespaces.                          |
| `kubectl config set-context --current --namespace=ns_name` | Set a default namespace for current kubectl context.      |
| `kubectl config view --minify \| grep namespace:`          | Get the namespace set as default of the current context   |
| `kubectl get pod pod_name -n ns_name`                      | Get a specific pod in a namespace.                        |
| `kubectl run test --image=nginx -n ns_name`                | Run a test pod in a given namespace.                      |
| `kubectl create -f pod.yaml --namespace=ns_name`           | Run a test pod in a given namespace.                      |

---

## Lab: Built-in Namespace

```sh
# list built-in ns
kubectl get ns
# NAME              STATUS   AGE
# default           Active   4d12h
# kube-node-lease   Active   4d12h
# kube-public       Active   4d12h
# kube-system       Active   4d12h
```

---

### `default` Namespace

```sh
kubectl describe ns default
# Name:         default
# Labels:       kubernetes.io/metadata.name=default
# Annotations:  <none>
# Status:       Active

kubectl get all -n default
# NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   4d12h
```

---

### `kube-system` Namespace

```sh
kubectl describe ns kube-system
# Name:         kube-system
# Labels:       kubernetes.io/metadata.name=kube-system
# Annotations:  <none>
# Status:       Active

# No resource quota.

# No LimitRange resource.

kubectl get all -n kube-system
# NAME                                         READY   STATUS    RESTARTS       AGE
# pod/coredns-668d6bf9bc-2ztgc                 1/1     Running   4 (38m ago)    4d12h
# pod/coredns-668d6bf9bc-sb6nr                 1/1     Running   4 (38m ago)    4d12h
# pod/etcd-docker-desktop                      1/1     Running   4 (38m ago)    4d12h
# pod/kube-apiserver-docker-desktop            1/1     Running   4 (38m ago)    4d12h
# pod/kube-controller-manager-docker-desktop   1/1     Running   4 (38m ago)    4d12h
# pod/kube-proxy-l9pz4                         1/1     Running   4 (38m ago)    4d12h
# pod/kube-scheduler-docker-desktop            1/1     Running   7 (38m ago)    4d12h
# pod/storage-provisioner                      1/1     Running   11 (38m ago)   4d12h
# pod/vpnkit-controller                        1/1     Running   4 (38m ago)    4d12h

# NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
# service/kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   4d12h

# NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# daemonset.apps/kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   4d12h

# NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/coredns   2/2     2            2           4d12h

# NAME                                 DESIRED   CURRENT   READY   AGE
# replicaset.apps/coredns-668d6bf9bc   2         2         2       4d1
```

---

### `kube-public` Namespace

```sh
kubectl describe ns kube-public
# Name:         kube-public
# Labels:       kubernetes.io/metadata.name=kube-public
# Annotations:  <none>
# Status:       Active

# No resource quota.

# No LimitRange resource.

kubectl get all -n kube-public
# No resources found in kube-public namespace.
```

---

### `kube-node-lease` Namespace

```sh
kubectl describe ns kube-node-lease
# Name:         kube-node-lease
# Labels:       kubernetes.io/metadata.name=kube-node-lease
# Annotations:  <none>
# Status:       Active

# No resource quota.

# No LimitRange resource.

kubectl get all -n kube-node-lease
# No resources found in kube-node-lease namespace.
```

---

## Lab: Create Namespace(Imperative Method)

```sh
kubectl create ns myns
# namespace/myns created
kubectl get ns | grep myns
# myns              Active   41m
kubectl describe ns myns
# Name:         myns
# Labels:       kubernetes.io/metadata.name=myns
# Annotations:  <none>
# Status:       Active

# No resource quota.

# No LimitRange resource.

kubectl run nginx --image=nginx -n myns
# pod/nginx created

kubectl get pod
# No resources found in default namespace.

kubectl get pod -n myns
# NAME    READY   STATUS    RESTARTS   AGE
# nginx   1/1     Running   0          45s

kubectl describe pod nginx -n myns
# Name:             nginx
# Namespace:        myns
# Priority:         0
# Service Account:  default
# Node:             docker-desktop/192.168.65.3
# Start Time:       Mon, 29 Sep 2025 12:04:36 -0400
# Labels:           run=nginx
# Annotations:      <none>
# Status:           Running
# IP:               10.1.2.175
# IPs:
#   IP:  10.1.2.175
# Containers:
#   nginx:
```

---

- Remove:
  - When removing ns, the related resources will be removed as well.

```sh
# all pods in all ns
kubectl get pod --all-namespaces
# NAMESPACE     NAME                                     READY   STATUS    RESTARTS        AGE
# kube-system   coredns-668d6bf9bc-2ztgc                 1/1     Running   4 (137m ago)    4d14h
# kube-system   coredns-668d6bf9bc-sb6nr                 1/1     Running   4 (137m ago)    4d14h
# kube-system   etcd-docker-desktop                      1/1     Running   4 (137m ago)    4d14h
# kube-system   kube-apiserver-docker-desktop            1/1     Running   4 (137m ago)    4d14h
# kube-system   kube-controller-manager-docker-desktop   1/1     Running   4 (137m ago)    4d14h
# kube-system   kube-proxy-l9pz4                         1/1     Running   4 (137m ago)    4d14h
# kube-system   kube-scheduler-docker-desktop            1/1     Running   7 (137m ago)    4d14h
# kube-system   storage-provisioner                      1/1     Running   11 (136m ago)   4d14h
# kube-system   vpnkit-controller                        1/1     Running   4 (137m ago)    4d14h
# myns          nginx                                    1/1     Running   0               31m

kubectl delete ns myns
# namespace "myns" deleted

# all pods in all ns
kubectl get pod --all-namespaces
# NAMESPACE     NAME                                     READY   STATUS    RESTARTS        AGE
# kube-system   coredns-668d6bf9bc-2ztgc                 1/1     Running   4 (139m ago)    4d14h
# kube-system   coredns-668d6bf9bc-sb6nr                 1/1     Running   4 (139m ago)    4d14h
# kube-system   etcd-docker-desktop                      1/1     Running   4 (139m ago)    4d14h
# kube-system   kube-apiserver-docker-desktop            1/1     Running   4 (139m ago)    4d14h
# kube-system   kube-controller-manager-docker-desktop   1/1     Running   4 (139m ago)    4d14h
# kube-system   kube-proxy-l9pz4                         1/1     Running   4 (139m ago)    4d14h
# kube-system   kube-scheduler-docker-desktop            1/1     Running   7 (139m ago)    4d14h
# kube-system   storage-provisioner                      1/1     Running   11 (138m ago)   4d14h
# kube-system   vpnkit-controller                        1/1     Running   4 (139m ago)    4d14h
```

---

## Lab: Create namespace(Declarative Method)

- `ns-dev.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

- `pod-nginx.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-nginx
  namespace: dev
  labels:
    app: nginx
spec:
  containers:
    - image: nginx
      name: nginx-con
```

```sh
kubectl apply -f .
# namespace/dev created
# pod/pod-nginx created

kubectl get pod
# No resources found in default namespace.

kubectl get pod -n dev
# NAME        READY   STATUS    RESTARTS   AGE
# pod-nginx   1/1     Running   0          3m11s

kubectl delete -f .
# namespace "dev" deleted
# pod "pod-nginx" deleted
```

---

## Lab: Set default for a context

```sh
kubectl config current-context
# docker-desktop

kubectl get pod
# No resources found in default namespace.

# set ns
kubectl config set-context docker-desktop --namespace=dev

kubectl get pod
# NAME        READY   STATUS    RESTARTS   AGE
# pod-nginx   1/1     Running   0          8m35s

kubectl config set-context docker-desktop --namespace=default

# get all pods in all ns
kubectl get pods --all-namespaces
# NAMESPACE     NAME                                     READY   STATUS    RESTARTS        AGE
# dev           pod-nginx                                1/1     Running   0               10m
# kube-system   coredns-668d6bf9bc-2ztgc                 1/1     Running   4 (133m ago)    4d14h
# kube-system   coredns-668d6bf9bc-sb6nr                 1/1     Running   4 (133m ago)    4d14h
# kube-system   etcd-docker-desktop                      1/1     Running   4 (133m ago)    4d14h
# kube-system   kube-apiserver-docker-desktop            1/1     Running   4 (133m ago)    4d14h
# kube-system   kube-controller-manager-docker-desktop   1/1     Running   4 (133m ago)    4d14h
# kube-system   kube-proxy-l9pz4                         1/1     Running   4 (133m ago)    4d14h
# kube-system   kube-scheduler-docker-desktop            1/1     Running   7 (133m ago)    4d14h
# kube-system   storage-provisioner                      1/1     Running   11 (132m ago)   4d14h
# kube-system   vpnkit-controller                        1/1     Running   4 (133m ago)    4d14h
# myns          nginx                                    1/1     Running   0               27m
```
