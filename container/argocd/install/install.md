# ArgoCD: Installation

[Back](../index.md)

- [ArgoCD: Installation](#argocd-installation)
  - [Installation](#installation)
  - [Exposing ArgoCD Server](#exposing-argocd-server)
  - [Install ArgoCD CLI](#install-argocd-cli)

---

## Installation

- ref:
  - https://argo-cd.readthedocs.io/en/latest/operator-manual/installation/
  - helm: https://github.com/argoproj/argo-helm
- Env: Docker Desktop

```sh
kubectl create ns argocd
# namespace/argocd created

helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
# Hang tight while we grab the latest from your chart repositories...
# ...Successfully got an update from the "argo" chart repository
# Update Complete. ⎈Happy Helming!⎈

helm install argocd argo/argo-cd -n argocd --create-namespace

kubectl get po -n argocd
# NAME                                                READY   STATUS    RESTARTS   AGE
# argocd-application-controller-0                     1/1     Running   0          5m1s
# argocd-applicationset-controller-7dc6bb5fcb-gmlzt   1/1     Running   0          5m1s
# argocd-dex-server-69b96cbcdd-4ftrj                  1/1     Running   0          5m1s
# argocd-notifications-controller-5996578cc4-2whqm    1/1     Running   0          5m1s
# argocd-redis-65f4b95795-xrpmc                       1/1     Running   0          5m1s
# argocd-repo-server-577479c9bd-b4q8b                 1/1     Running   0          5m1s
# argocd-server-7dcc98b5cb-95mzp                      1/1     Running   0          5m1s

kubectl get svc -n argocd
# NAME                               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
# argocd-applicationset-controller   ClusterIP   10.111.218.255   <none>        7000/TCP            5m27s
# argocd-dex-server                  ClusterIP   10.99.221.148    <none>        5556/TCP,5557/TCP   5m27s
# argocd-redis                       ClusterIP   10.105.175.250   <none>        6379/TCP            5m27s
# argocd-repo-server                 ClusterIP   10.98.64.246     <none>        8081/TCP            5m27s
# argocd-server                      ClusterIP   10.101.163.51    <none>        80/TCP,443/TCP      5m27s

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

---

## Exposing ArgoCD Server

- By default ArgoCD server is **not exposed** with external endpoint.
- Expose by using:
  - **Service**: `LoadBalancer`
    - Change the argocd-server service type to LoadBalancer
  - `Ingress`:
    - Use your preferred ingress controller
    - Create an ingress resource that point into argocd-server service.
  - **Port-forward**:
    - simply you can use this to access locally on your machine
    - `kubectl port-forward svc/argocd-server -n argocd 8080:443`

---

## Install ArgoCD CLI

- ref:
  - https://argo-cd.readthedocs.io/en/stable/cli_installation/#archlinux

```sh
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

argocd version
# argocd: v3.3.8+7ae7d2c
#   BuildDate: 2026-04-21T17:45:55Z
#   GitCommit: 7ae7d2cc723f5408b080a31263e705198af08613
#   GitTreeState: clean
#   GoVersion: go1.25.5
#   Compiler: gc
#   Platform: linux/amd64
# {"level":"fatal","msg":"Argo CD server address unspecified","time":"2026-04-27T15:28:00-04:00"}
```

- login

```sh
# port forward 
kubectl port-forward svc/argocd-server -n argocd 8080:443
# login
argocd login localhost:8080
# WARNING: server certificate had error: error creating connection: tls: failed to verify certificate: x509: certificate signed by unknown authority. Proceed insecurely (y/n)? y
# Username: admin
# Password:
# 'admin:login' logged in successfully
# Context 'localhost:8080' updated

```
