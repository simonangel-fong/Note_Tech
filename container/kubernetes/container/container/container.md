




## container Status and state

- `Waiting`: waiting to be started
- `Running`: the `container` has been **created** and `processes` are **running** in it
- `Terminated`: the `processes` that had been **running** in the container have **terminated**.
- `Unknown`: The state of the container **couldn’t be determined**

### Init Container Status

- In the `status.initContainerStatuses` field

---

### Lab: Get Container Status and state

```sh
kubectl describe pod web
# ...
# Containers:
#   web:
#     Container ID:   docker://1f12820fdf03c49c3f454d34e92c25bddfbcd74eb60bb550401d35bee8c06360
#     Image:          nginx
#     Image ID:       docker-pullable://nginx@sha256:fb01117203ff38c2f9af91db1a7409459182a37c87cced5cb442d1d8fcc66d19
#     Port:           <none>
#     Host Port:      <none>
#     State:          Running
#       Started:      Mon, 22 Dec 2025 17:02:01 -0500
#     Ready:          True
#     Restart Count:  0
#     Environment:    <none>
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-qmvjn (ro)
# ...


kubectl get pod web -o json | jq .status.containerStatuses
# [
#   {
#     "containerID": "docker://1f12820fdf03c49c3f454d34e92c25bddfbcd74eb60bb550401d35bee8c06360",
#     "image": "nginx:latest",
#     "imageID": "docker-pullable://nginx@sha256:fb01117203ff38c2f9af91db1a7409459182a37c87cced5cb442d1d8fcc66d19",
#     "lastState": {},
#     "name": "web",
#     "ready": true,
#     "resources": {},
#     "restartCount": 0,
#     "started": true,
#     "state": {
#       "running": {
#         "startedAt": "2025-12-22T22:02:01Z"
#       }
#     },
#     "volumeMounts": [
#       {
#         "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount",
#         "name": "kube-api-access-qmvjn",
#         "readOnly": true,
#         "recursiveReadOnly": "Disabled"
#       }
#     ]
#   }
# ]
```

---

### Lab: Pod phase

#### Running a pod

```yaml
# demo_pod_state.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: web
  name: web
spec:
  containers:
    - image: nginx
      name: web
```

- Apply

```sh
# terminal A:
kubectl apply -f demo_pod_state.yaml
# pod/web created

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS    RESTARTS   AGE
# web    0/1     Pending   0          0s
# web    0/1     Pending   0          0s
# web    0/1     ContainerCreating   0          0s
# web    1/1     Running             0          8s
```

---

#### Update a pod manifest file

```yaml
# demo_pod_state.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: web-app # updated
  name: web
spec:
  containers:
    - image: nginx
      name: web
```

- Apply

```sh
# terminal A:
kubectl apply -f demo_pod_state.yaml
# pod/web configured

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS    RESTARTS   AGE
# web    1/1     Running   0          14s
# web    1/1     Running   0          64s
# web    1/1     Running   0          64s
# web    1/1     Running   1 (5s ago)   69s
```

---

#### edit

```sh
# edit: update image: nginx:1.29.4-alpine
kubectl edit pod web
# pod/web edited

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS    RESTARTS      AGE
# web    1/1     Running   1 (42s ago)   106s
```

---

#### Deleting a pod

```sh
# terminal A:
kubectl delete -f demo_pod_state.yaml
# pod "web" deleted from default namespace

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS    RESTARTS        AGE
# web    1/1     Running   1 (4m50s ago)   5m54s
# web    1/1     Terminating   1 (7m12s ago)   8m16s
# web    1/1     Terminating   1 (7m12s ago)   8m16s
# web    0/1     Completed     1 (7m13s ago)   8m17s
# web    0/1     Completed     1               8m18s
# web    0/1     Completed     1               8m18s
# web    0/1     Completed     1               8m18s
```

---

#### Lab: Pod state - ErrImagePull

```sh
# terminal A:
kubectl run web --image=xnign
# pod/web created

kubectl delete pod web
# pod "web" deleted from default namespace

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS    RESTARTS   AGE
# web    0/1     Pending   0          0s
# web    0/1     Pending   0          0s
# web    0/1     ContainerCreating   0          0s
# web    0/1     ErrImagePull        0          1s
# web    0/1     ImagePullBackOff    0          16s
# web    0/1     ErrImagePull        0          31s
# web    0/1     ImagePullBackOff    0          42s
# web    0/1     ErrImagePull        0          56s
# web    0/1     ImagePullBackOff    0          71s
# web    0/1     ErrImagePull        0          101s
# web    0/1     ImagePullBackOff    0          116s
# web    0/1     Terminating         0          2m59s
# web    0/1     Terminating         0          2m59s
# web    0/1     Terminating         0          3m
# web    0/1     ContainerStatusUnknown   0          3m1s
# web    0/1     ContainerStatusUnknown   0          3m1s
# web    0/1     ContainerStatusUnknown   0          3m1s
# ...
```

---

#### Lab: Pod state - One-off Complete

- indefinite/one-off pod:
  - `--restart=Never`

```sh
# terminal A:
kubectl run demo --image=busybox --restart=Never -- sleep 10
# pod/demo created

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS    RESTARTS   AGE
# demo   0/1     Pending   0          0s
# demo   0/1     Pending   0          0s
# demo   0/1     ContainerCreating   0          0s
# demo   1/1     Running             0          3s
# demo   0/1     Completed           0          13s
# demo   0/1     Completed           0          14s
```

- Delete

```sh
# terminal A:
kubectl get pod
# NAME   READY   STATUS      RESTARTS   AGE
# demo   0/1     Completed   0          78

kubectl delete pod demo
# pod "demo" deleted from default namespace

kubectl get pod
# No resources found in default namespace.

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS      RESTARTS   AGE
# demo   0/1     Completed   0          114s
# demo   0/1     Completed   0          2m
# demo   0/1     Completed   0          2m
```

---

#### Lab: Pod state - one-off Failed

- indefinite/one-off pod:
  - `--restart=Never`

```sh
# terminal A:
kubectl run demo --image=busybox --restart=Never -- slep 10 # incoreect command
# pod/demo created

kubectl get pod
# NAME   READY   STATUS               RESTARTS   AGE
# demo   0/1     ContainerCannotRun   0          67s

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS    RESTARTS   AGE
# demo   0/1     Pending   0          0s
# demo   0/1     Pending   0          0s
# demo   0/1     ContainerCreating   0          0s
# demo   0/1     ContainerCannotRun   0          3s
# demo   0/1     ContainerCannotRun   0          4s
```

- Delete

```sh
# terminal A:
kubectl delete pod demo
# pod "demo" deleted from default namespace

kubectl get pod
# No resources found in default namespace.

# terminal B:
kubectl get pod --watch
# NAME   READY   STATUS               RESTARTS   AGE
# demo   0/1     ContainerCannotRun   0          2m42s
# demo   0/1     ContainerCannotRun   0          2m49s
# demo   0/1     ContainerCannotRun   0          2m49s
```

---
