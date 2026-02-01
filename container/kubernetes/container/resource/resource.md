# Kubernetes: Container - Resources

[Back](../../index.md)

- [Kubernetes: Container - Resources](#kubernetes-container---resources)
  - [Resource](#resource)
    - [Request + Limit Strategy](#request--limit-strategy)
  - [Container Resource](#container-resource)
    - [Imperative Command](#imperative-command)
    - [Declarative Manifest](#declarative-manifest)
  - [Pod Resource](#pod-resource)
    - [Declarative Manifest](#declarative-manifest-1)
  - [Namespace Resource Usage Limits: `Limit Range`](#namespace-resource-usage-limits-limit-range)
    - [Lab: Namespace Limit Range](#lab-namespace-limit-range)
  - [Namespace Total Resource Limits: `ResourceQuota`](#namespace-total-resource-limits-resourcequota)
    - [Lab: ResourceQuota](#lab-resourcequota)
  - [Edit a pod](#edit-a-pod)
  - [Edit Deployments](#edit-deployments)

---

## Resource

- **CPU Resources**:
  - 1 AWS vCPU
  - 1 GCP
  - 1 Azure Core
  - 1 Hyperthread

- **Memory Resources**:
  - `1 Ki`: 1,024 bytes
  - `1 K`: 1,000 bytes
  - `1 Mi`: 1,048,576 bytes
  - `1 M`: 1,000,000 bytes

- **Scheduling**:
  - The `Scheduler` looks for a node that **has enough unallocated capacity** to satisfy the entire Pod's total request.

- **Exceed Limit**
  - CPU **cannot** exceed
  - memory **can** execeed
    - if memory is constantly over the limit, the pod will be terminated due to `OOMKilled` (out of memory error)

---

### Request + Limit Strategy

- CPU cannot consume limited resource

- 2 pods:

| Request | Limits | Resource concume                                                              |
| ------- | ------ | ----------------------------------------------------------------------------- |
| No      | No     | Default                                                                       |
| No      | Yes    | automatically set the **requests = limit**                                    |
| Yes     | Yes    | each pod is **limited** by `resource limit` ; **cannot** consume **idle cpu** |
| Yes     | No     | request resource allocate to each pod; each pod **can conume the idle cpu**   |

---

- Memory
  - Pod can consume more than limited memory; Memory cannot be throttled
  - Once the memory is assigned to a pod, the only way to retrieve the memory is to kill the pod and free up the memory.

| Request | Limits | Resource concume                                                           |
| ------- | ------ | -------------------------------------------------------------------------- |
| No      | No     | Default                                                                    |
| No      | Yes    | automatically set the **requests = limit**                                 |
| Yes     | Yes    | each pod is limited by `resource limit`; idle memory cannot consume        |
| Yes     | No     | request resource allocate to each pod; each pod can conume the idle memory |

---

## Container Resource

- `Container Resource`
  - the CPU/Memory resources available to a container
- `Container Resource Requests`:
  - The **minimum** amount of CPU/Memory guaranteed to the `container`.
  - used to **decide which node** has **enough "room"** to fit the `container`.
- `Container Resource Limits`:
  - The **maximum** amount a `container` can ever use.
  - `CPU Limit`:
    - If a `container` **hits** this, it is "**throttled**" (slowed down).
  - `Memory Limit`:
    - If a `container` **hits** this, it is **"OOMKilled" (Out of Memory)** and **restarted**.

---

### Imperative Command

| CMD                                                                               | DESC           |
| --------------------------------------------------------------------------------- | -------------- |
| `kubectl set resources deploy DEPLOY -c=CONTAINER --limits=cpu=200m,memory=512Mi` | Set resrources |

---

### Declarative Manifest

```yaml
kind: Pod
spec:
  containers:
    - name:
      # container resources
      resources:
        requests:
          cpu: 1
          memory: "1Gi"
        limits:
          cpu: 2
          memory: "2Gi"
```

---

## Pod Resource

- `Pod Resource`
  - the total CPU/Memory resources available to all containers
  - By **default**, pods do **not** have any `resources request` and `limit`.
    - A `pod` can consume as many resources as required on any node.
- `Pod Resource Requests`:
  - The **minimum** amount of CPU/Memory guaranteed to all `containers`.
  - used to **decide which node** has **enough "room"** to fit the `pod`.
- `Pod Resource Limits`:
  - The **maximum** amount all `containers` can ever use.

---

### Declarative Manifest

- to define resources required for a pod

```yaml
# pod
spec:
  resources:
    requests:
      cpu: 1
      memory: "1Gi"
    limits:
      cpu: 2
      memory: "2Gi"
  containers:
```

---

## Namespace Resource Usage Limits: `Limit Range`

- Used to define default resource reuqest and limit
  - only apply when a pod is created
  - not apply when the pod is running.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-constraint
  namespace: limit-resource
# pod
spec:
  limits:
    # contianer limit
    - type: Container
      default:
        cpu: 500m
        memory: 500Mi
      defaultRequest: # request
        cpu: 200m
        memory: 100Mi
      max: # limit
        cpu: "1"
        memory: 1Gi
      min: # request
        cpu: 100m
        memory: 50Mi
    # pod limit
    - type: Pod
      default:
        cpu: 500m
        memory: 500Mi
      defaultRequest: # request
        cpu: 200m
        memory: 100Mi
      max: # limit
        cpu: "1"
        memory: 1Gi
      min: # request
        cpu: 100m
        memory: 50Mi
```

---

### Lab: Namespace Limit Range

```yaml
# limitrange.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-constraint
  namespace: limit-resource
# pod
spec:
  limits:
    # contianer limit
    - type: Container
      default:
        cpu: 500m
        memory: 500Mi
      defaultRequest: # request
        cpu: 200m
        memory: 100Mi
      max: # limit
        cpu: "1"
        memory: 1Gi
      min: # request
        cpu: 100m
        memory: 50Mi
    # pod limit
    - type: Pod
      max: # limit
        cpu: "1"
        memory: 1Gi
      min: # request
        cpu: 100m
        memory: 50Mi
```

```sh
kubectl create ns limit-resource
# namespace/limit-resource created

kubectl apply -f limitrange.yaml
# limitrange/resource-constraint created

kubectl describe ns limit-resource
Name:         limit-resource
Labels:       kubernetes.io/metadata.name=limit-resource
Annotations:  <none>
Status:       Active

No resource quota.

Resource Limits
#  Type       Resource  Min   Max  Default Request  Default Limit  Max Limit/Request Ratio
#  ----       --------  ---   ---  ---------------  -------------  -----------------------
#  Container  cpu       100m  1    200m             500m           -
#  Container  memory    50Mi  1Gi  100Mi            500Mi          -
#  Pod        cpu       100m  1    -                -              -
#  Pod        memory    50Mi  1Gi  -                -              -
```

---

## Namespace Total Resource Limits: `ResourceQuota`

| CMD                                                             | Desc                          |
| --------------------------------------------------------------- | ----------------------------- |
| `kubectl get quota -n NAMESPACE`                                | List quota in a namespace     |
| `kubectl describe quota -n NAMESPACE`                           | Get quota info in a namespace |
| `kubectl create quota NAME --hard=cpu=1,memory=1G,pods=2`       | Create resource quota         |
| `kubectl create quota NAME --hard=pods=100 --scopes=BestEffort` | Create resource quota         |

- A hard limit to the total CPU and memory consumption at the namespace.

```yaml
# Quota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: resource-quota
# pod
spec:
  hard:
    requests.cpu: 4
    requests.memory: 4Gi
    limits.cpu: 10
    limits.memory: 10Gi
```

---

### Lab: ResourceQuota

```yaml
# demo-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: resource-quota
  namespace: limit-resource
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 4Gi
    limits.cpu: "10"
    limits.memory: 10Gi
    configmaps: "10"
    persistentvolumeclaims: "4"
    pods: "4"
    replicationcontrollers: "20"
    secrets: "10"
    services: "10"
    services.loadbalancers: "2"
```

```sh
kubectl apply -f demo-quota.yaml
# resourcequota/resource-quota created

# confirm
kubectl get quota resource-quota --namespace=limit-resource
# NAME             REQUEST                                                                                                                                                                                         LIMIT                                     AGE
# resource-quota   configmaps: 1/10, persistentvolumeclaims: 0/4, pods: 0/4, replicationcontrollers: 0/20, requests.cpu: 0/4, requests.memory: 0/4Gi, secrets: 0/10, services: 0/10, services.loadbalancers: 0/2   limits.cpu: 0/10, limits.memory: 0/10Gi   99s

# confirm
kubectl describe quota resource-quota --namespace=limit-resource
# Name:                   resource-quota
# Namespace:              limit-resource
# Resource                Used  Hard
# --------                ----  ----
# configmaps              1     10
# limits.cpu              0     10
# limits.memory           0     10Gi
# persistentvolumeclaims  0     4
# pods                    0     4
# replicationcontrollers  0     20
# requests.cpu            0     4
# requests.memory         0     4Gi
# secrets                 0     10
# services                0     10
# services.loadbalancers  0     2

# confirm ns
kubectl describe ns limit-resource
# Name:         limit-resource
# Labels:       kubernetes.io/metadata.name=limit-resource
# Annotations:  <none>
# Status:       Active

# Resource Quotas
#   Name:                   resource-quota
#   Resource                Used  Hard
#   --------                ---   ---
#   configmaps              1     10
#   limits.cpu              0     10
#   limits.memory           0     10Gi
#   persistentvolumeclaims  0     4
#   pods                    0     4
#   replicationcontrollers  0     20
#   requests.cpu            0     4
#   requests.memory         0     4Gi
#   secrets                 0     10
#   services                0     10
#   services.loadbalancers  0     2

```

---

## Edit a pod

- **CANNOT** edit specifications of an existing POD other than the below:
  - `spec.containers[*].image`
  - `spec.initContainers[*].image`
  - `spec.activeDeadlineSeconds`
  - `spec.tolerations`

- Command:
  - `kubectl edit pod pod_name`: to open the pod specification in an editor

---

## Edit Deployments

- the pod template can be editted.
- with every change the deployment will automatically delete and create a new pod with the new changes.
- Command: `kubectl edit deployment my-deployment`
