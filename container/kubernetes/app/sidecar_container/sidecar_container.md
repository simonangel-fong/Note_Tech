# Kubernetes - Pod: Multiple Container - Sidecar Container

[Back](../../index.md)

- [Kubernetes - Pod: Multiple Container - Sidecar Container](#kubernetes---pod-multiple-container---sidecar-container)
  - [Sidecar container](#sidecar-container)
  - [Init Container vs Sidecar Container](#init-container-vs-sidecar-container)
    - [Lab: Sidecar Container](#lab-sidecar-container)

---

## Sidecar container

- `sidecar containers`

  - a special case of `init containers`.(From offical doc)
  - the **secondary** containers that **run along with** the **main application container** within the **same** `Pod`.
  - used to **enhance or to extend the functionality** of the primary app container by providing additional services, or functionality such as **logging, monitoring, security, or data synchronization**, **without directly altering the primary application code**.

- Common use case:

  - **ElasticSearch DB** starts and continuously running
  - Kibana, the main application to display a dashboard, starts after

- specify a `restartPolicy` for containers listed in a Pod's `initContainers` field.

  - make container **independent** from other `init containers` and from the **main application container**(s) within the same pod.
  - can be started, stopped, or restarted **without affecting** the **main application container** and other `init containers`.
  - start and **remain running** **during the entire life** of the `Pod`.

- **Changing the image** of a `sidecar container` will **not** cause the `Pod` to **restart**, but will trigger a **container restart**.

- `sidecar containers` **support** `probes` to control their lifecycle.

---

- Manifest File

```yaml
spec:
  initContainers:
    restartPolicy: Always # ensures containers are continuously running
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

### Lab: Sidecar Container

```yaml
# demo-pod-sidecar.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod-sidecar
spec:
  containers:
    - name: main
      image: nginx
  initContainers:
    - name: sidecar # sidecar
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "Sidecar starts.";
          while true; do
           echo "Sidecar running";
           sleep 1;
          done
      restartPolicy: Always # side car
    - name: init # init container
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "init container starts.";
          sleep 10;
          echo "init container completed";
```

```sh
kubectl create -f demo-pod-sidecar.yaml
# pod/demo-pod-sidecar created

# confirm:
#  init: 2
#  ready: 2
kubectl get pod -w
# NAME               READY   STATUS               RESTARTS   AGE
# demo-pod-sidecar   0/2     Pending              0          0s
# demo-pod-sidecar   0/2     Pending              0          0s
# demo-pod-sidecar   0/2     Init:0/2             0          0s
# demo-pod-sidecar   1/2     Init:1/2             0          2s
# demo-pod-sidecar   1/2     Init:1/2             0          4s
# demo-pod-sidecar   1/2     PodInitializing      0          15s
# demo-pod-sidecar   2/2     Running              0          17s

# confirm sidecar is running
kubectl describe pod demo-pod-sidecar
# Init Containers:
#   sidecar:
#     State:          Running
#     Ready:          True
#   init:
#     State:          Terminated
#       Reason:       Completed
#       Exit Code:    0
#       Started:      Sat, 03 Jan 2026 20:43:57 -0500
#       Finished:     Sat, 03 Jan 2026 20:44:07 -0500
#     Ready:          True
# Containers:
#   main:
#     State:          Running
#       Started:      Sat, 03 Jan 2026 20:44:10 -0500
#     Ready:          True
# Events:
#   Type    Reason     Age   From               Message
#   ----    ------     ----  ----               -------
#   Normal  Scheduled  94s   default-scheduler  Successfully assigned default/demo-pod-sidecar to docker-desktop      
#   Normal  Pulling    94s   kubelet            Pulling image "busybox"
#   Normal  Pulled     93s   kubelet            Successfully pulled image "busybox" in 1.155s (1.155s including waiting). Image size: 2224358 bytes.
#   Normal  Created    93s   kubelet            Created container: sidecar
#   Normal  Started    93s   kubelet            Started container sidecar
#   Normal  Pulling    93s   kubelet            Pulling image "busybox"
#   Normal  Pulled     92s   kubelet            Successfully pulled image "busybox" in 734ms (734ms including waiting). Image size: 2224358 bytes.
#   Normal  Created    92s   kubelet            Created container: init
#   Normal  Started    92s   kubelet            Started container init
#   Normal  Pulling    80s   kubelet            Pulling image "nginx"
#   Normal  Pulled     80s   kubelet            Successfully pulled image "nginx" in 863ms (863ms including waiting). Image size: 59797235 bytes.
#   Normal  Created    79s   kubelet            Created container: main
#   Normal  Started    79s   kubelet            Started container main
```

---
