# Kubernetes - Resources Limit

[Back](../../index.md)

- [Kubernetes - Resources Limit](#kubernetes---resources-limit)
  - [Pod resource](#pod-resource)
  - [Resource Request](#resource-request)
  - [Resource](#resource)
    - [CPU](#cpu)
    - [Memory](#memory)
    - [Example](#example)
  - [Request + Limit Strategy](#request--limit-strategy)
    - [CPU](#cpu-1)
    - [Memory](#memory-1)
  - [Limit range](#limit-range)
  - [Quota](#quota)
  - [Edit a pod](#edit-a-pod)
  - [Edit Deployments](#edit-deployments)

---

## Pod resource

- By default, pods do not have any resources request and limit.
  - A pod can consume as many resources as required on any node.

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

- By default, a pod can consume unlimited resources
  - resource limit can be defined for a pod
- Exceed Limit
  - CPU **cannot** exceed
  - memory **can** execeed
    - if memory is constantly over the limit, the pod will be terminated due to `OOMKilled` (out of memory error)

### CPU

- `1 cpu`:
  - 1 AWS vCPU
  - 1 GCP
  - 1 Azure Core
  - 1 Hyperthread

---

### Memory

- `1 Ki`: 1,024 bytes
- `1 K`: 1,000 bytes
- `1 Mi`: 1,048,576 bytes
- `1 M`: 1,000,000 bytes

---

### Example

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
        limits:
          cpu: 2
          memory: "2Gi"
```

---

## Request + Limit Strategy

### CPU

- CPU cannot consume limited resource

- 2 pods:

| Request | Limits | Resource concume                                                        |
| ------- | ------ | ----------------------------------------------------------------------- |
| No      | No     | Default                                                                 |
| No      | Yes    | automatically set the requests = limit                                  |
| Yes     | Yes    | each pod is limited by limited resource;idle cpu cannot consume         |
| Yes     | No     | request resource allocate to each pod; each pod can conume the idle cpu |

---

### Memory

- Pod can consume more than limited memory; Memory cannot be throttled
  - Once the memory is assigned to a pod, the only way to retrieve the memory is to kill the pod and free up the memory.

| Request | Limits | Resource concume                                                           |
| ------- | ------ | -------------------------------------------------------------------------- |
| No      | No     | Default                                                                    |
| No      | Yes    | automatically set the requests = limit                                     |
| Yes     | Yes    | each pod is limited by limited resource;idle memory cannot consume         |
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
