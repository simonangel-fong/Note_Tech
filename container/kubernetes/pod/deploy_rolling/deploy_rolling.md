# Kubernetes - Pod: Deployment Rolling update & Rollback

[Back](../../index.md)

- [Kubernetes - Pod: Deployment Rolling update \& Rollback](#kubernetes---pod-deployment-rolling-update--rollback)
  - [Rollout \& Rollback](#rollout--rollback)
    - [How it works](#how-it-works)
    - [Deployment Strategy](#deployment-strategy)
  - [Imperative commands](#imperative-commands)
  - [Lab: Rollout \& Rollback](#lab-rollout--rollback)
    - [Upate Image - `set`](#upate-image---set)
    - [Upate Image - YAML](#upate-image---yaml)
    - [Rollback](#rollback)

---

## Rollout & Rollback

- `rollout`

  - the process of **deploying a new version** of resources.
  - Valid resource types include:
    - `deployments`
    - `daemonsets`
    - `statefulsets`

- `rollback`
  - a process of `deployment` that reverts it to a previous revision, restoring the earlier Pod template.
  - `kubectl rollout undo`

---

### How it works

- Upgrade

  - User upgrade the resources and apply
  - Deployment object follows the strategy to
    - create a new `ReplicaSet` which deploys pods of new version;
    - take down the pods of old verions in the old `ReplicaSet`

- Rollback
  - User upgrade the resources and issue `kubectl rollback undo`
  - Deployment object follows the strategy to
    - bring up the old `ReplicaSet` which deploys pods of the specific old version;
    - take down the pods of the current verions in the current `ReplicaSet`

---

### Deployment Strategy

- `Rolling Update` Strategy

  - default
  - take down and bring up pods one by one
  - no down time

- `Recreate` Strategy

  - bring down all pods before deploying new version
  - lead to application down time

- Yaml

```yaml
spec:
  strategy:
  type: Recreate
```

---

## Imperative commands

| CMD                                                                        | DESC                                 |
| -------------------------------------------------------------------------- | ------------------------------------ |
| `kubectl set image deploy deploy_name con_name=new_image`                  | update deployment image              |
| `kubectl apply -f yaml_file`                                               | update a deployment                  |
| `kubectl rollout status resource_type resource_name`                       | Show the status of the rollout       |
| `kubectl rollout history resource_type resource_name`                      | View rollout history                 |
| `kubectl rollout restart resource_type resource_name --selector=app=nginx` | Restart a resource with label        |
| `kubectl rollout resume resource_type resource_name`                       | Resume a paused resource             |
| `kubectl rollout pause resource_type resource_name`                        | Mark the provided resource as paused |
| `kubectl rollout undo resource_type resource_name`                         | Rollback to the previous version     |

---

## Lab: Rollout & Rollback

- `myapp-deploy.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: myapp
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - image: nginx:1.21
          name: nginx
```

- Create deployment

```sh
# create deployment
kubectl create -f myapp-deploy.yaml
# deployment.apps/myapp created

# confirm
kubectl rollout status deploy myapp
# Waiting for deployment "myapp" rollout to finish: 0 of 2 updated replicas are available...
# Waiting for deployment "myapp" rollout to finish: 1 of 2 updated replicas are available...
# deployment "myapp" successfully rolled out

kubectl get deploy -o wide
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES       SELECTOR
# myapp   2/2     2            2           26s   nginx        nginx:1.21   app=myapp

kubectl rollout history deploy myapp
# deployment.apps/myapp
# REVISION  CHANGE-CAUSE
# 1         <none>
```

---

### Upate Image - `set`

- Update nginx version 1.22.0 with `set`

```sh
# set image
kubectl set image deploy myapp nginx=nginx:1.22.0
# deployment.apps/myapp image updated

kubectl rollout status deploy myapp
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# deployment "myapp" successfully rolled out

kubectl get deploy -o wide
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES         SELECTOR
# myapp   2/2     2            2           81s   nginx        nginx:1.22.0   app=myapp

kubectl rollout history deploy myapp
# deployment.apps/myapp
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>
```

---

### Upate Image - YAML

- Update image nginx:1.23.0
  - Warning message due to different definition files.

```sh
# update:
kubectl apply -f myapp-deploy.yaml
# Warning: resource deployments/myapp is missing the kubectl.kubernetes.io/last-applied-configuration annotation which is required by kubectl apply. kubectl apply should only be used on resources created declaratively by either kubectl create --save-config or kubectl apply. The missing annotation will be patched automatically.
# deployment.apps/myapp configured

kubectl rollout status deploy myapp
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# deployment "myapp" successfully rolled out

kubectl get deploy -o wide
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES       SELECTOR
# myapp   2/2     2            2           4m11s   nginx        nginx:1.23   app=myapp

kubectl rollout history deploy myapp
# deployment.apps/myapp
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>
# 3         <none>
```

---

### Rollback

- rollback the last version

```sh
# rollback the last version
kubectl rollout undo deploy myapp
# deployment.apps/myapp rolled back

kubectl rollout status deploy myapp
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# deployment "myapp" successfully rolled out

kubectl get deploy -o wide
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES         SELECTOR
# myapp   2/2     2            2           6m22s   nginx        nginx:1.22.0   app=myapp

# the previous 2 version become 4
kubectl rollout history deploy myapp
# deployment.apps/myapp
# REVISION  CHANGE-CAUSE
# 1         <none>
# 3         <none>
# 4         <none>
```

- Rollback to the first version

```sh
# rollback to 1st version
kubectl rollout undo deploy myapp --to-revision=1
# deployment.apps/myapp rolled back

kubectl rollout status deploy myapp
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 out of 2 new replicas have been updated...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "myapp" rollout to finish: 1 old replicas are pending termination...
# deployment "myapp" successfully rolled out

kubectl get deploy -o wide
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES       SELECTOR
# myapp   2/2     2            2           12m   nginx        nginx:1.21   app=myapp

kubectl rollout history deploy myapp
# deployment.apps/myapp
# REVISION  CHANGE-CAUSE
# 3         <none>
# 4         <none>
# 5         <none>
```

---

```sh
kubectl describe deploy myapp
# Name:                   myapp
# Namespace:              default
# CreationTimestamp:      Mon, 27 Oct 2025 23:13:57 -0400
# Labels:                 app=myapp
# Annotations:            deployment.kubernetes.io/revision: 5
# Selector:               app=myapp
# Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
# StrategyType:           RollingUpdate
# MinReadySeconds:        0
# RollingUpdateStrategy:  25% max unavailable, 25% max surge
# Pod Template:
#   Labels:  app=myapp
#   Containers:
#    nginx:
#     Image:         nginx:1.21
#     Port:          <none>
#     Host Port:     <none>
#     Environment:   <none>
#     Mounts:        <none>
#   Volumes:         <none>
#   Node-Selectors:  <none>
#   Tolerations:     <none>
# Conditions:
#   Type           Status  Reason
#   ----           ------  ------
#   Available      True    MinimumReplicasAvailable
#   Progressing    True    NewReplicaSetAvailable
# OldReplicaSets:  myapp-5996b49c6d (0/0 replicas created), myapp-68f46dbb95 (0/0 replicas created)
# NewReplicaSet:   myapp-8dfbbd9bf (2/2 replicas created)
# Events:
#   Type    Reason             Age                From                   Message
#   ----    ------             ----               ----                   -------
#   Normal  ScalingReplicaSet  36m                deployment-controller  Scaled up replica set myapp-8dfbbd9bf from 0 to 2
#   Normal  ScalingReplicaSet  36m                deployment-controller  Scaled down replica set myapp-8dfbbd9bf from 2 to 1
#   Normal  ScalingReplicaSet  36m                deployment-controller  Scaled down replica set myapp-8dfbbd9bf from 1 to 0
#   Normal  ScalingReplicaSet  34m                deployment-controller  Scaled up replica set myapp-68f46dbb95 from 0 to 1
#   Normal  ScalingReplicaSet  33m                deployment-controller  Scaled up replica set myapp-68f46dbb95 from 1 to 2
#   Normal  ScalingReplicaSet  33m                deployment-controller  Scaled down replica set myapp-5996b49c6d from 1 to 0
#   Normal  ScalingReplicaSet  31m (x2 over 36m)  deployment-controller  Scaled up replica set myapp-5996b49c6d from 0 to 1
#   Normal  ScalingReplicaSet  31m (x2 over 36m)  deployment-controller  Scaled up replica set myapp-5996b49c6d from 1 to 2
#   Normal  ScalingReplicaSet  24m (x2 over 33m)  deployment-controller  Scaled down replica set myapp-5996b49c6d from 2 to 1
#   Normal  ScalingReplicaSet  24m (x5 over 31m)  deployment-controller  (combined from similar events): Scaled down replica set myapp-5996b49c6d from 1 to 0
```

> StrategyType: RollingUpdate
> Message: Scale up and down one at a time
