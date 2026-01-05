# Kubernetes: Storage - Use Downward API as Volume

[Back](../../index.md)

- [Kubernetes: Storage - Use Downward API as Volume](#kubernetes-storage---use-downward-api-as-volume)
  - [Lab: downwardAPI volume for metadata](#lab-downwardapi-volume-for-metadata)
  - [Lab: downwardAPI volume for resource](#lab-downwardapi-volume-for-resource)

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
