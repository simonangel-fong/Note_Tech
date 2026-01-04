# Kubernetes - Storage: Volume

[Back](../../index.md)

- [Kubernetes - Storage: Volume](#kubernetes---storage-volume)
  - [Container storage](#container-storage)
    - [Container Storage Interface](#container-storage-interface)
    - [Container Volume](#container-volume)
    - [Inject data as file using volume](#inject-data-as-file-using-volume)
  - [Pod Volume](#pod-volume)
    - [Lab: without volume vs with volume](#lab-without-volume-vs-with-volume)
      - [no volume](#no-volume)
      - [Pod volume](#pod-volume-1)

---

## Container storage

- each `container` has its own **isolated** `filesystem` provided by the `container image`.

- `Mounting`

  - the act of **attaching the filesystem** of the `storage device` or `volume` into a specific **location** in the operating system’s **file tree**

- **Note**: When any volume is mounted to a directory in the container’s filesystem, the files that are in the `container image` in that directory can **no longer be accessed**.
  - That is why `subPath` can be used.

---

### Container Storage Interface

- `Container Runtime interface(CRI)`
  - used to handle the communication between the Kubernetes and container runtimes.
- `Container Network Interface(CNI)`

  - used to coordinate between different network solution and kubernetes.

- `Container Storage Interface(CSI)`
  - used to coordinate between different storage solution and kubernetes.
  - define a set of `remote procedure calls(rpc)`

---

### Container Volume

- `Volume`

  - a **directory** accessible by `containers` along with the pod's lifecycle, allowing **data to persist** beyond a `container`'s lifecycle
  - **Lifecycle**:
    - Tied to the **pod's existence**
  - **Data Persistence**:
    - Data **persisted** when `container` **restarts**.
    - Data is **lost** when the `pod` is **deleted**
  - **Scope**:
    - Defined within the pod `spec`
  - no an API object

- Use case:
  - e.g.,
    - main container: web server, read only, show content, `/var/html`
    - sidecar container: agen app, read/write, edit content, `/var/data`
  - e.g.,
    - init container: create config file, read/write
    - main container: use config file, read only

---

- A `container` can **mount zero or more** of these `volumes` in **different locations**
- A `pod` can have **multiple** `volumes`
- A `volume` can be **mounted** in **more than one** `container` to share files.

---

### Inject data as file using volume

- inject data from:
  - `configMap` object: `spec.volumes.configMap`
  - `secret` object: `spec.volumes.secret`
  - `downwardAPI` object: `spec.volumes.downwardAPI`

---

## Pod Volume

- **Without** the `volume` mounted in the container, the **entire filesystem** of the `container` is **ephemeral**.
- Volumes can **persist data** across `container` **restarts**.
  - All `volumes` in a `pod` are created **when the `pod` is set up**
    - before any of its `containers` are **started**.
  - `Volumes` are **torn down** when the pod is **shut down**.
  - The **lifecycle** of a `volume` is **tied to** the **lifecycle** of the entire `pod`
    - **independent** of the **lifecycle** of the `container` in which it is mounted.
  - the new restrart container can access the same data in the mounted volume.

---

### Lab: without volume vs with volume

#### no volume

```yaml
# demo-non-volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-non-volume
spec:
  containers:
    - name: nginx
      image: nginx
    - name: mongo
      image: mongo
```

```sh
# create app
kubectl apply -f demo-non-volume.yaml
# pod/demo-non-volume created

# confirm
kubectl get pod
# NAME              READY   STATUS    RESTARTS   AGE
# demo-non-volume   2/2     Running   0          27s

# insert data
kubectl exec -it demo-non-volume -c mongo -- mongosh
db.telemetry.insertOne({device_id: 1, x: 1, y: 2});
# {
#   acknowledged: true,
#   insertedId: ObjectId('694b4e86dae1c244908de666')
# }

# get data
kubectl exec -it demo-non-volume -c mongo -- mongosh
db.telemetry.find()
# [
#   {
#     _id: ObjectId('694b4e86dae1c244908de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]

# shutdown db
kubectl exec -it demo-non-volume -c mongo -- mongosh admin --eval "db.shutdownServer()"
# command terminated with exit code 137

# monitor terminal
kubectl get ev -w
# 0s          Normal    Pulling     pod/demo-non-volume   Pulling image "mongo"
# 0s          Normal    Pulled      pod/demo-non-volume   Successfully pulled image "mongo" in 1.263s (1.263s including waiting). Image size: 327004046 bytes.
# 0s          Normal    Created     pod/demo-non-volume   Created container: mongo
# 0s          Normal    Started     pod/demo-non-volume   Started container mongo

kubectl get pod -w
# NAME              READY   STATUS    RESTARTS   AGE
# demo-non-volume   2/2     Running   0          3m32s
# demo-non-volume   1/2     NotReady   0          4m
# demo-non-volume   2/2     Running    1 (3s ago)   4m3s

kubectl describe pod demo-non-volume
# Events:
#   Type    Reason     Age                 From               Message
#   ----    ------     ----                ----               -------
#   Normal  Scheduled  5m11s               default-scheduler  Successfully assigned default/demo-non-volume to docker-desktop
#   Normal  Pulling    5m11s               kubelet            Pulling image "nginx"
#   Normal  Pulled     5m10s               kubelet            Successfully pulled image "nginx" in 1.256s (1.256s including waiting). Image size: 59795293 bytes.
#   Normal  Created    5m9s                kubelet            Created container: nginx
#   Normal  Started    5m9s                kubelet            Started container nginx
#   Normal  Pulled     5m8s                kubelet            Successfully pulled image "mongo" in 797ms (797ms including waiting). Image size: 327004046 bytes.
#   Normal  Pulling    71s (x2 over 5m9s)  kubelet            Pulling image "mongo"
#   Normal  Pulled     70s                 kubelet            Successfully pulled image "mongo" in 1.263s (1.263s including waiting). Image size: 327004046 bytes.
#   Normal  Created    69s (x2 over 5m8s)  kubelet            Created container: mongo
#   Normal  Started    69s (x2 over 5m8s)  kubelet            Started container mongo

# try to read data
kubectl exec -it demo-non-volume -c mongo -- mongosh --eval "db.telemetry.find()"
# none
```

> Pod has 2 containers: nginx + mongo
> container mongo restart, but nginx is still running, therefore the pod still runs.
> No data persists after mongo restart
> -> container without volume cannot persists data.

---

#### Pod volume

```yaml
# demo-volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-volume
spec:
  # pod vol
  volumes:
    - name: mongo-vol
      emptyDir: {}
  containers:
    - name: nginx
      image: nginx
    - name: mongo
      image: mongo
      volumeMounts:
        - name: mongo-vol # reference vol
          mountPath: /data/db # path in container
```

```sh
kubectl apply -f demo-volume.yaml
# pod/demo-volume created

kubectl get pod demo-volume
# NAME          READY   STATUS    RESTARTS   AGE
# demo-volume   2/2     Running   0          29s

# insert data
kubectl exec -it demo-volume -c mongo -- mongosh
db.telemetry.insertOne({device_id: 1, x: 1, y: 2});
# {
#   acknowledged: true,
#   insertedId: ObjectId('694b56d088e4cd1e7c8de666')
# }

# get data
kubectl exec -it demo-volume -c mongo -- mongosh
db.telemetry.find()
# [
#   {
#     _id: ObjectId('694b56d088e4cd1e7c8de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]

# shutdown db
kubectl exec -it demo-volume -c mongo -- mongosh admin --eval "db.shutdownServer()"
# command terminated with exit code 137

# monitor terminal
kubectl get ev -w
# 0s          Normal    Pulling     pod/demo-volume       Pulling image "mongo"
# 0s          Normal    Pulled      pod/demo-volume       Successfully pulled image "mongo" in 1.144s (1.144s including waiting). Image size: 327004046 bytes.
# 0s          Normal    Created     pod/demo-volume       Created container: mongo
# 0s          Normal    Started     pod/demo-volume       Started container mongo

kubectl get pod -w
# NAME          READY   STATUS    RESTARTS   AGE
# demo-volume   2/2     Running   0          3m12s
# demo-volume   1/2     NotReady   0          3m58s
# demo-volume   2/2     Running    1 (3s ago)   4m1s

kubectl describe pod demo-volume
# Events:
#   Type    Reason     Age                  From               Message
#   ----    ------     ----                 ----               -------
#   Normal  Scheduled  4m34s                default-scheduler  Successfully assigned default/demo-volume to docker-desktop
#   Normal  Pulling    4m34s                kubelet            Pulling image "nginx"
#   Normal  Pulled     4m33s                kubelet            Successfully pulled image "nginx" in 1.214s (1.215s including waiting). Image size: 59795293 bytes.
#   Normal  Created    4m32s                kubelet            Created container: nginx
#   Normal  Started    4m32s                kubelet            Started container nginx
#   Normal  Pulled     4m32s                kubelet            Successfully pulled image "mongo" in 764ms (764ms including waiting). Image size: 327004046 bytes.
#   Normal  Pulling    36s (x2 over 4m32s)  kubelet            Pulling image "mongo"
#   Normal  Created    35s (x2 over 4m31s)  kubelet            Created container: mongo
#   Normal  Pulled     35s                  kubelet            Successfully pulled image "mongo" in 1.144s (1.144s including waiting). Image size: 327004046 bytes.
#   Normal  Started    34s (x2 over 4m31s)  kubelet            Started container mongo

# try to read data
kubectl exec -it demo-volume -c mongo -- mongosh --eval "db.telemetry.find()"
# [
#   {
#     _id: ObjectId('694b56d088e4cd1e7c8de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]
```

---
