# Kubernetes - Storage

[Back](../../index.md)

- [Kubernetes - Storage](#kubernetes---storage)
  - [Docker Storage](#docker-storage)
    - [Storage Drivers](#storage-drivers)
    - [Volumes](#volumes)
  - [Storage Driver](#storage-driver)
  - [Volume Drivers](#volume-drivers)
  - [Container Storage Interface](#container-storage-interface)
  - [Volume](#volume)
    - [HostPath](#hostpath)
    - [Persistent Volume](#persistent-volume)
    - [Declarative Method](#declarative-method)
    - [Imperative Command](#imperative-command)
    - [Persistent Volume Claims](#persistent-volume-claims)
    - [Declarative](#declarative)
    - [Imperative Command](#imperative-command-1)
  - [Storage Class](#storage-class)
    - [Declarative Method](#declarative-method-1)
    - [Imperative Commands](#imperative-commands)

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

## Storage Class

- Static Provisioning

  - a volume must be created before a pv creates.

- Dynamic Provisioning
  - the volume automatically is created
  - implemented by storageClass

---

### Declarative Method

- create a storage class with `google cloud engine`
  - pc is not required

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  replication-type: none
```

- Create a pvc with storage class

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: google-storage # refer storage class
  resources:
    requests:
      storage: 500Mi
```

- Apply PVC to a pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - image: alpine
      name: alpine
      command: ["/bin/sh", "-c"]
      args: ["shuf -i 0-100 -n 1 >> /opt/number.out;"]
      volumeMounts:
        - mountPath: /opt
          name: data-volume

  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: myclaim # refer pvc
```

---

### Imperative Commands

| Command                                       | Description                                                                       |
| --------------------------------------------- | --------------------------------------------------------------------------------- |
| `kubectl get storageclass` / `kubectl get sc` | List all StorageClasses in the cluster.                                           |
| `kubectl get sc <name>`                       | Show basic info for a specific StorageClass.                                      |
| `kubectl describe sc <name>`                  | Show detailed configuration, reclaim policy, parameters, and provisioner details. |
| `kubectl delete sc <name>`                    | Delete a specific StorageClass.                                                   |
