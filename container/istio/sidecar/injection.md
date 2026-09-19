# Istio Sidecar - Sidecar injection

[Back](../index.md)

- [Istio Sidecar - Sidecar injection](#istio-sidecar---sidecar-injection)
  - [Sidecar injection](#sidecar-injection)
    - [Lab: Sidecar injection namespace](#lab-sidecar-injection-namespace)
    - [Lab: Sidecar injection simple pod](#lab-sidecar-injection-simple-pod)
    - [Lab: inject with `istioctl`](#lab-inject-with-istioctl)

---

## Sidecar injection

- mesh pod runs an `Istio sidecar proxy`.
- 2 ways to inject sidecar:
  - enable sidecar injection in namespace
    - label: `istio-injection=enabled`
  - using `istioctl` command

---

### Lab: Sidecar injection namespace

```sh
# ##############################
# before injection
# ##############################
# create deploy
k create deploy before --image=nginx --replicas=2
# deployment.apps/before created

# confirm
k get po -l app=before
# NAME                      READY   STATUS    RESTARTS   AGE
# before-6cdfd6fc76-cx55w   1/1     Running   0          19s
# before-6cdfd6fc76-sb5dm   1/1     Running   0          19s

# ##############################
# enable injection
# ##############################
kubectl label namespace default istio-injection=enabled --overwrite
# namespace/default labeled

# confirm
kubectl get namespace default --show-labels
# NAME      STATUS   AGE     LABELS
# default   Active   5d16h   istio-injection=enabled,kubernetes.io/metadata.name=default

# ##############################
# Restart deploy
# ##############################
k get po -l app=before
# NAME                      READY   STATUS     RESTARTS   AGE
# before-6cdfd6fc76-cx55w   1/1     Running    0          96s
# before-6cdfd6fc76-sb5dm   1/1     Running    0          96s

k rollout restart deploy before
# deployment.apps/before restarted

# confirm
k get po -l app=before
# NAME                      READY   STATUS    RESTARTS   AGE
# before-7d59fb6c55-nzhwx   2/2     Running   0          11s
# before-7d59fb6c55-rq8h4   2/2     Running   0          48s

# ##############################
# new deploy
# ##############################
# create deploy
k create deploy after --image=nginx --replicas=2
# deployment.apps/after created

# confirm
k get po -l app=after
# NAME                     READY   STATUS    RESTARTS   AGE
# after-7b76c758b9-9n77s   2/2     Running   0          15s
# after-7b76c758b9-xtt4z   2/2     Running   0          14s
```

---

### Lab: Sidecar injection simple pod

```sh
k create ns app
# namespace/app created

k run non-inject --image=nginx -n app
# pod/non-inject created

k get po -n app
# NAME         READY   STATUS    RESTARTS   AGE
# non-inject   1/1     Running   0          17s

k run injected --image=nginx -n app -l sidecar.istio.io/inject="true"
# pod/injected created

k get po -n app
# NAME         READY   STATUS    RESTARTS   AGE
# injected     2/2     Running   0          14s
# non-inject   1/1     Running   0          44s
```

---

### Lab: inject with `istioctl`

```sh
cat <<EOF | istioctl kube-inject -f - | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: istioctl-app
  namespace: app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: istioctl-app
  template:
    metadata:
      labels:
        app: istioctl-app
    spec:
      containers:
      - name: istioctl-app
        image: nginx
EOF
# deployment.apps/istioctl-app created

k get po -n app -l app=istioctl-app
# NAME                            READY   STATUS    RESTARTS   AGE
# istioctl-app-5954846c75-dtzpm   2/2     Running   0          33s

```
