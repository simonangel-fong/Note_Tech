# Kubernetes: Storage - Use `secret` as Environment Variable

[Back](../../index.md)

- [Kubernetes: Storage - Use `secret` as Environment Variable](#kubernetes-storage---use-secret-as-environment-variable)
  - [Use `secret` as Environment Variables](#use-secret-as-environment-variables)
  - [Lab: Use Secret as Environment variables](#lab-use-secret-as-environment-variables)
    - [Create Secret](#create-secret)
    - [Import a Key from one Secret](#import-a-key-from-one-secret)
    - [Bulk Import](#bulk-import)

---

## Use `secret` as Environment Variables

- Note that exposure of `secret` as env var could be a risk.
  - recommend to use `secret volume`

```yaml
# specify keys
spec:
  containers:
  - name: busybox
    env:
    - name: TLS_CERT
        valueFrom:
          secretKeyRef:
            name: tls-secret
            key: tls.crt

```

---

## Lab: Use Secret as Environment variables

### Create Secret

```sh
kubectl create secret generic app-secret --from-literal=DB_USER=user --from-literal=DB_PWD=pwd
# secret/app-secret created
```

---

### Import a Key from one Secret

- `pod-secret-key.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-secret-key
spec:
  containers:
    - name: myapp
      command: ["sh", "-c", "env | grep -E 'DB_USER|DB_PWD' && sleep 2000"]
      image: busybox:latest
      env:
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: DB_USER
```

```sh
kubectl create -f pod-secret-key.yaml
# pod/pod-secret-key created

kubectl get pod
# NAME             READY   STATUS    RESTARTS   AGE
# pod-secret-key   1/1     Running   0          18s

kubectl logs pod/pod-secret-key
# DB_USER=user

kubectl delete pod/pod-secret-key
# pod "pod-secret-key" deleted from default namespace
```

---

### Bulk Import

- `pod-secret-bulk.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-secret-bulk
spec:
  containers:
    - name: myapp
      command: ["sh", "-c", "env | grep -E 'DB_USER|DB_PWD' && sleep 2000"]
      image: busybox:latest
      envFrom:
        - secretRef:
            name: app-secret
```

```sh
kubectl create -f pod-secret-bulk.yaml
# pod/pod-secret-bulk created

kubectl get pod
# NAME              READY   STATUS    RESTARTS   AGE
# pod-secret-bulk   1/1     Running   0          13s

kubectl logs pod/pod-secret-bulk
# DB_PWD=pwd
# DB_USER=user

kubectl delete pod/pod-secret-bulk
# pod "pod-secret-bulk" deleted from default namespace
```

---
