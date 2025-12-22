# Kubernetes - Pod: Multi-containers

[Back](../../index.md)

- [Kubernetes - Pod: Multi-containers](#kubernetes---pod-multi-containers)
  - [Multi-containers Pod](#multi-containers-pod)
  - [Co-located containers](#co-located-containers)
    - [Lab: Co-located Containers](#lab-co-located-containers)

---

## Multi-containers Pod

- `multi-containers pod`

  - the pod that runs multiple containers to compose a single, tightly-coupled workload.

- features:

  - share the same network (IP address)
  - share volumes (files/directories)
  - have coordinated Pod lifecycle
    - scheduled together
    - if the Pod dies, all containers go down

- Common multi-containers patterns:
  - `Co-located containers`
  - `Init containers`
  - `Sidecar containers`

---

## Co-located containers

- `co-located containers`
  - individual **containers** that run together inside a Pod
  - containers are **equal partners** inside the Pod.
    - all start together, not in a sequence

---

- Example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myWebApp
spec:
  containers:
    - name: web-app
      image: web-app
      ports:
        - containerPort: 8080
    - name: main-app
      image: main-app
```

---

### Lab: Co-located Containers

- `colocated_container.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: colocated-containers-demo
spec:
  containers:
    - name: busybox
      image: busybox
      command: ["sh", "-c", "echo The app is running! && sleep 3600"]
    - name: redis
      image: redis
```

```sh
kubectl create -f colocated_container.yaml
# pod/colocated-containers-demo created

kubectl get pod colocated-containers-demo
# NAME                        READY   STATUS    RESTARTS   AGE
# colocated-containers-demo   2/2     Running   0          22s

kubectl describe pod colocated-containers-demo
# Name:             colocated-containers-demo
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             docker-desktop/192.168.65.3
# Start Time:       Fri, 31 Oct 2025 15:03:10 -0400
# Labels:           <none>
# Annotations:      <none>
# Status:           Running
# IP:               10.1.0.142
# IPs:
#   IP:  10.1.0.142
# Containers:
#   busybox:
#     Container ID:  docker://1f1df002aa159aaedc33cd9b691b612cd0a33cffdf1e41791053a8ff211c23e4
#     Image:         busybox
#     Image ID:      docker-pullable://busybox@sha256:e3652a00a2fabd16ce889f0aa32c38eec347b997e73bd09e69c962ec7f8732ee
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       sh
#       -c
#       echo The app is running! && sleep 3600
#     State:          Running
#       Started:      Fri, 31 Oct 2025 15:03:11 -0400
#     Ready:          True
#     Restart Count:  0
#     Environment:    <none>
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-j49vw (ro)
#   redis:
#     Container ID:   docker://31c028656cb724485cb526caceb119ef2c5fb98554b4236905d221882591aa3c
#     Image:          redis
#     Image ID:       docker-pullable://redis@sha256:4521b581dbddea6e7d81f8fe95ede93f5648aaa66a9dacd581611bf6fe7527bd
#     Port:           <none>
#     Host Port:      <none>
#     State:          Running
#       Started:      Fri, 31 Oct 2025 15:03:12 -0400
#     Ready:          True
#     Restart Count:  0
#     Environment:    <none>
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-j49vw (ro)
# Conditions:
#   Type                        Status
#   PodReadyToStartContainers   True
#   Initialized                 True
#   Ready                       True
#   ContainersReady             True
#   PodScheduled                True
# Volumes:
#   kube-api-access-j49vw:
#     Type:                    Projected (a volume that contains injected data from multiple sources)
#     TokenExpirationSeconds:  3607
#     ConfigMapName:           kube-root-ca.crt
#     Optional:                false
#     DownwardAPI:             true
# QoS Class:                   BestEffort
# Node-Selectors:              <none>
# Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
#                              node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
# Events:
#   Type    Reason     Age   From               Message
#   ----    ------     ----  ----               -------
#   Normal  Scheduled  56s   default-scheduler  Successfully assigned default/colocated-containers-demo to docker-desktop
#   Normal  Pulling    56s   kubelet            Pulling image "busybox"
#   Normal  Pulled     55s   kubelet            Successfully pulled image "busybox" in 684ms (684ms including waiting). Image size: 2224358 bytes.
#   Normal  Created    55s   kubelet            Created container: busybox
#   Normal  Started    55s   kubelet            Started container busybox
#   Normal  Pulling    55s   kubelet            Pulling image "redis"
#   Normal  Pulled     54s   kubelet            Successfully pulled image "redis" in 687ms (687ms including waiting). Image size: 52458645 bytes.
#   Normal  Created    54s   kubelet            Created container: redis
#   Normal  Started    54s   kubelet            Started container redis
```

---
