# Kubernetes - CluterRole & ClusterRoleBinding

[Back](../../index.md)

- [Kubernetes - CluterRole \& ClusterRoleBinding](#kubernetes---cluterrole--clusterrolebinding)
  - [ClusterRole](#clusterrole)
  - [Declararive](#declararive)
    - [Imperative Commands](#imperative-commands)

---

## ClusterRole

- Resources are categorized as
  - namespaced resources
  - cluster scope
    - node
    - pv
    - clusterroles
    - clusterrolebindings
    - certificatesignrequests
    - namespaces

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

- `Role` and `RoleBinding` are used to authorize a user to namespace resources.
- `ClusterRole` and `ClusterRoleBindings` are used to authorize a user to cluster resources

---

- **namespace resources** can be managed by `ClusterRole` and `ClusterRoleBindings`

  - e.g.,
    - pod resources can be defined by cluster role
    - the authorized user can access all the defined pod across the cluster

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

-------
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

## Declararive

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

| **Command**                                                                                   | **Description**                                                           |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `kubectl create clusterrole NAME --verb=VERB --resource=RESOURCE`                             | Create a **ClusterRole** with specific verbs and resources.               |
| `kubectl create clusterrole NAME --verb=get,list,watch --resource=pods,nodes`                 | Create a ClusterRole with **multiple verbs and resources**.               |
| `kubectl get clusterroles`                                                                    | List all ClusterRoles.                                                    |
| `kubectl describe clusterrole NAME`                                                           | Show detailed rules inside a ClusterRole.                                 |
| `kubectl delete clusterrole NAME`                                                             | Delete a ClusterRole.                                                     |
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

```sh
kubectl create clusterrole storage-admin --resource=persistentvolumes,storageclasses --verb=create,list,get,delete

kubectl create clusterrolebinding michelle-storage-admin


kubectl create clusterrolebinding michelle-storage-admin --clusterrole=storage-admin --user=michelle
```
