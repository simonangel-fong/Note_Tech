# Kubernetes - Storage: Node Local Persistent Volumes

[Back](../../index.md)

- [Kubernetes - Storage: Node Local Persistent Volumes](#kubernetes---storage-node-local-persistent-volumes)
  - [Node Local Persistent Volume](#node-local-persistent-volume)
  - [Lab: Install hostPath - `rancher`](#lab-install-hostpath---rancher)
    - [Lab: Node Local PV](#lab-node-local-pv)

---

## Node Local Persistent Volume

- `Local persistent volumes`

  - Kubernetes scheduler ensures that the pod is always scheduled on the node to which the local volume is attached.

- Use `PersistentVolume.spec.nodeAffinity` feature to schedule pod to a node

---

## Lab: Install hostPath - `rancher`

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
