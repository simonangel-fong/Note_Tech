# Kubernetes: Container - Init Container

[Back](../../index.md)

- [Kubernetes: Container - Init Container](#kubernetes-container---init-container)
  - [Init Container](#init-container)
    - [Idempotent](#idempotent)
    - [Common Commands:](#common-commands)
    - [Lab: Init Containers](#lab-init-containers)

---

## Init Container

- `init containers`/`regular init containers`

  - containers that only run **during Pod startup**.
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

### Idempotent

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
# demo-container-init.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-container-init
spec:
  initContainers:
    - name: 1st-init
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "$(date) 1st-init starts."
          sleep 10
          echo "$(date) 1st-init completed."
    - name: 2nd-init
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "$(date) 2nd-init starts."
          sleep 10
          echo "$(date) 2nd-init completed."
  containers:
    - name: main
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "$(date) main starts."
          while true; do
            echo "$(date) main running";
            sleep 1;
          done
```

```sh
kubectl create -f demo-container-init.yaml
# pod/demo-container-init created

kubectl get pod -w
# NAME                  READY   STATUS            RESTARTS   AGE
# demo-container-init   0/1     Pending           0          0s
# demo-container-init   0/1     Pending           0          0s
# demo-container-init   0/1     Init:0/2          0          0s
# demo-container-init   0/1     Init:0/2          0          3s
# demo-container-init   0/1     Init:1/2          0          12s
# demo-container-init   0/1     Init:1/2          0          15s
# demo-container-init   0/1     PodInitializing   0          24s
# demo-container-init   1/1     Running           0          26s

# confirm: 1st init -> 2nd init -> main
kubectl logs demo-container-init --all-containers
# Sun Jan  4 02:16:51 UTC 2026 1st-init starts.
# Sun Jan  4 02:17:01 UTC 2026 1st-init completed.
# Sun Jan  4 02:17:02 UTC 2026 2nd-init starts.
# Sun Jan  4 02:17:12 UTC 2026 2nd-init completed.
# Sun Jan  4 02:17:14 UTC 2026 main starts.
# Sun Jan  4 02:17:14 UTC 2026 main running
# Sun Jan  4 02:17:15 UTC 2026 main running
```

---

- Inspect init container log

```sh
kubectl logs demo-container-init -c 1st-init
# Sun Jan  4 02:16:51 UTC 2026 1st-init starts.
# Sun Jan  4 02:17:01 UTC 2026 1st-init completed.

kubectl logs demo-container-init -c 2nd-init
# Sun Jan  4 02:17:02 UTC 2026 2nd-init starts.
# Sun Jan  4 02:17:12 UTC 2026 2nd-init completed.
```

---
