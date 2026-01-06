# Kubernetes: Deployment

[Back](../../index.md)

- [Kubernetes: Deployment](#kubernetes-deployment)
  - [Deployment](#deployment)
    - [Deployment status](#deployment-status)
    - [Additional Labels](#additional-labels)
    - [Deployment vs ReplicaSet](#deployment-vs-replicaset)
    - [Deployment Deletion](#deployment-deletion)
  - [Imperative Command](#imperative-command)
  - [Declarative Manifest](#declarative-manifest)
    - [Key fields](#key-fields)
  - [Scaling Deployment](#scaling-deployment)
  - [Good Practice: Omitting `replicas` field](#good-practice-omitting-replicas-field)
    - [Lab: omitting `replicas` field](#lab-omitting-replicas-field)
      - [Problem](#problem)
      - [Solution](#solution)
  - [Lab: Default Replica and strategy](#lab-default-replica-and-strategy)

---

## Deployment

- `Deployment`

  - an **abstraction layer** over `ReplicaSet`
  - manage the **deployment** of `ReplicaSet`.
    - can **update** the `ReplicaSet` and **roll back to the previous version**.

- mainly used for **stateless workloads**

  - the `pods` created with `deployment` are **fungible**

- Major roles:

  - **Declarative Updates**:
    - declare the desired state with YAML (or CLI)
  - **Scaling**
    - Easily scale applications up or down
  - **Rolling Updates**
    - **Deploy new versions** of your app without downtime.
  - **Rollback**
    - If something goes wrong, you can roll back to a previous version
  - **Self-healing**
    - If a Pod crashes or a node goes down, the Deployment (via ReplicaSet) ensures new Pods are scheduled.

---

### Deployment status

- `Progressing`;
  - `Deployment` **creates** a new `ReplicaSet`.
  - `Deployment` is **scaling up** its newest `ReplicaSet`.
  - `Deployment` is **scaling down** its older `ReplicaSet(s)`.
  - New `Pods` become **ready or available** (ready for at least MinReadySeconds).
- `complete`:
  - All of the `replicas` **have been updated to the latest version**
  - All of the `replicas` are **available**.
  - **No old** `replicas` for the Deployment are running.
- `Failed`

  - Insufficient **quota**
  - `Readiness probe` failures
  - **Image pull** errors
  - Insufficient **permissions**
  - Limit **ranges**
  - Application runtime **misconfiguration**

- **Troubleshooting** `Deployment` failure:
  - `kubectl describe`:
    - get details of deploy and replicaset
    - event: show failure event
    - condition: show Type, Status, Reason
  - `kubectl get -o yaml`
    - output the detail message of deployment and replicaset

---

### Additional Labels

- `pod-template-hash` Label
  - Automatically add to the underlying `rs` and `pod`
    - become part of the underlying `RS` name
  - **calculated** from the contents of the **Pod template**
- When the `Pod template` gets **changed**, a **new** `ReplicaSet` is **created**.

---

### Deployment vs ReplicaSet

- `ReplicaSet`: Ensures a **fixed number** of Pods are running.
- `Deployment`: Manages `ReplicaSets`, and adds features like `rolling updates` and `rollbacks`.

  - Most of the time, you won’t create ReplicaSets directly — you use a Deployment.

- `Deployment` **controls** the `ReplicaSet`, which in turn controls the individual `Pods`.
- a `ReplicaSet` object that’s **automatically created** when **creating** the `Deployment` object.

  - A `Deployment` object **doesn**'t directly **manage** the `Pod` objects, but **manages** them through a `ReplicaSet` object

- **Updating Pod template**

  - `ReplicaSet`: update only the **new** created pod
  - `Deploymen`: update pods immediately

- Existing pod: the existing pods with matching labels
  - `ReplicaSet`: controlled by RS
  - `Deploymen`: not controlled by Deploy, because additional label `pod-template-hash` will be added.

---

### Deployment Deletion

- when you delete a `Deployment` object, the underlying `ReplicaSet` and `Pods` are also deleted.

- Preserving the `ReplicaSet` and `Pods`

  - `kubectl delete deploy NAME --cascade=orphan`

- Adopting an existing `ReplicaSet` and `Pods`
  - Recreate deployment if the pod template unchanged.
  - because the additional label `pod-template-hash` is calculated based on the pod template.

---

## Imperative Command

- CRUD

| Command                                                                           | Description                                            |
| --------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `kubectl explain deploy`                                                          | show deployment documentation                          |
| `kubectl get deploy`                                                              | List all Deployments in the current namespace.         |
| `kubectl describe deploy deploy_name`                                             | Show detailed information about a specific Deployment. |
| `kubectl create deploy deploy_name --image=img_name`                              | Create a deployment using image                        |
| `kubectl create deploy nginx --image=nginx --dry-run=client --replicas=4 -o yaml` | Show the deployemnt in yaml file                       |
| `kubectl set image deploy_name nginx=nginx:1.25`                                  | Update the container image in a deployment             |
| `kubectl delete deploy deploy_name`                                               | Delete a Deployment by name.                           |
| `kubectl scale deploy deploy_name --replicas=count-num`                           | Scale the number of replicas for a Deployment.         |

- List Deploy: `kubectl get deploy`
  - `NAME`:
    - Deployment name
    - nignx
  - `READY`:
    - e.g.,3/3
    - the number of running **pod**/the desired number of **pods**
  - `UP-TO-DATE`
    - e.g.,3
    - the number of Pods that runs the current version
    - used to indicate whether rollout is still in progress.
  - `AVAILABLE`
    - e.g.,3
    - the number of pods that both are ready and have been ready for `spec.minReadySeconds`
    - used for rolling updates and zero-downtime guarantees.
  - `AGE`
    - e.g., 18m
    - Time since the **Deployment** object was created
    - Get updated when
      - cluster restarted
      - rolled out a new version
      - Pod crashed and was recreated

---

## Declarative Manifest

### Key fields

- `spec.replicas`:
  - desired number of replica
- `spec.selector`:
  - label selector
  - `matchLabels`: a map of lables
  - `matchExpressions`: a list of label selector requirements
- `spec.template`:
  - Pod template
- `spec.strategy`:
  - how `Pods` are replaced when **updating the Pod template**.

---

## Scaling Deployment

- When scaling a `Deployment`, the `Deployment controller` does nothing but **scale the underlying** `ReplicaSet`

  - `Deployment controller` updates the desired number of the replicas in the `ReplicaSet`
  - then the `ReplicaSet controller` to do the rest.

- If scale the underlying `RS`, the `RS controller` scales the number of pod imdiately.

  - then the `deploy controller` detects the difference between the desired replicas in the `deploy` and the underlying `rs`, and update the replicas in the `rs`
  - finally, `rs controller` reconcile the pod number.

- If the underlying `rs` object get deleted, the `deploy controller` will recreate the `rs`

---

## Good Practice: Omitting `replicas` field

- Practical but problematical scenario:

  - define `replicas=3` in manifest
  - scale to 5 with `kubectl scale`
  - update manifest without changing the `replicas` field and apply
    - replicas return to 3, disrupting the service.

- To avoid **accidentally scaling** a Deployment each time you **reapply its manifest file**

  - omitting the `replicas` field, which creates only 1 replica when creating
  - then `kubectl scale` to update the replica number
    - the replica number won't be touched even reapply the manifest.

- if the `replica` already apply:
  - `kubectl apply edit-last-applied deploy NAME`: to remove the replicas field in the snapshot

---

### Lab: omitting `replicas` field

#### Problem

- manifest

```yaml
# demo-deploy-with-replica.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-deploy-with-replica
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - image: nginx
          name: nginx
```

```sh
kubectl apply -f demo-deploy-with-replica.yaml
# deployment.apps/demo-deploy-with-replica created

kubectl get deploy
# NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
# demo-deploy-with-replica   3/3     3            3           25s
```

- Manually scale

```sh
kubectl scale deploy demo-deploy-with-replica --replicas=5
# deployment.apps/demo-deploy-with-replica scaled

# confirm
kubectl get deploy
# NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
# demo-deploy-with-replica   5/5     5            5           2m56s
```

- reapply the manifest

```sh
kubectl apply -f demo-deploy-with-replica.yaml
# deployment.apps/demo-deploy-with-replica configured

# confirm: replica back to 3
kubectl get deploy
# NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
# demo-deploy-with-replica   3/3     3            3           3m53s
```

> the replica number change back to 3

---

#### Solution

- manifest without replica

```yaml
# demo-deploy-without-replica.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-deploy-without-replica
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - image: nginx
          name: nginx
```

```sh
kubectl apply -f demo-deploy-without-replica.yaml
# deployment.apps/demo-deploy-without-replica created

kubectl get deploy
# NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
# demo-deploy-without-replica   1/1     1            1           22s
```

- Manually scale

```sh
kubectl scale deploy demo-deploy-without-replica --replicas=5
# deployment.apps/demo-deploy-without-replica scaled

kubectl get deploy
# NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
# demo-deploy-without-replica   5/5     5            5           2m33s
```

- make some change and reapply manifest
  - add label: tier=web

```sh
kubectl apply -f demo-deploy-without-replica.yaml
# deployment.apps/demo-deploy-without-replica configured

kubectl get deploy demo-deploy-without-replica
# NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
# demo-deploy-without-replica   5/5     5            5           5m29s
```

> the replica remain 5.

---

## Lab: Default Replica and strategy

```yaml
# demo-deploy-default-replica.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-deploy-default-replica
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        type: front-end
    spec:
      containers:
        - name: nginx
          image: nginx
```

```sh
# create deployment
kubectl create -f demo-deploy-default-replica.yaml
# deployment.apps/demo-deploy-default-replica created

kubectl get deploy
# NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
# demo-deploy-default-replica   1/1     1            1           96s

# also create rs
kubectl get rs
# NAME                                     DESIRED   CURRENT   READY   AGE
# demo-deploy-default-replica-65cf588b89   1         1         1       106s

kubectl get pods
# NAME                                           READY   STATUS    RESTARTS   AGE
# demo-deploy-default-replica-65cf588b89-v4kpd   1/1     Running   0          2m20s

# confirm deploy:
#   default replica=1; default StrategyType=RollingUpdate; RollingUpdateStrategy:25% max unavailable, 25% max surge
kubectl describe deploy demo-deploy-default-replica
# Selector:               app=nginx
# Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
# StrategyType:           RollingUpdate
# RollingUpdateStrategy:  25% max unavailable, 25% max surge

# confirm rs:
#   Controlled by: deloy
#   additional label added: pod-template-hash + selector labels
kubectl describe rs demo-deploy-default-replica
# Labels:         app=nginx
#                 pod-template-hash=65cf588b89
#                 type=front-end
# Controlled By:  Deployment/demo-deploy-default-replica
# Replicas:       1 current / 1 desired

# confirm pod:
#   Controlled by rs
#   additional label added: pod-template-hash + selector labels
kubectl describe pod demo-deploy-default-replica
# Controlled By:  ReplicaSet/demo-deploy-default-replica-65cf588b89
# Labels:           app=nginx
#                   pod-template-hash=65cf588b89
#                   type=front-end
```

---
