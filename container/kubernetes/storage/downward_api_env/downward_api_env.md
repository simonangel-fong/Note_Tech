# Kubernetes: Storage - Use Downward API as Environment Variable

[Back](../../index.md)

- [Kubernetes: Storage - Use Downward API as Environment Variable](#kubernetes-storage---use-downward-api-as-environment-variable)
  - [Lab: Get pod's Metadata as Environment Variable](#lab-get-pods-metadata-as-environment-variable)
  - [Lab: Get pod's Resource as Environment Variable](#lab-get-pods-resource-as-environment-variable)

---

## Lab: Get pod's Metadata as Environment Variable

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

## Lab: Get pod's Resource as Environment Variable

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
