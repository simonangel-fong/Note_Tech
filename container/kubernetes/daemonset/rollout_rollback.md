# Kubernetes: DaemonSets - Rollout & Rollback

[Back](../index.md)

- [Kubernetes: DaemonSets - Rollout \& Rollback](#kubernetes-daemonsets---rollout--rollback)
  - [Imperative Command](#imperative-command)
  - [Update Strategy](#update-strategy)
  - [Update Strategy - RollingUpdate](#update-strategy---rollingupdate)
    - [Lab: Update Strategy](#lab-update-strategy)
  - [Update Strategy - OnDelete](#update-strategy---ondelete)
    - [Lab: OnDelete strategy](#lab-ondelete-strategy)

---

## Imperative Command

## Update Strategy

- When `pod template` gets updated, `ds controller` automatically deletes the old `Pods` and creates the new `pods`

- `spec.updateStrategy` field
  - `RollingUpdate`
  - `OnDelete`

---

## Update Strategy - RollingUpdate

- `RollingUpdate`:
  - default
  - Pods are replaced one by one.
  - the controller waits until the new Pod is ready before updating the Pods on the other Nodes.
  - parameters:
    - `maxSurge: 0`
      - should be zero
      - when it > 0, it allow more than one ds running on a node, which is not supported, resulting in dead lock.
    - `maxUnavailable`
      - recommended `1`;
      - only one Node is affected if the ds pod does not start.
    - `maxSurge:0;maxUnavailable>node_number`
      - act like `Recreate`; replace all ds
      - if the ds pod template has readiness probe but it fails, these parameters are ignored.

---

### Lab: Update Strategy

```yaml
# demo-ds-rollingupdate.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: demo-ds-rollingupdate
spec:
  minReadySeconds: 30
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 1
  selector:
    matchLabels:
      app: monitor
  template:
    metadata:
      labels:
        app: monitor
    spec:
      containers:
        - name: monitor
          image: busybox
          command:
            - sleep
            - infinity
```

```sh
kubectl apply -f demo-ds-rollingupdate.yaml
# daemonset.apps/demo-ds-rollingupdate created

# update image
kubectl set image ds demo-ds-rollingupdate monitor=busybox:1.36
# daemonset.apps/demo-ds-rollingupdate image updated

# confirm:
#   update one by one
#   avaiable every 30s
kubectl get ds -w
# NAME                    DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
# demo-ds-rollingupdate   2         2         2       2            2           <none>          86s
# demo-ds-rollingupdate   2         2         2       2            2           <none>          102s
# demo-ds-rollingupdate   2         2         2       0            2           <none>          102s
# demo-ds-rollingupdate   2         2         1       1            1           <none>          2m12s
# demo-ds-rollingupdate   2         2         2       1            1           <none>          2m15s
# demo-ds-rollingupdate   2         2         2       1            2           <none>          2m45s
# demo-ds-rollingupdate   2         1         1       1            1           <none>          3m16s
# demo-ds-rollingupdate   2         2         1       2            1           <none>          3m16s
# demo-ds-rollingupdate   2         2         2       2            1           <none>          3m20s
# demo-ds-rollingupdate   2         2         2       2            2           <none>          3m50s

```

---

## Update Strategy - OnDelete

- `OnDelete`:
  - performs the update in a semiautomatic way
  - `ds controller` waits for **manual Pod deletion**, and then replaces it with a new Pod
    - can replace Pods at your own pace.
  - used to update **cluster-critical** `Pods` with much more control

---

### Lab: OnDelete strategy

```yaml
# demo-ds-ondelete.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: demo-ds-ondelete
spec:
  minReadySeconds: 30
  updateStrategy:
    type: OnDelete # strategy
  selector:
    matchLabels:
      app: monitor
  template:
    metadata:
      labels:
        app: monitor
    spec:
      containers:
        - name: monitor
          image: busybox
          command:
            - sleep
            - infinity
```

```sh
kubectl apply -f demo-ds-ondelete.yaml
# daemonset.apps/demo-ds-ondelete created

kubectl get ds
# NAME               DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
# demo-ds-ondelete   2         2         2       2            2           <none>          41s

kubectl set image ds demo-ds-ondelete monitor=busybox:1.36
# daemonset.apps/demo-ds-ondelete image updated
```

> no ds get updated unless manually gets deleted

```sh
kubectl get pod
# NAME                     READY   STATUS    RESTARTS   AGE
# demo-ds-ondelete-4qvl6   1/1     Running   0          99s
# demo-ds-ondelete-wxlnm   1/1     Running   0          99s

# manually delete
kubectl delete po demo-ds-ondelete-4qvl6 --wait=false
# pod "demo-ds-ondelete-4qvl6" deleted

# confirm
kubectl get ds -w
# NAME               DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
# demo-ds-ondelete   2         2         2       2            2           <none>          96s
# demo-ds-ondelete   2         2         2       2            2           <none>          108s
# demo-ds-ondelete   2         2         2       0            2           <none>          108s
# demo-ds-ondelete   2         2         1       1            1           <none>          3m44s
# demo-ds-ondelete   2         2         2       1            1           <none>          3m48s
# demo-ds-ondelete   2         2         2       1            2           <none>          4m18s

# confirm
kubectl get pod
# NAME                     READY   STATUS    RESTARTS   AGE
# demo-ds-ondelete-bd9lg   1/1     Running   0          99s
# demo-ds-ondelete-wxlnm   1/1     Running   0          5m23s

# manually delete another one
kubectl delete po demo-ds-ondelete-wxlnm --wait=false
# pod "demo-ds-ondelete-wxlnm" deleted

# confirm
kubectl get ds -w
# NAME               DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
# demo-ds-ondelete   2         2         1       2            1           <none>          7m17s
# demo-ds-ondelete   2         2         2       2            1           <none>          7m21s
# demo-ds-ondelete   2         2         2       2            2           <none>          7m51s
```

---
