# Kubernetes - Pod: Downward API

[Back](../../index.md)

- [Kubernetes - Pod: Downward API](#kubernetes---pod-downward-api)
  - [Downward API](#downward-api)
    - [Common feilds](#common-feilds)
  - [Lab: Get pod's metadata](#lab-get-pods-metadata)
  - [Lab: Get pod's Resource](#lab-get-pods-resource)
  - [Lab: downwardAPI volume for metadata](#lab-downwardapi-volume-for-metadata)
  - [Lab: downwardAPI volume for resource](#lab-downwardapi-volume-for-resource)

---

## Downward API

- `Downward API`

  - a Kubernetes mechanism that allows a `container` to **consume information** about itself or its host without using the Kubernetes client or API server.
  - a way to **inject values** from the pod’s `metadata`, `spec`, or `status` fields down into the container.

- 2 types of injection:
  - as env ver
    - pod’s general metadata: `spec.containers.env.fieldRef`
    - resource constraints: `spec.containers.env.resourceFieldRef`
  - as file: `spec.volumes.downwardAPI`

---

### Common feilds

- Available from `fieldRef` field

| fieldRef Fields               | env   | vol   | DESC                                     |
| ----------------------------- | ----- | ----- | ---------------------------------------- |
| `metadata.name`               | Y     | Y     | pod’s name.                              |
| `metadata.namespace`          | Y     | Y     | pod’s namespace.                         |
| `metadata.uid`                | Y     | Y     | pod’s uid.                               |
| `metadata.labels`             | **N** | Y     | pod’s labels.                            |
| `metadata.labels['key']`      | Y     | Y     | value of the specified label.            |
| `metadata.annotations`        | **N** | Y     | pod’s annotations.                       |
| `metadata.annotations['key']` | Y     | Y     | The value of the specified annotation.   |
| `spec.nodeName`               | Y     | **N** | name of the worker node the pod runs on. |
| `spec.serviceAccountName`     | Y     | **N** | name of the pod’s service account.       |
| `status.podIP`                | Y     | **N** | pod’s IP address.                        |
| `status.hostIP`               | Y     | **N** | worker node’s IP address.                |

- Available from `resourceFieldRef` field

| resourceFieldRef Fields      | env | vol | DESC                                   |
| ---------------------------- | --- | --- | -------------------------------------- |
| `requests.cpu`               | Y   | Y   | container’s CPU request.               |
| `requests.memory`            | Y   | Y   | container’s memory request.            |
| `requests.ephemeral-storage` | Y   | Y   | container’s ephemeral storage request. |
| `limits.cpu`                 | Y   | Y   | container’s CPU limit.                 |
| `limits.memory`              | Y   | Y   | container’s memory limit.              |
| `limits.ephemeral-storage`   | Y   | Y   | container’s ephemeral storage limit.   |

- For **resource fields**, the `containerName` field must be specified because volumes are defined at the **pod level** and it isn’t obvious which container’s resources are being referenced.

---

## Lab: Get pod's metadata

```yaml
# demo-downapi-env-metadata.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-downapi-env-metadata
spec:
  containers:
    - name: busybox
      image: busybox
      env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: NODE_IP
          valueFrom:
            fieldRef:
              fieldPath: status.hostIP
      command:
        - sh
      args:
        - "-c"
        - |
          echo "node name:  $NODE_NAME"
          echo "node ip:    $NODE_IP"
          echo "pod name:   $POD_NAME"
          echo "pod ip:     $POD_IP"
          sleep 500
```

- Apply

```sh
kubectl apply -f demo-downapi-env-metadata.yaml
# pod/demo-downapi-env-metadata created

# check log
kubectl logs pod/demo-downapi-env-metadata
# node name:  docker-desktop
# node ip:    192.168.65.3
# pod name:   demo-downapi-env-metadata
# pod ip:     10.1.2.215

# confirm
kubectl get pod -o wide
# NAME                        READY   STATUS    RESTARTS   AGE     IP           NODE             NOMINATED NODE   READINESS GATES
# demo-downapi-env-metadata   1/1     Running   0          3m13s   10.1.2.215   docker-desktop   <none>           <none>

kubectl get node -o wide
# NAME             STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE         KERNEL-VERSION                       CONTAINER-RUNTIME
# docker-desktop   Ready    control-plane   51d   v1.34.1   192.168.65.3   <none>        Docker Desktop   5.15.153.1-microsoft-standard-WSL2   docker://28.5.1
```

---

## Lab: Get pod's Resource

```yaml
# demo-downapi-env-resource.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-downapi-env-resource
spec:
  containers:
    - name: busybox
      image: busybox
      env:
        - name: REQ_CPU_CORES
          valueFrom:
            resourceFieldRef:
              resource: requests.cpu
        - name: REQ_MEMORY_KB
          valueFrom:
            resourceFieldRef:
              resource: requests.memory
              divisor: 1k
        - name: REQ_EPHEMERAL_STORAGE
          valueFrom:
            resourceFieldRef:
              resource: requests.ephemeral-storage
              divisor: 1k
        - name: MAX_CPU_CORES
          valueFrom:
            resourceFieldRef:
              resource: limits.cpu
        - name: MAX_MEMORY_KB
          valueFrom:
            resourceFieldRef:
              resource: limits.memory
              divisor: 1M
        - name: MAX_EPHEMERAL_STORAGE
          valueFrom:
            resourceFieldRef:
              resource: limits.ephemeral-storage
              divisor: 1G
      command:
        - sh
      args:
        - "-c"
        - |
          echo "request cpu:                $REQ_CPU_CORES"
          echo "request memory:             $REQ_MEMORY_KB"
          echo "request ephemeral-storage:  $REQ_EPHEMERAL_STORAGE"
          echo "limit cpu:                  $MAX_CPU_CORES"
          echo "limit memory:               $MAX_MEMORY_KB"
          echo "limit ephemeral-storage:    $MAX_EPHEMERAL_STORAGE"
          sleep 500
```

- Apply

```sh
kubectl apply -f demo-downapi-env-resource.yaml
# pod/demo-downapi-env-resource created

# check log
kubectl logs pod/demo-downapi-env-resource
# request cpu:                0
# request memory:             0
# request ephemeral-storage:  0
# limit cpu:                  12
# limit memory:               8063
# limit ephemeral-storage:    973

```

---

## Lab: downwardAPI volume for metadata

```yaml
## demo-downapi-vol-meta.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-downapi-vol-meta
  labels:
    os: busybox
spec:
  volumes:
    - name: pod-meta
      downwardAPI:
        items:
          - path: pod-name.txt
            fieldRef:
              fieldPath: metadata.name
          - path: pod-labels.txt
            fieldRef:
              fieldPath: metadata.labels
          - path: pod-annotations.txt
            fieldRef:
              fieldPath: metadata.annotations
  containers:
    - name: busybox
      image: busybox
      volumeMounts:
        - name: pod-meta
          mountPath: /pod-metadata
      command:
        - sh
      args:
        - "-c"
        - |
          echo "pod name: $(cat /pod-metadata/pod-name.txt)"
          echo -e "pod labels: \n $(cat /pod-metadata/pod-labels.txt)\n"
          echo -e "pod annotations: \n $(cat /pod-metadata/pod-annotations.txt)\n"

          sleep 500
```

```sh
kubectl apply -f demo-downapi-vol-meta.yaml
# pod/demo-downapi-vol-meta created

kubectl logs pod/demo-downapi-vol-meta
# pod name: demo-downapi-vol-meta
# pod labels:
#  os="busybox"

# pod annotations:
#  kubectl.kubernetes.io/last-applied-configuration="{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{},\"labels\":{\"os\":\"busybox\"},\"name\":\"demo-downapi-vol-meta\",\"namespace\":\"default\"},\"spec\":{\"containers\":[{\"args\":[\"-c\",\"echo \\"pod name: $(cat /pod-metadata/pod-name.txt)\\"\necho -e \\"pod labels: \\n $(cat /pod-metadata/pod-labels.txt)\\n\\"\necho -e \\"pod annotations: \\n $(cat /pod-metadata/pod-annotations.txt)\\n\\"\n\nsleep 500\n\"],\"command\":[\"sh\"],\"image\":\"busybox\",\"name\":\"busybox\",\"volumeMounts\":[{\"mountPath\":\"/pod-metadata\",\"name\":\"pod-meta\"}]}],\"volumes\":[{\"downwardAPI\":{\"items\":[{\"fieldRef\":{\"fieldPath\":\"metadata.name\"},\"path\":\"pod-name.txt\"},{\"fieldRef\":{\"fieldPath\":\"metadata.labels\"},\"path\":\"pod-labels.txt\"},{\"fieldRef\":{\"fieldPath\":\"metadata.annotations\"},\"path\":\"pod-annotations.txt\"}]},\"name\":\"pod-meta\"}]}}
# "
# kubernetes.io/config.seen="2025-12-27T16:44:45.619494388Z"
# kubernetes.io/config.source="api"
```

---

## Lab: downwardAPI volume for resource

```yaml
# demo-downapi-vol-resource.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-downapi-vol-resource
  labels:
    os: busybox
spec:
  volumes:
    - name: pod-resource
      downwardAPI:
        items:
          - path: "cpu_request"
            resourceFieldRef:
              containerName: busybox
              resource: requests.cpu
              divisor: 1m
          - path: "cpu_limit"
            resourceFieldRef:
              containerName: busybox
              resource: limits.cpu
              divisor: 1m
  containers:
    - name: busybox
      image: busybox
      resources:
        requests:
          cpu: "250m"
          memory: "100Mi"
        limits:
          cpu: "500m"
          memory: "200Mi"
      volumeMounts:
        - name: pod-resource
          mountPath: /pod-resource
      command:
        - sh
      args:
        - "-c"
        - |
          echo "resource cpu: $(cat /pod-resource/cpu_request)"
          echo "limit cpu:    $(cat /pod-resource/cpu_limit)"

          sleep 500

```

```sh
kubectl apply -f demo-downapi-vol-resource.yaml
# pod/demo-downapi-vol-resource created

kubectl logs pod/demo-downapi-vol-resource
# resource cpu: 250
# limit cpu:    500
```