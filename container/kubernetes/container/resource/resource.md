# Kubernetes: Container - Resources

[Back](../../index.md)

- [Kubernetes: Container - Resources](#kubernetes-container---resources)
  - [Container Resource](#container-resource)
    - [Declarative Manifest](#declarative-manifest)
  - [Pod Resource](#pod-resource)
  - [Resource Request](#resource-request)
  - [Resource](#resource)
    - [Request + Limit Strategy](#request--limit-strategy)
  - [Limit range](#limit-range)
    - [Imperative Commands](#imperative-commands)
  - [Quota](#quota)
  - [Edit a pod](#edit-a-pod)
  - [Edit Deployments](#edit-deployments)

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

### Declarative Manifest

```yaml
kind: Pod
spec:
  containers:
    - name:
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

## Resource Request

- to define resources required for a pod

```yaml
# pod
spec:
  containers:
    - name:
      image:
      resources:
        requests:
          cpu: 1
          memory: "1Gi"
```

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

## Limit range

- Used to define default resource reuqest and limit
  - only apply when a pod is created
  - not apply when the pod is running.

```yaml
# limit range for cpu
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-resource-constraint
# pod
spec:
  limits:
    - default: # limit
        cpu: 500m
      defaultRequest: # request
        cpu: 500m
      max: # limit
        cpu: "1"
      min: # request
        cpu: 100m
      type: Container
```

---

```yaml
# limit range for cpu
apiVersion: v1
kind: LimitRange
metadata:
  name: memory-resource-constraint
# pod
spec:
  limits:
    - default: # limit
        cpu: 1Gi
      defaultRequest: # request
        cpu: 1Gi
      max: # limit
        cpu: 1Gi
      min: # request
        cpu: 500Mi
      type: Container
```

---

### Imperative Commands

| Command | Description      |
| ------- | ---------------- |
|         | Display resource |
|         |                  |

---

## Quota

- A hard limit to the total CPU and memory consumption at the namespace.

```yaml
# Quota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: my-resource-quota
# pod
spec:
  hard:
    requests.cpu: 4
    requests.memory: 4Gi
    limits.cpu: 10
    limits.memory: 10Gi
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
