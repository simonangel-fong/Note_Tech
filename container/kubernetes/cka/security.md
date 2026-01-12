# CKA - Security

[Back](../index.md)

- [CKA - Security](#cka---security)
  - [Security](#security)
    - [Task: Security Standard](#task-security-standard)
    - [Task: RBAC](#task-rbac)
    - [Task: RBAC](#task-rbac-1)

---

## Security

### Task: Security Standard

Enforce the Restricted Pod Security Standard on the namespace restricted-ns.
Pods in that namespace cannot:
. have privileged access
· host networking
. have any elevated rights

---

- Setup env

```sh
kubectl create ns restricted-ns
```

---

- Solution

- ref: https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/

```sh
# label ns as restricted
kubectl label --overwrite ns restricted-ns pod-security.kubernetes.io/enforce=restricted
# namespace/restricted-ns labeled

# confirm
kubectl describe ns restricted-ns
# Labels:       kubernetes.io/metadata.name=restricted-ns
#               pod-security.kubernetes.io/enforce=restricted
```

- If to set it to a specific version

```sh
kubectl label --overwrite ns restricted-ns pod-security.kubernetes.io/enforce-version=v1.35
# namespace/restricted-ns labeled

kubectl describe ns restricted-ns
# Labels:       kubernetes.io/metadata.name=restricted-ns
#               pod-security.kubernetes.io/enforce-version=v1.35

```

---

### Task: RBAC

CKA EXAM OBJECTIVE: Manage role based access control (RBAC)
TASK:

1. Create a ClusterRole named app-creator that allows create permissions for Deployments, StatefulSets, and DaemonSets.
2. Create a ServiceAccount named app-dev.
3. Bind the ServiceAccount app-dev to the ClusterRole app-creator using a ClusterRoleBinding.

---

- Solution

```sh
kubectl create clusterrole app-creator --verb=create --resource=deployments,statefulsets,daemonsets --dry-run=client -o yaml > clusterrole.yaml

k apply -f clusterrole.yaml
# clusterrole.rbac.authorization.k8s.io/app-creator created

k describe clusterrole app-creator
# Name:         app-creator
# Labels:       <none>
# Annotations:  <none>
# PolicyRule:
#   Resources          Non-Resource URLs  Resource Names  Verbs
#   ---------          -----------------  --------------  -----
#   daemonsets.apps    []                 []              [create]
#   deployments.apps   []                 []              [create]
#   statefulsets.apps  []                 []              [create]

kubectl create serviceaccount app-dev
# serviceaccount/app-dev created

kubectl describe sa app-dev
# Name:                app-dev
# Namespace:           default
# Labels:              <none>
# Annotations:         <none>
# Image pull secrets:  <none>
# Mountable secrets:   <none>
# Tokens:              <none>
# Events:              <none>


kubectl create clusterrolebinding app-creator-binding --clusterrole=app-creator --user=app-dev
# clusterrolebinding.rbac.authorization.k8s.io/app-creator-binding created

kubectl describe clusterrolebinding app-creator-binding
# Name:         app-creator-binding
# Labels:       <none>
# Annotations:  <none>
# Role:
#   Kind:  ClusterRole
#   Name:  app-creator
# Subjects:
#   Kind  Name     Namespace
#   ----  ----     ---------
#   User  app-dev

```

### Task: RBAC

Context
为部署流水线创建一个新的 ClusterRole 并将其绑定到范围为特定的 namespace 的特定 ServiceAccount。

Task
创建一个名为 deployment-clusterrole 且仅允许创建以下资源类型的新 ClusterRole：
Deployment
StatefulSet
DaemonSet
在现有的 namespace app-team1 中创建一个名为 cicd-token 的新 ServiceAccount。
限于 namespace app-team1 中，将新的 ClusterRole deployment-clusterrole 绑定到新的 ServiceAccount cicd-token。Copy

---

```sh
# create cluster role
kubectl create clusterrole deployment-clusterrole --resource=deployment,statefulsets,daemonsets --verb=create

# create sa
kubectl create sa cicd-token -n app-team1

# cluster role binding
kubectl create rolebinding cicd-token-rolebinding --clusterrole=deployment-clusterrole --serviceaccount=cicd-token -n app-team1

# confirm
kubectl -n app-team1 describe rolebinding cicd-token-rolebinding

```

---
