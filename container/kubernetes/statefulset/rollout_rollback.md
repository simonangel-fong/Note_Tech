# Kubernetes: StatefulSet - Rollout & Rollback

[Back](../index.md)

- [Kubernetes: StatefulSet - Rollout \& Rollback](#kubernetes-statefulset---rollout--rollback)
  - [Imperative Command](#imperative-command)
  - [Updating Strategy](#updating-strategy)
    - [Unready pod](#unready-pod)
  - [Updating Strategy - RollingUpdate](#updating-strategy---rollingupdate)
    - [Lab: StatefulSet RollingUpdate Strategy](#lab-statefulset-rollingupdate-strategy)
    - [RollingUpdate with partition: Implement Canary Deployment](#rollingupdate-with-partition-implement-canary-deployment)
    - [Lab: Implement Canary Deployment with Partition](#lab-implement-canary-deployment-with-partition)
  - [Updating Strategy - OnDelete strategy](#updating-strategy---ondelete-strategy)
    - [Lab: OnDelete strategy](#lab-ondelete-strategy)
  - [Rollback](#rollback)
  - [Rollout History: `ControllerRevision` Object](#rollout-history-controllerrevision-object)

---

## Imperative Command

- Update

| Command                                               | Description                                              |
| ----------------------------------------------------- | -------------------------------------------------------- |
| `kubectl rollout history sts NAME`                    | View the rollout history of changes to the StatefulSets. |
| `kubectl get controllerrevisions`                     | Show revision objects                                    |
| `kubectl rollout undo sts NAME`                       | Rollback to the previous version                         |
| `kubectl rollout undo sts NAME --to-revision VERSION` | Rollback to a specific version                           |

---

## Updating Strategy

- `updateStrategy` field
  - `RollingUpdate`
    - default
    - `Pods` are **replaced one by one**
      - pod with highest ordinal number is deleted and replaced first
      - when the new pod is ready
      - pod with the next highest ordinal number is replaced.
  - `OnDelete`
    - **waits** for each Pod to be **manually deleted**.
      - When the old Pod gets manually deleted, the controller replaces it with a new Pod
      - the replacement of the pod can in any order.

---

### Unready pod

- If a new `Pod` **fails to become ready** during the update, the update is also **paused**.
  - The rollout will **resume** when the `Pod` is **ready again**.
- So, if you deploy a **faulty version** whose readiness probe **never succeeds**, the update will be **blocked** after the first Pod is replaced.
- If the number of replicas in the `StatefulSet` is **sufficient**, the service provided by the Pods in the `StatefulSet` is **unaffected**.

---

## Updating Strategy - RollingUpdate

- only **one** `Pod` is **replaced** at a time.

- with `minReadySeconds` field:
  - **causes** the `controller` to **wait a certain amount of time** after the new Pods are ready **before replacing** the other Pods.

---

### Lab: StatefulSet RollingUpdate Strategy

```yaml
# demo-mongodb-rollingupdate.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: demo-mongodb-rollingupdate
spec:
  serviceName: mongodb-svc # headless svc
  replicas: 3
  minReadySeconds: 30 # wait for 30s for readiness
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
        - name: mongodb
          image: mongo:8
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: data
              mountPath: /data/db
  volumeClaimTemplates: # a unique PVC for each pod
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

```sh
kubectl apply -f demo-mongodb-rollingupdate.yaml
# statefulset.apps/demo-mongodb-rollingupdate created

# confirm
kubectl get sts -o wide
# NAME                         READY   AGE     CONTAINERS   IMAGES
# demo-mongodb-rollingupdate   3/3     4m14s   mongodb      mongo:8

kubectl set image sts demo-mongodb-rollingupdate mongodb=mongo:8.2.3
# statefulset.apps/demo-mongodb-rollingupdate image updated

# confirm:
#  sts update one by one
kubectl rollout status sts demo-mongodb-rollingupdate
# Waiting for 1 pods to be ready...
# Waiting for 1 pods to be ready...
# Waiting for 1 pods to be ready...
# Waiting for partitioned roll out to finish: 1 out of 3 new pods have been updated...
# Waiting for partitioned roll out to finish: 1 out of 3 new pods have been updated...
# Waiting for 1 pods to be ready...
# Waiting for 1 pods to be ready...
# Waiting for 1 pods to be ready...
# Waiting for partitioned roll out to finish: 2 out of 3 new pods have been updated...
# Waiting for partitioned roll out to finish: 2 out of 3 new pods have been updated...
# Waiting for 1 pods to be ready...
# Waiting for 1 pods to be ready...
# Waiting for 1 pods to be ready...
# partitioned roll out complete: 3 new pods have been updated...


# confirm:
#  sts update one by one
kubectl get sts -o wide -w
# NAME                         READY   AGE     CONTAINERS   IMAGES
# demo-mongodb-rollingupdate   3/3     3m50s   mongodb      mongo:8
# demo-mongodb-rollingupdate   3/3     4m37s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   3/3     4m37s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     4m38s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     4m38s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     4m38s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   3/3     4m39s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   3/3     5m10s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     5m10s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     5m11s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     5m11s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   3/3     5m13s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   3/3     6m14s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     6m15s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     6m15s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   2/3     6m15s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   3/3     6m18s   mongodb      mongo:8.2.3
# demo-mongodb-rollingupdate   3/3     7m18s   mongodb      mongo:8.2.3

# confirm:
#   sts update from highest
#   wait for ready
kubectl get pod -w
# NAME                           READY   STATUS              RESTARTS   AGE
# demo-mongodb-rollingupdate-0   1/1     Running             0          3m55s
# demo-mongodb-rollingupdate-1   1/1     Running             0          2m51s
# demo-mongodb-rollingupdate-2   1/1     Running             0          2m19s
# demo-mongodb-rollingupdate-2   1/1     Terminating         0          3m1s
# demo-mongodb-rollingupdate-2   1/1     Terminating         0          3m1s
# demo-mongodb-rollingupdate-2   0/1     Completed           0          3m2s
# demo-mongodb-rollingupdate-2   0/1     Completed           0          3m2s
# demo-mongodb-rollingupdate-2   0/1     Completed           0          3m2s
# demo-mongodb-rollingupdate-2   0/1     Pending             0          0s
# demo-mongodb-rollingupdate-2   0/1     Pending             0          0s
# demo-mongodb-rollingupdate-2   0/1     ContainerCreating   0          0s
# demo-mongodb-rollingupdate-2   1/1     Running             0          1s
# demo-mongodb-rollingupdate-1   1/1     Terminating         0          4m6s
# demo-mongodb-rollingupdate-1   1/1     Terminating         0          4m6s
# demo-mongodb-rollingupdate-1   0/1     Completed           0          4m6s
# demo-mongodb-rollingupdate-1   0/1     Completed           0          4m7s
# demo-mongodb-rollingupdate-1   0/1     Completed           0          4m7s
# demo-mongodb-rollingupdate-1   0/1     Completed           0          4m7s
# demo-mongodb-rollingupdate-1   0/1     Pending             0          0s
# demo-mongodb-rollingupdate-1   0/1     Pending             0          0s
# demo-mongodb-rollingupdate-1   0/1     ContainerCreating   0          0s
# demo-mongodb-rollingupdate-1   1/1     Running             0          2s
# demo-mongodb-rollingupdate-0   1/1     Terminating         0          6m14s
# demo-mongodb-rollingupdate-0   1/1     Terminating         0          6m14s
# demo-mongodb-rollingupdate-0   0/1     Completed           0          6m15s
# demo-mongodb-rollingupdate-0   0/1     Completed           0          6m15s
# demo-mongodb-rollingupdate-0   0/1     Completed           0          6m15s
# demo-mongodb-rollingupdate-0   0/1     Pending             0          0s
# demo-mongodb-rollingupdate-0   0/1     Pending             0          0s
# demo-mongodb-rollingupdate-0   0/1     ContainerCreating   0          0s
# demo-mongodb-rollingupdate-0   1/1     Running             0          3s

# confirm history
kubectl rollout history sts demo-mongodb-rollingupdate
# statefulset.apps/demo-mongodb-rollingupdate
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>

kubectl get controllerrevisions
# NAME                                    CONTROLLER                                    REVISION   AGE
# demo-mongodb-rollingupdate-77dbc6c455   statefulset.apps/demo-mongodb-rollingupdate   2          18m
# demo-mongodb-rollingupdate-86bc878446   statefulset.apps/demo-mongodb-rollingupdate   1          21m

# confirm the version image get updated
kubectl describe controllerrevisions demo-mongodb-rollingupdate-77dbc6c455
# Name:         demo-mongodb-rollingupdate-77dbc6c455
# Namespace:    default
# Labels:       app=mongodb
#               controller.kubernetes.io/hash=77dbc6c455
# Annotations:  <none>
# API Version:  apps/v1
# Data:
#   Spec:
#     Template:
#       $patch:  replace
#       Metadata:
#         Labels:
#           App:  mongodb
#       Spec:
#         Containers:
#           Image:              mongo:8.2.3
#           Image Pull Policy:  IfNotPresent
#           Name:               mongodb
#           Ports:
#             Container Port:  27017
#             Protocol:        TCP
#           Resources:
#           Termination Message Path:    /dev/termination-log
#           Termination Message Policy:  File
#           Volume Mounts:
#             Mount Path:  /data/db
#             Name:        data
#         Dns Policy:      ClusterFirst
#         Restart Policy:  Always
#         Scheduler Name:  default-scheduler
#         Security Context:
#         Termination Grace Period Seconds:  30
# Kind:                                      ControllerRevision
# Metadata:
#   Creation Timestamp:  2026-01-01T19:43:27Z
#   Owner References:
#     API Version:           apps/v1
#     Block Owner Deletion:  true
#     Controller:            true
#     Kind:                  StatefulSet
#     Name:                  demo-mongodb-rollingupdate
#     UID:                   b608d553-b8f9-476f-aa58-ade3a9716e96
#   Resource Version:        2953656
#   UID:                     feb160f5-94c5-4f6e-8f5c-22fe8e90889b
# Revision:                  2
# Events:                    <none>

```

---

### RollingUpdate with partition: Implement Canary Deployment

- `sts` does not support `kubectl rollout pause` command

- `spec.updateStrategy.rollingUpdate.partition` field
  - specifies the **ordinal number** at which the StatefulSet should be **partitioned**.
  - pods with an ordinal number lower than the partition value aren’t updated.

![pic](./pic/sts_update_partition.png)

- Use case:

  - If you set the `partition` value appropriately, you can implement a `Canary deployment`, control the **rollout manually**, or **stage an update** instead of triggering it immediately.

- Implement Canary
  - set `partition` = replica and apply, as a safe net to block any auto update
  - `kubectl patch sts` to scale down `parition` by 1;
    - sts controller automatically update the highest pod
    - then test this new pod
  - if test is passed, continue `kubectl patch sts` to scale down `parition` by 1
  - until `parition` = 0

---

### Lab: Implement Canary Deployment with Partition

```yaml
# demo-sts-update-partition.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: demo-sts-update-partition
spec:
  serviceName: mongodb-svc # headless svc
  replicas: 3
  minReadySeconds: 30 # wait for 30s for readiness
  updateStrategy:
    type: RollingUpdate # RollingUpdate strategy
    rollingUpdate:
      partition: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
        - name: mongodb
          image: mongo:8
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: data
              mountPath: /data/db
  volumeClaimTemplates: # a unique PVC for each pod
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

```sh
kubectl apply -f demo-sts-update-partition.yaml
# statefulset.apps/demo-sts-update-partition created

kubectl get sts demo-sts-update-partition
# NAME                        READY   AGE
# demo-sts-update-partition   3/3     76s
```

- Update image

```sh
kubectl set image sts demo-sts-update-partition mongodb=mongo:8.2.3

# confirm: no sts get updated
kubectl rollout status sts demo-sts-update-partition
# partitioned roll out complete: 0 new pods have been updated...
```

> No pod update due to partition = replicas

---

- Update partition to 2 and change image

```yaml
# demo-sts-update-partition-patch.yaml
spec:
  updateStrategy:
    rollingUpdate:
      partition: 2
```

```sh
# update partition number
kubectl patch sts demo-sts-update-partition --patch-file demo-sts-update-partition-patch.yaml
# statefulset.apps/demo-sts-update-partition patched

kubectl rollout status sts demo-sts-update-partition
# Waiting for 1 pods to be ready...
# partitioned roll out complete: 1 new pods have been updated...

# confirm
kubectl get sts -w
# NAME                        READY   AGE
# demo-sts-update-partition   3/3     2m33s
# demo-sts-update-partition   3/3     3m56s
# demo-sts-update-partition   3/3     3m56s
# demo-sts-update-partition   3/3     14m
# demo-sts-update-partition   3/3     14m
# demo-sts-update-partition   2/3     14m
# demo-sts-update-partition   2/3     14m
# demo-sts-update-partition   2/3     14m
# demo-sts-update-partition   3/3     14m

# confirm:
#  highest get updated
kubectl get pod -w
# NAME                          READY   STATUS              RESTARTS   AGE
# demo-sts-update-partition-0   1/1     Running             0          2m53s
# demo-sts-update-partition-1   1/1     Running             0          2m21s
# demo-sts-update-partition-2   1/1     Running             0          109s
# demo-sts-update-partition-2   1/1     Terminating         0          13m
# demo-sts-update-partition-2   1/1     Terminating         0          13m
# demo-sts-update-partition-2   0/1     Completed           0          13m
# demo-sts-update-partition-2   0/1     Completed           0          13m
# demo-sts-update-partition-2   0/1     Completed           0          13m
# demo-sts-update-partition-2   0/1     Pending             0          0s
# demo-sts-update-partition-2   0/1     Pending             0          0s
# demo-sts-update-partition-2   0/1     ContainerCreating   0          0s
# demo-sts-update-partition-2   1/1     Running             0          2s

# confirm from status
#  replica Revision
kubectl get sts demo-sts-update-partition -o yaml
# status:
#   availableReplicas: 3
#   currentReplicas: 2
#   currentRevision: demo-sts-update-partition-86bc878446
#   updateRevision: demo-sts-update-partition-77dbc6c455
#   updatedReplicas: 1
```

- Try to delete pod with partition update
  - if one of the **old Pods** get deleted, the replacement Pod will be created **with the previous template**.
  - If one of the **new pods** get deleted, it’ll be recreated with the new template.

```sh
# delete -0 with old version
kubectl delete pod demo-sts-update-partition-1
# pod "demo-sts-update-partition-1" deleted from default namespace

# confirm: replica and revision unchanged
kubectl get sts demo-sts-update-partition -o yaml
# status:
#   currentReplicas: 2
#   currentRevision: demo-sts-update-partition-86bc878446
#   updateRevision: demo-sts-update-partition-77dbc6c455
#   updatedReplicas: 1
```

---

- Completing a partitioned update

- Scale down partition to 0

```sh
# update demo-sts-update-partition-patch.yaml
# partition: 1
kubectl patch sts demo-sts-update-partition --patch-file demo-sts-update-partition-patch.yaml
# statefulset.apps/demo-sts-update-partition patched

# confirm updated=2
kubectl get sts demo-sts-update-partition -o yaml
# status:
#   currentReplicas: 1
#   currentRevision: demo-sts-update-partition-86bc878446
#   updateRevision: demo-sts-update-partition-77dbc6c455
#   updatedReplicas: 2

# update demo-sts-update-partition-patch.yaml
# partition: 0
kubectl patch sts demo-sts-update-partition --patch-file demo-sts-update-partition-patch.yaml
# statefulset.apps/demo-sts-update-partition patched

# confirm currentReplicas=updatedReplicas=3
kubectl get sts demo-sts-update-partition -o yaml
# status:
#   currentReplicas: 3
#   currentRevision: demo-sts-update-partition-77dbc6c455
#   updateRevision: demo-sts-update-partition-77dbc6c455
#   updatedReplicas: 3
```

---

## Updating Strategy - OnDelete strategy

- Pod’s `readiness` status is **irrelevant**
  - because the rollout is controlled manually

---

### Lab: OnDelete strategy

```yaml
# demo-sts-update-ondelete.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: demo-sts-update-ondelete
spec:
  serviceName: mongodb-svc # headless svc
  replicas: 3
  minReadySeconds: 30 # wait for 30s for readiness
  updateStrategy:
    type: OnDelete # OnDelete strategy
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
        - name: mongodb
          image: mongo:8
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: data
              mountPath: /data/db
  volumeClaimTemplates: # a unique PVC for each pod
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

```sh
kubectl apply -f demo-sts-update-ondelete.yaml
# statefulset.apps/demo-sts-update-ondelete created

kubectl get sts -o wide
# NAME                       READY   AGE     CONTAINERS   IMAGES
# demo-sts-update-ondelete   3/3     3m10s   mongodb      mongo:8

# update image
kubectl set image sts demo-sts-update-ondelete mongodb=mongo:8.2.3
# statefulset.apps/demo-sts-update-ondelete image updated
```

> Sts controller do nothing due to the `onDelete` strategy

---

- Manually delete pod
  - not necessary to have to delete the Pod with the highest ordinal number first.

```sh
kubectl delete pod demo-sts-update-ondelete-1
# pod "demo-sts-update-ondelete-1" deleted from default namespace

# confirm: controller create new pod
kubectl get pod -w
# NAME                         READY   STATUS             RESTARTS   AGE
# demo-sts-update-ondelete-0   1/1     Running            0          89s
# demo-sts-update-ondelete-1   1/1     Running            0          57s
# demo-sts-update-ondelete-2   1/1     Running            0          25s
# demo-sts-update-ondelete-1   1/1     Terminating        0          18m
# demo-sts-update-ondelete-1   1/1     Terminating        0          18m
# demo-sts-update-ondelete-1   0/1     Completed          0          18m
# demo-sts-update-ondelete-1   0/1     Completed          0          18m
# demo-sts-update-ondelete-1   0/1     Completed          0          18m
# demo-sts-update-ondelete-1   0/1     Pending            0          0s
# demo-sts-update-ondelete-1   0/1     Pending            0          0s
# demo-sts-update-ondelete-1   0/1     ContainerCreating  0          0s
# demo-sts-update-ondelete-1   1/1     Running            0          1s

# delet next pod
kubectl delete pod demo-sts-update-ondelete-2
# pod "demo-sts-update-ondelete-2" deleted from default namespace

# confirm: controller create new pod
kubectl get pod -w
# NAME                         READY   STATUS               RESTARTS   AGE
# demo-sts-update-ondelete-0   1/1     Running              0          22m
# demo-sts-update-ondelete-1   1/1     Running              0          2m46s
# demo-sts-update-ondelete-2   1/1     Running              0          20m
# demo-sts-update-ondelete-2   1/1     Terminating          0          21m
# demo-sts-update-ondelete-2   1/1     Terminating          0          21m
# demo-sts-update-ondelete-2   0/1     Completed            0          21m
# demo-sts-update-ondelete-2   0/1     Completed            0          21m
# demo-sts-update-ondelete-2   0/1     Completed            0          21m
# demo-sts-update-ondelete-2   0/1     Pending              0          0s
# demo-sts-update-ondelete-2   0/1     Pending              0          0s
# demo-sts-update-ondelete-2   0/1     ContainerCreating    0          0s
# demo-sts-update-ondelete-2   1/1     Running              0          1s


# delet next pod
kubectl delete pod demo-sts-update-ondelete-0
# pod "demo-sts-update-ondelete-0" deleted from default namespace

# confirm: controller create new pod
kubectl get pod -w
# NAME                         READY   STATUS               RESTARTS   AGE
# demo-sts-update-ondelete-0   1/1     Running              0          24m
# demo-sts-update-ondelete-1   1/1     Running              0          4m55s
# demo-sts-update-ondelete-2   1/1     Running              0          95s
# demo-sts-update-ondelete-0   1/1     Terminating          0          24m
# demo-sts-update-ondelete-0   1/1     Terminating          0          24m
# demo-sts-update-ondelete-0   0/1     Completed            0          24m
# demo-sts-update-ondelete-0   0/1     Completed            0          24m
# demo-sts-update-ondelete-0   0/1     Completed            0          24m
# demo-sts-update-ondelete-0   0/1     Pending              0          0s
# demo-sts-update-ondelete-0   0/1     Pending              0          0s
# demo-sts-update-ondelete-0   0/1     ContainerCreating    0          0s
# demo-sts-update-ondelete-0   1/1     Running              0          1s

# confirm all replicas get updated
kubectl get sts demo-sts-update-ondelete -o yaml
# status:
#   replicas: 3
#   updateRevision: demo-sts-update-ondelete-77dbc6c455
#   updatedReplicas: 3

```

- Rolling Back

```sh
# before
kubectl get sts -o wide
# NAME                       READY   AGE   CONTAINERS   IMAGES
# demo-sts-update-ondelete   3/3     26m   mongodb      mongo:8.2.3

kubectl rollout undo sts demo-sts-update-ondelete
# statefulset.apps/demo-sts-update-ondelete rolled back

kubectl get sts -o wide
# NAME                       READY   AGE   CONTAINERS   IMAGES
# demo-sts-update-ondelete   3/3     28m   mongodb      mongo:8
```

---

## Rollback

- use cases:

  - When updating the `StatefulSet` and the rollout **hangs**
  - When the rollout was successful, but want to **revert to the previous revision**

- If the strategy is `RollingUpdate`, the Pods are **reverted one at a time.**

---

```sh
kubectl rollout undo sts demo-sts-update-partition
# statefulset.apps/demo-sts-update-partition rolled back

# confirm: image = 8.0
kubectl get sts -o wide
# NAME                        READY   AGE   CONTAINERS   IMAGES
# demo-sts-update-partition   3/3     55m   mongodb      mongo:8
```

---

## Rollout History: `ControllerRevision` Object

- `ControllerRevision` objects

  - the object stores the revision history of `StatefulSets` and `DaemonSets`
  - a generic object that represents an **immutable snapshot** of the **state of an object** at a particular point in time.

- vs history of deployment
  - `deployment`: using rs
  - `StatefulSets`: using `ControllerRevision`

---
