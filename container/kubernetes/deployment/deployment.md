# Kubernetes - Deployment

[Back](../index.md)

- [Kubernetes - Deployment](#kubernetes---deployment)
  - [Deployment](#deployment)
    - [Changing the Deployment](#changing-the-deployment)
    - [Deployment Strategies](#deployment-strategies)
    - [Common Commands](#common-commands)
    - [Lab: Create Deployment](#lab-create-deployment)
  - [Common Commands](#common-commands-1)
  - [Updates and Rollback](#updates-and-rollback)
    - [Deployment strategy](#deployment-strategy)
    - [Rollback](#rollback)
    - [Lab: Deployment Rollout and rollback](#lab-deployment-rollout-and-rollback)
    - [Lab: Rollback](#lab-rollback)
    - [Lab: With Rollout with Error](#lab-with-rollout-with-error)
  - [Common Questions](#common-questions)

---

## Deployment

- `Deployments`

  - upgraded and higher version of `replication controller`.
  - manage the **deployment** of `replica sets`.
  - have the capability to **update** the `replica set` and are also capable of **rolling back to the previous version**.

- Features
  - `matchLabels`
  - `selectors`
- `deployment controller`
  - has the capability to change the deployment midway.

---

### Changing the Deployment

- **Updating**:

  - The user can **update** the ongoing deployment **before it is completed**.
  - In this, the **existing** deployment will be **settled** and **new** deployment will be **created**.

- **Deleting**:

  - The user can **pause/cancel the deployment** by deleting it **before it is completed**.
  - **Recreating the same deployment** will resume it.

- **Rollback**
  - **roll back** the deployment or the deployment in progress.
  - The user can create or update the deployment by using `DeploymentSpec.PodTemplateSpec = oldRC.PodTemplateSpec`.

---

### Deployment Strategies

- `Deployment strategies`

  - help in **defining how the new RC should replace** the existing RC.

- **Recreate**

  - **kill all the existing RC** and then bring up the new ones.
  - This results in **quick deployment** however it will result in **downtime** when the old pods are down and the new pods have not come up.

- **Rolling Update**
  - **gradually brings down** the **old** RC and **brings up** the new one.
  - This results in **slow deployment**, however there is no deployment.
  - At all times, few **old** pods and few **new** pods are **available** in this process.

---

### Common Commands

| Command                                                    | Description                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------- |
| `kubectl get deployments`                                  | List all Deployments in the current namespace.                |
| `kubectl describe deployment <deployment>`                 | Show detailed information about a specific Deployment.        |
| `kubectl create -f <file.yaml>`                            | Create a Deployment from a YAML file.                         |
| `kubectl apply -f <file.yaml>`                             | Apply changes to a Deployment configuration from a YAML file. |
| `kubectl delete deployment <deployment>`                   | Delete a Deployment by name.                                  |
| `kubectl scale deployment <deployment> --replicas=<count>` | Scale the number of replicas for a Deployment.                |

- Rollout

| Command                                           | Description                                            |
| ------------------------------------------------- | ------------------------------------------------------ |
| `kubectl rollout status deployment/<deployment>`  | Check the status of a rollout for the Deployment.      |
| `kubectl rollout history deployment/<deployment>` | View the rollout history of changes to the Deployment. |
| `kubectl rollout undo deployment/<deployment>`    | Rollback to the previous version of the Deployment.    |

---

### Lab: Create Deployment

- deployment-def.yaml

```sh
apiVersion: apps/v1
kind: Deployment # Specify object kind
metadata:
  name: mydeploy
  labels:
    app: myapp
    type: front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      type: front-end
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-controller
          image: nginx
```

```sh
# create deployment
kubectl create -f deployment-def.yaml

kubectl get deployments
# NAME       READY   UP-TO-DATE   AVAILABLE   AGE
# mydeploy   3/3     3            3           32s

# also create rs
kubectl get rs
# NAME                  DESIRED   CURRENT   READY   AGE
# mydeploy-8544bc744c   3         3         3       117s

kubectl get pods
# NAME                        READY   STATUS    RESTARTS   AGE
# mydeploy-8544bc744c-k2scs   1/1     Running   0          2m24s
# mydeploy-8544bc744c-pzvgf   1/1     Running   0          2m24s
# mydeploy-8544bc744c-wssrt   1/1     Running   0          2m24s

kubectl get all
# NAME                            READY   STATUS    RESTARTS   AGE
# pod/mydeploy-8544bc744c-k2scs   1/1     Running   0          3m19s
# pod/mydeploy-8544bc744c-pzvgf   1/1     Running   0          3m19s
# pod/mydeploy-8544bc744c-wssrt   1/1     Running   0          3m19s

# NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   95d

# NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/mydeploy   3/3     3            3           3m19s

# NAME                                  DESIRED   CURRENT   READY   AGE
# replicaset.apps/mydeploy-8544bc744c   3         3         3       3m19s

# get details
kubectl describe deployment mydeploy
# Name:                   mydeploy
# Namespace:              default
# CreationTimestamp:      Sun, 27 Jul 2025 14:14:37 -0400
# Labels:                 app=myapp
#                         type=front-end
# Annotations:            deployment.kubernetes.io/revision: 1
# Selector:               type=front-end
# Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
# StrategyType:           RollingUpdate
# MinReadySeconds:        0
# RollingUpdateStrategy:  25% max unavailable, 25% max surge
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
# Conditions:
#   Type           Status  Reason
#   ----           ------  ------
#   Available      True    MinimumReplicasAvailable
#   Progressing    True    NewReplicaSetAvailable
# OldReplicaSets:  <none>
# NewReplicaSet:   mydeploy-8544bc744c (3/3 replicas created)
# Events:
#   Type    Reason             Age    From                   Message
#   ----    ------             ----   ----                   -------
#   Normal  ScalingReplicaSet  7m58s  deployment-controller  Scaled up replica set mydeploy-8544bc744c from 0 to 3
```

---

## Common Commands

- How many rs exist on the system?
  - `kubectl get rs`
- How many deployment exist on the system?
  - `kubectl get deployments`
- How many PODs
  - `kubectl get pods`
- Out of all the existing PODs, how many are ready?
  - `kubectl get pods`
- What is the image used to create pod in the deployment
  - `kubectl describe deployment deploy_name` / `kubectl describe pod pod_name`
- Why the deployment is not ready.
  - `kubectl describe deployment deploy_name`
  - check event
- Create a new deployemnt with a yaml file
  - `kubectl create -f yaml_file`
  - Check if the version is apps/v1
  - Check if the matchLabels match with POD labels
  - Check the case, **D**eployment, not **d**eployment
- Create a new deployment
  - opt1:
    - create yaml file
    - create deploy
  - Opt2:
    - `kubectl create deployment --help` for helping info
    - `kubectl create deployment httpd-frontend --image=httpd:2.4-alpine --replicas=3`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-frontend
  labels:
    type: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      name: httpd
      labels:
        tier: frontend
    spec:
      containers:
        - name: httpd-pod
          image: httpd:2.4-alpine
```

---

## Updates and Rollback

- Rollout and versioning

```sh
# check the status
kubectl rollout status deployment/httpd-frontend
# deployment "httpd-frontend" successfully rolled out

kubectl rollout history deployment/httpd-frontend
# deployment.apps/httpd-frontend
# REVISION  CHANGE-CAUSE
# 1         <none>
```

---

### Deployment strategy

- `Recreate Strategy`
  - Destroy all old POD and create all new POD
  - application downtime
  - When `describe`, shows scale down to 0, then scale up to replicas number
- `Rolling Update`
  - Take down and recreate POD one by one
  - Default
  - When `describe`, shows scale down and up one at a time.
  - Behind the scence:
    - Upgrade creates a new rs, then take one pod from the old rs, and bring up one pod in new rs, until all pods in old rs are down.
    - Can be verify duration deployment upgrade, `kubectl get rs`

---

- Update POD:
  - opt1:
    - change yaml file / app
    - `kubectl apply -f yaml_file`
  - opt2:
    - `kubectl set image deployment/deploy_name nginx=nginx:1.9.1`, yaml file remain upchanged

---

### Rollback

- `Rollback`
  - undo a change
  - Behind the scence:
    - Rollback creates a new rs, then take one pod from the new version rs, and bring up one pod in old rs, until all pods in new rs are down.
    - Can be verify duration deployment upgrade, `kubectl get rs`

```sh
kubectl rollout undo deployment/deploy_name
```

---

### Lab: Deployment Rollout and rollback

- Create without record

```sh
kubectl create -f deployment-def.yaml
# deployment.apps/mydeploy created

kubectl rollout status deployment/mydeploy
# Waiting for deployment "mydeploy" rollout to finish: 0 of 6 updated replicas are available...
# Waiting for deployment "mydeploy" rollout to finish: 1 of 6 updated replicas are available...
# Waiting for deployment "mydeploy" rollout to finish: 2 of 6 updated replicas are available...
# Waiting for deployment "mydeploy" rollout to finish: 3 of 6 updated replicas are available...
# Waiting for deployment "mydeploy" rollout to finish: 4 of 6 updated replicas are available...
# Waiting for deployment "mydeploy" rollout to finish: 5 of 6 updated replicas are available...
# deployment "mydeploy" successfully rolled out

kubectl rollout history deployment/mydeploy
# deployment.apps/mydeploy
# REVISION  CHANGE-CAUSE
# 1         <none>

# delete
kubectl delete deployment mydeploy
```

- create with record

```sh
kubectl create -f deployment-def.yaml --record

kubectl rollout status deployment/mydeploy
# deployment "mydeploy" successfully rolled out

kubectl rollout history deployment/mydeploy
# deployment.apps/mydeploy
# REVISION  CHANGE-CAUSE
# 1         kubectl create --filename=deployment-def.yaml --record=true
```

- Update the yaml file

```yaml
image: nginx:1.28.0
```

- update deployment

```sh
kubectl apply -f deployment-def.yaml

kubectl rollout status deployment/mydeploy
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 2 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 2 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 2 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 5 of 6 updated replicas are available...
# deployment "mydeploy" successfully rolled out

kubectl rollout history deployment/mydeploy
# REVISION  CHANGE-CAUSE
# 1         kubectl create --filename=deployment-def.yaml --record=true
# 2         kubectl create --filename=deployment-def.yaml --record=true

# confirm
kubectl describe deployment mydeploy
# Name:                   mydeploy
# Namespace:              default
# CreationTimestamp:      Sun, 27 Jul 2025 15:49:31 -0400
# Labels:                 app=myapp
#                         type=front-end
# Annotations:            deployment.kubernetes.io/revision: 2
#                         kubernetes.io/change-cause: kubectl create --filename=deployment-def.yaml --record=true
# Selector:               type=front-end
# Replicas:               6 desired | 6 updated | 6 total | 6 available | 0 unavailable
# StrategyType:           RollingUpdate
# MinReadySeconds:        0
# RollingUpdateStrategy:  25% max unavailable, 25% max surge
# Pod Template:
#   Labels:  app=myapp
#            type=front-end
#   Containers:
#    nginx-controller:
#     Image:         nginx:1.28.0
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
# OldReplicaSets:  mydeploy-8544bc744c (0/0 replicas created)
# NewReplicaSet:   mydeploy-5d87c7977b (6/6 replicas created)
# Events:
#   Type    Reason             Age                From                   Message
#   ----    ------             ----               ----                   -------
#   Normal  ScalingReplicaSet  8m44s              deployment-controller  Scaled up replica set mydeploy-8544bc744c from 0 to 6
#   Normal  ScalingReplicaSet  2m10s              deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 0 to 2
#   Normal  ScalingReplicaSet  2m10s              deployment-controller  Scaled down replica set mydeploy-8544bc744c from 6 to 5
#   Normal  ScalingReplicaSet  2m10s              deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 2 to 3
#   Normal  ScalingReplicaSet  2m1s               deployment-controller  Scaled down replica set mydeploy-8544bc744c from 5 to 4
#   Normal  ScalingReplicaSet  2m1s               deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 3 to 4
#   Normal  ScalingReplicaSet  2m                 deployment-controller  Scaled down replica set mydeploy-8544bc744c from 4 to 3
#   Normal  ScalingReplicaSet  2m                 deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 4 to 5
#   Normal  ScalingReplicaSet  2m                 deployment-controller  Scaled down replica set mydeploy-8544bc744c from 3 to 2
#   Normal  ScalingReplicaSet  116s (x3 over 2m)  deployment-controller  (combined from similar events): Scaled down replica set mydeploy-8544bc744c from 1 to 0
```

- Change the image

```sh
kubectl set image deployment/mydeploy nginx-container=nginx:1.29.0-alpine

kubectl rollout status deployment/mydeploy
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 4 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 5 out of 6 new replicas have been updated...
# Waiting for deployment "mydeploy" rollout to finish: 2 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 2 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 2 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "mydeploy" rollout to finish: 5 of 6 updated replicas are available...
# deployment "mydeploy" successfully rolled out

kubectl rollout history deployment/mydeploy
# deployment.apps/mydeploy
# REVISION  CHANGE-CAUSE
# 1         kubectl create --filename=deployment-def.yaml --record=true
# 2         kubectl create --filename=deployment-def.yaml --record=true
# 3         kubectl create --filename=deployment-def.yaml --record=true
# 4         kubectl create --filename=deployment-def.yaml --record=true
# 5         kubectl create --filename=deployment-def.yaml --record=true

kubectl describe deployment mydeploy
# Name:                   mydeploy
# Namespace:              default
# CreationTimestamp:      Sun, 27 Jul 2025 15:49:31 -0400
# Labels:                 app=myapp
#                         type=front-end
# Annotations:            deployment.kubernetes.io/revision: 5
#                         kubernetes.io/change-cause: kubectl create --filename=deployment-def.yaml --record=true
# Selector:               type=front-end
# Replicas:               6 desired | 6 updated | 6 total | 6 available | 0 unavailable
# StrategyType:           RollingUpdate
# MinReadySeconds:        0
# RollingUpdateStrategy:  25% max unavailable, 25% max surge
# Pod Template:
#   Labels:  app=myapp
#            type=front-end
#   Containers:
#    nginx-container:
#     Image:         nginx:1.29.0-alpine
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
# OldReplicaSets:  mydeploy-8544bc744c (0/0 replicas created), mydeploy-5d87c7977b (0/0 replicas created), mydeploy-665d64f479 (0/0 replicas created), mydeploy-6796f69db (0/0 replicas created)
# NewReplicaSet:   mydeploy-75db8bc54d (6/6 replicas created)
# Events:
#   Type    Reason             Age                 From                   Message
#   ----    ------             ----                ----                   -------
#   Normal  ScalingReplicaSet  18m                 deployment-controller  Scaled up replica set mydeploy-8544bc744c from 0 to 6
#   Normal  ScalingReplicaSet  12m                 deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 0 to 2
#   Normal  ScalingReplicaSet  12m                 deployment-controller  Scaled down replica set mydeploy-8544bc744c from 6 to 5
#   Normal  ScalingReplicaSet  12m                 deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 2 to 3
#   Normal  ScalingReplicaSet  11m                 deployment-controller  Scaled down replica set mydeploy-8544bc744c from 5 to 4
#   Normal  ScalingReplicaSet  11m                 deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 3 to 4
#   Normal  ScalingReplicaSet  11m                 deployment-controller  Scaled down replica set mydeploy-8544bc744c from 4 to 3
#   Normal  ScalingReplicaSet  11m                 deployment-controller  Scaled up replica set mydeploy-5d87c7977b from 4 to 5
#   Normal  ScalingReplicaSet  11m                 deployment-controller  Scaled down replica set mydeploy-8544bc744c from 3 to 2
#   Normal  ScalingReplicaSet  69s (x19 over 11m)  deployment-controller  (combined from similar events): Scaled up replica set mydeploy-75db8bc54d from 0 to 3

```

---

### Lab: Rollback

```sh
kubectl rollout undo deployment/mydeploy
# deployment.apps/mydeploy rolled back

kubectl rollout history deployment/mydeploy
# deployment.apps/mydeploy 
# REVISION  CHANGE-CAUSE
# 1         kubectl create --filename=deployment-def.yaml --record=true
# 2         kubectl create --filename=deployment-def.yaml --record=true
# 3         kubectl create --filename=deployment-def.yaml --record=true
# 5         kubectl create --filename=deployment-def.yaml --record=true
# 6         kubectl create --filename=deployment-def.yaml --record=true
```

### Lab: With Rollout with Error

- Update yaml file

```yaml
          image: nginx:1.28.0-error
```

```sh
kubectl apply -f deployment-def.yaml --record

# rollout stuck due to the error
kubectl rollout status deployment/mydeploy
# Waiting for deployment "mydeploy" rollout to finish: 3 out of 6 new replicas have been updated...
# Ctrl + C to exit

# confirm get stuck
kubectl get deployment
# NAME       READY   UP-TO-DATE   AVAILABLE   AGE
# mydeploy   5/6     3            5           29m

kubectl get pods
# NAME                        READY   STATUS             RESTARTS   AGE
# mydeploy-5ff5ff84b-ff44x    0/1     ImagePullBackOff   0          2m10s
# mydeploy-5ff5ff84b-nn5w9    0/1     ImagePullBackOff   0          2m10s
# mydeploy-5ff5ff84b-s22gb    0/1     ImagePullBackOff   0          2m10s
# mydeploy-75db8bc54d-2mmvq   1/1     Running            0          12m
# mydeploy-75db8bc54d-bjlcv   1/1     Running            0          11m
# mydeploy-75db8bc54d-fldnf   1/1     Running            0          11m
# mydeploy-75db8bc54d-vr5z5   1/1     Running            0          11m
# mydeploy-75db8bc54d-zkct5   1/1     Running            0          12m

# rollback deployment
kubectl rollout undo deployment/mydeploy
# deployment.apps/mydeploy rolled back

# confirm
kubectl get deployment
# NAME       READY   UP-TO-DATE   AVAILABLE   AGE
# mydeploy   6/6     6            6           32m

kubectl get pods
# NAME                        READY   STATUS    RESTARTS   AGE
# mydeploy-75db8bc54d-2mmvq   1/1     Running   0          15m
# mydeploy-75db8bc54d-bjlcv   1/1     Running   0          15m
# mydeploy-75db8bc54d-fldnf   1/1     Running   0          15m
# mydeploy-75db8bc54d-lccts   1/1     Running   0          37s
# mydeploy-75db8bc54d-vr5z5   1/1     Running   0          15m
# mydeploy-75db8bc54d-zkct5   1/1     Running   0          15m

kubectl rollout history deployment/mydeploy
```

---

## Common Questions

- Inspect the number of PODs in deployment
  - `kubectl get deploy`
- Image used
  - `kubectl describe deploy deploy_name`
- Identify the deloyment strategy
  - `kubectl describe deploy deploy_name`
  - StrategyType
- Update the image
  - `kubectl set image deploy deploy_name container_name=image_name`

- How many PODs can be down fo upgrade at a time. Consider the number of pods is 4
  - `kubectl describe deploy deploy_name`
  - RollingUpdateStrategy:  25% max unavailable, 25% max surge
    - only 1/4 can be taken down at a time.
    - Answer is 1
- Change the deployment strategy to **Recreate**
  - `kubect edit deploy deploy_name`
  - update the strategy, type: Recreate
  ```yaml
  strategy:
    type: Recreate
  ```