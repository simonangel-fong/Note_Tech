# Kubernetes - Pod: Multiple Container - Init Container

[Back](../../index.md)

- [Kubernetes - Pod: Multiple Container - Init Container](#kubernetes---pod-multiple-container---init-container)
  - [Init containers](#init-containers)
    - [idempotent](#idempotent)
    - [Common Commands:](#common-commands)
    - [Lab: Init Containers](#lab-init-containers)

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

- Common use case:

  - Initialize files in the volumes used by the pod’s main containers.
    - e.g.,
      - retrieving certificates and private keys used by the main container from secure certificate stores,
      - generating config files,
      - downloading data
  - Initialize the pod’s networking system.
  - Delay the start of the pod’s main containers until a precondition is met
    - e.g.,
      - confirm rds starts before backend starts

- When `Init container` fails

  - `Pod` never starts its regular containers.
  - `Pod` stays in `Init:CrashLoopBackOff` (effectively failed until the init succeeds).

---

### idempotent

- `Init containers` are normally **only executed once**.
  - Even if one of the pod’s `main containers` is **terminated** later, the pod’s `init containers` are not reexecuted.
- if it requires to **restart** the entire `pod`, the pod’s `init containers` might be **executed again**.
  - `init containers` must be **idempotent**.

---

### Common Commands:

| CMD                                                       | DESC                                 |
| --------------------------------------------------------- | ------------------------------------ |
| `kubectl describe pod pod_name \| grep "Init Containers"` | Check if a pod has an ini containers |

---

- Example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-demo
spec:
  containers:
    - name: web
      image: nginx
      ports:
        - containerPort: 8080
   initContainers:
    # 1st init con
    - name: 1st-init-con
      image: busybox
      command: ["echo", "this is the 1st init con"]
    # 2nd init con
    - name: st-init-con
      image: busybox
      command: ["echo", "this is the 2nd init con"]
```

> run init containers: db-checker -> api-checker

---

### Lab: Init Containers

```yaml
# demo-init-container.yaml
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
kubectl create -f demo-init-container.yaml
# pod/init-containers-demo created

kubectl get pod --watch
# NAME                   READY   STATUS    RESTARTS   AGE
# init-containers-demo   0/1     Pending   0          0s
# init-containers-demo   0/1     Pending   0          0s
# init-containers-demo   0/1     Init:0/2   0          0s
# init-containers-demo   0/1     Init:0/2   0          3s
# init-containers-demo   0/1     Init:1/2   0          13s
# init-containers-demo   0/1     Init:1/2   0          14s
# init-containers-demo   0/1     PodInitializing   0          27s
# init-containers-demo   1/1     Running           0          29s

kubectl get event -w
# 2m56s       Normal   Scheduled   pod/init-containers-demo       Successfully assigned default/init-containers-demo to docker-desktop
# 2m55s       Normal   Pulling     pod/init-containers-demo       Pulling image "busybox"
# 2m54s       Normal   Pulled      pod/init-containers-demo       Successfully pulled image "busybox" in 1.018s (1.018s including waiting). Image size: 2224358 bytes.
# 2m54s       Normal   Created     pod/init-containers-demo       Created container: 1st-check
# 2m54s       Normal   Started     pod/init-containers-demo       Started container 1st-check
# 2m43s       Normal   Pulling     pod/init-containers-demo       Pulling image "busybox"
# 2m43s       Normal   Pulled      pod/init-containers-demo       Successfully pulled image "busybox" in 779ms (779ms including waiting). Image size: 2224358 bytes.
# 2m42s       Normal   Created     pod/init-containers-demo       Created container: 2nd-check
# 2m42s       Normal   Started     pod/init-containers-demo       Started container 2nd-check
# 2m29s       Normal   Pulling     pod/init-containers-demo       Pulling image "nginx"
# 2m28s       Normal   Pulled      pod/init-containers-demo       Successfully pulled image "nginx" in 909ms (909ms including waiting). Image size: 59795293 bytes.
# 2m28s       Normal   Created     pod/init-containers-demo       Created container: main-app
# 2m28s       Normal   Started     pod/init-containers-demo       Started container main-app
# 49m         Normal   Killing     pod/multi-container-log-demo   Stopping container redis
# 49m         Normal   Killing     pod/multi-container-log-demo   Stopping container busybox
# 3m28s       Normal   Killing     pod/web-64c966cf88-9cnn9       Stopping container nginx
# 3m28s       Normal   Killing     pod/web-64c966cf88-x57zc       Stopping container nginx

kubectl logs init-containers-demo --all-containers
# 1st-check starts.
# 1st-check completed.
# 2nd-check starts.
# 2nd-check completed.
# /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
# /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
# 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
# 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
# /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
# /docker-entrypoint.sh: Configuration complete; ready for start up
# 2025/12/21 22:53:34 [notice] 1#1: using the "epoll" event method
# 2025/12/21 22:53:34 [notice] 1#1: nginx/1.29.4
# 2025/12/21 22:53:34 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19)
# 2025/12/21 22:53:34 [notice] 1#1: OS: Linux 5.15.153.1-microsoft-standard-WSL2
# 2025/12/21 22:53:34 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
# 2025/12/21 22:53:34 [notice] 1#1: start worker processes
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 29
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 30
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 31
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 32
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 33
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 34
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 35
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 36
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 37
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 38
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 39
# 2025/12/21 22:53:34 [notice] 1#1: start worker process 40
```

---

- Inspect init container log

```sh
kubectl logs init-containers-demo -c 1st-check
# 1st-check starts.
# 1st-check completed.

kubectl logs init-containers-demo -c 2nd-check
# 2nd-check starts.
# 2nd-check completed.
```

---
