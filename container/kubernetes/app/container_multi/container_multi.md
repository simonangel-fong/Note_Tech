# Kubernetes - Pod: Multi-containers

[Back](../../index.md)

- [Kubernetes - Pod: Multi-containers](#kubernetes---pod-multi-containers)
  - [Multi-containers Pod](#multi-containers-pod)
  - [Co-located containers](#co-located-containers)
    - [Lab: Co-located Containers](#lab-co-located-containers)
  - [Init containers](#init-containers)
    - [Lab: Init Containers](#lab-init-containers)
  - [Sidecar containers](#sidecar-containers)
    - [Lab: Sidecar Container](#lab-sidecar-container)
  - [Init Container vs Sidecar Container](#init-container-vs-sidecar-container)

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

## Init containers

- `init containers`/`regular init containers`

  - containers that only run during Pod startup.
  - the **secondary containers** that **starts and runs before** the **main application containers** within the **same** `Pod`.
  - the containers in a `multi-containers pod` that starts and runs before the main application containers.
  - A `pod` can have **multiple** `init containers`.
    - `kubelet` runs the Pod's `init containers` **in the order** they appear in the Pod's `spec`.
  - start before the main container

- features:

  - **Ordered, blocking startup;**
    - `Init containers` always **run to completion**.
    - Each `init container` **must complete successfully** before the next one starts.
  - **Failures prevent Pod readiness**
    - If a Pod's `init container` **fails**, the `kubelet` **repeatedly restarts** that `init container` until it succeeds.
    - However, if the Pod has a **restartPolicy of Never**, and an `init container` fails during startup of that Pod, Kubernetes treats the overall Pod as **failed**.

- When `Init container` fails

  - `Pod` never starts its regular containers.
  - `Pod` stays in `Init:CrashLoopBackOff` (effectively failed until the init succeeds).

- Common Commands:

| CMD                                                       | DESC                                 |
| --------------------------------------------------------- | ------------------------------------ |
| `kubectl describe pod pod_name \| grep "Init Containers"` | Check if a pod has an ini containers |

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
   initContainers:
    # 1st init con
    - name: db-checker
      image: busybox
      command: 'wait-for-db-ready.sh'
    # 2nd init con
    - name: api-checker
      image: busybox
      command: "wait-for-api-ready.sh"
```

> run init containers: db-checker -> api-checker

---

### Lab: Init Containers

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-containers-demo
spec:
  containers:
    - name: main-app
      image: nginx
  initContainers:
    - name: 1st-check
      image: busybox
      command:
        [
          "sh",
          "-c",
          "echo 1st-check starts. && sleep 10 && echo 1st-check completed.",
        ]
    - name: 2nd-check
      image: busybox
      command:
        [
          "sh",
          "-c",
          "echo 2nd-check starts. && sleep 10 && echo 2nd-check completed.",
        ]
```

```sh
kubectl create -f init_container.yaml
# pod/init-containers-demo created

kubectl get pod --watch
# NAME                   READY   STATUS     RESTARTS   AGE
# init-containers-demo   0/1     Init:0/2   0          4s
# init-containers-demo   0/1     Init:1/2   0          13s
# init-containers-demo   0/1     Init:1/2   0          14s
# init-containers-demo   0/1     PodInitializing   0          25s
# init-containers-demo   1/1     Running           0          27s

kubectl describe pod init-containers-demo
# Init Containers:
#   1st-check:
#     Image:         busybox
#     Command:
#       sh
#       -c
#       echo 1st-check starts. && sleep 10 && echo 1st-check completed.
#     State:          Terminated
#       Reason:       Completed
#       Exit Code:    0
#     Ready:          True
#     Restart Count:  0
#   2nd-check:
#     Image:         busybox
#     Command:
#       sh
#       -c
#       echo 2nd-check starts. && sleep 10 && echo 2nd-check completed.
#     State:          Terminated
#       Reason:       Completed
#       Exit Code:    0
#     Ready:          True
#     Restart Count:  0
# Containers:
#   main-app:
#     Image:          nginx
#     Port:           <none>
#     State:          Running
#     Ready:          True
#     Restart Count:  0


# Events:
#   Type    Reason     Age   From               Message
#   ----    ------     ----  ----               -------
#   Normal  Scheduled  59s   default-scheduler  Successfully assigned default/init-containers-demo to docker-desktop
#   Normal  Pulling    59s   kubelet            Pulling image "busybox"
#   Normal  Pulled     58s   kubelet            Successfully pulled image "busybox" in 1.13s (1.13s including waiting). Image size: 2224358 bytes.
#   Normal  Created    57s   kubelet            Created container: 1st-check
#   Normal  Started    57s   kubelet            Started container 1st-check
#   Normal  Pulling    46s   kubelet            Pulling image "busybox"
#   Normal  Pulled     46s   kubelet            Successfully pulled image "busybox" in 527ms (527ms including waiting). Image size: 2224358 bytes.
#   Normal  Created    46s   kubelet            Created container: 2nd-check
#   Normal  Started    46s   kubelet            Started container 2nd-check
#   Normal  Pulling    34s   kubelet            Pulling image "nginx"
#   Normal  Pulled     33s   kubelet            Successfully pulled image "nginx" in 1.056s (1.056s including waiting). Image size: 59773923 bytes.
#   Normal  Created    33s   kubelet            Created container: main-app
#   Normal  Started    33s   kubelet            Started container main-app
```

---

## Sidecar containers

- `sidecar containers`

  - a special case of `init containers`.(From offical doc)
  - the **secondary** containers that **run along with** the **main application container** within the **same** `Pod`.
  - used to **enhance or to extend the functionality** of the primary app container by providing additional services, or functionality such as **logging, monitoring, security, or data synchronization**, **without directly altering the primary application code**.

- Common use case:

  - ElasticSearch DB starts and continuously running
  - Kibana, the main application to display a dashboard, starts after

- specify a `restartPolicy` for containers listed in a Pod's `initContainers` field.

  - make container **independent** from other `init containers` and from the **main application container**(s) within the same pod.
  - can be started, stopped, or restarted **without affecting** the **main application container** and other `init containers`.
  - start and **remain running** **during the entire life** of the `Pod`.

- **Changing the image** of a `sidecar container` will **not** cause the `Pod` to **restart**, but will trigger a **container restart**.

- `sidecar containers` **support** `probes` to control their lifecycle.

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
   initContainers:
    - name: db-checker
      image: busybox
      command: 'wait-for-db-ready.sh'
      restartPolicy: Always     # ensures containers are continuously running
```

---

### Lab: Sidecar Container

- `sidecar_container.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: sidecar-containers-demo
spec:
  containers:
    - name: main-app
      image: nginx
  initContainers:
    - name: 1st-check
      image: busybox
      command:
        [
          "sh",
          "-c",
          "echo 1st-check starts. && sleep 10 && echo 1st-check completed.",
        ]
      restartPolicy: Always
    - name: 2nd-check
      image: busybox
      command:
        [
          "sh",
          "-c",
          "echo 2nd-check starts. && sleep 10 && echo 2nd-check completed.",
        ]
```

```sh
kubectl replace --force -f sidecar_container.yaml
kubectl create -f sidecar_container.yaml
# pod/sidecar-containers-demo created

kubectl get pod --watch
# NAME                      READY   STATUS     RESTARTS   AGE
# sidecar-containers-demo   0/2     Init:0/2   0          0s
# sidecar-containers-demo   1/2     Init:1/2   0          4s
# sidecar-containers-demo   1/2     Init:1/2   0          6s
# sidecar-containers-demo   1/2     PodInitializing   0          16s
# sidecar-containers-demo   2/2     Running           0          18

kubectl describe pod sidecar-containers-demo
# Init Containers:
#   1st-check:
#     Image:          nginx
#     State:          Running
#     Ready:          True
#   2nd-check:
#     Image:         busybox
#     Command:
#       sh
#       -c
#       echo 2nd-check starts. && sleep 10 && echo 2nd-check completed.
#     State:          Terminated
#       Reason:       Completed
#       Exit Code:    0
#     Ready:          True
# Containers:
#   main-app:
#     Image:          redis
#     State:          Running
#     Ready:          True

# Events:
#   Type    Reason     Age   From               Message
#   ----    ------     ----  ----               -------
#   Normal  Created    79s   kubelet            Created container: 1st-check
#   Normal  Started    79s   kubelet            Started container 1st-check
#   Normal  Pulling    78s   kubelet            Pulling image "busybox"
#   Normal  Pulled     77s   kubelet            Successfully pulled image "busybox" in 1.362s (1.362s including waiting). Image size: 2224358 bytes.
#   Normal  Created    77s   kubelet            Created container: 2nd-check
#   Normal  Started    77s   kubelet            Started container 2nd-check
#   Normal  Pulling    66s   kubelet            Pulling image "redis"
#   Normal  Pulled     65s   kubelet            Successfully pulled image "redis" in 963ms (963ms including waiting). Image size: 52458645 bytes.
#   Normal  Created    65s   kubelet            Created container: main-app
#   Normal  Started    65s   kubelet            Started container main-app

```

---

## Init Container vs Sidecar Container

| Dimension      | **Init (regular)**                                                | **Sidecar (native)**                                                                                         |
| -------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Where declared | `spec.initContainers`                                             | `spec.initContainers`                                                                                        |
| Key field      | _(no special restart policy)_                                     | `restartPolicy: Always`                                                                                      |
| Start order    | Before all app containers                                         | Starts **before** app containers (ordered), then app containers start                                        |
| Duration       | Runs to completion; then **exits**                                | Long-running; **remains** for Pod lifetime                                                                   |
| On failure     | **Blocks** Pod readiness; retried until success                   | Restarts automatically; Pod may be NotReady if probes fail                                                   |
| Probes         | Regular inits **don’t support** liveness/readiness/startup probes | Sidecars **can** use readiness (affects Pod Ready) and other probes                                          |
| Data/IPC       | Can prep volumes/env only during init                             | Shares volumes/localhost with app during runtime                                                             |
| Shutdown       | N/A (already exited)                                              | Shuts down when Pod ends; for Jobs, native sidecars exit once primary containers finish so Jobs can complete |

---
