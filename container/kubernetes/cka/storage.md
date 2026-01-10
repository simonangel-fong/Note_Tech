# CKA - Storage

[Back](../index.md)

- [CKA - Storage](#cka---storage)
  - [PVC](#pvc)
    - [TASK PVC](#task-pvc)
      - [Solution](#solution)
    - [TASK 2: StorageClass](#task-2-storageclass)
    - [Solution](#solution-1)
    - [TASK 3: STORAGE](#task-3-storage)
      - [Solution](#solution-2)

---

## PVC

### TASK PVC

A developer needs a persistent volume for an application. Create a PersistentVolumeClaim with:
· size 100Mi
. access mode ReadWriteOnce
. using the storage class "csi-hostpath-sc" (installed)

Create a Pod that mounts this PVC at /data and verify that the volume is automatically created and mounted.

---

#### Solution

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

### TASK 2: StorageClass

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

### Solution

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

### TASK 3: STORAGE

Manually create a PersistentVolume that:
· is named static-pv-example
. requests 200Mi
. uses a hostPath on node01
. access mode ReadWriteOnce
. Retain reclaim policy

Then create a matching PersistentVolumeClaim (static-pvc-example) to bind to it

#### Solution

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
    path: "/mnt/data-static"  # existed path
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