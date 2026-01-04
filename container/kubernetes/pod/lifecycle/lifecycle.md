# Kubernetes: Pod - Lifecycle

[Back](../../index.md)

- [Kubernetes: Pod - Lifecycle](#kubernetes-pod---lifecycle)
  - [Pod Phase](#pod-phase)
  - [Pod Conditions](#pod-conditions)
    - [Lab: Pod Contidtions](#lab-pod-contidtions)
  - [Pod Lifecycle](#pod-lifecycle)
    - [Initialization stage](#initialization-stage)
      - [Pulling the container image](#pulling-the-container-image)
      - [Running the containers](#running-the-containers)
      - [Restarting failed init containers](#restarting-failed-init-containers)
    - [Run stage](#run-stage)
      - [`post-start hook` error impact a container](#post-start-hook-error-impact-a-container)
      - [Pulling the container image](#pulling-the-container-image-1)
      - [Running the container](#running-the-container)
      - [Terminating and restarting the container on failures](#terminating-and-restarting-the-container-on-failures)
      - [Termination Grace Period](#termination-grace-period)
    - [Termination stage](#termination-stage)
      - [Containers Termination](#containers-termination)
      - [Deletion Grace Period](#deletion-grace-period)
  - [Lab: Pod phase](#lab-pod-phase)
    - [Running a pod](#running-a-pod)
    - [Update a pod manifest file](#update-a-pod-manifest-file)
    - [edit](#edit)
    - [Deleting a pod](#deleting-a-pod)
  - [Lab: Pod state - ErrImagePull](#lab-pod-state---errimagepull)
  - [Lab: Pod state - One-off Complete](#lab-pod-state---one-off-complete)
  - [Lab: Pod state - one-off Failed](#lab-pod-state---one-off-failed)

---

## Pod Phase

| Pod Phase | Description                                                                         |
| --------- | ----------------------------------------------------------------------------------- |
| `Pending` | Since `object` is **accepted**, until one of the `container` is **running**         |
| `Running` | Since **At least one** of containers is **running**                                 |
| `Unknown` | The state of the Pod **cannot be determined**. `Kubelet` has **stopped reporting**. |

---

- `Finite Pod`: pod that is **not** intended to run **indefinitely**

| Pod Phase   | Description                                                       |
| ----------- | ----------------------------------------------------------------- |
| `Succeeded` | **All** `containers` **complete** successfully                    |
| `Failed`    | **At least one** of the `container` **terminates unsuccessfully** |

---

## Pod Conditions

- `Pod Condition`

  - a **detailed report** on whether a Pod has **passed a specific milestone** or "health check" in its lifecycle.

- `PodScheduled`: Whether the pod has been **scheduled to a node**.
- `Initialized`: Whether the `init containers` have **all completed**.
- `ContainersReady`: Whether **all containers** in the pod are ready.
- `Ready`: Whether the **readiness gates** are all reporting that **all containers are ready**.

| Condition Type              | Description                                                                            |
| --------------------------- | -------------------------------------------------------------------------------------- |
| `PodScheduledHas`           | Whether the Pod been **assigned to a node** by the `Scheduler`                         |
| `Initialized`               | Whether all `Init Containers` have **finished successfully**                           |
| `ContainersReady`           | Whether **all** `containers` are in the Pod **currently ready**                        |
| `Ready`                     | Whether the Pod's `Readiness Probes` are passed                                        |
| `PodReadyToStartContainers` | Whether the sandbox and network are **set up** so the Kubelet can start pulling images |

---

### Lab: Pod Contidtions

```sh
kubectl run web --image=nginx
# pod/web created

kubectl describe pod web
# Conditions:
#   Type                        Status
#   PodScheduled                True
#   Initialized                 True
#   ContainersReady             True
#   Ready                       True
#   PodReadyToStartContainers   True

kubectl get pod web -o yaml
# status:
#   conditions:
#     - type: PodScheduled
#       status: "True"
#       observedGeneration: 1
#       lastTransitionTime: "2026-01-02T19:26:06Z"
#       lastProbeTime: null
#     - type: Initialized
#       status: "True"
#       observedGeneration: 1
#       lastTransitionTime: "2026-01-02T19:26:06Z"
#       lastProbeTime: null
#     - type: PodReadyToStartContainers
#       status: "True"
#       observedGeneration: 1
#       lastTransitionTime: "2026-01-03T17:28:37Z"
#       lastProbeTime: null
#     - type: ContainersReady
#       status: "True"
#       observedGeneration: 1
#       lastTransitionTime: "2026-01-03T17:28:37Z"
#       lastProbeTime: null
#     - type: Ready
#       status: "True"
#       observedGeneration: 1
#       lastTransitionTime: "2026-01-03T17:28:37Z"
#       lastProbeTime: null
```

---

## Pod Lifecycle

- `initialization stage`
  - when the pod’s `init containers` run
- `run stage`
  - when the `regular containers` of the pod run
- `termination stage`
  - when the pod’s containers are **terminated**

---

### Initialization stage

- the stage when `init containers` run

![pic](./pic/init_stage.png)

#### Pulling the container image

- Before each `init container` is started, its container image is pulled to the `worker node`

- `containers.imagePullPolicy` field
  - determines whether the image is pulled every time, only the first time, or never.
  - value:
    - `Always`:
      - pulled image every time the container is (re)started.
      - the registry still needs to be contacted
        - container will not run if registry unavailable, even the image stored locally.
    - `Never`:
      - never pulled from the registry
      - image must exist on the worker node beforehand, can be
        - stored locally
        - built on the node
      - if not available locally, raise `ErrImageNeverPull` event
    - `IfNotPresent`
      - pulled if it is **not already** present on the node
      - image is only **pulled the first time** it’s required.
    - if not specified
      - image tag == `:latest`: defaults to `Always`
      - Otherwise, default to `IfNotPresent`

---

#### Running the containers

- repeated process of `init containers`

  - image pull
  - container start
  - next image pull
  - next container start
  - ...
  - untill all init containers completed.

- All `init containers` must run to **completion** before the `regular containers` can **start**

---

#### Restarting failed init containers

- When an `init container` terminates with an **error**
  - if pod’s `restart policy` == `Always`/`OnFailure`
    - failed `init container` is **restarted**
  - if pod’s `restart policy` == `Never`
    - **subsequent** `init containers` and the pod’s `regular containers` are never started
    - status: `Init:Error`
    - fix:
      - delete and recreate the pod object

---

### Run stage

- the stage when init containers are completed and regular containers create.

![pic](./pic/running_stage.png)

---

#### `post-start hook` error impact a container

- **Sequential Start, Parallel Execution**
  - `Regular containers` are **created synchronously** in the **order** they are **defined in the pod’s spec**.
  - All `regular containers` execute **parallelly**.
    - **No Blocking**: it **does not wait** for one container to be "ready" or "successful" before starting the next.
- `post-start hook` runs **asynchronously** with the `Regular container` process
  - execution execution of the `post-start hook handler` **blocks** the creation and start of the **its container**.
  - `container` might **restart** based on the `restart policy`
  - No Impact on Others

---

- **termination** of `containers` is performed in **parallel**.
- `pre-stop hooks` of the containers are all **invoked at the same time**
  - `pre-stop hook` **blocks** the shutdown of the container in which it is defined
  - does not **block** the **shutdown** of **other** containers

---

#### Pulling the container image

- image is **pulled** from the image **registry**, following the pod’s `imagePullPolicy`.

  - Once the image is **pulled**, the `container` is **created**.

- Even if **a** container image **can’t be pulled**, the **other** containers in the pod are **started** nevertheless.
  - **risk**:
    - it could raise dependency issue across containers if the dependent container take time pulling image before start.

---

#### Running the container

- The container **starts** when the `main container process` **starts**.
- `post-start hook` runs **asynchronously**
- `startup probe` started
  - followed by `liveness probe` is started

---

#### Terminating and restarting the container on failures

- container is terminated if:

  - `startup probe` fails
  - `liveness probe` fails
  - `post-start hook` fails

- Container restarts based on the `restartPolicy`
  - if `restartPolicy` == `Never`, container remain in the `Terminated` state
  - note:
    - `startup hook` fails + `restartPolicy` == `Never`: pod status == `Completed`

---

#### Termination Grace Period

- `termination grace period`:
  - the amount of time to terminate a container
- `pod.spec.terminationGracePeriodSeconds` field
  - default: 30s
  - timer starts when
    - `pre-stop hook` is called
    - the `TERM` signal is sent if no hook is defined
  - If the `process` is **still running** after the `termination grace period` has **expired**, it’s terminated by force via the `KILL` signal.
    - This terminates the container.

---

### Termination stage

- the `stage` when the pod object is **deleted**.
  - pod status is changed to `Terminating`.

---

#### Containers Termination

- the pod’s `containers` are **terminated** in **parallel**

  - if `pre-stop hook` is not called
    - `TERM signals` are sent to `container`
  - if `pre-stop hook` is called,

    - executes pre-stop hook
    - then `TERM signals` are sent to `container`
    - terminate process by `KILL` signal if the `deletion grace period` **expires**

- After **all** the `containers` in the `pod` have **stopped** running, the `pod` object is **deleted**.

---

#### Deletion Grace Period

- the **amount of time** for the `containers` to **shut down** on their own.
- field `metadata.deletionGracePeriodSeconds`

  - By default, it gets its value from the `spec.terminationGracePeriodSeconds` field
    - `30s`

- it is advisable to extend it if the application usually **needs more time to shut down gracefully**.

- Example: manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kiada-ssl-shortgraceperiod
spec:
  terminationGracePeriodSeconds: 50
  containers:
```

- Imperative Command

```sh
# give the pod 10s to shut down
kubectl delete po kiada-ssl --grace-period 10

# check the log for TERM signal
kubectl logs POD_NAME -c CONTAINER_NAME -f
```

---

## Lab: Pod phase

### Running a pod

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

### Update a pod manifest file

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

### edit

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

### Deleting a pod

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

## Lab: Pod state - ErrImagePull

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

## Lab: Pod state - One-off Complete

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

## Lab: Pod state - one-off Failed

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
