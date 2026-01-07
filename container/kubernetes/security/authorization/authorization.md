# Kubernetes - Authorization

[Back](../../index.md)

- [Kubernetes - Authorization](#kubernetes---authorization)
  - [Authorization](#authorization)
  - [Authorization Modes](#authorization-modes)
    - [`Node authorizer`](#node-authorizer)
    - [`Attribute-based access control`(`ABAC`)](#attribute-based-access-controlabac)
    - [`Role-based access control`(`RBAC`)](#role-based-access-controlrbac)
    - [`Webhook authorization`(`Webhook`)](#webhook-authorizationwebhook)
  - [API service](#api-service)
  - [`Role-based access control`(`RBAC`)](#role-based-access-controlrbac-1)
  - [Lab: Authorization](#lab-authorization)

---

## Authorization

- `Authorization`

  - **evaluates** all of the **request attributes** against **policies**, potentially also consulting external services, and then **allows** or **denies** the request.
  - takes place **following** `authentication` within the `API server`

- **By default**:

  - access is denied

---

## Authorization Modes

- The Kubernetes API server may **authorize a request** using one of several authorization modes:

  - `AlwaysAllow`
    - **allows all** requests
    - brings security risks.
  - `AlwaysDeny`
    - **blocks all** requests
  - `ABAC (attribute-based access control)`

    - defines an **access control paradigm** whereby access rights are granted to users **through the use of policies** which combine **attributes** together.
    - The **policies** can use any type of **attributes** (user attributes, resource attributes, object, environment attributes, etc).

  - `RBAC (role-based access control)`

    - a method of **regulating access** to computer or network resources **based on the roles of individual users** within an enterprise.
    - **access** is the **ability** of an individual user to **perform a specific task**, such as view, create, or modify a file.
    - use `rbac.authorization.k8s.io` API group to drive **authorization decisions**, allowing you to dynamically configure permission policies through the Kubernetes API.

  - `Node`
    - grants permissions to `kubelets` **based on the pods they are scheduled to run.**
  - `Webhook`
    - makes a **synchronous HTTP callout**, blocking the request until the `remote HTTP service` responds to the query.
    - can write your own software to handle the callout, or use solutions from the ecosystem.

---

### `Node authorizer`

- `kubelet` access to api server
- request name: `system:node`
- group: `system:nodes`

---

### `Attribute-based access control`(`ABAC`)

- External access to the API
- controled by a JSON policy file
  - `{"kind": "Policy", "spec": {"user": "dev-user", "namespace": "*", "resource":"pods","apiGroup":"*"}}`
- hard to use:
  - require to edit policy manually and restart API server

---

### `Role-based access control`(`RBAC`)

- controll the access to the API server by defining a role

---

### `Webhook authorization`(`Webhook`)

- manage authorization externally
- e.g., `Open Policy Agent`, a 3-rd party tools helps with admission control and authorization.

---

## API service

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
```
