# Kubernetes - Storage: Volume - `hostPath`

[Back](../../index.md)

- [Kubernetes - Storage: Volume - `hostPath`](#kubernetes---storage-volume---hostpath)
  - [`hostPath` Volume](#hostpath-volume)
    - [Lab: hostPath volume - Security Risk demo](#lab-hostpath-volume---security-risk-demo)
    - [Lab: Install `rancher` for `hostPath`](#lab-install-rancher-for-hostpath)

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

### Lab: Install `rancher` for `hostPath`

```sh
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
# namespace/local-path-storage created
# serviceaccount/local-path-provisioner-service-account created
# role.rbac.authorization.k8s.io/local-path-provisioner-role created
# clusterrole.rbac.authorization.k8s.io/local-path-provisioner-role created
# rolebinding.rbac.authorization.k8s.io/local-path-provisioner-bind created
# clusterrolebinding.rbac.authorization.k8s.io/local-path-provisioner-bind created
# deployment.apps/local-path-provisioner created
# storageclass.storage.k8s.io/local-path created
# configmap/local-path-config created

kubectl get sc
# NAME         PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
# local-path   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  3m3s


kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
# storageclass.storage.k8s.io/local-path patched

kubectl get sc
# NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
# local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  20m

kubectl get sc -o yaml
# apiVersion: v1
# items:
# - apiVersion: storage.k8s.io/v1
#   kind: StorageClass
#   metadata:
#     annotations:
#       kubectl.kubernetes.io/last-applied-configuration: |
#         {"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"},"name":"hostpath"},"provisioner":"docker.io/hostpath","reclaimPolicy":"Delete","volumeBindingMode":"Immediate"}
#       storageclass.kubernetes.io/is-default-class: "true"
#     creationTimestamp: "2025-11-05T18:00:48Z"
#     name: hostpath
#     resourceVersion: "402"
#     uid: 1f503168-2cfb-4064-a51e-66605b6bdd4a
#   provisioner: docker.io/hostpath
#   reclaimPolicy: Delete
#   volumeBindingMode: Immediate
# - apiVersion: storage.k8s.io/v1
#   kind: StorageClass
#   metadata:
#     annotations:
#       kubectl.kubernetes.io/last-applied-configuration: |
#         {"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{},"name":"local"},"provisioner":"kubernetes.io/no-provisioner","volumeBindingMode":"WaitForFirstConsumer"}
#     creationTimestamp: "2025-12-25T20:00:45Z"
#     name: local
#     resourceVersion: "2478232"
#     uid: 927380ce-05a7-4e26-84a9-ccaa463f5f23
#   provisioner: kubernetes.io/no-provisioner
#   reclaimPolicy: Delete
#   volumeBindingMode: WaitForFirstConsumer
# kind: List
# metadata:
#   resourceVersion: ""
```

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
