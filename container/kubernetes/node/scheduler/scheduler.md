# Kubernetes - Control Plane: Scheduler

[Back](../../index.md)

- [Kubernetes - Control Plane: Scheduler](#kubernetes---control-plane-scheduler)
  - [Scheduler](#scheduler)
    - [How it works - From API to Kubelet](#how-it-works---from-api-to-kubelet)
    - [!!!How it works - Phases](#how-it-works---phases)
      - [Scheduling Queue](#scheduling-queue)
    - [Scheduling Process](#scheduling-process)
    - [Scheduler Policies \& Features](#scheduler-policies--features)
  - [Imperative Command](#imperative-command)
  - [Lab: Scheduler info](#lab-scheduler-info)

---

## Scheduler

- `scheduler`

  - a `control plane` component responsible for **deciding** which `node` a newly created `Pod` should run on.
    - doesn’t run the Pod itself
    - only makes placement decisions.

- Types of Scheduling
  - **Manual** Scheduling:
    - By **specifying nodeName directly** in the `Pod spec`.
  - **Default** Scheduler:
    - Built into Kubernetes, covers most needs.
  - **Multiple** Schedulers:
    - can run custom schedulers alongside the default one.

---

### How it works - From API to Kubelet

- When a Pod is created:

1. User or Controller sends a **Pod creation request** to the `API server`.
   - e.g.,
     - user: `kubectl apply -f pod.yaml`
     - Controller: ReplicaSet creates a Pod.
2. `API server` stores the new `Pod` object in `etcd`.
   - At this point, the `Pod` has **no** `nodeName` assigned, so its status is `Pending`.
3. `Scheduler` monitors the `API server` for Pods in the `Pending` state (Pods without nodeName).
4. `Scheduler` retrieves the list of **available** `nodes` from the `API server`.
5. `Scheduler` filters out `nodes` that cannot host the Pod.
   - e.g., insufficient CPU/memory, taints not tolerated, node affinity not satisfied.
6. `Scheduler` scores the remaining nodes according to preferences.
   - e.g., balance load, spread Pods, use node affinity, pack Pods together.
7. `Scheduler` selects the **highest-scoring** `node` as the placement target.
8. `Scheduler` **updates** the `Pod object` in the `API server` by setting the `nodeName` field.
9. `Kubelet` on the chosen node sees the updated `Pod assignment` and **starts the container(s)** by pulling the image and running it.

---

### !!!How it works - Phases

- ref:

  - https://github.com/kubernetes/community/blob/master/contributors/devel/sig-scheduling/scheduling_code_hierarchy_overview.md
  - https://kubernetes.io/blog/2017/03/advanced-scheduling-in-kubernetes/

- Example

- Multiple nodes are avaialable with vary cpu and memory.
- Multiple pods are waiting for being scheduled.
- Pod defined to be scheduled.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webapp
spec:
  priorityClassName: high-priority
  container: data-processor
  - name: webapp
    image: webapp
    resources:
      requests:
        memory: "1Gi"
        cpu: 10
```

---

#### Scheduling Queue

- `Scheduling Queue`:
  - a schedule phase where pods **are sorted based on the priority** defined on the pods.
  - pods with **higher priority** gets to the **beginning of the queue** to be scheduled **first**.

---

### Scheduling Process

- **Filtering (Predicates)**
  - The `scheduler` **filters out** `nodes` that **cannot** host the `Pod`.
  - e.g.,
    - Not enough CPU/memory
    - Node taints not tolerated
    - NodeSelector/NodeAffinity rules don’t match
- **Scoring (Priorities)**
  - Among the remaining nodes, the scheduler scores them to pick the “best” one.
  - e.g.,
    - Spreading Pods across nodes (anti-affinity)
    - Packing Pods to save resources
    - Prioritizing nodes with certain labels

---

### Scheduler Policies & Features

- `NodeSelector`:

  - Assign Pod to nodes with **specific labels**.

- `Affinity` / `Anti-Affinity`:

  - Place Pods together or apart (e.g., high availability).

- `Taints` and `Tolerations`:

  - Control which Pods can run on **“special”** nodes.

- `Resource Requests & Limits`:

  - Ensures Pods land where resources are **sufficient**.

- `Priority Classes & Preemption`:
  - **Higher**-priority Pods can **evict** **lower**-priority ones if necessary.

---

## Imperative Command

| Command                                                           | Description                                     |
| ----------------------------------------------------------------- | ----------------------------------------------- |
| `kubectl get pods -n kube-system \| grep scheduler`               | Get scheduler Pod in the kube-system namespace. |
| `kubectl describe pod kube-scheduler-controlplane -n kube-system` | Get infomation of scheduler pod                 |
| `kubectl logs kube-scheduler-controlplane -n kube-system`         | Show the log of scheduling decision-making.     |

---

## Lab: Scheduler info

```sh
kubectl get pods -n kube-system | grep scheduler
# kube-scheduler-docker-desktop            1/1     Running   7 (21h ago)    5d9h

kubectl describe pod kube-scheduler-controlplane -n kube-system
# Name:                 kube-scheduler-docker-desktop
# Namespace:            kube-system
# Priority:             2000001000
# Priority Class Name:  system-node-critical
# Node:                 docker-desktop/192.168.65.3
# Start Time:           Mon, 29 Sep 2025 10:19:05 -0400
# Labels:               component=kube-scheduler
#                       tier=control-plane
# Annotations:          kubernetes.io/config.hash: bfe797ff5a3ebaafbe14820f2b118e22
#                       kubernetes.io/config.mirror: bfe797ff5a3ebaafbe14820f2b118e22
#                       kubernetes.io/config.seen: 2025-09-25T02:21:47.740404014Z
#                       kubernetes.io/config.source: file
# Status:               Running
# SeccompProfile:       RuntimeDefault
# IP:                   192.168.65.3
# IPs:
#   IP:           192.168.65.3
# Controlled By:  Node/docker-desktop
# Containers:
#   kube-scheduler:
#     Container ID:  docker://7ed6565ec02ad61983ec3fcfdab714eb171884c2f10087751bd2eb60163c3057
#     Image:         registry.k8s.io/kube-scheduler:v1.32.2
#     Image ID:      docker-pullable://registry.k8s.io/kube-scheduler@sha256:45710d74cfd5aa10a001d0cf81747b77c28617444ffee0503d12f1dcd7450f76
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       kube-scheduler
#       --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
#       --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
#       --bind-address=127.0.0.1
#       --kubeconfig=/etc/kubernetes/scheduler.conf
#       --leader-elect=true
#     State:          Running
#       Started:      Mon, 29 Sep 2025 10:19:07 -0400
#     Last State:     Terminated
#       Reason:       Error
#       Exit Code:    255
#       Started:      Sat, 27 Sep 2025 17:21:37 -0400
#       Finished:     Mon, 29 Sep 2025 10:18:45 -0400
#     Ready:          True
#     Restart Count:  7
#     Requests:
#       cpu:        100m
#     Liveness:     http-get https://127.0.0.1:10259/livez delay=10s timeout=15s period=10s #success=1 #failure=8
#     Readiness:    http-get https://127.0.0.1:10259/readyz delay=0s timeout=15s period=1s #success=1 #failure=3
#     Startup:      http-get https://127.0.0.1:10259/livez delay=10s timeout=15s period=10s #success=1 #failure=24
#     Environment:  <none>
#     Mounts:
#       /etc/kubernetes/scheduler.conf from kubeconfig (ro)
# Conditions:
#   Type                        Status
#   PodReadyToStartContainers   True
#   Initialized                 True
#   Ready                       True
#   ContainersReady             True
#   PodScheduled                True
# Volumes:
#   kubeconfig:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/kubernetes/scheduler.conf
#     HostPathType:  FileOrCreate
# QoS Class:         Burstable
# Node-Selectors:    <none>
# Tolerations:       :NoExecute op=Exists
# Events:            <none>

kubectl logs kube-scheduler-controlplane -n kube-system
# I0929 14:19:09.535015       1 serving.go:386] Generated self-signed cert in-memory
# W0929 14:19:12.446250       1 requestheader_controller.go:204] Unable to get configmap/extension-apiserver-authentication in kube-system.  Usually fixed by 'kubectl create rolebinding -n kube-system ROLEBINDING_NAME --role=extension-apiserver-authentication-reader --serviceaccount=YOUR_NS:YOUR_SA'
# W0929 14:19:12.446314       1 authentication.go:397] Error looking up in-cluster authentication configuration: configmaps "extension-apiserver-authentication" is forbidden: User "system:kube-scheduler" cannot get resource "configmaps" in API group "" in the namespace "kube-system"
# W0929 14:19:12.446333       1 authentication.go:398] Continuing without authentication configuration. This may treat all requests as anonymous.
# W0929 14:19:12.446343       1 authentication.go:399] To require authentication configuration lookup to succeed, set --authentication-tolerate-lookup-failure=false
# I0929 14:19:12.487553       1 server.go:166] "Starting Kubernetes Scheduler" version="v1.32.2"
# I0929 14:19:12.487596       1 server.go:168] "Golang settings" GOGC="" GOMAXPROCS="" GOTRACEBACK=""
# I0929 14:19:12.491828       1 configmap_cafile_content.go:205] "Starting controller" name="client-ca::kube-system::extension-apiserver-authentication::client-ca-file"
# I0929 14:19:12.491840       1 secure_serving.go:213] Serving securely on 127.0.0.1:10259
# I0929 14:19:12.491860       1 tlsconfig.go:243] "Starting DynamicServingCertificateController"
# I0929 14:19:12.493343       1 shared_informer.go:313] Waiting for caches to sync for client-ca::kube-system::extension-apiserver-authentication::client-ca-file
# I0929 14:19:12.593017       1 leaderelection.go:257] attempting to acquire leader lease kube-system/kube-scheduler...
# I0929 14:19:12.594132       1 shared_informer.go:320] Caches are synced for client-ca::kube-system::extension-apiserver-authentication::client-ca-file
# I0929 14:19:28.061242       1 leaderelection.go:271] successfully acquired lease kube-system/kube-scheduler
```

---
