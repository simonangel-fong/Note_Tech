# CKA - Storage

[Back](../index.md)

- [CKA - Storage](#cka---storage)
  - [PV + PVC](#pv--pvc)
    - [Task: Create a PV](#task-create-a-pv)
    - [Task: PV hostpath](#task-pv-hostpath)
    - [Task: PVC + pod mount](#task-pvc--pod-mount)
    - [Task: PVC + pod](#task-pvc--pod)
    - [Task: PVC + pod mount](#task-pvc--pod-mount-1)
    - [\*\*\*Task: PV + PVC](#task-pv--pvc)
  - [StorageClass](#storageclass)
    - [\*\*\*\*Task: StorageClass + PV](#task-storageclass--pv)
  - [Task: PVC](#task-pvc)
    - [Task: SC](#task-sc)

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
. using the storage class "local-path" (installed)

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

### \*\*\*Task: PV + PVC

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
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/static-pv
    type: DirectoryOrCreate
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

k get pv static-pv-example
# NAME                CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                        STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# static-pv-example   200Mi      RWO            Retain           Bound    default/static-pvc-example                  <unset>                          46s
```

```yaml
# task-03-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: static-pvc-example
spec:
  storageClassName: ""
  volumeName: static-pv-example
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
# NAME                 STATUS   VOLUME              CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# static-pvc-example   Bound    static-pv-example   200Mi      RWO                           <unset>                 80s
```

---

## StorageClass

### \*\*\*\*Task: StorageClass + PV

Create a StorageClass:
. named fast-storage
. uses the rancher.io/local-path provisioner
sets a Retain reclaim policy
. uses Immediate binding (default)

Create a PersistentVolume and a PersistentVolumeClaim:
. the PV should use fast-storage
· configure node affinity so Kubernetes knows where to create the volume (node01)
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
# task-sc-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: fast-storage-pv
spec:
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-storage
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/fast-storage/pv
    type: DirectoryOrCreate
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
kubectl apply -f task-sc-pv.yaml
# persistentvolume/fast-storage-pv created

kubectl get pv fast-storage-pv
# NAME              CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# fast-storage-pv   100Mi      RWO            Retain           Available           fast-storage   <unset>                          55s
```

---

```yaml
# task-sc-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: fast-storage-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-storage
  volumeName: fast-storage-pv
  resources:
    requests:
      storage: 100Mi
```

```sh
kubectl apply -f task-sc-pvc.yaml
# persistentvolumeclaim/fast-storage-pvc created

kubectl get pvc fast-storage-pvc
# NAME               STATUS   VOLUME            CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# fast-storage-pvc   Bound    fast-storage-pv   100Mi      RWO            fast-storage   <unset>                 11s
```

---

## Task: PVC

A user accidentally deleted the MariaDB Deployment in the mariadb namespace, which was configured with persistent storage. Your responsibility is to re-establish the Deployment while ensuring data is preserved by reusing the available PersistentVolume.

Task:
A PersistentVolume already exists and is retained for reuse. only one pv exist.

Create a PersistentVolumeClaim (PVC) named mariadb in the mariadb NS with the spec: Access mode ReadWriteOnce and Storage 250Mi

Edit the MariaDB Deploy file located at ~/mariadb-deploy.yaml to use PVC created in the previous step.

Apply the updated Deployment file to the cluster.

Ensure the MariaDB Deployment is running and Stable

- Create Env

```sh
ssh node02
sudo mkdir -p /mnt/data/mariadb
sudo chmod 777 /mnt/data/mariadb

ssh controlplane
kubectl create namespace mariadb

# create pv
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mariadb-pv
spec:
  capacity:
    storage: 250Mi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-path
  hostPath:
    path: /mnt/data/mariadb
EOF

kubectl get pv mariadb-pv

# Create the MariaDB deploy YAML file
cat <<'EOF' > ~/mariadb-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mariadb
  namespace: mariadb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mariadb
  template:
    metadata:
      labels:
        app: mariadb
    spec:
      containers:
      - name: mariadb
        image: mariadb:11.4
        ports:
        - containerPort: 3306
        env:
        - name: MARIADB_ROOT_PASSWORD
          value: "rootpass"
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
      volumes:
      - name: data
        # Intentionally wrong for your task: not using PVC yet
        emptyDir: {}
EOF


# “accidentally deleted”
kubectl -n mariadb delete deployment mariadb --ignore-not-found
kubectl -n mariadb delete pvc mariadb --ignore-not-found

# Confirm
kubectl -n mariadb get deploy,pods,pvc
kubectl get pv
ls -l ~/mariadb-deploy.yaml

```

---

- Solution

```sh
# get pv storageClass
kubectl get pv
# NAME         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# mariadb-pv   250Mi      RWO            Retain           Available           local-path     <unset>                          6s
```

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mariadb
  namespace: mariadb
spec:
  storageClassName: local-path # match the pv sc
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 250Mi
```

```sh


kubectl apply -f pvc.yaml
# persistentvolumeclaim/mariadb created

# confirm
kubectl get pvc mariadb -n mariadb
# NAME      STATUS   VOLUME       CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# mariadb   Bound    mariadb-pv   250Mi      RWO            local-path     <unset>                 6s

vi mariadb-deploy.yaml
# volumes:
# - name: data
#   persistentVolumeClaim:
#     claimName: mariadb

kubectl apply -f mariadb-deploy.yaml
# deployment.apps/mariadb created

kubectl get pod -n mariadb
# NAME                       READY   STATUS    RESTARTS   AGE
# mariadb-586c877688-f5bbd   1/1     Running   0          77s

kubectl describe pod mariadb-586c877688-f5bbd -n mariadb
# Containers:
#   mariadb:
#     Mounts:
#       /var/lib/mysql from data (rw)
# Volumes:
#   data:
#     Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
#     ClaimName:  mariadb
```

---

### Task: SC

Create a new StorageClass named low-latency that uses the existing provisioner rancher.io/local-path.
Set the VolumeBindingMode to WaitForFirstConsumer. (Mandatory or the score will be reduced)

Make the newly created StorageClass (low-latency) the default StorageClass in the cluster.

Do NOT modify any existing Deployments or PersistentVolumeClaims. (If modified, the-score will be reduced)

---

- Solution

```yaml
# sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: low-latency
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
```

```sh
kubectl apply -f sc.yaml
# storageclass.storage.k8s.io/low-latency created

# Mark the default StorageClass as non-default
kubectl patch sc local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
# storageclass.storage.k8s.io/local-path patched

kubectl get sc
# NAME                    PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
# local-path              rancher.io/local-path   Delete          WaitForFirstConsumer   false                  2d22h
# low-latency (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  5s
```
