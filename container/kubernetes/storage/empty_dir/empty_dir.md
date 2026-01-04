# Kubernetes - Storage: Volume - `emptyDir`

[Back](../../index.md)

- [Kubernetes - Storage: Volume - `emptyDir`](#kubernetes---storage-volume---emptydir)
  - [`emptyDir`](#emptydir)
    - [Declarative Manifest](#declarative-manifest)
    - [Classic use case: work with init container](#classic-use-case-work-with-init-container)
    - [Lab: emptyDir - share file](#lab-emptydir---share-file)

---

## `emptyDir`

- a **temporary volume** that is created when a `Pod` is **assigned** to a `node` and **exists as long as** that Pod remains on that node.

- **physical path** of directory on `host node`
  - `/var/lib/kubelet/pods/pod_uid/volumes/kubernetes.io~empty/volume_name/`
- if the `pod` is **deleted**, the directory is **deleteed** as well.

---

### Declarative Manifest

- `pod.spec.volumes` field

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
