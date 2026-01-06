# Kubernetes: Deployment - Rollout & Rollback

[Back](../../index.md)

- [Kubernetes: Deployment - Rollout \& Rollback](#kubernetes-deployment---rollout--rollback)
  - [Imperative Command](#imperative-command)
  - [Deployment Strategies](#deployment-strategies)
    - [`Recreate`](#recreate)
      - [Lab: `Recreate` Strategy](#lab-recreate-strategy)
    - [`Rolling Update`](#rolling-update)
      - [Parameters](#parameters)
      - [Lab: `RollingUdate` Strategy](#lab-rollingudate-strategy)
  - [Control Rollout Process](#control-rollout-process)
    - [Pausing and Resuming the Rollout Process](#pausing-and-resuming-the-rollout-process)
  - [Preventing a Faulty Version](#preventing-a-faulty-version)
    - [With `Recreate` Strategy](#with-recreate-strategy)
      - [Lab: Recreate with `minReadySeconds`](#lab-recreate-with-minreadyseconds)
    - [With RollingOut Strategy](#with-rollingout-strategy)
      - [Lab: RollingOut with `minReadySeconds`](#lab-rollingout-with-minreadyseconds)
      - [Lab: RollingOut with `minReadySeconds` if a faulty version](#lab-rollingout-with-minreadyseconds-if-a-faulty-version)
  - [Rollout History](#rollout-history)
  - [Rollout Restart](#rollout-restart)
  - [Rollback](#rollback)
    - [Rolling Back vs Apply Old Manifest](#rolling-back-vs-apply-old-manifest)

---

## Imperative Command

- Rollout

| Command                                                    | Description                          |
| ---------------------------------------------------------- | ------------------------------------ |
| `kubectl rollout status deploy NAME`                       | Show the status of the rollout       |
| `kubectl rollout history deploy NAME`                      | View rollout history                 |
| `kubectl rollout restart deploy NAME --selector=app=nginx` | Restart a resource with label        |
| `kubectl rollout resume deploy NAME`                       | Resume a paused resource             |
| `kubectl rollout pause deploy NAME`                        | Mark the provided resource as paused |
| `kubectl rollout undo deploy NAME`                         | Rollback to the previous version     |

---

## Deployment Strategies

- `Deployment strategies`

  - help in defining **how** the **new** `ReplicaSet` should **replace** the **existing** `ReplicaSet`.

---

### `Recreate`

- **kill all the existing RC** and then **bring up the new ones**.
- This results in **quick deployment** however it will result in **downtime** when the old pods are down and the new pods have not come up.

- what happens underneath?

  - when the `pod template` update
    1. `Deployment controller` **update** the desired replica to 0
    2. `ReplicaSet Controller` **updates** the **old** `ReplicaSet`'s replica to 0
    3. `ReplicaSet Controller` **removes** old `Pod`
    4. `Deployment controller` creates a new `ReplicaSet` with new hash
    5. `ReplicaSet Controller` create `pod`

- the downtime occurts between the old and new `rs`

---

#### Lab: `Recreate` Strategy

```yaml
# demo-strategy-recreate.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-strategy-recreate
spec:
  replicas: 4
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: demo-recreate
  template:
    metadata:
      labels:
        app: demo-recreate
    spec:
      containers:
        - image: web
          name: nginx
```

- apply

```sh
kubectl apply -f demo-strategy-recreate.yaml
# deployment.apps/demo-strategy-recreate created

kubectl get deploy
# NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
# demo-strategy-recreate   3/3     3            3           3m20s
```

- update replica and apply
  - pod won't update because the template stay the same

```sh
kubectl apply -f demo-strategy-recreate.yaml
# deployment.apps/demo-strategy-recreate configured

kubectl get deploy
# NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
# demo-strategy-recreate   4/4     4            4           5m30s

# confirm: check history
kubectl rollout history deployment/demo-strategy-recreate
# deployment.apps/demo-strategy-recreate
# REVISION  CHANGE-CAUSE
# 1         <none>
```

---

- Update image
  - image httpd

```sh
kubectl set image deploy demo-strategy-recreate web=httpd
# deployment.apps/demo-strategy-recreate image updated

# confirm: get update
kubectl rollout history deployment/demo-strategy-recreate
# deployment.apps/demo-strategy-recreate
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>

# confirm:
#   Ready = 0 for a short time
kubectl get deploy -w
# NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
# demo-strategy-recreate   4/4     4            4           79s
# demo-strategy-recreate   4/4     4            4           94s
# demo-strategy-recreate   4/4     0            4           94s
# demo-strategy-recreate   0/4     0            0           94s
# demo-strategy-recreate   0/4     0            0           97s
# demo-strategy-recreate   0/4     0            0           97s
# demo-strategy-recreate   0/4     4            0           97s
# demo-strategy-recreate   1/4     4            1           102s
# demo-strategy-recreate   2/4     4            2           104s
# demo-strategy-recreate   3/4     4            3           106s
# demo-strategy-recreate   4/4     4            4           106s

# confirm
kubectl rollout status
```

- Update both image and labels

```sh
# linux
kubectl patch deploy demo-strategy-recreate --patch '
{
  "spec": {
    "template": {
      "metadata": {
        "labels": {
          "demo": "true"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "web",
            "image": "traefik"
          }
        ]
      }
    }
  }
}'

# windows
kubectl patch deploy demo-strategy-recreate --patch "{\"spec\": {\"template\": {\"metadata\":{\"labels\":{\"demo\":\"true\"}}, \"spec\": {\"containers\": [{\"name\": \"web\", \"image\": \"traefik\"}]}}}}"
# deployment.apps/demo-strategy-recreate patched

# confirm: downtime exist
kubectl get deploy -o wide -w
# NAME                     READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
# demo-strategy-recreate   4/4     4            4           15m   web          httpd    app=demo-recreate
# demo-strategy-recreate   4/4     4            4           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   4/4     0            4           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   0/4     0            0           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   0/4     0            0           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   0/4     0            0           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   0/4     4            0           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   1/4     4            1           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   2/4     4            2           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   3/4     4            3           19m   web          traefik   app=demo-recreate
# demo-strategy-recreate   4/4     4            4           19m   web          traefik   app=demo-recreate

# confirm: update
kubectl rollout history deployment/demo-strategy-recreate
# deployment.apps/demo-strategy-recreate
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>
# 3         <none>

# confirm the underlying rs
kubectl get rs
# NAME                                DESIRED   CURRENT   READY   AGE
# demo-strategy-recreate-68cd744854   4         4         4       4m52s
# demo-strategy-recreate-6f979ddc4f   0         0         0       24m
# demo-strategy-recreate-764d5b8785   0         0         0       22m
```

---

### `Rolling Update`

- **default**
- **gradually brings down** the **old** `RS` and **brings up** the new one.
- This results in **slow deployment**, however there is no deployment.
- At all times, few **old** pods and few **new** pods are **available** in this process.

- the Pods are **replaced gradually**, by simultaneously

  - **scaling down** the `old ReplicaSet`
  - **scaling up** the `new ReplicaSet`

- what happens underneath?

  - when the `pod template` update
    1. `Deployment Controller` **creates** a **new** `ReplicaSet` with **new hash**
    2. `Deployment Controller` **scale down** the **old** `ReplicaSet` and **scale up** the **new** `ReplicaSet` gradually, while keeping the total pod number close to the **desired number**.
    3. `ReplicaSet Controller` creates `Pod` in **new** `ReplicaSet` and **removes** `Pod` in **old** `ReplicaSet`
    4. Repeat process
    5. Until **old** `ReplicaSet` **scale down to 0** and **new** `ReplicaSet` **scale up to desired number**.

---

#### Parameters

- `spec.strategy.rollingUpdate.maxSurge`:
  - The **maximum number** of `Pods` **above** the **desired number** of replicas that the `Deployment` can have **during the rolling update**.
  - can be
    - an absolute number
    - a percentage of the desired number
  - default: `25%`

---

- `spec.strategy.rollingUpdate.maxUnavailable`:
  - The **maximum number** of `Pods` relative to the **desired replica** count that can be **unavailable** during the rolling update.
  - can be
    - an absolute number
    - a percentage of the desired number
  - 25%

---

- example:
  - `MaxSurge=0; maxUnavailable=0`:
    - unavailable
    - no pod be replace at any time
  - `replicas=3; MaxSurge=0; maxUnavailable=1`:
    - total pod always = 3+0 = 3
    - avaible always = 3-1 = 2
    - scale down the `old rs` first, then scale up the `new rs`
  - `replicas=3; MaxSurge=1; maxUnavailable=0`:
    - total pod always = 3+1 = 4
    - avaible always = 3-0 = 3
    - scale up the `new rs` first, then scale down the `old rs`
  - `replicas=3; maxSurge=1, maxUnavailable=1`:
    - total pod always = 3+1 = 4
    - avaible always = 3-1 = 2
    - scale down the `old rs` and scale up the `new rs`; when one new pod available, one old pod get removed.
  - `replicas=10; maxSurge=25%, maxUnavailable=25%`:
    - total pod = 10 \* 125% ~= 13
    - available pod = 10 \* 75% ~= 8
  - higher values of `maxSurge` and `maxUnavailable`
    - higher `maxSurge`: more new pod created in the new `rs`
    - higher `maxUnavailable`: more old pod get removed in the old `rs`

---

#### Lab: `RollingUdate` Strategy

```yaml
# demo-strategy-rollingupdate.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-strategy-rollingupdate
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 1
  minReadySeconds: 10
  selector:
    matchLabels:
      app: demo-rollingupdate
  template:
    metadata:
      labels:
        app: demo-rollingupdate
    spec:
      containers:
        - image: web
          name: nginx
```

```sh
kubectl apply -f demo-strategy-rollingupdate.yaml
# deployment.apps/demo-strategy-rollingupdate created

# get the rollout status
kubectl rollout status deploy demo-strategy-rollingupdate
# Waiting for deployment "demo-strategy-rollingupdate" rollout to finish: 0 of 3 updated replicas are available...
# Waiting for deployment "demo-strategy-rollingupdate" rollout to finish: 0 of 3 updated replicas are available...
# Waiting for deployment "demo-strategy-rollingupdate" rollout to finish: 0 of 3 updated replicas are available...
# Waiting for deployment "demo-strategy-rollingupdate" rollout to finish: 1 of 3 updated replicas are available...
# Waiting for deployment "demo-strategy-rollingupdate" rollout to finish: 2 of 3 updated replicas are available...
# deployment "demo-strategy-rollingupdate" successfully rolled out

# confirm rs by monitoring:
kubectl get rs -w
# NAME                                     DESIRED   CURRENT   READY   AGE
# demo-strategy-rollingupdate-79f49b4c46   3         0         0       0s
# demo-strategy-rollingupdate-79f49b4c46   3         0         0       0s
# demo-strategy-rollingupdate-79f49b4c46   3         3         0       0s
# demo-strategy-rollingupdate-79f49b4c46   3         3         1       3s
# demo-strategy-rollingupdate-79f49b4c46   3         3         2       4s
# demo-strategy-rollingupdate-79f49b4c46   3         3         3       8s
# demo-strategy-rollingupdate-79f49b4c46   3         3         3       13s
# demo-strategy-rollingupdate-79f49b4c46   3         3         3       14s
# demo-strategy-rollingupdate-79f49b4c46   3         3         3       18s

# confirm deploy by monitoring:
kubectl get deploy -w
# NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
# demo-strategy-rollingupdate   0/3     0            0           0s
# demo-strategy-rollingupdate   0/3     0            0           0s
# demo-strategy-rollingupdate   0/3     0            0           0s
# demo-strategy-rollingupdate   0/3     3            0           0s
# demo-strategy-rollingupdate   1/3     3            0           3s
# demo-strategy-rollingupdate   2/3     3            0           4s
# demo-strategy-rollingupdate   3/3     3            0           8s
# demo-strategy-rollingupdate   3/3     3            1           13s
# demo-strategy-rollingupdate   3/3     3            2           14s
# demo-strategy-rollingupdate   3/3     3            3           18s

# confirm history
kubectl rollout history deploy demo-strategy-rollingupdate
# deployment.apps/demo-strategy-rollingupdate
# REVISION  CHANGE-CAUSE
# 1         <none>

```

- Set image

```sh
kubectl set image deploy demo-strategy-rollingupdate web=httpd
# deployment.apps/demo-strategy-rollingupdate image updated

# confirm rs by monitoring:
# old rs scale down and new rs scale up gradually
kubectl get rs -w
# NAME                                     DESIRED   CURRENT   READY   AGE
# demo-strategy-rollingupdate-79f49b4c46   3         3         3       2m26s
# demo-strategy-rollingupdate-6b9cc477f4   0         0         0       0s
# demo-strategy-rollingupdate-6b9cc477f4   0         0         0       0s
# demo-strategy-rollingupdate-79f49b4c46   2         3         3       2m41s
# demo-strategy-rollingupdate-6b9cc477f4   1         0         0       0s
# demo-strategy-rollingupdate-79f49b4c46   2         3         3       2m41s
# demo-strategy-rollingupdate-79f49b4c46   2         2         2       2m41s
# demo-strategy-rollingupdate-6b9cc477f4   1         0         0       0s
# demo-strategy-rollingupdate-6b9cc477f4   1         1         0       0s
# demo-strategy-rollingupdate-6b9cc477f4   1         1         1       4s
# demo-strategy-rollingupdate-6b9cc477f4   1         1         1       16s
# demo-strategy-rollingupdate-79f49b4c46   1         2         2       2m57s
# demo-strategy-rollingupdate-79f49b4c46   1         2         2       2m57s
# demo-strategy-rollingupdate-6b9cc477f4   2         1         1       16s
# demo-strategy-rollingupdate-79f49b4c46   1         1         1       2m57s
# demo-strategy-rollingupdate-6b9cc477f4   2         1         1       16s
# demo-strategy-rollingupdate-6b9cc477f4   2         2         1       16s
# demo-strategy-rollingupdate-6b9cc477f4   2         2         2       18s
# demo-strategy-rollingupdate-6b9cc477f4   2         2         2       28s
# demo-strategy-rollingupdate-79f49b4c46   0         1         1       3m9s
# demo-strategy-rollingupdate-79f49b4c46   0         1         1       3m9s
# demo-strategy-rollingupdate-6b9cc477f4   3         2         2       28s
# demo-strategy-rollingupdate-6b9cc477f4   2         2         1       16s
# demo-strategy-rollingupdate-79f49b4c46   0         0         0       3m9s
# demo-strategy-rollingupdate-6b9cc477f4   3         2         2       28s
# demo-strategy-rollingupdate-6b9cc477f4   3         3         2       28s
# demo-strategy-rollingupdate-6b9cc477f4   3         3         3       30s
# demo-strategy-rollingupdate-6b9cc477f4   3         3         3       41s

# confirm deploy by monitoring:
#  always ready: 2
kubectl get deploy -w
# NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
# demo-strategy-rollingupdate   3/3     3            3           2m34s
# demo-strategy-rollingupdate   3/3     3            3           2m41s
# demo-strategy-rollingupdate   3/3     3            3           2m41s
# demo-strategy-rollingupdate   3/3     0            3           2m41s
# demo-strategy-rollingupdate   2/3     0            2           2m41s
# demo-strategy-rollingupdate   2/3     1            2           2m41s
# demo-strategy-rollingupdate   3/3     1            2           2m45s
# demo-strategy-rollingupdate   3/3     1            3           2m57s
# demo-strategy-rollingupdate   2/3     1            2           2m57s
# demo-strategy-rollingupdate   2/3     2            2           2m57s
# demo-strategy-rollingupdate   3/3     2            2           2m59s
# demo-strategy-rollingupdate   2/3     1            2           2m41s
# demo-strategy-rollingupdate   3/3     2            3           3m9s
# demo-strategy-rollingupdate   2/3     2            2           3m9s
# demo-strategy-rollingupdate   2/3     3            2           3m9s
# demo-strategy-rollingupdate   3/3     3            2           3m11s
# demo-strategy-rollingupdate   3/3     3            3           3m22s

```

## Control Rollout Process

- `spec.progressDeadlineSeconds` field
  - configure the **rollout progress deadline**
    - `rollout process` never stops completely when reaching deadline
  - default: `600s`
  - confirm by `status.conditions.Progressing`

---

### Pausing and Resuming the Rollout Process

- `kubectl rollout pause deployment kiada`
  - sets `spec.paused` = true
  - `Deployment controller` **checks** this field **before** any change to the underlying `ReplicaSets`.
- deployment running **both** the old and new versions

- `kubectl rollout resume deployment kiada`

---

## Preventing a Faulty Version

- `Ready` vs `Available`

  - `Ready`:
    - the pods are passing `readiness probes`
  - `Available`:
    - the pod is ready **for a specific amount of time**
    - the `rolling update` continues only if the new pod is avaialbe.

- `minReadySeconds` field

  - used to define the **amount of time** between `ready` and `avaialbe`.
  - default: `0`
    - the pods are available when reaady.
  - during this time, a Pod can **receives client requests**.

---

### With `Recreate` Strategy

- Scenario:
  - `replicas: 3`
  - `strategy: Recreate`
  - `minReadySeconds: 60`
- How it works:
  - new manifest applys
  - `Deployment Controller` first **scales down** the **desired replica** of the old `ReplicaSet` to **zero**;
  - `ReplicaSet Controller` **terminates** the old pods of the old `ReplicaSet`
  - `Deployment Controller` **waits** for the Pods to be fully terminated;
  - `Deployment Controller` **creates** a new `ReplicaSet` and scale up
  - `ReplicaSet Controller` **creates** new pod aligned with the new `ReplicaSet`
  - New pods pass `Reaadiness Probe`; Pods accept traffic.
  - The `Deployment`
    - shows status of `READY 3/3` but `AVAILABLE 0`
    - waits until the `minReadySeconds: 60`
  - If pods stay healthy after `minReadySeconds`, deployment status shows `AVAILABLE 3/3`

| Phase       | Deployment Status        | Real-World Impact                          |
| ----------- | ------------------------ | ------------------------------------------ |
| Start       | `3/3 READY, 3 AVAILABLE` | Old version running.                       |
| Scale Down  | `0/0 READY, 0 AVAILABLE` | Downtime begins. All old pods are killed.  |
| Scale Up    | `0/3 READY, 0 AVAILABLE` | New pods are starting (ContainerCreating). |
| Probes Pass | `3/3 READY, 0 AVAILABLE` | Downtime ends. Traffic flows to new pods.  |
| Probation   | `3/3 READY, 0 AVAILABLE` | minReadySeconds timer is counting          |
| Success     | `3/3 READY, 3 AVAILABLE` | Rollout complet                            |

---

#### Lab: Recreate with `minReadySeconds`

```yaml
# demo-recreate-minreadyseconds.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-recreate-minreadyseconds
spec:
  replicas: 3
  minReadySeconds: 60
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - image: nginx
          name: web
```

```sh
kubectl apply -f demo-recreate-minreadyseconds.yaml
# deployment.apps/demo-recreate-minreadyseconds created

# update image
kubectl set image deploy demo-recreate-minreadyseconds web=httpd
# deployment.apps/demo-recreate-minreadyseconds image updated


# rollout status: wait until 60s
kubectl rollout status deploy demo-recreate-minreadyseconds
# Waiting for deployment "demo-recreate-minreadyseconds" rollout to finish: 0 of 3 updated replicas are available...
# Waiting for deployment "demo-recreate-minreadyseconds" rollout to finish: 0 of 3 updated replicas are available...
# Waiting for deployment "demo-recreate-minreadyseconds" rollout to finish: 0 of 3 updated replicas are available...
# Waiting for deployment "demo-recreate-minreadyseconds" rollout to finish: 0 of 3 updated replicas are available...
# deployment "demo-recreate-minreadyseconds" successfully rolled out

# deploy status:
#   READY=0 for short time
#   all ready: 4m36s
#   all available: 5m36s
kubectl get deploy -w
# NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
# demo-recreate-minreadyseconds   3/3     3            3           3m50s
# demo-recreate-minreadyseconds   3/3     3            3           4m28s
# demo-recreate-minreadyseconds   3/3     0            3           4m28s
# demo-recreate-minreadyseconds   0/3     0            0           4m28s
# demo-recreate-minreadyseconds   0/3     0            0           4m30s
# demo-recreate-minreadyseconds   0/3     0            0           4m30s
# demo-recreate-minreadyseconds   0/3     3            0           4m30s
# demo-recreate-minreadyseconds   1/3     3            0           4m34s
# demo-recreate-minreadyseconds   2/3     3            0           4m34s
# demo-recreate-minreadyseconds   3/3     3            0           4m36s
# demo-recreate-minreadyseconds   3/3     3            3           5m36s

# rs:
#  old rs scale down to 0
#  create new rs
#  new rs scale up
kubectl get rs -w
# NAME                                       DESIRED   CURRENT   READY   AGE
# demo-recreate-minreadyseconds-5f876cbdc4   3         3         3       3m57s
# demo-recreate-minreadyseconds-5f876cbdc4   0         3         3       4m28s
# demo-recreate-minreadyseconds-5f876cbdc4   0         3         3       4m28s
# demo-recreate-minreadyseconds-5f876cbdc4   0         0         0       4m28s
# demo-recreate-minreadyseconds-59778758cd   3         0         0       0s
# demo-recreate-minreadyseconds-59778758cd   3         0         0       1s
# demo-recreate-minreadyseconds-59778758cd   3         3         0       1s
# demo-recreate-minreadyseconds-59778758cd   3         3         1       5s
# demo-recreate-minreadyseconds-59778758cd   3         3         2       5s
# demo-recreate-minreadyseconds-59778758cd   3         3         3       7s
# demo-recreate-minreadyseconds-59778758cd   3         3         3       67s

```

---

### With RollingOut Strategy

- Scenario:
  - `replicas: 3`
  - `strategy: RollingUpdate`
  - `maxSurge: 1`
  - `maxUnavailable: 0`
  - `minReadySeconds: 60`
- How it works:
  - New manifest applies.
  - `Deployment Controller` **creates** a `new ReplicaSet` (New RS).
  - `Deployment Controller` **scales** the `new ReplicaSet` to **1** (calculated as replicas + maxSurge).
  - `ReplicaSet Controller` creates the first `new pod`.
  - `New pod` **passes** `Readiness Probe`; Pod begins **accepting traffic**.
  - The `Deployment` shows `READY 4/3` but `AVAILABLE 3`.
  - `Deployment Controller` waits until the `minReadySeconds: 60` timer finishes for that specific pod.
  - Once the pod is **Available**, the `Deployment Controller` **scales down** the `old ReplicaSet` to **2**.
  - The cycle repeats:
    - It "surges" a second new pod, waits 60s, then kills a second old pod.
  - This continues until only the 3 new pods remain.

| Phase           | Pod Count (Old/New) | Deployment Status        | Real-World Impact                    |
| --------------- | ------------------- | ------------------------ | ------------------------------------ |
| Start           | 3 Old / 0 New       | `3/3 READY, 3 AVAILABLE` | Only old version running.            |
| First Surge     | 3 Old / 1 New       | `4/3 READY, 3 AVAILABLE` | New pod starting; total 4 pods.      |
| First Ready     | 3 Old / 1 New       | `4/3 READY, 3 AVAILABLE` | Traffic hits new pod. Timer starts.  |
| First Available | 3 Old / 1 New       | `4/3 READY, 4 AVAILABLE` | New pod passed 60s probation.        |
| Scale Down      | 2 Old / 1 New       | `3/3 READY, 3 AVAILABLE` | One old pod killed. Total back to 3. |
| Second Surge    | 2 Old / 2 New       | `4/3 READY, 3 AVAILABLE` | Process repeats for the next pod.    |
| Success         | 0 Old / 3 New       | `3/3 READY, 3 AVAILABLE` | Rollout complete; 0 downtime.        |

---

#### Lab: RollingOut with `minReadySeconds`

```yaml
# demo-rollingout-minreadyseconds.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-rollingout-minreadyseconds
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  minReadySeconds: 60
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx
```

```sh
kubectl apply -f demo-rollingout-minreadyseconds.yaml
# deployment.apps/demo-rollingout-minreadyseconds created

# update image
kubectl set image deploy demo-rollingout-minreadyseconds web=httpd
# deployment.apps/demo-rollingout-minreadyseconds image updated


# rollout status: wait until 60s
kubectl rollout status deploy demo-rollingout-minreadyseconds
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 1 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 1 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 1 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 1 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 2 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 2 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 2 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 2 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "demo-rollingout-minreadyseconds" rollout to finish: 1 old replicas are pending termination...
# deployment "demo-rollingout-minreadyseconds" successfully rolled out

# deploy status:
# repeat process:
#   READY & avaialable: up to 4 and down to 4
kubectl get deploy -w
# NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
# demo-rollingout-minreadyseconds   3/3     3            0           22s
# demo-rollingout-minreadyseconds   3/3     3            3           68s
# demo-rollingout-minreadyseconds   3/3     3            3           81s
# demo-rollingout-minreadyseconds   3/3     3            3           81s
# demo-rollingout-minreadyseconds   3/3     0            3           81s
# demo-rollingout-minreadyseconds   3/3     1            3           81s
# demo-rollingout-minreadyseconds   4/3     1            3           84s
# demo-rollingout-minreadyseconds   4/3     1            4           2m26s
# demo-rollingout-minreadyseconds   3/3     1            3           2m26s
# demo-rollingout-minreadyseconds   3/3     2            3           2m26s
# demo-rollingout-minreadyseconds   4/3     2            3           2m29s
# demo-rollingout-minreadyseconds   4/3     2            4           3m31s
# demo-rollingout-minreadyseconds   3/3     2            3           3m31s
# demo-rollingout-minreadyseconds   3/3     3            3           3m31s
# demo-rollingout-minreadyseconds   4/3     3            3           3m34s
# demo-rollingout-minreadyseconds   4/3     3            4           4m36s
# demo-rollingout-minreadyseconds   3/3     3            3           4m36s

# rs:
kubectl get rs -w
# NAME                                         DESIRED   CURRENT   READY   AGE
# demo-rollingout-minreadyseconds-5f876cbdc4   3         3         3       27s
# demo-rollingout-minreadyseconds-5f876cbdc4   3         3         3       68s
# demo-rollingout-minreadyseconds-59778758cd   1         0         0       0s
# demo-rollingout-minreadyseconds-59778758cd   1         0         0       0s
# demo-rollingout-minreadyseconds-59778758cd   1         1         0       0s
# demo-rollingout-minreadyseconds-59778758cd   1         1         1       3s
# demo-rollingout-minreadyseconds-59778758cd   1         1         1       65s
# demo-rollingout-minreadyseconds-5f876cbdc4   2         3         3       2m26s
# demo-rollingout-minreadyseconds-59778758cd   2         1         1       65s
# demo-rollingout-minreadyseconds-5f876cbdc4   2         3         3       2m26s
# demo-rollingout-minreadyseconds-59778758cd   2         1         1       65s
# demo-rollingout-minreadyseconds-5f876cbdc4   2         2         2       2m26s
# demo-rollingout-minreadyseconds-59778758cd   2         2         1       65s
# demo-rollingout-minreadyseconds-59778758cd   2         2         2       68s
# demo-rollingout-minreadyseconds-59778758cd   2         2         2       2m10s
# demo-rollingout-minreadyseconds-5f876cbdc4   1         2         2       3m31s
# demo-rollingout-minreadyseconds-59778758cd   3         2         2       2m10s
# demo-rollingout-minreadyseconds-5f876cbdc4   1         2         2       3m31s
# demo-rollingout-minreadyseconds-5f876cbdc4   1         1         1       3m31s
# demo-rollingout-minreadyseconds-59778758cd   3         2         2       2m10s
# demo-rollingout-minreadyseconds-59778758cd   3         3         2       2m10s
# demo-rollingout-minreadyseconds-59778758cd   3         3         3       2m13s
# demo-rollingout-minreadyseconds-59778758cd   3         3         3       3m15s
# demo-rollingout-minreadyseconds-5f876cbdc4   0         1         1       4m36s
# demo-rollingout-minreadyseconds-5f876cbdc4   0         1         1       4m36s
# demo-rollingout-minreadyseconds-5f876cbdc4   0         0         0       4m36s

```

---

#### Lab: RollingOut with `minReadySeconds` if a faulty version

```yaml
# demo-rollingout-minreadyseconds-faulty.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-rollingout-minreadyseconds-faulty
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  minReadySeconds: 60
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx
```

```sh
kubectl apply -f demo-rollingout-minreadyseconds-faulty.yaml
# deployment.apps/demo-rollingout-minreadyseconds-faulty created

# update faulty image
kubectl set image deploy demo-rollingout-minreadyseconds-faulty web=web

# confirm: rollout get stuck
kubectl rollout status deploy demo-rollingout-minreadyseconds-faulty
# Waiting for deployment "demo-rollingout-minreadyseconds-faulty" rollout to finish: 1 out of 3 new replicas have been updated...
# Waiting for deployment "demo-rollingout-minreadyseconds-faulty" rollout to finish: 1 out of 3 new replicas have been updated...
# error: deployment "demo-rollingout-minreadyseconds-faulty" exceeded its progress deadline

# deploy status:
kubectl get deploy -w
# NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
# demo-rollingout-minreadyseconds-faulty   3/3     3            3           2m58s
# demo-rollingout-minreadyseconds-faulty   3/3     3            3           3m19s
# demo-rollingout-minreadyseconds-faulty   3/3     3            3           3m19s
# demo-rollingout-minreadyseconds-faulty   3/3     0            3           3m19s
# demo-rollingout-minreadyseconds-faulty   3/3     1            3           3m19s

# rs:
kubectl get rs -w
# NAME                                                DESIRED   CURRENT   READY   AGE
# demo-rollingout-minreadyseconds-faulty-5f876cbdc4   3         3         3       3m6s
# demo-rollingout-minreadyseconds-faulty-7fc574699b   1         0         0       0s
# demo-rollingout-minreadyseconds-faulty-7fc574699b   1         0         0       0s
# demo-rollingout-minreadyseconds-faulty-7fc574699b   1         1         0       0s

kubectl get pod
# NAME                                                      READY   STATUS             RESTARTS   AGE
# demo-rollingout-minreadyseconds-faulty-5f876cbdc4-9zgdr   1/1     Running            0          5m23s
# demo-rollingout-minreadyseconds-faulty-5f876cbdc4-p4sd4   1/1     Running            0          5m23s
# demo-rollingout-minreadyseconds-faulty-5f876cbdc4-w7xtk   1/1     Running            0          5m23s
# demo-rollingout-minreadyseconds-faulty-7fc574699b-rqqgb   0/1     ImagePullBackOff   0          2m4s
```

> rolling update gets stuck because the image is incorrect and the `maxUnavailable: 0`, which does not allow unavailable pod.
> therefore deployment rolling update provide a safety net.

---

- fix: rollback

```sh
# check history before rollback
kubectl rollout history deployment demo-rollingout-minreadyseconds-faulty
# deployment.apps/demo-rollingout-minreadyseconds-faulty
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>

# rollback deploy
kubectl rollout undo deployment demo-rollingout-minreadyseconds-faulty
# deployment.apps/demo-rollingout-minreadyseconds-faulty rolled back

# deploy status
kubectl get deploy -w
# NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
# demo-rollingout-minreadyseconds-faulty   3/3     1            3           17m
# demo-rollingout-minreadyseconds-faulty   3/3     1            3           18m
# demo-rollingout-minreadyseconds-faulty   3/3     1            3           18m
# demo-rollingout-minreadyseconds-faulty   3/3     3            3           18m
# demo-rollingout-minreadyseconds-faulty   3/3     3            3           18m

kubectl get rs -w
# NAME                                                DESIRED   CURRENT   READY   AGE
# demo-rollingout-minreadyseconds-faulty-5f876cbdc4   3         3         3       17m
# demo-rollingout-minreadyseconds-faulty-7fc574699b   1         1         0       13m
# demo-rollingout-minreadyseconds-faulty-5f876cbdc4   3         3         3       18m
# demo-rollingout-minreadyseconds-faulty-7fc574699b   0         1         0       14m
# demo-rollingout-minreadyseconds-faulty-7fc574699b   0         1         0       14m
# demo-rollingout-minreadyseconds-faulty-7fc574699b   0         0         0       14m

kubectl rollout history deployment demo-rollingout-minreadyseconds-faulty
# deployment.apps/demo-rollingout-minreadyseconds-faulty
# REVISION  CHANGE-CAUSE
# 2         <none>
# 3         <none>

# confirm: image roll back
kubectl get deploy -o wide
# NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
# demo-rollingout-minreadyseconds-faulty   3/3     3            3           20m   web          nginx    app=web
```

---

## Rollout History

- `CHANGE-CAUSE` colume

  - pass message by the `--record` option of the `kubectl` command
    - has deprecated

- inspect each revision

  - `kubectl rollout history deploy NAME --revision 2`

- revision history

  - represented by the `ReplicaSets` associated with the Deployment

- `deploy.spec.revisionHistoryLimit`

  - specify the **size of the revision history**, and thus the **number** of `ReplicaSets` that the Deployment controller **keeps** for a given Deployment,
  - default: 10

- revision numbe also stored in the `ReplicaSet’s` **annotations**

---

## Rollout Restart

- **deletes and replaces** the `Pods` using the **same strategy** used for updates.
- refresh Pods without changing anything in the configuration.

- it follows the deployment strategy
  - `RollingUpdate` strategy: the Pods are **recreated gradually**
  - `Recreate`: deleted and recreated simultaneously.

---

## Rollback

- `Rollback`

  - undo a change
  - Behind the scence:
    - Rollback creates a new rs, then take one pod from the new version rs, and bring up one pod in old rs, until all pods in new rs are down.
    - Can be verify duration deployment upgrade, `kubectl get rs`

- if the `RollingUpdate` strategy is used, the Pods are **rolled back gradually**.
- The `kubectl rollout undo` command can be used **while the rollout process is running** to **cancel** the `rollout`, or after the `rollout` is **complete** to undo it.

- When a `Deployment` is **paused** with the `kubectl pause` command, the `kubectl rollout undo` command **does nothing until you resume** the Deployment with `kubectl rollout resume`.

---

### Rolling Back vs Apply Old Manifest

- `kubectl rollout undo` command:

  - reverts only the **Pod template**
  - **preserves any other changes** you made to the Deployment manifest.
    - e.g.,
      - **update strategy**
      - **desired number** of replicas

- `kubectl apply` command:
  - overwrites these changes that no included in the manifest.

---
