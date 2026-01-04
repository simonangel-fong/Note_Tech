# Kubernetes - StatefulSet

[Back](../index.md)

- [Kubernetes - StatefulSet](#kubernetes---statefulset)
  - [StatefulSet Object](#statefulset-object)
    - [Associated Objects](#associated-objects)
    - [Pod Replacement](#pod-replacement)
    - [Headless Service](#headless-service)
    - [Declarative Manifest](#declarative-manifest)
    - [Imperative Commands](#imperative-commands)
    - [Lab: StatefulSet](#lab-statefulset)
      - [Explain](#explain)
      - [Create StatefulSet](#create-statefulset)
      - [Pod Replacement](#pod-replacement-1)
      - [Deleting StatefulSet](#deleting-statefulset)
  - [Handling Node Failure](#handling-node-failure)
      - [Solution A: Manual Intervention](#solution-a-manual-intervention)
      - [Solution B: Fix the disconnection](#solution-b-fix-the-disconnection)
  - [Scaling a StatefulSet](#scaling-a-statefulset)
    - [Pod Management Policy](#pod-management-policy)
    - [PersistentVolumeClaim Retention Policy](#persistentvolumeclaim-retention-policy)

---

## StatefulSet Object

- `stateful workload`

  - a piece of software that must **store and maintain state** in order to function.
  - state must be **maintained** when the workload is **restarted or relocated**.
  - harder to scale
    - **can’t** simply add and remove replicas **without considering their state**,

- `statefulset`

  - the API object designed to manage applications that need to **maintain their identity and state**.

- Limitation of PV to share state:
  - in most cloud environments, the underlying **storage technology** typically **only** supports the `ReadWriteOnce` and `ReadOnlyMany` access modes, not `ReadWriteMany`,
  - **can’t** mount the volume on multiple nodes in `read/write mode`.

---

### Associated Objects

- the `Pod` is controlled and managed by the `StatefulSet`

  - `StatefulSets` own the `Pods` **directly**

- `PersistentVolumeClaim`:

  - each `Pod` instance gets its own `PersistentVolumeClaim`.
  - The name of the claim is made up of the `claimName` and the **name** of the Pod.

- Additional labels in pod:

  - `apps.kubernetes.io/pod-index`: the order of the pod
  - `controller-revision-hash`: hash value calculated based on the statefulset template to track the version
  - `statefulset.kubernetes.io/pod-name`: specifies the Pod name

---

### Pod Replacement

- `StatefulSet Controller` ensures that there are always the **desired number** of `Pods` configured in the replicas field.

  - if a `StatefulSet Pod` is **deleted** and replaced by the `controller` with a new instance
  - the replica **retains the same identity** and is **associated with the same** `PersistentVolumeClaim`.

---

### Headless Service

- `peer discovery`

  - the ability for each cluster member to **find the other members**.
  - an application deployed via a `StatefulSet` needs to **find all other** `Pods` in the `StatefulSet` via `DNS`

- For example, a client connecting to a **MongoDB replica** set must know the addresses of **all the replicas**, so it can find the **primary replica** when it needs to **write data**.

  - You must specify the **addresses in the connection string** you pass to the MongoDB client.

- Exposing stateful Pods through **DNS individually**

  - The `headless Service` provide `A` or `AAAA` record that resolves directly to the individual Pod’s IP.
  - the pod's resolvable address:
    - `POD_NAME.SVC_NAME.NAMESPACE.CLUSTER_DOMAIN`
    - e.g., `mongo-1.mongodb-svc.default.svc.cluster.local`

- Exposing stateful Pods via **SRV records**
  - SRV record address:
    - `PORT_NAME.PROTOCOL_NAME.SVC_NAME.NAMESPACE.CLUSTER_DOMAIN`
    - e.g., `_mongodb._tcp.mongodb-svc.default.svc.cluster.local`
    - MongoDB connection string: `mongodb+srv://mongodb-svc.default.svc.cluster.local`

---

- it’s common for a `StatefulSet` to be associated with both a `regular Service` and a `headless Service`.
  - `headless Service`: helps `sts pod` **to find each other**
  - `regular service`: help client traffice to forwards to those pod are ready.
    - since the `sts` needs to find each other event they are unready.

---

### Declarative Manifest

- `podManagementPolicy`

  - specify how pods are **created**
  - `OrderedReady`
    - default
    - pods are **created in increasing order**
  - `Parallel`
    - create pods in parallel

- `volumeClaimTemplates`
  - specify the **templates** for the `PersistentVolumeClaims` that the controller creates for each replica.
  - must specify the name
  - name must match the name in the volumes

---

### Imperative Commands

| CMD                                                    | DESC                            |
| ------------------------------------------------------ | ------------------------------- |
| `kubectl explain statefulset`                          | API schema                      |
| `kubectl get sts <name> -o yaml`                       | Export YAML                     |
| `kubectl get statefulset` / `kubectl get sts`          | List StatefulSets               |
| `kubectl describe sts <name>`                          | Detailed info & events          |
| `kubectl create sts <name> --image=<img> --replicas=N` | Create StatefulSet imperatively |
| `kubectl scale sts <name> --replicas=N`                | Scale replicas                  |
| `kubectl rollout status sts <name>`                    | Watch rolling update            |
| `kubectl rollout history sts <name>`                   | View revision history           |
| `kubectl rollout undo sts <name>`                      | Rollback to previous revision   |
| `kubectl delete sts <name>`                            | Delete StatefulSet              |
| `kubectl delete pod <sts-pod>`                         | Restart a single replica        |
| `kubectl edit sts <name>`                              | Live edit                       |
| `kubectl get pods -l app=<label> -o wide`              | View ordered pods               |
| `kubectl get pvc`                                      | List persistent volumes         |
| `kubectl get pvc -l app=<label>`                       | View volumes per pod            |

---

### Lab: StatefulSet

#### Explain

```sh
kubectl explain sts
# GROUP:      apps
# KIND:       StatefulSet
# VERSION:    v1

# DESCRIPTION:
#     StatefulSet represents a set of pods with consistent identities. Identities
#     are defined as:
#       - Network: A single stable DNS and hostname.
#       - Storage: As many VolumeClaims as requested.

#     The StatefulSet guarantees that a given network identity will always map to
#     the same storage identity.

# FIELDS:
#   apiVersion    <string>
#     APIVersion defines the versioned schema of this representation of an object.
#     Servers should convert recognized schemas to the latest internal value, and
#     may reject unrecognized values. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

#   kind  <string>
#     Kind is a string value representing the REST resource this object
#     represents. Servers may infer this from the endpoint the client submits
#     requests to. Cannot be updated. In CamelCase. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

#   metadata      <ObjectMeta>
#     Standard object's metadata. More info:
#     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

#   spec  <StatefulSetSpec>
#     Spec defines the desired identities of pods in this set.

#   status        <StatefulSetStatus>
#     Status is the current status of Pods in this StatefulSet. This data may be
#     out of date by some window of time.

kubectl explain sts.spec
# GROUP:      apps
# KIND:       StatefulSet
# VERSION:    v1

# FIELD: spec <StatefulSetSpec>


# DESCRIPTION:
#     Spec defines the desired identities of pods in this set.
#     A StatefulSetSpec is the specification of a StatefulSet.

# FIELDS:
#   minReadySeconds       <integer>
#     Minimum number of seconds for which a newly created pod should be ready
#     without any of its container crashing for it to be considered available.
#     Defaults to 0 (pod will be considered available as soon as it is ready)

#   ordinals      <StatefulSetOrdinals>
#     ordinals controls the numbering of replica indices in a StatefulSet. The
#     default ordinals behavior assigns a "0" index to the first replica and
#     increments the index by one for each additional replica requested.

#   persistentVolumeClaimRetentionPolicy  <StatefulSetPersistentVolumeClaimRetentionPolicy>
#     persistentVolumeClaimRetentionPolicy describes the lifecycle of persistent
#     volume claims created from volumeClaimTemplates. By default, all persistent
#     volume claims are created as needed and retained until manually deleted.
#     This policy allows the lifecycle to be altered, for example by deleting
#     persistent volume claims when their stateful set is deleted, or when their
#     pod is scaled down.

#   podManagementPolicy   <string>
#   enum: OrderedReady, Parallel
#     podManagementPolicy controls how pods are created during initial scale up,
#     when replacing pods on nodes, or when scaling down. The default policy is
#     `OrderedReady`, where pods are created in increasing order (pod-0, then
#     pod-1, etc) and the controller will wait until each pod is ready before
#     continuing. When scaling down, the pods are removed in the opposite order.
#     The alternative policy is `Parallel` which will create pods in parallel to
#     match the desired scale without waiting, and on scale down will delete all
#     pods at once.

#     Possible enum values:
#      - `"OrderedReady"` will create pods in strictly increasing order on scale
#     up and strictly decreasing order on scale down, progressing only when the
#     previous pod is ready or terminated. At most one pod will be changed at any
#     time.
#      - `"Parallel"` will create and delete pods as soon as the stateful set
#     replica count is changed, and will not wait for pods to be ready or complete
#     termination.

#   replicas      <integer>
#     replicas is the desired number of replicas of the given Template. These are
#     replicas in the sense that they are instantiations of the same Template, but
#     individual replicas also have a consistent identity. If unspecified,
#     defaults to 1.

#   revisionHistoryLimit  <integer>
#     revisionHistoryLimit is the maximum number of revisions that will be
#     maintained in the StatefulSet's revision history. The revision history
#     consists of all revisions not represented by a currently applied
#     StatefulSetSpec version. The default value is 10.

#   selector      <LabelSelector> -required-
#     selector is a label query over pods that should match the replica count. It
#     must match the pod template's labels. More info:
#     https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors

#   serviceName   <string>
#     serviceName is the name of the service that governs this StatefulSet. This
#     service must exist before the StatefulSet, and is responsible for the
#     network identity of the set. Pods get DNS/hostnames that follow the pattern:
#     pod-specific-string.serviceName.default.svc.cluster.local where
#     "pod-specific-string" is managed by the StatefulSet controller.

#   template      <PodTemplateSpec> -required-
#     template is the object that describes the pod that will be created if
#     insufficient replicas are detected. Each pod stamped out by the StatefulSet
#     will fulfill this Template, but have a unique identity from the rest of the
#     StatefulSet. Each pod will be named with the format
#     <statefulsetname>-<podindex>. For example, a pod in a StatefulSet named
#     "web" with index number "3" would be named "web-3". The only allowed
#     template.spec.restartPolicy value is "Always".

#   updateStrategy        <StatefulSetUpdateStrategy>
#     updateStrategy indicates the StatefulSetUpdateStrategy that will be employed
#     to update Pods in the StatefulSet when a revision is made to Template.

#   volumeClaimTemplates  <[]PersistentVolumeClaim>
#     volumeClaimTemplates is a list of claims that pods are allowed to reference.
#     The StatefulSet controller is responsible for mapping network identities to
#     claims in a way that maintains the identity of a pod. Every claim in this
#     list must have at least one matching (by name) volumeMount in one container
#     in the template. A claim in this list takes precedence over any volumes in
#     the template, with the same name.

```

---

#### Create StatefulSet

- Headless serive

```yaml
# demo-mongodb-svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-svc
  labels:
    app: mongodb
spec:
  clusterIP: None # Headless
  selector:
    app: mongodb
  ports:
    - name: mongodb
      port: 27017
      targetPort: 27017
```

- Mongodb with statefulset

```yaml
# demo-mongodb.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
spec:
  serviceName: mongodb-svc
  replicas: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
        - name: mongodb
          image: mongo
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: data
              mountPath: /data/db
  volumeClaimTemplates: # a unique PVC for each pod
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

```sh
kubectl apply -f demo-mongodb-svc.yaml
# service/mongodb-svc created

kubectl apply -f demo-mongodb.yaml
# statefulset.apps/mongodb created

kubectl get sts -o wide
# NAME      READY   AGE   CONTAINERS   IMAGES
# mongodb   3/3     55s   mongodb      mongo

# confirm: no rs
kubectl get rs
# No resources found in default namespace.

kubectl rollout status sts mongodb
# Waiting for 3 pods to be ready...
# Waiting for 2 pods to be ready...
# Waiting for 2 pods to be ready...
# Waiting for 1 pods to be ready...
# Waiting for 1 pods to be ready...
# partitioned roll out complete: 3 new pods have been updated...

kubectl describe sts mongodb
# Name:               mongodb
# Namespace:          default
# CreationTimestamp:  Wed, 31 Dec 2025 17:50:43 -0500
# Selector:           app=mongodb
# Labels:             <none>
# Annotations:        <none>
# Replicas:           3 desired | 3 total
# Update Strategy:    RollingUpdate
#   Partition:        0
# Pods Status:        3 Running / 0 Waiting / 0 Succeeded / 0 Failed
# Pod Template:
#   Labels:  app=mongodb
#   Containers:
#    mongodb:
#     Image:        mongo
#     Port:         27017/TCP
#     Host Port:    0/TCP
#     Environment:  <none>
#     Mounts:
#       /data/db from data (rw)
#   Volumes:         <none>
#   Node-Selectors:  <none>
#   Tolerations:     <none>
# Volume Claims:
#   Name:          data
#   StorageClass:
#   Labels:        <none>
#   Annotations:   <none>
#   Capacity:      10Gi
#   Access Modes:  [ReadWriteOnce]
# Events:
#   Type    Reason            Age    From                    Message
#   ----    ------            ----   ----                    -------
#   Normal  SuccessfulCreate  2m33s  statefulset-controller  create Claim data-mongodb-0 Pod mongodb-0 in StatefulSet mongodb success
#   Normal  SuccessfulCreate  2m33s  statefulset-controller  create Pod mongodb-0 in StatefulSet mongodb successful
#   Normal  SuccessfulCreate  2m30s  statefulset-controller  create Claim data-mongodb-1 Pod mongodb-1 in StatefulSet mongodb success
#   Normal  SuccessfulCreate  2m30s  statefulset-controller  create Pod mongodb-1 in StatefulSet mongodb successful
#   Normal  SuccessfulCreate  2m27s  statefulset-controller  create Claim data-mongodb-2 Pod mongodb-2 in StatefulSet mongodb success
#   Normal  SuccessfulCreate  2m27s  statefulset-controller  create Pod mongodb-2 in StatefulSet mongodb successful


kubectl get pod -o wide
# NAME        READY   STATUS    RESTARTS   AGE     IP           NODE             NOMINATED NODE   READINESS GATES
# mongodb-0   1/1     Running   0          2m54s   10.1.3.214   docker-desktop   <none>           <none>
# mongodb-1   1/1     Running   0          2m50s   10.1.3.215   docker-desktop   <none>           <none>
# mongodb-2   1/1     Running   0          2m48s   10.1.3.216   docker-desktop   <none>           <none>

# confirm pod:
#   Controlled By:  StatefulSe
#   mount read/write volume
kubectl describe pod mongodb-0
# Labels:           app=mongodb
#                   apps.kubernetes.io/pod-index=0
#                   controller-revision-hash=mongodb-86954b94c4
#                   statefulset.kubernetes.io/pod-name=mongodb-0
# Controlled By:  StatefulSet/mongodb
# Volumes:
#   data:
#     Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
#     ClaimName:  data-mongodb-0
#     ReadOnly:   false


# confirm: pvc
kubectl get pvc -o wide
# NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE    VOLUMEMODE
# data-mongodb-0   Bound    pvc-76d4f6d8-c326-478a-b1b8-9fa9bb1064f2   10Gi       RWO            hostpath       <unset>                 175m   Filesystem
# data-mongodb-1   Bound    pvc-4e72560b-6a6d-4cc2-8f40-5efd8e2ab85d   10Gi       RWO            hostpath       <unset>                 175m   Filesystem
# data-mongodb-2   Bound    pvc-5b70bd9e-f4d9-4ecd-a4f3-919e926dbe38   10Gi       RWO            hostpath       <unset>                 174m   Filesystem

kubectl get pv -o wide
# NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                    STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE    VOLUMEMODE
# pvc-4e72560b-6a6d-4cc2-8f40-5efd8e2ab85d   10Gi       RWO            Delete           Bound    default/data-mongodb-1   hostpath       <unset>                          175m   Filesystem
# pvc-5b70bd9e-f4d9-4ecd-a4f3-919e926dbe38   10Gi       RWO            Delete           Bound    default/data-mongodb-2   hostpath       <unset>                          175m   Filesystem
# pvc-76d4f6d8-c326-478a-b1b8-9fa9bb1064f2   10Gi       RWO            Delete           Bound    default/data-mongodb-0   hostpath       <unset>                          175m   Filesystem
```

- Run pod to verify

```sh
# run mongo cli
kubectl run mongo-client --rm -it --image=mongo -- mongosh --host mongodb-0.mongodb-svc --eval "db.adminCommand('ping')"
# { ok: 1 }

# test using svr url
kubectl run mongo-client --rm -it --image=mongo -- mongosh "mongodb+srv://mongodb-svc.default.svc.cluster.local/?tls=false"
# test>

# insert test data
kubectl run mongo-client --rm -it --image=mongo -- mongosh "mongodb+srv://mongodb-svc.default.svc.cluster.local/?tls=false" --eval "db.getSiblingDB('testdb').inventory.insertOne({ item: 'notebook', qty: 50, status: 'ready' })"
# {
#   acknowledged: true,
#   insertedId: ObjectId('6955e00d90775733ee8de666')
# }

# confirm
kubectl run mongo-client --rm -it --image=mongo -- mongosh "mongodb+srv://mongodb-svc.default.svc.cluster.local/?tls=false" --eval "db.getSiblingDB('testdb').inventory.find().pretty()"
# [
#   {
#     _id: ObjectId('6955e00d90775733ee8de666'),
#     item: 'notebook',
#     qty: 50,
#     status: 'ready'
#   },
# ]


kubectl run mongo-client --rm -it --image=mongo -- mongosh "mongodb+srv://mongodb-svc.default.svc.cluster.local/?tls=false" --eval "rs.hello().primary"
```

---

#### Pod Replacement

```sh
kubectl delete pod mongodb-1
# pod "mongodb-1" deleted from default namespace

# confirm pod replacement
kubectl get po
# NAME        READY   STATUS    RESTARTS   AGE
# mongodb-0   1/1     Running   0          84m
# mongodb-1   1/1     Running   0          22s
# mongodb-2   1/1     Running   0          84m
```

---

#### Deleting StatefulSet

```sh
# before deletion
kubectl get sts
# NAME      READY   AGE
# mongodb   3/3     17h

kubectl get pvc
# NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# data-mongodb-0   Bound    pvc-76d4f6d8-c326-478a-b1b8-9fa9bb1064f2   10Gi       RWO            hostpath       <unset>                 19h
# data-mongodb-1   Bound    pvc-4e72560b-6a6d-4cc2-8f40-5efd8e2ab85d   10Gi       RWO            hostpath       <unset>                 19h
# data-mongodb-2   Bound    pvc-5b70bd9e-f4d9-4ecd-a4f3-919e926dbe38   10Gi       RWO            hostpath       <unset>                 19h

kubectl get pv
# NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                    STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# pvc-4e72560b-6a6d-4cc2-8f40-5efd8e2ab85d   10Gi       RWO            Delete           Bound    default/data-mongodb-1   hostpath       <unset>                          19h
# pvc-5b70bd9e-f4d9-4ecd-a4f3-919e926dbe38   10Gi       RWO            Delete           Bound    default/data-mongodb-2   hostpath       <unset>                          19h
# pvc-76d4f6d8-c326-478a-b1b8-9fa9bb1064f2   10Gi       RWO            Delete           Bound    default/data-mongodb-0   hostpath       <unset>                          19h

kubectl delete sts mongodb
# statefulset.apps "mongodb" deleted from default namespace

# confirm
kubectl get sts
# No resources found in default namespace.

# confirm: pvc preserved
kubectl get pvc
# NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# data-mongodb-0   Bound    pvc-76d4f6d8-c326-478a-b1b8-9fa9bb1064f2   10Gi       RWO            hostpath       <unset>                 19h
# data-mongodb-1   Bound    pvc-4e72560b-6a6d-4cc2-8f40-5efd8e2ab85d   10Gi       RWO            hostpath       <unset>                 19h
# data-mongodb-2   Bound    pvc-5b70bd9e-f4d9-4ecd-a4f3-919e926dbe38   10Gi       RWO            hostpath       <unset>                 19h

kubectl get pv
# NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                    STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# pvc-4e72560b-6a6d-4cc2-8f40-5efd8e2ab85d   10Gi       RWO            Delete           Bound    default/data-mongodb-1   hostpath       <unset>                          20h
# pvc-5b70bd9e-f4d9-4ecd-a4f3-919e926dbe38   10Gi       RWO            Delete           Bound    default/data-mongodb-2   hostpath       <unset>                          20h
# pvc-76d4f6d8-c326-478a-b1b8-9fa9bb1064f2   10Gi       RWO            Delete           Bound    default/data-mongodb-0   hostpath       <unset>                          20h

# manually delete pvc
kubectl delete pvc data-mongodb-0 data-mongodb-1 data-mongodb-2
# persistentvolumeclaim "data-mongodb-0" deleted from default namespace
# persistentvolumeclaim "data-mongodb-1" deleted from default namespace
# persistentvolumeclaim "data-mongodb-2" deleted from default namespace

kubectl get pv
# No resources found

```

---

## Handling Node Failure

- if a node is disconnected, the pod of the `StatefulSet` that runs on the failed node will be marked as `Terminating` due to `Node is not ready`, even though it is still running on the node.

  - `StatefulSet Controller` will **not** delete and restart a new pod automatically.

---

#### Solution A: Manual Intervention

- `kubectl delete pod` command has no effect, because the pod is already `Terminating`
  - it works only when the `kubelet` on the failure node report the deleteion completes.
- `kubectl delete pod NAME --force --grace-period 0`: force to delete pod

  - should **confirm** the node **fails** and the pod get **deleted** **beforehand**.
  - `StatefulSet controller` then recreate the pod automatically.

- The recreated pod may not start.
  - Scenario 1: using local volume
    - the underlying `pv` is a **local volume on the failed node**.
    - recreated pod is `Pending`
      - `kubectl describe` for detailed events
        - `1 node had volume node affinity conflict.`
  - Scenario 2: using network attached volumes
    - Pod will be scheduled on **another node** but requires the `volume` to be **detached** from the **failed node**
    - recreated pod is `ContainerCreating`
    - events: `FailedAttachVolume`
    - solution: delete the old `pvc` and the `pod`
      - `kubectl delete pvc/PVC_NAME pod/POD_NAME`
      - then the controller recreates the PVC and pod, the replica will sync the data.

---

#### Solution B: Fix the disconnection

- When the node is back **online**, the **deletion** of the Pod is **complete**, and the **new** Pod is **created**.

---

## Scaling a StatefulSet

- When you **scale up** a `StatefulSet`, the `controller` creates both

  - a new `Pod`
  - a new `PersistentVolumeClaim`

- Scaling down

  - the `Pod` with the **highest ordinal number** is deleted first.
  - by default, the `PersistentVolumeClaims` are **preserved**
    - because the pvc deletion causes the bound `PersistentVolume` to be **recycled** or **deleted**, resulting in **data loss**.
    - can be change by `persistentVolumeClaimRetentionPolicy`
    - When the `sts` scale up again, the preserve pvc can be reattached.

![pic](./pic/sts_pvc.png)

- for some database, if scale down to 1, may lead to the Service is no longer available due to lack of `quorum`

---

### Pod Management Policy

- `podManagementPolicy` field

  - `OrderedReady`:
    - default,
    - **scale up/down** the `Pods` **sequentially**
      - wait for each pod ready before create the next pod
      - wait for graceful time to terminate the pod before the next one.
    - the policy **doesn’t apply** when you **delete** the `StatefulSet`.
    - possible scenario:
      - when the app has bug to be ready; the technology need multiple instance to be ready;
      - the `sts` get stuck because Pod is never ready
      - when debug by deletion, because it still wait a graceful termination, it could be the case it gets stuck during the deletion.
    - used depends on the technology; can prevent race condition or concurrent startup problem
  - `Parallel`:
    - scale up/down all Pods at the same time
      - no waiting

- Common use: `podManagementPolicy` + `minReadySeconds`

  - `minReadySeconds`: applied when scale up, can avoid race condition; not applied when scale down

- **NOTE**:
  - the policy **doesn't apply** for **`StatefulSet` Deletion**
  - **good practices**: scale down to **zero**, then **delete**

---

### PersistentVolumeClaim Retention Policy

- `persistentVolumeClaimRetentionPolicy` field:

  - specify the **retention policy** to be used during **scaledown** and when the `StatefulSet` is **deleted**.
  - `Retain`
    - default
    - pvc will be preserved.
  - `Delete`
    - can be deleted if the workload managed by the `StatefulSet` **never requires data to be preserved**

- Example

```yaml
spec:
  persistentVolumeClaimRetentionPolicy:
    whenScaled: Delete
    whenDeleted: Retain
```

- also can configure the `StatefulSetAutoDeletePVC` feature when creating cluster

- If you want to **delete** a `StatefulSet` but **keep** the `Pods` and the `PersistentVolumeClaims`, you can use the `--cascade=orphan` option.
  - In this case, the `PersistentVolumeClaims` will be **preserved** even if the **retention policy** is set to `Delete`.

---


