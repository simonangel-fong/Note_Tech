# Kubernetes: Storage - Use `ConfigMap` as Environment Variable

[Back](../../index.md)

- [Kubernetes: Storage - Use `ConfigMap` as Environment Variable](#kubernetes-storage---use-configmap-as-environment-variable)
  - [Using Configmaps as environment variables](#using-configmaps-as-environment-variables)
  - [Lab: Use ConfigMap as Environment variables](#lab-use-configmap-as-environment-variables)
    - [Create ConfigMap](#create-configmap)
    - [Bulk Import](#bulk-import)
    - [Import a Key](#import-a-key)

---

## Using Configmaps as environment variables

- Import value

```yaml
kind: Pod
spec:
  containers:
    - name: app
      env:
        - name: APP_MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MODE
```

---

- bulk import:

```yaml
kind: Pod
spec:
  containers:
    - name: app
      envFrom:
        - configMapRef:
            name: mapp-config
```

---

## Lab: Use ConfigMap as Environment variables

### Create ConfigMap

```sh
kubectl create cm app-config --from-literal=APP_MODE=prod --from-literal=LOG_LEVEL=info
# configmap/app-config created
```

---

### Bulk Import

- `pod-conf-bulk.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-conf-bulk
spec:
  containers:
    - name: myapp
      command: ["sh", "-c", "env | grep -E 'APP_MODE|LOG_LEVEL' && sleep 2000"]
      image: busybox:latest
      envFrom:
        - configMapRef:
            name: app-config
```

```sh
kubectl create -f pod-conf-bulk.yaml
# pod/pod-conf-bulk created

kubectl get pod
# NAME            READY   STATUS    RESTARTS   AGE
# pod-conf-bulk   1/1     Running   0          13s

kubectl logs pod/pod-conf-bulk
# APP_MODE=prod
# LOG_LEVEL=info

kubectl delete pod/pod-conf-bulk
# pod "pod-conf-bulk" deleted from default namespace
```

---

### Import a Key

- `pod-conf-key.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-conf-key
spec:
  containers:
    - name: myapp
      image: busybox
      command: ["sh", "-c", "env | grep -E 'APP_MODE|LOG_LEVEL' && sleep 2000"]
      env:
        - name: APP_MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MODE
```

```sh
kubectl create -f pod-conf-key.yaml
# pod/pod-conf-key created

kubectl get pod
# NAME            READY   STATUS    RESTARTS   AGE
# pod-conf-bulk   1/1     Running   0          13s

kubectl logs pod/pod-conf-key
# APP_MODE=prod

kubectl delete pod/pod-conf-key
# pod "pod-conf-key" deleted from default namespace
```

---
