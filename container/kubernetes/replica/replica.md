# Kubernetes - Replica

[Back](../index.md)

- [Kubernetes - Replica](#kubernetes---replica)
  - [Replication Controller(Old, Replaced by replica set)](#replication-controllerold-replaced-by-replica-set)
    - [Common Commands](#common-commands)
    - [Lab: ReplicationController](#lab-replicationcontroller)
  - [Replica Sets](#replica-sets)
    - [Method to scale number of pods in rs](#method-to-scale-number-of-pods-in-rs)
    - [Common Commands](#common-commands-1)
    - [Creating Replica Sets](#creating-replica-sets)
  - [Common Questions](#common-questions)

---

## Replication Controller(Old, Replaced by replica set)

- `Replication Controller`

  - responsible for **managing the pod lifecycle**.
  - responsible for making sure that the **specified number of pod replicas** are running **at any point of time**.
  - used in time when one wants to make sure that the **specified number** of pod or **at least one** pod is running.
  - It has the capability to **bring up or down** the specified no of pod.

- It is a best practice to use the `replication controller` to **manage the pod life cycle** rather than creating a pod again and again.

---

### Common Commands

| Command                                    | Description                                                       |
| ------------------------------------------ | ----------------------------------------------------------------- |
| `kubectl get rc`                           | List all ReplicationControllers in the current namespace.         |
| `kubectl create -f <file.yaml>`            | Create a ReplicationController from a YAML file.                  |
| `kubectl describe rc <rc>`                 | Show detailed information about a specific ReplicationController. |
| `kubectl delete rc <rc>`                   | Delete a ReplicationController by name.                           |
| `kubectl scale rc <rc> --replicas=<count>` | Scale the number of replicas for a ReplicationController.         |
| `kubectl rollout status rc/<rc>`           | Check the status of a rollout for the ReplicationController.      |
| `kubectl rollout history rc/<rc>`          | View the rollout history of changes to the ReplicationController. |
| `kubectl rollout undo rc/<rc>`             | Rollback to the previous version of the ReplicationController.    |
| `kubectl replace -f <file.yaml>`           | Replace a ReplicationController with a new one from a YAML file.  |

---

### Lab: ReplicationController

- Create yaml file

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

# confirm
kubectl get pods
# NAME             READY   STATUS    RESTARTS      AGE
# myapp-rc-2cjhx   1/1     Running   0             16s
# myapp-rc-b2rt2   1/1     Running   0             16s
# myapp-rc-kngzb   1/1     Running   0             16s

# confirm rc
kubectl get replicationcontroller
# NAME       DESIRED   CURRENT   READY   AGE
# myapp-rc   3         3         3       87s

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

- Scale number

```sh
kubectl scale rc myapp-rc --replicas=5

# confirm
kubectl get rc
# NAME       DESIRED   CURRENT   READY   AGE
# myapp-rc   5         5         5       16m

kubectl scale rc myapp-rc --replicas=1

# confirm
kubectl get pods
# NAME             READY   STATUS    RESTARTS      AGE
# myapp-rc-kngzb   1/1     Running   0             18m
```

---

- Delete

```sh
kubectl delete rc myapp-rc

# confirm
kubectl get rc
# No resources found in default namespace.

kubectl get pods
```

---

## Replica Sets

- `Replica Set` ensures **how many replica of pod** should be running.
  - It can be considered as a **replacement** of `replication controller`.
- The key difference between the `replica set` and the `replication controller` is,
  - the `replication controller` only supports **equality-based selector**
  - the `replica set` supports **set-based selector**.

---

- Benefits

  - High Availability
  - Load Balancing and scaling

- Role of rs
  - monitor the pod
    - if one pod fails, rs create a new one.
- How RS monitors multiple pods?
  - using `matchLabels` under the `selectors` to filter pods

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

### Common Commands

| Command                                    | Description                                            |
| ------------------------------------------ | ------------------------------------------------------ |
| `kubectl get rs`                           | List all ReplicaSets in the current namespace.         |
| `kubectl create -f <file.yaml>`            | Create a ReplicaSet from a YAML file.                  |
| `kubectl describe rs <rs>`                 | Show detailed information about a specific ReplicaSet. |
| `kubectl delete rs <rs>`                   | Delete a ReplicaSet by name.                           |
| `kubectl scale rs <rs> --replicas=<count>` | Scale the number of replicas for a ReplicaSet.         |
| `kubectl rollout status rs/<rs>`           | Check the status of a rollout for the ReplicaSet.      |
| `kubectl rollout history rs/<rs>`          | View the rollout history of changes to the ReplicaSet. |
| `kubectl rollout undo rs/<rs>`             | Rollback to the previous version of the ReplicaSet.    |
| `kubectl replace -f <file.yaml>`           | Replace a ReplicaSet with a new one from a YAML file.  |

---

### Creating Replica Sets

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

- Scale

```sh
kubectl scale rs myapp-replicaset --replicas=7

kubectl get rs
# NAME               DESIRED   CURRENT   READY   AGE
# myapp-replicaset   7         7         7       3m46
```

- Delete a pod to test pod auto creation

```sh
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-b9w2c   1/1     Running   0          70s
# myapp-replicaset-gj8sd   1/1     Running   0          70s
# myapp-replicaset-n44vm   1/1     Running   0          70s

# delete a pod manually
kubectl delete pod myapp-replicaset-b9w2c

# list pods
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-gj8sd   1/1     Running   0          2m24s
# myapp-replicaset-hrkpg   1/1     Running   0          9s
# myapp-replicaset-n44vm   1/1     Running   0          2m24s
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

- Create new pod manually to test rs

```sh
# create yaml
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

# create pod with same labels
kubectl create -f pod.yaml

# confirm, remain 3 pods
kubectl get pods
# NAME                     READY   STATUS    RESTARTS   AGE
# myapp-replicaset-gj8sd   1/1     Running   0          8m59s
# myapp-replicaset-hrkpg   1/1     Running   0          6m44s
# myapp-replicaset-n44vm   1/1     Running   0          8m59s

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

- Change replica number in temp file
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

- Delete

```sh
kubectl delete rs myapp-replicaset
```

---

## Common Questions

- How many RS exits in default namespace
  - `kubectl get rs`
- How many pods are desired in the specific rs
  - `kubectl get rs`
- What is the image used in the specific rs
  - `kubectl describe rs rs_name`
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
