# Kubernetes - Labels and Selectors

[Back](../../index.md)

- [Kubernetes - Labels and Selectors](#kubernetes---labels-and-selectors)
  - [Labels](#labels)
    - [standard label keys](#standard-label-keys)
  - [Label Selectors](#label-selectors)
    - [equality-based selectors](#equality-based-selectors)
    - [set-based selectors](#set-based-selectors)
    - [Imperative Command](#imperative-command)
  - [Declarative](#declarative)
  - [Lab: Labels and Selector](#lab-labels-and-selector)
    - [Create pod with label](#create-pod-with-label)
    - [Filter pod](#filter-pod)
    - [Add label](#add-label)
    - [Remove label](#remove-label)
  - [`nodeSelector`: Scheduling pod by labels](#nodeselector-scheduling-pod-by-labels)
    - [Lab: Pod schaduling by labels](#lab-pod-schaduling-by-labels)
  - [Specify PV for a PVC with label](#specify-pv-for-a-pvc-with-label)
    - [Lab: PVC label](#lab-pvc-label)
  - [Fileter object by field selector](#fileter-object-by-field-selector)

---

## Labels

- `labels`

  - **Key–value pairs** attached to objects (Pods, Nodes, Services, Deployments, etc.).
  - used to add metadata that describes an object’s **attributes**.

- intended for identification, grouping, and selection,

- Characteristics:
  - Labels are **not unique**
    - many objects can share the same label
  - Labels are intended for **grouping and querying**, not for uniqueness.
  - Good for things like environment (dev, test, prod), version (v1, v2), or role (frontend, backend).

---

- Kubernetes components usually use **prefixed label keys**
  - e.g., `kubernetes.io/` and `k8s.io/`

```sh
kubectl get node -L kubernetes.io/arch
# NAME             STATUS   ROLES           AGE   VERSION   ARCH
# docker-desktop   Ready    control-plane   52d   v1.34.1   amd64
```

---

### standard label keys

- Well-known labels on Nodes and PersistentVolumes by kerbunetes

| Label key                          | Example value  | Applied to             | Description                                                   |
| ---------------------------------- | -------------- | ---------------------- | ------------------------------------------------------------- |
| `kubernetes.io/arch`               | `amd64`        | Node                   | The architecture of the node.                                 |
| `kubernetes.io/os`                 | `linux`        | Node                   | The operating system running on the node.                     |
| `kubernetes.io/hostname`           | `worker-node2` | Node                   | The node’s hostname.                                          |
| `topology.kubernetes.io/region`    | `eu-west3`     | Node, PersistentVolume | The region in which the node or persistent volume is located. |
| `topology.kubernetes.io/zone`      | `eu-west3-c`   | Node, PersistentVolume | The zone in which the node or persistent volume is located.   |
| `node.kubernetes.io/instance-type` | `micro-1`      | Node                   | The node instance type.                                       |

- Recommended labels

| Label                          | Example           | Description                                                              |
| ------------------------------ | ----------------- | ------------------------------------------------------------------------ |
| `app.kubernetes.io/name`       | `quotes`          | The name of the entire application.                                      |
| `app.kubernetes.io/instance`   | `quotes-foo`      | The name of the application instance to identify the purpose.            |
| `app.kubernetes.io/component`  | `database`        | The role in the application **architecture**.                            |
| `app.kubernetes.io/part-of`    | `kubia-demo`      | The name of the **application suite** to which this application belongs. |
| `app.kubernetes.io/version`    | `1.0.0`           | The version of the application.                                          |
| `app.kubernetes.io/managed-by` | `quotes-operator` | The **tool** that manages the deployment and update of this application. |

---

## Label Selectors

- A **query** that allows Kubernetes (or you) to **select a group** of objects based on labels.
- Use Case: Services, ReplicaSets, Deployments, and kubectl commands rely heavily on selectors.

- can combine multiple selectors

  - e.g., `app=quote,rel=canary`

- two types of label selectors:
  - `equality-based selectors`
  - `set-based selectors`

---

### equality-based selectors

- `equality-based selector`
  - filter objects based on **whether the value** of a particular label is **equal to or not equal to** a particular **value**.
  - e.g.,
    - `app=quote`
    - `app!=quote`

---

### set-based selectors

- `set-based selectors`
  - filter objects by sepcify:
    - a set of **values** that a particular label **must have**: `app in (quiz, quote)`
    - a set of **values** that a particular label **must not have**: `app notin (kiada)`
    - a particular **label key** that should be **present** in the object’s labels: `'env'`
    - a particular **label** key that should **not be present** in the object’s labels;: `'!env'`

---

### Imperative Command

- manage label on object

| CMD                                                   | DESC                              |
| ----------------------------------------------------- | --------------------------------- |
| `kubectl label node node_name size=large`             | Add or update a label on a node   |
| `kubectl label pod mypod env=prod`                    | Add a label on a pod              |
| `kubectl label pod --all env=prod`                    | Add a label on all pods           |
| `kubectl label pod mypod app=web tier=frontend`       | Add multiple labels on a pod      |
| `kubectl label pod mypod env=dev app=api --overwrite` | Update multiple labels on a pod   |
| `kubectl label pod mypod env-`                        | Remove a label from a pod         |
| `kubectl label pod --all env-`                        | Remove a label from all pods      |
| `kubectl label pod mypod tier- app-`                  | Remove multiple labels from a pod |

- Filter

| CMD                                                     | DESC                                     |
| ------------------------------------------------------- | ---------------------------------------- |
| `kubectl get pods --show-labels`                        | Show all pods with all labels            |
| `kubectl get pods -L key1,key2`                         | Show all pods with label keys in columns |
| `kubectl get pods -l env=prod --no-headers \| wc -l`    | Count number of pods with a given label  |
| `kubectl get all -l 'env'`                              | Filter all if have a label               |
| `kubectl get all -l '!env'`                             | Filter all if not have a label           |
| `kubectl get pods -l '!env'`                            | Filter pod if not have a label           |
| `kubectl get pods -l env=production`                    | Filter pod if label equal to a value     |
| `kubectl get pods -l env!=production`                   | Filter pod if label not equal to a value |
| `kubectl get pods -l 'env in (production, staging)'`    | Filter pod if label in a set.            |
| `kubectl get pods -l 'env notin (dev)'`                 | Filter pod if label not in a set.        |
| `kubectl run nginx --image=nginx -l "app=web,env=prod"` | Create pod with label                    |
| `kubectl delete pod -l "app=web,env=prod"`              | Delete pod with label                    |

---

## Declarative

- Label

```yaml
aptVersion: v1
kind: Pod
metadata:
  labels:
    key: value
spec:
```

- Selector

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
    tier: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

---

## Lab: Labels and Selector

### Create pod with label

```sh
kubectl run nginx-prod --image=nginx -l "app=web,env=prod"
kubectl run nginx-dev --image=nginx -l "app=web,env=dev"
kubectl run nginx-staging --image=nginx -l "app=web,env=staging"
```

### Filter pod

```sh
kubectl get pod
# NAME            READY   STATUS    RESTARTS   AGE
# nginx-dev       1/1     Running   0          14s
# nginx-prod      1/1     Running   0          14s
# nginx-staging   1/1     Running   0          9s

kubectl get pods --show-labels
# NAME            READY   STATUS    RESTARTS   AGE   LABELS
# nginx-dev       1/1     Running   0          13m   app=web,env=dev
# nginx-prod      1/1     Running   0          13m   app=web,env=prod
# nginx-staging   1/1     Running   0          13m   app=web,env=staging

kubectl get pod -l "app"
# NAME            READY   STATUS    RESTARTS   AGE
# nginx-dev       1/1     Running   0          3m43s
# nginx-prod      1/1     Running   0          3m43s
# nginx-staging   1/1     Running   0          3m38s

kubectl get pod -l "db"
# No resources found in default namespace.

kubectl get pod -l "!db"
# NAME            READY   STATUS    RESTARTS   AGE
# nginx-dev       1/1     Running   0          4m19s
# nginx-prod      1/1     Running   0          4m19s
# nginx-staging   1/1     Running   0          4m14s

kubectl get pod -l "env=prod"
# NAME         READY   STATUS    RESTARTS   AGE
# nginx-prod   1/1     Running   0          52s

kubectl get pod -l "env!=prod"
# NAME            READY   STATUS    RESTARTS   AGE
# nginx-dev       1/1     Running   0          6m
# nginx-staging   1/1     Running   0          5m55s

kubectl get pod -l "app=web,env=dev"
# NAME        READY   STATUS    RESTARTS   AGE
# nginx-dev   1/1     Running   0          10m

kubectl get pods -l "env in (dev, staging)"
# NAME            READY   STATUS    RESTARTS   AGE
# nginx-dev       1/1     Running   0          13m
# nginx-staging   1/1     Running   0          13m

kubectl get pods -l "env notin (dev, staging)"
# NAME         READY   STATUS    RESTARTS   AGE
# nginx-prod   1/1     Running   0          15m

kubectl get pods -l "env in (dev), app in (web)" --show-labels
# NAME        READY   STATUS    RESTARTS   AGE   LABELS
# nginx-dev   1/1     Running   0          19m   app=web,env=dev
```

### Add label

```sh
# add label
kubectl label pod nginx-dev local=true
# pod/nginx-dev labeled

kubectl get pod nginx-dev --show-labels
# NAME        READY   STATUS    RESTARTS   AGE   LABELS
# nginx-dev   1/1     Running   0          17m   app=web,env=dev,local=true

# remove label
kubectl label pod nginx-dev local-
# pod/nginx-dev unlabeled

kubectl get pod nginx-dev --show-labels
# NAME        READY   STATUS    RESTARTS   AGE   LABELS
# nginx-dev   1/1     Running   0          17m   app=web,env=dev
```

### Remove label

```sh
kubectl delete pod -l app=web
# pod "nginx-dev" deleted
# pod "nginx-prod" deleted
# pod "nginx-staging" deleted
```

---


## `nodeSelector`: Scheduling pod by labels

- In production, it is common to control pod scheduling by using lables
- `nodeSelector` field:
  - only supports specifying an equality-based label selector.

---

### Lab: Pod schaduling by labels

- front-end pod scheduled in front-end nodes
- back-end pod scheduled in back-end nodes

```sh
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   30d   v1.33.6
# node01         Ready    <none>          30d   v1.33.6
# node02         Ready    <none>          30d   v1.33.6

kubectl label node node01 node-role=front-end
# node/node01 labeled

# confirm
kubectl get node -L node-role
# NAME           STATUS   ROLES           AGE   VERSION   NODE-ROLE
# controlplane   Ready    control-plane   30d   v1.33.6
# node01         Ready    <none>          30d   v1.33.6   front-end
# node02         Ready    <none>          30d   v1.33.6
```

```yaml
# demo-schedule-label-pod-front.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-schedule-label-pod-front
spec:
  nodeSelector:
    node-role: front-end
  containers:
    - name: nginx
      image: nginx
```

```sh
kubectl apply -f demo-schedule-label-pod-front.yaml
# pod/demo-schedule-label-pod-front created

kubectl get pod demo-schedule-label-pod-front -o wide
# NAME                            READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# demo-schedule-label-pod-front   1/1     Running   0          72s   10.244.1.11   node01   <none>           <none>
```

---

## Specify PV for a PVC with label

- can specify a `label selector` in the `PersistentVolumeClaim` object definition to indicate which `persistent volumes` Kubernetes should consider for binding.

  - **Without** the `label selector`, **any** available `persistent volume` that matches the **capacity** and **access modes** specified in the claim will be **bound**.
  - If the `claim` specifies a `label selector`, Kubernetes also **checks the labels** of the available `persistent volumes` and **binds** the claim to a volume **only** if its labels **match** the label selector in the claim
  - supports both `equality-based` and `set-based selectors`

- match a single label: `pvc.spec.selector.matchLabels`
- match multiple labels: `pvc.spec.selector.matchExpressions`

```yaml
spec:
  matchExpressions:
    - key: type
      operator: NotIn
      values:
        - ssd
    - key: age
      operator: In
      values:
        - old
        - very-old
```

---

### Lab: PVC label

- Label node

```sh
kubectl label node node02 ssd=""
# node/node02 labeled

kubectl get node -l ssd
# NAME     STATUS   ROLES    AGE   VERSION
# node02   Ready    <none>   32d   v1.33.6
```

---

- Create pv match node label

```yaml
# demo-pvc-label-pv.yaml
kind: PersistentVolume
apiVersion: v1
metadata:
  name: demo-pvc-label-pv
  labels:
    type: ssd
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
            - key: ssd
              operator: Exists
```

```sh
kubectl apply -f demo-pvc-label-pv.yaml
# persistentvolume/demo-pvc-label-pv created

# confirm
kubectl get pv -l type=ssd
# NAME                CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# demo-pvc-label-pv   1Gi        RWO            Retain           Available           sc-local       <unset>                          18s
```

```yaml
# demo-pvc-label-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc-label-pvc
spec:
  selector: # seletor
    matchLabels:
      type: ssd
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
```

```sh
kubectl apply -f demo-pvc-label-pvc.yaml
# persistentvolumeclaim/demo-pvc-label-pvc created

```

## Fileter object by field selector

- `metadata.name` and `metadata.namespace` fields are always supported for all object types
- `field selectors` support the equal (`=` or `==`) and not equal (`!=`) operator
- multiple field selectors: `field1=value1,field2=value2`

- example

```sh
# create pods
kubectl run nginx --image=nginx
# pod/nginx created

kubectl run busybox-succeed --image=busybox --restart=Never sleep 10
# pod/busybox created

kubectl run busybox-fail --image=busybox --restart=Never exit 1
# pod/busybox-exit created

kubectl get pod
# NAME              READY   STATUS               RESTARTS   AGE
# busybox-fail      0/1     ContainerCannotRun   0          11s
# busybox-succeed   0/1     Completed            0          16s
# nginx             1/1     Running              0          24s

kubectl get pod --field-selector status.phase=Running
# NAME    READY   STATUS    RESTARTS   AGE
# nginx   1/1     Running   0          38s


kubectl get pods --field-selector status.phase=Running --all-namespaces
# NAMESPACE              NAME                                                    READY   STATUS    RESTARTS        AGE
# default                nginx                                                   1/1     Running   0               19m
# kube-system            coredns-66bc5c9577-4mvht                                1/1     Running   67 (36h ago)    52d
# kube-system            coredns-66bc5c9577-w2rm7                                1/1     Running   67 (36h ago)    52d
# kube-system            etcd-docker-desktop                                     1/1     Running   67 (36h ago)    52d
# kube-system            kube-apiserver-docker-desktop                           1/1     Running   67 (36h ago)    52d
# kube-system            kube-controller-manager-docker-desktop                  1/1     Running   67 (36h ago)    52d
# kube-system            kube-proxy-vs9tn                                        1/1     Running   67 (36h ago)    52d
# kube-system            kube-scheduler-docker-desktop                           1/1     Running   69 (36h ago)    52d
# kube-system            storage-provisioner                                     1/1     Running   135 (36h ago)   52d
# kube-system            vpnkit-controller                                       1/1     Running   67 (36h ago)    52d
# kubernetes-dashboard   dashboard-metrics-scraper-6866d44d4c-xdxw2              1/1     Running   4 (36h ago)     7d22h
# kubernetes-dashboard   kubernetes-dashboard-6d56bb967c-w64wb                   1/1     Running   4 (36h ago)     7d22h
# kubernetes-dashboard   kubernetes-dashboard-api-cdd8b755b-ttxh9                1/1     Running   7 (36h ago)     7d23h
# kubernetes-dashboard   kubernetes-dashboard-auth-797bdfd56f-4skj2              1/1     Running   4 (36h ago)     7d23h
# kubernetes-dashboard   kubernetes-dashboard-kong-9849c64bd-lg4z9               1/1     Running   4 (36h ago)     7d23h
# kubernetes-dashboard   kubernetes-dashboard-metrics-scraper-7685fd8b77-mcvfz   1/1     Running   4 (36h ago)     7d23h
# kubernetes-dashboard   kubernetes-dashboard-web-5c9f966b98-pcdhk               1/1     Running   4 (36h ago)     7d23h

kubectl get pods --field-selector status.phase!=Running
# NAME              READY   STATUS               RESTARTS   AGE
# busybox-fail      0/1     ContainerCannotRun   0          18m
# busybox-succeed   0/1     Completed            0          18m


kubectl get pod --field-selector status.phase=Succeeded
# NAME              READY   STATUS      RESTARTS   AGE
# busybox-succeed   0/1     Completed   0          40s

kubectl get pod --field-selector status.phase=Failed
# NAME           READY   STATUS               RESTARTS   AGE
# busybox-fail   0/1     ContainerCannotRun   0          49s

kubectl get pod --field-selector metadata.name=nginx
# NAME    READY   STATUS    RESTARTS   AGE
# nginx   1/1     Running   0          7m37s

kubectl get pod --field-selector metadata.namespace=default
# NAME              READY   STATUS               RESTARTS   AGE
# busybox-fail      0/1     ContainerCannotRun   0          7m50s
# busybox-succeed   0/1     Completed            0          7m55s
# nginx             1/1     Running              0          8m3s

kubectl get pod --field-selector spec.nodeName=docker-desktop
# NAME              READY   STATUS               RESTARTS   AGE
# busybox-fail      0/1     ContainerCannotRun   0          11m
# busybox-succeed   0/1     Completed            0          11m
# nginx             1/1     Running              0          11m

```
