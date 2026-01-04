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
