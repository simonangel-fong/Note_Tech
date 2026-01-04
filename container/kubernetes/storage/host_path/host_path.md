# Kubernetes - Storage: Volume - `hostPath`

[Back](../../index.md)

- [Kubernetes - Storage: Volume - `hostPath`](#kubernetes---storage-volume---hostpath)
  - [`hostPath` Volume](#hostpath-volume)
    - [Lab: hostPath volume - Security Risk demo](#lab-hostpath-volume---security-risk-demo)

---

## `hostPath` Volume

- `hostPath` volume

  - points to a **specific file or directory** **already exists** in the filesystem of the `host node`
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
