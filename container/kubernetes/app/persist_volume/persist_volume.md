# Kubernetes - Application: Persistent Storage

[Back](../../index.md)

- [Kubernetes - Application: Persistent Storage](#kubernetes---application-persistent-storage)
  - [Persistent Volume (PV)](#persistent-volume-pv)
    - [Lab: Create a Persistent Volume](#lab-create-a-persistent-volume)
  - [persistent volume claims(PVC)](#persistent-volume-claimspvc)
  - [Liftcycle: PV \& PVC](#liftcycle-pv--pvc)
    - [Lab: Create PVC](#lab-create-pvc)
    - [Lab: mount to a pod](#lab-mount-to-a-pod)
      - [Survive from pod restart](#survive-from-pod-restart)
    - [Lab: Delete PVC](#lab-delete-pvc)
    - [Lab: Recreate PV, PVC, and pod](#lab-recreate-pv-pvc-and-pod)
    - [Lab: Delete PVC in use](#lab-delete-pvc-in-use)
    - [Lab: Delete PV in use](#lab-delete-pv-in-use)
    - [Lab: Share PV with multiple pods](#lab-share-pv-with-multiple-pods)
    - [Lab: Create Custom SC with parameters(skip)](#lab-create-custom-sc-with-parametersskip)
  - [Node Local Persistent Volume](#node-local-persistent-volume)
    - [Lab: Node Local PV](#lab-node-local-pv)

---

## Persistent Volume (PV)

- `Persistent Volume (PV)`

  - an API object that represents a piece of **storage** in the cluster, provisioned by an administrator or dynamically via `Storage Classes`.
  - object **stores the information** about the **underlying storage**

- A `PersistentVolume` object represents a portion of the **disk space** that is available to applications within the cluster.

  - decouples this information from the pod.

- Manged by `cluster admin`

- Feature

  - **lifecycle**:
    - **Independent** of the **pod's existence**
  - **Data Persistence**
    - Data is **retained** even after the consuming pod is **deleted**.
  - **Scope**
    - A **cluster**-wide resource
  - can be attached to **multiple** `pods` simultaneously,

- If the `volume` has **already been used** and might **contain data**, it should be erased before another user claims the volume.
  - therefore, the status become `RELEASED` when the pvc is deleteed.
  - Should be removed by using `kubectl delete pv`
- deleting the `pv` object is equivalent to deleting a **data pointer**.
  - Creating the same `pv` object is equivalent to Recreating the data point
  - the stored data remains.

---

- Deletion of a `PV` in used
  - the deletion is blocked.
  - fix by delete underlying `PVC`

---

- `accessModes` field:

  - determines how many nodes, not pods, can attach the volume at a time
    - Even if a `volume` can only be attached to a **single** `node`, it can be mounted in **many pods** if they all run on that **single node**.
  - values:
    - `ReadWriteOnce`/`RWO`
      - can be mounted by a **single** `worker node` in `read/write` mode.
      - While it’s mounted to the node, other nodes **can’t mount** the volume.
    - `ReadWriteMany`/`RWX`
      - can be mounted in `read/write` mode on **multiple** `worker nodes` at the same time.
    - `ReadOnlyMany`/`ROX`
      - can be mounted on **multiple** `worker nodes` simultaneously in `read-only` mode.

- `persistentVolumeReclaimPolicy` field:

  - `Retain`
    - default policy
    - the PV retains when it is released.
  - `Delete`

    - the **underlying storage** are automatically **deleted** upon release.
    - efault policy for `dynamically provisioned persistent volumes`

  - if a PV is released and the policy changes from `Retain` to `Delete`
    - underlying storage will be **deleted immediately**

---

- ## `volumeMode` field:

---

### Lab: Create a Persistent Volume

- Explain

```sh
kubectl explain pv.spec.hostPath
# KIND:       PersistentVolume
# VERSION:    v1

# FIELD: hostPath <HostPathVolumeSource>


# DESCRIPTION:
#     hostPath represents a directory on the host. Provisioned by a developer or
#     tester. This is useful for single-node development and testing only! On-host
#     storage is not supported in any way and WILL NOT WORK in a multi-node
#     cluster. More info:
#     https://kubernetes.io/docs/concepts/storage/volumes#hostpath
#     Represents a host path mapped into a pod. Host path volumes do not support
#     ownership management or SELinux relabeling.

# FIELDS:
#   path  <string> -required-
#     path of the directory on the host. If the path is a symlink, it will follow
#     the link to the real path. More info:
#     https://kubernetes.io/docs/concepts/storage/volumes#hostpath

#   type  <string>
#   enum: "", BlockDevice, CharDevice, Directory, ....
#     type for HostPath Volume Defaults to "" More info:
#     https://kubernetes.io/docs/concepts/storage/volumes#hostpath

#     Possible enum values:
#      - `""` For backwards compatible, leave it empty if unset
#      - `"BlockDevice"` A block device must exist at the given path
#      - `"CharDevice"` A character device must exist at the given path
#      - `"Directory"` A directory must exist at the given path
#      - `"DirectoryOrCreate"` If nothing exists at the given path, an empty
#     directory will be created there as needed with file mode 0755, having the
#     same group and ownership with Kubelet.
#      - `"File"` A file must exist at the given path
#      - `"FileOrCreate"` If nothing exists at the given path, an empty file will
#     be created there as needed with file mode 0644, having the same group and
#     ownership with Kubelet.
#      - `"Socket"` A UNIX socket must exist at the given path
```

- PV

```yaml
# demo-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: demo-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    # - ReadWriteOnce
    - ReadWriteMany
    - ReadOnlyMany
  hostPath:
    path: /var/demo-pv # directory in the worker node’s filesystem
```

```sh
kubectl apply -f demo-pv.yaml
# persistentvolume/demo-pv created

kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Available                          <unset>                          20s

kubectl get pv -o wide
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE   VOLUMEMODE
# demo-pv   1Gi        RWO,ROX        Retain           Available                          <unset>                          62s   Filesystem

kubectl describe pv demo-pv
# Name:            demo-pv
# Labels:          <none>
# Annotations:     pv.kubernetes.io/bound-by-controller: yes
# Finalizers:      [kubernetes.io/pv-protection]
# StorageClass:
# Status:          Bound
# Claim:           default/demo-pvc
# Reclaim Policy:  Retain
# Access Modes:    RWO,ROX
# VolumeMode:      Filesystem
# Capacity:        1Gi
# Node Affinity:   <none>
# Message:
# Source:
#     Type:          HostPath (bare host directory volume)
#     Path:          /var/demo-pv
#     HostPathType:
# Events:            <none>
```

---

## persistent volume claims(PVC)

- `persistent volume claims(PVC)`

  - the object represents **application request for storage** that is the persistent volume
  - the ownership of the persistent volume
    - lifecycle not tied to a pod
      - Created before a pod use the `persistent volume`
      - Remain the ownership after pod deletion.
      - release volume when pvc delete.

- Multiple `pod` across the nodes can reference to the one `PVC`

- Benefits of using PV + PVC

  - the **infrastructure-specific details** are now **decoupled** from the application represented by the `pod`.
    - cluster admin create the `PersistentVolume` objects with all their **infrastructure-related low-level details**.
    - software developers focus solely on describing the applications and their needs via the `Pod` and `PersistentVolumeClaim` objects.
      - only needs to know the `pv` name

- Managed by the `app dev`

- with `persistentVolume`
  - By claiming the `persistent volume`, the `pods` now have the **exclusive right** to use the `volume`.
  - **No one** else can claim it until it is released by deleting the `PersistentVolumeClaim` object.

---

- The deletion of `PVC` in use
  - Status stays `Terminating`
  - the pod **stays running**.
  - fix: delete the underlying pod

---

- `volumeName` field:
  - the name of persistent volume
  - if empty, k8s **randomly choose one** of the persistent volumes whose capacity and access modes match the claim
- `volumeMode` field:
  - defines what type of volume is required by the claim.
  - default: `Filesystem`

---

## Liftcycle: PV & PVC

![pic](./pic/lifecycle.png)

- `underlying volume`

  - created beforehand
  - e.g., device, nfs

- Mannually provisioned `PV` status

  - `Available`: Created/Recreated
  - `Bound`: a PVC created
  - `Released`: PVC deleted
  - manually provisioned `persistent volumes` is **decoupled** with `underlying volume`

- `PVC`:

  - `Pending`: When created, befor bound to a PV
  - `Bound`: Bound to a PV

- If the PVC policy == `Delete`:
  - PVC, PV, and underlying volumes are deleted.

---

### Lab: Create PVC

```sh
kubectl explain pvc.spec
# KIND:       PersistentVolumeClaim
# VERSION:    v1

# FIELD: spec <PersistentVolumeClaimSpec>


# DESCRIPTION:
#     spec defines the desired characteristics of a volume requested by a pod
#     author. More info:
#     https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims
#     PersistentVolumeClaimSpec describes the common attributes of storage devices
#     and allows a Source for provider-specific attributes

# FIELDS:
#   accessModes   <[]string>
#     accessModes contains the desired access modes the volume should have. More
#     info:
#     https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1

#   dataSource    <TypedLocalObjectReference>
#     dataSource field can be used to specify either: * An existing VolumeSnapshot
#     object (snapshot.storage.k8s.io/VolumeSnapshot) * An existing PVC
#     (PersistentVolumeClaim) If the provisioner or an external controller can
#     support the specified data source, it will create a new volume based on the
#     contents of the specified data source. When the AnyVolumeDataSource feature
#     gate is enabled, dataSource contents will be copied to dataSourceRef, and
#     dataSourceRef contents will be copied to dataSource when
#     dataSourceRef.namespace is not specified. If the namespace is specified,
#     then dataSourceRef will not be copied to dataSource.

#   dataSourceRef <TypedObjectReference>
#     dataSourceRef specifies the object from which to populate the volume with
#     data, if a non-empty volume is desired. This may be any object from a
#     non-empty API group (non core object) or a PersistentVolumeClaim object.
#     When this field is specified, volume binding will only succeed if the type
#     of the specified object matches some installed volume populator or dynamic
#     provisioner. This field will replace the functionality of the dataSource
#     field and as such if both fields are non-empty, they must have the same
#     value. For backwards compatibility, when namespace isn't specified in
#     dataSourceRef, both fields (dataSource and dataSourceRef) will be set to the
#     same value automatically if one of them is empty and the other is non-empty.
#     When namespace is specified in dataSourceRef, dataSource isn't set to the
#     same value and must be empty. There are three important differences between
#     dataSource and dataSourceRef: * While dataSource only allows two specific
#     types of objects, dataSourceRef
#       allows any non-core object, as well as PersistentVolumeClaim objects.
#     * While dataSource ignores disallowed values (dropping them), dataSourceRef
#       preserves all values, and generates an error if a disallowed value is
#       specified.
#     * While dataSource only allows local objects, dataSourceRef allows objects
#       in any namespaces.
#     (Beta) Using this field requires the AnyVolumeDataSource feature gate to be
#     enabled. (Alpha) Using the namespace field of dataSourceRef requires the
#     CrossNamespaceVolumeDataSource feature gate to be enabled.

#   resources     <VolumeResourceRequirements>
#     resources represents the minimum resources the volume should have. If
#     RecoverVolumeExpansionFailure feature is enabled users are allowed to
#     specify resource requirements that are lower than previous value but must
#     still be higher than capacity recorded in the status field of the claim.
#     More info:
#     https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources

#   selector      <LabelSelector>
#     selector is a label query over volumes to consider for binding.

#   storageClassName      <string>
#     storageClassName is the name of the StorageClass required by the claim. More
#     info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1

#   volumeAttributesClassName     <string>
#     volumeAttributesClassName may be used to set the VolumeAttributesClass used
#     by this claim. If specified, the CSI driver will create or update the volume
#     with the attributes defined in the corresponding VolumeAttributesClass. This
#     has a different purpose than storageClassName, it can be changed after the
#     claim is created. An empty string or nil value indicates that no
#     VolumeAttributesClass will be applied to the claim. If the claim enters an
#     Infeasible error state, this field can be reset to its previous value
#     (including nil) to cancel the modification. If the resource referred to by
#     volumeAttributesClass does not exist, this PersistentVolumeClaim will be set
#     to a Pending state, as reflected by the modifyVolumeStatus field, until such
#     as a resource exists. More info:
#     https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/

#   volumeMode    <string>
#   enum: Block, Filesystem
#     volumeMode defines what type of volume is required by the claim. Value of
#     Filesystem is implied when not included in claim spec.

#     Possible enum values:
#      - `"Block"` means the volume will not be formatted with a filesystem and
#     will remain a raw block device.
#      - `"Filesystem"` means the volume will be or is formatted with a
#     filesystem.

#   volumeName    <string>
#     volumeName is the binding reference to the PersistentVolume backing this
#     claim.

```

```yaml
# demo-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
    # - ReadWriteMany
  storageClassName: ""
  volumeName: demo-pv
```

```sh
kubectl apply -f demo-pvc.yaml
# persistentvolumeclaim/demo-pvc created

# confirm pvc bound
kubectl get pvc
# NAME       STATUS   VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-pvc   Bound    demo-pv   1Gi        RWO,ROX                       <unset>                 88s

kubectl get pvc -o wide
# NAME       STATUS   VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE    VOLUMEMODE
# demo-pvc   Bound    demo-pv   1Gi        RWO,ROX                       <unset>                 2m7s   Filesystem

kubectl describe pvc demo-pvc
# Name:          demo-pvc
# Namespace:     default
# StorageClass:
# Status:        Bound
# Volume:        demo-pv
# Labels:        <none>
# Annotations:   pv.kubernetes.io/bind-completed: yes
# Finalizers:    [kubernetes.io/pvc-protection]
# Capacity:      1Gi
# Access Modes:  RWO,ROX
# VolumeMode:    Filesystem
# Used By:       <none>
# Events:        <none>
```

- confirm pv status bound

```sh
kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM              STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Bound    default/demo-pvc                  <unset>                          76m
```

---

### Lab: mount to a pod

- Mount a pod

```yaml
# demo-pod-pvc.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod-pvc
spec:
  volumes:
    - name: db # volume name
      persistentVolumeClaim:
        claimName: demo-pvc # pvc name
  containers:
    - name: nginx
      image: nginx
      ports:
        - name: http
          containerPort: 80
    - name: mongo
      image: mongo
      volumeMounts:
        - name: db # volume name
          mountPath: /data/db
```

```sh
kubectl apply -f demo-pod-pvc.yaml
# pod/demo-pod-pvc created

# confirm
kubectl get pod/demo-pod-pvc
# NAME           READY   STATUS    RESTARTS   AGE
# demo-pod-pvc   2/2     Running   0          46s

kubectl describe pod/demo-pod-pvc
# Volumes:
#   db:
#     Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
#     ClaimName:  demo-pvc
#     ReadOnly:   false
```

- Insert data

```sh
# insert data
kubectl exec -it demo-pod-pvc -c mongo -- mongosh -eval "db.telemetry.insertOne({device_id: 1, x: 1, y: 2});"
# {
#   acknowledged: true,
#   insertedId: ObjectId('694c3fe4487ac8f7fb8de666')
# }

kubectl exec -it demo-pod-pvc -c mongo -- mongosh -eval "db.telemetry.find()"
# [
#   {
#     _id: ObjectId('694c3fe4487ac8f7fb8de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]
```

---

#### Survive from pod restart

```sh
# Delete Pod
kubectl delete pod demo-pod-pvc
# pod "demo-pod-pvc" deleted from default namespace

kubectl get pvc
# NAME       STATUS   VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-pvc   Bound    demo-pv   1Gi        RWO,ROX                       <unset>                 85m

kubectl apply -f demo-pod-pvc.yaml
# pod/demo-pod-pvc created

# confirm
kubectl exec -it demo-pod-pvc -c mongo -- mongosh -eval "db.telemetry.find()"
# [
#   {
#     _id: ObjectId('694c3fe4487ac8f7fb8de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]
```

---

### Lab: Delete PVC

```sh
kubectl delete pod demo-pod-pvc
# pod "demo-pod-pvc" deleted from default namespace

kubectl delete pvc demo-pvc
# persistentvolumeclaim "demo-pvc" deleted from default namespace
```

- recreate pvc

```sh
kubectl apply -f demo-pvc.yaml
# persistentvolumeclaim/demo-pvc created

# confirm pv: released status
kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM              STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Released   default/demo-pvc                  <unset>                          70s

# confirm status: pending
kubectl get pvc
# NAME       STATUS    VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-pvc   Pending   demo-pv   0                                        <unset>                 36s
```

- Delete PVC and PV

```sh
kubectl delete pvc demo-pvc
# persistentvolumeclaim "demo-pvc" deleted from default namespace

kubectl delete pv demo-pv
# persistentvolume "demo-pv" deleted
```

---

### Lab: Recreate PV, PVC, and pod

```sh
kubectl apply -f demo-pv.yaml
# persistentvolume/demo-pv created

kubectl apply -f demo-pvc.yaml
# persistentvolumeclaim/demo-pvc created

# confirm
kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM              STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Bound    default/demo-pvc                  <unset>                          41s

kubectl get pvc
# NAME       STATUS   VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-pvc   Bound    demo-pv   1Gi        RWO,ROX                       <unset>                 35s

# create pod
kubectl apply -f demo-pod-pvc.yaml
# pod/demo-pod-pvc created

# confirm data
kubectl exec -it demo-pod-pvc -c mongo -- mongosh -eval "db.telemetry.find()"
# [
#   {
#     _id: ObjectId('694c3fe4487ac8f7fb8de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]
```

> deletion of pv, pvc will not remove the stored ddata.

---

### Lab: Delete PVC in use

```sh
kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM              STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Bound    default/demo-pvc                  <unset>                          21m

kubectl get pvc
# NAME       STATUS   VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-pvc   Bound    demo-pv   1Gi        RWO,ROX                       <unset>                 21m

kubectl get pod
# NAME           READY   STATUS    RESTARTS   AGE
# demo-pod-pvc   2/2     Running   0          19m

# delete pvc
kubectl delete pvc demo-pvc
# persistentvolumeclaim "demo-pvc" deleted from default namespace

# pvc status: pending
kubectl get pvc
# NAME       STATUS        VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-pvc   Terminating   demo-pv   1Gi        RWO,ROX                       <unset>                 22m

# ========== fix ============

# delete pod
kubectl delete pod demo-pod-pvc
# pod "demo-pod-pvc" deleted from default namespace

# confirm
kubectl get pvc
# No resources found in default namespace.

kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM              STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Released   default/demo-pvc                  <unset>                          25m
```

---

### Lab: Delete PV in use

```sh
# recreate pvc
kubectl apply -f demo-pv.yaml
# recreate pv
kubectl apply -f demo-pvc.yaml
# persistentvolumeclaim/demo-pvc created

kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM              STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Bound    default/demo-pvc                  <unset>                          14s
kubectl get pvc
# NAME       STATUS   VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-pvc   Bound    demo-pv   1Gi        RWO,ROX                       <unset>                 22s

#  delete pv in use: get stuck
kubectl delete pv demo-pv
# persistentvolume "demo-pv" deleted

kubectl get pv
# NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS        CLAIM              STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pv   1Gi        RWO,ROX        Retain           Terminating   default/demo-pvc                  <unset>                          85s

# ======== fix ========

# remove pvc
kubectl delete pvc demo-pvc
# persistentvolumeclaim "demo-pvc" deleted from default namespace

# confirm
kubectl get pv
# No resources found
```

---

### Lab: Share PV with multiple pods

```yaml
# demo-share-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: demo-share-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
    - ReadOnlyMany
  hostPath:
    path: /var/demo-share-pv # directory in the worker node’s filesystem
```

```yaml
# demo-share-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-share-pvc
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
    # - ReadWriteMany
  storageClassName: ""
  volumeName: demo-share-pv
```

```yaml
# demo-pod-share-pvc-writer.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod-share-pvc-writer
spec:
  volumes:
    - name: share-data
      persistentVolumeClaim:
        claimName: demo-share-pvc
  containers:
    - name: writer
      image: busybox
      command:
        - sh
        - -c
        - |
          while true; do
            echo "<h1>Hello from the data writer container!$(date)</h1>" > /share/index.html;
            sleep 1;
          done
      volumeMounts:
        - name: share-data
          mountPath: /share
```

```yaml
# demo-pod-share-pvc-nginx.yaml
apiVersion: v1
kind: Pod
metadata:
  generateName: demo-pod-share-pvc-nginx
spec:
  volumes:
    - name: share-data
      persistentVolumeClaim:
        claimName: demo-share-pvc
        readOnly: true
  containers:
    - name: nginx
      image: nginx:alpine
      volumeMounts:
        - name: share-data
          mountPath: /usr/share/nginx/html
      ports:
        - containerPort: 80
```

```sh
kubectl apply -f demo-share-pv.yaml
# persistentvolume/demo-share-pv created

kubectl get pv
# NAME            CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                    STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-share-pv   1Gi        RWO,ROX        Retain           Bound    default/demo-share-pvc                  <unset>                          75s

kubectl apply -f demo-share-pvc.yaml
# persistentvolumeclaim/demo-share-pvc created

kubectl get pvc
# NAME             STATUS   VOLUME          CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# demo-share-pvc   Bound    demo-share-pv   1Gi        RWO,ROX                       <unset>                 23s

kubectl apply -f demo-pod-share-pvc-writer.yaml
# pod/demo-pod-share-pvc-writer created

kubectl create -f demo-pod-share-pvc-nginx.yaml
# pod/demo-pod-share-pvc-nginx created

kubectl get pod
# NAME                        READY   STATUS    RESTARTS   AGE
# demo-pod-share-pvc-nginx    1/1     Running   0          13s
# demo-pod-share-pvc-writer   1/1     Running   0          117s

kubectl port-forward demo-pod-share-pvc-nginx 8080:80
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

curl http://localhost:8080/
# <h1>Hello from the data writer container!Wed Dec 24 23:07:24 UTC 2025</h1>
```

---


### Lab: Create Custom SC with parameters(skip)

---

## Node Local Persistent Volume

- `Local persistent volumes`

  - Kubernetes scheduler ensures that the pod is always scheduled on the node to which the local volume is attached.

- Use `PersistentVolume.spec.nodeAffinity` feature to schedule pod to a node

---

---


```sh
tee pv-std.yaml<<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-std
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  hostPath:
    path: "/data"
EOF

kubectl apply -f pv-std.yaml
# persistentvolume/pv-std created

kubectl get pv
# NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# pv-std   1Gi        RWO            Retain           Available           standard       <unset>                          13s







tee sc-std.yaml<<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF

kubectl apply -f sc-std.yaml
# storageclass.storage.k8s.io/standard created

kubectl get sc
# NAME                   PROVISIONER                    RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
# local-path (default)   rancher.io/local-path          Delete          WaitForFirstConsumer   false                  68m
# standard               kubernetes.io/no-provisioner   Delete          WaitForFirstConsumer   false                  17s



tee pvc-std.yaml<<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-std
spec:
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi
  accessModes:
  - ReadWriteOnce
EOF

kubectl apply -f pvc-std.yaml
# persistentvolumeclaim/pvc-std created


kubectl get pvc
# NAME      STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# pvc-std   Pending                                      standard       <unset>                 40s




tee pod-writer.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  generateName: pod-writer-
spec:
  volumes:
    - name: share-data
      persistentVolumeClaim:
        claimName: pvc-std
  containers:
    - name: writer
      image: busybox
      command:
        - sh
        - -c
        - |
          while true; do
            echo "<h1>Hello from the data writer container!$(date)</h1>" > /share/index.html;
            sleep 1;
          done
      volumeMounts:
        - name: share-data
          mountPath: /share
EOF

kubectl create -f pod-writer.yaml
# pod/pod-writer-mlhfw created
kubectl create -f pod-writer.yaml
# pod/pod-writer-9frng created
kubectl create -f pod-writer.yaml
# pod/pod-writer-25qm5 created

kubectl get pod -o wide | grep pod-writer
# pod-writer-25qm5   1/1     Running   0          91s   10.244.1.10   node01   <none>           <none>
# pod-writer-9frng   1/1     Running   0          93s   10.244.2.12   node02   <none>           <none>
# pod-writer-mlhfw   1/1     Running   0          94s   10.244.1.9    node01   <none>           <none>

kubectl get pvc
# NAME      STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# pvc-std   Bound    pv-std   1Gi        RWO            standard       <unset>                 103s

kubectl get pod pod-writer -o wide
# NAME         READY   STATUS    RESTARTS   AGE     IP           NODE     NOMINATED NODE   READINESS GATES
# pod-writer   1/1     Running   0          3m13s   10.244.1.8   node01   <none>           <none>

# confirm in node01
ls /data
# index.html
```

---

### Lab: Node Local PV

```sh
kubectl get nodes
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   30d   v1.33.6
# node01         Ready    <none>          30d   v1.33.6
# node02         Ready    <none>          30d   v1.33.6

tee pv-local.yaml<<EOF
kind: PersistentVolume
apiVersion: v1
metadata:
  name: pv-local
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: sc-local
  capacity:
    storage: 1Gi
  local:
    path: /ssd
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
            - node02
EOF

kubectl apply -f pv-local.yaml
# persistentvolume/pv-local created

kubectl get pv
# NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# pv-local   1Gi        RWO            Retain           Bound    default/pvc-local   sc-local       <unset>                          16m

tee sc-local.yaml<<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: sc-local
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF

kubectl apply -f sc-local.yaml
# storageclass.storage.k8s.io/sc-local created

kubectl get sc
# NAME                   PROVISIONER                    RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
# local-path (default)   rancher.io/local-path          Delete          WaitForFirstConsumer   false                  5h56m
# sc-local               kubernetes.io/no-provisioner   Delete          WaitForFirstConsumer   false                  9s

tee pvc-local.yaml<<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-local
spec:
  storageClassName: sc-local
  resources:
    requests:
      storage: 1Gi
  accessModes:
  - ReadWriteOnce
EOF

kubectl apply -f pvc-local.yaml
# persistentvolumeclaim/pvc-local created

kubectl get pvc
# NAME        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# pvc-local   Pending                                      sc-local       <unset>                 15s

kubectl get pv
# NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# pv-local   2Gi        RWO            Retain           Available           pv-local       <unset>                          3m7s

tee pod-local-writer.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  generateName: pod-local-writer-
spec:
  volumes:
    - name: share-data
      persistentVolumeClaim:
        claimName: pvc-local
  containers:
    - name: writer
      image: busybox
      command:
        - sh
        - -c
        - |
          while true; do
            echo "<h1>Hello from the data writer container!$(date)</h1>" > /share/index.html;
            sleep 1;
          done
      volumeMounts:
        - name: share-data
          mountPath: /share
EOF

kubectl create -f pod-local-writer.yaml
# pod/pod-local-writer-n6f7z created
kubectl create -f pod-local-writer.yaml
# pod/pod-local-writer-j95xw created
kubectl create -f pod-local-writer.yaml
# pod/pod-local-writer-wxkxf created
kubectl create -f pod-local-writer.yaml
# pod/pod-local-writer-kqf4h created
kubectl create -f pod-local-writer.yaml
# pod/pod-local-writer-6dfvg created

kubectl get pod -o wide | grep pod-local-writer
# pod-local-writer-6dfvg   1/1     Running   0          26s   10.244.2.17   node02   <none>           <none>
# pod-local-writer-j95xw   1/1     Running   0          16m   10.244.2.13   node02   <none>           <none>
# pod-local-writer-kqf4h   1/1     Running   0          28s   10.244.2.16   node02   <none>           <none>
# pod-local-writer-n6f7z   1/1     Running   0          17m   10.244.2.14   node02   <none>           <none>
# pod-local-writer-wxkxf   1/1     Running   0          16m   10.244.2.15   node02   <none>           <none>

kubectl get pv
# NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# pv-local   1Gi        RWO            Retain           Bound    default/pvc-local   sc-local       <unset>     
kubectl get pvc
# NAME        STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# pvc-local   Bound    pv-local   1Gi        RWO            sc-local       <unset>                 19m

# confirm in node02
ls /ssd
# index.html

```
