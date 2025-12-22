# Kubernetes - Fundamental: API Object

[Back](../../index.md)

- [Kubernetes - Fundamental: API Object](#kubernetes---fundamental-api-object)
  - [Kubernetes API Oject](#kubernetes-api-oject)
    - [Resource vs object](#resource-vs-object)
    - [Common Command](#common-command)
    - [Lab: API resources](#lab-api-resources)
    - [Lab: Access API via HTTP](#lab-access-api-via-http)
  - [Object Manifest](#object-manifest)
    - [Association with Controllers](#association-with-controllers)
    - [Output Object manifest file](#output-object-manifest-file)
    - [Fields of Object Manifest File](#fields-of-object-manifest-file)
    - [Common Commands](#common-commands)
    - [Lab: Explain an object](#lab-explain-an-object)
  - [Object Status Conditions](#object-status-conditions)
    - [Common Commands](#common-commands-1)
    - [Lab: Retrieve API Ojbect status condition](#lab-retrieve-api-ojbect-status-condition)
  - [Filter Object info: JSON Path](#filter-object-info-json-path)
    - [Lab: filter node info](#lab-filter-node-info)
    - [Lab: filter node info](#lab-filter-node-info-1)
  - [Event objects](#event-objects)
    - [Common Commands](#common-commands-2)
    - [Lab: Get events object](#lab-get-events-object)

---

## Kubernetes API Oject

- `Kubernetes API`

  - the central point of interaction with the cluster
  - an **HTTP-based RESTful API** where the state is represented by resources on which you perform `CRUD` operations (Create, Read, Update, Delete) using standard HTTP methods such as `POST`, `GET`, `PUT/PATCH` or `DELETE`.

- `API Object`
  - then entity **stored** in the `etcd` and are managed via the `Kubernetes API`.

---

### Resource vs object

- `resource` and `object` are used interchangeably with subtle differences
- `resource`:

  - an essential concept in RESTful APIs;
  - each resource is assigned a `URI` or `Uniform Resource Identifier` that uniquely identifies it
  - in k8s api, url: `/api/v1/deployments`
    - `GET /api/v1/namespaces/default/deployments`: list all deploys
    - `GET /api/v1/namespaces/default/deployments/deploy_id`: describe deploy
    - `PUT /api/v1/namespaces/default/deployments/deploy_id`: update deploy
    - `POST /api/v1/namespaces/default/deployments/deploy_id`: update deploy
  - **GET request**:

    - returns the object in structured text form.
    - The default data model is `JSON`,

  - **POST or PUT request**:
    - update the object

---

- `object`
  - a **single** `object` instance can also be exposed via **multiple** `resources` if multiple API versions exist for an object type.
  - In some cases, a `resource` **doesn’t** represent any `object` at all.
  - e.g.,
    - `POST /apis/authorization.k8s.io/v1/subjectaccessreviews`
    - used to verify whether a subject (a person or a service) is authorized
    - no object is created by the POST request.

---

### Common Command

| CMD                     | DESC                                                                         |
| ----------------------- | ---------------------------------------------------------------------------- |
| `kubectl proxy`         | creates a local gateway between local machine and the Kubernetes API server. |
| `kubectl api-resources` | list all resources                                                           |

---

### Lab: API resources

```sh
# list all resources
kubectl api-resources
# NAME                                SHORTNAMES   APIVERSION                          NAMESPACED   KIND
# bindings                                         v1                                  true         Binding
# componentstatuses                   cs           v1                                  false        ComponentStatus
# configmaps                          cm           v1                                  true         ConfigMap
# endpoints                           ep           v1                                  true         Endpoints
# events                              ev           v1                                  true         Event
# limitranges                         limits       v1                                  true         LimitRange
# namespaces                          ns           v1                                  false        Namespace
# nodes                               no           v1                                  false        Node
# persistentvolumeclaims              pvc          v1                                  true         PersistentVolumeClaim
# persistentvolumes                   pv           v1                                  false        PersistentVolume
# pods                                po           v1                                  true         Pod
# podtemplates                                     v1                                  true         PodTemplate
# replicationcontrollers              rc           v1                                  true         ReplicationController
# resourcequotas                      quota        v1                                  true         ResourceQuota
# secrets                                          v1                                  true         Secret
# serviceaccounts                     sa           v1                                  true         ServiceAccount
# services                            svc          v1                                  true         Service
# mutatingwebhookconfigurations                    admissionregistration.k8s.io/v1     false        MutatingWebhookConfiguration
# validatingadmissionpolicies                      admissionregistration.k8s.io/v1     false        ValidatingAdmissionPolicy
# validatingadmissionpolicybindings                admissionregistration.k8s.io/v1     false        ValidatingAdmissionPolicyBinding
# validatingwebhookconfigurations                  admissionregistration.k8s.io/v1     false        ValidatingWebhookConfiguration
# customresourcedefinitions           crd,crds     apiextensions.k8s.io/v1             false        CustomResourceDefinition
# apiservices                                      apiregistration.k8s.io/v1           false        APIService
# controllerrevisions                              apps/v1                             true         ControllerRevision
# daemonsets                          ds           apps/v1                             true         DaemonSet
# deployments                         deploy       apps/v1                             true         Deployment
# replicasets                         rs           apps/v1                             true         ReplicaSet
# statefulsets                        sts          apps/v1                             true         StatefulSet
# selfsubjectreviews                               authentication.k8s.io/v1            false        SelfSubjectReview
# tokenreviews                                     authentication.k8s.io/v1            false        TokenReview
# localsubjectaccessreviews                        authorization.k8s.io/v1             true         LocalSubjectAccessReview
# selfsubjectaccessreviews                         authorization.k8s.io/v1             false        SelfSubjectAccessReview
# selfsubjectrulesreviews                          authorization.k8s.io/v1             false        SelfSubjectRulesReview
# subjectaccessreviews                             authorization.k8s.io/v1             false        SubjectAccessReview
# horizontalpodautoscalers            hpa          autoscaling/v2                      true         HorizontalPodAutoscaler
# cronjobs                            cj           batch/v1                            true         CronJob
# jobs                                             batch/v1                            true         Job
# certificatesigningrequests          csr          certificates.k8s.io/v1              false        CertificateSigningRequest
# ingressclassparameterses                         configuration.konghq.com/v1alpha1   true         IngressClassParameters
# kongclusterplugins                  kcp          configuration.konghq.com/v1         false        KongClusterPlugin
# kongconsumergroups                  kcg          configuration.konghq.com/v1beta1    true         KongConsumerGroup
# kongconsumers                       kc           configuration.konghq.com/v1         true         KongConsumer
# kongcustomentities                  kce          configuration.konghq.com/v1alpha1   true         KongCustomEntity
# kongingresses                       ki           configuration.konghq.com/v1         true         KongIngress
# konglicenses                        kl           configuration.konghq.com/v1alpha1   false        KongLicense
# kongplugins                         kp           configuration.konghq.com/v1         true         KongPlugin
# kongupstreampolicies                kup          configuration.konghq.com/v1beta1    true         KongUpstreamPolicy
# kongvaults                          kv           configuration.konghq.com/v1alpha1   false        KongVault
# tcpingresses                                     configuration.konghq.com/v1beta1    true         TCPIngress
# udpingresses                                     configuration.konghq.com/v1beta1    true         UDPIngress
# leases                                           coordination.k8s.io/v1              true         Lease
# endpointslices                                   discovery.k8s.io/v1                 true         EndpointSlice
# events                              ev           events.k8s.io/v1                    true         Event
# flowschemas                                      flowcontrol.apiserver.k8s.io/v1     false        FlowSchema
# prioritylevelconfigurations                      flowcontrol.apiserver.k8s.io/v1     false        PriorityLevelConfiguration
# ingressclasses                                   networking.k8s.io/v1                false        IngressClass
# ingresses                           ing          networking.k8s.io/v1                true         Ingress
# ipaddresses                         ip           networking.k8s.io/v1                false        IPAddress
# networkpolicies                     netpol       networking.k8s.io/v1                true         NetworkPolicy
# servicecidrs                                     networking.k8s.io/v1                false        ServiceCIDR
# runtimeclasses                                   node.k8s.io/v1                      false        RuntimeClass
# poddisruptionbudgets                pdb          policy/v1                           true         PodDisruptionBudget
# clusterrolebindings                              rbac.authorization.k8s.io/v1        false        ClusterRoleBinding
# clusterroles                                     rbac.authorization.k8s.io/v1        false        ClusterRole
# rolebindings                                     rbac.authorization.k8s.io/v1        true         RoleBinding
# roles                                            rbac.authorization.k8s.io/v1        true         Role
# deviceclasses                                    resource.k8s.io/v1                  false        DeviceClass
# resourceclaims                                   resource.k8s.io/v1                  true         ResourceClaim
# resourceclaimtemplates                           resource.k8s.io/v1                  true         ResourceClaimTemplate
# resourceslices                                   resource.k8s.io/v1                  false        ResourceSlice
# priorityclasses                     pc           scheduling.k8s.io/v1                false        PriorityClass
# csidrivers                                       storage.k8s.io/v1                   false        CSIDriver
# csinodes                                         storage.k8s.io/v1                   false        CSINode
# csistoragecapacities                             storage.k8s.io/v1                   true         CSIStorageCapacity
# storageclasses                      sc           storage.k8s.io/v1                   false        StorageClass
# volumeattachments                                storage.k8s.io/v1                   false        VolumeAttachment
# volumeattributesclasses             vac          storage.k8s.io/v1                   false        VolumeAttributesClass
```

---

### Lab: Access API via HTTP

```sh
# access the API through the proxy using plain HTTP.
kubectl proxy
# Starting to serve on 127.0.0.1:8001

curl http://127.0.0.1:8001/apis/apps/v1/namespaces/default/deployments
# {
#   "kind": "DeploymentList",
#   "apiVersion": "apps/v1",
#   "metadata": {
#     "resourceVersion": "2119788"
#   },
#   "items": [
#     {
#       "metadata": {
#         "name": "nginx",
#         "namespace": "default",
#         "uid": "1d2ffb21-5f78-49ee-8b10-db754a485c45",
#         "resourceVersion": "2114866",
#         "generation": 2,
#         "creationTimestamp": "2025-12-20T19:10:45Z",
#         "labels": {
#           "app": "nginx"
#         },
#         "annotations": {
#           "deployment.kubernetes.io/revision": "1"
#         },
#         "managedFields": [
#           {
#             "manager": "kubectl",
#             "operation": "Update",
#             "apiVersion": "apps/v1",
#             "fieldsType": "FieldsV1",
#             "fieldsV1": {
#               "f:spec": {
#                 "f:replicas": {}
#               }
#             },
#             "subresource": "scale"
#           },
#           {
#             "manager": "kubectl-create",
#             "operation": "Update",
#             "apiVersion": "apps/v1",
#             "time": "2025-12-20T19:10:45Z",
#             "fieldsType": "FieldsV1",
#             "fieldsV1": {
#               "f:metadata": {
#                 "f:labels": {
#                   ".": {},
#                   "f:app": {}
#                 }
#               },
#               "f:spec": {
#                 "f:progressDeadlineSeconds": {},
#                 "f:revisionHistoryLimit": {},
#                 "f:selector": {},
#                 "f:strategy": {
#                   "f:rollingUpdate": {
#                     ".": {},
#                     "f:maxSurge": {},
#                     "f:maxUnavailable": {}
#                   },
#                   "f:type": {}
#                 },
#                 "f:template": {
#                   "f:metadata": {
#                     "f:labels": {
#                       ".": {},
#                       "f:app": {}
#                     }
#                   },
#                   "f:spec": {
#                     "f:containers": {
#                       "k:{\"name\":\"nginx\"}": {
#                         ".": {},
#                         "f:image": {},
#                         "f:imagePullPolicy": {},
#                         "f:name": {},
#                         "f:ports": {
#                           ".": {},
#                           "k:{\"containerPort\":80,\"protocol\":\"TCP\"}": {
#                             ".": {},
#                             "f:containerPort": {},
#                             "f:protocol": {}
#                           }
#                         },
#                         "f:resources": {},
#                         "f:terminationMessagePath": {},
#                         "f:terminationMessagePolicy": {}
#                       }
#                     },
#                     "f:dnsPolicy": {},
#                     "f:restartPolicy": {},
#                     "f:schedulerName": {},
#                     "f:securityContext": {},
#                     "f:terminationGracePeriodSeconds": {}
#                   }
#                 }
#               }
#             }
#           },
#           {
#             "manager": "kube-controller-manager",
#             "operation": "Update",
#             "apiVersion": "apps/v1",
#             "time": "2025-12-20T21:32:32Z",
#             "fieldsType": "FieldsV1",
#             "fieldsV1": {
#               "f:metadata": {
#                 "f:annotations": {
#                   ".": {},
#                   "f:deployment.kubernetes.io/revision": {}
#                 }
#               },
#               "f:status": {
#                 "f:availableReplicas": {},
#                 "f:conditions": {
#                   ".": {},
#                   "k:{\"type\":\"Available\"}": {
#                     ".": {},
#                     "f:lastTransitionTime": {},
#                     "f:lastUpdateTime": {},
#                     "f:message": {},
#                     "f:reason": {},
#                     "f:status": {},
#                     "f:type": {}
#                   },
#                   "k:{\"type\":\"Progressing\"}": {
#                     ".": {},
#                     "f:lastTransitionTime": {},
#                     "f:lastUpdateTime": {},
#                     "f:message": {},
#                     "f:reason": {},
#                     "f:status": {},
#                     "f:type": {}
#                   }
#                 },
#                 "f:observedGeneration": {},
#                 "f:readyReplicas": {},
#                 "f:replicas": {},
#                 "f:updatedReplicas": {}
#               }
#             },
#             "subresource": "status"
#           }
#         ]
#       },
#       "spec": {
#         "replicas": 3,
#         "selector": {
#           "matchLabels": {
#             "app": "nginx"
#           }
#         },
#         "template": {
#           "metadata": {
#             "labels": {
#               "app": "nginx"
#             }
#           },
#           "spec": {
#             "containers": [
#               {
#                 "name": "nginx",
#                 "image": "nginx",
#                 "ports": [
#                   {
#                     "containerPort": 80,
#                     "protocol": "TCP"
#                   }
#                 ],
#                 "resources": {},
#                 "terminationMessagePath": "/dev/termination-log",
#                 "terminationMessagePolicy": "File",
#                 "imagePullPolicy": "Always"
#               }
#             ],
#             "restartPolicy": "Always",
#             "terminationGracePeriodSeconds": 30,
#             "dnsPolicy": "ClusterFirst",
#             "securityContext": {},
#             "schedulerName": "default-scheduler"
#           }
#         },
#         "strategy": {
#           "type": "RollingUpdate",
#           "rollingUpdate": {
#             "maxUnavailable": "25%",
#             "maxSurge": "25%"
#           }
#         },
#         "revisionHistoryLimit": 10,
#         "progressDeadlineSeconds": 600
#       },
#       "status": {
#         "observedGeneration": 2,
#         "replicas": 3,
#         "updatedReplicas": 3,
#         "readyReplicas": 3,
#         "availableReplicas": 3,
#         "conditions": [
#           {
#             "type": "Progressing",
#             "status": "True",
#             "lastUpdateTime": "2025-12-20T19:10:48Z",
#             "lastTransitionTime": "2025-12-20T19:10:45Z",
#             "reason": "NewReplicaSetAvailable",
#             "message": "ReplicaSet \"nginx-7ccccd94f7\" has successfully progressed."
#           },
#           {
#             "type": "Available",
#             "status": "True",
#             "lastUpdateTime": "2025-12-20T21:32:32Z",
#             "lastTransitionTime": "2025-12-20T21:32:32Z",
#             "reason": "MinimumReplicasAvailable",
#             "message": "Deployment has minimum availability."
#           }
#         ]
#       }
#     }
#   ]
# }

```

---

## Object Manifest

- `Object manifest`

  - a file, typically written in YAML or JSON, that acts as a **blueprint to define the desired state** of a Kubernetes `object` or application within a cluster

- objects manifest file consists of the following four sections:
- `Type Metadata`
  - specifies the object type,
  - the **group** to which the type belongs, and the **API version**.
- `Object Metadata`
  - holds the basic information about the object instance, including its name, time of creation, owner of the object, and other **identifying information**.
  - The fields are the same for all object types.
- `Spec`
  - info write to API
  - the part in which you **specify the desired state of the object**.
- `Status`
  - info read to API
  - contains the current **actual state** of the object.
  - For a pod, it tells you the condition of the pod, the status of each of its containers, its IP address, the node it’s running on, and other information that reveals what’s happening to your pod

---

- **All** Kubernetes API `objects` contain the `Type` and `object` metadata sections, but **not all** have the `Spec` and `Status` sections.
  - Those that don’t, typically contain just **static data** and **don’t have** a corresponding `controller`
  - e.g., Event object

---

### Association with Controllers

- Each `controller` is usually only responsible for one `object type`.
- The specific `controller`
  - reads te **desired status** of a k8s `object` that the user submits.
  - perform operations
  - report back the **actual state** of the `object`

---

### Output Object manifest file

```sh
# output the manifest of an existing object
kubectl get deploy nginx -o yaml
```

---

### Fields of Object Manifest File

- `apiVersion` field
  - specify the API version and the API group to which the resource belongs
  - the schema used to describe this object
  - only one schema exists for each type
- `kind` field
  - type of the object that this object manifest specifies.
- `metadata` field
  - contains the **metadata** of this object instance.
  - common:
    - name of the object
    - labels
    - annotations
- `spec` field
  - specify the desired status of this object
  - contains many more fields that use to configure the object.
- `status` field

  - contains the **last observed state** of the thing the object represents.
  - differs between the different kinds of object

---

### Common Commands

| Command                                           | Description                                               |
| ------------------------------------------------- | --------------------------------------------------------- |
| `kubectl explain OBJECT`                          | lists the top-level fields                                |
| `kubectl explain OBJECT.FIELD`                    | lists the sub fields                                      |
| `kubectl explain OBJECT --api-versio=API_VERSION` | List fields with a specific version                       |
| `kubectl explain OBJECT --recursive`              | Show hierarchical list of fields without the descriptions |

---

### Lab: Explain an object

```sh
kubectl explain pod
# KIND:       Pod
# VERSION:    v1

# DESCRIPTION:
#     Pod is a collection of containers that can run on a host. This resource is
#     created by clients and scheduled onto hosts.

# FIELDS:
#   apiVersion    <string>
#     APIVersion defines the versioned schema of this representation of an object.
#     Servers should convert recognized schemas to the latest internal value, and
#     may reject unrecognized values. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

#   kind  <string>
#     Kind is a string value representing the REST resource this object
#     represents. Servers may infer this from the endpoint the client submits
#     requests to. Cannot be updated. In CamelCase. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

#   metadata      <ObjectMeta>
#     Standard object's metadata. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

#   spec  <PodSpec>
#     Specification of the desired behavior of the pod. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

#   status        <PodStatus>
#     Most recently observed status of the pod. This data may not be up to date.
#     Populated by the system. Read-only. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status


kubectl explain pod.spec

kubectl explain node --recursive
```

---

## Object Status Conditions

- `status conditions`

  - indicate the individual aspects of the object's current state
  - a standardized way for `controllers` to **report** on the object's **health** and **readiness** in a structured, consistent manner.
  - help both human users and controllers **understand the current state** of an object and track its **progress toward** the `desired state` defined in the .spec.

- Structure of a Condition

  - `type` field:
    - condition type
    - Common:
      - pod:
        - `Ready`,
        - `Initialized`,
        - `PodScheduled`,
      - node:
        - `Ready`
        - `DiskPressure`,
        - `MemoryPressure`,
        - `PIDPressure`
      - Deployment:
        - `Progressing`
        - `Available`
  - `status` field:
    - specify the state of the condition
    - `True`, `False` or `Unknown`,
  - `reason` field:
    - machine-facing reason for the last transition of the condition
  - `message` field:
    - a human-facing message with details about the transition
  - `lastTransitionTime` field
    - indicates when the **condition moved** from one status to another
  - `lastHeartbeatTime` field
    - reveals the last time the controller **received an update** on the given condition.

---

### Common Commands

| CMD                                                                                        | DESC                                         |
| ------------------------------------------------------------------------------------------ | -------------------------------------------- |
| `kubectl get pods POD_NAME -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'`  | display the pod's status conditions          |
| `kubectl get node NODE_NAME -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'` | display the pod’s status conditions          |
| `kubectl get node NODE_NAME -o json \| jq .status.conditions`                              | display the node’s status conditions         |
| `kubectl get node NODE_NAME -o yaml \| yq .status.conditions`                              | display the node’s status conditions         |
| `kubectl describe OBJECT`                                                                  | Print a detailed description of the selected |

---

### Lab: Retrieve API Ojbect status condition

```sh
kubectl get node docker-desktop -o json | jq .status.conditions
# [
#   {
#     "lastHeartbeatTime": "2025-12-21T01:40:05Z",
#     "lastTransitionTime": "2025-11-05T18:00:34Z",
#     "message": "kubelet has sufficient memory available",
#     "reason": "KubeletHasSufficientMemory",
#     "status": "False",
#     "type": "MemoryPressure"
#   },
#   {
#     "lastHeartbeatTime": "2025-12-21T01:40:05Z",
#     "lastTransitionTime": "2025-11-05T18:00:34Z",
#     "message": "kubelet has no disk pressure",
#     "reason": "KubeletHasNoDiskPressure",
#     "status": "False",
#     "type": "DiskPressure"
#   },
#   {
#     "lastHeartbeatTime": "2025-12-21T01:40:05Z",
#     "lastTransitionTime": "2025-11-05T18:00:34Z",
#     "message": "kubelet has sufficient PID available",
#     "reason": "KubeletHasSufficientPID",
#     "status": "False",
#     "type": "PIDPressure"
#   },
#   {
#     "lastHeartbeatTime": "2025-12-21T01:40:05Z",
#     "lastTransitionTime": "2025-11-05T18:00:36Z",
#     "message": "kubelet is posting ready status",
#     "reason": "KubeletReady",
#     "status": "True",
#     "type": "Ready"
#   }
# ]
```

---

## Filter Object info: JSON Path

- used to fileter info retrieved from API server

---

### Lab: filter node info

```sh
kubectl get node
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   46d   v1.34.1

# output in json
kubectl get node -o json > node.json

# get metadata: name
kubectl get nodes -o=jsonpath='{.items[*].metadata.name}'
# 'docker-desktop'

# get cpu
kubectl get nodes -o=jsonpath='{.items[*].status.capacity.cpu}'
# '12'

# gen a report
kubectl get nodes -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.capacity.cpu}{"\n"}{end}'
# docker-desktop  12

kubectl get nodes -o=custom-columns="NAME:.metadata.name,CPU:.status.capacity.cpu"
# NAME             CPU
# docker-desktop   12

# sort
kubectl get nodes --sort-by=.status.capacity.cpu
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   46d   v1.34.1
```

### Lab: filter node info

```sh
kubectl create deploy web --image=nginx --replicas=4
# deployment.apps/web created
kubectl create deploy redis --image=redis --replicas=3
# deployment.apps/redis created

# get image
kubectl get deploy -o=jsonpath="{.items[*].spec.template.spec.containers[0].image}"
# redis nginx

kubectl get deploy -o=custom-columns="NAME:.metadata.name,Image:.spec.template.spec.containers[0].image"
# NAME    Image
# redis   redis
# web     nginx

# sort
kubectl get deploy --sort-by=.metadata.name
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE
# redis   3/3     3            3           71s
# web     4/4     4            4           111s
```

---

## Event objects

- `events`

  - represented by `Event objects` that are **created** and **read** via the Kubernetes API.
  - deleted **one hour** after its **creation** to reduce the burden on `etcd`, the data store for Kubernetes API objects.

- `Event objects` have **no** `spec` and `status` sections

- Two types of events exist:

  - `Normal`
  - `Warning`:
    - generated by `controllers` when something prevents them from **reconciling the object**.

- How it works:
  - `controller` manages the object
    - read spec and update status
  - `controller` generates `Event objects`, showing actions and state changes
  - events are store in `etcd`
    - automatically purged one hour after created.

---

### Common Commands

| CMD                                            | DESC                                                  |
| ---------------------------------------------- | ----------------------------------------------------- |
| `kubectl describe OBJECT`                      | Show details, including events related to this object |
| `kubectl get events`/`kubectl get ev`          | list recent events                                    |
| `kubectl get events -o wide`                   | list recent events with additional column             |
| `kubectl get ev --field-selector type=Warning` | display only Warning events                           |

---

### Lab: Get events object

```sh
kubectl create deploy warning --image=warning --replicas=3
# deployment.apps/warning created

kubectl get ev
# Warning: short name "ev" could also match lower priority resource events.events.k8s.io
# LAST SEEN   TYPE      REASON              OBJECT                         MESSAGE
# 8m13s       Normal    Killing             pod/nginx-7ccccd94f7-jtbsr     Stopping container nginx
# 8m13s       Normal    SuccessfulDelete    replicaset/nginx-7ccccd94f7    Deleted pod: nginx-7ccccd94f7-jtbsr
# 8m13s       Normal    ScalingReplicaSet   deployment/nginx               Scaled down replica set nginx-7ccccd94f7 from 3 to 2
# 22s         Normal    Scheduled           pod/warning-d874477f8-6qn9h    Successfully assigned default/warning-d874477f8-6qn9h to docker-desktop
# 4s          Normal    Pulling             pod/warning-d874477f8-6qn9h    Pulling image "warning"
# 4s          Warning   Failed              pod/warning-d874477f8-6qn9h    Failed to pull image "warning": Error response from daemon: pull access denied for warning, repository does not exist or may require 'docker login'
# 4s          Warning   Failed              pod/warning-d874477f8-6qn9h    Error: ErrImagePull
# 19s         Normal    BackOff             pod/warning-d874477f8-6qn9h    Back-off pulling image "warning"
# 19s         Warning   Failed              pod/warning-d874477f8-6qn9h    Error: ImagePullBackOff
# 22s         Normal    Scheduled           pod/warning-d874477f8-994bp    Successfully assigned default/warning-d874477f8-994bp to docker-desktop
# 7s          Normal    Pulling             pod/warning-d874477f8-994bp    Pulling image "warning"
# 7s          Warning   Failed              pod/warning-d874477f8-994bp    Failed to pull image "warning": Error response from daemon: pull access denied for warning, repository does not exist or may require 'docker login'
# 7s          Warning   Failed              pod/warning-d874477f8-994bp    Error: ErrImagePull
# 19s         Normal    BackOff             pod/warning-d874477f8-994bp    Back-off pulling image "warning"
# 19s         Warning   Failed              pod/warning-d874477f8-994bp    Error: ImagePullBackOff
# 22s         Normal    Scheduled           pod/warning-d874477f8-ql7d9    Successfully assigned default/warning-d874477f8-ql7d9 to docker-desktop
# 6s          Normal    Pulling             pod/warning-d874477f8-ql7d9    Pulling image "warning"
# 6s          Warning   Failed              pod/warning-d874477f8-ql7d9    Failed to pull image "warning": Error response from daemon: pull access denied for warning, repository does not exist or may require 'docker login'
# 6s          Warning   Failed              pod/warning-d874477f8-ql7d9    Error: ErrImagePull
# 19s         Normal    BackOff             pod/warning-d874477f8-ql7d9    Back-off pulling image "warning"
# 19s         Warning   Failed              pod/warning-d874477f8-ql7d9    Error: ImagePullBackOff
# 22s         Normal    SuccessfulCreate    replicaset/warning-d874477f8   Created pod: warning-d874477f8-994bp
# 22s         Normal    SuccessfulCreate    replicaset/warning-d874477f8   Created pod: warning-d874477f8-ql7d9
# 22s         Normal    SuccessfulCreate    replicaset/warning-d874477f8   Created pod: warning-d874477f8-6qn9h
# 22s         Normal    ScalingReplicaSet   deployment/warning             Scaled up replica set warning-d874477f8 from 0 to 3


# event object info for type of event
kubectl explain events
  # type  <string>
  #   Type of this event (Normal, Warning), new types could be added in the future

# filter only warning event
kubectl get ev --field-selector type=Warning
# Warning: short name "ev" could also match lower priority resource events.events.k8s.io
# LAST SEEN   TYPE      REASON   OBJECT                        MESSAGE
# 5s          Warning   Failed   pod/warning-d874477f8-6qn9h   Failed to pull image "warning": Error response from daemon: pull access denied for warning, repository does not exist or may require 'docker login'
# 5s          Warning   Failed   pod/warning-d874477f8-6qn9h   Error: ErrImagePull
# 21s         Warning   Failed   pod/warning-d874477f8-6qn9h   Error: ImagePullBackOff
# 49s         Warning   Failed   pod/warning-d874477f8-994bp   Failed to pull image "warning": Error response from daemon: pull access denied for warning, repository does not exist or may require 'docker login'
# 49s         Warning   Failed   pod/warning-d874477f8-994bp   Error: ErrImagePull
# 9s          Warning   Failed   pod/warning-d874477f8-994bp   Error: ImagePullBackOff
# 46s         Warning   Failed   pod/warning-d874477f8-ql7d9   Failed to pull image "warning": Error response from daemon: pull access denied for warning, repository does not exist or may require 'docker login'
# 46s         Warning   Failed   pod/warning-d874477f8-ql7d9   Error: ErrImagePull
# 12s         Warning   Failed   pod/warning-d874477f8-ql7d9   Error: ImagePullBackOff
```

---

- Event object cannot be delete using `kubectl delete all -all`

```sh
kubectl get event
# LAST SEEN   TYPE     REASON      OBJECT                     MESSAGE
# 27m         Normal   Scheduled   pod/init-containers-demo   Successfully assigned default/init-containers-demo to docker-desktop
# 27m         Normal   Pulling     pod/init-containers-demo   Pulling image "busybox"
# 27m         Normal   Pulled      pod/init-containers-demo   Successfully pulled image "busybox" in 1.018s (1.018s including waiting). Image size: 2224358 bytes.
# ...

kubectl  delete all --all

kubectl get event
# LAST SEEN   TYPE     REASON      OBJECT                     MESSAGE
# 27m         Normal   Scheduled   pod/init-containers-demo   Successfully assigned default/init-containers-demo to docker-desktop
# 27m         Normal   Pulling     pod/init-containers-demo   Pulling image "busybox"
# 27m         Normal   Pulled      pod/init-containers-demo   Successfully pulled image "busybox" in 1.018s (1.018s including waiting). Image size: 2224358 bytes.
# ...

# delete all event
kubectl delete event --all
# event "init-containers-demo.18835cddd8eb5ed5" deleted from default namespace
# event "init-containers-demo.18835cddfc62a87b" deleted from default namespace
# event "init-containers-demo.18835cde391aa01d" deleted from default namespace
# event "init-containers-demo.18835cde4681a7a7" deleted from default namespace
# event "init-containers-demo.18835cde4cb35ff5" deleted from default namespace
# event "init-containers-demo.18835ce0b85eac47" deleted from default namespace
# ...

kubectl get event
# No resources found in default namespace.
```
