# Kubernetes - Labels and Selectors

[Back](../../index.md)

- [Kubernetes - Labels and Selectors](#kubernetes---labels-and-selectors)
  - [Labels](#labels)
  - [Label Selectors](#label-selectors)
    - [Imperative Command](#imperative-command)
  - [Declarative](#declarative)
  - [Lab: Labels and Selector](#lab-labels-and-selector)
    - [Create pod with label](#create-pod-with-label)
    - [Filter pod](#filter-pod)
    - [Add label](#add-label)
    - [Remove label](#remove-label)
  - [Annotation](#annotation)

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

## Label Selectors

- A **query** that allows Kubernetes (or you) to **select a group** of objects based on labels.
- Use Case: Services, ReplicaSets, Deployments, and kubectl commands rely heavily on selectors.

---

### Imperative Command

- Filter

| CMD                                                     | DESC                                     |
| ------------------------------------------------------- | ---------------------------------------- |
| `kubectl get all -l '!env'`                             | Filter all if not have a label           |
| `kubectl get pods -l '!env'`                            | Filter pod if not have a label           |
| `kubectl get pods -l env=production`                    | Filter pod if label equal to a value     |
| `kubectl get pods -l env!=production`                   | Filter pod if label not equal to a value |
| `kubectl get pods -l 'env in (production, staging)'`    | Filter pod if label in a set.            |
| `kubectl get pods -l 'env notin (dev)'`                 | Filter pod if label not in a set.        |
| `kubectl run nginx --image=nginx -l "app=web,env=prod"` | Create pod with label                    |
| `kubectl delete pod -l "app=web,env=prod"`              | Delete pod with label                    |
| `kubectl label pod mypod env=production`                | Add or update a label                    |
| `kubectl label pod mypod env-`                          | Remove a label                           |

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

## Annotation

- `Annotation`
  - **a key–value pair of metadata** attached to an object that is intended only for **information storage and reference**
  - not for identification, grouping, or selection.
