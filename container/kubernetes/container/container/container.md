# Kubernetes: Container

[Back](../../index.md)

- [Kubernetes: Container](#kubernetes-container)
  - [Container](#container)
  - [Container Status and state](#container-status-and-state)
    - [Lab: Get Container Status and state](#lab-get-container-status-and-state)

---

## Container

- `Containers` are designed to run **only a single** `process`, not counting any `child processes` that it spawns.

  - `Container` only **restarts** when the `root process` dies.
  - e.g., container_w (process_w) writes log; Container_r (Process_r) reads log.
    - If process_w dies, only requires container_w restart.
  - Otherwise, hard to manage
    - e.g., One container (2 processes) read and write log. If either process dies, whether the whole container restarts.

- Therefore, one `container` **should not** have **multiple** `processes`.

---

## Container Status and state

- `Waiting`: waiting to be started
- `Running`: the `container` has been **created** and `processes` are **running** in it
- `Terminated`: the `processes` that had been **running** in the container have **terminated**.
- `Unknown`: The state of the container **couldn’t be determined**

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
