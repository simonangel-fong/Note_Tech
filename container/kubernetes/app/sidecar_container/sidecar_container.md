# Kubernetes - Pod: Multiple Container - Sidecar Container

[Back](../../index.md)

- [Kubernetes - Pod: Multiple Container - Sidecar Container](#kubernetes---pod-multiple-container---sidecar-container)
  - [Sidecar container](#sidecar-container)
    - [Muli-container Pod vs Multiple pod](#muli-container-pod-vs-multiple-pod)
  - [K8s: Sidecar containers](#k8s-sidecar-containers)
    - [Lab: Sidecar Container](#lab-sidecar-container)
  - [Init Container vs Sidecar Container](#init-container-vs-sidecar-container)

---

## Sidecar container

- Multi-container pod is only appropriate if the application consists of a `primary process` and one or more processes that **complement** the operation of the primary process.

- `sidecar container`
  - container in which the complementary process runs
  - a pod can have **more than one** `sidecar`
  - e.g.,
    - container_web(primary process) host website directory;container_download(complementary process) periodically download updated file; both containers mount on the same volume to share files.
    - Container_backend(primary process) process request; container_log(complementary process) record log

---

### Muli-container Pod vs Multiple pod

- Multi-container pod is required when:
  - Do these containers have to run on the **same host**?
  - Do I want to **manage** them as a **single unit**?
  - Do they form a **unified whole** instead of being independent components?
  - Do they have to be **scaled** together?
  - Can a single node meet their combined **resource** needs?

---

## K8s: Sidecar containers

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
