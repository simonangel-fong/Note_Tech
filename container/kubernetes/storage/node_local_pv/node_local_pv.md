# Kubernetes: Storage - `Node Local Persistent Volumes`

[Back](../../index.md)

- [Kubernetes: Storage - `Node Local Persistent Volumes`](#kubernetes-storage---node-local-persistent-volumes)
  - [Node Local Persistent Volume](#node-local-persistent-volume)
  - [Lab: Node Local Persistent Volume](#lab-node-local-persistent-volume)

---

## Node Local Persistent Volume

- `Local persistent volumes`

  - Kubernetes scheduler **ensures** that the pod is always **scheduled on the node** to which the `local volume` is attached.

- Use `PersistentVolume.spec.nodeAffinity` feature to schedule pod to a node

---

## Lab: Node Local Persistent Volume

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
