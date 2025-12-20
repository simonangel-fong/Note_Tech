# Kubernetes - Pod: ReplicaSet

[Back](../../index.md)

- [Kubernetes - Pod: ReplicaSet](#kubernetes---pod-replicaset)
  - [ReplicaSet](#replicaset)
    - [vs Deployment](#vs-deployment)
    - [Common Commands - `ReplicaSets`](#common-commands---replicasets)
    - [Method to scale number of pods in rs](#method-to-scale-number-of-pods-in-rs)
  - [Lab: ReplicaSets](#lab-replicasets)
    - [Creating ReplicaSets](#creating-replicasets)
    - [Scale ReplicaSet](#scale-replicaset)
    - [Delete a pod to test pod auto creation](#delete-a-pod-to-test-pod-auto-creation)
    - [Create new pod manually to test rs](#create-new-pod-manually-to-test-rs)
    - [Change replica number in temp file](#change-replica-number-in-temp-file)
    - [Delete RS](#delete-rs)
  - [ReplcationController](#replcationcontroller)
    - [Common Commands - `ReplicationControllers`](#common-commands---replicationcontrollers)
  - [Lab: ReplicationController](#lab-replicationcontroller)
    - [Create RC](#create-rc)
    - [Scale Replicas](#scale-replicas)
    - [Delete RC](#delete-rc)
  - [Common Questions](#common-questions)

---

- ref:
  - https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/

## ReplicaSet

- `ReplicaSet`

  - used to replce the old technology `Replication Controller`
  - a workload **controller** that ensures a **specified number** of **identical** `Pods` are always running.
  - defined declaratively in a **YAML manifest** and continuously watches the cluster state through the Kubernetes `Control Plane`.

- A `ReplicaSet` keeps your app **highly available**.

  - If a `Pod` **fails**, is **deleted**, or a node **crashes**, `ReplicaSet` **creates a replacement** Pod.
  - If there are **too many** Pods, `ReplicaSet` removes extra ones.

- Primary roles:

  - **Scaling**:
    - ensures **the desired number** of **replicas** (Pods) are running.
    - can increase/decrease replicas dynamically (`kubectl scale`).
  - **Self-healing**:
    - if a Pod **crashes**, the `ReplicaSet` automatically **recreates** it.
  - **Pod Management**:
    - tracks Pods using **label selectors**.
    - Any Pod with **matching** labels is **managed** by the RS.
  - **Foundation for `Deployments`**:
    - rarely use `ReplicaSets` directly.
    - Instead, `Deployments` manage `ReplicaSets` for **rolling updates** and **rollback**.

---

- `spec.template`: the template to define pod
- `spec.replicas`: the desired number of pod
- `spec.selector.matchLabels`:
  - the label selector, can include the label created before the rs.
  - the matchLables must match **at least one** of the labels defined in metadata; Otherwise, cannot create rs.

---

### vs Deployment

- Troubleshoting - Confuse with deploy and rs

```sh
# when get rs, it might return rs with random suffix
kubectl get rs
# NAME               DESIRED   CURRENT   READY   AGE
# nginx-5bb7d64fc4   3         3         3       41s

# it is caused by deployment,not rs.
# the commond kubectl delete rs rs_name wouldn't help
# it should be remove by
kubectl get deploy
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE
# nginx   3/3     3            3           145m

kubectl delete deploy
# deployment.apps "nginx" deletedD

kubectl get deploy
# No resources found in default namespace.

kubectl get rs
# No resources found in default namespace.
```

---

### Common Commands - `ReplicaSets`

| Command                                      | Description                                            |
| -------------------------------------------- | ------------------------------------------------------ |
| `kubectl get rs`                             | List all ReplicaSets in the current namespace.         |
| `kubectl create -f yaml_file`                | Create a ReplicaSet from a YAML file.                  |
| `kubectl replace -f yaml_file`               | Replace a ReplicaSet with a new one from a YAML file.  |
| `kubectl describe rs rs_name`                | Show detailed information about a specific ReplicaSet. |
| `kubectl edit rs rs_name`                    | Live edit resources                                    |
| `kubectl delete rs rs_name`                  | Delete a ReplicaSet by name.                           |
| `kubectl scale rs rs_name --replicas=rs_num` | Scale the number of replicas for a ReplicaSet.         |
| `kubectl rollout status rs/rs_name`          | Check the status of a rollout for the ReplicaSet.      |
| `kubectl rollout history rs/rs_name`         | View the rollout history of changes to the ReplicaSet. |
| `kubectl rollout undo rs/rs_name`            | Rollback to the previous version of the ReplicaSet.    |
| `kubectl explain rs`                         | Show document of rs                                    |

---

### Method to scale number of pods in rs

- opt1:
  - update the `replicas` in yaml file
  - `kubectl apply -f yaml_file`
- opt2:
  - `kubectl scale -f yaml_file --replicas=6`
  - the nubmer of replicas in the file remain unchanged
- opt3:
  - `kubectl scale rs rs_name --replicas=6`

---

## Lab: ReplicaSets

### Creating ReplicaSets

- Create yaml file `rs-definition.yaml`

```yaml
apiVersion: apps/v1 # version support rs
kind: ReplicaSet # specify objec kind is rs
metadata: # metadata of rs
  name: myapp-replicaset
  labels:
    app: myapp
    type: front-end
spec: # specification of rs
  replicas: 3 # specify pod number
  selector: # specify selector, required in rs
    matchLabels:
      type: front-end
  template: # define template of pod
    metadata: # metadata of pod
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec: # specification of pod
      containers:
        - name: nginx-controller
          image: nginx
```

- create pod

```sh
# create
kubectl create -f rs-definition.yaml
# replicaset.apps/myapp-replicaset created

# confirm
kubectl get rs
# NAME               DESIRED   CURRENT   READY   AGE
# myapp-replicaset   3         3         3       69s

kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-8vvdh   1/1     Running   0          106s
# myapp-replicaset-k7ksc   1/1     Running   0          106s
# myapp-replicaset-tpc58   1/1     Running   0          106s

kubectl describe rs myapp-replicaset
# Name:         myapp-replicaset
# Namespace:    default
# Selector:     type=front-end
# Labels:       app=myapp
#               type=front-end
# Annotations:  <none>
# Replicas:     3 current / 3 desired
# Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
# Pod Template:
#   Labels:  app=myapp
#            type=front-end
#   Containers:
#    nginx-controller:
#     Image:         nginx
#     Port:          <none>
#     Host Port:     <none>
#     Environment:   <none>
#     Mounts:        <none>
#   Volumes:         <none>
#   Node-Selectors:  <none>
#   Tolerations:     <none>
# Events:
#   Type    Reason            Age    From                   Message
#   ----    ------            ----   ----                   -------
#   Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: myapp-replicaset-8vvdh
#   Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: myapp-replicaset-tpc58
#   Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: myapp-replicaset-k7ksc
```

### Scale ReplicaSet

```sh
# scale up
kubectl scale rs myapp-replicaset --replicas=7
# replicaset.apps/myapp-replicaset scaled

kubectl get rs
# NAME               DESIRED   CURRENT   READY   AGE
# myapp-replicaset   7         7         7       3m46

kubectl get pod
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-26qn5   1/1     Running   0          58s
# myapp-replicaset-8t9p7   1/1     Running   0          7m
# myapp-replicaset-9sqtq   1/1     Running   0          58s
# myapp-replicaset-bbhvq   1/1     Running   0          7m
# myapp-replicaset-fnvpw   1/1     Running   0          58s
# myapp-replicaset-fwcgb   1/1     Running   0          58s
# myapp-replicaset-xsd58   1/1     Running   0          7m

# scale down
kubectl scale rs myapp-replicaset --replicas=1
# replicaset.apps/myapp-replicaset scaled

kubectl get rs
# NAME               DESIRED   CURRENT   READY   AGE
# myapp-replicaset   1         1         1       8m

kubectl get pod
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-xsd58   1/1     Running   0          8m18s

# scale down to zero
kubectl scale rs myapp-replicaset --replicas=0
# replicaset.apps/myapp-replicaset scaled

kubectl get rs
# NAME               DESIRED   CURRENT   READY   AGE
# myapp-replicaset   0         0         0       8m51s

kubectl get pod
# No resources found in default namespace.
```

### Delete a pod to test pod auto creation

```sh
# scale up to 3
kubectl scale rs myapp-replicaset --replicas=3
# replicaset.apps/myapp-replicaset scaled

kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-dcrqj   1/1     Running   0          9s
# myapp-replicaset-kgxq2   1/1     Running   0          9s
# myapp-replicaset-vjlj7   1/1     Running   0          9s

# delete a pod manually
kubectl delete pod myapp-replicaset-vjlj7
# pod "myapp-replicaset-vjlj7" deleted from default namespace

# list pods
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-64qrn   1/1     Running   0          11s
# myapp-replicaset-dcrqj   1/1     Running   0          43s
# myapp-replicaset-kgxq2   1/1     Running   0          43s
# one pod has been created automatically.

# confirm in details
kubectl describe rs myapp-replicaset
# Name:         myapp-replicaset
# Namespace:    default
# Selector:     type=front-end
# Labels:       app=myapp
#               type=front-end
# Annotations:  <none>
# Replicas:     3 current / 3 desired
# Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
# Pod Template:
#   Labels:  app=myapp
#            type=front-end
#   Containers:
#    nginx-controller:
#     Image:         nginx
#     Port:          <none>
#     Host Port:     <none>
#     Environment:   <none>
#     Mounts:        <none>
#   Volumes:         <none>
#   Node-Selectors:  <none>
#   Tolerations:     <none>
# Events:
#   Type    Reason            Age   From                   Message
#   ----    ------            ----  ----                   -------
#   Normal  SuccessfulCreate  4m2s  replicaset-controller  Created pod: myapp-replicaset-b9w2c
#   Normal  SuccessfulCreate  4m2s  replicaset-controller  Created pod: myapp-replicaset-n44vm
#   Normal  SuccessfulCreate  4m2s  replicaset-controller  Created pod: myapp-replicaset-gj8sd
#   Normal  SuccessfulCreate  107s  replicaset-controller  Created pod: myapp-replicaset-hrkpg
```

### Create new pod manually to test rs

```sh
# create yaml
tee > pod.yaml <<EOF
apiVersion: v1
kind: Pod
metadata: # metadata of pod
  name: myapp-pod
  labels:
    app: myapp
    type: front-end
spec: # specification of pod
  containers:
    - name: nginx-controller
      image: nginx
EOF

# create pod with same labels
kubectl create -f pod.yaml
# pod/myapp-pod created

# confirm, remain 3 pods
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-64qrn   1/1     Running   0          98s
# myapp-replicaset-dcrqj   1/1     Running   0          2m10s
# myapp-replicaset-kgxq2   1/1     Running   0          2m10s

# check details, event shows pod deletion
kubectl describe rs myapp-replicaset
# Name:         myapp-replicaset
# Namespace:    default
# Selector:     type=front-end
# Labels:       app=myapp
#               type=front-end
# Annotations:  <none>
# Replicas:     3 current / 3 desired
# Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
# Pod Template:
#   Labels:  app=myapp
#            type=front-end
#   Containers:
#    nginx-controller:
#     Image:         nginx
#     Port:          <none>
#     Host Port:     <none>
#     Environment:   <none>
#     Mounts:        <none>
#   Volumes:         <none>
#   Node-Selectors:  <none>
#   Tolerations:     <none>
# Events:
#   Type    Reason            Age    From                   Message
#   ----    ------            ----   ----                   -------
#   Normal  SuccessfulCreate  9m43s  replicaset-controller  Created pod: myapp-replicaset-b9w2c
#   Normal  SuccessfulCreate  9m43s  replicaset-controller  Created pod: myapp-replicaset-n44vm
#   Normal  SuccessfulCreate  9m43s  replicaset-controller  Created pod: myapp-replicaset-gj8sd
#   Normal  SuccessfulCreate  7m28s  replicaset-controller  Created pod: myapp-replicaset-hrkpg
#   Normal  SuccessfulDelete  54s    replicaset-controller  Deleted pod: myapp-pod
```

### Change replica number in temp file

- the original yaml file remain unchanged

```sh
# edit temp file
kubectl edit rs myapp-replicaset
# spec:
#   replicas: 4

# confirm
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-gj8sd   1/1     Running   0          15m
# myapp-replicaset-hrkpg   1/1     Running   0          12m
# myapp-replicaset-mg82w   1/1     Running   0          58s
# myapp-replicaset-n44vm   1/1     Running   0          15m
```

### Delete RS

```sh
kubectl delete rs myapp-replicaset
# replicaset.apps "myapp-replicaset" deleted from default namespace

kubectl get rs
# No resources found in default namespace.
```

---

## ReplcationController

- `ReplcationController`
  - the original controller (predecessor of `ReplicaSet`) that **ensures a specified number** of `Pod` replicas are running at any given time.
  - watches Pods in the cluster.
    - If a `Pod` **dies**, `ReplcationController` creates a new one.
    - If **extra** `Pods` appear, it removes them.
  - uses **label selectors** (just like ReplicaSet) to decide which Pods it manages.
- It does the **same** core job as `ReplicaSet`: maintaining a stable set of running Pods.

- Role

  - **High Availability**: keeps the application alive by ensuring the desired number of Pods.
  - **Scaling**: you can increase or decrease the replica count.
  - **Pod Replacement**: self-heals Pods that fail or are deleted.

---

- `spec.template`: the template used to define pod
- `spec.template.metadata.labels`: the label selector used to manage pods
- `spec.replicas`: the desired number of pods
- `spec.spec`: the specification of each pod

---

### Common Commands - `ReplicationControllers`

| Command                                      | Description                                                       |
| -------------------------------------------- | ----------------------------------------------------------------- |
| `kubectl get rc`                             | List all ReplicationControllers in the current namespace.         |
| `kubectl create -f yaml_file`                | Create a ReplicationController from a YAML file.                  |
| `kubectl describe rc rc_name`                | Show detailed information about a specific ReplicationController. |
| `kubectl edit rc rc_name`                    | Live edit resources                                               |
| `kubectl delete rc rc_name`                  | Delete a ReplicationController by name.                           |
| `kubectl scale rc rc_name --replicas=rc_num` | Scale the number of replicas for a ReplicationController.         |
| `kubectl rollout status rc/rc_name`          | Check the status of a rollout for the ReplicationController.      |
| `kubectl rollout history rc/rc_name`         | View the rollout history of changes to the ReplicationController. |
| `kubectl rollout undo rc/rc_name`            | Rollback to the previous version of the ReplicationController.    |
| `kubectl replace -f yaml_file`               | Replace a ReplicationController with a new one from a YAML file.  |
| `kubectl explain rc`                         | Show document of rc                                               |

---

## Lab: ReplicationController

### Create RC

- Create yaml file
- `rc-definition.yaml`

```yaml
apiVersion: v1 # v1 supports
kind: ReplicationController # specify the object kind is ReplicationController
metadata: # metadata of rc
  name: myapp-rc
  labels:
    app: myapp
    type: front-end
spec: # specification of rc
  template: # specify template, can use the pod definition
    metadata: # metadata of each pod provision by template
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec: # specification of each pod
      containers:
        - name: nginx-container
          image: nginx
  replicas: 3 # specify the number of replicas, child of rc spec
```

- Create pods

```sh
# create pod
kubectl create -f rc-definition.yaml
# replicationcontroller/myapp-rc created

# confirm rc
kubectl get rc
# NAME       DESIRED   CURRENT   READY   AGE
# myapp-rc   3         3         3       87s

# confirm
kubectl get pods
# NAME             READY   STATUS    RESTARTS      AGE
# myapp-rc-2cjhx   1/1     Running   0             16s
# myapp-rc-b2rt2   1/1     Running   0             16s
# myapp-rc-kngzb   1/1     Running   0             16s

# get details
kubectl describe rc myapp-rc
# Name:         myapp-rc
# Namespace:    default
# Selector:     app=myapp,type=front-end
# Labels:       app=myapp
#               type=front-end
# Annotations:  <none>
# Replicas:     3 current / 3 desired
# Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
# Pod Template:
#   Labels:  app=myapp
#            type=front-end
#   Containers:
#    nginx-container:
#     Image:         nginx
#     Port:          <none>
#     Host Port:     <none>
#     Environment:   <none>
#     Mounts:        <none>
#   Volumes:         <none>
#   Node-Selectors:  <none>
#   Tolerations:     <none>
# Events:
#   Type    Reason            Age   From                    Message
#   ----    ------            ----  ----                    -------
#   Normal  SuccessfulCreate  14m   replication-controller  Created pod: myapp-rc-b2rt2
#   Normal  SuccessfulCreate  14m   replication-controller  Created pod: myapp-rc-kngzb
#   Normal  SuccessfulCreate  14m   replication-controller  Created pod: myapp-rc-2cjhx
```

---

### Scale Replicas

```sh
# scale up
kubectl scale rc myapp-rc --replicas=5
# replicationcontroller/myapp-rc scaled

# confirm
kubectl get rc
# NAME       DESIRED   CURRENT   READY   AGE
# myapp-rc   5         5         5       16m

# scale down
kubectl scale rc myapp-rc --replicas=1
# replicationcontroller/myapp-rc scaled

kubectl get rc
# NAME       DESIRED   CURRENT   READY   AGE
# myapp-rc   1         1         1       17m35s

# confirm
kubectl get pods
# NAME             READY   STATUS    RESTARTS      AGE
# myapp-rc-kngzb   1/1     Running   0             18m
```

---

### Delete RC

```sh
# remove
kubectl delete rc myapp-rc
# replicationcontroller "myapp-rc" deleted from default namespace

# confirm
kubectl get rc
# No resources found in default namespace.

kubectl get pods
# No resources found in default namespace.
```

---

## Common Questions

- How many RS exits in default namespace
  - `kubectl get rs`
- How many pods are desired in the specific rs
  - `kubectl get rs`
- What is the image used in the specific rs
  - `kubectl describe rs rs_name | grep Image`
- How many pods are ready in a rs
  - `kubectl get rs`
- Why the pods are not ready
  - `kubectl describe pod pod_name`
- Delete any one of the pod
  - `kubectl delete pod pod_name`
- How many pods exist after deletion?
  - `kubectl get pods`
- Why are there still 4 pods after deletion?
  - ReplicaSet ensure the desired number of PODs always run
- Create a rs using yaml file
  - `kubectl create -f yaml_file`
  - correct the version if error.
  - use command for information `kubectl explain replicaset`
  ```yaml
  GROUP: apps
  KIND: ReplicaSet
  VERSION: v1
  ```
- Fix error in a yaml file and create rs
  - check whether the `selector`'s `matchLabels` matches with `template`'s `metadata` `labels`
- Delete specific rs
  - `kubectl delete rs rs_name`
- Update the rs using a specific image
  - `kubectl edit rs rs_name`: update temp file
  - `kubectl delete pod pod_name`: delete the old pod, rs will create new pods apply new temp file
- Scale number of pods in a rs
  - `kubectl scale rs rs_name --replicas=5`
