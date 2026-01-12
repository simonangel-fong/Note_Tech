# CKA - Storage

[Back](../index.md)

- [CKA - Storage](#cka---storage)
  - [PV + PVC](#pv--pvc)
    - [Task: Create a PV](#task-create-a-pv)
    - [Task: PV hostpath](#task-pv-hostpath)
    - [Task: PVC + pod mount](#task-pvc--pod-mount)
    - [Task: PVC + pod](#task-pvc--pod)
    - [Task: PVC + pod mount](#task-pvc--pod-mount-1)
    - [Task: PV + PVC](#task-pv--pvc)
  - [StorageClass](#storageclass)
    - [Task: StorageClass + PV](#task-storageclass--pv)

---

## PV + PVC

### Task: Create a PV

Create a PV name rompv with the accessmode ReadOnlyMany and a capacity of 1Gi.

---

- Solution

```yaml
# task-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: rompv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadOnlyMany
  hostPath:
    path: "/mnt/data"
```

```sh
k apply -f task-pv.yaml
# persistentvolume/rompv created

# confirm
k get pv rompv
# NAME    CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# rompv   1Gi        ROX            Retain           Available                          <unset>                          42s
```

> if pv type is not specified, use hostPath

---

### Task: PV hostpath

设置配置环境：
[candidate@node-1] $ kubectl config use-context hk8s

Task
创建名为 app-config 的 persistent volume，容量为 1Gi，访问模式为 ReadWriteMany。
volume 类型为 hostPath，位于 /srv/app-config

---

```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-config
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: "/srv/app-config"
```

```sh
kubectl apply -f pv.yaml
# persistentvolume/app-config created

kubectl get pv app-config
# NAME         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# app-config   1Gi        RWX            Retain           Available                          <unset>                          27s

kubectl describe pv app-config
# Name:            app-config
# Labels:          <none>
# Annotations:     <none>
# Finalizers:      [kubernetes.io/pv-protection]
# StorageClass:
# Status:          Available
# Claim:
# Reclaim Policy:  Retain
# Access Modes:    RWX
# VolumeMode:      Filesystem
# Capacity:        1Gi
# Node Affinity:   <none>
# Message:
# Source:
#     Type:          HostPath (bare host directory volume)
#     Path:          /srv/app-configCopy
#     HostPathType:
# Events:            <none>
```

---

### Task: PVC + pod mount

A developer needs a persistent volume for an application. Create a PersistentVolumeClaim with:
· size 100Mi
. access mode ReadWriteOnce
. using the storage class "csi-hostpath-sc" (installed)

Create a Pod that mounts this PVC at /data and verify that the volume is automatically created and mounted.

---

- Solution

- ref:
  - https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims
  - https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
  storageClassName: csi-hostpath-sc
```

```sh
kubectl apply -f pvc.yaml
# persistentvolumeclaim/task-pvc created

# confirm
kubectl get pvc task-pvc
# NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      VOLUMEATTRIBUTESCLASS   AGE
# task-pvc   Bound    pvc-92755743-039e-488b-86c0-d0a46a2ebdda   100Mi      RWO            csi-hostpath-sc   <unset>                 6m30s
```

- pod

```yaml
# pvc-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: task-pvc-pod
spec:
  volumes:
    - name: task-pvc-vol
      persistentVolumeClaim:
        claimName: task-pvc
  containers:
    - name: busybox
      image: busybox
      volumeMounts:
        - mountPath: "/data"
          name: task-pvc-vol
      command:
        - "sh"
        - "-c"
      args:
        - |
          echo "task pvc" >> /data/msg.txt;
          sleep infinity
```

```sh
kubectl apply -f pvc-pod.yaml
# pod/task-pvc-pod created

kubectl get pod task-pvc-pod
# NAME           READY   STATUS    RESTARTS   AGE
# task-pvc-pod   1/1     Running   0          36s

kubectl describe pod task-pvc-pod
# Volumes:
#   task-pvc-vol:
#     Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
#     ClaimName:  task-pvc
#     ReadOnly:   false
```

---

### Task: PVC + pod

设置配置环境：
[candidate@node-1] $ kubectl config use-context ok8s

Task
创建一个新的 PersistentVolumeClaim：
名称: pv-volume
Class: csi-hostpath-sc
容量: 10Mi

创建一个新的 Pod，来将 PersistentVolumeClaim 作为 volume 进行挂载：
名称：web-server
Image：nginx:1.16
挂载路径：/usr/share/nginx/html

配置新的 Pod，以对 volume 具有 ReadWriteOnce 权限。

最后，使用 kubectl edit 或 kubectl patch 将 PersistentVolumeClaim 的容量扩展为 70Mi，并记录此更改。

---

- Solution

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-volume
spec:
  storageClassName: csi-hostpath-sc
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
```

```sh
kubectl apply -f pvc.yaml
# persistentvolumeclaim/pv-volume created

kubectl get pvc
# NAME                 STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      VOLUMEATTRIBUTESCLASS   AGE
# pv-volume            Bound     pvc-20bb7ba7-c811-47c6-85fb-13881c9af538   10Mi       RWO            csi-hostpath-sc   <unset>                 4m
```

```yaml
# pvc-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  volumes:
    - name: pv-storage
      persistentVolumeClaim:
        claimName: pv-volume
  containers:
    - name: nginx
      image: nginx:1.16
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: pv-storage
```

```sh
kubectl apply -f pvc-pod.yaml
# pod/web-server created

kubectl get pod web-server
# NAME         READY   STATUS    RESTARTS   AGE
# web-server   1/1     Running   0          24s

kubectl describe pod web-server
# Containers:
#   nginx:
#     Mounts:
#       /usr/share/nginx/html from pv-storage (rw)
# Volumes:
#   pv-storage:
#     Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
#     ClaimName:  pv-volume
```

- update

```sh
kubectl edit pvc pv-volume --record
# spec:
#   resources:
#     requests:
#       storage: 70Mi
# persistentvolumeclaim/pv-volume edited

# confirm
kubectl get pvc pv-volume
# NAME        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      VOLUMEATTRIBUTESCLASS   AGE
# pv-volume   Bound    pvc-20bb7ba7-c811-47c6-85fb-13881c9af538   70Mi       RWO            csi-hostpath-sc   <unset>                 12m

kubectl describe pvc pv-volume
# Capacity:      70Mi
# Events:
#   Type     Reason                    Age                    From                                                                           Message
#   ----     ------                    ----                   ----                                                                           -------
#   Normal   Resizing                  26s                    external-resizer hostpath.csi.k8s.io                                           External resizer is resizing volume pvc-20bb7ba7-c811-47c6-85fb-13881c9af538
#   Normal   FileSystemResizeRequired  25s                    external-resizer hostpath.csi.k8s.io                                           Require file system resize of volume on node
```

---

### Task: PVC + pod mount

Manage persistent volumes and persistent volume claims

Task :

1. Create a PersistentVolumeClaim named rwopvc that does the following:
2. Capacity of 400Mi
3. Access mode of ReadWriteOnce
4. mount to a pod named rwopod at the mount path /var/www/html

---

- Solution

```yaml
# task-pvc02.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rwopvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 400Mi

---
apiVersion: v1
kind: Pod
metadata:
  name: rwopod
spec:
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - mountPath: "/var/www/html"
          name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: rwopvc
```

```sh
kubectl apply -f task-pvc02.yaml

k get pvc rwopvc

k describe pod rwopod
# Containers:
#   nginx:
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-cvmsd (ro)
#       /var/www/html from mypd (rw)
# Volumes:
#   mypd:
#     Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
#     ClaimName:  rwopvc
#     ReadOnly:   false
```

---

### Task: PV + PVC

Manually create a PersistentVolume that:
· is named static-pv-example
. requests 200Mi
. uses a hostPath on node01
. access mode ReadWriteOnce
. Retain reclaim policy

Then create a matching PersistentVolumeClaim (static-pvc-example) to bind to it

- Solution

```yaml
# task-03-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: static-pv-example
spec:
  capacity:
    storage: 200Mi
  accessModes:
    - ReadWriteOnce
  # policy
  persistentVolumeReclaimPolicy: Retain
  # host path
  hostPath:
    path: "/mnt/data-static" # existed path
    type: Directory
  # node affinity
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - node01
```

```sh
kubectl apply -f task-03-pv.yaml
# persistentvolume/static-pv-example created

kubectl get pv static-pv-example
# NAME                CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# static-pv-example   200Mi      RWO            Retain           Available                          <unset>                          23s
```

```yaml
# task-03-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: static-pvc-example
spec:
  volumeName: static-pv-example # specify the name
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 200Mi
```

```sh
kubectl apply -f task-03-pvc.yaml
# persistentvolumeclaim/static-pvc-example created

kubectl get pvc static-pvc-example
# NAME                 STATUS    VOLUME              CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# static-pvc-example   Pending   static-pv-example   0                         local-path     <unset>                 30s
```

---

## StorageClass

### Task: StorageClass + PV

Create a StorageClass:
. named fast-storage
. uses the rancher.io/local-path provisioner
sets a Retain reclaim policy
. uses Immediate binding (default)

Create a PersistentVolume and a PersistentVolumeClaim:
. the PV should use fast-storage
· configure node affinity so Kubernetes knows where to create the volume
. the PVC should bind to that PV
. Verify that when the PVC is deleted, the PV remains (in Released state)

---

- Solution

```yaml
# storageClass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: rancher.io/local-path
reclaimPolicy: Retain
volumeBindingMode: Immediate
```

```sh
kubectl apply -f storageClass.yaml
# storageclass.storage.k8s.io/fast-storage created
kubectl get sc fast-storage
# NAME           PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
# fast-storage   rancher.io/local-path   Retain          Immediate           false                  12s
```

```yaml
# pvc-sc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pvc-sc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Mi
  storageClassName: fast-storage
```

```sh
kubectl apply -f pvc-sc.yaml
# persistentvolumeclaim/task-pvc-sc created

kubectl get pvc task-pvc-sc
# NAME          STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# task-pvc-sc   Pending                                      fast-storage   <unset>                 3m16s
```

---
