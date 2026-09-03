# Kubernetes - `kind`

[Back](../../index.md)

- [Kubernetes - `kind`](#kubernetes---kind)
  - [Install `kind`](#install-kind)
  - [Create Cluster](#create-cluster)
    - [with default config](#with-default-config)
    - [with cluster name](#with-cluster-name)
    - [with specify manifest](#with-specify-manifest)

---

## Install `kind`

- ref: https://kind.sigs.k8s.io/

```sh
# PowerShell as an Administrator
choco install kind

kind --version
# kind version 0.31.0

# linux
# For AMD64 / x86_64
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.33.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

---

## Create Cluster

### with default config

- require docker spin up

```sh
kind create cluster
# Creating cluster "kind" ...
#  • Ensuring node image (kindest/node:v1.35.0) 🖼  ...
#  ✓ Ensuring node image (kindest/node:v1.35.0) 🖼
#  • Preparing nodes 📦   ...
#  ✓ Preparing nodes 📦
#  • Writing configuration 📜  ...
#  ✓ Writing configuration 📜
#  • Starting control-plane 🕹️  ...
#  ✓ Starting control-plane 🕹️
#  • Installing CNI 🔌  ...
#  ✓ Installing CNI 🔌
#  • Installing StorageClass 💾  ...
#  ✓ Installing StorageClass 💾
# Set kubectl context to "kind-kind"
# You can now use your cluster with:

# kubectl cluster-info --context kind-kind

# Thanks for using kind! 😊

# confirm
kind get clusters
# kind

kubectl cluster-info --context kind-kind
# Kubernetes control plane is running at https://127.0.0.1:8095
# CoreDNS is running at https://127.0.0.1:8095/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

kubectl get node
# NAME                 STATUS   ROLES           AGE   VERSION
# kind-control-plane   Ready    control-plane   56s   v1.35.0

kubectl get sc
# NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
# standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  2m28s

# deploy sample app
kubectl run demo-web --image=nginx
# pod/demo-web created

kubectl get po
# NAME       READY   STATUS    RESTARTS   AGE
# demo-web   1/1     Running   0          16s

# clean up
kind delete cluster
# Deleting cluster "kind" ...
# Deleted nodes: ["kind-control-plane"]

kubectl get node
```

---

### with cluster name

```sh
# create with name
kind create cluster -n mycluster

# confirm
kind get clusters
# mycluster

# remove
kind delete cluster -n mycluster
# Deleting cluster "mycluster" ...
# Deleted nodes: ["mycluster-control-plane"]
```

---

### with specify manifest

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 8080
        protocol: TCP
      - containerPort: 443
        hostPort: 8443
        protocol: TCP
  - role: worker
  - role: worker
```

```sh
kind create cluster --name mycluster --config kind-config.yaml
# Creating cluster "mycluster" ...
#  ✓ Ensuring node image (kindest/node:v1.37.0) 🖼️
#  ✓ Preparing nodes 📦 📦 📦
#  ✓ Writing configuration 📜
#  ✓ Starting control-plane 🕹️
#  ✓ Installing CNI 🔌
#  ✓ Installing StorageClass 💾
#  ✓ Joining worker nodes 🚜
# Set kubectl context to "kind-mycluster"
# You can now use your cluster with:

# kubectl cluster-info --context kind-mycluster

# Have a nice day! 👋

# confirm
kind get clusters
# mycluster

kubectl get nodes --show-labels | grep ingress
# mycluster-control-plane   Ready    control-plane   114s   v1.37.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,ingress-ready=true,kubernetes.io/arch=amd64,kubernetes.io/hostname=mycluster-control-plane,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=,node.kubernetes.io/exclude-from-external-load-balancers=
```

- install ingress

```sh
# install ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# confirm
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s
# pod/ingress-nginx-controller-596f5b6bcf-7k26l condition met

kubectl get pods -n ingress-nginx -o wide
kubectl get svc -n ingress-nginx
```

- install demo

```yaml
# nginx-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-nginx
  template:
    metadata:
      labels:
        app: my-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: my-nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
spec:
  rules:
    - host: nginx.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
```

```sh
# apply
kubectl apply -f nginx-app.yaml
# deployment.apps/nginx-deployment created
# service/nginx-service created
# ingress.networking.k8s.io/nginx-ingress created

# test access
curl -H "Host: nginx.local" http://localhost:8080/
```
