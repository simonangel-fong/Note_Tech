# Kubernetes Security: RBAC Authorization

[Back](../../index.md)

- [Kubernetes Security: RBAC Authorization](#kubernetes-security-rbac-authorization)
  - [RBAC Authorization](#rbac-authorization)
    - [Cluster Resources \& Namespace Resources](#cluster-resources--namespace-resources)
    - [Resource Verbs](#resource-verbs)
    - [Lab: Cluster Resources \& Namespace Resources](#lab-cluster-resources--namespace-resources)
  - [`Role` \& `RoleBinding`](#role--rolebinding)
    - [Declarative Manifest](#declarative-manifest)
  - [`ClusterRole` \& `ClusterRoleBinding`](#clusterrole--clusterrolebinding)
    - [Declarative Manifest](#declarative-manifest-1)
    - [Imperative Commands](#imperative-commands)
  - [`Role` and `RoleBinding`](#role-and-rolebinding)
    - [Declararive Manifest](#declararive-manifest)
    - [Imperative Commands](#imperative-commands-1)

---

## RBAC Authorization

- `Role-based access control (RBAC)`

  - a method of **regulating access to resources** based on the **roles of individual users**.
  - uses the `rbac.authorization.k8s.io` API group to **drive authorization decisions**.

- To enable `RBAC`, start the API server with the `--authorization-config` flag set to a file that includes the RBAC authorizer;

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AuthorizationConfiguration
authorizers:
  - type: RBAC
```

---

- Define four kinds of Kubernetes object:
  - `Role`,
  - `ClusterRole`,
  - `RoleBinding`
  - and `ClusterRoleBinding`.

---

### Cluster Resources & Namespace Resources

- **Resources** are categorized as

  - `namespaced resources`
  - `cluster resources`

- a Kubernetes object always has to be either `namespaced` or `not namespaced`;

  - it **can't be both**.

- `Role` and `RoleBinding`

  - are used to **authorize a user** to `namespace resources`.

- `ClusterRole` and `ClusterRoleBindings`:
  - are used to **authorize a user** to `cluster resources`
  - can also be used to manage `namespace resources`.
    - e.g.,
      - `pod resources` can be defined by `cluster role`
      - the authorized user can access all the defined pod across the cluster

---

### Resource Verbs

- Common

| Verb             | Meaning                        |
| ---------------- | ------------------------------ |
| get              | Read one object                |
| list             | List many objects              |
| watch            | Subscribe to changes           |
| create           | Create new object              |
| update           | Replace object                 |
| patch            | Modify part of object          |
| delete           | Delete object                  |
| deletecollection | Delete many at once            |
| impersonate      | Act as another user            |
| escalate         | Create privileged RBAC objects |
| bind             | Bind roles                     |

- Common to return verbs
  - `kubectl api-resources -o wide`

---

### Lab: Cluster Resources & Namespace Resources

```sh
# command to list namespace resrouces
kubectl api-resources --namespaced=true
# NAME                        SHORTNAMES   APIVERSION                     NAMESPACED   KIND
# bindings                                 v1                             true         Binding
# configmaps                  cm           v1                             true         ConfigMap
# endpoints                   ep           v1                             true         Endpoints
# events                      ev           v1                             true         Event
# limitranges                 limits       v1                             true         LimitRange
# persistentvolumeclaims      pvc          v1                             true         PersistentVolumeClaim
# pods                        po           v1                             true         Pod
# podtemplates                             v1                             true         PodTemplate
# replicationcontrollers      rc           v1                             true         ReplicationController
# resourcequotas              quota        v1                             true         ResourceQuota
# secrets                                  v1                             true         Secret
# serviceaccounts             sa           v1                             true         ServiceAccount
# services                    svc          v1                             true         Service
# controllerrevisions                      apps/v1                        true         ControllerRevision
# daemonsets                  ds           apps/v1                        true         DaemonSet
# deployments                 deploy       apps/v1                        true         Deployment
# replicasets                 rs           apps/v1                        true         ReplicaSet
# statefulsets                sts          apps/v1                        true         StatefulSet
# localsubjectaccessreviews                authorization.k8s.io/v1        true         LocalSubjectAccessReview
# horizontalpodautoscalers    hpa          autoscaling/v2                 true         HorizontalPodAutoscaler
# cronjobs                    cj           batch/v1                       true         CronJob
# jobs                                     batch/v1                       true         Job
# leases                                   coordination.k8s.io/v1         true         Lease
# endpointslices                           discovery.k8s.io/v1            true         EndpointSlice
# events                      ev           events.k8s.io/v1               true         Event
# ingresses                   ing          networking.k8s.io/v1           true         Ingress
# networkpolicies             netpol       networking.k8s.io/v1           true         NetworkPolicy
# poddisruptionbudgets        pdb          policy/v1                      true         PodDisruptionBudget
# rolebindings                             rbac.authorization.k8s.io/v1   true         RoleBinding
# roles                                    rbac.authorization.k8s.io/v1   true         Role
# resourceclaims                           resource.k8s.io/v1             true         ResourceClaim
# resourceclaimtemplates                   resource.k8s.io/v1             true         ResourceClaimTemplate
# csistoragecapacities                     storage.k8s.io/v1              true         CSIStorageCapacity

# command to list cluster resrouces
kubectl api-resources --namespaced=false
# NAME                                SHORTNAMES   APIVERSION                        NAMESPACED   KIND
# componentstatuses                   cs           v1                                false        ComponentStatus
# namespaces                          ns           v1                                false        Namespace
# nodes                               no           v1                                false        Node
# persistentvolumes                   pv           v1                                false        PersistentVolume
# mutatingwebhookconfigurations                    admissionregistration.k8s.io/v1   false        MutatingWebhookConfiguration
# validatingadmissionpolicies                      admissionregistration.k8s.io/v1   false        ValidatingAdmissionPolicy
# validatingadmissionpolicybindings                admissionregistration.k8s.io/v1   false        ValidatingAdmissionPolicyBinding
# validatingwebhookconfigurations                  admissionregistration.k8s.io/v1   false        ValidatingWebhookConfiguration
# customresourcedefinitions           crd,crds     apiextensions.k8s.io/v1           false        CustomResourceDefinition
# apiservices                                      apiregistration.k8s.io/v1         false        APIService
# selfsubjectreviews                               authentication.k8s.io/v1          false        SelfSubjectReview
# tokenreviews                                     authentication.k8s.io/v1          false        TokenReview
# selfsubjectaccessreviews                         authorization.k8s.io/v1           false        SelfSubjectAccessReview
# selfsubjectrulesreviews                          authorization.k8s.io/v1           false        SelfSubjectRulesReview
# subjectaccessreviews                             authorization.k8s.io/v1           false        SubjectAccessReview
# certificatesigningrequests          csr          certificates.k8s.io/v1            false        CertificateSigningRequest
# flowschemas                                      flowcontrol.apiserver.k8s.io/v1   false        FlowSchema
# prioritylevelconfigurations                      flowcontrol.apiserver.k8s.io/v1   false        PriorityLevelConfiguration
# ingressclasses                                   networking.k8s.io/v1              false        IngressClass
# ipaddresses                         ip           networking.k8s.io/v1              false        IPAddress
# servicecidrs                                     networking.k8s.io/v1              false        ServiceCIDR
# runtimeclasses                                   node.k8s.io/v1                    false        RuntimeClass
# clusterrolebindings                              rbac.authorization.k8s.io/v1      false        ClusterRoleBinding
# clusterroles                                     rbac.authorization.k8s.io/v1      false        ClusterRole
# deviceclasses                                    resource.k8s.io/v1                false        DeviceClass
# resourceslices                                   resource.k8s.io/v1                false        ResourceSlice
# priorityclasses                     pc           scheduling.k8s.io/v1              false        PriorityClass
# csidrivers                                       storage.k8s.io/v1                 false        CSIDriver
# csinodes                                         storage.k8s.io/v1                 false        CSINode
# storageclasses                      sc           storage.k8s.io/v1                 false        StorageClass
# volumeattachments                                storage.k8s.io/v1                 false        VolumeAttachment
# volumeattributesclasses             vac          storage.k8s.io/v1                 false        VolumeAttributesClass

```

---

## `Role` & `RoleBinding`

- `Role`:

  - the object that **contains rules** that represent a **set of permissions** to **regulate the access** to the `namespaced resources`.
  - must specify `namespace`

- `RoleBinding`

  - used to **grant the permissions** defined in a `role` to a `user` or set of users.
  - holds
    - a list of `subjects` (users, groups, or service accounts)
    - a reference to the `role` being granted.
  - **grants permissions** within a specific `namespace`

- A `RoleBinding` may reference any `Role` **in the same namespace**.
- A `RoleBinding` can reference a `ClusterRole` and bind that `ClusterRole` to **the namespace** of the `RoleBinding`.

---

### Declarative Manifest

```yaml
# demo-role-rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""] # "" indicates the core API group
    resources: ["pods"]
    verbs: ["get", "watch", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
  - kind: User
    name: jane
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role # specify Role or ClusterRole
  name: pod-reader # name of Role or ClusterRole
  apiGroup: rbac.authorization.k8s.io
```

---

## `ClusterRole` & `ClusterRoleBinding`

- `ClusterRole` object:

  - the object that **contains rules** that represent a **set of permissions** to **regulate the access** to the `non-namespaced resource`.

- `ClusterRoleBinding`

  - used to **grant the permissions** defined in a `ClusterRole` to a `user` or set of users.
  - holds
    - a list of `subjects` (users, groups, or service accounts)
    - a reference to the `ClusterRole` being granted.
  - grants that access `cluster-wide`.

---

### Declarative Manifest

- `ClusterRole.rules.apiGroups` value:
  - use `kubectl api-resources` to specify the resource
  - in the `VERSION` colume, `v1` = `""`; the remain is the `apiGroups`

```yaml
# ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
  - apiGroups: [""] # "" indicates the core API group
    resources: ["secrets"]
    verbs: ["get", "watch", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
  - kind: Group
    name: manager # Name is case sensitive
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole # Specify the cluster role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

---

### Imperative Commands

- **Cluster Role**

| **Command**                                                                   | **Description**                                             |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `kubectl create clusterrole NAME --verb=VERB --resource=RESOURCE`             | Create a **ClusterRole** with specific verbs and resources. |
| `kubectl create clusterrole NAME --verb=get,list,watch --resource=pods,nodes` | Create a ClusterRole with **multiple verbs and resources**. |
| `kubectl get clusterroles`                                                    | List all ClusterRoles.                                      |
| `kubectl describe clusterrole NAME`                                           | Show detailed rules inside a ClusterRole.                   |
| `kubectl delete clusterrole NAME`                                             | Delete a ClusterRole.                                       |

- **Cluster Role Binding**

| **Command**                                                                                   | **Description**                                                           |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `kubectl create clusterrolebinding BINDNAME --clusterrole=NAME --user=USERNAME`               | Bind a ClusterRole to a **user** (cluster-wide).                          |
| `kubectl create clusterrolebinding BINDNAME --clusterrole=NAME --group=GROUPNAME`             | Bind a ClusterRole to a **group**.                                        |
| `kubectl create clusterrolebinding BINDNAME --clusterrole=NAME --serviceaccount=NAMESPACE:SA` | Bind a ClusterRole to a **ServiceAccount**.                               |
| `kubectl get clusterrolebindings`                                                             | List all ClusterRoleBindings.                                             |
| `kubectl describe clusterrolebinding NAME`                                                    | Show details of a ClusterRoleBinding.                                     |
| `kubectl delete clusterrolebinding NAME`                                                      | Delete a ClusterRoleBinding.                                              |
| `kubectl create rolebinding NAME --clusterrole=CRNAME -n NAMESPACE --user=USERNAME`           | Bind a ClusterRole **inside a namespace** using RoleBinding.              |
| `kubectl auth can-i VERB RESOURCE --as USER`                                                  | Test if a user has permissions defined by ClusterRole/ClusterRoleBinding. |
| `kubectl auth can-i VERB RESOURCE --all-namespaces --as USER`                                 | Test cluster-wide permissions.                                            |

---

## `Role` and `RoleBinding`

- Example: Any user/serviceaccount with this role can view pods in every namespace.

```yaml
# cluster role
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: view-pods-everywhere
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]

---
# clusterrolebinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: bind-view-pods-everywhere
subjects:
  - kind: User
    name: simon
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view-pods-everywhere
  apiGroup: rbac.authorization.k8s.io
```

---

### Declararive Manifest

- ClusterRole

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-administrator
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["list", "get", "create", "delete"]
```

- ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-role-binding
subjects:
  - kind: User
    name: cluster-admin
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-administrator
  apiGroup: rbac.authorization.k8s.io
```

---

### Imperative Commands

- Role

| Command                                                                 | Description                  |
| ----------------------------------------------------------------------- | ---------------------------- |
| `kubectl create role NAME --verb=VERB --resource=RESOURCE -n NAMESPACE` | Create a Role in a namespace |
| `kubectl create role NAME --verb=get,list,watch --resource=pods -n dev` | Role with multiple verbs     |
| `kubectl get roles -n NAMESPACE`                                        | List Roles in namespace      |
| `kubectl describe role NAME -n NAMESPACE`                               | Show Role rules              |
| `kubectl delete role NAME -n NAMESPACE`                                 | Delete Role                  |

- RoleBinding

| Command                                                                                          | Description                           |
| ------------------------------------------------------------------------------------------------ | ------------------------------------- |
| `kubectl create rolebinding BINDNAME --role=ROLENAME --user=USERNAME -n NAMESPACE`               | Bind Role to a user                   |
| `kubectl create rolebinding BINDNAME --role=ROLENAME --group=GROUPNAME -n NAMESPACE`             | Bind Role to a group                  |
| `kubectl create rolebinding BINDNAME --role=ROLENAME --serviceaccount=NAMESPACE:SA -n NAMESPACE` | Bind Role to ServiceAccount           |
| `kubectl create rolebinding BINDNAME --clusterrole=CRNAME --user=USERNAME -n NAMESPACE`          | Bind a ClusterRole inside a namespace |
| `kubectl get rolebindings -n NAMESPACE`                                                          | List RoleBindings                     |
| `kubectl describe rolebinding NAME -n NAMESPACE`                                                 | Show RoleBinding details              |
| `kubectl delete rolebinding NAME -n NAMESPACE`                                                   | Delete RoleBinding                    |
