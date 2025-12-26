



## Lab: Install hostPath - 

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