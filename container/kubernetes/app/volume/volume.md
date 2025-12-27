# Kubernetes - Application: Storage

[Back](../../index.md)

- [Kubernetes - Application: Storage](#kubernetes---application-storage)
  - [Container storage](#container-storage)
  - [Volume](#volume)
    - [Inject data as file using volume](#inject-data-as-file-using-volume)
    - [Persisting files across container restarts](#persisting-files-across-container-restarts)
    - [Lab: without volume vs with volume](#lab-without-volume-vs-with-volume)
      - [no volume](#no-volume)
      - [Pod volume](#pod-volume)
    - [volume types](#volume-types)
  - [emptyDir](#emptydir)
    - [Classic use case: work with init container](#classic-use-case-work-with-init-container)
    - [Lab: emptyDir - share file](#lab-emptydir---share-file)
  - [hostPath volume](#hostpath-volume)
    - [Lab: hostPath volume - Security Risk demo](#lab-hostpath-volume---security-risk-demo)
  - [Docker Storage](#docker-storage)
    - [Storage Drivers](#storage-drivers)
    - [Volumes](#volumes)
  - [Storage Driver](#storage-driver)
  - [Volume Drivers](#volume-drivers)
  - [Container Storage Interface](#container-storage-interface)
  - [Volume](#volume-1)
    - [HostPath](#hostpath)
    - [Persistent Volume](#persistent-volume)
    - [Declarative Method](#declarative-method)
    - [Imperative Command](#imperative-command)
    - [Persistent Volume Claims](#persistent-volume-claims)
    - [Declarative](#declarative)
    - [Imperative Command](#imperative-command-1)

---

## Container storage

- each `container` has its own **isolated** `filesystem` provided by the `container image`.

- `Mounting`

  - the act of **attaching the filesystem** of the `storage device` or `volume` into a specific **location** in the operating system’s **file tree**

- **Note**: When any volume is mounted to a directory in the container’s filesystem, the files that are in the `container image` in that directory can **no longer be accessed**.
  - That is why `subPath` can be used.

---

## Volume

- `Volume`

  - a **directory** accessible by `containers` along with the pod's lifecycle, allowing **data to persist** beyond a `container`'s lifecycle
  - **Lifecycle**:
    - Tied to the **pod's existence**
  - **Data Persistence**:
    - Data persisted when container restarts.
    - Data is lost when the `pod` is **deleted**
  - **Scope**:
    - Defined within the pod `spec`
  - no an API object

- Use case:
  - e.g.,
    - main container: web server, read only, show content, `/var/html`
    - sidecar container: agen app, read/write, edit content, `/var/data`
  - e.g.,
    - init container: create config file, read/write
    - main container: use config file, read only

---

- A `container` can **mount zero or more** of these `volumes` in **different locations**
- A `pod` can have **multiple** `volumes`
- A `volume` can be **mounted** in **more than one** `container` to share files.

---

### Inject data as file using volume

- inject data from:
  - `configMap` object: `spec.volumes.configMap`
  - `secret` object: `spec.volumes.secret`
  - `downwardAPI` object: `spec.volumes.downwardAPI`

---

### Persisting files across container restarts

- **Without** the `volume` mounted in the container, the **entire filesystem** of the `container` is **ephemeral**.
- Volumes can **persist data** across `container` **restarts**.
  - All `volumes` in a `pod` are created **when the `pod` is set up**
    - before any of its `containers` are **started**.
  - `Volumes` are **torn down** when the pod is **shut down**.
  - The **lifecycle** of a `volume` is **tied to** the **lifecycle** of the entire `pod`
    - **independent** of the **lifecycle** of the `container` in which it is mounted.
  - the new restrart container can access the same data in the mounted volume.

### Lab: without volume vs with volume

#### no volume

```yaml
# demo-non-volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-non-volume
spec:
  containers:
    - name: nginx
      image: nginx
    - name: mongo
      image: mongo
```

```sh
# create app
kubectl apply -f demo-non-volume.yaml
# pod/demo-non-volume created

# confirm
kubectl get pod
# NAME              READY   STATUS    RESTARTS   AGE
# demo-non-volume   2/2     Running   0          27s

# insert data
kubectl exec -it demo-non-volume -c mongo -- mongosh
db.telemetry.insertOne({device_id: 1, x: 1, y: 2});
# {
#   acknowledged: true,
#   insertedId: ObjectId('694b4e86dae1c244908de666')
# }

# get data
kubectl exec -it demo-non-volume -c mongo -- mongosh
db.telemetry.find()
# [
#   {
#     _id: ObjectId('694b4e86dae1c244908de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]

# shutdown db
kubectl exec -it demo-non-volume -c mongo -- mongosh admin --eval "db.shutdownServer()"
# command terminated with exit code 137

# monitor terminal
kubectl get ev -w
# 0s          Normal    Pulling     pod/demo-non-volume   Pulling image "mongo"
# 0s          Normal    Pulled      pod/demo-non-volume   Successfully pulled image "mongo" in 1.263s (1.263s including waiting). Image size: 327004046 bytes.
# 0s          Normal    Created     pod/demo-non-volume   Created container: mongo
# 0s          Normal    Started     pod/demo-non-volume   Started container mongo

kubectl get pod -w
# NAME              READY   STATUS    RESTARTS   AGE
# demo-non-volume   2/2     Running   0          3m32s
# demo-non-volume   1/2     NotReady   0          4m
# demo-non-volume   2/2     Running    1 (3s ago)   4m3s

kubectl describe pod demo-non-volume
# Events:
#   Type    Reason     Age                 From               Message
#   ----    ------     ----                ----               -------
#   Normal  Scheduled  5m11s               default-scheduler  Successfully assigned default/demo-non-volume to docker-desktop
#   Normal  Pulling    5m11s               kubelet            Pulling image "nginx"
#   Normal  Pulled     5m10s               kubelet            Successfully pulled image "nginx" in 1.256s (1.256s including waiting). Image size: 59795293 bytes.
#   Normal  Created    5m9s                kubelet            Created container: nginx
#   Normal  Started    5m9s                kubelet            Started container nginx
#   Normal  Pulled     5m8s                kubelet            Successfully pulled image "mongo" in 797ms (797ms including waiting). Image size: 327004046 bytes.
#   Normal  Pulling    71s (x2 over 5m9s)  kubelet            Pulling image "mongo"
#   Normal  Pulled     70s                 kubelet            Successfully pulled image "mongo" in 1.263s (1.263s including waiting). Image size: 327004046 bytes.
#   Normal  Created    69s (x2 over 5m8s)  kubelet            Created container: mongo
#   Normal  Started    69s (x2 over 5m8s)  kubelet            Started container mongo

# try to read data
kubectl exec -it demo-non-volume -c mongo -- mongosh --eval "db.telemetry.find()"
# none
```

> Pod has 2 containers: nginx + mongo
> container mongo restart, but nginx is still running, therefore the pod still runs.
> No data persists after mongo restart
> -> container without volume cannot persists data.

---

#### Pod volume

```yaml
# demo-volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-volume
spec:
  # pod vol
  volumes:
    - name: mongo-vol
      emptyDir: {}
  containers:
    - name: nginx
      image: nginx
    - name: mongo
      image: mongo
      volumeMounts:
        - name: mongo-vol # reference vol
          mountPath: /data/db # path in container
```

```sh
kubectl apply -f demo-volume.yaml
# pod/demo-volume created

kubectl get pod demo-volume
# NAME          READY   STATUS    RESTARTS   AGE
# demo-volume   2/2     Running   0          29s

# insert data
kubectl exec -it demo-volume -c mongo -- mongosh
db.telemetry.insertOne({device_id: 1, x: 1, y: 2});
# {
#   acknowledged: true,
#   insertedId: ObjectId('694b56d088e4cd1e7c8de666')
# }

# get data
kubectl exec -it demo-volume -c mongo -- mongosh
db.telemetry.find()
# [
#   {
#     _id: ObjectId('694b56d088e4cd1e7c8de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]

# shutdown db
kubectl exec -it demo-volume -c mongo -- mongosh admin --eval "db.shutdownServer()"
# command terminated with exit code 137

# monitor terminal
kubectl get ev -w
# 0s          Normal    Pulling     pod/demo-volume       Pulling image "mongo"
# 0s          Normal    Pulled      pod/demo-volume       Successfully pulled image "mongo" in 1.144s (1.144s including waiting). Image size: 327004046 bytes.
# 0s          Normal    Created     pod/demo-volume       Created container: mongo
# 0s          Normal    Started     pod/demo-volume       Started container mongo

kubectl get pod -w
# NAME          READY   STATUS    RESTARTS   AGE
# demo-volume   2/2     Running   0          3m12s
# demo-volume   1/2     NotReady   0          3m58s
# demo-volume   2/2     Running    1 (3s ago)   4m1s

kubectl describe pod demo-volume
# Events:
#   Type    Reason     Age                  From               Message
#   ----    ------     ----                 ----               -------
#   Normal  Scheduled  4m34s                default-scheduler  Successfully assigned default/demo-volume to docker-desktop
#   Normal  Pulling    4m34s                kubelet            Pulling image "nginx"
#   Normal  Pulled     4m33s                kubelet            Successfully pulled image "nginx" in 1.214s (1.215s including waiting). Image size: 59795293 bytes.
#   Normal  Created    4m32s                kubelet            Created container: nginx
#   Normal  Started    4m32s                kubelet            Started container nginx
#   Normal  Pulled     4m32s                kubelet            Successfully pulled image "mongo" in 764ms (764ms including waiting). Image size: 327004046 bytes.
#   Normal  Pulling    36s (x2 over 4m32s)  kubelet            Pulling image "mongo"
#   Normal  Created    35s (x2 over 4m31s)  kubelet            Created container: mongo
#   Normal  Pulled     35s                  kubelet            Successfully pulled image "mongo" in 1.144s (1.144s including waiting). Image size: 327004046 bytes.
#   Normal  Started    34s (x2 over 4m31s)  kubelet            Started container mongo

# try to read data
kubectl exec -it demo-volume -c mongo -- mongosh --eval "db.telemetry.find()"
# [
#   {
#     _id: ObjectId('694b56d088e4cd1e7c8de666'),
#     device_id: 1,
#     x: 1,
#     y: 2
#   }
# ]
```

---

### volume types

- `emptyDir`
  - A simple **directory** that allows the `pod` to store data **for the duration of its life cycle**.
  - The directory is created **just before** the `pod` **starts** and is **initially empty**.
- `hostPath`
  - Used for **mounting files** from the `worker node’s` **filesystem** into the `pod`.
- `configMap`, `secret`, `downwardAPI`, and the projected volume type
  - Special types of volumes used to **expose information** about the pod and other **Kubernetes objects** through files.
  - typically used to **configure the application** running in the `pod`.
- `persistentVolumeClaim`
  - A portable way to **integrate external storage** into pods.
  - points to a `PersistentVolumeClaim` **object** that **points** to a `PersistentVolume` object that finally references the actual storage.
- `nfs`
  - An **NFS share** mounted into the pod.
- `gcePersistentDisk(Google Compute Engine Persistent Disk)`, `awsElasticBlockStore (Amazon Web Services Elastic Block Store)`, `azureFile (Microsoft Azure File Service)`, `azureDisk (Microsoft Azure Data Disk)`
  - Used for mounting **cloud provider**-specific storage.
- `cephfs`, `cinder`, `fc`, `flexVolume`, `flocker`, `glusterfs`, `iscsi`, `portworxVolume`, `quobyte`, `rbd`, `scaleIO`, `storageos`, `photonPersistentDisk`, `vsphereVolume`
  - Used for mounting other types of **network storage**.
- `csi`
  - A pluggable way of **adding storage via** the `Container Storage Interface`.
  - allows anyone to implement their own storage driver that is then referenced in the csi volume definition.

---

## emptyDir

- Get volume explain
  - `kubectl explain pod.spec.volumes`
- Get emptyDir explain

```sh
kubectl explain pod.spec.volumes.emptyDir
# KIND:       Pod
# VERSION:    v1

# FIELD: emptyDir <EmptyDirVolumeSource>


# DESCRIPTION:
#     emptyDir represents a temporary directory that shares a pod's lifetime. More
#     info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir
#     Represents an empty directory for a pod. Empty directory volumes support
#     ownership management and SELinux relabeling.

# FIELDS:
#   medium        <string>
#     medium represents what type of storage medium should back this directory.
#     The default is "" which means to use the node's default medium. Must be an
#     empty string (default) or Memory. More info:
#     https://kubernetes.io/docs/concepts/storage/volumes#emptydir

#   sizeLimit     <Quantity>
#     sizeLimit is the total amount of local storage required for this EmptyDir
#     volume. The size limit is also applicable for memory medium. The maximum
#     usage on memory medium EmptyDir would be the minimum value between the
#     SizeLimit specified here and the sum of memory limits of all containers in a
#     pod. The default is nil which means that the limit is undefined. More info:
#     https://kubernetes.io/docs/concepts/storage/volumes#emptydir
```

- physical path of directory on host node
  - `/var/lib/kubelet/pods/pod_uid/volumes/kubernetes.io~empty/volume_name/`
- if the `pod` is **deleted**, the directory is **deleteed** as well.

- `spec.volumes` configuration

  - `medium` field:
    - default: medium of the `host node`; the directory is created on one of the **node’s disks**
    - value:
      - `Memory`: use `tmpfs`, a **virtual memory filesystem** where the files are kept in **memory** instead of on the hard disk.
  - `sizeLimit` field:
    - total amount of local storage
    - e.g., `10Mi`

- common `spec.containers.volumeMounts` configuration
  - `name` field: name of the volume to mount.
  - `mountPath` field: path within the container at which to mount the volume.
  - `readOnly` field:
    - Whether to mount the volume as read-only.
    - Defaults: `false`.

---

### Classic use case: work with init container

- requirements:
  - db pod is empty when created and need manually insert init data
  - db needs to insert init data automatically
  - db needs to persist data
- solution:
  - define 2 volumes:
    - init_script_vol
    - db_data_vol
  - Copy script of inserting data to the init_container_image
  - setup init container to copy the script from init_container_image to the init_script_vol
  - mount init_script_vol to regular container to automatically execute the init script
  - mount db_data_vol to persist data even db container restart.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-init-db
spec:
  volumes:
    - name: initdb
      emptyDir: {}
    - name: db-data
      emptyDir: {}
  # init container
  initContainers:
    - name: installer
      image: installer_image
      volumeMounts:
        - name: initdb
          mountPath: /initdb.d
  # container
  containers:
    - name: mongo
      image: mongo
      volumeMounts:
        - name: initdb
          mountPath: /docker-entrypoint-initdb.d/ # use entry point for init script
          readOnly: true
        - name: db-data
          mountPath: /data/db
```

---

### Lab: emptyDir - share file

```yaml
# demo-emptydir-sharefile.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-emptydir-sharefile
spec:
  volumes:
    - name: shared-data
      emptyDir: {}
  # no restart
  restartPolicy: Never

  containers:
    - name: file-writer
      image: busybox
      volumeMounts:
        - name: shared-data
          mountPath: /app-data
      command:
        [
          "/bin/sh",
          "-c",
          "echo '<h1>Hello from the data writer container!</h1>' > /app-data/index.html; sleep 10",
        ]

    - name: nginx
      image: nginx:alpine
      volumeMounts:
        - name: shared-data
          mountPath: /usr/share/nginx/html
      ports:
        - containerPort: 80
```

```sh
kubectl apply -f demo-emptydir-sharefile.yaml
# pod/demo-emptydir-sharefile created

kubectl get pod
# NAME                      READY   STATUS     RESTARTS      AGE
# demo-emptydir-sharefile   1/2     NotReady   0             23s

kubectl port-forward demo-emptydir-sharefile 8080:80
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

curl localhost:8080
# <h1>Hello from the data writer container!</h1>

```

---

## hostPath volume

- `hostPath` volume

  - points to a **specific file or directory** in the filesystem of the `host node`
  - can be a risk:
    - pod can be deploy on any node; but the content in the hostPath dir of each node can be different.
    - also can be a security risk

- `hostPath` volume types

  - `<empty>`: no checks before it mounts the volume.
  - `Directory`: checks if a directory exists
  - `DirectoryOrCreate`: create directory if not exists
  - `File`: path must be a file.
  - `FileOrCreate`: create file if not exists
  - `BlockDevice`: path must be a block device.
  - `CharDevice`: path must be a character device.
  - `Socket`: path must be a UNIX socket.

- explain

```sh
kubectl explain pod.spec.volumes.hostPath
# KIND:       Pod
# VERSION:    v1

# FIELD: hostPath <HostPathVolumeSource>


# DESCRIPTION:
#     hostPath represents a pre-existing file or directory on the host machine
#     that is directly exposed to the container. This is generally used for system
#     agents or other privileged things that are allowed to see the host machine.
#     Most containers will NOT need this. More info:
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

---

### Lab: hostPath volume - Security Risk demo

```yaml
# demo-hostpath.yaml
apiVersion: v1
kind: Pod
metadata:
  name: node-explorer
spec:
  volumes:
    - name: host-root
      hostPath:
        path: /
  containers:
    - name: node-explorer
      image: alpine
      command: ["sleep", "9999999999"]
      volumeMounts:
        - name: host-root
          mountPath: /host
```

```sh
kubectl apply -f demo-hostpath.yaml
# pod/node-explorer created

kubectl get pod/node-explorer
# NAME            READY   STATUS    RESTARTS   AGE
# node-explorer   1/1     Running   0          22s

# show risk: can explore node filesystem
kubectl exec -it node-explorer -- sh
/ # ls
bin    etc    host   media  opt    root   sbin   sys    usr
dev    home   lib    mnt    proc   run    srv    tmp    var

/ # mkdir /var/test
/ # ls -dl /var/test
drwxr-xr-x    2 root     root          4096 Dec 24 05:09 /var/test
```

---

## Docker Storage

### Storage Drivers

- Docker File System:
  - `var/lib/docker`
    - aufs
    - containers
    - image
    - volumes

---

- `Image Layer` Architecture

  - command: `docker build`
  - Each line of instruction in a Dockerfile creates new layer in the Docker image.
  - Each lay stores the changes from the previous layer.
    - When building an image, Docker tries to reuse the unchanged previous layer and creates only the changed layers.
  - read only
    - Layers are immutable, and get modified only by a new build.

- `Container layer`:
  - Docker creates a new writable layer on top of the `image layers`.
  - a read write layer.
  - stores data created by the container.
    - e.g., log files, temporary files, files modified by user.
  - `Copy on write mechanism`
    - When the file in the `image layer` gets modified, Docker automatically creates a copy of the `image layer` in the `container layer` and enables read / write.
  - live only when the container is running
    - new layer gets destroyed along with container.

---

### Volumes

- `Volume`

  - used persist the data in `Container Layer`

- command: `docker volume create data_volume`

  - File system
    - create a new dir: `/var/lib/docker/data_volum`

- `Volume Mounting`

  - mounts a volume from the volumes dir.
  - `docker run -v data_volume:/var/lib/mysql mysql`
  - if the volume is not created yet, Docker automatically creates the volume

- `Bind mounting`

  - mount a directory
  - `docker run -v /data/mysql:/var/lib/mysql mysql`

- `--mount`: new style with key value pair

```sh
docker run \
    --mount type=bind,source=/data/mysqll,target/var/lib/mysql mysql
```

---

## Storage Driver

- the component to enable layered architecture, e.g., create layers, move files across layers
- Common Storage Drivers, depends on the OS
  - `AUFS`: default in Ubuntu
  - `ZFS`
  - `BTRFS`
  - `Device Mapper`: fedora/ CentOS
  - `Overlay`
  - `Overlay2`

---

## Volume Drivers

- `volume drivers plugin`

  - the component to handle Docker volumes
  - default: `local`

- Can be specified in the container

```sh
# save data in the AWS ebs
docker run -it\
    --name mysql    \
    --volume-driver rexray/ebs  \
    --mount src=ebs-vol,target=/var/lib/mysql   \
    mysql
```

---

## Container Storage Interface

- `Container Runtime interface(CRI)`
  - used to handle the communication between the Kubernetes and container runtimes.
- `Container Network Interface(CNI)`

  - used to coordinate between different network solution and kubernetes.

- `Container Storage Interface(CSI)`
  - used to coordinate between different storage solution and kubernetes.
  - define a set of `remote procedure calls(rpc)`

---

## Volume

Types

### HostPath

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-example-linux
spec:
  nodeSelector:
    kubernetes.io/os: linux
  containers:
    - name: example-container
      image: registry.k8s.io/test-webserver
      volumeMounts:
        - mountPath: /foo
          name: example-volume
          readOnly: true
  volumes:
    - name: example-volume
      # mount /data/foo, but only if that directory already exists
      hostPath:
        path: /data/foo # directory location on host
        type: Directory # this field is optional
```

---

### Persistent Volume

- a cluster wide pool of storage volumes for app deployement.
- the user can select storage from this pool by persistent volume claim.

---

### Declarative Method

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 5Gi
  hostPath:
    path: /tmp/data
```

- accessModes:
  - ReadOnlyMany
  - ReadWriteOnce
  - ReadWriteMany

---

### Imperative Command

| Command                                           | Description                                                             |
| ------------------------------------------------- | ----------------------------------------------------------------------- |
| `kubectl get persistentvolume` / `kubectl get pv` | List all PersistentVolumes in the cluster.                              |
| `kubectl get pv <name>`                           | Show a specific PV (basic info).                                        |
| `kubectl describe pv <name>`                      | Show detailed status, events, and spec of a specific PV.                |
| `kubectl delete pv <name>`                        | Delete a specific PV object (actual storage depends on reclaim policy). |

---

### Persistent Volume Claims

- object to use the pv

  - bind the volume with the pod
  - if no volume is available, the claim remains pending.

- reclaim policy
  - `retain`:
    - default
    - keep PV and it's data
  - `delete`:
    - delete PV

### Declarative

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

---

- Using PVCs in Pods

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
        - mountPath: "/var/www/html"
          name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

### Imperative Command

| Command                                                 | Description                                               |
| ------------------------------------------------------- | --------------------------------------------------------- |
| `kubectl get persistentvolumeclaim` / `kubectl get pvc` | List all PersistentVolumeClaims in the current namespace. |
| `kubectl get pvc -n <namespace>`                        | List PVCs in a specific namespace.                        |
| `kubectl describe pvc <name>`                           | Show detailed status, events, and spec of a specific PVC. |
| `kubectl delete pvc <name>`                             | Delete a specific PVC.                                    |

---

Lab

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-log
spec:
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: /pv/log
  persistentVolumeReclaimPolicy: Retain
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-log-1
spec:
  accessModes:
    - ReadWriteOnce
  volumeName: pv-log
  resources:
    requests:
      storage: 50Mi
```

---
